import streamlit as st

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="EV Şarj Hesaplayıcı Salih Piraz",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Özel CSS stillemesi - Koyu tema ve modern tasarım
st.markdown("""
<style>
    /* Ana tema renkleri */
    :root {
        --primary-gold: #FFD700;
        --primary-blue: #1E90FF;
        --dark-bg: #0E1117;
        --card-bg: #1A1D24;
        --card-border: #2D3139;
        --text-primary: #FFFFFF;
        --text-secondary: #8B949E;
        --accent-green: #00D4AA;
        --accent-orange: #FF8C00;
        --accent-purple: #A855F7;
    }
    
    /* Genel sayfa stili */
    .stApp {
        background: linear-gradient(135deg, #0E1117 0%, #1A1D24 50%, #0E1117 100%);
    }
    
    /* Başlık stili */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF8C00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
    }
    
    .sub-title {
        font-size: 1.1rem;
        color: #8B949E;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Kart stilleri */
    .metric-card {
        background: linear-gradient(145deg, #1A1D24 0%, #22262E 100%);
        border: 1px solid #2D3139;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(255, 215, 0, 0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.95rem;
        color: #8B949E;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    /* Renk varyasyonları */
    .gold-text {
        color: #FFD700;
    }
    
    .green-text {
        color: #00D4AA;
    }
    
    .blue-text {
        color: #1E90FF;
    }
    
    .orange-text {
        color: #FF8C00;
    }
    
    .purple-text {
        color: #A855F7;
    }
    
    .red-text {
        color: #FF6B6B;
    }
    
    /* Bölüm başlıkları */
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #FFD700;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #2D3139;
    }
    
    /* Araç bilgi kartı */
    .vehicle-info-card {
        background: linear-gradient(145deg, #1A1D24 0%, #22262E 100%);
        border: 1px solid #FFD700;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
    }
    
    .vehicle-spec {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid #2D3139;
    }
    
    .vehicle-spec:last-child {
        border-bottom: none;
    }
    
    .spec-label {
        color: #8B949E;
    }
    
    .spec-value {
        color: #FFD700;
        font-weight: 600;
    }
    
    /* Slider ve input stilleri */
    .stSlider > div > div {
        background-color: #FFD700 !important;
    }
    
    .stSelectbox > div > div {
        background-color: #1A1D24;
        border-color: #2D3139;
    }
    
    /* Divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        margin: 2rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #8B949E;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #2D3139;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Progress bar style */
    .charge-progress {
        background: #2D3139;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .charge-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    /* Şarj eğrisi bilgi kartı */
    .curve-info {
        background: linear-gradient(145deg, #1A1D24 0%, #22262E 100%);
        border: 1px solid #2D3139;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        font-size: 0.9rem;
    }
    
    .curve-zone {
        display: flex;
        justify-content: space-between;
        padding: 0.4rem 0;
        border-bottom: 1px solid #2D3139;
    }
    
    .curve-zone:last-child {
        border-bottom: none;
    }
    
    .zone-fast {
        color: #00D4AA;
    }
    
    .zone-medium {
        color: #FFD700;
    }
    
    .zone-slow {
        color: #FF8C00;
    }
    
    .zone-very-slow {
        color: #FF6B6B;
    }
    
    /* ========== MOBİL RESPONSIVE ========== */
    @media screen and (max-width: 768px) {
        /* Başlık */
        .main-title {
            font-size: 1.8rem !important;
        }
        
        .sub-title {
            font-size: 0.9rem;
        }
        
        /* Metric kartları */
        .metric-card {
            padding: 1rem;
            margin-bottom: 0.5rem;
        }
        
        .metric-value {
            font-size: 1.5rem !important;
        }
        
        .metric-label {
            font-size: 0.75rem;
        }
        
        .metric-icon {
            font-size: 1.5rem;
        }
        
        /* Section header */
        .section-header {
            font-size: 1.1rem;
        }
        
        /* Divider */
        .custom-divider {
            margin: 1rem 0;
        }
    }
    
    @media screen and (max-width: 480px) {
        /* Çok küçük ekranlar */
        .main-title {
            font-size: 1.5rem !important;
        }
        
        .metric-value {
            font-size: 1.2rem !important;
        }
        
        .metric-label {
            font-size: 0.65rem;
            letter-spacing: 0;
        }
    }
</style>
""", unsafe_allow_html=True)

