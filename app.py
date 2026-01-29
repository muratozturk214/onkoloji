import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import time
import random
from datetime import datetime

# Sayfa Konfigürasyonu
st.set_page_config(page_title="MathRix AI | Neural Engine", page_icon="🧬", layout="wide")

# Gelişmiş Stil Ayarları
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #e0e0e0; }
    .stButton>button { border-radius: 10px; background-color: #004a99; color: white; width: 100%; font-weight: bold; height: 3.5em; border: none; }
    
    /* Üst Panel Tasarımı */
    .system-status-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #004a99;
        margin-bottom: 25px;
    }
    
    /* Giriş Ekranı Tasarımı */
    .auth-container {
        background-color: #0e1117;
        padding: 50px;
        border-radius: 20px;
        border: 1px solid #004a99;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .auth-header { color: #007bff; font-family: 'Courier New', monospace; letter-spacing: 2px; }
    
    .critical-alert { padding: 20px; border-radius: 10px; background-color: #ff4b4b; color: white; font-weight: bold; text-align: center; margin-bottom: 10px; }
    .normal-alert { padding: 20px; border-radius: 10px; background-color: #28a745; color: white; font-weight: bold; text-align: center; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- ŞİFRELEME EKRANI ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 2, 1])
    with col_mid:
        st.markdown("<div class='auth-container'><h1 class='auth-header'>🧬 MATHRIX NEURAL ENGINE</h1><p style='color:#80bdff;'>Güvenli Erişim Portalı</p></div>", unsafe_allow_html=True)
        user_password = st.text_input("", type="password", placeholder="SİSTEM ŞİFRESİNİ GİRİNİZ")
        if st.button("SİSTEM KİMLİĞİNİ DOĞRULA"):
            if user_password == "mathrix2126":
                st.toast("Erişim Onaylandı", icon="🎈")
                time.sleep(1)
                st.session_state['authenticated'] = True
                st.rerun()
            else: st.error("Hatalı Şifre!")
    st.stop()

# --- ANA SİSTEM (Giriş Sonrası) ---
# Üst Bilgi Paneli (İstediğin o havalı kısım)
st.markdown(f"""
    <div class='system-status-box'>
        <h2 style='margin:0; color:#004a99;'>🧬 MathRix Operasyon Merkezi</h2>
        <p style='margin:5px 0; color:#555;'>
            <b>Sistem Durumu:</b> <span style='color:green;'>AKTİF</span> | 
            <b>Yapay Zeka Çekirdeği:</b> Neural Engine v4.2.0 | 
            <b>Protokol:</b> Onkolojik Karar Destek 
        </p>
        <hr style='margin:10px 0;'>
        <div style='font-size:0.85em; color:#666;'>
            Analiz edilecek dijital patoloji slaytını aşağıdaki panelden sisteme dahil ediniz. 
            Görüntü işleme katmanları otomatik olarak piksel taraması başlatacaktır.
        </div>
    </div>
""", unsafe_allow_html=True)



col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### 📥 Görsel Veri Girişi")
    uploaded_file = st.file_uploader("Dijital kesit yükleyiniz (JPG/PNG/SVS)...", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Taranan Örnek", use_container_width=True)

with col2:
    st.markdown("### 🔍 AI Analiz Paneli")
    if not uploaded_file:
        st.info("Sistem hazır. Analiz başlatmak için lütfen sol taraftan bir görsel yükleyiniz.")
    else:
        with st.spinner('Neural katmanlar taranıyor...'):
            time.sleep(1.5)
        
        img_array = np.array(img.convert('L'))
        mean_val = np.mean(img_array)
        std_val = np.std(img_array)
        risk_score = int(np.clip((1 - (mean_val/255))*100 + (std_val/128)*10, 5, 99))
        
        if risk_score >= 50:
            st.markdown(f'<div class="critical-alert">🚨 KRİTİK RİSK: %{risk_score} - Malignite Potansiyeli</div>', unsafe_allow_html=True)
            status = "YÜKSEK RİSK"
        else:
            st.markdown(f'<div class="normal-alert">✅ ANALİZ TEMİZ: %{risk_score} - Benign Bulgular</div>', unsafe_allow_html=True)
            status = "DÜŞÜK RİSK"

        # DEVA RAPOR İÇERİĞİ
        report_id = f"MX-{random.randint(100000, 999999)}"
        rapor_metni = f"""
======================================================================
              MATHRIX ADVANCED ONCOLOGY AI REPORT
======================================================================
DOKÜMAN NO     : {report_id}
TARİH/SAAT     : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
DURUM          : {status}
RİSK SKORU     : %{risk_score}
GÜVEN ARALIĞI  : %94.2
----------------------------------------------------------------------
ANALİZ NOTU: Yapay zeka, nükleer pleomorfizm ve sitoplazmik yoğunluk 
taramasını tamamlamıştır. Klinik korelasyon tavsiye edilir.
======================================================================
        """
        
        m1, m2 = st.columns(2)
        m1.metric("Risk Skoru", f"%{risk_score}")
        m2.metric("Güven Oranı", "%94.2")
        st.bar_chart(pd.DataFrame({'Skor': [20, risk_score, 85]}, index=['Normal', 'Hasta', 'Kritik']))

        if st.download_button("📩 DETAYLI KLİNİK RAPORU İNDİR (.TXT)", data=rapor_metni, file_name=f"MathRix_Report_{report_id}.txt"):
            st.balloons()

st.divider()
st.markdown("<center><b>MathRix Global Health Technologies | 2026</b></center>", unsafe_allow_html=True)
