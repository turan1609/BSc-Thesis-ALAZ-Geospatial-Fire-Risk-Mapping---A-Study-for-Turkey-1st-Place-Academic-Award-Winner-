import os
import time
import math
import pandas as pd
import numpy as np
import xarray as xr
import h3

# ====================================================================
# VAN WAGNER (1987) FWI HESAPLAMA MOTORU
# ====================================================================
def fwi_day(T, RH, W, P, mo_idx, ffmc0, dmc0, dc0):
    Le = [6.5,7.5,9.0,12.8,13.9,13.9,12.4,10.9,9.4,8.0,7.0,6.0]
    Lf = [-1.6,-1.6,-1.6,0.9,3.8,5.8,6.4,5.0,2.4,0.4,-1.6,-1.6]
    m_i = mo_idx - 1 
    
    # FFMC
    mo = 147.2*(101-ffmc0)/(59.5+ffmc0)
    if P > 0.5:
        rf = P - 0.5
        if mo <= 150:
            mr = mo + 42.5*rf*math.exp(-100/(251-mo))*(1-math.exp(-6.93/rf))
        else:
            mr = (mo + 42.5*rf*math.exp(-100/(251-mo))*(1-math.exp(-6.93/rf))
                  + 0.0015*(mo-150)**2*rf**0.5)
        mo = min(mr, 250)
    
    Ed = 0.942*RH**0.679+11*math.exp((RH-100)/10)+0.18*(21.1-T)*(1-math.exp(-0.115*RH))
    Ew = 0.618*RH**0.753+10*math.exp((RH-100)/10)+0.18*(21.1-T)*(1-math.exp(-0.115*RH))
    
    if mo > Ed:
        ko = 0.424*(1-(RH/100)**1.7)+0.0694*W**0.5*(1-(RH/100)**8)
        kd = ko*0.581*math.exp(0.0365*T)
        m = Ed + (mo-Ed)*10**(-kd)
    elif mo < Ew:
        k1 = 0.424*(1-((100-RH)/100)**1.7)+0.0694*W**0.5*(1-((100-RH)/100)**8)
        kw = k1*0.581*math.exp(0.0365*T)
        m = Ew-(Ew-mo)*10**(-kw)
    else:
        m = mo
    ffmc = max(0, min(101, 59.5*(250-m)/(147.2+m)))
    
    # DMC
    dmc = dmc0
    if P > 1.5:
        re = 0.92*P-1.27
        Mo = 20+math.exp(5.6348-dmc0/43.43)
        b = (100/(0.5+0.3*dmc0) if dmc0<=33 else 14-1.3*math.log(dmc0) if dmc0<=65 else 6.2*math.log(dmc0)-17.2)
        Mr = Mo+1000*re/(48.77+b*re)
        dmc = max(0, 244.72-43.43*math.log(max(Mr-20, 1e-6)))
    if T > -1.1: dmc = dmc + 100*1.894*(T+1.1)*(100-RH)*Le[m_i]*1e-6
    dmc = max(0, dmc)
    
    # DC
    dc = dc0
    if P > 2.8:
        rd = 0.83*P-1.27
        Qo = 800*math.exp(-dc0/400)
        Qr = Qo+3.937*rd
        dc = max(0, 400*math.log(max(800/Qr, 1e-6)))
    if T > -2.8: dc = dc + 0.5*max(0, 0.36*(T+2.8)+Lf[m_i])
    dc = max(0, dc)
    
    # ISI
    m2 = 147.2*(101-ffmc)/(59.5+ffmc)
    isi = 0.208*math.exp(0.05039*W)*91.9*math.exp(-0.1386*m2)*(1+m2**5.31/4.93e7)
    
    # BUI
    bui = (0.8*dmc*dc/(dmc+0.4*dc+1e-6) if dmc<=0.4*dc else dmc-(1-0.8*dc/(dmc+0.4*dc+1e-6))*(0.92+(0.0114*dmc)**1.7))
    bui = max(0, bui)
    
    # FWI
    fD = 0.626*bui**0.809+2 if bui<=80 else 1000/(25+108.64*math.exp(-0.023*bui))
    B = 0.1*isi*fD
    fwi = math.exp(2.72*(0.434*math.log(B))**0.647) if B > 1 else B
    
    return ffmc, dmc, dc, isi, bui, fwi

