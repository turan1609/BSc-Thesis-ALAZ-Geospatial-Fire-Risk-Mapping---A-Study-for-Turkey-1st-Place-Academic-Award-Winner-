"""
M14 — Model Comparison: XGBoost vs SVM vs ANN
=============================================
Hocanın istekleri:
  1. Kullanılan feature/metriklerin açıklanması
  2. Örnek veri seti paylaşılacak
  3. 2 adet ML daha eklenecek (SVM, ANN)
  4. Kullanılan platformlar/arayüzler/cloud
  5. 3 bölge × 3 model = 9 sonuç tablosu

Author: Yusuf TURAN
"""

import os, sys, time, warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import joblib
from datetime import datetime

from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    roc_auc_score, f1_score, recall_score, precision_score, brier_score_loss
)
from sklearn.calibration import CalibratedClassifierCV

# ─── Paths ───────────────────────────────────────────────────
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH       = os.path.join(BASE, "Ara_dosyalar", "M11", "M11_final_dataset.parquet")
FEATURE_SETS    = os.path.join(BASE, "Sonuclar", "M12", "M12_pruned_feature_sets.joblib")
XGB_METRICS     = os.path.join(BASE, "Sonuclar", "M13", "M13_final_test_metrics.csv")
OUT_DIR         = os.path.join(BASE, "Tablolar")
os.makedirs(OUT_DIR, exist_ok=True)

REGIONS = ["MED", "CON", "BLK"]

# ═══════════════════════════════════════════════════════════════
#  STEP 1 — Load Data & Apply Temporal Split
# ═══════════════════════════════════════════════════════════════
print("=" * 70)
print("  M14 — MODEL COMPARISON: XGBoost vs SVM vs ANN")
print("=" * 70)
print()

print("[1/7] Loading dataset...")
df = pd.read_parquet(DATA_PATH)
df["Tarih"] = pd.to_datetime(df["Tarih"])
df["year"] = df["Tarih"].dt.year
print(f"  Total: {len(df):,} rows × {df.shape[1]} columns")

# Temporal Split — same as M12/M13
train_df = df[df["year"] <= 2021].copy()
val_df   = df[df["year"] == 2022].copy()
test_df  = df[df["year"] >= 2023].copy()
print(f"  Train (<=2021): {len(train_df):,} | Val (2022): {len(val_df):,} | Test (>=2023): {len(test_df):,}")

# Load pruned feature sets per region — filter to columns available in dataset
raw_feature_sets = joblib.load(FEATURE_SETS)
available_cols = set(df.columns)
feature_sets = {}
for region, feats in raw_feature_sets.items():
    valid = [f for f in feats if f in available_cols]
    dropped = [f for f in feats if f not in available_cols]
    feature_sets[region] = valid
    if dropped:
        print(f"  [{region}] Dropped {len(dropped)} missing features: {dropped}")
print(f"  Feature sets loaded: {', '.join(f'{k}={len(v)}' for k,v in feature_sets.items())}")
print()

# ═══════════════════════════════════════════════════════════════
#  STEP 2 — Train SVM for each region (FULL DATA)
# ═══════════════════════════════════════════════════════════════
print("[2/7] Training SVM models (full data, RBF kernel)...")
print("  [!] This may take a while on large regions...")
print()

svm_results = []

for region in REGIONS:
    feats = feature_sets[region]
    
    # Region subsets
    tr = train_df[train_df["Bolge"] == region]
    te = test_df[test_df["Bolge"] == region]
    vl = val_df[val_df["Bolge"] == region]
    
    X_train = tr[feats].values
    y_train = tr["Target"].values
    X_val   = vl[feats].values
    y_val   = vl["Target"].values
    X_test  = te[feats].values
    y_test  = te["Target"].values
    
    print(f"  [{region}] Train: {len(tr):,} | Val: {len(vl):,} | Test: {len(te):,} | Features: {len(feats)}")
    sys.stdout.flush()
    
    # Normalize (SVM requires scaling)
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_val_s   = scaler.transform(X_val)
    X_test_s  = scaler.transform(X_test)
    
    # Train SVM with probability=True for AUC and Brier
    try:
        t0 = time.time()
        svm = SVC(
            kernel="rbf",
            C=1.0,
            gamma="scale",
            probability=True,
            class_weight="balanced",
            cache_size=1000,   # MB -- speeds up training
            max_iter=50000,
            random_state=42,
            verbose=False,
        )
        svm.fit(X_train_s, y_train)
        elapsed = time.time() - t0
        print(f"       Training done in {elapsed:.1f}s")
        
        # Predict
        y_prob = svm.predict_proba(X_test_s)[:, 1]
        y_pred = svm.predict(X_test_s)
        
        auc   = roc_auc_score(y_test, y_prob)
        f1    = f1_score(y_test, y_pred)
        rec   = recall_score(y_test, y_pred)
        prec  = precision_score(y_test, y_pred)
        brier = brier_score_loss(y_test, y_prob)
        
        print(f"       AUC: {auc:.4f} | F1: {f1:.4f} | Recall: {rec:.4f} | Brier: {brier:.4f}")
        
        svm_results.append({
            "Region": region, "Model": "SVM",
            "AUC": round(auc, 4), "F1": round(f1, 4),
            "Recall": round(rec, 4), "Precision": round(prec, 4),
            "Brier": round(brier, 4),
        })
    except Exception as e:
        print(f"       [ERROR] SVM {region} failed: {e}")
        svm_results.append({
            "Region": region, "Model": "SVM",
            "AUC": 0, "F1": 0, "Recall": 0, "Precision": 0, "Brier": 1,
        })
    
    # Checkpoint: save partial results after each region
    pd.DataFrame(svm_results).to_csv(os.path.join(OUT_DIR, "_svm_checkpoint.csv"), index=False)
    print(f"       Checkpoint saved.")
    print()
    sys.stdout.flush()

