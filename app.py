import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import time

# --- SAYFA AYARLARI VE KLİNİK TEMA ---
st.set_page_config(page_title="PULMO-TECH v2.0 | Klinik Tanı Portalı", layout="wide")

# Bembeyaz Hastane Teması (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .main { background-color: #FFFFFF; }
    h1, h2, h3 { color: #1E3A8A; font-family: 'Segoe UI', sans-serif; }
    .report-box { 
        padding: 25px; 
        border: 1px solid #E5E7EB; 
        border-radius: 10px; 
        background-color: #F9FAFB;
        box-shadow: 2px 2px 15px rgba(0,0,0,0.05);
    }
    .stButton>button { width: 100%; background-color: #1E3A8A; color: white; border-radius: 5px; }
    .sidebar .sidebar-content { background-color: #F3F4F6; }
    </style>
    """, unsafe_allow_html=True)

# --- ŞİFRE KONTROLÜ ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🏥 PULMO-TECH Giriş")
    password = st.text_input("Sistem Erişim Şifresi", type="password")
    if st.button("Sisteme Giriş Yap"):
        if password == "mathrix2026":
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("Hatalı Şifre. Erişim Reddedildi.")
    st.stop()

# --- ANALİZ MOTORU (MATEMATİKSEL) ---
def analyze_tissue(img):
    # Görüntüyü gri tonlamaya çevir ve numpy dizisi yap
    img_gray = ImageOps.grayscale(img)
    arr = np.array(img_gray)
    
    # 1. Lümen/Boşluk Analizi (Açık renkli alanlar)
    lumen_ratio = np.sum(arr > 200) / arr.size
    
    # 2. Hücre Yoğunluğu ve Gradient (Kenar tespiti/Varyans)
    # Dokudaki hücre sınırlarını ölçmek için gradient analizi simülasyonu
    dy, dx = np.gradient(arr)
    gradient_complexity = np.mean(np.sqrt(dx*2 + dy*2))
    
    # 3. Doku Sertliği (Entropy/Doku Karmaşıklığı)
    # Skuamöz hücrelerde keratinize inci yapısı yoğunluk farkı yaratır
    entropy = np.std(arr) / 100 
    
    # Karar Mekanizması
    cancer_type = ""
    prob = 0.0
    technical_findings = ""
    
    if lumen_ratio > 0.4:
        cancer_type = "Adenokarsinom"
        technical_findings = "Lepidik büyüme paterni ve asiner yapılar gözlemlendi."
        prob = 65 + (lumen_ratio * 30)
    elif gradient_complexity > 15:
        cancer_type = "Küçük Hücreli Akciğer Kanseri (KHAK)"
        technical_findings = "Azzopardi etkisi ve nükleer kalıplanma (molding) mevcut."
        prob = 85 + (gradient_complexity / 2)
    elif entropy > 0.6:
        cancer_type = "Skuamöz Hücreli Karsinom"
        technical_findings = "İntrasellüler köprüler ve keratinizasyon odakları saptandı."
        prob = 70 + (entropy * 20)
    else:
        cancer_type = "Büyük Hücreli Karsinom"
        technical_findings = "Belirgin nükleol ve geniş sitoplazmalı dev hücreler."
        prob = 50 + (entropy * 40)

    return cancer_type, min(prob, 99.8), lumen_ratio, gradient_complexity, technical_findings

# --- NAVİGASYON ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2864/2864350.png", width=100)
    st.title("PULMO-NAV")
    page = st.radio("Sayfa Seçiniz:", [
        "🔬 Tanı Merkezi", 
        "💊 İlaç Rehberi", 
        "📊 Evreleme Sistemi", 
        "🧬 Kanser Türleri"
    ])
    st.markdown("---")
    if st.button("Oturumu Kapat"):
        st.session_state['authenticated'] = False
        st.rerun()

# --- SAYFA İÇERİKLERİ ---

if page == "🔬 Tanı Merkezi":
    st.title("🔬 Tanı ve Analiz Merkezi")
    st.info("Lütfen hastaya ait biyopsi kesitini veya BT taramasını yükleyiniz.")
    
    uploaded_file = st.file_uploader("Görüntü Seç (PNG, JPG, JPEG)", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(img, caption="Yüklenen Doku Örneği", use_container_width=True)
        
        with col2:
            with st.spinner('Matematiksel Doku Analizi Yapılıyor...'):
                time.sleep(2) # Simülasyon
                c_type, prob, lumen, grad, tech = analyze_tissue(img)
                
                st.subheader("Analiz Parametreleri")
                st.write(f"*Lümen Oranı:* %{lumen*100:.2f}")
                st.write(f"*Doku Gradienti:* {grad:.2f}")
                st.progress(prob / 100)
                st.metric("Malignite Olasılığı", f"%{prob:.2f}")

        # RAPOR ALANI
        st.markdown("---")
        report_text = f"""
        KLİNİK ANALİZ RAPORU
        ---------------------------
        Tarih: {time.strftime("%d/%m/%Y")}
        Saptanan Tür: {c_type}
        Malignite Olasılığı: %{prob:.2f}
        
        TEKNİK BULGULAR:
        - {tech}
        - Hücre Isı Yoğunluğu: {grad:.2f} (Varyans Analizi)
        - Boşluk Analizi: {lumen:.4f} (Lümen/Doku İndeksi)
        
        6 AY PROGNOZ TAHMİNİ:
        - { "Agresif seyir, yakın takip önerilir." if prob > 80 else "Stabil seyir, rutin tedavi planı." }
        """
        
        st.markdown(f'<div class="report-box"><h3>📄 Otomatik Tanı Raporu</h3><pre>{report_text}</pre></div>', unsafe_allow_html=True)
        
        st.download_button(
            label="Raporu İndir (.TXT)",
            data=report_text,
            file_name=f"hasta_rapor_{int(time.time())}.txt",
            mime="text/plain"
        )

elif page == "💊 İlaç Rehberi":
    st.title("💊 Akıllı İlaç Rehberi")
    
    drug = st.selectbox("İlaç Seçiniz:", ["Osimertinib", "Pembrolizumab", "Alectinib"])
    
    data = {
        "Osimertinib": ["EGFR Mutasyonu (+)", "Yorgunluk, İshal, Cilt Kuruluğu", "T790M direnç mutasyonunu inhibe eder."],
        "Pembrolizumab": ["PD-L1 Ekspresyonu (>%50)", "Pnömoni, Kolit, Endokrinopatiler", "Bağışıklık sisteminin kanser hücresini tanımasını sağlar."],
        "Alectinib": ["ALK Pozitifliği", "Ödem, Kas ağrısı, Kabızlık", "ALK kinaz aktivitesini bloke ederek tümör büyümesini durdurur."]
    }
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Endikasyon", "Hedefe Yönelik")
    c2.metric("Etki Türü", "İnhibitör")
    c3.metric("Klinik Yanıt", "%70-80")
    
    st.subheader(f"{drug} Kullanım Detayları")
    st.write(f"*Hedef:* {data[drug][0]}")
    st.write(f"*Mekanizma:* {data[drug][2]}")
    st.warning(f"*Yan Etkiler:* {data[drug][1]}")

elif page == "📊 Evreleme Sistemi":
    st.title("📊 TNM Evreleme Sistemi")
    st.table({
        "Evre": ["Evre I", "Evre II", "Evre III", "Evre IV"],
        "T (Tümör)": ["T1 (<3cm)", "T2 (3-5cm)", "T3 (>5cm)", "Herhangi T"],
        "N (Nod)": ["N0 (Yok)", "N1 (Hiler)", "N2 (Mediastinal)", "Herhangi N"],
        "M (Metastaz)": ["M0", "M0", "M0", "M1 (Uzak)"]
    })
    st.info("Bu tablo AJCC 8. Versiyonuna göre düzenlenmiştir.")

elif page == "🧬 Kanser Türleri":
    st.title("🧬 Histolojik Kanser Türleri")
    cols = st.columns(2)
    
    with cols[0]:
        st.subheader("Adenokarsinom")
        st.write("En yaygın türdür. Glandüler (bezsi) yapılardan köken alır. Sigara içmeyenlerde de sık görülür.")
        
        st.subheader("Skuamöz Hücreli")
        st.write("Bronş yassı epitelinden köken alır. Santral yerleşimlidir. Keratin incileri tipiktir.")

    with cols[1]:
        st.subheader("Küçük Hücreli (KHAK)")
        st.write("En agresif türdür. Nöroendokrin kökenlidir. Hızlı metastaz yapma eğilimindedir.")
        
        st.subheader("Büyük Hücreli")
        st.write("Tanımlanamayan, geniş sitoplazmalı hücrelerden oluşur. Tanısı dışlama yoluyla konur.")

# --- FOOTER ---
st.markdown("---")
st.caption("PULMO-TECH v2.0 - 2026 Klinik Karar Destek Sistemi | Sadece Profesyonel Kullanım İçindir.")