# Araç veritabanı - Marka kısaltmaları ile
VEHICLES = {
    "Opel Grandland 2025 Elektrikli": {
        "battery_capacity": 73,  # kWh
        "max_dc_power": 160,     # kW
        "max_ac_power": 11,      # kW
        "brand_color": "#FFD700",
        "brand_short": "OPEL",
        "brand_icon": "⚡"
    },
    "Tesla Model Y": {
        "battery_capacity": 75,  # kWh
        "max_dc_power": 250,     # kW
        "max_ac_power": 11,      # kW
        "brand_color": "#E31937",
        "brand_short": "TESLA",
        "brand_icon": "🔴"
    },
    "Togg T10X": {
        "battery_capacity": 88.5,  # kWh
        "max_dc_power": 180,       # kW
        "max_ac_power": 22,        # kW
        "brand_color": "#00A0E3",
        "brand_short": "TOGG",
        "brand_icon": "🔵"
    },
    "BYD Atto 3": {
        "battery_capacity": 60.5,  # kWh
        "max_dc_power": 88,        # kW
        "max_ac_power": 7,         # kW
        "brand_color": "#C41E3A",
        "brand_short": "BYD",
        "brand_icon": "🔶"
    },
    "Hyundai Ioniq 5": {
        "battery_capacity": 77.4,  # kWh
        "max_dc_power": 220,       # kW
        "max_ac_power": 11,        # kW
        "brand_color": "#002C5F",
        "brand_short": "HYUNDAI",
        "brand_icon": "🔷"
    },
    "Volkswagen ID.4": {
        "battery_capacity": 77,  # kWh
        "max_dc_power": 135,     # kW
        "max_ac_power": 11,      # kW
        "brand_color": "#001E50",
        "brand_short": "VW",
        "brand_icon": "🔵"
    }
}

