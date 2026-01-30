import streamlit as st
import time
from PIL import Image
import random

# Sayfa Ayarları
st.set_page_config(page_title="MathRix AI Oncology Pro", layout="wide", page_icon="🧪")

# --- GELİŞMİŞ GÖRSEL TASARIM (SİYAH KUTULAR KALDIRILDI) ---
st.markdown("""
    <style>
    /* Ana Arka Plan: Koyu Lacivertten Gece Mavisine Yumuşak Geçiş */
    .stApp {
        background: linear-gradient(160deg, #001529 0%, #003366 100%);
        color: #e6f7ff;
    }
    
    /* Neon Mavi Giriş Kartı */
    .login-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(20px);
        padding: 50px;
        border-radius: 30px;
        border: 2px solid #00d4ff;
        text-align: center;
        box-shadow: 0px 0px 40px rgba(0, 212, 255, 0.4);
    }

    /* Şeffaf Bilgi Kartları (Siyah Değil!) */
    .glass-box {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 212, 255, 0.3);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .glass-box:hover {
        border: 1px solid #00d4ff;
        box-shadow: 0px 0px 15px rgba(0, 212, 255, 0.2);
    }

    /* Başlık Stilleri */
    h1, h2, h3 {
        color: #00d4ff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Buton Stili */
    .stButton>button {
        background: linear-gradient(90deg, #00d4ff, #008cff);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: bold;
        padding: 10px 25px;
        transition: 0.5s;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GİRİŞ EKRANI (ŞIK VE MAVİ) ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.markdown("<br><br><div class='login-card'>", unsafe_allow_html=True)
        st.markdown("<h1>🧬 MATHRIX CORE</h1>", unsafe_allow_html=True)
        st.write("Profesyonel Onkoloji Karar Destek Sistemine Hoş Geldiniz")
        password = st.text_input("Erişim Anahtarını Girin:", type="password")
        if st.button("SİSTEMİ YÜKLE"):
            if password == "mathrix2026":
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Erişim Reddedildi: Geçersiz Anahtar.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- ANA PANEL ---
st.markdown("<h1 style='text-align: center;'>🧪 MATHRIX AI: ONKOLOJİK ANALİZ VE 3T REHBERİ</h1>", unsafe_allow_html=True)

# --- GELİŞMİŞ BİLGİ BANKASI ---
st.markdown("### 📘 Klinik Bilgi ve İlaç Taksonomisi")
tab1, tab2, tab3 = st.tabs(["📂 Kanser Tipleri", "💊 İlaç Mekanizmaları", "📊 Karşılaştırma Analizi"])

with tab1:
    st.markdown("#### Akciğer Karsinomu Morfolojik Dalları")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='glass-box'><b style='color:#00d4ff;'>🔹 Adenokarsinom</b><br><br>En sık görülen tiptir. Müsin üreten glandüler hücrelerden gelişir. Genetik testlere (EGFR/ALK) en iyi yanıt veren gruptur.</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='glass-box'><b style='color:#ff4b4b;'>🔸 Skuamöz Hücreli</b><br><br>Genelde bronşların merkezinde, sigara içiciliğiyle ilişkili olarak keratinleşen hücrelerden oluşur. Agresif seyirlidir.</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='glass-box'><b style='color:#ffa500;'>🔸 Büyük Hücreli</b><br><br>Hücreleri çok büyüktür ve belirgin nükleollere sahiptir. Hızlı yayılım gösterir ve erken metastaz yapma eğilimindedir.</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("#### 🏥 Onkolojik İlaç ve Tedavi Dalları")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class='glass-box'>
        <b style='color:#00d4ff;'>🎯 Hedefe Yönelik Tedaviler (Akıllı İlaçlar)</b><br><br>
        • <b>Osimertinib:</b> EGFR mutasyonlarını doğrudan bloke eder.<br>
        • <b>Alectinib:</b> ALK füzyon genlerini durdurur.<br>
        • <b>Bevacizumab:</b> Tümörün kanlanmasını engelleyen anjiyogenez inhibitörüdür.
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class='glass-box'>
        <b style='color:#00ff99;'>🛡️ İmmünoterapi (Bağışıklık Modülatörleri)</b><br><br>
        • <b>Pembrolizumab:</b> PD-1 yolunu kapatarak bağışıklık sistemini aktif eder.<br>
        • <b>Nivolumab:</b> T-hücrelerinin kanseri tanımasını sağlar.<br>
        • <b>Ipilimumab:</b> CTLA-4 inhibitörü olarak bağışıklık yanıtını güçlendirir.
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.table({
        "Özellik": ["Birincil Konum", "En Sık Mutasyon", "Yayılım Hızı", "Alt Tip"],
        "Adeno": ["Periferik (Dış)", "EGFR, ALK, ROS1", "Orta", "Glandüler"],
        "Skuamöz": ["Santral (Merkez)", "FGFR1, PIK3CA", "Hızlı", "Yassı Epitel"],
        "Büyük Hücreli": ["Diffüz (Yaygın)", "Belirsiz", "Çok Hızlı", "Pleomorfik"]
    })

st.divider()

# --- ANALİZ PANELİ ---
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("📁 Vaka Giriş Ünitesi")
    uploaded_file = st.file_uploader("Dijital Patoloji Görüntüsünü Yükle", type=["jpg", "png", "jpeg"])
    
    st.markdown("---")
    metastaz_alanlari = st.multiselect(
        "Metastaz Saptanan Alanları İşaretleyin:",
        ["Beyin", "Karaciğer", "Kemik", "Sürrenal (Böbrek Üstü)", "Lenf Düğümü"]
    )
    
    evre_sonucu = "Evre 4 (İleri Metastatik)" if metastaz_alanlari else "Evre 1-3 (Lokal Yayılım)"
    st.markdown(f"<div style='background:rgba(0,212,255,0.1); padding:15px; border-radius:12px;'><b>Mevcut Evre:</b> <span style='color:#00d4ff;'>{evre_sonucu}</span></div>", unsafe_allow_html=True)

with col_right:
    if uploaded_file:
        st.image(Image.open(uploaded_file), use_container_width=True, caption="İncelenen Doku Kesiti")
        
        if st.button("🔬 DERİN ANALİZİ VE 3T RAPORUNU BAŞLAT"):
            with st.status("Neural Core Derin Analiz Yapıyor...", expanded=True) as status:
                st.write("Hücresel nükleer atipi taranıyor...")
                time.sleep(1)
                st.write("Pleomorfik yapılar skorlanıyor...")
                time.sleep(1)
                status.update(label="Analiz Başarıyla Tamamlandı!", state="complete", expanded=False)
            
            secilen_tur = random.choice(["Adenokarsinom", "Skuamöz Hücreli Karsinom", "Büyük Hücreli Karsinom"])
            risk = random.uniform(94.2, 99.8)
            
            # --- DETAYLI ANALİZ ÇIKTISI ---
            st.error(f"### 🚩 KRİTİK BULGU: {secilen_tur.upper()}")
            
            # Bu metin ekranda gözükecek
            analiz_metni = f"""
            *1. TANI (Diagnosis):* Yapılan mikroskobik taramada *%{risk:.1f}* olasılıkla *{secilen_tur}* tespit edilmiştir. Hücre çekirdeklerinde hiperkromazi ve belirgin nükleer kontur düzensizliği izlenmektedir.
            
            *2. TEDAVİ (Therapy):* {evre_sonucu} protokolü uyarınca; 
            - PD-L1 testi çalışılarak uygunsa *Pembrolizumab* tedavisi,
            - Genetik mutasyon saptanırsa (EGFR+) *Osimertinib* kullanımı değerlendirilmelidir.
            
            *3. TAKİP (Tracking):* Agresif seyir potansiyeli nedeniyle 8-12 haftalık periyotlarla PET-BT ve tümör marker (CEA, CYFRA 21-1) takibi önerilir.
            """
            st.markdown(analiz_metni)
            
            # --- İNDİRİLECEK RAPOR (EKRANDAKİYLE AYNI VE DETAYLI) ---
            rapor_dosyasi = f"""
            MATHRIX AI ONKOLOJI - RESMI VAKA ANALIZ RAPORU
            -------------------------------------------
            TARIH: {time.strftime('%d/%m/%Y')} | RAPOR ID: MX-{random.randint(1000,9999)}
            
            [TANI ANALIZI]
            Saptanan Tur: {secilen_tur}
            Analiz Guven Skoru: %{risk:.1f}
            Klinik Evreleme: {evre_sonucu}
            Metastazlar: {', '.join(metastaz_alanlari) if metastaz_alanlari else 'Yok'}
            
            [TIBBI DEGERLENDIRME]
            Dokuda saptanan {secilen_tur} ile uyumlu pleomorfik nukleuslar ve malign hucre karsinomlari 
            karar destek sistemi tarafindan onaylanmistir.
            
            [3T TEDAVI YOL HARITASI]
            - Tani: NGS ve IHC boyama ile teshis kesinlestirilmelidir.
            - Tedavi: {evre_sonucu} icin Immunoterapi veya Akilli Ilac kombinasyonu planlanmalidir.
            - Takip: 3 aylik periyotlarla PET-BT radyolojik izlem.
            
            Bu rapor lise seviyesi bir AI projesi simülasyonudur.
            -------------------------------------------
            MathRix Health Systems 2026
            """
            
            st.download_button(
                label="📩 TÜM ANALİZİ RAPOR OLARAK İNDİR",
                data=rapor_dosyasi,
                file_name=f"MathRix_Final_Rapor_{secilen_tur}.txt",
                mime="text/plain"
            )
    else:
        st.info("Analiz için lütfen soldaki panelden bir görsel yükleyin.")

st.markdown("<br><hr><center>MathRix Global Health Systems © 2026 | Professional Oncology Analytics</center>", unsafe_allow_html=True)
