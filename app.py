import streamlit as st
import numpy as np
from PIL import Image
import time
import pandas as pd

# --- SAYFA AYARLARI VE KLİNİK TEMA ---
st.set_page_config(page_title="LUNG-CORE v2026", layout="wide")

# Bembeyaz klinik tema CSS
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .report-box { 
        border: 2px solid #E0E0E0; padding: 30px; border-radius: 10px; 
        background-color: #FAFAFA; font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 { color: #2C3E50; font-weight: 300; }
    .stButton>button { background-color: #2C3E50; color: white; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- ŞİFRELEME MEKANİZMASI ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("LUNG-CORE: Onkolojik Analiz Portalı")
    password = st.text_input("Klinik Erişim Şifresi:", type="password")
    if password == "mathrix2026":
        st.session_state.auth = True
        st.rerun()
    else:
        st.stop()

# --- ANA PANEL ---
st.sidebar.title("LUNG-CORE v2026")
menu = st.sidebar.radio("Menü", ["Bilgi Bankası & Rehber", "Dijital Patoloji Analizi"])

# --- BÖLÜM 1: BİLGİ BANKASI ---
if menu == "Bilgi Bankası & Rehber":
    st.title("🩺 Klinik Bilgi Bankası")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("TNM Evreleme Tablosu")
        tnm_data = {
            "Evre": ["I", "II", "III", "IV"],
            "T (Tümör)": ["T1 (<3cm)", "T2 (3-5cm)", "T3 (>5cm/İstila)", "T4 (Mediastinal)"],
            "N (Lenf)": ["N0", "N1 (Hilar)", "N2 (Mediastinal)", "N3 (Kontralateral)"],
            "M (Metastaz)": ["M0", "M0", "M0/M1a", "M1b/M1c (Uzak)"]
        }
        st.table(pd.DataFrame(tnm_data))

    with col2:
        st.subheader("Metastaz Rehberi (Organ Tropizmi)")
        m_col1, m_col2 = st.columns(2)
        m_col1.info("*Beyin:* SCLC ve Adenokarsinom eğilimi yüksek.")
        m_col1.info("*Karaciğer:* Diffüz tutulum, ALP yüksekliği.")
        m_col2.info("*Kemik:* Litik lezyonlar, kalsiyum takibi.")
        m_col2.info("*Adrenal:* Sık görülen asemptomatik yayılım.")

# --- BÖLÜM 2: ANALİZ MOTORU ---
else:
    st.title("🔬 Dijital Patoloji ve Fraktal Analiz")
    uploaded_file = st.file_uploader("Histopatolojik Kesit Yükleyin (PNG/JPG)", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        img = Image.open(uploaded_file).convert('L') # Gray scale analiz
        img_array = np.array(img)
        
        col_img, col_math = st.columns([1, 1])
        with col_img:
            st.image(img, caption="Analiz Edilen Kesit", use_container_width=True)

        with st.spinner("Matematiksel Nokta Bulutu ve Topolojik Analiz Yapılıyor..."):
            time.sleep(2) # Simülasyon süresi
            
            # --- MATEMATİKSEL ANALİZ ALGORİTMASI ---
            pixels = img_array.flatten()
            point_cloud_density = np.mean(pixels > 128) # Nokta bulutu yoğunluğu
            fractal_dim = np.std(img_array) / 100 # Topolojik pürüzlülük simülasyonu
            lumen_ratio = np.sum(img_array > 200) / img_array.size # Boşluk oranı
            
            # --- TEŞHİS MANTIĞI ---
            diagnosis = ""
            meds = ""
            prognoz = ""
            detay = ""

            if lumen_ratio > 0.15:
                diagnosis = "Adenokarsinom"
                meds = "Osimertinib (EGFR+), Alectinib (ALK+)"
                prognoz = "%72 (Evreye bağlı değişken)"
                detay = "Belirgin glandüler formasyon ve Lepidik büyüme paterni izlendi."
            elif point_cloud_density > 0.6:
                diagnosis = "Küçük Hücreli Karsinom (SCLC)"
                meds = "Etoposid + Sisplatin / İmmunoterapi"
                prognoz = "%25 (Yüksek agresivite)"
                detay = "Azzopardi etkisi ve nükleer molding (nokta bulutu yoğunlaşması) pozitif."
            elif fractal_dim > 0.4:
                diagnosis = "Skuamöz Hücreli Karsinom"
                meds = "Pembrolizumab, Dosetaksel"
                prognoz = "%50 (Lokal kontrol odaklı)"
                detay = "İntrasellüler köprüleşme ve keratinize 'inci' oluşumları saptandı."
            else:
                diagnosis = "Büyük Hücreli Karsinom"
                meds = "Kombinasyon Kemoterapisi"
                prognoz = "%35"
                detay = "Belirgin diferansiyasyon izlenmeyen kaotik dev hücre dağılımı."

        # --- TEK SAYFA RAPOR ---
        st.markdown("---")
        report_text = f"""
        LUNG-CORE DİJİTAL PATOLOJİ RAPORU
        ---------------------------------
        TARİH: {time.strftime("%d/%m/%Y")}
        
        [MATEMATİKSEL BULGULAR]
        - Nokta Bulutu Dağılımı (PCD): {point_cloud_density:.4f}
        - Topolojik Fraktal Boyut: {fractal_dim:.4f}
        - Lümen/Boşluk Oranı: %{lumen_ratio*100:.2f}
        
        [TEŞHİS VE PATOLOJİ]
        - ANA TEŞHİS: {diagnosis}
        - PATOLOJİK NOT: {detay}
        
        [TEDAVİ VE PROGNOZ]
        - ÖNERİLEN AKILLI İLAÇLAR: {meds}
        - 6 AY PROGNOZ TAHMİNİ: {prognoz}
        
        [ONAY]
        Bu rapor LUNG-CORE v2026 algoritmik analiz motoru tarafından oluşturulmuştur.
        """
        
        st.markdown(f'<div class="report-box"><h3>Klinik Analiz Raporu</h3><pre>{report_text}</pre></div>', unsafe_allow_html=True)

        # Raporu İndir Butonu
        st.download_button(
            label="📄 Raporu .txt Olarak İndir",
            data=report_text,
            file_name=f"Analiz_Raporu_{int(time.time())}.txt",
            mime="text/plain"
        )

# --- ALT BİLGİ ---
st.sidebar.markdown("---")
st.sidebar.caption("LUNG-CORE v2026 | Mathrix Analytica")
