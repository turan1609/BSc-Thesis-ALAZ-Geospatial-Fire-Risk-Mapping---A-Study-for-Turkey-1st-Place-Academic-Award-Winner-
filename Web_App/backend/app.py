from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import pandas as pd
import numpy as np
import os

from inference import ALAZEngine
from netcdf_engine import NetCDFProcessor

app = FastAPI(title="ALAZ Karar Destek API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tekil (Singleton) Örnekleme (RAM Optimizasyonu)
print("🌐 ALAZ & FWI Motorları Servis İçin Ayağa Kalkıyor...")
fwi_engine = NetCDFProcessor()
alaz_engine = ALAZEngine()

class SimulateRequest(BaseModel):
    start_date: str
    end_date: str
    mode: str  # 'fwi', 'alaz', 'compare'

@app.get("/")
def read_root():
    return {"message": "ALAZ API Canlı!"}

# ============================================================
# ANA SİMÜLASYON ENDPOINT'İ
# ============================================================
@app.post("/api/simulate")
def simulate(req: SimulateRequest):
    try:
        # ---- DOĞRULAMA ----
        try:
            d1 = pd.to_datetime(req.start_date)
            d2 = pd.to_datetime(req.end_date)
        except:
            raise HTTPException(status_code=400, detail="Geçersiz Tarih Formatı. Lütfen YYYY-AA-GG giriniz.")

        if d1.year > 2025 or d2.year > 2025:
            raise HTTPException(status_code=400, detail="Hata: Gelecek zaman seçemezsiniz! Sistem altyapımızdaki iklim (ERA5) ve uydu verileri maksimum 2025 yılına kadar günceldir.")

        diff_days = (d2 - d1).days
        if diff_days < 0:
            raise HTTPException(status_code=400, detail="Hata: Bitiş tarihi, Başlangıç tarihinden küçük olamaz.")
        if diff_days > 7:
            raise HTTPException(status_code=400, detail="Limit Aşımı: Sistem stabilitesi için zaman aralığı maksimum 7 gün seçilebilir.")

        if req.mode in ['alaz', 'compare']:
            if d1.year not in [2023, 2024, 2025]:
                raise HTTPException(status_code=400, detail="Model Test Limiti: ALAZ veya Karşılaştırmalı Mod; sadece test yılları (2023-2025) üzerinden çalıştırılabilir.")

        if req.mode == 'compare' and diff_days > 0:
            raise HTTPException(status_code=400, detail="Karşılaştırma Modunda tarih aralığı sadece 1 GÜN olmak zorundadır.")

        # ---- YÜRÜTME ----
        results = None

        if req.mode == 'fwi':
            df = fwi_engine.get_fwi_series(req.start_date, req.end_date)
            df['fwi_value'] = df['FWI_Final']   # Ham FWI (EFFIS renklendirme için)
            df['mode'] = 'fwi'
            df = df.replace({np.nan: None, np.inf: None, -np.inf: None})
            results = df[['GRID_ID', 'fwi_value', 'mode', 'date']].to_dict(orient='records')

        elif req.mode == 'alaz':
            df = alaz_engine.get_alaz_series(req.start_date, req.end_date)
            df = df.replace({np.nan: None, np.inf: None, -np.inf: None})
            results = df.to_dict(orient='records')

        elif req.mode == 'compare':
            df_f = fwi_engine.extract_climate_and_fwi(req.start_date)
            df_f['fwi_value'] = df_f['FWI_Final']   # Ham EFFIS
            df_a = alaz_engine.run_prediction(req.start_date)
            df_merge = pd.merge(df_f[['GRID_ID', 'fwi_value']], df_a[['GRID_ID', 'risk_percent']], on='GRID_ID')
            df_merge['date'] = req.start_date
            df_merge = df_merge.replace({np.nan: None, np.inf: None, -np.inf: None})
            results = df_merge.to_dict(orient='records')

        return {
            "status": "success",
            "metadata": {"start": req.start_date, "end": req.end_date, "mode": req.mode},
            "data": results
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Sistem Hatası (Console loguna bak): {str(e)}")

# ============================================================
# GRID DETAY ENDPOINT'İ (Tıklama → Bilgi Paneli)
# ============================================================
@app.get("/api/grid-detail")
def grid_detail(grid_id: str, date: str, mode: str):
    try:
        result = {"grid_id": grid_id, "date": date}

        def safe_round(v, n=1):
            return round(float(v), n) if pd.notna(v) else None

        # 1. Topoğrafya (M2 Statik Verisi)
        m2_match = alaz_engine.static_db[alaz_engine.static_db['GRID_ID'] == grid_id]
        if not m2_match.empty:
            row = m2_match.iloc[0]
            result['topography'] = {
                'elevation': safe_round(row['elevation']),
                'slope': safe_round(row['slope_mean']),
                'bolge': str(row['Bolge']),
                'corine_class': int(row['corine_class']) if pd.notna(row['corine_class']) else None
            }

        # 2. Hava Durumu + FWI (Cache'den)
        fwi_cache = os.path.join(fwi_engine.cache_dir, f"{date}_fwi.parquet")
        if os.path.exists(fwi_cache):
            df = pd.read_parquet(fwi_cache)
            fwi_match = df[df['GRID_ID'] == grid_id]
            if not fwi_match.empty:
                r = fwi_match.iloc[0]
                result['weather'] = {
                    'temperature': safe_round(r['M_T_Celsius']),
                    'humidity': safe_round(r['M_RH_Percent']),
                    'wind_speed': safe_round(r['M_Wind_Speed']),
                    'precipitation': safe_round(r['M_Precip_24h'], 2)
                }
                result['fwi'] = {
                    'ffmc': safe_round(r['FWI_FFMC']),
                    'dmc': safe_round(r['FWI_DMC']),
                    'dc': safe_round(r['FWI_DC']),
                    'isi': safe_round(r['FWI_ISI']),
                    'bui': safe_round(r['FWI_BUI']),
                    'fwi_final': safe_round(r['FWI_Final'])
                }

        # 3. ALAZ Spesifik Veriler
        if mode in ['alaz', 'compare']:
            dt = pd.to_datetime(date)
            alaz_cache = os.path.join(alaz_engine.cache_dir, f"{date}_alaz.parquet")

            alaz_risk = None
            if os.path.exists(alaz_cache):
                df_a = pd.read_parquet(alaz_cache)
                a_match = df_a[df_a['GRID_ID'] == grid_id]
                if not a_match.empty:
                    alaz_risk = round(float(a_match.iloc[0]['risk_percent']), 2)

            ndvi_val = None
            if alaz_engine.m8_ndvi:
                raw = alaz_engine.m8_ndvi.get((grid_id, dt.month))
                if raw is not None:
                    ndvi_val = round(float(raw), 4)

            dsf = None
            if alaz_engine.events_db is not None:
                past = alaz_engine.events_db[
                    (alaz_engine.events_db['GRID_ID'] == grid_id) &
                    (alaz_engine.events_db['Tarih'] < dt)
                ]
                if not past.empty:
                    dsf = int((dt - past['Tarih'].max()).days)
                else:
                    dsf = int((dt - pd.Timestamp('2008-01-01')).days)

            result['alaz'] = {
                'risk_percent': alaz_risk,
                'ndvi': ndvi_val,
                'days_since_last_fire': dsf
            }

        return result

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
