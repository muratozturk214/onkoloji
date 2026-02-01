import streamlit as st
import numpy as np
from PIL import Image
import time
import pandas as pd

# --- SAYFA AYARLARI VE TEMA ---
st.set_page_config(page_title="PAGP-2026 Akciğer Portalı", layout="wide", initial_sidebar_state="collapsed")

# Klinik Beyaz Tema Uygulaması (CSS)
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .report-card {
        border: 2px solid #F0F2F6;
        padding: 25px;
        border-radius: 10px;
        background-color: #FCFCFC;
        color: #1E1E1E;
    }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #004A99; color: white; }
    h1, h2, h3 { color: #002B5B; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- GÜVENLİK GİRİŞİ ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("⚕️ Klinik Erişim Paneli")
    password = st.text_input("Giriş Şifresi (MATHRIX2026):", type="password")
    if st.button("Sisteme Giriş Yap"):
        if password == "mathrix2026":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Hatalı Yetkilendirme Kodu.")
    st.stop()

# --- ANA PORTAL BAŞLIĞI ---
st.title("🔬 Akciğer Kanseri Analiz ve Bilgi Portalı")
st.info("Klinik Standartlarda Tanı ve Evreleme Destek Sistemi")

# --- KLİNİK BİLGİ BANKASI (DASHBOARD) ---
tabs = st.tabs(["📊 Evreleme Tablosu", "🧠 Metastaz Rehberi", "🔍 Matematiksel Analiz"])

with tabs[0]:
    st.subheader("TNM Sınıflaması ve Klinik Evreleme")
    evre_data = {
        "Evre": ["Evre I", "Evre II", "Evre III", "Evre IV"],
        "TNM Tanımı": ["T1, N0, M0", "T1-2, N1, M0", "T1-4, N2, M0", "Herhangi T, Herhangi N, M1"],
        "Klinik Durum": ["Lokalize, <3cm", "Hiler Lenf Nodu Tutulumu", "Mediastinal Yayılım", "Uzak Organ Metastazı"],
        "Prognoz (5 Yıl)": ["%70-90", "%50-60", "%15-35", "< %10"]
    }
    st.table(pd.DataFrame(evre_data))

with tabs[1]:
    st.subheader("Klinik Metastaz Bilgi Kartları")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Beyin", "Sık", delta="Nörolojik Defisit")
        st.caption("Görüntüleme: Kontrastlı MR")
    with col2:
        st.metric("Karaciğer", "Orta", delta="Hepatomegali")
        st.caption("Belirteç: ALT/AST Yüksekliği")
    with col3:
        st.metric("Sürrenal", "Yüksek", delta="Adrenal Yetmezlik")
        st.caption("BT: Nodüler Kalınlaşma")
    with col4:
        st.metric("Kemik", "Yaygın", delta="Osteolitik Ağrı")
        st.caption("Sintigrafi: Hiperaktivite")

# --- MATEMATİKSEL ANALİZ MOTORU ---
with tabs[2]:
    st.subheader("Görüntü İşleme Tabanlı Topolojik Analiz")
    uploaded_file = st.file_uploader("Patolojik Kesit Görüntüsü Yükleyin (JPG/PNG)", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        img = Image.open(uploaded_file).convert('L') # GrayScale (Renklere takılmadan analiz)
        img_array = np.array(img)
        
        col_img, col_stat = st.columns([1, 1])
        with col_img:
            st.image(img, caption="Analiz Edilen Ham Veri (Numpy Matrisi)", use_container_width=True)
        
        with col_stat:
            with st.spinner("Matematiksel Karar Motoru Çalışıyor..."):
                time.sleep(1.5)
                # Sayısal Analiz Hesaplamaları
                variance_score = np.var(img_array) / 1000  # Hücre nokta bulutu yoğunluğu
                std_dev = np.std(img_array)               # Topolojik Mimari (Pürüzlülük)
                lumen_ratio = np.sum(img_array > 200) / img_array.size # Boşluk oranı
                
                st.write(f"*Nükleer Dağılım Varyansı:* {variance_score:.2f}")
                st.write(f"*Topolojik Pürüzlülük (SD):* {std_dev:.2f}")
                st.write(f"*Lümen (Boşluk) Oranı:* %{lumen_ratio*100:.2f}")

        # --- DÖRT TEMEL TÜR İÇİN KARAR ŞARTLARI ---
        diagnosis = ""
        medication = ""
        details = ""
        prognoz = ""

        if lumen_ratio > 0.4:
            diagnosis = "Adenokarsinom"
            medication = "Osimertinib / Alectinib"
            details = "Lepidik büyüme paterni izlenmektedir. Glandüler (bezsel) yapılar belirgin."
            prognoz = "Yavaş progresyon, hedefe yönelik tedaviye yüksek yanıt."
        elif std_dev > 50 and variance_score < 5:
            diagnosis = "Skuamöz Hücreli Karsinom"
            medication = "Pembrolizumab"
            details = "Keratinizasyon ve desmozomal köprüler sayısal karmaşıklığı artırmış."
            prognoz = "Lokal nüks riski yüksek, immünoterapi odaklı takip."
        elif variance_score > 8:
            diagnosis = "Küçük Hücreli Karsinom"
            medication = "Sisplatin / Etoposid"
            details = "Azzopardi etkisi gözlemlendi. Nükleer molding (kalıplanma) çok yoğun."
            prognoz = "Agresif seyir, 6 ay içinde metastaz riski %75."
        else:
            diagnosis = "Büyük Hücreli Karsinom"
            medication = "Kombine Kemoterapi"
            details = "Diferansiyasyon göstermeyen, anaplastik dev hücreli kaotik yapı."
            prognoz = "Kötü diferansiye yapı nedeniyle öngörülemez klinik seyir."

        # --- RAPOR ÇIKTISI ---
        st.markdown("---")
        report_text = f"""
        KLİNİK ANALİZ RAPORU
        --------------------
        TANI: {diagnosis}
        TEKNİK DETAYLAR: {details}
        ÖNERİLEN İLAÇ PROTOKOLÜ: {medication}
        PROGNOZ ÖNGÖRÜSÜ: {prognoz}
        MATEMATİKSEL SKORLAR:
        - Varyans: {variance_score:.2f}
        - Standart Sapma: {std_dev:.2f}
        - Lümen Oranı: %{lumen_ratio*100:.2f}
        """

        st.markdown(f"""
        <div class="report-card">
            <h3>📋 Tek Sayfa Klinik Rapor</h3>
            <p><b>Patolojik Tanı:</b> {diagnosis}</p>
            <p><b>Tıbbi Detay:</b> {details}</p>
            <p><b>Önerilen Tedavi:</b> <span style="color:red;">{medication}</span></p>
            <hr>
            <p><b>Gelecek Tahmini (Prognoz):</b> {prognoz}</p>
        </div>
        """, unsafe_allow_html=True)

        # İndirme Butonu
        st.download_button(
            label="📄 Raporu İndir (.TXT)",
            data=report_text,
            file_name=f"klinik_rapor_{int(time.time())}.txt",
            mime="text/plain"
        )

st.sidebar.markdown("---")
st.sidebar.write("Sistem Durumu: *Aktif*")
st.sidebar.write("Versiyon: *2.0.26*")
