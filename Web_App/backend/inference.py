import pandas as pd
import numpy as np
import os
import joblib
from netcdf_engine import NetCDFProcessor

class ALAZEngine:
    def __init__(self, base_dir=r"C:\Users\Yusuf\Desktop\Tez-bolgesel"):
        self.base_dir = base_dir
        self.nc_engine = NetCDFProcessor(base_dir)
        self.cache_dir = os.path.join(base_dir, "Web_App", "cache", "alaz")
        os.makedirs(self.cache_dir, exist_ok=True)
        
        self.static_db = None
        self.events_db = None
        self.m8_ndvi = None
        self.models = {}
        self.features = {}
        self._load_assets()

    def _load_assets(self):
        print("[ALAZ] M2 (Topoloji), M3 (Yangın Geçmişi) ve M8 (NDVI) belleğe alınıyor...")
        self.static_db = pd.read_parquet(os.path.join(self.base_dir, "Ara_dosyalar", "M2_gridler_bolge.parquet"))
        
        # 1. Yangın Geçmişi (days_since_last_fire)
        m3_path = os.path.join(self.base_dir, "Ara_dosyalar", "M3_yangin_pozitifler.parquet")
        if os.path.exists(m3_path):
            df_m3 = pd.read_parquet(m3_path, columns=['GRID_ID', 'Tarih'])
            df_m3['Tarih'] = pd.to_datetime(df_m3['Tarih'])
            self.events_db = df_m3.sort_values('Tarih')
            
        # 2. NDVI (GEE'nin Web Alternatifi - Tarihsel Aylık Medyan)
        m8_path = os.path.join(self.base_dir, "Ara_dosyalar", "M8_final_dataset.parquet")
        if os.path.exists(m8_path):
            df_m8 = pd.read_parquet(m8_path, columns=['GRID_ID', 'Tarih', 'NDVI'])
            df_m8['month'] = pd.to_datetime(df_m8['Tarih']).dt.month
            # Her gridin yıl bağımsız o aydaki NDVI medyanını sözlüğe çevir (Hız için)
            self.m8_ndvi = df_m8.groupby(['GRID_ID', 'month'])['NDVI'].median().to_dict()
            
        # 3. Model ve Pruned Features
        models_dir = os.path.join(self.base_dir, "Sonuclar", "M13")
        self.models = joblib.load(os.path.join(models_dir, "M13_calibrated_regional_models.joblib"))
        self.features = joblib.load(os.path.join(self.base_dir, "Sonuclar", "M12", "M12_pruned_feature_sets.joblib"))

    def compute_ml_features(self, df_fwi, target_date_str):
        print(f"[ALAZ] Makine Öğrenmesi (Sentetik) özellikleri üretiliyor: {target_date_str}")
        dt = pd.to_datetime(target_date_str)
        month = dt.month
        
        # Topoloji (Static M2) ile FWI birleştir
        df_ml = pd.merge(df_fwi, self.static_db, on="GRID_ID", how="inner")
        
        # A) NDVI Atama (Medyan Imputation)
        if self.m8_ndvi is not None:
            df_ml['NDVI'] = df_ml['GRID_ID'].map(lambda g: self.m8_ndvi.get((g, month), np.nan))
            df_ml['NDVI'].fillna(df_ml['NDVI'].median(), inplace=True)
            
        # B) I_FWI_x_NDVI (Etkileşim)
        if 'NDVI' in df_ml.columns and 'FWI_Final' in df_ml.columns:
            df_ml['I_FWI_x_NDVI'] = df_ml['FWI_Final'] * df_ml['NDVI']
            
        # C) last_fire_days (Mantık: O tarihten önce yanmış mı?)
        if self.events_db is not None:
             # O günden önceki tüm yangınları alıp, grid bazında max tarih
             past_fires = self.events_db[self.events_db['Tarih'] < dt]
             last_fire_dict = past_fires.groupby('GRID_ID')['Tarih'].max().to_dict()
             
             base_date = pd.Timestamp('2008-01-01')
             def calc_days(gid):
                 if gid in last_fire_dict:
                     return (dt - last_fire_dict[gid]).days
                 return (dt - base_date).days
                     
             df_ml['days_since_last_fire'] = df_ml['GRID_ID'].apply(calc_days)
             
        return df_ml

    def run_prediction(self, date_str):
        """API tarafından çağırılır. Hem özellikleri üretir hem modeli koşturur."""
        cache_path = os.path.join(self.cache_dir, f"{date_str}_alaz.parquet")
        if os.path.exists(cache_path):
            return pd.read_parquet(cache_path)
            
        # 1. ALAZ, öncelikle iklim (FWI) değerlerine ihtiyaç duyar
        df_fwi = self.nc_engine.extract_climate_and_fwi(date_str)
        
        # 2. ALAZ Özelliklerini Üret
        df_ml = self.compute_ml_features(df_fwi, date_str)
        df_ml['risk_percent'] = 0.0
        df_ml['mode'] = 'ALAZ (ML)'
        
        print(f"[ALAZ] XGBoost bölgesel tahminleme başlıyor...")
        for bolge in ['MED', 'CON', 'BLK']:
            mask = df_ml['Bolge'] == bolge
            if mask.sum() == 0: continue
            
            model = self.models[bolge]
            feats = self.features[bolge]
            
            # Eksik model özelliklerini sıfırla/median ile doldur
            for f in feats:
                if f not in df_ml.columns:
                    df_ml[f] = 0
                    
            X = df_ml.loc[mask, feats]
            
            # Gerçek Tahmin
            probs = model.predict_proba(X)[:, 1] * 100
            df_ml.loc[mask, 'risk_percent'] = probs
            
        # Sadece Frontend'e Gönderilecek (JSON yükünü hafifletmek için) seçili kolonlar
        results = df_ml[['GRID_ID', 'risk_percent', 'mode']]
        results.to_parquet(cache_path, index=False)
        print(f"✅ {date_str} ALAZ Inference Bitti! Cache'e yazıldı.")
        
        return results

    def get_alaz_series(self, start_date, end_date):
        """Çoklu gün dizimi için"""
        dates = pd.date_range(start_date, end_date)
        all_dfs = []
        for d in dates:
            d_str = d.strftime('%Y-%m-%d')
            daily_df = self.run_prediction(d_str)
            daily_df['date'] = d_str
            all_dfs.append(daily_df)
        return pd.concat(all_dfs, ignore_index=True)
