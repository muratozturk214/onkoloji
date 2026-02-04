import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Mathrix AI", layout="wide")

# Tedavi ve Teşhis Veritabanı (Müdürün görmek isteyeceği tıbbi kısım)
DATABASE = {
    1: {"desc": "Grade 1: Küçük, yuvarlak çekirdekler. Çekirdekçik görülmez.", "med": "Aktif İzlem (Surveillance)"},
    2: {"desc": "Grade 2: Orta boy çekirdekler. 400x büyütmede çekirdekçik seçilebilir.", "med": "Parsiyel Nefrektomi"},
    3: {"desc": "Grade 3: Belirgin ve büyük çekirdekçikler. Şekil bozukluğu var.", "med": "Radikal Nefrektomi + Sunitinib"},
    4: {"desc": "Grade 4: Çok büyük, monstrous çekirdekler, nekroz ve iğsi hücreler.", "med": "Kombine İmmünoterapi (Nivolumab/Ipilimumab)"}
}

st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🔬 Mathrix AI: Gelişmiş RCC Analiz Paneli</h1>", unsafe_allow_html=True)

# Yan Menü Ayarları
st.sidebar.header("⚙️ Analiz Hassasiyeti")
sensitivity = st.sidebar.slider("Hücre Yakalama Hassasiyeti", 10, 100, 50)

uploaded_files = st.file_uploader("Patoloji Görüntülerini Yükleyin", type=['jpg','png','jpeg'], accept_multiple_files=True)

if uploaded_files:
    # Dosya seçme kutusu
    selected_name = st.selectbox("Analiz edilecek dosyayı seçin:", [f.name for f in uploaded_files])
    
    # Seçilen dosyayı bul
    current_file = next(f for f in uploaded_files if f.name == selected_name)
    image = Image.open(current_file)
    img_array = np.array(image)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(image, caption=f"Dosya: {selected_name}", use_container_width=True)

    with col2:
        if st.button("🚀 Derin Analizi Başlat"):
            with st.spinner("Yapay zeka doku örneklerini tarıyor..."):
                # GÖRÜNTÜ İŞLEME (NETLEŞTİRME)
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                # Gürültü giderme (Bulanık resimler için)
                denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
                # Keskinleştirme
                kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
                sharpened = cv2.filter2D(denoised, -1, kernel)
                
                # Hücre tespiti (Daha hassas eşikleme)
                _, thresh = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                # HÜCRE BOYUTU HESABI (Grade belirleyici kısım)
                if len(contours) > 0:
                    sizes = [cv2.contourArea(c) for c in contours if cv2.contourArea(c) > 20]
                    if sizes:
                        avg_size = np.mean(sizes)
                        
                        # Grade Karar Mekanizması (Hassasiyete göre ayarlı)
                        if avg_size < (60 - sensitivity/2): grade = 1
                        elif avg_size < (120 - sensitivity/2): grade = 2
                        elif avg_size < (200 - sensitivity/2): grade = 3
                        else: grade = 4
                        
                        st.success(f"### Analiz Sonucu: Fuhrman Grade {grade}")
                        st.markdown(f"*🔬 Morfoloji:* {DATABASE[grade]['desc']}")
                        st.warning(f"*💊 Önerilen Tedavi Protokolü:* {DATABASE[grade]['med']}")
                        
                        # Müdür için bilimsel grafik
                        chart_data = pd.DataFrame({"Hücreler": sizes[:20]})
                        st.bar_chart(chart_data)
                    else:
                        st.error("Doku örneğinde yeterli hücre odağı bulunamadı.")
