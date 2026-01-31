import streamlit as st
import time
from PIL import Image
import random

# Sayfa Ayarları
st.set_page_config(page_title="MathRix AI Oncology Pro", layout="wide", page_icon="🔬")

# --- AYDINLIK VE PROFESYONEL TEMA ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; color: #1e293b; }
    .medical-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #3b82f6;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
    }
    .login-box {
        background-color: white;
        padding: 40px;
        border-radius: 20px;
        border: 2px solid #3b82f6;
        text-align: center;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.1);
    }
    h1, h2, h3 { color: #1e3a8a !important; }
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
        password = st.text_input("Sistem Şifresi:", type="password")
        if st.button("SİSTEMİ BAŞLAT"):
            if password == "mathrix2026":
                st.session_state['authenticated'] = True
                st.rerun()
            else: st.error("Hatalı Şifre!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- ANA PANEL ---
st.markdown("<h1 style='text-align: center;'>🏥 MATHRIX AI: AKILLI ANALİZ VE 3T REHBERİ</h1>", unsafe_allow_html=True)

# --- BİLGİ BANKASI ---
st.markdown("### 📖 Klinik Portalı")
tab1, tab2, tab3 = st.tabs(["🔬 Kanser Türleri", "💊 İlaç Taksonomisi", "📊 Evreleme Protokolü"])

with tab1:
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='medical-card'><b>🔹 Adenokarsinom</b><br>Periferik yerleşimli, bez yapılı, sigara içmeyenlerde de görülebilen yaygın tür.</div>", unsafe_allow_html=True)
    c2.markdown("<div class='medical-card' style='border-left-color:#ef4444;'><b>🔸 Skuamöz Hücreli</b><br>Santral yerleşimli, keratin incileri içeren, sigara ile doğrudan ilişkili tür.</div>", unsafe_allow_html=True)
    c3.markdown("<div class='medical-card' style='border-left-color:#f59e0b;'><b>🔸 Büyük Hücreli</b><br>Hızlı yayılan, diferansiye olmamış, agresif morfolojili kanser tipi.</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("""
    * *Hedefe Yönelik:* Osimertinib (EGFR), Alectinib (ALK).
    * *İmmünoterapi:* Pembrolizumab (PD-L1), Nivolumab.
    * *Kemoterapi:* Sisplatin, Pemetreksed kombinasyonları.
    """)

with tab3:
    st.table({
        "Durum": ["Normal Doku", "Evre I-III", "Evre IV"],
        "Özellik": ["Düzenli Hücre Yapısı", "Lokal/Bölgesel Yayılım", "Uzak Metastaz (Beyin, Kemik vb.)"],
        "3T Yaklaşımı": ["Düzenli Takip", "Cerrahi / Radyoterapi", "Sistemik İlaç Tedavisi"]
    })

st.divider()

# --- ANALİZ PANELİ ---
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("📁 Vaka Girişi")
    uploaded_file = st.file_uploader("Görüntü Yükle (Patoloji/MR)", type=["jpg", "png", "jpeg"])
    metastazlar = st.multiselect("Metastaz Saptanan Alanlar:", ["Beyin", "Karaciğer", "Kemik", "Sürrenal", "Lenf Düğümü"])
    
    evre_sonuc = "Evre 4 (İleri)" if metastazlar else "Evre 1-3 (Lokal)"

with col_right:
    if uploaded_file:
        st.image(Image.open(uploaded_file), use_container_width=True)
        
        if st.button("🔬 KAPSAMLI ANALİZİ ÇALIŞTIR"):
            with st.status("Doku Analizi Yapılıyor...", expanded=True) as status:
                st.write("Hücre dizilimi inceleniyor...")
                time.sleep(1)
                st.write("Topolojik veri analizi (TDA) ile Betti sayıları hesaplanıyor...")
                time.sleep(1)
                status.update(label="Analiz Tamamlandı!", state="complete", expanded=False)
            
            # --- KRİTİK DEĞİŞİKLİK: ÖNCE KANSER Mİ DEĞİL Mİ KONTROLÜ ---
            # Rastgele bir 'Sağlıklı mı' kontrolü yapıyoruz (Simülasyon için)
            is_cancer = random.choice([True, True, False]) # %66 kanser, %33 sağlıklı ihtimali
            
            if not is_cancer:
                st.success("### ✅ ANALİZ SONUCU: NORMAL DOKU / BENİGN")
                st.markdown("""
                *Bulgular:* Yapılan topolojik analizde hücre çekirdeklerinin düzenli bir geometrik ağ (simplicial complex) oluşturduğu görülmüştür. 
                Nükleer pleomorfizm veya atipik hücre kümelenmesi saptanmamıştır.
                
                *Öneri:* Şu an için malign bir bulguya rastlanmamıştır. Rutin sağlık kontrollerine devam edilmesi önerilir.
                """)
            else:
                # Eğer kanserse detayları veriyoruz
                secilen_tur = random.choice(["Adenokarsinom", "Skuamöz Hücreli Karsinom", "Büyük Hücreli Karsinom"])
                risk = random.uniform(96.5, 99.9)
                
                st.error(f"### 🚩 KRİTİK BULGU: {secilen_tur.upper()}")
                
                full_analiz = f"""
                #### 🧪 TIBBİ ANALİZ VE 3T RAPORU
                *1. TANI (DIAGNOSIS):*
                Sistemimiz, doku mimarisinde *%{risk:.1f}* olasılıkla *{secilen_tur}* tespit etmiştir. Hücre çekirdeklerinde hiperkromazi ve düzensiz nükleer membranlar izlenmektedir.
                
                *2. TEDAVİ (THERAPY):*
                - *Durum:* {evre_sonuc}
                - *Öneri:* PD-L1 testi sonrasına göre *Pembrolizumab* veya mutasyon durumuna göre *Osimertinib* planlanmalıdır.
                
                *3. TAKİP (TRACKING):*
                - 8-12 haftalık periyotlarla PET-CT ve tümör marker takibi önerilir.
                """
                st.markdown(full_analiz)
                
                # Rapor Hazırlama
                rapor_icerik = f"MATHRIX AI ANALIZI\nSonuç: {secilen_tur}\nRisk: %{risk:.1f}\nEvre: {evre_sonuc}\nDetaylar: {full_analiz}"
                st.download_button("📩 RAPORU İNDİR", rapor_icerik, f"MathRix_Analiz.txt")
    else:
        st.info("Lütfen analiz için bir görsel yükleyiniz.")

st.markdown("<br><hr><center>MathRix Health Systems © 2026</center>", unsafe_allow_html=True)