# ═══════════════════════════════════════════════════════════════
#  STEP 3 — Train ANN for each region (FULL DATA)
# ═══════════════════════════════════════════════════════════════
print("[3/7] Training ANN models (MLP, full data)...")
print()

ann_results = []

for region in REGIONS:
    feats = feature_sets[region]
    
    tr = train_df[train_df["Bolge"] == region]
    te = test_df[test_df["Bolge"] == region]
    
    X_train = tr[feats].values
    y_train = tr["Target"].values
    X_test  = te[feats].values
    y_test  = te["Target"].values
    
    print(f"  [{region}] Train: {len(tr):,} | Test: {len(te):,} | Features: {len(feats)}")
    sys.stdout.flush()
    
    # Normalize
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)
    
    # Train MLP
    try:
        t0 = time.time()
        ann = MLPClassifier(
            hidden_layer_sizes=(128, 64, 32),
            activation="relu",
            solver="adam",
            learning_rate="adaptive",
            learning_rate_init=0.001,
            max_iter=500,
            early_stopping=True,
            validation_fraction=0.1,
            n_iter_no_change=20,
            batch_size=256,
            random_state=42,
            verbose=False,
        )
        ann.fit(X_train_s, y_train)
        elapsed = time.time() - t0
        print(f"       Training done in {elapsed:.1f}s ({ann.n_iter_} epochs)")
        
        # Predict
        y_prob = ann.predict_proba(X_test_s)[:, 1]
        y_pred = ann.predict(X_test_s)
        
        auc   = roc_auc_score(y_test, y_prob)
        f1    = f1_score(y_test, y_pred)
        rec   = recall_score(y_test, y_pred)
        prec  = precision_score(y_test, y_pred)
        brier = brier_score_loss(y_test, y_prob)
        
        print(f"       AUC: {auc:.4f} | F1: {f1:.4f} | Recall: {rec:.4f} | Brier: {brier:.4f}")
        
        ann_results.append({
            "Region": region, "Model": "ANN",
            "AUC": round(auc, 4), "F1": round(f1, 4),
            "Recall": round(rec, 4), "Precision": round(prec, 4),
            "Brier": round(brier, 4),
        })
    except Exception as e:
        print(f"       [ERROR] ANN {region} failed: {e}")
        ann_results.append({
            "Region": region, "Model": "ANN",
            "AUC": 0, "F1": 0, "Recall": 0, "Precision": 0, "Brier": 1,
        })
    
    print()
    sys.stdout.flush()

# ═══════════════════════════════════════════════════════════════
#  STEP 4 — Load existing XGBoost results
# ═══════════════════════════════════════════════════════════════
print("[4/7] Loading existing XGBoost results...")

xgb_raw = pd.read_csv(XGB_METRICS)
xgb_results = []
for _, row in xgb_raw.iterrows():
    region = row.iloc[0]  # Bölge column
    xgb_results.append({
        "Region": region, "Model": "XGBoost",
        "AUC": round(row["AUC"], 4),
        "F1": round(row["F1"], 4),
        "Recall": round(row["Recall"], 4),
        "Precision": round(row["Precision"], 4),
        "Brier": round(row["Brier"], 4),
    })

print(f"  Loaded {len(xgb_results)} XGBoost results")
print()

