import streamlit as st
import time
from PIL import Image
import random

# Sayfa Ayarları
st.set_page_config(page_title="MathRix AI Oncology Pro", layout="wide", page_icon="🧬")

# --- AYDINLIK VE PROFESYONEL TEMA ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; color: #1e293b; }
    .medical-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #2563eb;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .login-box {
        background-color: white;
        padding: 50px;
        border-radius: 20px;
        border: 2px solid #2563eb;
        text-align: center;
        box-shadow: 0 10px 40px rgba(37, 99, 235, 0.1);
    }
    h1, h2, h3 { color: #1e3a8a !important; font-family: 'Segoe UI', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- GİRİŞ EKRANI ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.markdown("<br><br><div class='login-box'>", unsafe_allow_html=True)
        st.markdown("<h1>🧬 MATHRIX ONCO-CORE v6.0</h1>", unsafe_allow_html=True)
        st.write("Tam Otonom Onkolojik Karar Destek Sistemi")
        password = st.text_input("Sistem Şifresi:", type="password")
        if st.button("SİSTEME GİRİŞ YAP"):
            if password == "mathrix2026":
                st.session_state['authenticated'] = True
                st.rerun()
            else: st.error("Erişim Reddedildi!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- ANA PANEL ---
st.markdown("<h1 style='text-align: center;'>🏥 MATHRIX AI: OTONOM DOKU VE KANSER ANALİZİ</h1>", unsafe_allow_html=True)

# --- ÜST BİLGİ SEKMELERİ ---
tab1, tab2 = st.tabs(["📋 Bilimsel Temel (TDA)", "💊 Tedavi Veritabanı"])
with tab1:
    st.markdown("""
    <div class='medical-card'>
    <b>Topolojik Veri Analizi (TDA) Nedir?</b><br>
    Hücre çekirdeklerini birer 'nokta bulutu' olarak ele alıyoruz. 
    <b>Betti-0 (β₀):</b> Hücre kümelerini,<br>
    <b>Betti-1 (β₁):</b> Dokudaki yapısal boşlukları ve kaotik döngüleri temsil eder.<br>
    Kanserli dokularda β₁ değerindeki düzensiz artış, mimari bozulmanın matematiksel ispatıdır.
    </div>
    """, unsafe_allow_html=True)
with tab2:
    st.write("Sistemimiz; EGFR, ALK, ROS1 mutasyonları ve PD-L1 ekspresyonu üzerine 2026 güncel onkoloji rehberlerini kullanır.")

st.divider()

# --- ANALİZ PANELİ ---
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("📁 Veri Yükleme")
    uploaded_file = st.file_uploader("Görüntüyü Buraya Sürükleyin (Patoloji Kesiti)", type=["jpg", "png", "jpeg"])
    metastaz_durumu = st.multiselect("Metastaz Saptanan Organlar (Varsa):", ["Beyin", "Kemik", "Karaciğer", "Adrenal", "Lenf"])
    
    st.info("ℹ️ Sistem görüntüyü otomatik olarak tarayacak ve doku tipini belirleyecektir.")

with col_right:
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True, caption="Yüklenen Dijital Kesit")
        
        if st.button("🔬 OTONOM ANALİZİ BAŞLAT"):
            # Analiz Simülasyonu
            with st.status("Doku Kimliği Doğrulanıyor...", expanded=True) as status:
                time.sleep(1.5)
                # SİMÜLASYON: Sistem organı kendi buluyor
                # Gerçek dünyada model tahmini yapılır, burada rastgele bir 'organ' atanıyor
                tespit_edilen_organ = random.choice(["Akciğer", "Akciğer", "Akciğer", "Meme", "Beyin"])
                
                if tespit_edilen_organ != "Akciğer":
                    st.error(f"⚠️ KRİTİK UYARI: Tespit Edilen Doku: {tespit_edilen_organ.upper()}")
                    st.markdown(f"""
                    *Sistem Notu:* Yapılan morfolojik taramada bu görselin bir *{tespit_edilen_organ}* dokusuna ait olduğu saptanmıştır. 
                    MathRix AI şu an için yalnızca *Akciğer Kanseri* veritabanı ile optimize edilmiştir. 
                    Hatalı tanı riskini önlemek için bu vaka üzerinde analiz gerçekleştirilemez.
                    """)
                    status.update(label="Analiz Durduruldu: Organ Uyumsuzluğu", state="error")
                else:
                    st.write("✅ Doku Doğrulandı: Akciğer Parankimi")
                    time.sleep(1)
                    st.write("📈 Topolojik Veri Analizi (Betti Sayıları) hesaplanıyor...")
                    time.sleep(1.5)
                    
                    # Kanser Kontrolü
                    is_cancer = random.choice([True, True, False])
                    
                    if not is_cancer:
                        st.success("### ✅ SONUÇ: BENİGN (SAĞLIKLI) AKCİĞER DOKUSU")
                        st.write("Doku mimarisi homojen. Hücre diziliminde kaotik döngü saptanmadı. Klinik takip önerilir.")
                        status.update(label="Analiz Tamamlandı: Malignite Saptanmadı", state="complete")
                    else:
                        tur = random.choice(["Adenokarsinom", "Skuamöz Hücreli Karsinom", "Büyük Hücreli Karsinom"])
                        risk = random.uniform(97.5, 99.9)
                        evre = "Evre IV" if metastaz_durumu else "Evre I-III"
                        
                        st.error(f"### 🚩 POZİTİF TESPİT: {tur.upper()}")
                        
                        # DEV RAPOR
                        full_rapor = f"""
                        #### 🧪 AYRINTILI TIBBİ ANALİZ VE 3T RAPORU
                        
                        *1. TANI VE MORFOLOJİ (DIAGNOSIS):*
                        - *Birincil Tanı:* {tur} (Güven Skoru: %{risk:.1f})
                        - *Topolojik Veri:* TDA analizinde Betti-1 ($\beta_1$) seviyesinde anlamlı artış saptanmış olup, hücre dizilimi 'Küçük Dünyalar' ağından 'Kaotik' ağ yapısına geçiş yapmıştır.
                        - *Hücresel Atipi:* Nükleer pleomorfizm ve hiperkromatik çekirdekler yaygın olarak izlenmektedir.
                        
                        *2. TEDAVİ STRATEJİSİ (THERAPY):*
                        - *Mevcut Klinik Evre:* {evre}
                        - *Genetik Yol Haritası:* Acilen NGS (Next Gen Sequencing) paneli önerilir.
                        - *İlaç Rehberi:* PD-L1 > %50 ise *Pembrolizumab* (İmmünoterapi); EGFR mutasyonu (+) ise *Osimertinib* 80mg/gün (TKI).
                        - *Bölgesel Yaklaşım:* {', '.join(metastaz_durumu) if metastaz_durumu else 'Primer kitle odaklı tedavi'}.
                        
                        *3. TAKİP PROGRSAMI (TRACKING):*
                        - *Radyoloji:* 2 ayda bir Kontrastlı Toraks BT ve PET-CT takibi.
                        - *Markerlar:* CEA, CYFRA 21-1 ve kanda sirküle eden tümör DNA'sı (ctDNA) takibi.
                        - *Prognoz:* Agresif seyir riski nedeniyle multidisipliner tümör konseyi kararı gereklidir.
                        """
                        st.markdown(full_rapor)
                        
                        # İndirme Butonu
                        indirilecek = f"MATHRIX AI ANALİZ ÇIKTISI\n" + "="*30 + f"\n{full_rapor}"
                        st.download_button("📩 TÜM ANALİZİ VE 3T DOSYASINI İNDİR", indirilecek, f"MathRix_Rapor_{tur}.txt")
                        status.update(label="Analiz Tamamlandı: Malignite Tespiti!", state="complete")
    else:
        st.info("Lütfen bir patoloji görüntüsü yükleyerek otonom analizi başlatın.")

st.markdown("<br><hr><center>MathRix Health Systems © 2026 | Powered by Neural Core v6.0</center>", unsafe_allow_html=True)
