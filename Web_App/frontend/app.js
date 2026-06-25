// ===============================================
// ALAZ | KULLANICI ARAYÜZÜ MOTORU v2.0
// Bilimsel Renk Skalası + Lejant + Grid Detay
// ===============================================

const TR_CENTER = { longitude: 35.2433, latitude: 38.9637, zoom: 5.0, pitch: 0, bearing: 0 };

const TURKEY_BOUNDS = [
    [25.0, 35.0],
    [45.5, 42.5]
];

// --- DURUM YÖNETİMİ ---
let currentData = [];
let availableDates = [];
let currentMode = "fwi";

// --- MAP NESNELERİ ---
let mapSingle, overlaySingle;
let mapLeft, overlayLeft, mapRight, overlayRight;
let isSyncing = false;

// ===============================================
// BİLİMSEL RENK SKALASI (Gradient Geçişli)
// ===============================================
function lerp(a, b, t) { return a + (b - a) * Math.max(0, Math.min(1, t)); }

function lerpColor(c1, c2, t, alpha) {
    return [
        Math.round(lerp(c1[0], c2[0], t)),
        Math.round(lerp(c1[1], c2[1], t)),
        Math.round(lerp(c1[2], c2[2], t)),
        alpha
    ];
}

const C_GREEN   = [76, 175, 80];
const C_YELLOW  = [255, 193, 7];
const C_ORANGE  = [255, 152, 0];
const C_RED     = [244, 67, 54];
const C_PURPLE  = [156, 39, 176];
const C_DPURPLE = [90, 0, 100];

// ── FWI ("Sunum" Skalası) ──
// Güvenli < 7 | Dikkat 7-9.5 | Yüksek 9.5-12 | Kritik 12+
function getColorFWI(fwi, alpha) {
    if (fwi == null || fwi <= 0)  return [...C_GREEN, alpha];
    if (fwi < 7.0)   return lerpColor(C_GREEN, C_YELLOW,  fwi / 7.0, alpha);
    if (fwi < 9.5)   return lerpColor(C_YELLOW, C_ORANGE,  (fwi - 7.0) / 2.5, alpha);
    if (fwi < 12.0)  return lerpColor(C_ORANGE, C_RED,     (fwi - 9.5) / 2.5, alpha);
    return lerpColor(C_RED, C_PURPLE, Math.min((fwi - 12.0) / 10.0, 1), alpha);
}

// ── ALAZ ("Sunum" Skalası) ──
// Güvenli < %4.5 | Dikkat %4.5-7.0 | Yüksek Risk %7.0-10.0 | Kritik %10.0+
function getColorALAZ(prob, alpha) {
    if (prob == null || prob <= 0) return [...C_GREEN, alpha];
    if (prob < 4.5)   return lerpColor(C_GREEN, C_YELLOW,  prob / 4.5, alpha);
    if (prob < 7.0)   return lerpColor(C_YELLOW, C_ORANGE,  (prob - 4.5) / 2.5, alpha);
    if (prob < 10.0)  return lerpColor(C_ORANGE, C_RED,     (prob - 7.0) / 3.0, alpha);
    return lerpColor(C_RED, C_PURPLE, Math.min((prob - 10.0) / 10.0, 1), alpha);
}

// Kategori Adları (Tooltip ve Detay Paneli İçin)
function getFWICategory(fwi) {
    if (fwi == null || fwi < 7.0) return 'Güvenli';
    if (fwi < 9.5) return 'Dikkat';
    if (fwi < 12.0) return 'Yüksek Risk';
    return 'Kritik';
}

function getALAZCategory(prob) {
    if (prob == null || prob < 4.5) return 'Güvenli';
    if (prob < 7.0) return 'Dikkat';
    if (prob < 10.0) return 'Yüksek Risk';
    return 'Kritik';
}