# ═══════════════════════════════════════════════════════════════
#  STEP 5 — Build 9-row comparison table
# ═══════════════════════════════════════════════════════════════
print("[5/7] Building 3×3 comparison table...")

all_results = xgb_results + svm_results + ann_results
results_df = pd.DataFrame(all_results)

# Sort by Region then Model
region_order = {"MED": 0, "CON": 1, "BLK": 2}
model_order  = {"XGBoost": 0, "SVM": 1, "ANN": 2}
results_df["_r"] = results_df["Region"].map(region_order)
results_df["_m"] = results_df["Model"].map(model_order)
results_df = results_df.sort_values(["_r", "_m"]).drop(columns=["_r", "_m"]).reset_index(drop=True)

out_path = os.path.join(OUT_DIR, "M14_model_karsilastirma.csv")
results_df.to_csv(out_path, index=False)
print(f"  Saved: {out_path}")
print()
print("  " + "=" * 65)
print("           3 REGION x 3 MODEL COMPARISON TABLE")
print("  " + "=" * 65)
print()
print(results_df.to_string(index=False))
print()

# Best model per region
for region in REGIONS:
    sub = results_df[results_df["Region"] == region]
    best = sub.loc[sub["AUC"].idxmax()]
    print(f"  [BEST] {region}: Best model = {best['Model']} (AUC={best['AUC']:.4f})")
print()

# ═══════════════════════════════════════════════════════════════
#  STEP 6 — Sample Dataset
# ═══════════════════════════════════════════════════════════════
print("[6/7] Creating sample dataset...")

samples = []
for region in REGIONS:
    sub = df[df["Bolge"] == region]
    pos = sub[sub["Target"] == 1].sample(n=min(5, len(sub[sub["Target"]==1])), random_state=42)
    neg = sub[sub["Target"] == 0].sample(n=min(5, len(sub[sub["Target"]==0])), random_state=42)
    samples.append(pos)
    samples.append(neg)

sample_df = pd.concat(samples, ignore_index=True)
sample_path = os.path.join(OUT_DIR, "ornek_veri_seti.csv")
sample_df.to_csv(sample_path, index=False)
print(f"  Saved: {sample_path} ({len(sample_df)} rows)")
print()

# ═══════════════════════════════════════════════════════════════
#  STEP 7 — Feature Explanation Table
# ═══════════════════════════════════════════════════════════════
print("[7/7] Creating feature explanation table...")

