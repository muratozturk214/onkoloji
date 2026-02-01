import streamlit as st
import time
from PIL import Image, ImageStat
import numpy as np

# --- SİSTEM AYARLARI ---
st.set_page_config(page_title="MathRix Oncology Personalize v4", layout="wide", page_icon="🧬")

# --- ULTRA TIBBİ CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f4f8; }
    .diagnosis-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        color: white; padding: 40px; border-radius: 25px; text-align: center; border: 4px solid #60a5fa;
    }
    .patient-specific-report {
        background: white; padding: 30px; border-radius: 20px;
        border-top: 8px solid #ef4444; margin-top: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .treatment-step {
        background: #f0fdf4; padding: 15px; border-radius: 10px;
        border-left: 5px solid #22c55e; margin-bottom: 10px; color: #166534; font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ŞİFRELEME ---
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if not st.session_state['authenticated']:
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("<div style='background:white; padding:40px; border-radius:20px; border:2px solid #1e40af; text-align:center;'><h2>🧬 MATHRIX ONCO-CORE LOGIN</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Sistem Şifresi:", type="password")
        if st.button("GİRİŞ"):
            if pwd == "mathrix2026":
                st.session_state['authenticated'] = True
                st.rerun()
    st.stop()

# --- ANA PANEL ---
st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>🫁 KİŞİSELLEŞTİRİLMİŞ ONKOLOJİ KARAR DESTEK SİSTEMİ</h1>", unsafe_allow_html=True)

# --- BİLGİ BANKASI (HİÇBİR ŞEY SİLİNMEDİ) ---
with st.expander("📚 Genel Onkoloji ve İlaç Rehberi (Referans Bilgiler)", expanded=False):
    st.write("*Adeno:* EGFR/ALK mutasyonları, Osimertinib. *Skuamöz:* Keratinizasyon, Pembrolizumab. *Büyük Hücreli:* Agresif seyir, Sisplatin.")

st.divider()

# --- GİRİŞ PANELİ: HASTAYA ÖZEL VERİLER ---
col_file, col_patient = st.columns([1, 1])

with col_file:
    st.subheader("📁 1. Patoloji Kesiti")
    file = st.file_uploader("Görüntü Yükle", type=["jpg", "png", "jpeg"])

with col_patient:
    st.subheader("👤 2. Hasta Klinik Durumu")
    metastaz = st.selectbox("Metastaz (Yayılma) Var mı?", ["Yok (Lokalize)", "Beyin Metastazı", "Kemik Metastazı", "Karaciğer/Çoklu Metastaz"])
    sigara = st.radio("Sigara Öyküsü:", ["Hiç İçmemiş", "Eski İçici", "Aktif İçici"])
    yas = st.slider("Hasta Yaşı:", 18, 90, 60)

if st.button("🔬 MULTİ-DİSİPLİNER ANALİZİ BAŞLAT") and file:
    img = Image.open(file).convert("RGB")
    
    # KARAR MEKANİZMASI (RESİM + KLİNİK VERİ BİRLEŞİMİ)
    stat = ImageStat.Stat(img)
    std_val = np.mean(stat.stddev)
    mean_val = np.mean(stat.mean)
    
    # 1. Tanı Belirleme (Resimden)
    if std_val > 52: tani = "SKUAMÖZ HÜCRELİ KARSİNOM"
    elif mean_val < 115: tani = "BÜYÜK HÜCRELİ KARSİNOM"
    else: tani = "ADENOKARSİNOM"
    
    # 2. Rapor Hazırlama (Kişiselleştirilmiş)
    st.markdown(f"<div class='diagnosis-card'><h3>TEŞHİS: {tani}</h3></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='patient-specific-report'>", unsafe_allow_html=True)
    st.subheader(f"📋 Hastaya Özel Klinik Yol Haritası (Yaş: {yas})")
    
    # DURUM 1: METASTAZ VARSA (SİSTEM BUNU AYIRIR)
    if metastaz != "Yok (Lokalize)":
        st.error(f"⚠️ DİKKAT: Hastada {metastaz} saptanmıştır. Bu durum Evre IV (Metastatik) kabul edilir.")
        if "BÜYÜK HÜCRELİ" in tani:
            tedavi = "Agresif Kemoterapi (Sisplatin + Etoposid) + İmmünoterapi kombinasyonu acildir."
            not_detay = "Büyük hücreli karsinomun yüksek bölünme hızı nedeniyle yayılım alanı radyoterapi ile desteklenmelidir."
        elif "ADENOKARSİNOM" in tani:
            tedavi = "Likit Biyopsi ile EGFR/ALK mutasyonu bakılmalı, pozitifse Osimertinib başlanmalıdır."
            not_detay = "Beyin metastazı riski nedeniyle kan-beyin bariyerini geçen akıllı ilaçlar tercih edilmelidir."
        else: # Skuamöz
            tedavi = "Pembrolizumab (İmmünoterapi) ağırlıklı protokol."
            not_detay = "Skuamöz hücrelerde kemik metastazı ağrı yönetimi (Palyatif) önceliklidir."
    
    # DURUM 2: LOKALİZE İSE
    else:
        st.success("✅ Tümör şu an için akciğerde sınırlı görünmektedir (Lokalize).")
        tedavi = "Cerrahi Rezeksiyon (Lobektomi) + Adjuvan Kemoterapi."
        not_detay = "Erken evre yakalandığı için kür (tam iyileşme) şansı yüksektir."

    # RAPORU EKRANA BASMA
    st.markdown(f"*Önerilen Tedavi Protokolü:* {tedavi}")
    st.markdown(f"*Klinik Gerekçe:* {not_detay}")
    
    st.markdown("<h4>📍 Uygulama Adımları:</h4>", unsafe_allow_html=True)
    st.markdown(f"<div class='treatment-step'>1. {tani} morfolojisi için moleküler panel (NGS) onayı al.</div>", unsafe_allow_html=True)
    if metastaz != "Yok (Lokalize)":
        st.markdown(f"<div class='treatment-step'>2. {metastaz} bölgesi için radyoserrahi (Gamma Knife/CyberKnife) konsültasyonu iste.</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='treatment-step'>2. Toraks cerrahisi ile operabilite değerlendirmesi yap.</div>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='treatment-step'>3. Hasta yaşı ({yas}) ve genel kondisyonuna göre doz ayarı yapılmış kemoterapi planla.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.image(img, caption="Analiz Edilen Hasta Kesiti", use_container_width=True)
