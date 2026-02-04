import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Mathrix AI", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🔬 Mathrix AI: Kararlı Patoloji Analizi</h1>", unsafe_allow_html=True)

DATABASE = {
    1: {"desc": "Grade 1: Küçük, uniform çekirdekler (~10µm).", "med": "Aktif İzlem / Takip"},
    2: {"desc": "Grade 2: Orta boy çekirdekler (~15µm).", "med": "Parsiyel Cerrahi"},
    3: {"desc": "Grade 3: Belirgin nükleol, düzensiz sınır (~20µm).", "med": "Radikal Cerrahi + Adjuvan"},
    4: {"desc": "Grade 4: Dev çekirdekler (>20µm) ve iğsi hücreler.", "med": "İmmünoterapi (Nivolumab+Ipilimumab)"}
}

uploaded_files = st.file_uploader("Dosyaları Yükleyin", type=['jpg','png','jpeg'], accept_multiple_files=True)

if uploaded_files:
    selected_name = st.selectbox("Analiz edilecek resim:", [f.name for f in uploaded_files])
    current_file = next(f for f in uploaded_files if f.name == selected_name)
    image = Image.open(current_file)
    img_array = np.array(image)

    if st.button("🔬 Hassas Analizi Başlat"):
        # Görüntü Ön İşleme
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        # Gürültü azaltma (Yanlış ölçümü engeller)
        blurred = cv2.medianBlur(gray, 5) 
        
        # Hücre tespiti
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Akıllı Ölçüm: Sadece gerçek hücre olabilecek boyutları al
        sizes = []
        for c in contours:
            area = cv2.contourArea(c)
            if 50 < area < 3000: # Tozları ve dev lekeleri eliyoruz
                sizes.append(np.sqrt(area)) # Çap hesabı
        
        if sizes:
            # Ortalamadan ziyade medyan (ortanca) değer yanılmayı azaltır
            final_size = np.median(sizes)
            
            # Tıbbi Sınırlar (Fuhrman Kriterleri)
            if final_size < 12: grade = 1
            elif final_size < 18: grade = 2
            elif final_size < 24: grade = 3
            else: grade = 4
            
            # Ekrana Yazdırma
            st.success(f"### Analiz Sonucu: Fuhrman Grade {grade}")
            st.info(f"📏 Ölçülen Kararlı Çekirdek Çapı: {final_size:.2f} px")
            st.write(f"*Açıklama:* {DATABASE[grade]['desc']}")
            st.warning(f"*Tedavi Planı:* {DATABASE[grade]['med']}")
        else:
            st.error("Resim çok bulanık, hücre seçilemedi.")