class NetCDFProcessor:
    def __init__(self, base_dir=r"C:\Users\Yusuf\Desktop\Tez-bolgesel"):
        self.raw_dir = os.path.join(base_dir, "Ham-Data", "ERA5_Raw")
        self.skin_dir = os.path.join(base_dir, "Ham-Data", "ERA5_Skin")
        self.cache_dir = os.path.join(base_dir, "Web_App", "cache", "fwi")
        self.m2_path = os.path.join(base_dir, "Ara_dosyalar", "M2_gridler_bolge.parquet")
        
        os.makedirs(self.cache_dir, exist_ok=True)
        
        self.grid_to_era5 = None
        self.ordered_grids = None

    def build_grid_mapping(self):
        """H3 Gridlerini ERA5 Koordinatlarına Müşterinin argmin Mantığıyla Eşleştirir"""
        if self.grid_to_era5 is not None:
            return
            
        print("[Yavaş İşlem] H3 -> ERA5 Eşleşmesi Kuruluyor (Bunu 1 kere yapar)...")
        m2 = pd.read_parquet(self.m2_path, columns=['GRID_ID'])
        unique_grids = m2['GRID_ID'].unique()
        self.ordered_grids = unique_grids
        
        era5_lat_grid = np.arange(35.50, 42.51, 0.1)
        era5_lon_grid = np.arange(25.50, 45.01, 0.1)
        
        mapping = {}
        for gid in unique_grids:
            try:
                lat, lon = h3.cell_to_latlng(gid)
            except:
                lat, lon = h3.h3_to_geo(gid) # v3/v4 uyum
            nearest_lat = era5_lat_grid[np.argmin(np.abs(era5_lat_grid - lat))]
            nearest_lon = era5_lon_grid[np.argmin(np.abs(era5_lon_grid - lon))]
            mapping[gid] = (round(nearest_lat, 1), round(nearest_lon, 1))
            
        self.grid_to_era5 = mapping
        print("✅ Eşleştirme Bitti!")

    def _clean_open(self, path):
        ds = xr.open_dataset(path)
        if 'expver' in ds.dims:
            ds_list = [ds.isel(expver=i) for i in range(len(ds.expver))]
            ds = ds_list[0]
            for other in ds_list[1:]:
                ds = ds.fillna(other)
        if 'number' in ds.dims:
            ds = ds.isel(number=0)
        return ds

    def extract_climate_and_fwi(self, date_str):
        """Web App: Verilen gün için .nc dosyasını açıp FWI dahil tüm veriyi Cache'e atar"""
        cache_path = os.path.join(self.cache_dir, f"{date_str}_fwi.parquet")
        if os.path.exists(cache_path):
            return pd.read_parquet(cache_path)
            
        self.build_grid_mapping()
        
        dt = pd.to_datetime(date_str)
        y, m, d = dt.year, dt.month, dt.day
        
        lf = os.path.join(self.raw_dir, f"ERA5_Land_{y}_{m:02d}.nc")
        ef = os.path.join(self.raw_dir, f"ERA5_Extras_{y}_{m:02d}.nc")
        sf = os.path.join(self.skin_dir, f"ERA5_SkinTemp_{y}_{m:02d}.nc") # Ya da Skin_...
        
        if not os.path.exists(lf) or not os.path.exists(ef):
            raise FileNotFoundError(f"{y}-{m:02d} ait NetCDF ham verisi (ERA5_Land veya Extras) dizinde bulunamadı!")

        print(f"[{date_str}] NetCDF İşleniyor: ERA5 -> H3 Extraction...")
        
        ds_l = self._clean_open(lf)
        ds_e = self._clean_open(ef)
        try:
            ds_s = self._clean_open(sf)
        except Exception:
            ds_s = ds_l # Dummy fallback
            
        # Target hour: 10 UTC (öğlen 13:00 TSİ) for the specific date
        target_timestamp = pd.Timestamp(f"{date_str} 10:00:00")
        
        try:
            sl = ds_l.sel(valid_time=target_timestamp)
            se = ds_e.sel(valid_time=target_timestamp)
            try:
                ss = ds_s.sel(valid_time=target_timestamp)
            except:
                ss = sl # fallback
        except KeyError:
            ds_l.close()
            raise Exception(f"{target_timestamp} .nc dosyasında bulunamadı!")
            
        # 1 günlük total precipitation
        tp_raw = ds_l['tp'].sel(valid_time=slice(f"{date_str} 00:00", f"{date_str} 23:59")).sum(dim='valid_time')
        
        # Grid loop Extraction
        results = []
        # FWI Initial values for "On-the-fly" dashboard logic
        ffmc, dmc, dc = 85.0, 6.0, 15.0 
        
        # Hızlandırmak için .values matrix olarak alalım
        lats = ds_l.latitude.values
        lons = ds_l.longitude.values
        
        t2m_mat = sl['t2m'].values
        d2m_mat = se['d2m'].values
        u10_mat = sl['u10'].values
        v10_mat = sl['v10'].values
        tp_mat = tp_raw.values * 1000  # mm'e çevir
        
        for gid in self.ordered_grids:
            elat, elon = self.grid_to_era5[gid]
            
            # Find matrix indices
            lat_idx = np.argmin(np.abs(lats - elat))
            lon_idx = np.argmin(np.abs(lons - elon))
            
            t2m_val = t2m_mat[lat_idx, lon_idx] - 273.15
            
            # Kıyı Şeridi / Deniz NaN Kontrolü (En Yakın Geçerli Komşuyu Arama)
            if np.isnan(t2m_val):
                found = False
                # Çevresel matris indekslerinde arama (1 veya 2 birim komşuluk)
                for dy in [-1, 1, 0, -2, 2]:
                    for dx in [-1, 1, 0, -2, 2]:
                        if dy == 0 and dx == 0: continue
                        n_lat = max(0, min(len(lats)-1, lat_idx + dy))
                        n_lon = max(0, min(len(lons)-1, lon_idx + dx))
                        if not np.isnan(t2m_mat[n_lat, n_lon]):
                            lat_idx, lon_idx = n_lat, n_lon
                            t2m_val = t2m_mat[lat_idx, lon_idx] - 273.15
                            found = True
                            break
                    if found: break
                
                # Extreme durum: Eğer etrafta da hiç değer bulunamazsa standart bir yaz ortalaması bas
                if not found:
                    t2m_val = 25.0
                    
            # Artık lat_idx ve lon_idx güvenli bir karasal koordinata sabitlendi, hepsini çekebiliriz
            d2m_val = d2m_mat[lat_idx, lon_idx] - 273.15
            u10_val = u10_mat[lat_idx, lon_idx]
            v10_val = v10_mat[lat_idx, lon_idx]
            tp_val = tp_mat[lat_idx, lon_idx]
            
            # Formüller
            wind = np.sqrt(u10_val**2 + v10_val**2)
            rh = (100 * np.exp(17.27 * d2m_val / (d2m_val + 237.3)) / 
                  np.exp(17.27 * t2m_val / (t2m_val + 237.3)))
            rh = max(0, min(100, rh))
            
            # FWI Hesabı
            f_ffmc, f_dmc, f_dc, f_isi, f_bui, f_fwi = fwi_day(
                t2m_val, rh, wind, tp_val, m, ffmc, dmc, dc
            )
            
            results.append({
                'GRID_ID': gid,
                'M_T_Celsius': t2m_val,
                'M_RH_Percent': rh,
                'M_Wind_Speed': wind,
                'M_Precip_24h': tp_val,
                'FWI_FFMC': f_ffmc,
                'FWI_DMC': f_dmc,
                'FWI_DC': f_dc,
                'FWI_ISI': f_isi,
                'FWI_BUI': f_bui,
                'FWI_Final': f_fwi
            })
            
        ds_l.close()
        ds_e.close()
        try: ds_s.close()
        except: pass
        
        df = pd.DataFrame(results)
        df.to_parquet(cache_path, index=False)
        print(f"✅ {date_str} için NetCDF işlemi tamamlandı ve CACHE'e kaydedildi.")
        return df

    def get_fwi_series(self, start_date, end_date):
        """API'nin çağırdığı ana FWI metod"""
        dates = pd.date_range(start_date, end_date)
        all_dfs = []
        for d in dates:
            d_str = d.strftime('%Y-%m-%d')
            daily_df = self.extract_climate_and_fwi(d_str)
            daily_df['date'] = d_str
            all_dfs.append(daily_df)
        return pd.concat(all_dfs, ignore_index=True)
