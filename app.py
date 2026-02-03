import streamlit as st
import cv2
import numpy as np
from PIL import Image

# 1. SAYFA AYARLARI VE GÖRSEL TASARIM
st.set_page_config(page_title="Mathrix: Böbrek Analizörü", layout="wide")
st.title("🔬 Mathrix: Böbrek Kanseri Karar Destek Sistemi")
st.sidebar.header("Proje Hakkında")
st.sidebar.info("Mathrix, patologların hücreleri manuel sayma ve ilaç rehberlerini tarama yükünü azaltmak için geliştirilmiştir.")

# 2. DOSYA YÜKLEME
uploaded_file = st.file_uploader("Mikroskop Görüntüsünü Analiz İçin Yükleyin...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Görüntüyü oku
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    
    # İşleme için kopya oluştur (Renkli gösterim için)
    output_img = img_array.copy()
    
    # 3. GÖRÜNTÜ İŞLEME (ANALİZ MOTORU)
    # Gri tonlama ve gürültü temizleme
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Otomatik eşikleme (Hücre çekirdeklerini ayırma)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Konturları (hücre sınırlarını) bul
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    valid_areas = []
    for c in contours:
        area = cv2.contourArea(c)
        if area > 15:  # Çok küçük tozları ele
            valid_areas.append(area)
            # ANALİZİN KANITI: Hücrenin etrafına kırmızı kutu çiz
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(output_img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # 4. İSTATİSTİKSEL HESAPLAMA
    avg_area = np.mean(valid_areas) if valid_areas else 0
    
    # 5. EKRAN GÖSTERİMİ (İKİ PANEL)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Orijinal Görüntü")
        st.image(image, use_container_width=True)
        
    with col2:
        st.subheader("Mathrix İşaretleme (Kanıt)")
        st.image(output_img, use_container_width=True)

    # 6. KARAR VE İLAÇ REHBERİ EŞLEŞTİRME (VİZYON)
    st.divider()
    st.subheader("🩺 Patoloji ve Tedavi Raporu")
    
    if avg_area == 0:
        st.error("Hücre yapısı analiz edilemedi. Lütfen net bir mikroskop görüntüsü yükleyin.")
    else:
        # Dereceleme Mantığı (Fuhrman Grade Sistemi)
        if avg_area < 90:
            grade = "Grade 1-2 (Düşük Risk)"
            protocol = "Aktif İzlem (İlaçsız Takip)"
            desc = "Hücre çekirdekleri küçük ve düzenli. Literatür: Cerrahi yeterlidir."
            status = "success"
        elif 90 <= avg_area < 280:
            grade = "Grade 3 (Yüksek Risk)"
            protocol = "Sunitinib veya Pazopanib"
            desc = "Çekirdekler belirginleşmiş. Rehber: Hedefe yönelik TKI tedavisi önerilir."
            status = "warning"
        else:
            grade = "Grade 4 (Kritik Risk)"
            protocol = "Nivolumab + Ipilimumab (İmmünoterapi)"
            desc = "Amorf ve dev çekirdekler. ACİL: Agresif kombinasyon protokolü uygulanmalıdır."
            status = "error"

        # Sonuçları Havalı Göster
        st.info(f"*Tespit Edilen Ortalama Çekirdek Alanı:* {round(avg_area, 2)} piksel")
        
        if status == "success": st.success(f"*Teşhis:* {grade}")
        elif status == "warning": st.warning(f"*Teşhis:* {grade}")
        else: st.error(f"*Teşhis:* {grade}")
        
        st.markdown(f"### 💊 Önerilen İlaç Protokolü: *{protocol}*")
        st.write(f"*Uzman Notu:* {desc}")

st.divider()
st.caption("Mathrix v1.0 | Patolog Karar Destek Sistemi - 2026")
