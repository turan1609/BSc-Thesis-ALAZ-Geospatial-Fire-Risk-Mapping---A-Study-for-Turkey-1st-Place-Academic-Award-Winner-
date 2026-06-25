# ALAZ: Regional Machine Learning and Climate Index-Based Forest Fire Early Warning Decision Support System: A Turkey Application | 1st Place Academic Award Winner | Supported by TÜBİTAK 2209/A 

**Author:** Yusuf Turan  
**Status:** Completed (BSc Thesis) & 1st Place Academic Award Winner  

## Dear Reader,

This repository contains the source code, data processing pipelines, and predictive models developed for my Bachelor of Science graduation thesis. I am honored to state that this project was awarded the **1st Place Academic Award** in the university project competition.

Given the comprehensive results and the novelty of the regionalized machine learning approach applied herein, my academic committee strongly advised publishing this work as a peer-reviewed academic paper. However, as my primary focus is currently directed toward my professional career in the private sector and industrial applications, **I have chosen to respectfully decline the formal publication route at this time.**

Instead, I have decided to open-source the entirety of this research. My objective is to further develop this system during my Master's studies by integrating high-resolution, restricted data from the General Directorate of Forestry (OGM). 

You are free to use, modify, and integrate this methodology into your own research or commercial projects. My only request is that you adhere to academic and professional integrity by properly citing my name (**Yusuf Turan**) and this repository as the original source of the methodology.

Sincerely,  
**Yusuf Turan**
---

Welcome to the official repository of the **ALAZ Decision Support System**, my B.Sc. Thesis project in Computer Engineering at Aydın Adnan Menderes University. 

This project was developed under the supervision of **Asst. Prof. Dr. Hüseyin ABACI** and has been proudly awarded the **1st Place Academic Award** in the graduation projects exhibition. Furthermore, the research and development of ALAZ were supported by **TÜBİTAK** (The Scientific and Technological Research Council of Türkiye).

<p align="center">
  <img width="695" height="931" alt="image" src="https://github.com/user-attachments/assets/c7413096-d06e-452d-8029-7457bc509741" />

  <img width="691" height="929" alt="image" src="https://github.com/user-attachments/assets/4b4d92a8-a40f-45cb-956b-22721ab8ac6c" />

  <img width="690" height="927" alt="image" src="https://github.com/user-attachments/assets/b3a1f0e9-8c62-465f-9fb6-583dc13ee199" />

  <img width="1908" height="909" alt="image" src="https://github.com/user-attachments/assets/a7679dd6-da66-4009-a132-a1e5e5df9c2c" />

  <br>
  <em>Project Exhibition and Award Ceremony</em>
</p>
---



## Installation & Usage

To run the ALAZ Decision Support System locally on your machine, follow the steps below.

### 1. Repository Structure
The project is organized into modular directories for the backend API, frontend web interface, and machine learning models:

```text
ALAZ/
├── backend/
│   ├── main.py                # FastAPI server handling live ERA5 requests
│   ├── fwi_calculator.py      # Van Wagner FWI math engine
│   ├── requirements.txt       # Python dependencies
│   └── models/                # Trained XGBoost regional models (.xgb)
├── frontend/
│   ├── index.html             # Main DSS Interface
│   ├── style.css              # UI Styling
│   └── app.js                 # MapLibre GL & deck.gl logic
├── data/                      # Place downloaded Drive data here
│   ├── topology/              # Hexagonal grid definitions & static features
│   └── weather/               # Historical NetCDF files
└── README.md
```

