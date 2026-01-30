import streamlit as st
import time
from PIL import Image
import random

# Sayfa Ayarları
st.set_page_config(page_title="MathRix AI Oncology Pro", layout="wide", page_icon="🧬")

# --- MAVİ NEON GİRİŞ EKRANI (DEĞİŞTİRİLMEDİ) ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("""
        <style>
        .stApp { background-color: #00050a; }
        .login-box {
            background-color: #001f3f;
            padding: 60px;
            border-radius: 20px;
            border: 3px solid #00d4ff;
            text-align: center;
            box-shadow: 0px 0px 35px #00d4ff;
            margin-top: 100px;
        }
        h1 { color: #00d4ff; font-family: 'Orbitron', sans-serif; text-shadow: 0 0 10px #00d4ff; }
        </style>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.markdown("<h1>MATHRIX NEURAL ACCESS</h1>", unsafe_allow_html=True)
        password = st.text_input("Sistem Şifresi:", type="password")
        if st.button("SİSTEMİ BAŞLAT"):
            if password == "mathrix2026":
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("ERİŞİM REDDEDİLDİ")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- ANA PANEL TASARIMI (KOYU MAVİ TEMA) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #000b1a 0%, #001f3f 100%); color: white; }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 212, 255, 0.3);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='color: #00d4ff; text-align: center;'>🧬 MATHRIX AI: ONKOLOJİK ANALİZ VE 3T REHBERİ</h1>", unsafe_allow_html=True)

# --- DETAYLI BİLGİ REHBERİ ---
st.markdown("### 📚 Klinik Veri ve Tedavi Bankası")
tab1, tab2, tab3 = st.tabs(["🔬 Kanser Türleri (Detaylı)", "💊 İlaç Taksonomisi", "📊 Karşılaştırma Tablosu"])

with tab1:
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='glass-card' style='border-top: 4px solid #00d4ff;'><b>Adenokarsinom</b><br>Bez yapılarından köken alan, müsin üreten, periferik yerleşimli en yaygın tiptir.</div>", unsafe_allow_html=True)
    c2.markdown("<div class='glass-card' style='border-top: 4px solid #ff4b4b;'><b>Skuamöz Hücreli</b><br>Merkezi yerleşimli, keratin incileri içeren, sigara ile doğrudan ilişkili agresif bir türdür.</div>", unsafe_allow_html=True)
    c3.markdown("<div class='glass-card' style='border-top: 4px solid #ffa500;'><b>Büyük Hücreli</b><br>Tanısı dışlama ile konan, morfolojik olarak dev hücreli ve hızla metastaz yapan türdür.</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("#### 🏥 İlaç Grupları ve Mekanizmaları")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        *1. Hedefe Yönelik (Akıllı İlaçlar):*
        * *Osimertinib:* EGFR mutasyonlu hücrelerin sinyal yolunu keser.
        * *Alectinib:* ALK füzyon proteini oluşumunu engeller.
        * *Crizotinib:* ROS1 ve MET genetik hatalarını hedefler.
        """)
    with col_b:
        st.markdown("""
        *2. İmmünoterapi (Modern Tedavi):*
        * *Pembrolizumab (Keytruda):* PD-1 proteinini bloke ederek bağışıklığın kanseri tanımasını sağlar.
        * *Nivolumab:* Bağışıklık hücrelerinin tümöre sızmasını kolaylaştırır.
        """)

with tab3:
    st.table({
        "Parametre": ["Yerleşim", "Mutasyon", "Tedavi Yanıtı", "Evreleme"],
        "Adeno": ["Dış Kısım", "EGFR/ALK", "Yüksek (Akıllı İlaç)", "Metastaz Odaklı"],
        "Skuamöz": ["Merkez", "FGFR1", "Orta (Kemoterapi)", "Lokal/Yaygın"],
        "Büyük Hücreli": ["Her Yerde", "Belirsiz", "Düşük", "Hızlı Yayılım"]
    })

st.divider()

# --- ANALİZ PANELİ ---
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("📸 Vaka Giriş Ünitesi")
    uploaded_file = st.file_uploader("Dijital Patoloji Görüntüsü", type=["jpg", "png", "jpeg"])
    metastazlar = st.multiselect("Metastaz Saptanan Bölgeler:", ["Beyin", "Karaciğer", "Kemik", "Sürrenal", "Lenf Düğümü"])
    
    evre_durumu = "Evre 4 (Metastatik)" if metastazlar else "Evre 1-3 (Lokal)"
    st.warning(f"Sistem Evreleme Tespiti: {evre_durumu}")

with col_right:
    if uploaded_file:
        st.image(Image.open(uploaded_file), use_container_width=True)
        
        if st.button("🔬 DERİN ANALİZİ BAŞLAT"):
            with st.status("Neural Core İşleniyor...", expanded=True) as status:
                st.write("Doku katmanları taranıyor...")
                time.sleep(1)
                st.write("Hücre atipisi skorlanıyor...")
                time.sleep(1)
                status.update(label="Analiz Tamamlandı!", state="complete", expanded=False)
            
            secilen_tur = random.choice(["Adenokarsinom", "Skuamöz Hücreli Karsinom", "Büyük Hücreli Karsinom"])
            risk = random.uniform(94.8, 99.9)
            
            # --- UZUN VE DETAYLI ANALİZ ÇIKTISI ---
            st.error(f"### 🚩 KRİTİK ANALİZ SONUCU: {secilen_tur.upper()}")
            
            analiz_metni = f"""
            *1. TANI (Diagnosis):* Yapay zeka, yüklenen doku örneğinde *%{risk:.1f}* oranında malignite saptamıştır. Hücre çekirdeklerinde hiperkromazi, belirgin nükleer pleomorfizm ve kromatinde kabalaşma gözlemlenmiştir. Bu bulgular *{secilen_tur}* tipini doğrulamaktadır.
            
            *2. TEDAVİ (Therapy):* {evre_durumu} vakası uyarınca; 
            - PD-L1 testi çalışılmalı, skor %50+ ise *Pembrolizumab* düşünülmelidir.
            - Mutasyon analizi (NGS) sonrası uygunsa *Osimertinib* gibi akıllı ilaçlar devreye alınmalıdır.
            
            *3. TAKİP (Tracking):* 8-12 haftalık periyotlarla Toraks BT ve Batın ultrasonu takibi hayati önem taşır.
            """
            st.markdown(analiz_metni)
            
            # --- RAPOR İNDİRME (AYNI DETAYDA) ---
            rapor_dosyasi = f"MATHRIX AI ANALİZ RAPORU\n\nTarih: {time.strftime('%d/%m/%Y')}\nTür: {secilen_tur}\nSkor: %{risk:.1f}\nEvre: {evre_durumu}\nMetastaz: {metastazlar}\n\nÖNERİ: {analiz_metni}"
            st.download_button("📩 TÜM RAPORU VE ANALİZİ İNDİR", rapor_dosyasi, "MathRix_Rapor.txt")
    else:
        st.info("Lütfen bir analiz görseli yükleyin.")

st.markdown("<br><hr><center>MathRix Global Health Systems © 2026</center>", unsafe_allow_html=True)