def calculate_realistic_charging_time(current_percent, target_percent, battery_capacity, max_power, station_power, charge_type):
    """
    Gerçekçi şarj süresini hesaplar - DC şarj eğrisini dikkate alır.
    
    GERÇEK DÜNYA KALİBRASYONU:
    - Opel Grandland test verisi: %12→%99, 69.12 kWh, 93 dakika, 150 kW istasyon
    - Ortalama güç: 44.6 kW (teorik 150 kW'nin %30'u)
    
    DC Şarj Eğrisi (Gerçek dünya Li-ion batarya davranışı):
    - %0-10: Batarya çok soğuk/sıcak olabilir, yavaş başlar (~%28)
    - %10-20: Isınma tamamlanıyor, hız artıyor (~%38)
    - %20-50: İyi performans bölgesi (~%48)
    - %50-80: Sürdürülebilir güç (~%44)
    - %80-90: Belirgin yavaşlama başlar (~%24)
    - %90-95: Ciddi yavaşlama, BMS koruma (~%12)
    - %95-100: Trickle charge, çok yavaş (~%5.5)
    
    NOT: Araç üreticisinin belirttiği "max DC" güç sadece anlık peak değeridir.
    Gerçek ortalama güç bunun yaklaşık %30-50'si civarındadır.
    
    ŞARJ VERİMLİLİĞİ:
    - DC şarj: ~%92 verimlilik (ısı, dönüştürücü kayıpları)
    - AC şarj: ~%90 verimlilik (AC/DC dönüşüm, şarj cihazı kayıpları)
    Bu kayıplar yüzünden istasyondan çekilen enerji, bataryaya giren enerjiden fazladır.
    """
    
    # Şarj verimliliği faktörleri (bataryaya giren / istasyondan çekilen)
    DC_EFFICIENCY = 0.92  # DC şarj verimliliği
    AC_EFFICIENCY = 0.90  # AC şarj verimliliği
    
    # Efektif max güç (istasyon ve araç limitinin minimumu)
    effective_max_power = min(station_power, max_power)
    
    # AC şarj için basit lineer hesaplama (AC şarj daha stabil)
    if "AC" in charge_type:
        energy_to_battery = (target_percent - current_percent) / 100 * battery_capacity
        # AC şarjda verimlilik kaybı - istasyondan daha fazla enerji çekilir
        energy_from_station = energy_to_battery / AC_EFFICIENCY
        charge_time_hours = energy_to_battery / (effective_max_power * 0.95)
        return charge_time_hours, energy_to_battery, energy_from_station, AC_EFFICIENCY, {"AC Şarj": (current_percent, target_percent, effective_max_power * 0.95)}
    
    # DC şarj için parçalı hesaplama - GERÇEK DÜNYA DEĞERLERİ
    # Bu değerler Opel Grandland gerçek kullanım verisine göre kalibre edildi
    # Test: %12→%99, 69.12 kWh, 93 dakika, 150 kW istasyon
    charge_zones = [
        (0, 10, 0.28),    # %0-10: Çok yavaş başlangıç
        (10, 20, 0.38),   # %10-20: Isınma, yavaş
        (20, 50, 0.48),   # %20-50: İyi performans (peak)
        (50, 80, 0.44),   # %50-80: Hâlâ iyi ama azalıyor
        (80, 90, 0.24),   # %80-90: Belirgin yavaşlama
        (90, 95, 0.12),   # %90-95: Ciddi yavaşlama
        (95, 100, 0.055), # %95-100: Trickle charge
    ]
    
    total_time_hours = 0
    total_energy_to_battery = 0
    zone_details = {}
    
    for zone_start, zone_end, power_factor in charge_zones:
        # Bu bölgede şarj yapılacak mı kontrol et
        if target_percent <= zone_start or current_percent >= zone_end:
            continue
        
        # Bölge içindeki gerçek başlangıç ve bitiş noktaları
        actual_start = max(current_percent, zone_start)
        actual_end = min(target_percent, zone_end)
        
        if actual_start >= actual_end:
            continue
        
        # Bu bölgedeki enerji miktarı
        zone_energy = (actual_end - actual_start) / 100 * battery_capacity
        
        # Bu bölgedeki efektif güç
        zone_power = effective_max_power * power_factor
        
        # Bu bölgedeki süre
        zone_time = zone_energy / zone_power
        
        total_time_hours += zone_time
        total_energy_to_battery += zone_energy
        
        zone_name = f"%{zone_start}-{zone_end}"
        zone_details[zone_name] = {
            "start": actual_start,
            "end": actual_end,
            "power": zone_power,
            "energy": zone_energy,
            "time_minutes": zone_time * 60,
            "power_factor": power_factor
        }
    
    # İstasyondan çekilen enerji (verimlilik kayıpları dahil)
    energy_from_station = total_energy_to_battery / DC_EFFICIENCY
    
    return total_time_hours, total_energy_to_battery, energy_from_station, DC_EFFICIENCY, zone_details