feature_info = [
    # Meteorology (ERA5-Land)
    ("M_T_Celsius",       "Meteorology",   "2m air temperature (°C) from ERA5-Land reanalysis at noon"),
    ("M_Dewpoint_C",      "Meteorology",   "2m dewpoint temperature (°C) — indicates atmospheric moisture content"),
    ("M_Wind_Speed",      "Meteorology",   "10m wind speed (m/s), derived from U and V components: sqrt(u2+v2)"),
    ("M_RH_Percent",      "Meteorology",   "Relative humidity (%) computed via Magnus formula from T and dewpoint"),
    ("M_SurfPressure",    "Meteorology",   "Surface atmospheric pressure (hPa) from ERA5-Land"),
    ("M_Soil_L1",         "Meteorology",   "Volumetric soil water content in layer 1 (0–7 cm depth, m³/m³)"),
    ("M_VPD_kPa",         "Meteorology",   "Vapor Pressure Deficit (kPa) — atmospheric drying power on vegetation"),
    ("M_Precip_7Day",     "Meteorology",   "Cumulative precipitation over the preceding 7 days (mm)"),
    ("M_Precip_30Day",    "Meteorology",   "Cumulative precipitation over the preceding 30 days (mm)"),
    ("M_Precip_90Day",    "Meteorology",   "Cumulative precipitation over the preceding 90 days (mm)"),
    ("M_Days_Since_Rain", "Meteorology",   "Consecutive dry days (days since last >=1mm precipitation event)"),
    # FWI (Van Wagner 1987)
    ("FWI_FFMC",          "Fire Weather",  "Fine Fuel Moisture Code — surface litter moisture, fast response (~2/3 day)"),
    ("FWI_DMC",           "Fire Weather",  "Duff Moisture Code — moderate-depth organic moisture (~15-day lag)"),
    ("FWI_DC",            "Fire Weather",  "Drought Code — deep soil/organic dryness indicator (~52-day memory)"),
    ("FWI_ISI",           "Fire Weather",  "Initial Spread Index — rate of fire spread, coupling wind and FFMC"),
    ("FWI_BUI",           "Fire Weather",  "Build-Up Index — total fuel available, combining DMC and DC"),
    ("FWI_Final",         "Fire Weather",  "Fire Weather Index — final composite danger rating"),
    # Vegetation (MODIS)
    ("NDVI",              "Vegetation",    "Normalized Difference Vegetation Index from MODIS Terra MOD13Q1 (250m)"),
    ("perc_tree",         "Land Cover",    "Percentage of tree cover within the H3 grid cell (from CORINE 2018)"),
    ("perc_shrub_grass",  "Land Cover",    "Percentage of shrub/grassland cover within the H3 grid cell"),
    ("perc_agri",         "Land Cover",    "Percentage of agricultural land within the H3 grid cell"),
    ("perc_water",        "Land Cover",    "Percentage of water bodies within the H3 grid cell"),
    # Topography (SRTM)
    ("elevation",         "Topography",    "Mean elevation (m) within H3 polygon from SRTM 30m DEM"),
    ("slope_mean",        "Topography",    "Mean terrain slope (degrees) from SRTM 30m DEM"),
    ("northness",         "Topography",    "Cosine of aspect angle — north-facing slope indicator"),
    ("eastness",          "Topography",    "Sine of aspect angle — east-facing slope indicator"),
    # Anthropogenic (OSM)
    ("days_since_last_fire","Anthropogenic","Days elapsed since the last recorded fire in the same grid cell"),
    ("dist_road_all",     "Anthropogenic", "Distance (m) to nearest road of any type from OpenStreetMap"),
    ("dist_road_forest",  "Anthropogenic", "Distance (m) to nearest forest/track road from OpenStreetMap"),
    ("dist_settlement",   "Anthropogenic", "Distance (m) to nearest populated settlement from OpenStreetMap"),
    ("log_dist_road",     "Anthropogenic", "Log-transformed distance to nearest road (normalizes skewed distribution)"),
    ("log_dist_forest",   "Anthropogenic", "Log-transformed distance to nearest forest road"),
    ("log_dist_settlement","Anthropogenic","Log-transformed distance to nearest settlement"),
    # Interaction Terms
    ("I_FWI_x_NDVI",      "Interaction",  "FWI × NDVI — captures when dangerous weather meets stressed vegetation"),
    ("I_FWI_x_Wind",      "Interaction",  "FWI × Wind Speed — amplifies risk when wind accelerates fire spread"),
    ("I_VPD_x_DryDays",   "Interaction",  "VPD × Dry Days — cumulative atmospheric-soil drying stress"),
    ("I_Dewpoint_x_Wind", "Interaction",  "Dewpoint × Wind — nocturnal moisture recovery disrupted by wind"),
    ("I_FWI_x_NDVI_CON",  "Interaction",  "Region-specific FWI×NDVI term for Continental zone fire dynamics"),
    ("I_Wind_x_RoadDist", "Interaction",  "Wind × Road Distance — human access under wind-driven fire conditions"),
    # Temporal Encoding
    ("T_month_sin",       "Temporal",     "Sine encoding of month — captures cyclical seasonality"),
    ("T_month_cos",       "Temporal",     "Cosine encoding of month — captures cyclical seasonality"),
    ("T_doy_sin",         "Temporal",     "Sine encoding of day-of-year — fine-grained seasonal signal"),
    ("T_doy_cos",         "Temporal",     "Cosine encoding of day-of-year — fine-grained seasonal signal"),
    # Wind components
    ("wind_sin",          "Meteorology",  "Sine of wind direction — directional wind component"),
    ("wind_cos",          "Meteorology",  "Cosine of wind direction — directional wind component"),
    # Derived terrain
    ("chimney_index",     "Topography",   "Topographic channeling index — fire chimney effect on steep valleys"),
    ("chimney_effect",    "Topography",   "Binary chimney effect indicator (slope + valley alignment)"),
    ("twi_proxy",         "Topography",   "Topographic Wetness Index proxy — soil moisture accumulation potential"),
]

feat_df = pd.DataFrame(feature_info, columns=["Feature", "Domain", "Description"])
feat_path = os.path.join(OUT_DIR, "feature_aciklamalari.csv")
feat_df.to_csv(feat_path, index=False, encoding="utf-8-sig")
print(f"  Saved: {feat_path} ({len(feat_df)} features)")
print()

# ═══════════════════════════════════════════════════════════════
#  Summary
# ═══════════════════════════════════════════════════════════════
print("=" * 70)
print("  [OK] ALL TASKS COMPLETE")
print("=" * 70)
print()
print("  Generated files:")
print(f"   1. {out_path}")
print(f"   2. {sample_path}")
print(f"   3. {feat_path}")
print()
print("  Final 9-row comparison:")
print(results_df[["Region","Model","AUC","Recall","Brier"]].to_string(index=False))