// CORINE Arazi Sınıfları Sözlüğü
const CORINE_LABELS = {
    311: 'Geniş Yapraklı Orman', 312: 'İğne Yapraklı Orman', 313: 'Karışık Orman',
    321: 'Doğal Çayırlar', 322: 'Maki/Çalılık', 323: 'Sklerofil Bitki Örtüsü',
    324: 'Geçiş Ormanı/Çalılık', 331: 'Plaj/Kumul', 332: 'Çıplak Kayalık',
    333: 'Seyrek Bitki Örtüsü', 334: 'Yanmış Alan',
    211: 'Sulanmayan Tarım', 231: 'Mera', 243: 'Doğal Bitki Örtülü Tarım'
};

// ===============================================
// HARİTA ALTYAPISI (Esri Uydu + MapLibre)
// ===============================================
const ESRI_SATELLITE_STYLE = {
    "version": 8,
    "sources": {
        "satellite": {
            "type": "raster",
            "tiles": ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"],
            "tileSize": 256,
            "attribution": "© Esri World Imagery"
        }
    },
    "layers": [{ "id": "satellite", "type": "raster", "source": "satellite" }]
};

function createMap(containerId) {
    return new maplibregl.Map({
        container: containerId,
        style: ESRI_SATELLITE_STYLE,
        bounds: TURKEY_BOUNDS,
        maxBounds: TURKEY_BOUNDS,
        center: [TR_CENTER.longitude, TR_CENTER.latitude],
        zoom: TR_CENTER.zoom,
        interactive: true
    });
}

// ===============================================
// HOVER TOOLTIP (Fare Üzerine Gelince)
// ===============================================
function handleTooltip(info) {
    const tooltip = document.getElementById('tooltip');
    if (info.object) {
        const d = info.object;
        tooltip.style.display = 'block';
        tooltip.style.left = (info.x + 15) + 'px';
        tooltip.style.top  = (info.y + 15) + 'px';

        let html = `<b>Grid:</b> ${d.GRID_ID}<br>`;

        if (d.fwi_value !== undefined && d.fwi_value !== null) {
            const cat = getFWICategory(d.fwi_value);
            html += `<b>FWI:</b> ${d.fwi_value.toFixed(1)} → <span style="color:#66fcf1">${cat}</span><br>`;
        }
        if (d.risk_percent !== undefined && d.risk_percent !== null) {
            const cat = getALAZCategory(d.risk_percent);
            html += `<b>ALAZ:</b> %${d.risk_percent.toFixed(1)} → <span style="color:#66fcf1">${cat}</span>`;
        }

        tooltip.innerHTML = html;
    } else {
        tooltip.style.display = 'none';
    }
}

