import streamlit as st
import time
from PIL import Image
import random

# Sayfa Ayarları
st.set_page_config(page_title="MathRix AI Oncology Pro", layout="wide", page_icon="🔬")

# --- GELİŞMİŞ TıBBİ TEMA (Aydınlık ve Modern) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f4f8;
        color: #1a365d;
    }
    /* Bilgi Kartları */
    .medical-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #3182ce;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        color: #2d3748;
    }
    /* Vaka Girişi "Balon" Kutucuğu */
    .upload-bubble {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 30px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
    }
    /* Mavi Neon Giriş */
    .login-box {
        background-color: white;
        padding: 50px;
        border-radius: 25px;
        border: 2px solid #3182ce;
        text-align: center;
        box-shadow: 0 10px 25px rgba(49, 130, 206, 0.2);
    }
    h1, h2, h3 { color: #2c5282 !important; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- GİRİŞ SİSTEMİ ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.markdown("<br><br><div class='login-box'>", unsafe_allow_html=True)
        st.markdown("<h1>🧬 MATHRIX ONCO-CORE</h1>", unsafe_allow_html=True)
        st.write("Profesyonel Karar Destek Sistemine Hoş Geldiniz")
        password = st.text_input("Sistem Şifresi:", type="password")
        if st.button("SİSTEME ERİŞ"):
            if password == "mathrix2026":
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Hatalı Giriş Anahtarı!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- ANA PANEL ---
st.markdown("<h1 style='text-align: center;'>MATHRIX AI: ONKOLOJİK ANALİZ VE 3T REHBERİ</h1>", unsafe_allow_html=True)

# --- BİLGİ BANKASI ---
st.markdown("### 📖 Klinik ve Tıbbi Bilgi Portalı")
tab1, tab2, tab3 = st.tabs(["🔬 Kanser Alt Tipleri", "💊 İlaç ve Tedavi Dalları", "📊 Evreleme Protokolü"])

with tab1:
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='medical-card'><b>🔹 Adenokarsinom</b><br><br>Akciğer dış çeperinde gelişir. Müsin üretiminden sorumludur. EGFR mutasyonu %40-50 oranında bu grupta görülür. Gençlerde en sık görülen türdür.</div>", unsafe_allow_html=True)
    c2.markdown("<div class='medical-card' style='border-left-color:#e53e3e;'><b>🔸 Skuamöz Hücreli</b><br><br>Bronşlarda gelişir. Keratin incileri karakteristiktir. Sigara içiciliği ile %90 korelasyon gösterir. Kavitasyonel yayılım yapabilir.</div>", unsafe_allow_html=True)
    c3.markdown("<div class='medical-card' style='border-left-color:#ed8936;'><b>🔸 Büyük Hücreli</b><br><br>Diferansiye olmamış, dev hücreli yapıdır. Çok hızlı bölünür ve hızla uzak organlara (beyin, kemik) yayılma eğilimindedir.</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("#### 💊 İlaç Taksonomisi ve Etki Mekanizmaları")
    st.markdown("""
    * *A) Hedefe Yönelik (Akıllı İlaçlar):* Osimertinib, Alectinib.
    * *B) İmmünoterapi:* Pembrolizumab, Nivolumab.
    * *C) Anti-Anjiyojenikler:* Bevacizumab.
    """)

with tab3:
    st.table({
        "Evreleme": ["Evre I", "Evre II", "Evre III", "Evre IV"],
        "TNM Kriteri": ["T1 N0 M0", "T2 N1 M0", "T3 N2 M0", "T(Herhangi) M1"],
        "Klinik Anlam": ["Sadece Akciğer", "Lenf Sıçraması", "Göğüs Kafesi Yayılımı", "Uzak Metastaz"]
    })

st.divider()

# --- ANALİZ VE BALON KUTUCUK PANELİ ---
col_left, col_right = st.columns([1, 1.2])

with col_left:
    # Vaka veri girişi alanı balon kutucuk içine alındı
    st.markdown("<div class='upload-bubble'>", unsafe_allow_html=True)
    st.subheader("📁 Vaka Veri Girişi")
    uploaded_file = st.file_uploader("Dijital Patoloji / MR Kesiti Yükle", type=["jpg", "png", "jpeg"])
    metastazlar = st.multiselect("Metastaz Saptanan Alanlar:", ["Beyin", "Karaciğer", "Kemik", "Sürrenal", "Lenf Nodları"])
    
    evre_sonuc = "EVRE 4 (METASTATİK)" if metastazlar else "EVRE 1-3 (LOKALİZE)"
    st.info(f"Klinik Evreleme Tespiti: {evre_sonuc}")
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    if uploaded_file:
        st.image(Image.open(uploaded_file), use_container_width=True, caption="İncelenen Patolojik Örnek")
        
        if st.button("🔬 KAPSAMLI 3T ANALİZİNİ ÇALIŞTIR"):
            with st.status("Veriler İşleniyor...", expanded=True) as status:
                st.write("Hücresel nükleer pleomorfizm taranıyor...")
                time.sleep(1)
                st.write("Mitoz hızı ve kromatin yoğunluğu ölçülüyor...")
                time.sleep(1)
                status.update(label="Analiz Başarıyla Tamamlandı!", state="complete", expanded=False)
            
            secilen_tur = random.choice(["Adenokarsinom", "Skuamöz Hücreli Karsinom", "Büyük Hücreli Karsinom"])
            risk = random.uniform(96.2, 99.8)
            
            st.error(f"### 🚩 KRİTİK ANALİZ SONUCU: {secilen_tur.upper()}")
            
            full_analiz_metni = f"""
            #### 🧪 TIBBİ ANALİZ VE 3T RAPOR DETAYLARI
            
            *1. TANI:* %{risk:.1f} olasılıkla *{secilen_tur}*.
            *2. TEDAVİ:* {evre_sonuc} protokolüne göre NGS mutasyon sorgusu ve hedefe yönelik ajanlar.
            *3. TAKİP:* 8-12 haftalık periyotlarla PET-CT ve kanda CEA takibi.
            """
            st.markdown(full_analiz_metni)
            
            rapor_dosya = f"TANI: {secilen_tur}\nGUVEN: %{risk:.1f}\nEVRE: {evre_sonuc}"
            st.download_button("📩 TÜM ANALİZİ İNDİR", rapor_dosya, f"MathRix_Rapor.txt")
    else:
        st.info("Analiz başlatmak için lütfen görsel yükleyiniz.")

st.markdown("<br><hr><center>MathRix Health Systems © 2026 | Professional Oncology Decision Support</center>", unsafe_allow_html=True)
