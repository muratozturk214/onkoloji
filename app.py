import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pandas as pd

# Sayfa Ayarları ve Başlık
st.set_page_config(page_title="Mathrix AI", page_icon="🏥", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏥 Mathrix AI: RCC Patoloji ve Tedavi Analizi</h1>", unsafe_allow_html=True)

# Tıbbi Mantık Çerçevesi (Senin istediğin o "doğru" mantık burası)
DATABASE = {
    1: {"desc": "Grade 1: Küçük, yuvarlak ve düzenli çekirdekler.", "med": "Aktif İzlem veya Parsiyel Nefrektomi."},
    2: {"desc": "Grade 2: Biraz daha büyük çekirdekler, hafif düzensizlik.", "med": "Nefrektomi düşünülmeli."},
    3: {"desc": "Grade 3: Belirgin çekirdekçikler ve şekil bozukluğu.", "med": "Radikal Nefrektomi + Adjuvan Tedavi."},
    4: {"desc": "Grade 4: Çok büyük, canavar görünümlü çekirdekler ve nekroz.", "med": "İmmünoterapi: Nivolumab + Ipilimumab kombinasyonu."}
}

# Görüntü İşleme Fonksiyonu
def analyze_image(img):
    # Resmi analiz edip çekirdek boyutunu ölçen kısım
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) > 0:
        areas = [cv2.contourArea(c) for c in contours]
        avg_area = np.mean(areas)
        # Matematiksel ölçüm: Alanı boyuta çeviriyoruz
        size_um = np.sqrt(avg_area) * 0.5 
        
        # Derece Kararı (Tıbbi Kurallara Göre)
        if size_um < 15: return 1, size_um
        elif size_um < 20: return 2, size_um
        elif size_um < 25: return 3, size_um
        else: return 4, size_um
    return None, 0

# Arayüz
uploaded_file = st.file_uploader("Analiz için bir patoloji görüntüsü seçin...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Yüklenen Görüntü", width=300)
    
    if st.button("Mathrix AI ile Analiz Et"):
        img_array = np.array(image)
        grade, size = analyze_image(img_array)
        
        if grade:
            st.success(f"Analiz Tamamlandı! Tespit Edilen: Fuhrman Grade {grade}")
            st.info(f"📏 Ortalama Çekirdek Boyutu: {size:.2f} μm")
            
            # Sonuç Kartı
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🔬 Patolojik Açıklama")
                st.write(DATABASE[grade]["desc"])
            with col2:
                st.subheader("💊 Tedavi Önerisi")
                st.warning(DATABASE[grade]["med"])
        else:
            st.error("Görüntü analiz edilemedi. Lütfen daha net bir kesit yükleyin.")

st.markdown("---")
st.caption("Not: Bu sistem bir yapay zeka asistanıdır. Kesin teşhis için patolog onayı gereklidir.")