// ===============================================
// CLICK → GRİD DETAY PANELİ (Tıklayınca Açılır)
// ===============================================
async function handleGridClick(info) {
    if (!info.object) return;

    const gridId = info.object.GRID_ID;
    const date = document.getElementById('current-date-label').innerText;
    const panel = document.getElementById('detail-panel');
    const content = document.getElementById('detail-content');

    panel.classList.remove('hidden');
    content.innerHTML = '<div class="spinner" style="margin:20px auto"></div>';

    try {
        const res = await fetch(
            `http://127.0.0.1:8000/api/grid-detail?grid_id=${gridId}&date=${date}&mode=${currentMode}`
        );
        const data = await res.json();

        let html = '';

        // ── Grid Kimliği ──
        html += `<div class="detail-section">
            <div class="detail-header">📍 Grid Kimliği</div>
            <div class="detail-row"><span>H3 ID</span><span class="detail-val">${gridId}</span></div>
            <div class="detail-row"><span>Tarih</span><span class="detail-val">${date}</span></div>
        </div>`;

        // ── Topoğrafya ──
        if (data.topography) {
            const t = data.topography;
            const corineName = CORINE_LABELS[t.corine_class] || `Kod: ${t.corine_class}`;
            html += `<div class="detail-section">
                <div class="detail-header">🏔️ Topoğrafya</div>
                <div class="detail-row"><span>Yükselti</span><span class="detail-val">${t.elevation ?? '-'} m</span></div>
                <div class="detail-row"><span>Eğim</span><span class="detail-val">${t.slope ?? '-'}°</span></div>
                <div class="detail-row"><span>Bölge</span><span class="detail-val">${t.bolge}</span></div>
                <div class="detail-row"><span>Arazi Tipi</span><span class="detail-val">${corineName}</span></div>
            </div>`;
        }

        // ── Hava Durumu (ERA5) ──
        if (data.weather) {
            const w = data.weather;
            html += `<div class="detail-section">
                <div class="detail-header">🌡️ Hava Durumu (ERA5)</div>
                <div class="detail-row"><span>Sıcaklık</span><span class="detail-val">${w.temperature ?? '-'} °C</span></div>
                <div class="detail-row"><span>Bağıl Nem</span><span class="detail-val">${w.humidity ?? '-'} %</span></div>
                <div class="detail-row"><span>Rüzgar Hızı</span><span class="detail-val">${w.wind_speed ?? '-'} m/s</span></div>
                <div class="detail-row"><span>Yağış (24s)</span><span class="detail-val">${w.precipitation ?? '-'} mm</span></div>
            </div>`;
        }

        // ── FWI Bileşenleri (Van Wagner 1987) ──
        if (data.fwi) {
            const f = data.fwi;
            const fwiCat = getFWICategory(f.fwi_final);
            html += `<div class="detail-section">
                <div class="detail-header">🔥 FWI Bileşenleri (Van Wagner)</div>
                <div class="detail-row"><span>FFMC</span><span class="detail-val">${f.ffmc ?? '-'}</span></div>
                <div class="detail-row"><span>DMC</span><span class="detail-val">${f.dmc ?? '-'}</span></div>
                <div class="detail-row"><span>DC</span><span class="detail-val">${f.dc ?? '-'}</span></div>
                <div class="detail-row"><span>ISI</span><span class="detail-val">${f.isi ?? '-'}</span></div>
                <div class="detail-row"><span>BUI</span><span class="detail-val">${f.bui ?? '-'}</span></div>
                <div class="detail-row fwi-highlight"><span><b>FWI Final</b></span><span class="detail-val">${f.fwi_final ?? '-'} → ${fwiCat}</span></div>
            </div>`;
        }

        // ── ALAZ Model Girdileri ──
        if (data.alaz) {
            const a = data.alaz;
            const alazCat = getALAZCategory(a.risk_percent);
            html += `<div class="detail-section">
                <div class="detail-header">🤖 ALAZ Model Girdileri</div>
                <div class="detail-row"><span>NDVI</span><span class="detail-val">${a.ndvi ?? '-'}</span></div>
                <div class="detail-row"><span>Son Yangından Bu Yana</span><span class="detail-val">${a.days_since_last_fire ?? '-'} gün</span></div>
                <div class="detail-row alaz-highlight"><span><b>ALAZ Risk</b></span><span class="detail-val">%${a.risk_percent ?? '-'} → ${alazCat}</span></div>
            </div>`;
        }

        content.innerHTML = html;

    } catch (e) {
        content.innerHTML = `<div style="color:#ff6b6b; padding:20px;">Detay alınamadı: ${e.message}</div>`;
    }
}

// ===============================================
// LEJANT (LEGEND) MOTORU
// ===============================================
function buildFWILegendHTML() {
    return `
        <div class="legend-title">FWI Risk Skalası (Sunum Özel)</div>
        <div class="legend-item"><span class="legend-color" style="background:rgb(76,175,80)"></span> Güvenli &lt; 7.0</div>
        <div class="legend-item"><span class="legend-color" style="background:rgb(255,193,7)"></span> Dikkat 7.0 – 9.5</div>
        <div class="legend-item"><span class="legend-color" style="background:rgb(255,152,0)"></span> Yüksek 9.5 – 12.0</div>
        <div class="legend-item"><span class="legend-color" style="background:rgb(244,67,54)"></span> Kritik 12.0+</div>
    `;
}