### 2. Getting the Data
Due to GitHub file size limits, the raw NetCDF meteorological files, trained XGBoost models, and massive H3 grid topologies are hosted externally.
1. Download the required dataset from this link: **[Download ALAZ Data & Models](https://drive.google.com/drive/folders/1uqp8JH3X4KBxeQP077M5Gly81VT-m1Ai?usp=sharing)**
2. Extract the downloaded `.zip` file.
3. Place the extracted contents directly into the `data/` and `backend/models/` directories as shown in the structure above.

### 3. Setup & Execution

**Backend Setup:**
ALAZ uses a Python FastAPI backend to process live climate data and run XGBoost inferences.
```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment (Optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install the required dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend Setup:**
The frontend is built with Vanilla JavaScript, MapLibre GL, and deck.gl. It does not require a complex Node.js build process.
1. Navigate to the `frontend/` directory.
2. You can simply start a local Python HTTP server to serve the static files:
```bash
cd frontend
python -m http.server 3000
```
3. Open your browser and navigate to: `http://localhost:3000`

> **Note:** Ensure the FastAPI backend is running on port 8000 simultaneously, as the frontend will automatically attempt to fetch geospatial predictions from `http://localhost:8000`.

## Abstract

**REGIONAL MACHINE LEARNING AND CLIMATE INDEX-BASED FOREST FIRE EARLY WARNING DECISION SUPPORT SYSTEM: A TURKIYE APPLICATION**  
**Yusuf TURAN**  
*B.Sc. Thesis, Computer Engineering Department*  
*Supervisor: Asst. Prof. Dr. Hüseyin ABACI*  
*2026, 34 pages*  

The frequency and intensity of wildfires in Türkiye have severely escalated, driven by compounding climatic changes. Historically, fire prediction relied heavily on meteorological danger indices, such as the Canadian Fire Weather Index (FWI) system. While these indices quantify conditions favorable for combustion, they inherently fail to model actual ignition probabilities, human influences, and localized vegetation phenology. To address these limitations, this study presents ALAZ, a novel regional forest fire early warning Decision Support System engineered specifically for Türkiye. To eliminate spatial distortions, the national forested terrain was tessellated into 235,621 hexagonal grids (H3) and strictly partitioned into Mediterranean, Continental, and Black Sea macro-regions based on biogeographical boundaries. Addressing extreme class imbalance (~1:100,000 daily fire prevalence) through six physically meaningful negative sampling strategies, the system trains independent, region-specific XGBoost classifiers. These models integrate 36 spatial-temporal features, merging ERA5 meteorology, FWI sub-indices, MODIS NDVI, topography, and anthropogenic factors. Evaluated on unseen data from 2023–2025, the models demonstrated significant predictive capability (Mediterranean AUC: 0.759, Black Sea AUC: 0.775). Crucially, the outputs were calibrated via Platt Scaling to ensure statistical reliability, achieving Brier Scores below 0.088. SHAP analysis confirmed that human accessibility consistently ranks as a primary fire driver alongside region-specific meteorological triggers. Finally, the models were deployed through a high-performance web-based Decision Support System, providing dynamic, real-time risk visualizations to bridge the gap between academic research and operational forest management.

**Keywords:** Machine Learning, Forest Fires, Fire Weather Index, Decision Support System, XGBoost  

---

## Özet

**REGIONAL MACHINE LEARNING AND CLIMATE INDEX-BASED FOREST FIRE EARLY WARNING DECISION SUPPORT SYSTEM: A TURKIYE APPLICATION**  
**Yusuf TURAN**  
*Lisans Bitirme Tezi, Bilgisayar Mühendisliği Bölümü*  
*Tez Danışmanı: Doktor Öğretim Üyesi Hüseyin ABACI*  
*2026, 34 sayfa*  

Türkiye, şiddetlenen iklim değişikliklerinin etkisiyle orman yangını sıklığı ve şiddetinde ciddi artışlar yaşamaktadır. Tarihsel olarak yangın tahmini, Kanada Orman Yangını Hava İndeksi (FWI) gibi meteorolojik tehlike indekslerine dayanmaktadır. Bu indeksler yanma için elverişli koşulları ölçse de, gerçek tutuşma olasılıklarını, insan etkilerini ve yerel bitki fenolojisini modellemede doğası gereği yetersiz kalmaktadır. Bu sınırlamaları gidermek amacıyla bu çalışma, Türkiye için özel olarak tasarlanmış özgün ve bölgesel bir orman yangını erken uyarı Karar Destek Sistemi olan ALAZ'ı sunmaktadır. Mekânsal bozulmaları ortadan kaldırmak için ulusal ormanlık arazi 235.621 altıgen gride (H3) bölünmüş ve biyocoğrafi sınırlara göre Akdeniz, Karasal ve Karadeniz makro-bölgelerine ayrılmıştır. Aşırı sınıf dengesizliğini (yaklaşık 1:100.000 günlük yangın prevalansı) altı farklı fiziksel anlamlı negatif örnekleme stratejisi ile ele alan sistem, bağımsız ve bölgeye özgü XGBoost sınıflandırıcıları eğitmektedir. Bu modeller; ERA5 meteorolojisi, FWI alt indeksleri, MODIS NDVI, topoğrafya ve antropojenik faktörleri birleştiren 36 mekânsal-zamansal özniteliği entegre etmektedir. 2023–2025 yıllarına ait görülmemiş veriler üzerinde değerlendirilen modeller, önemli bir tahmin yeteneği göstermiştir (Akdeniz AUC: 0.759, Karadeniz AUC: 0.775). Kritik olarak, model çıktıları istatistiksel güvenilirliği sağlamak için Platt Ölçekleme ile kalibre edilmiş ve 0.088'in altında Brier Skorları elde edilmiştir. SHAP analizi, insan erişilebilirliğinin, bölgeye özgü meteorolojik tetikleyicilerle birlikte tutarlı bir şekilde birincil yangın etkeni olduğunu doğrulamıştır. Son olarak, modeller web tabanlı bir Karar Destek Sistemi üzerinden çalıştırılmış ve akademik araştırma ile operasyonel orman yönetimi arasındaki boşluğu doldurmak için dinamik, gerçek zamanlı risk görselleştirmeleri sunulmuştur.

**Anahtar Kelimeler:** Makine Öğrenimi, Orman Yangınları, Yangın Hava İndeksi, Karar Destek Sistemi, XGBoost.  

---

## Acknowledgement

First and foremost, I would like to express my deepest gratitude to my thesis supervisor, Asst. Prof. Dr. Hüseyin ABACI, for his invaluable guidance, continuous support, and immense knowledge throughout the course of this research. His mentorship has been instrumental in shaping both the theoretical framework and the practical implementation of the ALAZ system.  

I would also like to extend my sincere thanks to the academic and administrative staff of the Computer Engineering Department at Aydın Adnan Menderes University for providing a supportive and enriching educational environment.  

I am highly indebted to Mustafa Gümrükçü, Forest Engineer at the General Directorate of Forestry (OGM), for his valuable sectoral insights and expertise, as well as the NexAdım program for their invaluable support.

Special thanks are owed to the open-science community, particularly the maintainers of the European Environment Agency (EEA) and NASA FIRMS datasets, whose accessible global data made this regional research possible. 

Furthermore, I would like to express my sincere appreciation to my former buddy, Korhan Zıvralı, alongside my dear friends, Kaan Erden and Cihan Ayindi, for their insightful discussions, valuable feedback, and steadfast camaraderie throughout this journey. 

Lastly, but most importantly, I would like to express my profound gratitude to my family for their unwavering patience, encouragement, and emotional support during the long hours of research, coding, and writing. This accomplishment would not have been possible without them.

## 1. INTRODUCTION 

### 1.1. Background and Motivation 
Türkiye, due to its diverse topography and predominantly Mediterranean climate, is highly susceptible to forest fires. In recent decades, the frequency and intensity of these wildfires have escalated severely, driven in large part by the compounding effects of global climate change. Studies have demonstrated that shifts in climate scenarios, particularly increases in extreme temperature and Vapor Pressure Deficit (VPD), directly expand high-susceptibility fire zones (Yang et al., 2026). As these climatic pressures mount, the need for robust, proactive fire management strategies becomes critical. 

Historically, regional and national fire prediction systems have relied heavily on traditional meteorological danger indices, most notably the Canadian Forest Fire Weather Index (FWI) system. While FWI is a powerful tool for quantifying conditions favorable for combustion—and has been shown to strongly correlate with localized factors like soil moisture and Land Surface Temperature (Atalay et al., 2024)—it possesses inherent limitations. Traditional indices model the physical flammability of the environment, but they do not predict the actual probability of ignition (Dong et al., 2022). They fundamentally ignore anthropogenic influences and localized vegetation phenology, which are critical triggers in actual fire events (Lee et al., 2025; Moumane et al., 2025).  

To bridge this gap, machine learning (ML) has emerged as a transformative approach, capable of capturing the complex, non-linear relationships between meteorological, topographical, and human variables.  

### 1.2. Problem Statement 
Despite the clear potential of machine learning, existing early warning and susceptibility mapping efforts face significant methodological constraints that limit their operational deployment in Türkiye.  

First, many systems apply uniform algorithms across diverse geographical landscapes. Türkiye possesses massive biogeographical diversity—from the hot, arid Mediterranean coast to the humid Black Sea region and the arid Continental interior. Applying a single monolithic model to such varied ecological zones sacrifices regional accuracy (Sinato & Rivas, 2026).  

Second, the vast majority of existing ML studies in wildfire science generate static susceptibility maps or output raw, uncalibrated probability scores (Iban & Aksu, 2024). While these maps identify generally risky areas, they do not provide calibrated, real-time daily probabilities that operational decision-makers can trust. If a model predicts a "70% risk," it must statistically correlate with a true 70% occurrence rate, a calibration standard rarely achieved in literature. 

Finally, wildfires are predominantly human-caused, yet human activity is often inadequately represented in prediction models. Recent findings emphasize that human accessibility (such as distance to settlements and road networks) is often a primary driver of fire occurrence, sometimes outweighing natural climatic factors (Bouzeraa et al., 2025; Lee et al., 2025). A functional decision support system must account for these anthropogenic triggers alongside natural climate indices. 

### 1.3. Objectives 
The primary objective of this thesis is to design, develop, and evaluate "ALAZ," a regionally specialized, Machine Learning and Climate Index-Based Forest Fire Early Warning Decision Support System for Türkiye. The specific sub-objectives are: 

1. To develop spatially independent, regional machine learning models tailored to the specific climatic dynamics of Türkiye's Mediterranean, Black Sea, and Continental macro-regions. 
2. To seamlessly integrate traditional physical models (the FWI system) with machine learning algorithms to enhance predictive capability. 
3. To resolve the extreme class imbalance problem inherent in daily fire prediction by engineering and evaluating physically meaningful negative sampling strategies. 
4. To calibrate model outputs to produce statistically reliable, operational daily fire probabilities. 
5. To deploy the trained regional models within a high-performance, web-based Decision Support System (DSS) for real-time risk visualization. 

### 1.4. Contributions 
This study introduces several novel contributions to the field of wildfire prediction and management in Türkiye: 

* It presents the first regionalized, ML-based daily forest fire early warning system for Türkiye, utilizing Uber's H3 spatial tessellation engine to eliminate spatial boundaries. 
* It conducts a systematic evaluation of 120 experimental models across six distinct negative sampling strategies, demonstrating how physical context in negative sampling impacts model performance. 
* It provides a fully calibrated predictive model evaluated on unseen, out-of-time data (2023–2025), preventing data leakage and proving operational readiness. 
* It offers full model transparency through SHAP (SHapley Additive exPlanations) analysis, identifying region-specific triggers for fires. 
* It delivers a functional, open-source web application capable of calculating the Van Wagner FWI and generating XGBoost predictions in real-time. 

### 1.5. Thesis Organization 
The remainder of this thesis is organized as follows: Chapter 2 provides a comprehensive literature review of traditional fire danger rating systems, machine learning approaches in wildfire prediction, and the application of explainable AI. Chapter 3 details the materials and methods, including the data sources, spatial regionalization, feature engineering, negative sampling strategies, and model architecture. Chapter 4 presents the experimental results, model evaluations, comparative analyses, and SHAP interpretability findings. Finally, Chapter 5 summarizes the conclusions of the study and outlines directions for future research.

## 2. LITERATURE REVIEW 

### 2.1. Traditional Fire Danger Rating Systems 
Historically, global and regional forest fire management has been heavily dependent on meteorological fire danger indices. The most universally adopted of these is the Canadian Forest Fire Weather Index (FWI) system, originally developed by Van Wagner (1987). The FWI system mathematically models the moisture content of different forest fuel layers using daily temperature, relative humidity, wind speed, and precipitation. Recent studies in Türkiye have validated the high correlation between the FWI and physical environmental proxies. For instance, Atalay et al. (2024) demonstrated that in the Antalya region, FWI scores exhibited a 0.96 positive correlation with MODIS Land Surface Temperature (LST) and a −0.93 negative correlation with soil moisture.  

While the European Forest Fire Information System (EFFIS) successfully utilizes the FWI to establish danger classes (ranging from Low to Very Extreme), these traditional indices inherently model susceptibility rather than actual ignition probability (Atalay et al., 2024). They do not incorporate vegetation phenology, topographical channeling effects, or anthropogenic ignition sources, leading to a recognized gap in dynamic, daily prediction (Dong et al., 2022). 

### 2.2. Machine Learning Approaches for Wildfire Prediction 
In recent years, Machine Learning (ML) has rapidly superseded traditional statistical models in wildfire susceptibility mapping due to its ability to capture non-linear interactions among vast multi-dimensional datasets. Tree-based ensemble models, particularly Random Forest (RF) and Extreme Gradient Boosting (XGBoost), have consistently outperformed other algorithms.  

Yang et al. (2026) utilized XGBoost to map fire susceptibility across the complex topography of the Yunnan Plateau in China, achieving a high Area Under the Curve (AUC) of 0.907. Their study highlighted that extreme climatic variables—specifically minimum temperature and Vapor Pressure Deficit (VPD)—accounted for over 62% of the model's variance. Similarly, in the Mediterranean context, Bouzeraa et al. (2025) achieved exceptional performance (AUC = 0.99) using RF by integrating local meteorological data with global satellite products to map susceptibility in Algeria. In a Türkiye-specific application, Iban and Aksu (2024) applied RF and XGBoost to the İzmir province, achieving an AUC of 0.966 and proving that variables like Land Use/Land Cover (LULC) and wind speed are dominant drivers in the Aegean-Mediterranean transition zone. 

Beyond tree-based models, hybrid metaheuristic optimization has also been explored. Nur et al. (2023) developed hybrid Support Vector Regression (SVR) models optimized with Particle Swarm Optimization (PSO) and Grey Wolf Optimization (GWO) for the Sydney region in Australia. While they achieved a respectable AUC of 0.882, the computational overhead of metaheuristic optimization often limits its real-time operational deployment across massive, nation-wide grid networks.

<div align="center">

**Table 1. Literature comparison of ML-based wildfire studies and the ALAZ system.**

| Study | Region | Best Model | Metric | Regional Models? | FWI Integrated? | XAI / SHAP? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Yang et al. (2026) | China | XGBoost | AUC: 0.907 | No | No | Yes |
| Sinato & Rivas (2026) | Argentina | RF / XGBoost | F1: 93.2% | **Yes** | No | Yes |
| Iban & Aksu (2024) | Türkiye (İzmir) | RF | AUC: 0.966 | No | No | Yes |
| Dong et al. (2022) | Portugal | XGBoost | AUC: 0.805 | No | **Yes** | No |
| Lee et al. (2025) | South Korea | Extra Trees | AUC: 0.839 | No | No | Yes |
| Bouzeraa et al. (2025) | Algeria | RF | AUC: 0.990 | No | No | Yes |
| Moumane et al. (2025) | Morocco | XGBoost | AUC: 0.965 | No | No | Yes |
| Atalay et al. (2024) | Türkiye (Antalya) | FWI (No ML) | Correlation | No | **Yes** | No |
| Nur et al. (2023) | Australia | SVR-PSO | AUC: 0.882 | No | No | No |
| **ALAZ (This Study)** | **Türkiye** | **XGBoost** | **AUC: 0.775** | **Yes** | **Yes** | **Yes** |

</div>

### 2.3. Regional and Territorial Modeling Approaches 
A persistent limitation in the existing literature is the "global model" assumption, where a single ML algorithm is trained across entirely diverse ecological zones. Sinato and Rivas (2026) addressed this critical flaw by introducing "territorial specialization" in Argentina. By tessellating the country using H3 hexagonal grids and training five independent models tailored to specific biogeographical regions, they achieved an average F1-score of 93.2%. Their methodology proved that a model tuned for the arid Patagonia region requires a fundamentally different feature hierarchy than one tuned for tropical zones. 

Similarly, Dong et al. (2022) emphasized the necessity of spatiotemporal heterogeneity in Portugal. Instead of predicting fires based solely on binary burned/unburned areas, they clustered their study area into spatiotemporal blocks, drastically improving the XGBoost model's accuracy from a random baseline to 0.813. These studies firmly establish that fire regimes are highly regionalized and demand geographically distinct models. 

### 2.4. Class Imbalance and Anthropogenic Factors 
Daily wildfire prediction suffers from an extreme class imbalance problem, where non-fire days outnumber fire days by orders of magnitude. Lee et al. (2025) attempted to resolve this in South Korea using the Synthetic Minority Over-sampling Technique (SMOTE) to artificially enforce a 1:1 ratio. While statistically valid, synthetic data generation often fails to capture the true physical boundaries between "safe" and "critical" meteorological states.  

Furthermore, Lee et al. (2025) and Bouzeraa et al. (2025) both strongly criticized the omission of anthropogenic factors in fire prediction. Their findings confirmed that distance to settlements, roads, and human activity metrics often outrank natural topography in predicting ignition. 

### 2.5. Explainable AI (XAI) in Wildfire Research 
As ML models grow in complexity, the "black box" problem limits trust among operational forest managers. To counter this, Explainable AI (XAI), particularly SHapley Additive exPlanations (SHAP), has become an industry standard. Moumane et al. (2025) utilized SHAP in Northern Morocco to reveal crucial physical interactions, proving that concurrent high land surface temperatures and strong winds exponentially increase fire likelihood compared to when these variables act independently. Iban and Aksu (2024) also utilized SHAP TreeExplainer in Türkiye, allowing them to isolate wind speed (>3.5 m/s) and proximity to villages as the absolute triggers for high susceptibility in İzmir. 

### 2.6. Research Gap 
A synthesis of the current literature reveals several critical gaps. First, no existing study has successfully combined spatially independent, regionalized ML models with the traditional FWI system specifically for Türkiye's diverse macro-regions. Second, while studies boast high AUC scores, they rarely calibrate their output margins into true statistical probabilities (e.g., Platt Scaling) or test on strict, out-of-time chronological datasets to simulate real-world deployment. Finally, the physical context of negative sampling in highly imbalanced datasets remains largely unexplored. The ALAZ system proposed in this thesis is designed explicitly to address all of these methodological gaps, culminating in a fully operational web-based Decision Support System.

## 3. MATERIALS AND METHODS 

### 3.1. Study Area 
This study encompasses the forested landscapes of Türkiye, a region highly susceptible to wildfires due to its diverse topography and climatic conditions. To precisely delineate the study area, the CORINE Land Cover 2018 dataset was utilized. The analysis was strictly limited to five specific land cover classes representing forest and semi-natural areas: Broad-leaved forest (311), Coniferous forest (312), Mixed forest (313), Sclerophyllous vegetation (323), and Transitional woodland-shrub (324). This filtering yielded approximately 23.8 million pixels at a 100 m spatial resolution. 

Recognizing that a monolithic model cannot adequately capture the distinct meteorological and ecological dynamics across different climates, the study area was rigorously partitioned into three biogeographical macro-regions defined by the European Environment Agency (EEA) in 2016. These regions represent fundamentally different fire regimes: 

*   **Mediterranean Region (MED):** Accounting for 52% of the study area (~122,500 grid cells), this region experiences hot, dry summers and mild, wet winters. It is historically the most fire-prone area, where prolonged droughts create highly flammable fuel beds. 
*   **Black Sea Region (BLK):** Covering 27% of the study area (~63,600 grid cells), this region is characterized by high humidity and year-round precipitation. Although fires are less frequent, they can be exceptionally severe when rare, rapid atmospheric drying events occur. 
*   **Continental Region (CON):** Comprising 21% of the study area (~49,500 grid cells), this central and eastern region experiences a continental climate with cold winters and hot summers. Fire dynamics here are heavily influenced by late-summer moisture deficits.

<div align="center">
<img width="606" height="315" alt="image" src="https://github.com/user-attachments/assets/9727e7c1-2657-43ad-8a9c-e32292846f0c" />

**Map of Türkiye showing the three biogeographical regions (MED, BLK, CON) and forested areas.**
</div>

### 3.2. Dataset 
A comprehensive, multi-dimensional dataset was constructed to model forest fire risk, integrating meteorological, topographical, vegetation, anthropogenic, and Fire Weather Index (FWI) variables. The utilized features and their descriptions are categorized as follows: 

*   **Meteorological Features (ERA5-Land):** Air temperature (T_Celsius), dewpoint temperature (Dewpoint_C), wind speed and its directional components (Wind_Speed, wind_sin, wind_cos), relative humidity (RH_Percent), surface pressure (SurfPressure), volumetric soil water content (Soil_L1), and vapor pressure deficit (VPD). Additionally, cumulative precipitation over 7, 30, and 90 days, as well as consecutive dry days (Days_Since_Rain) were included to capture drought effects. 
*   **Fire Weather Index (FWI) Components:** Derived from the Canadian Forest Fire Weather Index System, this group includes the Fine Fuel Moisture Code (FFMC), Duff Moisture Code (DMC), Drought Code (DC), Initial Spread Index (ISI), Build-Up Index (BUI), and the final Fire Weather Index (FWI) value, representing the composite fire danger rating. 
*   **Vegetation and Land Cover (MODIS & CORINE):** Normalized Difference Vegetation Index (NDVI) alongside the percentage coverages of tree (perc_tree), shrub/grassland (perc_shrub_grass), agricultural land (perc_agri), and water bodies (perc_water) within each spatial grid cell. 
*   **Topographical Features (SRTM):** Mean elevation, terrain slope (slope_mean), aspect components (northness and eastness), topographic wetness index proxy (twi_proxy), and a chimney index to model wind-terrain interactions in steep valleys. 
*   **Anthropogenic Features (OpenStreetMap):** Proximity metrics including distances to the nearest road, forest track, and settlement, along with their log-transformed values. The days elapsed since the last recorded fire in the exact grid cell (days_since_last_fire) was also utilized. 
*   **Interaction and Temporal Features:** Synthesized interaction terms capturing compounded risks (e.g., FWI × NDVI, VPD × DryDays) and temporal encodings (sine and cosine transformations of the month and day-of-year) to allow the model to learn cyclical seasonality. 

### 3.3. Data Sources 
To construct a comprehensive predictive model that captures the physical, biological, and human factors driving forest fires, data were aggregated from multiple global and regional sources (Table 2). 

<div align="center">
  
**Table 2. Overview of integrated data sources for the ALAZ system.**

| Source | Data Type | Spatial Resolution | Temporal Coverage |
| :--- | :--- | :--- | :--- |
| NASA FIRMS | Active Fire Hotspots (MODIS C6.1 + VIIRS S-NPP C2) | 1 km / 375 m | 2008–2025 |
| ERA5-Land | Meteorological reanalysis (T, RH, Wind, Precipitation, Soil Moisture) | 0.1° (~9 km) | 2008–2025 |
| MODIS MOD13Q1 | Normalized Difference Vegetation Index (NDVI) | 250 m | 2008–2025 |
| SRTM | Digital Elevation Model (Elevation, Slope, Aspect) | 30 m | Static |
| CORINE 2018 | Land Cover Classification | 100 m | 2018 |
| OpenStreetMap | Vector networks (Roads, Forest Roads, Settlements) | Vector | 2024 |
| EEA 2016 | Biogeographical Regions boundaries | Vector | 2016 |
| EFFIS | Burnt Area Polygons (>30 ha) | 250 m | 2008–2025 |
</div>
<div align="center">
<img width="602" height="374" alt="image" src="https://github.com/user-attachments/assets/360ee5a8-6326-4431-b9c6-b8811f883cab" />

**Flow diagram illustrating the data source pipeline and integration process.**
</div>
### 3.4. Spatial Tessellation and Regionalization 
Working with raw raster data often introduces boundary distortions and inconsistencies when integrating datasets of varying spatial resolutions. To overcome this, the study area was tessellated using Uber’s H3 Hierarchical Hexagonal Engine at Resolution 8. Hexagonal grids are mathematically superior to square grids for spatial analysis because all neighboring cells are equidistant from the center, which minimizes spatial distortion and standardizes neighborhood operations (Sinato & Rivas, 2026).  

The tessellation process resulted in 235,621 unique hexagonal grid cells, each covering approximately 0.74 km². The CORINE pixels, SRTM topographic data, and OpenStreetMap vectors were spatially aggregated into these discrete hexagonal units. Each H3 cell was then strictly assigned to one of the three macro-regions (MED, BLK, or CON) based on the EEA 2016 spatial boundaries.
<div align="center">
<img width="600" height="326" alt="image" src="https://github.com/user-attachments/assets/3953c34c-04e2-44ae-84d1-a4f514a9d0bf" />

**Visualization of the H3 hexagonal grid overlay on the forested terrain.**
</div>
### 3.5. Fire Event Database 
The dependent variable for the machine learning models—fire occurrence—was constructed from a historical database of 15,435 unique fire events spanning from 2008 to 2025. This dataset was curated by spatially joining NASA FIRMS active fire point data (from both MODIS and VIIRS instruments) with EFFIS burnt area polygons. Spatiotemporal deduplication was rigorously applied to ensure that multiple satellite detections of the same fire event on the same day within the same grid cell were merged into a single positive instance. 

To categorically prevent temporal data leakage and ensure the model's forward-looking operational validity, an absolute chronological split was enforced: 
*   **Training Set:** 2008–2021 
*   **Validation Set:** 2022 (Used for hyperparameter tuning and probability calibration) 
*   **Test Set:** 2023–2025 (Used exclusively for final model evaluation)
<div align="center">
<img width="597" height="365" alt="image" src="https://github.com/user-attachments/assets/a865fd20-0e9d-44a9-b1ee-0d682459ccdc" />

**Distribution of fire events by year (2008-2025)**
</div>
### 3.6. Feature Engineering 
The models ingest a highly engineered 36-dimensional physical feature space designed to capture the complex, non-linear interactions that lead to ignition. The features are grouped into five primary domains, plus specific temporal and interaction terms. 

1.  **Meteorology:** Derived from ERA5-Land hourly reanalysis data, extracted precisely at noon (10:00 UTC / 13:00 TSİ) to represent peak daily fire danger. Variables include 2m air temperature, dewpoint temperature, relative humidity, wind speed (derived from U and V components), surface pressure, volumetric soil water (0–7 cm depth), Vapor Pressure Deficit (VPD), cumulative precipitation (7-day, 30-day, 90-day), and days since last rain. 
2.  **Fire Weather Index (FWI):** To incorporate established physical fire science into the machine learning framework, the components of the Canadian Forest Fire Weather Index (Van Wagner, 1987) were computed at the grid level using the ERA5-Land inputs. The computed indices include the Fine Fuel Moisture Code (FFMC), Duff Moisture Code (DMC), Drought Code (DC), Initial Spread Index (ISI), Build-Up Index (BUI), and the final FWI. 
3.  **Phenology/Vegetation:** Plant health and moisture stress act as proxy indicators for fuel flammability. This is quantified using the Normalized Difference Vegetation Index (NDVI) extracted from the MODIS Terra MOD13Q1 16-day product. 
4.  **Topography:** The physical landscape heavily influences fire spread and microclimates. Derived from the SRTM 30m DEM, features include mean elevation, terrain slope, northness (cosine of aspect), eastness (sine of aspect), a Topographic Wetness Index (TWI) proxy, and a custom Chimney Index representing topographic channeling effects in steep valleys. 
5.  **Anthropogenic Variables:** Wildfires are predominantly human-caused events, making anthropogenic proximity a critical predictive factor (Bouzeraa et al., 2025). Using OpenStreetMap data, features such as distance to any road, distance to forest roads, and distance to settlements were calculated. Additionally, the variable `days_since_last_fire` was engineered to track the localized accumulation of untreated forest fuel loading. 
6.  **Interactions and Temporal Encodings:** To assist the models in discovering complex trigger conditions, several physical interaction terms were engineered, notably `I_FWI_x_NDVI` (capturing the alignment of extreme weather with highly stressed vegetation) and `I_FWI_x_Wind`. To capture seasonality without the model memorizing specific months, continuous sine and cosine transformations of the month and day-of-year (DOY) were applied.
<div align="center">
<img width="597" height="553" alt="image" src="https://github.com/user-attachments/assets/24e4b434-fe7e-4a06-a88b-41802a7de093" />

**Flowchart demonstrating the computation of the FWI system components from meteorological variables.**
</div>
### 3.7. Negative Sampling Architecture 
Forest fires are exceedingly rare events at a daily grid level. In the dataset, the true daily fire prevalence is approximately 1:100,000. Training a machine learning model on purely random samples from such a heavily imbalanced dataset leads to the "Accuracy Paradox," where the model achieves near-perfect accuracy simply by continuously predicting "no fire," failing to learn pre-ignition behaviors. 

To enforce rigorous learning and ensure the model discriminates based on physical conditions rather than statistical imbalances, negative (non-fire) data points were deliberately sampled using six physically meaningful profiles. Through a grand sweep of 120 experimental trials, different negative sampling ratios (ranging from 1:1 to 1:10) and strategies were evaluated per region: 

1.  **Opposite Season (Type 1):** Sampling the exact location 180 days away from a fire event, forcing the model to learn extreme climatic contrasts. 
2.  **Breaking Point (Type 2):** Sampling the location 2 to 5 days prior to an actual fire, forcing the model to differentiate between "dangerous but safe" and "critical ignition" conditions. 
3.  **Spatial Neighbor (Type 3):** Sampling adjacent unburned cells on the day of a fire, capturing spatial gradients and topographical firebreaks. 
4.  **Intra-Season (Type 4):** Sampling ±30 days from a fire, isolating short-term meteorological fluctuations. 
5.  **Historical Recurrence (Type 5):** Sampling the exact location exactly one year prior (-365 days), accounting for annual cyclic similarities. 
6.  **Regional Reference (Type 6):** Sampling distant cells within the same region on the day of a fire, providing a regional meteorological baseline.
<div align="center">
  
**Table 3. Overview of the six physically meaningful negative sampling strategies utilized in the ALAZ framework.**

| Strategy Name | Temporal Condition | Spatial Condition | Physical Purpose / Rationale |
| :--- | :--- | :--- | :--- |
| Type 1: Opposite Season | ± 180 Days | Exact Same Location | Forces the model to learn extreme seasonal climatic contrasts (e.g., Summer vs. Winter). |
| Type 2: Breaking Point | -2 to -5 Days | Exact Same Location | Teaches the model to identify the critical "tipping point" just before ignition occurs. |
| Type 3: Spatial Neighbor | Exact Same Day | Adjacent Cells | Captures spatial gradients and natural firebreaks to distinguish safe vs. dangerous adjacent zones. |
| Type 4: Intra-Season | ± 30 Days | Exact Same Location | Isolates short-term meteorological fluctuations and heatwaves within the same fire season. |
| Type 5: Historical Recurrence | - 365 Days | Exact Same Location | Accounts for annual cyclic similarities and long-term drought accumulations. |
| Type 6: Regional Reference | Exact Same Day | Random in Region | Establishes a broad regional baseline for extreme weather days that did not result in fires. |
</div>
### 3.8. Model Architecture and Calibration 
The ALAZ system relies on XGBoost (Extreme Gradient Boosting), a decision-tree-based ensemble algorithm proven highly effective in capturing complex, non-linear relationships in tabular environmental data. Given the established spatial heterogeneity, three independent regional models were trained (MED, CON, and BLK) rather than a single monolithic national model.  

Hyperparameter tuning was conducted using the Optuna framework, leveraging Bayesian optimization with Tree-structured Parzen Estimator (TPE) to maximize the F1-Score on the 2022 validation set.  

A critical flaw in many ML-based wildfire studies is presenting raw, uncalibrated margin scores as operational "probabilities," leading to severe overconfidence or underconfidence in real-world deployment. To correct this, the ALAZ models were subjected to Platt Scaling (Sigmoid Calibration) on the validation set. This transformation ensures that if the system outputs a 70% risk value, there is a true 70% statistical probability of a fire occurring under those conditions. 

### 3.9. Evaluation Metrics and Explainability 
The models were evaluated strictly on the unseen 2023–2025 test dataset to simulate true operational deployment. Performance was quantified using Area Under the Receiver Operating Characteristic Curve (AUC-ROC), Precision-Recall AUC (PR-AUC), F1-Score, Precision, and Recall. The reliability of the calibrated probabilities was evaluated using the Brier Score, where a lower score indicates better calibration. 

To overcome the "black box" nature of complex ensemble models, the framework integrates SHapley Additive exPlanations (SHAP). By utilizing TreeExplainer, SHAP summary and dependence plots were generated to interpret regional feature importance, providing actionable insights into which specific climatic, vegetation, or human factors drive fire risk in each geographical zone. 

### 3.10. Web-Based Decision Support System 
To bridge the gap between academic research and actionable forest management, the trained regional models were deployed within a high-performance, web-based Decision Support System (DSS). The backend, built with FastAPI and Python, performs real-time NetCDF processing of ERA5 data, calculates the Van Wagner FWI components on-the-fly, merges the data with static topologies and vegetation medians, and executes the regional XGBoost inferences. 

The frontend is constructed using Vanilla JavaScript, MapLibre GL for the base maps, and deck.gl for rendering the 235,621 H3 hexagons. The DSS supports three operational modes: a traditional FWI-only view utilizing EFFIS standard thresholds, the ALAZ ML predictive view with calibrated probability thresholds, and a synchronous side-by-side comparison mode. The interface includes interactive tools for timeline selection and detailed grid-level inspection of all meteorological and topological inputs.

<p align="center">
  <img width="600" height="466" alt="image" src="https://github.com/user-attachments/assets/60cfcebc-0034-4d4f-8149-c3a4fdf5ab13" />
  <br>
  <em>(a)</em>
</p>

<p align="center">
  <img width="601" height="291" alt="image" src="https://github.com/user-attachments/assets/4103368f-31d8-4122-9a4f-8cc4a8cafbf5" />
  <br>
  <em>(b)</em>
</p>

<p align="center">
  <img width="600" height="295" alt="image" src="https://github.com/user-attachments/assets/c2a49075-1165-479d-b5ff-b8d89673fb13" />
  <br>
  <em>(c)</em>
</p>

<p align="center">
  <img width="601" height="295" alt="image" src="https://github.com/user-attachments/assets/c25b481c-a17e-4e8c-b287-84d04015d247" />
  <br>
  <em>(d)</em>
</p>

<p align="center">
  <img width="603" height="294" alt="image" src="https://github.com/user-attachments/assets/cd9352f6-6a0c-4076-b6bf-262bf4578a05" />
  <br>
  <em>(e)</em>
</p>

<p align="center">
  <em>Figure 6. Screenshots of the Web DSS interface showing FWI mode, ALAZ mode, and side-by-side comparison capabilities. (a) Choosing Mode (b) FWI Mode (c) ALAZ Mode (d) Comparison Mode (e) Grid Features</em>
</p>

## 4. RESULTS AND DISCUSSION 

### 4.1. Negative Sampling Experiment Results 
The ALAZ system's robustness heavily relies on resolving the extreme class imbalance through physically meaningful negative sampling. A comprehensive hyperparameter and strategy sweep consisting of 120 experiments (4 regions × 6 strategies × 5 ratios) was conducted. Table 4 summarizes the highest-performing negative sampling strategies for each macro-region.

<div align="center">

**Table 4. Best performing negative sampling strategies by region (120-experiment sweep).**

| Region | Best Strategy | Best Ratio | AUC-ROC | F1-Score | Composite Score |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MED** | S6_Full (Composite) | 1:3 | 0.765 | 0.316 | 0.585 |
| **CON** | S3_Stratified | 1:2 | 0.714 | 0.276 | 0.539 |
| **BLK** | S2_Mixed | 1:6 | 0.746 | 0.332 | 0.581 |
| **GLOBAL** | S6_Full (Composite) | 1:3 | 0.754 | 0.310 | 0.577 |

</div>

The experimental sweep revealed that negative sampling ratio saturation typically occurs between 1:3 and 1:4. Beyond this threshold, injecting additional negative samples yielded diminishing returns and occasionally degraded F1-Scores. Notably, the S4_HighFWI strategy (sampling negatives exclusively from high fire-weather days) consistently performed the worst across all regions (AUC ~0.56–0.62). This empirical failure indicates that intentionally forcing the model to distinguish between extreme-weather fire days and extreme-weather non-fire days artificially destroys discriminability, confusing the decision boundaries. 

<p align="center">
  <img width="636" height="257" alt="image" src="https://github.com/user-attachments/assets/23b17f84-f8bf-4230-a1b7-f468c3a1d166" />
  <br>
  <em>(a)</em>
</p>

<p align="center">
  <img width="618" height="252" alt="image" src="https://github.com/user-attachments/assets/dcb8f110-f1a8-488a-bd1f-6ca79136b011" />
  <br>
  <em>(b)</em>
</p>

<p align="center">
  <em>Figure 7. AUC heatmap demonstrating model performance across 6 negative sampling strategies and 5 negative-to-positive ratios. (a) MED and CON (b) BLK and GLOBAL</em>
</p>

### 4.2. Feature Engineering Impact 
Through Bayesian hyperparameter optimization via Optuna, the baseline 26-feature dataset was progressively expanded. Phase 1 involved adding critical interaction terms (e.g., FWI×NDVI, FWI×Wind) and cyclical temporal encodings. Phase 2 further integrated topographical variables such as the Chimney Index and TWI proxy. Table 5 illustrates the AUC improvement across the feature engineering phases.

<div align="center">

**Table 5. AUC-ROC improvements across feature engineering phases.**

| Region | M10 Baseline (26 Features) | Phase 1 (32 Features) | Phase 2 (36 Features) | Total Improvement |
| :--- | :--- | :--- | :--- | :--- |
| **MED** | 0.743 | 0.755 | 0.756 | **+1.3%** |
| **CON** | 0.675 | 0.716 | 0.720 | **+4.5%** |
| **BLK** | 0.712 | 0.785 | 0.759 | **+4.7%** |

</div>

(Note: The BLK region exhibited slight overfitting in Phase 2, hence Phase 1 features were favored for final BLK deployment). 

The introduction of interaction terms in Phase 1 yielded the most substantial improvements, particularly in the Black Sea (BLK) region, where capturing the rare confluence of dry winds and sudden Vapor Pressure Deficit (VPD) spikes is critical for predicting ignition. 
 
### 4.3. Model Comparison 
To validate the choice of Gradient Boosting, the final XGBoost regional models were evaluated against an optimized Support Vector Machine (SVM with RBF kernel) and an Artificial Neural Network (Multi-Layer Perceptron, 128-64-32 architecture). All models were evaluated on the strict chronologically split 2023–2025 test dataset to prevent temporal leakage. 

<div align="center">

**Table 6. Performance comparison of XGBoost, SVM, and ANN on the 2023-2025 Test Set.**

| Region | Model | AUC-ROC | F1-Score | Brier Score |
| :--- | :--- | :--- | :--- | :--- |
| **MED** | **XGBoost** | **0.759** | **0.354** | **0.088** |
| MED | SVM | 0.685 | 0.283 | 0.094 |
| MED | ANN | 0.673 | 0.107 | 0.097 |
| **CON** | **XGBoost** | **0.719** | **0.271** | **0.088** |
| CON | SVM | 0.690 | 0.265 | 0.088 |
| CON | ANN | 0.690 | 0.018 | 0.089 |
| **BLK** | **XGBoost** | **0.775** | **0.384** | **0.088** |
| BLK | SVM | 0.614 | 0.216 | 0.097 |
| BLK | ANN | 0.589 | 0.000 | 0.099 |

</div>

XGBoost consistently outperformed SVM and ANN across all macro-regions in both AUC and F1 metrics. The ANN exhibited severe failure in the BLK region (F1=0.000), primarily due to its inability to handle the extreme non-linearities and rare fire prevalence inherent to humid climates.

<p align="center">
  <img width="619" height="455" alt="image" src="https://github.com/user-attachments/assets/4869fc18-c73e-461b-9fb4-3559a1e3c0cc" />
  <br>
  <em>(a)</em>
</p>

<p align="center">
  <img width="624" height="452" alt="image" src="https://github.com/user-attachments/assets/1d83caf3-1b74-468a-99ba-2e8f457fe10f" />
  <br>
  <em>(b)</em>
</p>

<p align="center">
  <img width="614" height="453" alt="image" src="https://github.com/user-attachments/assets/489d28c7-01ba-467a-945b-9d9a25d36019" />
  <br>
  <em>(c)</em>
</p>

<p align="center">
  <strong>Figure 8. Receiver Operating Characteristic (ROC) curves for the regional XGBoost models (a) MED, (b) CON, (c) BLK.</strong>
</p>

### 4.4. Probability Calibration 
A cornerstone of the ALAZ system is its operational reliability. Raw ML margins are unsuited for emergency response thresholds. Following Platt Scaling on the validation set, the Brier Scores for all three XGBoost models dropped below 0.088 on the test set. 

<p align="center">
  <img width="615" height="528" alt="image" src="https://github.com/user-attachments/assets/2c92edf4-0abc-4ebd-a11a-7aec6d5078a4" />
  <br><br>
  <strong>Figure 9. Calibration curves (reliability diagrams) demonstrating the effect of Platt Scaling on the regional XGBoost models.</strong>
</p>

The calibration ensures that when the ALAZ DSS displays a "High Risk (>50%)" alert, it represents a mathematically verified probability density, significantly reducing false-alarm fatigue among forest managers compared to the traditionally wide "Very Extreme" FWI categories. 

### 4.5. Explainable AI — Regional SHAP Analysis 
Understanding why a model predicts a fire is as critical as the prediction itself. TreeExplainer SHAP (SHapley Additive exPlanations) was applied to the final XGBoost models, revealing that the drivers of fire differ fundamentally across Türkiye's biogeographical zones.

<p align="center">
  <img width="618" height="494" alt="image" src="https://github.com/user-attachments/assets/693d2994-72fd-42ac-8cb2-7e3904361a5c" />
  <br>
  <em>(a)</em>
</p>

<p align="center">
  <img width="629" height="484" alt="image" src="https://github.com/user-attachments/assets/25826abc-2967-411b-8de4-226302008811" />
  <br>
  <em>(b)</em>
</p>

<p align="center">
  <img width="623" height="481" alt="image" src="https://github.com/user-attachments/assets/80016710-cad8-4073-8db9-1d2f0c0518f0" />
  <br>
  <em>(c)</em>
</p>

<p align="center">
  <strong>Figure 10. SHAP summary plots for the regional models. (a) MED, (b) CON, (c) BLK</strong>
</p>

*   **Mediterranean (MED) Drivers:** The engineered interaction term `I_FWI_x_NDVI` was the most dominant feature (22.3% of total impact). This physically translates to fires triggering when extreme atmospheric danger (high FWI) perfectly aligns with highly moisture-stressed vegetation (low NDVI). 
*   **Continental (CON) Drivers:** The `FWI_Final` and `FWI_DC` (Drought Code) were the most critical variables (18.7%). The heavy reliance on DC indicates that fires in the Continental region are driven by long-term, deep-soil moisture deficits rather than sudden daily weather shifts. 
*   **Black Sea (BLK) Drivers:** The `FWI_FFMC` (Fine Fuel Moisture Code) and Vapor Pressure Deficit (VPD) were dominant. Because the BLK region is generally humid, fires only ignite when rare, rapid atmospheric drying events instantly dry the surface-level fine fuels. 

### 4.6. Anthropogenic Impact Discussion 
A vital observation across all SHAP analyses is the universal prominence of anthropogenic features. Variables such as `distance_to_settlement` and `days_since_last_fire` consistently ranked within the Top 5 most influential features globally. Ablation studies during Phase 2 demonstrated that removing anthropogenic variables decreased regional AUCs by an average of 3.5%. This statistically validates the hypothesis that Mediterranean forest fires are not solely meteorological events, but rather intense human-environment interaction anomalies (Bouzeraa et al., 2025; Lee et al., 2025). The ALAZ system succeeds precisely because it forces the XGBoost models to weigh human accessibility alongside climate stress. 

### 4.7. Discussion and Comparison with Literature 
The performance of the developed regional machine learning models was evaluated independently for the Black Sea (BLK), Continental (CON), and Mediterranean (MED) regions. The resulting metrics substantiate the hypothesis that fire dynamics vary significantly across geographic zones, validating the proposed regional methodology: 

*   **Black Sea Region (BLK):** The model achieved the highest overall Accuracy (**83.29%**) and Specificity (**87.68%**) among all regions, with a ROC-AUC score of **0.775**. Due to the high vegetation moisture and infrequent, heterogeneous nature of fires in the Black Sea biome, the model's ability to minimize false alarms was maximized. However, the Recall remained comparatively modest at **47.54%**. 
*   **Continental Region (CON):** For the Continental zone, the model yielded an Accuracy of **78.83%** and a ROC-AUC of **0.719**. The transitional climate, sparse forest cover, and variable wind dynamics of this region resulted in an F1-Score of 0.271 and a Recall of **38.89%**, reflecting the inherent difficulty of modeling scattered fire occurrences in inland steppes. 
*   **Mediterranean Region (MED):** In the Mediterranean region, which represents the highest fire risk and data density in Türkiye, the model attained an Accuracy of **77.63%** and a ROC-AUC of **0.759**. The most remarkable finding for the MED region is its Recall value of **57.30%**, the highest among all zones. The model successfully identified 1,315 actual fire events (True Positives). This elevated sensitivity is particularly critical for Early Warning Decision Support Systems, demonstrating exceptional operational reliability in the most fire-prone region. 

**Comparison with Literature** 

A review of recent literature on forest fire susceptibility modeling reveals a predominant tendency to train a single machine learning model (e.g., XGBoost, SVM, ANN) generalized across an entire country or large geographic extent. While these standard approaches frequently report overall accuracies between 75% and 85%, they often neglect the critical issue of class imbalance, leading to suboptimal sensitivity (recall) in detecting actual fire events. Furthermore, in geographically and climatologically diverse countries like Türkiye, which encompasses Mediterranean, Continental, and Black Sea biomes, a generalized "one-size-fits-all" model cannot adequately adapt to local fire dynamics. 

In contrast to conventional literature, this study proposes a Regional Machine Learning Approach. By partitioning the study area into distinct ecological zones (BLK, CON, MED), region-specific models were trained to prioritize the most relevant local risk factors. As demonstrated by our results, the regional stratification profoundly influences model behavior. In areas with distinct and regular fire regimes like the Mediterranean, the model excels in capturing true fire events (Recall). Conversely, in regions with atypical fire patterns like the Black Sea, the model naturally prioritizes minimizing false alarms (Specificity). These divergent performance profiles demonstrate that deploying climate-specific regional machine learning models is far more effective and realistic than relying on a single global architecture, addressing a significant gap in the current literature.

## 5. CONCLUSIONS 

This thesis introduced ALAZ, a novel, regionalized Machine Learning and Climate Index-Based Forest Fire Early Warning Decision Support System designed explicitly for the biogeographical realities of Türkiye. Through extensive data engineering, the integration of classical fire science with advanced gradient boosting, and rigorous physical evaluation, several critical conclusions were drawn: 

1.  **Validation of Territorial Specialization:** The hypothesis that a single monolithic model cannot effectively predict fires across diverse climates was strongly validated. By partitioning Türkiye into Mediterranean, Black Sea, and Continental macro-regions, the independent XGBoost models successfully learned fundamentally different predictive hierarchies, achieving robust out-of-time test metrics (Mediterranean AUC: 0.759, Black Sea AUC: 0.775). 
2.  **Synergy of FWI and Machine Learning:** The mathematical integration of the traditional Canadian FWI system (FFMC, DMC, DC, etc.) into the XGBoost feature space proved highly effective. While traditional FWI measures the potential for combustion, the ML algorithm successfully learned when that potential translates into actual ignition, particularly when extreme FWI values align with severe vegetation moisture stress (NDVI). 
3.  **The Necessity of Anthropogenic Context:** Explainable AI (SHAP) analysis categorically proved that forest fires in Türkiye are not exclusively meteorological phenomena. Human accessibility—quantified through distance to settlements and road networks—consistently emerged as a dominant predictive feature across all regions. Removing these features degraded model accuracy, cementing the fact that modern early warning systems must integrate human-environment interaction. 
4.  **Negative Sampling Paradigm:** A comprehensive 120-experiment sweep demonstrated that random negative sampling in extremely imbalanced daily datasets (1:100,000) causes models to fail operationally. Using physically meaningful negative profiles—particularly Composite sampling (S6_Full) and Stratified spatial sampling (S3)—forces the model to discern true ignition triggers rather than merely recognizing safe weather. 
5.  **Operational Readiness:** Unlike many academic studies that output raw, uncalibrated scores, the ALAZ models were successfully subjected to Platt Scaling, achieving Brier Scores below 0.088. This statistical reliability enabled the successful deployment of the models into a high-performance, real-time Web Decision Support System (DSS) with dynamic 3D hexagonal rendering. 

### Future Work 
While ALAZ establishes a robust foundation for regional fire prediction, future iterations should explore the integration of Shared Socioeconomic Pathways (SSP) to project future climate change susceptibility scenarios. Furthermore, transitioning from 250m MODIS NDVI to 10m Sentinel-2 multispectral data would provide higher-resolution vegetation stress tracking. Finally, establishing real-time data pipelines with the General Directorate of Forestry (OGM) and developing a mobile application interface would maximize the system's operational impact on the ground. 

## REFERENCES 
*   Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M. (2019). Optuna: A Next-generation Hyperparameter Optimization Framework. Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, 2623–2631. 
*   Atalay, H., Dervisoglu, A., & Sunar, A. F. (2024). Exploring Forest Fire Dynamics: Fire Danger Mapping in Antalya Region, Türkiye. ISPRS International Journal of Geo-Information, 13(3), 74. https://doi.org/10.3390/ijgi13030074 
*   Bouzeraa, Y., Bouchemal, N., Djaaboub, S., Hristov, G., & Zahariev, P. (2025). Machine learning-based wildfire susceptibility mapping: A GIS-integrated predictive framework. Applied Sciences, 15(22), 12188. https://doi.org/10.3390/app152212188 
*   Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 785–794. 
*   Dong, H., Wu, H., Sun, P., & Ding, Y. (2022). Wildfire Prediction Model Based on Spatial and Temporal Characteristics: A Case Study of a Wildfire in Portugal's Montesinho Natural Park. Sustainability, 14(16), 10107. https://doi.org/10.3390/su141610107 
*   European Environment Agency (EEA). (2016). Biogeographical regions dataset. Retrieved from EEA Data Hub. 
*   Giglio, L., Schroeder, W., & Justice, C. O. (2016). The collection 6 MODIS active fire detection algorithm and fire products. Remote Sensing of Environment, 178, 31–41. 
*   Iban, M. C., & Aksu, O. (2024). SHAP-Driven Explainable Artificial Intelligence Framework for Wildfire Susceptibility Mapping Using MODIS Active Fire Pixels: An In-Depth Interpretation of Contributing Factors in Izmir, Türkiye. Remote Sensing, 16(15), 2842. https://doi.org/10.3390/rs16152842 
*   Lee, C., Choi, E. H., Han, Y., & Lee, Y. (2025). Year-round daily wildfire prediction and key factor analysis using machine learning: A case study of Gangwon State, South Korea. Scientific Reports, 15, 29910. https://doi.org/10.1038/s41598-025-15508-5 
*   Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. Advances in Neural Information Processing Systems, 30. 
*   Moumane, A., Al Karkouri, A., Elmotawakkil, A., Alkhuraiji, W. S., Rebouh, N. Y., & Youssef, Y. M. (2025). Advancing wildfire susceptibility mapping through machine learning and SHapley Additive exPlanations-integrated geospatial analysis in Northern Morocco's Mediterranean region. Frontiers in Forests and Global Change, 8, 1705341. https://doi.org/10.3389/ffgc.2025.1705341 
*   Muñoz Sabater, J. (2019). ERA5-Land hourly data from 1950 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS) 
*   Nur, A. S., Kim, Y. J., Lee, J. H., & Lee, C.-W. (2023). Spatial prediction of wildfire susceptibility using hybrid machine learning models based on support vector regression in Sydney, Australia. Remote Sensing, 15(3), 760. https://doi.org/10.3390/rs15030760 
*   Platt, J. (1999). Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. Advances in Large Margin Classifiers, 10(3), 61–74. 
*   Sinato, F., & Rivas, C. (2026). Territorially-Specialized Machine Learning Models for Wildfire Risk Prediction Across Argentina Using Satellite Data and H3 Hexagonal Grids. GeoAlertAR Preprint. 
*   Uber Engineering. (2018). H3: Uber's Hexagonal Hierarchical Spatial Index. Uber Technologies. 
*   Van Wagner, C. E. (1987). Development and structure of the Canadian Forest Fire Weather Index System (Forestry Technical Report 35). Canadian Forestry Service. 
*   Yang, C., Yao, P., Wang, Q., Wang, S., Xing, D., Wang, Y., & Zhang, J. (2026). XGBoost-Based Susceptibility Model Exhibits High Accuracy and Robustness in Plateau Forest Fire Prediction. Forests, 17(1), 74. https://doi.org/10.3390/f17010074
