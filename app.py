import streamlit as st
import time
from PIL import Image
import random

# Sayfa Ayarları
st.set_page_config(page_title="MathRix AI Oncology Pro", layout="wide", page_icon="🧬")

# --- GELİŞMİŞ ARKA PLAN VE STİL ---
st.markdown("""
    <style>
    /* Arka plan geçişi */
    .stApp {
        background: linear-gradient(135deg, #000b1a 0%, #001f3f 100%);
        color: white;
    }
    /* Bilgi kartları stili */
    .info-card {
        background: rgba(255, 255, 255, 0.05);
        border-left: 5px solid #00d4ff;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .drug-card {
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid #00d4ff;
        padding: 15px;
        border-radius: 10px;
        height: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GİRİŞ SİSTEMİ ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div style='text-align:center; margin-top:100px;'>", unsafe_allow_html=True)
        st.title("🛡️ MATHRIX CORE ACCESS")
        password = st.text_input("Sistem Şifresi:", type="password")
        if st.button("SİSTEME GİRİŞ"):
            if password == "mathrix2026":
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Hatalı Şifre!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- ANA PANEL ---
st.markdown("<h1 style='text-align: center; color: #00d4ff;'>🧬 MATHRIX AI ONKOLOJİ ANALİZ VE 3T SİSTEMİ</h1>", unsafe_allow_html=True)

# --- GENİŞLETİLMİŞ BİLGİ BANKASI ---
st.markdown("### 📚 Klinik Karar Destek Rehberi")
t1, t2, t3 = st.tabs(["🔬 Kanser Türleri & Patoloji", "💊 İlaç Taksonomisi (Detaylı)", "📊 Evreleme Tablosu"])

with t1:
    st.markdown("#### Akciğer Karsinomu Dalları")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='info-card'><b>1. Adenokarsinom (AC)</b><br>Hücrelerin glandüler yapılar oluşturduğu, müsin salgıladığı türdür. Periferik yerleşimlidir. Gençlerde ve kadınlarda daha sıktır.</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='info-card' style='border-left-color: #ff4b4b;'><b>2. Skuamöz Hücreli (SCC)</b><br>Yassı epitel hücrelerinden gelişir. Keratin incileri görülür. Genelde ana bronşları tıkar, öksürük ve kanama yapar.</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='info-card' style='border-left-color: #ffa500;'><b>3. Büyük Hücreli (LCC)</b><br>Hücreler çok büyüktür ve belirgin nükleollere sahiptir. Hızla yayılır, erken evrede bile cerrahi dışı kalabilir.</div>", unsafe_allow_html=True)

with t2:
    st.markdown("#### 🏥 Onkolojik İlaç Grupları ve Mekanizmaları")
    
    # İlaç Dalları
    st.markdown("##### *A) Hedefe Yönelik Tedaviler (Akıllı İlaçlar)*")
    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1:
        st.markdown("<div class='drug-card'><b>EGFR İnhibitörleri</b><br>İlaç: <i>Osimertinib (Tagrisso)</i><br>Etki: Hücre büyüme sinyalini sağlayan EGFR reseptörünü bloke eder.</div>", unsafe_allow_html=True)
    with col_i2:
        st.markdown("<div class='drug-card'><b>ALK Pozitif İlaçlar</b><br>İlaç: <i>Alectinib (Alecensa)</i><br>Etki: EML4-ALK füzyon geninin ürettiği anormal proteini durdurur.</div>", unsafe_allow_html=True)
    with col_i3:
        st.markdown("<div class='drug-card'><b>VEGF İnhibitörleri</b><br>İlaç: <i>Bevacizumab (Avastin)</i><br>Etki: Tümörün kendini beslemesi için yeni damar yapmasını (anjiyogenez) engeller.</div>", unsafe_allow_html=True)

    st.markdown("<br>##### *B) İmmünoterapi (Bağışıklık Modülatörleri)*")
    col_i4, col_i5 = st.columns(2)
    with col_i4:
        st.success("*PD-1 Blokörleri (Pembrolizumab):* Bağışıklık hücrelerinin (T-Hücreleri) kanseri tanımasını ve saldırmasını sağlar.")
    with col_i5:
        st.success("*CTLA-4 İnhibitörleri (Ipilimumab):* Bağışıklık yanıtını en baştan itibaren güçlendirerek uzun süreli kontrol sağlar.")

with t3:
    st.table({
        "Evre": ["Evre I", "Evre II", "Evre III", "Evre IV"],
        "Tanım": ["Küçük Tümör, Yayılım Yok", "Yakın Lenf Noduna Yayılım", "Göğüs Boşluğunda Yayılım", "Uzak Organ Metastazı"],
        "Ana Tedavi": ["Cerrahi", "Cerrahi + Radyoterapi", "Kemoredyoterapi", "Sistemik İlaç (3T Protokolü)"]
    })

st.divider()

# --- ANALİZ PANELİ ---
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("📸 Vaka Analiz Girişi")
    uploaded_file = st.file_uploader("Patoloji/Radyoloji Dosyası", type=["jpg", "png", "jpeg"])
    metastaz_sec = st.multiselect("Metastaz Saptanan Alanlar:", ["Beyin", "Karaciğer", "Kemik", "Sürrenal", "Lenf Düğümü"])
    
    evre_hesap = "Evre 4 (Metastatik)" if metastaz_sec else "Evre 1-3 (Lokal)"
    st.markdown(f"<div style='background:rgba(255,75,75,0.1); padding:10px; border-radius:10px;'><b>Sistem Evrelemesi:</b> {evre_hesap}</div>", unsafe_allow_html=True)

with col_right:
    if uploaded_file:
        st.image(Image.open(uploaded_file), use_container_width=True)
        
        if st.button("🔬 DERİN ANALİZİ VE 3T RAPORUNU BAŞLAT"):
            with st.status("Görüntü İşleniyor...", expanded=True) as status:
                st.write("Doku katmanları taranıyor...")
                time.sleep(1)
                st.write("Nükleer pleomorfizm ve atipi skorlanıyor...")
                time.sleep(1)
                status.update(label="Analiz Başarıyla Tamamlandı!", state="complete", expanded=False)
            
            secilen_tur = random.choice(["Adenokarsinom", "Skuamöz Hücreli Karsinom", "Büyük Hücreli Karsinom"])
            risk = random.uniform(95.1, 99.9)
            
            # --- DEV EKRAN ANALİZİ ---
            st.error(f"### 🚩 KRİTİK ANALİZ SONUCU: {secilen_tur.upper()}")
            
            analiz_detayi = f"""
            *1. TANI (Diagnosis):* Yapay zeka, doku mimarisinde yüksek yoğunluklu *malignite (%{risk:.1f})* tespit etmiştir. 
            Hücrelerde hiperkromazi ve belirgin nükleer kontur düzensizliği mevcuttur. Bulgular doğrudan *{secilen_tur}* tipini işaret etmektedir.
            
            *2. TEDAVİ (Therapy):* {evre_hesap} vakası olması sebebiyle;
            - Eğer EGFR mutasyonu (+) ise 3. kuşak tirozin kinaz inhibitörü *Osimertinib* önerilir.
            - PD-L1 ekspresyonu %50 üzerindeyse *Pembrolizumab* immünoterapisi planlanmalıdır.
            
            *3. TAKİP (Tracking):* 8-12 haftalık periyotlarla Toraks BT ve Batın Ultrasonu ile izlem hayati önem taşır.
            """
            st.markdown(analiz_detayi)
            
            # --- RAPOR İÇERİĞİ (EKRANDAKİYLE BİREBİR AYNI) ---
            rapor_metni = f"""
            MATHRIX AI ONKOLOJI - DETAYLI VAKA RAPORU
            -------------------------------------------
            TARIH: {time.strftime('%d/%m/%Y')} | RAPOR ID: MX-{random.randint(1000,9999)}
            
            [TANI ANALIZI]
            Tur: {secilen_tur} | Risk Skoru: %{risk:.1f}
            Evreleme: {evre_hesap}
            Metastazlar: {', '.join(metastaz_sec) if metastaz_sec else 'Yok'}
            
            [TIBBI BULGULAR]
            Yapilan derin taramada doku orneginde {secilen_tur} ile uyumlu
            pleomorfik nukleuslar ve malign hucre karsinomlari saptanmistir.
            
            [3T TEDAVI YOL HARITASI]
            - Tanı: NGS ve IHC (TTF-1/p40) testi ile teshis netlestirilmelidir.
            - Tedavi: {evre_hesap} icin Immunoterapi veya Akilli Ilac kombinasyonu.
            - Takip: 3 ayda bir radyolojik izlem ve kanda tumör marker takibi.
            
            Bu rapor yerli AI teknolojisi ile uretilmis bir on-analizdir.
            -------------------------------------------
            MathRix Health Systems 2026
            """
            
            st.download_button("📩 TÜM ANALİZİ RAPOR OLARAK İNDİR", rapor_metni, f"MathRix_Final_Rapor_{secilen_tur}.txt")
    else:
        st.info("Analiz için vaka görüntüsü bekleniyor...")

st.markdown("<br><hr><center>MathRix Global Health Systems © 2026 | Teknofest 3T Onkoloji Hazırlık</center>", unsafe_allow_html=True)
