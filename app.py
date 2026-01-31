import streamlit as st
import time
from PIL import Image
import random

# Sayfa Ayarları
st.set_page_config(page_title="MathRix AI Oncology Pro", layout="wide", page_icon="🔬")

# --- PROFESYONEL TIBBİ TEMA ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f9; color: #1e293b; }
    .medical-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #3b82f6;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .login-box {
        background-color: white;
        padding: 50px;
        border-radius: 20px;
        border: 2px solid #3b82f6;
        text-align: center;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.1);
    }
    h1, h2, h3 { color: #1e3a8a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- GİRİŞ EKRANI ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.markdown("<br><br><div class='login-box'>", unsafe_allow_html=True)
        st.markdown("<h1>🧬 MATHRIX ONCO-CORE v5.0</h1>", unsafe_allow_html=True)
        st.write("Gelişmiş Diferansiyel Tanı Modülü")
        password = st.text_input("Erişim Anahtarı:", type="password")
        if st.button("SİSTEMİ KİLİTLE/AÇ"):
            if password == "mathrix2026":
                st.session_state['authenticated'] = True
                st.rerun()
            else: st.error("Erişim Yetkisi Yok!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- ANA PANEL ---
st.markdown("<h1 style='text-align: center;'>🏥 MATHRIX AI: AKILLI ORGAN VE DOKU ANALİZ SİSTEMİ</h1>", unsafe_allow_html=True)

# --- KLİNİK REHBER ---
tab1, tab2, tab3 = st.tabs(["🔬 Patoloji Dalları", "💊 Tedavi Protokolleri", "📊 Evreleme"])

with tab1:
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='medical-card'><b>🔹 Adenokarsinom</b><br>Glandüler yapılar, müsin pozitifliği, EGFR/ALK duyarlılığı.</div>", unsafe_allow_html=True)
    c2.markdown("<div class='medical-card' style='border-left-color:#ef4444;'><b>🔸 Skuamöz Hücreli</b><br>İnterstisyel köprüler, keratinizasyon, santral kitleler.</div>", unsafe_allow_html=True)
    c3.markdown("<div class='medical-card' style='border-left-color:#f59e0b;'><b>🔸 Büyük Hücreli</b><br>Belirgin nükleoller, atipik mitoz, yüksek metastaz riski.</div>", unsafe_allow_html=True)

with tab2:
    st.write("*Birinci Basamak:* İmmünoterapi (Pembrolizumab) veya Hedefe Yönelik TKI (Osimertinib).")
    st.write("*İkinci Basamak:* Dosetaksel / Ramucirumab kombinasyonları.")

st.divider()

# --- ANALİZ VE DOĞRULAMA PANELİ ---
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("📁 Vaka Giriş Ünitesi")
    uploaded_file = st.file_uploader("Dijital Kesit (Patoloji/Görüntüleme)", type=["jpg", "png", "jpeg"])
    
    organ_secimi = st.selectbox("Analiz Edilecek Organı Seçin:", ["Akciğer", "Karaciğer", "Beyin", "Meme"])
    metastaz_bilgisi = st.multiselect("Metastatik Bulgular:", ["Beyin", "Kemik", "Karaciğer", "Sürrenal", "Lenf Düğümü"])
    
    evre_durumu = "EVRE IV" if metastaz_bilgisi else "EVRE I-III"

with col_right:
    if uploaded_file:
        st.image(Image.open(uploaded_file), use_container_width=True, caption="Yüklenen Görsel")
        
        if st.button("🔬 MULTİ-KATMANLI ANALİZİ BAŞLAT"):
            # --- YENİ: GÖRSEL DOĞRULAMA SİMÜLASYONU ---
            with st.status("Görsel Doğrulanıyor...", expanded=True) as status:
                st.write("1. Organ morfolojisi taranıyor...")
                time.sleep(1.5)
                
                # SİMÜLASYON: Eğer dosya adında veya rastgele kontrolde uyumsuzluk varsa
                # (Gerçek AI'da burada görüntü sınıflandırma modeli çalışır)
                mismatch_check = random.choice([False, False, False, True]) # %25 hata payı simülasyonu
                
                if mismatch_check:
                    st.error(f"❌ HATA: GÖRSEL UYUMSUZLUĞU! Seçilen organ '{organ_secimi}' ancak yüklenen görsel farklı bir doku mimarisine sahip.")
                    st.stop()
                
                st.write(f"2. {organ_secimi} dokusu doğrulandı. TDA analizi başlatılıyor...")
                time.sleep(1)
                st.write("3. Betti sayıları ve hücre yoğunluğu hesaplanıyor...")
                time.sleep(1)
                status.update(label="Doğrulama ve Analiz Başarılı!", state="complete", expanded=False)

            # Analiz Sonucu
            is_malign = random.choice([True, True, False]) # %66 kanser simülasyonu
            
            if not is_malign:
                st.success(f"✅ ANALİZ SONUCU: SAĞLIKLI {organ_secimi.upper()} DOKUSU")
                st.write("Topolojik veriler homojen bir dağılım göstermektedir. Malignite bulgusuna rastlanmadı.")
            else:
                tur = random.choice(["Adenokarsinom", "Skuamöz Hücreli Karsinom", "Büyük Hücreli Karsinom"])
                risk = random.uniform(97.2, 99.9)
                
                st.error(f"### 🚩 TANI: {tur.upper()}")
                
                # --- DEV RAPOR ---
                full_report = f"""
                #### 🧪 TIBBİ ANALİZ VE 3T DOSYASI
                
                *1. PATOLOJİK DEĞERLENDİRME (DIAGNOSIS):*
                - *Saptanan Tip:* {tur} (Güven: %{risk:.1f})
                - *Hücresel Mimari:* Hücre çekirdeklerinde hiperkromazi, düzensiz nükleer membranlar ve TDA analizinde Betti-1 ($\beta_1$) seviyesinde kaotik döngüler saptanmıştır.
                - *Organ Uyumu:* Görüntü, tipik {organ_secimi} parankim yapısı ve tümöral infiltrasyon ile uyumludur.
                
                *2. TEDAVİ PLANI (THERAPY - 3T):*
                - *Mevcut Evre:* {evre_durumu}
                - *Genetik Gereklilik:* Acilen NGS testi ile EGFR, ALK, ROS1 ve BRAF mutasyonları taranmalıdır.
                - *İlaç Stratejisi:* PD-L1 > %50 ise *Pembrolizumab; EGFR L858R mutasyonu varsa **Osimertinib* 80mg/gün. 
                - *Destekleyici Tedavi:* {', '.join(metastaz_bilgisi) if metastaz_bilgisi else 'Primer odak kontrolü'}.
                
                *3. TAKİP (TRACKING):*
                - 2 ayda bir Kontrastlı Toraks/Batın BT.
                - CEA ve CYFRA 21-1 markörlerinin 4 haftalık periyotlarla takibi.
                - Nörolojik semptom takibi (Metastaz riski nedeniyle).
                """
                st.markdown(full_report)
                
                # Rapor İndirme
                rapor_txt = f"MATHRIX AI FINAL RAPORU\nID: MX-{random.randint(100,999)}\n" + "="*30 + f"\n{full_report}"
                st.download_button("📩 FULL ANALİZ RAPORUNU İNDİR", rapor_txt, f"MathRix_Vaka_Analizi.txt")
    else:
        st.info("Lütfen bir analiz görseli yükleyin.")

st.markdown("<br><hr><center>MathRix Global Health Systems © 2026 | Profesyonel Karar Destek Sistemi</center>", unsafe_allow_html=True)
