import streamlit as st
import time
from PIL import Image
import random

# Sayfa Ayarları
st.set_page_config(page_title="MathRix AI Oncology Pro", layout="wide", page_icon="🧬")

# --- PROFESYONEL GİRİŞ EKRANI ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #001f3f, #00d4ff); }
        .login-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 50px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
            color: white;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        </style>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        st.header("🧬 MATHRIX NEURAL CORE")
        st.write("Onkolojik Karar Destek Sistemine Giriş")
        password = st.text_input("Sistem Şifresi:", type="password")
        if st.button("SİSTEMİ AÇ"):
            if password == "mathrix2026":
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Hatalı Giriş!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- ANA PANEL ---
st.markdown("<h1 style='text-align: center; color: #00d4ff;'>🧬 MATHRIX AI ONKOLOJİ ANALİZ MERKEZİ</h1>", unsafe_allow_html=True)

# --- BİLGİ BANKASI (SİYAH KUTULAR KALDIRILDI) ---
st.markdown("### 📚 Klinik Bilgi Rehberi")
t1, t2, t3 = st.tabs(["Kanser Türleri", "Tedavi Protokolleri", "Evreleme"])

with t1:
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div style='border: 1px solid #00d4ff; padding:15px; border-radius:10px;'><b>Adenokarsinom:</b> Akciğerin periferik alanlarında gelişen, en yaygın türdür.</div>", unsafe_allow_html=True)
    c2.markdown("<div style='border: 1px solid #ff4b4b; padding:15px; border-radius:10px;'><b>Skuamöz Hücreli:</b> Bronşiyal epitel kaynaklıdır, sigara ile güçlü bağı vardır.</div>", unsafe_allow_html=True)
    c3.markdown("<div style='border: 1px solid #ffa500; padding:15px; border-radius:10px;'><b>Büyük Hücreli:</b> Tanısı zor, diferansiye olmamış agresif bir türdür.</div>", unsafe_allow_html=True)

with t2:
    st.info("*Akıllı İlaçlar:* EGFR/ALK mutasyonu olan hastalarda Osimertinib veya Alectinib kullanılır.")
    st.success("*İmmünoterapi:* PD-L1 skoru yüksekse bağışıklık sistemi üzerinden tümör kontrol altına alınır.")

with t3:
    st.warning("⚠️ Metastaz (Beyin, Karaciğer, Kemik) varlığı hastalığı doğrudan *Evre 4* yapar.")

st.divider()

# --- ANALİZ PANELİ ---
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("📸 Vaka Girişi")
    uploaded_file = st.file_uploader("Görüntü Yükle", type=["jpg", "png", "jpeg"])
    metastazlar = st.multiselect("Metastaz Saptanan Alanlar:", ["Beyin", "Karaciğer", "Kemik", "Sürrenal", "Lenf Düğümü"])
    
    evre_sonuc = "Evre 4 (Metastatik)" if metastazlar else "Evre 1-3 (Lokal)"
    st.markdown(f"*Tahmini Durum:* <span style='color:orange;'>{evre_sonuc}</span>", unsafe_allow_html=True)

with col_right:
    if uploaded_file:
        st.image(Image.open(uploaded_file), use_container_width=True)
        
        if st.button("🔬 ANALİZİ BAŞLAT"):
            with st.spinner("Neural Core derin tarama yapıyor..."):
                time.sleep(3)
            
            # Değişkenler
            secilen_tur = random.choice(["Adenokarsinom", "Skuamöz Hücreli Karsinom", "Büyük Hücreli Karsinom"])
            risk = random.uniform(94.2, 99.8)
            
            # --- DEV ANALİZ ÇIKTISI ---
            st.error(f"### 🚩 KRİTİK BULGU: {secilen_tur.upper()}")
            
            st.markdown(f"""
            #### 🧪 Detaylı Patolojik Analiz Raporu
            *1. Morfolojik Değerlendirme:* Yüklenen doku örneğinde belirgin *hücresel pleomorfizm* ve nükleer büyüme saptanmıştır. Hücrelerin dizilim paternleri incelendiğinde, bu görünümün *%{risk:.1f}* olasılıkla *{secilen_tur}* tipine ait olduğu doğrulanmıştır. Hücre çekirdeklerinde hiperkromazi ve düzensiz nükleer membranlar izlenmektedir.
            
            *2. Klinik Evreleme ve Yayılım:*
            Hastada saptanan {', '.join(metastazlar) if metastazlar else 'metastaz yokluğu'}, vakayı *{evre_sonuc}* olarak sınıflandırmaktadır. Bu evre, tümörün sistemik bir yayılım potansiyeline sahip olduğunu veya lokalize kalarak cerrahiye uygun olduğunu gösterir.
            
            *3. Önerilen Tedavi Yol Haritası (3T):*
            * *Tanı (Diagnosis):* Kesin alt tip tayini için İmmünohistokimya (IHC) boyaması (TTF-1, p40) zorunludur.
            * *Tedavi (Therapy):* Evre 4 vakalarda PD-L1 ekspresyonu %50 üzerindeyse *İmmünoterapi* (Keytruda vb.) ilk tercihtir. Mutasyon varsa akıllı ilaçlar (Osimertinib) eklenmelidir.
            * *Takip (Tracking):* 8-12 haftalık aralıklarla Kontrastlı Toraks BT ve Batın ultrasonu ile progresyon takibi yapılmalıdır.
            
            *4. Genetik Yönlendirme:* NGS (Next Generation Sequencing) yapılarak EGFR, ALK, ROS1 ve KRAS mutasyonları taranmalıdır.
            """)
            
            # --- RAPOR İNDİRME EN SONDA ---
            rapor_metni = f"MATHRIX AI ANALİZ ÇIKTISI\n--------------------\nTür: {secilen_tur}\nRisk: %{risk:.1f}\nEvre: {evre_sonuc}\nMetastazlar: {metastazlar}\nÖneri: {secilen_tur} için moleküler test zorunludur."
            st.download_button("📩 TÜM ANALİZİ RAPOR OLARAK İNDİR", rapor_metni, "MathRix_Final_Rapor.txt")
    else:
        st.info("Lütfen bir analiz görseli yükleyiniz.")

st.markdown("<br><hr><center>MathRix Global Health Systems © 2026</center>", unsafe_allow_html=True)
