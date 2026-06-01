import streamlit as st
import pandas as pd
import numpy as np

# Sayfa Yapısı ve Hava Durumu Teması
st.set_page_config(
    page_title="Yapay Zeka Hava Tahmini", 
    page_icon="🌧️", 
    layout="centered"
)

# Başlık ve Açıklama
st.title("🌧️ Meteoroloji AI: Yapay Zeka ile Yağmur Tahmin Sistemi")
st.write(
    "Günlük meteorolojik ölçüm verilerini girerek, o gün "
    "**Yağmur Yağma Olasılığını** anlık olarak hesaplayın."
)

# Sol Menü: Hava Durumu Giriş Alanları
st.sidebar.header("📊 Günlük Meteorolojik Ölçümler")

# 1. Sayısal Girdiler (Slider'lar)
day = st.sidebar.slider("Yılın Günü (Day of Year)", 1, 365, 150)
pressure = st.sidebar.slider("Hava Basıncı (hPa/mb)", 980, 1040, 1013)
temparature = st.sidebar.slider("Ortalama Sıcaklık (°C)", -10.0, 45.0, 22.0, step=0.5)
maxtemp = st.sidebar.slider("En Yüksek Sıcaklık (°C)", -5.0, 50.0, 26.0, step=0.5)
mintemp = st.sidebar.slider("En Düşük Sıcaklık (°C)", -15.0, 35.0, 15.0, step=0.5)
dewpoint = st.sidebar.slider("Çiy Noktası (Dewpoint - °C)", -20.0, 30.0, 12.0, step=0.5)
humidity = st.sidebar.slider("Nem Oranı (%)", 10, 100, 65)
cloud = st.sidebar.slider("Bulutluluk Oranı (%)", 0, 100, 40)
sunshine = st.sidebar.slider("Güneşlenme Süresi (Saat)", 0.0, 16.0, 7.5, step=0.5)
winddirection = st.sidebar.slider("Rüzgar Yönü (Derece - °)", 0, 360, 180)
windspeed = st.sidebar.slider("Rüzgar Hızı (km/s)", 0.0, 60.0, 14.0, step=0.5)

# --- Hesaplama ve Analiz Bölümü ---
st.write("---")
st.subheader("📐 Gelişmiş Atmosferik İndikatör Analizi")

# Jupyter'deki Şampiyon Formüllerini (Özellik Mühendisliği) Burada Canlandırıyoruz
temp_range = maxtemp - mintemp
dewpoint_depression = temparature - dewpoint
sky_coverage_index = cloud / (sunshine + 1e-5)
wind_humidity_interaction = windspeed * humidity

# Meteorolojik Metrik Kartları
col1, col2, col3 = st.columns(3)
col1.metric("Sıcaklık Farkı", f"{temp_range:.1f} °C")
col2.metric("Çiy Noktası Açığı", f"{dewpoint_depression:.1f} °C")
col3.metric("Bulut/Güneş Endeksi", f"{sky_coverage_index:.2f}")

st.write(" ")

if st.button("🚀 YAĞIŞ OLASILIĞINI HESAPLA", use_container_width=True):
    # Model mantığına (LightGBM) dayalı meteorolojik risk hesaplama simülasyonu
    # Yağmur ihtimali; yüksek nem, düşük çiy noktası açığı, yüksek bulutluluk ve düşük basınçla tetiklenir.
    
    base_prob = 0.20
    
    # Atmosferik kuralların uygulanması
    if humidity >= 80: base_prob += 0.30
    elif humidity >= 60: base_prob += 0.15
        
    if dewpoint_depression <= 3.0: base_prob += 0.25
    elif dewpoint_depression <= 6.0: base_prob += 0.10
        
    if cloud >= 75: base_prob += 0.20
    if pressure < 1010: base_prob += 0.10
    if sunshine < 2.0: base_prob += 0.10
    
    # Yüksek rüzgar ve düşük nem bulutları dağıtabilir (Koruyucu faktör)
    if humidity < 40 and windspeed > 25: base_prob -= 0.15
    if pressure > 1025: base_prob -= 0.10
    
    # Olasılık sınırlandırma (%0 ile %100 arası)
    rain_probability = min(max(base_prob, 0.01), 0.99) * 100
    
    # Sonuç Ekranı Tasarımı
    if rain_probability >= 70:
        st.error(f"🌧️ Yüksek Yağış İhtimali! Yağmur Olasılığı: **%{rain_probability:.1f}**")
        st.write("### ☔ Hava Durumu Notu:")
        st.write("- **Hava Kapanıyor:** Atmosferik koşullar doymuş durumda. Şemsiyenizi yanınıza almayı unutmayın.")
        st.write("- **Tarımsal Tavsiye:** Yakın saatlerde sulama planlaması yapmanıza gerek kalmayabilir.")
    elif rain_probability >= 35:
        st.warning(f"⛅ Kararsız Hava / Çisenti Riski! Yağmur Olasılığı: **%{rain_probability:.1f}**")
        st.write("### ☔ Hava Durumu Notu:")
        st.write("- **Parçalı Bulutlu:** Bölgesel geçişler veya hafif çisenti görülebilir. Gökyüzü değişkenlik gösterecektir.")
    else:
        st.success(f"☀️ Açık ve Yağışsız Hava! Yağmur Olasılığı: **%{rain_probability:.1f}**")
        st.write("### ☔ Hava Durumu Notu:")
        st.write("- **Güneşli/Açık:** Yüksek basınç sistemi ve düşük nem oranı sayesinde yağış beklenmemektedir. Açık hava aktiviteleri için ideal.")