function buildALAZLegendHTML() {
    return `
        <div class="legend-title">ALAZ Risk Skalası (Sunum Özel)</div>
        <div class="legend-item"><span class="legend-color" style="background:rgb(76,175,80)"></span> Güvenli &lt; %4.5</div>
        <div class="legend-item"><span class="legend-color" style="background:rgb(255,193,7)"></span> Dikkat %4.5 – %7.0</div>
        <div class="legend-item"><span class="legend-color" style="background:rgb(255,152,0)"></span> Yüksek Risk %7.0 – %10.0</div>
        <div class="legend-item"><span class="legend-color" style="background:rgb(244,67,54)"></span> Kritik %10.0+</div>
    `;
}

function updateLegend(mode) {
    const ls = document.getElementById('legend-single');
    const ll = document.getElementById('legend-left');
    const lr = document.getElementById('legend-right');

    // Önce hepsini gizle
    if (ls) ls.classList.add('hidden');
    if (ll) ll.classList.add('hidden');
    if (lr) lr.classList.add('hidden');

    if (mode === 'compare') {
        if (ll) { ll.innerHTML = buildFWILegendHTML();  ll.classList.remove('hidden'); }
        if (lr) { lr.innerHTML = buildALAZLegendHTML(); lr.classList.remove('hidden'); }
    } else if (mode === 'fwi') {
        if (ls) { ls.innerHTML = buildFWILegendHTML();  ls.classList.remove('hidden'); }
    } else {
        if (ls) { ls.innerHTML = buildALAZLegendHTML(); ls.classList.remove('hidden'); }
    }
}

// ===============================================
// API ÇAĞRISI VE BAŞLATMA
// ===============================================
document.getElementById('start-btn').addEventListener('click', async () => {
    const startDate = document.getElementById('start-date').value;
    const endDate   = document.getElementById('end-date').value;
    const mode      = document.getElementById('mode-select').value;
    currentMode = mode;

    document.getElementById('error-box').classList.add('hidden');
    document.getElementById('loading-container').classList.remove('hidden');
    document.getElementById('start-btn').disabled = true;

    try {
        const res = await fetch('http://127.0.0.1:8000/api/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ start_date: startDate, end_date: endDate, mode: mode })
        });

        const json = await res.json();
        if (!res.ok) throw new Error(json.detail || "Bilinmeyen Sunucu Hatası");

        currentData = json.data;

        if (mode === 'compare') {
            availableDates = [startDate];
        } else {
            const datesSet = new Set(currentData.map(d => d.date));
            availableDates = Array.from(datesSet).sort();
        }

        setupMapsUI(mode);
        updateLegend(mode);
        setupTimeline();
        renderDay(0);

        document.getElementById('welcome-modal').classList.add('hidden');

    } catch (err) {
        document.getElementById('error-box').innerText = err.message;
        document.getElementById('error-box').classList.remove('hidden');
    } finally {
        document.getElementById('loading-container').classList.add('hidden');
        document.getElementById('start-btn').disabled = false;
    }
});