# Ana başlık
st.markdown('<h1 class="main-title">⚡ EV Şarj Hesaplayıcı</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Gerçekçi şarj eğrisi ile süre ve maliyet hesaplayın</p>', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Araç Seçimi
st.markdown('<p class="section-header">🚗 Araç Seçimi</p>', unsafe_allow_html=True)
selected_vehicle = st.selectbox(
    "Aracınızı seçin:",
    options=list(VEHICLES.keys()),
    index=0,
    help="Listeden elektrikli aracınızı seçin"
)

# Seçilen araç bilgileri
vehicle = VEHICLES[selected_vehicle]

# Araç bilgi kartı - Marka Badge ile (Mobil Uyumlu)
st.markdown(f"""
<div class="vehicle-card" style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: linear-gradient(145deg, #1A1D24 0%, #22262E 100%); border-radius: 16px; border: 1px solid {vehicle['brand_color']}; margin-bottom: 1rem; flex-wrap: wrap;">
    <div style="flex-shrink: 0; width: 60px; height: 60px; background: linear-gradient(145deg, {vehicle['brand_color']}22, {vehicle['brand_color']}44); border: 2px solid {vehicle['brand_color']}; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
        <span style="font-size: 0.9rem; font-weight: 800; color: {vehicle['brand_color']}; text-align: center;">{vehicle['brand_short']}</span>
    </div>
    <div style="flex-grow: 1; min-width: 200px;">
        <div style="font-size: 1.1rem; font-weight: 700; color: {vehicle['brand_color']}; margin-bottom: 0.5rem;">{selected_vehicle}</div>
        <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
            <div style="min-width: 70px;">
                <span style="color: #8B949E; font-size: 0.75rem;">Batarya</span>
                <div style="color: #FFD700; font-weight: 600; font-size: 0.95rem;">{vehicle['battery_capacity']} kWh</div>
            </div>
            <div style="min-width: 60px;">
                <span style="color: #8B949E; font-size: 0.75rem;">Max DC</span>
                <div style="color: #1E90FF; font-weight: 600; font-size: 0.95rem;">{vehicle['max_dc_power']} kW</div>
            </div>
            <div style="min-width: 60px;">
                <span style="color: #8B949E; font-size: 0.75rem;">Max AC</span>
                <div style="color: #00D4AA; font-weight: 600; font-size: 0.95rem;">{vehicle['max_ac_power']} kW</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Şarj Ayarları
st.markdown('<p class="section-header">🔋 Şarj Ayarları</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    current_charge = st.number_input(
        "Mevcut Şarj Yüzdesi (%)",
        min_value=0,
        max_value=100,
        value=12,
        step=1,
        help="Aracınızın mevcut batarya yüzdesi"
    )

with col2:
    target_charge = st.number_input(
        "Hedef Şarj Yüzdesi (%)",
        min_value=0,
        max_value=100,
        value=99,
        step=1,
        help="Ulaşmak istediğiniz batarya yüzdesi"
    )

# Şarj durumu progress bar
if target_charge > current_charge:
    progress_percent = (current_charge / target_charge) * 100 if target_charge > 0 else 0
    st.markdown(f"""
    <div style="margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="color: #FFD700; font-weight: 600;">% Mevcut Şarj: {current_charge}%</span>
            <span style="color: #00D4AA; font-weight: 600;">% Hedef Şarj: {target_charge}%</span>
        </div>
        <div class="charge-progress" style="height: 12px; position: relative;">
            <div style="position: absolute; left: 0; top: 0; height: 100%; width: {current_charge}%; background: linear-gradient(90deg, #FF8C00, #FFD700); border-radius: 10px;"></div>
            <div style="position: absolute; left: {current_charge}%; top: 0; height: 100%; width: {target_charge - current_charge}%; background: linear-gradient(90deg, #FFD700, #00D4AA); border-radius: 0 10px 10px 0; opacity: 0.5;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# İstasyon Ayarları
st.markdown('<p class="section-header">⛽ Şarj İstasyonu Ayarları</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    charge_type = st.selectbox(
        "Şarj Türü",
        options=["DC (Hızlı Şarj)", "AC (Normal Şarj)"],
        index=0,
        help="DC: Hızlı şarj istasyonları, AC: Ev/İş yeri şarjı"
    )

with col2:
    station_power = st.number_input(
        "İstasyon Gücü (kW)",
        min_value=1.0,
        max_value=500.0,
        value=50.0 if "DC" in charge_type else 7.4,
        step=0.1,
        help="Şarj istasyonunun maksimum gücü"
    )

with col3:
    unit_price = st.number_input(
        "Birim Fiyat (TL/kWh)",
        min_value=0.01,
        max_value=50.0,
        value=11.50,
        step=0.01,
        help="kWh başına şarj ücreti"
    )

# DC Şarj Eğrisi bilgisi gizlendi (hesaplama arka planda çalışıyor)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Hesaplama
if target_charge > current_charge:
    # Araç max gücünü belirle (DC veya AC'ye göre)
    if "DC" in charge_type:
        vehicle_max_power = vehicle['max_dc_power']
    else:
        vehicle_max_power = vehicle['max_ac_power']
    
    # Gerçekçi şarj süresi hesaplama
    charge_time_hours, energy_to_battery, energy_from_station, efficiency, zone_details = calculate_realistic_charging_time(
        current_charge, 
        target_charge, 
        vehicle['battery_capacity'],
        vehicle_max_power,
        station_power,
        charge_type
    )
    
    # Efektif güç (istasyon ve araç kapasitesinin minimumu)
    effective_power = min(station_power, vehicle_max_power)
    
    # Süreyi saat ve dakikaya çevir
    total_minutes = int(charge_time_hours * 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    
    # Toplam maliyet (İSTASYONDAN ÇEKİLEN ENERJİ ÜZERİNDEN - gerçek fatura)
    total_cost = energy_from_station * unit_price
    
    # Sonuçları göster
    st.markdown('<p class="section-header">📊 Hesaplama Sonuçları</p>', unsafe_allow_html=True)
    
    # Efektif güç bilgisi
    if station_power > vehicle_max_power:
        st.info(f"⚠️ İstasyon gücü ({station_power} kW), aracın maksimum {'DC' if 'DC' in charge_type else 'AC'} kapasitesinden ({vehicle_max_power} kW) yüksek. Hesaplama {effective_power} kW ile yapıldı.")
    
    # Sonuç kartları
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        time_display = f"{hours}s {minutes}dk" if hours > 0 else f"{minutes} dk"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">⏱️</div>
            <div class="metric-value orange-text">{time_display}</div>
            <div class="metric-label">Toplam Süre</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">💰</div>
            <div class="metric-value gold-text">{total_cost:.2f} ₺</div>
            <div class="metric-label">Toplam Maliyet</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">⚡</div>
            <div class="metric-value green-text">{energy_from_station:.1f} kWh</div>
            <div class="metric-label">Çekilen Enerji</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🔋</div>
            <div class="metric-value blue-text">{energy_to_battery:.1f} kWh</div>
            <div class="metric-label">Bataryaya Giren</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Verimlilik bilgisi gizlendi (hesaplama arka planda çalışıyor)
    efficiency_loss = energy_from_station - energy_to_battery
    
    # Bölge bazlı süre dağılımı (DC şarj için)
    if "DC" in charge_type and zone_details:
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="section-header">⏱️ Bölge Bazlı Şarj Süresi Dağılımı</p>', unsafe_allow_html=True)
        
        # Bölge kartları
        zone_cols = st.columns(len(zone_details))
        
        zone_colors = {
            "%0-10": "red-text",
            "%10-20": "orange-text",
            "%20-50": "green-text", 
            "%50-80": "green-text",
            "%80-90": "gold-text",
            "%90-95": "orange-text",
            "%95-100": "red-text"
        }
        
        zone_icons = {
            "%0-10": "❄️",
            "%10-20": "🌡️",
            "%20-50": "⚡",
            "%50-80": "🚀",
            "%80-90": "📉",
            "%90-95": "🐌",
            "%95-100": "🐢"
        }
        
        for i, (zone_name, details) in enumerate(zone_details.items()):
            with zone_cols[i]:
                zone_minutes = int(details['time_minutes'])
                zone_power = details['power']
                color_class = zone_colors.get(zone_name, "gold-text")
                icon = zone_icons.get(zone_name, "⏱️")
                
                st.markdown(f"""
                <div class="metric-card" style="padding: 1rem;">
                    <div style="font-size: 1.2rem;">{icon}</div>
                    <div style="font-size: 0.8rem; color: #8B949E;">{zone_name}</div>
                    <div class="metric-value {color_class}" style="font-size: 1.5rem;">{zone_minutes} dk</div>
                    <div style="font-size: 0.75rem; color: #8B949E;">~{zone_power:.0f} kW</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Detaylı bilgi
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    with st.expander("📋 Detaylı Hesaplama Bilgileri", expanded=False):
        st.markdown(f"""
        | Parametre | Değer |
        |-----------|-------|
        | **Seçilen Araç** | {selected_vehicle} |
        | **Batarya Kapasitesi** | {vehicle['battery_capacity']} kWh |
        | **Şarj Türü** | {charge_type} |
        | **İstasyon Gücü** | {station_power} kW |
        | **Araç Max Gücü** | {vehicle_max_power} kW |
        | **Efektif Max Güç** | {effective_power} kW |
        | **Şarj Aralığı** | %{current_charge} → %{target_charge} |
        | **Bataryaya Giren Enerji** | {energy_to_battery:.2f} kWh |
        | **İstasyondan Çekilen Enerji** | {energy_from_station:.2f} kWh |
        | **Şarj Verimliliği** | %{efficiency*100:.0f} |
        | **Birim Fiyat** | {unit_price:.2f} TL/kWh |
        | **Ortalama Efektif Güç** | {energy_to_battery / charge_time_hours:.1f} kW |
        """)
        
        if "DC" in charge_type and zone_details:
            st.markdown("### Bölge Detayları")
            for zone_name, details in zone_details.items():
                st.markdown(f"""
                - **{zone_name}**: %{details['start']:.0f} → %{details['end']:.0f} | 
                  {details['energy']:.2f} kWh | {details['time_minutes']:.1f} dk | 
                  ~{details['power']:.0f} kW ({details['power_factor']*100:.0f}% güç)
                """)
    
    # Karşılaştırma: Lineer vs Gerçekçi
    with st.expander("📈 Lineer vs Gerçekçi Hesaplama Karşılaştırması", expanded=False):
        linear_time = energy_to_battery / effective_power
        linear_minutes = int(linear_time * 60)
        
        difference_minutes = total_minutes - linear_minutes
        difference_percent = ((total_minutes - linear_minutes) / linear_minutes) * 100 if linear_minutes > 0 else 0
        
        st.markdown(f"""
        | Hesaplama Yöntemi | Süre | Fark |
        |-------------------|------|------|
        | **Lineer (Basit)** | {linear_minutes} dakika | - |
        | **Gerçekçi (Eğrili)** | {total_minutes} dakika | +{difference_minutes} dk (+%{difference_percent:.0f}) |
        
        > 💡 **Not**: Gerçek dünyada batarya yönetim sistemi (BMS), bataryayı korumak için 
        > şarj hızını dinamik olarak ayarlar. Özellikle %80 üzerinde şarj ederken 
        > süre önemli ölçüde uzar.
        """)

else:
    st.warning("⚠️ Hedef şarj yüzdesi, mevcut şarj yüzdesinden büyük olmalıdır!")

# Footer
st.markdown("""
<div class="footer">
    <p>⚡ EV Şarj Hesaplayıcı | Gerçekçi Şarj Eğrisi ile Hesaplama</p>
    <p style="font-size: 0.75rem; margin-top: 0.5rem;">Not: Hesaplamalar tipik Li-ion batarya davranışına dayalıdır. Gerçek süreler çevresel koşullara, batarya sıcaklığına ve yaşına göre değişebilir.</p>
</div>
""", unsafe_allow_html=True)
