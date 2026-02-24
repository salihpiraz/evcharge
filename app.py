import streamlit as st
import re

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
    
    .metric-value { font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0; }
    .metric-label { font-size: 0.95rem; color: #8B949E; text-transform: uppercase; letter-spacing: 1px; }
    .metric-icon { font-size: 2rem; margin-bottom: 0.5rem; }
    
    /* Renk varyasyonları */
    .gold-text { color: #FFD700; }
    .green-text { color: #00D4AA; }
    .blue-text { color: #1E90FF; }
    .orange-text { color: #FF8C00; }
    .purple-text { color: #A855F7; }
    .red-text { color: #FF6B6B; }
    
    /* Bölüm başlıkları */
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #FFD700;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #2D3139;
    }
    
    .stSlider > div > div { background-color: #FFD700 !important; }
    .stSelectbox > div > div { background-color: #1A1D24; border-color: #2D3139; }
    
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        margin: 2rem 0;
    }
    
    .footer {
        text-align: center; color: #8B949E; font-size: 0.85rem;
        margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #2D3139;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .charge-progress {
        background: #2D3139; border-radius: 10px;
        height: 20px; overflow: hidden; margin: 1rem 0;
    }
    
    /* MOBİL RESPONSIVE */
    @media screen and (max-width: 768px) {
        .main-title { font-size: 1.8rem !important; }
        .sub-title { font-size: 0.9rem; }
        .metric-card { padding: 1rem; margin-bottom: 0.5rem; }
        .metric-value { font-size: 1.5rem !important; }
        .metric-label { font-size: 0.75rem; }
        .metric-icon { font-size: 1.5rem; }
        .section-header { font-size: 1.1rem; }
        .custom-divider { margin: 1rem 0; }
    }
    @media screen and (max-width: 480px) {
        .main-title { font-size: 1.5rem !important; }
        .metric-value { font-size: 1.2rem !important; }
        .metric-label { font-size: 0.65rem; letter-spacing: 0; }
    }
</style>
""", unsafe_allow_html=True)

# Araç veritabanı - Marka kısaltmaları ile
VEHICLES = {
    "Opel Grandland 2025 Elektrikli": {
        "battery_capacity": 73, "max_dc_power": 160, "max_ac_power": 11,
        "brand_color": "#FFD700", "brand_short": "OPEL", "brand_icon": "⚡"
    },
    "Tesla Model Y": {
        "battery_capacity": 75, "max_dc_power": 250, "max_ac_power": 11,
        "brand_color": "#E31937", "brand_short": "TESLA", "brand_icon": "🔴"
    },
    "Togg T10X": {
        "battery_capacity": 88.5, "max_dc_power": 180, "max_ac_power": 22,
        "brand_color": "#00A0E3", "brand_short": "TOGG", "brand_icon": "🔵"
    },
    "BYD Atto 3": {
        "battery_capacity": 60.5, "max_dc_power": 88, "max_ac_power": 7,
        "brand_color": "#C41E3A", "brand_short": "BYD", "brand_icon": "🔶"
    },
    "Hyundai Ioniq 5": {
        "battery_capacity": 77.4, "max_dc_power": 220, "max_ac_power": 11,
        "brand_color": "#002C5F", "brand_short": "HYUNDAI", "brand_icon": "🔷"
    },
    "Volkswagen ID.4": {
        "battery_capacity": 77, "max_dc_power": 135, "max_ac_power": 11,
        "brand_color": "#001E50", "brand_short": "VW", "brand_icon": "🔵"
    }
}


# ===== YAKIT FİYATI ÇEKME =====
@st.cache_data(ttl=3600)
def fetch_fuel_prices():
    """Güncel akaryakıt fiyatlarını web'den çekmeye çalışır."""
    try:
        import requests
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp = requests.get("https://www.petrolofisi.com.tr/akaryakit-fiyatlari", headers=headers, timeout=10)
        if resp.status_code == 200:
            text = resp.text
            prices = {}
            benzin_match = re.search(r'(?:Kurşunsuz\s*95|Benzin)[^\d]*(\d+[.,]\d+)', text)
            motorin_match = re.search(r'(?:Motorin|Eurodiesel)[^\d]*(\d+[.,]\d+)', text)
            if benzin_match:
                prices["benzin"] = float(benzin_match.group(1).replace(",", "."))
            if motorin_match:
                prices["motorin"] = float(motorin_match.group(1).replace(",", "."))
            if prices:
                return prices
    except Exception:
        pass
    try:
        import requests
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp = requests.get("https://www.opet.com.tr/akaryakit-fiyatlari", headers=headers, timeout=10)
        if resp.status_code == 200:
            text = resp.text
            prices = {}
            benzin_match = re.search(r'(?:Kurşunsuz\s*95)[^\d]*(\d+[.,]\d+)', text)
            motorin_match = re.search(r'(?:Motorin)[^\d]*(\d+[.,]\d+)', text)
            if benzin_match:
                prices["benzin"] = float(benzin_match.group(1).replace(",", "."))
            if motorin_match:
                prices["motorin"] = float(motorin_match.group(1).replace(",", "."))
            if prices:
                return prices
    except Exception:
        pass
    return None


def calculate_realistic_charging_time(current_percent, target_percent, battery_capacity, max_power, station_power, charge_type):
    """Gerçekçi şarj süresini hesaplar - DC şarj eğrisini dikkate alır."""
    DC_EFFICIENCY = 0.92
    AC_EFFICIENCY = 0.90
    effective_max_power = min(station_power, max_power)

    if "AC" in charge_type:
        energy_to_battery = (target_percent - current_percent) / 100 * battery_capacity
        energy_from_station = energy_to_battery / AC_EFFICIENCY
        charge_time_hours = energy_to_battery / (effective_max_power * 0.95)
        return charge_time_hours, energy_to_battery, energy_from_station, AC_EFFICIENCY, {"AC Şarj": (current_percent, target_percent, effective_max_power * 0.95)}

    charge_zones = [
        (0, 10, 0.28), (10, 20, 0.38), (20, 50, 0.48),
        (50, 80, 0.44), (80, 90, 0.24), (90, 95, 0.12), (95, 100, 0.055),
    ]
    total_time_hours = 0
    total_energy_to_battery = 0
    zone_details = {}
    for zone_start, zone_end, power_factor in charge_zones:
        if target_percent <= zone_start or current_percent >= zone_end:
            continue
        actual_start = max(current_percent, zone_start)
        actual_end = min(target_percent, zone_end)
        if actual_start >= actual_end:
            continue
        zone_energy = (actual_end - actual_start) / 100 * battery_capacity
        zone_power = effective_max_power * power_factor
        zone_time = zone_energy / zone_power
        total_time_hours += zone_time
        total_energy_to_battery += zone_energy
        zone_name = f"%{zone_start}-{zone_end}"
        zone_details[zone_name] = {
            "start": actual_start, "end": actual_end, "power": zone_power,
            "energy": zone_energy, "time_minutes": zone_time * 60, "power_factor": power_factor
        }
    energy_from_station = total_energy_to_battery / DC_EFFICIENCY
    return total_time_hours, total_energy_to_battery, energy_from_station, DC_EFFICIENCY, zone_details


# ===== ANA BAŞLIK =====
st.markdown('<h1 class="main-title">⚡ EV Şarj Hesaplayıcı</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Gerçekçi şarj eğrisi ile süre ve maliyet hesaplayın</p>', unsafe_allow_html=True)
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ===== SEKMELER =====
tab1, tab2 = st.tabs(["⚡ Şarj Süresi ve Maliyeti", "🛣️ 100 km Maliyet Karşılaştırması"])

# =============================================
# SEKME 1: EV ŞARJ HESAPLAYICI
# =============================================
with tab1:
    st.markdown('<p class="section-header">🚗 Araç Seçimi</p>', unsafe_allow_html=True)
    selected_vehicle = st.selectbox("Aracınızı seçin:", options=list(VEHICLES.keys()), index=0, help="Listeden elektrikli aracınızı seçin")
    vehicle = VEHICLES[selected_vehicle]

    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: linear-gradient(145deg, #1A1D24 0%, #22262E 100%); border-radius: 16px; border: 1px solid {vehicle['brand_color']}; margin-bottom: 1rem; flex-wrap: wrap;">
        <div style="flex-shrink: 0; width: 60px; height: 60px; background: linear-gradient(145deg, {vehicle['brand_color']}22, {vehicle['brand_color']}44); border: 2px solid {vehicle['brand_color']}; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
            <span style="font-size: 0.9rem; font-weight: 800; color: {vehicle['brand_color']};">{vehicle['brand_short']}</span>
        </div>
        <div style="flex-grow: 1; min-width: 200px;">
            <div style="font-size: 1.1rem; font-weight: 700; color: {vehicle['brand_color']}; margin-bottom: 0.5rem;">{selected_vehicle}</div>
            <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                <div style="min-width: 70px;"><span style="color: #8B949E; font-size: 0.75rem;">Batarya</span><div style="color: #FFD700; font-weight: 600; font-size: 0.95rem;">{vehicle['battery_capacity']} kWh</div></div>
                <div style="min-width: 60px;"><span style="color: #8B949E; font-size: 0.75rem;">Max DC</span><div style="color: #1E90FF; font-weight: 600; font-size: 0.95rem;">{vehicle['max_dc_power']} kW</div></div>
                <div style="min-width: 60px;"><span style="color: #8B949E; font-size: 0.75rem;">Max AC</span><div style="color: #00D4AA; font-weight: 600; font-size: 0.95rem;">{vehicle['max_ac_power']} kW</div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="section-header">🔋 Şarj Ayarları</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        current_charge = st.number_input("Mevcut Şarj Yüzdesi (%)", min_value=0, max_value=100, value=12, step=1, help="Aracınızın mevcut batarya yüzdesi")
    with col2:
        target_charge = st.number_input("Hedef Şarj Yüzdesi (%)", min_value=0, max_value=100, value=99, step=1, help="Ulaşmak istediğiniz batarya yüzdesi")

    if target_charge > current_charge:
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
    st.markdown('<p class="section-header">⛽ Şarj İstasyonu Ayarları</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        charge_type = st.selectbox("Şarj Türü", options=["DC (Hızlı Şarj)", "AC (Normal Şarj)"], index=0, help="DC: Hızlı şarj istasyonları, AC: Ev/İş yeri şarjı")
    with col2:
        station_power = st.number_input("İstasyon Gücü (kW)", min_value=1.0, max_value=500.0, value=50.0 if "DC" in charge_type else 7.4, step=0.1, help="Şarj istasyonunun maksimum gücü")
    with col3:
        unit_price = st.number_input("Birim Fiyat (TL/kWh)", min_value=0.01, max_value=50.0, value=11.50, step=0.01, help="kWh başına şarj ücreti")

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Hesaplama
    if target_charge > current_charge:
        vehicle_max_power = vehicle['max_dc_power'] if "DC" in charge_type else vehicle['max_ac_power']
        charge_time_hours, energy_to_battery, energy_from_station, efficiency, zone_details = calculate_realistic_charging_time(
            current_charge, target_charge, vehicle['battery_capacity'], vehicle_max_power, station_power, charge_type
        )
        effective_power = min(station_power, vehicle_max_power)
        total_minutes = int(charge_time_hours * 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        total_cost = energy_from_station * unit_price

        st.markdown('<p class="section-header">📊 Hesaplama Sonuçları</p>', unsafe_allow_html=True)
        if station_power > vehicle_max_power:
            st.info(f"⚠️ İstasyon gücü ({station_power} kW), aracın maksimum kapasitesinden ({vehicle_max_power} kW) yüksek. Hesaplama {effective_power} kW ile yapıldı.")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            time_display = f"{hours}s {minutes}dk" if hours > 0 else f"{minutes} dk"
            st.markdown(f'<div class="metric-card"><div class="metric-icon">⏱️</div><div class="metric-value orange-text">{time_display}</div><div class="metric-label">Toplam Süre</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><div class="metric-icon">💰</div><div class="metric-value gold-text">{total_cost:.2f} ₺</div><div class="metric-label">Toplam Maliyet</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><div class="metric-icon">⚡</div><div class="metric-value green-text">{energy_from_station:.1f} kWh</div><div class="metric-label">Çekilen Enerji</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="metric-card"><div class="metric-icon">🔋</div><div class="metric-value blue-text">{energy_to_battery:.1f} kWh</div><div class="metric-label">Bataryaya Giren</div></div>', unsafe_allow_html=True)

        # Bölge bazlı süre dağılımı (DC şarj için)
        if "DC" in charge_type and zone_details:
            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
            st.markdown('<p class="section-header">⏱️ Bölge Bazlı Şarj Süresi Dağılımı</p>', unsafe_allow_html=True)
            zone_cols = st.columns(len(zone_details))
            zone_colors = {"%0-10": "red-text", "%10-20": "orange-text", "%20-50": "green-text", "%50-80": "green-text", "%80-90": "gold-text", "%90-95": "orange-text", "%95-100": "red-text"}
            zone_icons = {"%0-10": "❄️", "%10-20": "🌡️", "%20-50": "⚡", "%50-80": "🚀", "%80-90": "📉", "%90-95": "🐌", "%95-100": "🐢"}
            for i, (zone_name, details) in enumerate(zone_details.items()):
                with zone_cols[i]:
                    zm = int(details['time_minutes'])
                    cc = zone_colors.get(zone_name, "gold-text")
                    ic = zone_icons.get(zone_name, "⏱️")
                    st.markdown(f'<div class="metric-card" style="padding: 1rem;"><div style="font-size: 1.2rem;">{ic}</div><div style="font-size: 0.8rem; color: #8B949E;">{zone_name}</div><div class="metric-value {cc}" style="font-size: 1.5rem;">{zm} dk</div><div style="font-size: 0.75rem; color: #8B949E;">~{details["power"]:.0f} kW</div></div>', unsafe_allow_html=True)

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
                    st.markdown(f"- **{zone_name}**: %{details['start']:.0f} → %{details['end']:.0f} | {details['energy']:.2f} kWh | {details['time_minutes']:.1f} dk | ~{details['power']:.0f} kW ({details['power_factor']*100:.0f}% güç)")

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

> 💡 **Not**: Gerçek dünyada BMS, bataryayı korumak için şarj hızını dinamik olarak ayarlar.
            """)
    else:
        st.warning("⚠️ Hedef şarj yüzdesi, mevcut şarj yüzdesinden büyük olmalıdır!")


# =============================================
# SEKME 2: 100 KM MALİYET HESAPLAYICI
# =============================================
with tab2:
    st.markdown('<p class="section-header">🚗 Araç Tipi Seçimi</p>', unsafe_allow_html=True)
    vehicle_type = st.radio("Araç tipini seçin:", ["⚡ Elektrikli", "⛽ Benzinli", "🛢️ Dizel"], horizontal=True, key="vtype")
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # === ELEKTRİKLİ ===
    if "Elektrikli" in vehicle_type:
        st.markdown('<p class="section-header">⚡ Elektrikli Araç — 100 km Maliyet</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            ev_consumption = st.number_input("Tüketim (kWh/100km)", min_value=5.0, max_value=50.0, value=17.0, step=0.1, key="evcons")
        with col2:
            ev_price = st.number_input("Elektrik Fiyatı (TL/kWh)", min_value=0.01, max_value=50.0, value=11.50, step=0.01, key="evprice")
        cost_100km = ev_consumption * ev_price
        cost_per_km = cost_100km / 100
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="section-header">📊 Sonuçlar</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-icon">💰</div><div class="metric-value gold-text">{cost_100km:.2f} ₺</div><div class="metric-label">100 km Maliyet</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-icon">📍</div><div class="metric-value green-text">{cost_per_km:.2f} ₺</div><div class="metric-label">Km Başı Maliyet</div></div>', unsafe_allow_html=True)

    # === BENZİNLİ ===
    elif "Benzinli" in vehicle_type:
        st.markdown('<p class="section-header">⛽ Benzinli Araç — 100 km Maliyet</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            benz_consumption = st.number_input("Tüketim (lt/100km)", min_value=1.0, max_value=30.0, value=6.0, step=0.1, key="benzcons")
        with col2:
            benzin_price = st.number_input("Benzin Fiyatı (TL/lt)", min_value=0.01, max_value=200.0, value=57.08, step=0.01, key="benzprice")
        if st.button("🔄 Güncel Benzin Fiyatını Çek", key="fetch_benzin"):
            prices = fetch_fuel_prices()
            if prices and "benzin" in prices:
                st.success(f"✅ Güncel benzin fiyatı: {prices['benzin']:.2f} TL/lt — Yukarıdaki alana bu değeri girebilirsiniz.")
            else:
                st.warning("⚠️ Fiyat çekilemedi. Lütfen manuel olarak girin.")
        cost_100km = benz_consumption * benzin_price
        cost_per_km = cost_100km / 100
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="section-header">📊 Sonuçlar</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-icon">💰</div><div class="metric-value gold-text">{cost_100km:.2f} ₺</div><div class="metric-label">100 km Maliyet</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-icon">📍</div><div class="metric-value orange-text">{cost_per_km:.2f} ₺</div><div class="metric-label">Km Başı Maliyet</div></div>', unsafe_allow_html=True)

    # === DİZEL ===
    elif "Dizel" in vehicle_type:
        st.markdown('<p class="section-header">🛢️ Dizel Araç — 100 km Maliyet</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            dizel_consumption = st.number_input("Tüketim (lt/100km)", min_value=1.0, max_value=30.0, value=5.0, step=0.1, key="dizelcons")
        with col2:
            dizel_price = st.number_input("Motorin Fiyatı (TL/lt)", min_value=0.01, max_value=200.0, value=57.81, step=0.01, key="dizelprice")
        if st.button("🔄 Güncel Motorin Fiyatını Çek", key="fetch_dizel"):
            prices = fetch_fuel_prices()
            if prices and "motorin" in prices:
                st.success(f"✅ Güncel motorin fiyatı: {prices['motorin']:.2f} TL/lt — Yukarıdaki alana bu değeri girebilirsiniz.")
            else:
                st.warning("⚠️ Fiyat çekilemedi. Lütfen manuel olarak girin.")
        cost_100km = dizel_consumption * dizel_price
        cost_per_km = cost_100km / 100
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="section-header">📊 Sonuçlar</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-icon">💰</div><div class="metric-value gold-text">{cost_100km:.2f} ₺</div><div class="metric-label">100 km Maliyet</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-icon">📍</div><div class="metric-value orange-text">{cost_per_km:.2f} ₺</div><div class="metric-label">Km Başı Maliyet</div></div>', unsafe_allow_html=True)

    # === KARŞILAŞTIRMA ===
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    with st.expander("📊 Hızlı Karşılaştırma: Elektrikli vs Benzinli vs Dizel", expanded=True):
        ev_def = 17.0 * 11.50
        benz_def = 6.0 * 57.08
        dizel_def = 4.8 * 57.81
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="metric-card" style="border: 1px solid #00D4AA;"><div class="metric-icon">⚡</div><div style="font-size: 0.9rem; font-weight: 600; color: #00D4AA; margin-bottom: 0.5rem;">Elektrikli</div><div class="metric-value green-text" style="font-size: 1.8rem;">{ev_def:.0f} ₺</div><div class="metric-label">100 km</div><div style="font-size: 0.75rem; color: #8B949E; margin-top: 0.5rem;">17 kWh × 11.50 TL</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card" style="border: 1px solid #FF8C00;"><div class="metric-icon">⛽</div><div style="font-size: 0.9rem; font-weight: 600; color: #FF8C00; margin-bottom: 0.5rem;">Benzinli</div><div class="metric-value orange-text" style="font-size: 1.8rem;">{benz_def:.0f} ₺</div><div class="metric-label">100 km</div><div style="font-size: 0.75rem; color: #8B949E; margin-top: 0.5rem;">6.0 lt × 57.08 TL</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card" style="border: 1px solid #A855F7;"><div class="metric-icon">🛢️</div><div style="font-size: 0.9rem; font-weight: 600; color: #A855F7; margin-bottom: 0.5rem;">Dizel</div><div class="metric-value purple-text" style="font-size: 1.8rem;">{dizel_def:.0f} ₺</div><div class="metric-label">100 km</div><div style="font-size: 0.75rem; color: #8B949E; margin-top: 0.5rem;">4.8 lt × 57.81 TL</div></div>', unsafe_allow_html=True)
        sav_b = benz_def - ev_def
        sav_d = dizel_def - ev_def
        st.markdown(f'<div style="background: linear-gradient(145deg, #1A1D24 0%, #22262E 100%); border: 1px solid #00D4AA; border-radius: 12px; padding: 1rem; margin-top: 1rem; text-align: center;"><span style="color: #00D4AA; font-weight: 600;">💡 Elektrikli araç 100 km\'de benzinliye göre <span style="font-size: 1.2rem;">{sav_b:.0f} ₺</span>, dizele göre <span style="font-size: 1.2rem;">{sav_d:.0f} ₺</span> tasarruf sağlar!</span></div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>⚡ EV Şarj Hesaplayıcı | Gerçekçi Şarj Eğrisi ile Hesaplama</p>
    <p style="font-size: 0.75rem; margin-top: 0.5rem;">Not: Hesaplamalar tipik Li-ion batarya davranışına dayalıdır. Gerçek süreler çevresel koşullara göre değişebilir.</p>
</div>
""", unsafe_allow_html=True)