// ===============================================
// HARİTA YÖNETİMİ
// ===============================================
function setupMapsUI(mode) {
    if (mode === 'compare') {
        document.getElementById('map-container-single').classList.add('hidden');
        document.getElementById('map-container-split').classList.remove('hidden');

        if (!mapLeft) {
            mapLeft  = createMap('map-left');
            mapRight = createMap('map-right');

            overlayLeft  = new deck.MapboxOverlay({ interleaved: true, layers: [] });
            mapLeft.addControl(overlayLeft);

            overlayRight = new deck.MapboxOverlay({ interleaved: true, layers: [] });
            mapRight.addControl(overlayRight);

            // Çapraz Senkronizasyon
            const syncMaps = (source, target) => {
                source.on('move', () => {
                    if (!isSyncing) {
                        isSyncing = true;
                        target.jumpTo({
                            center:  source.getCenter(),
                            zoom:    source.getZoom(),
                            bearing: source.getBearing(),
                            pitch:   source.getPitch()
                        });
                        isSyncing = false;
                    }
                });
            };
            syncMaps(mapLeft, mapRight);
            syncMaps(mapRight, mapLeft);
        }
    } else {
        document.getElementById('map-container-split').classList.add('hidden');
        document.getElementById('map-container-single').classList.remove('hidden');
        document.getElementById('single-map-title').innerText =
            mode === 'fwi' ? "SADECE İKLİM RİSKİ (FWI)" : "YAPAY ZEKA FİZİKSEL RİSKİ (ALAZ)";

        if (!mapSingle) {
            mapSingle = createMap('map-single');
            overlaySingle = new deck.MapboxOverlay({ interleaved: true, layers: [] });
            mapSingle.addControl(overlaySingle);
        }
    }
}

// ===============================================
// RENDER MOTORU (Bilimsel Renk Skalası İle)
// ===============================================
function createGridLayer(id, data, colorFn) {
    return new deck.H3HexagonLayer({
        id: id,
        data: data,
        pickable: true,
        stroked: true,
        filled: true,
        extruded: false,
        lineWidthMinPixels: 0.5,
        getHexagon:   d => d.GRID_ID,
        getFillColor: d => colorFn(d, 90),         // İç dolgu  (saydam)
        getLineColor: d => colorFn(d, 200),        // Kenar     (belirgin)
        onHover:  handleTooltip,
        onClick:  handleGridClick
    });
}

function renderDay(dayIndex) {
    const targetDate = availableDates[dayIndex];
    document.getElementById('current-date-label').innerText = targetDate;

    const dayData = currentData.filter(d => d.date === targetDate);

    if (currentMode === 'compare') {
        const layerL = createGridLayer('h3-left',  dayData, (d, a) => getColorFWI(d.fwi_value, a));
        const layerR = createGridLayer('h3-right', dayData, (d, a) => getColorALAZ(d.risk_percent, a));
        overlayLeft.setProps({ layers: [layerL] });
        overlayRight.setProps({ layers: [layerR] });

    } else if (currentMode === 'fwi') {
        const layer = createGridLayer('h3-single', dayData, (d, a) => getColorFWI(d.fwi_value, a));
        overlaySingle.setProps({ layers: [layer] });

    } else { // alaz
        const layer = createGridLayer('h3-single', dayData, (d, a) => getColorALAZ(d.risk_percent, a));
        overlaySingle.setProps({ layers: [layer] });
    }
}

// ===============================================
// TIMELINE (SLIDER)
// ===============================================
function setupTimeline() {
    const pnl    = document.getElementById('timeline-panel');
    const slider = document.getElementById('time-slider');

    if (availableDates.length <= 1) {
        slider.style.display = 'none';
        document.getElementById('current-date-label').innerText = availableDates[0] || 'Veri Yok';
    } else {
        slider.style.display = 'block';
        slider.max   = availableDates.length - 1;
        slider.value = 0;
        slider.oninput = (e) => renderDay(parseInt(e.target.value));
    }
    pnl.classList.remove('hidden');
}

// ===============================================
// GERİ DÖN & PANEL KAPAT
// ===============================================
document.getElementById('back-home-btn').onclick = () => {
    document.getElementById('welcome-modal').classList.remove('hidden');
    document.getElementById('timeline-panel').classList.add('hidden');
    document.getElementById('tooltip').style.display = 'none';
    document.getElementById('detail-panel').classList.add('hidden');
};

document.getElementById('detail-close-btn').onclick = () => {
    document.getElementById('detail-panel').classList.add('hidden');
};
