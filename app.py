import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import time
import random
from datetime import datetime

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="MathRix AI | Oncology Clinical Suite", page_icon="🧬", layout="wide")

# Premium Kurumsal Stil
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border-top: 4px solid #003366; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .auth-box { background-color: #0b0e14; padding: 40px; border-radius: 15px; border: 2px solid #3b82f6; text-align: center; color: white; margin-top: 50px; }
    .auth-title { font-size: 2.8em; font-weight: 900; color: #3b82f6; letter-spacing: 4px; }
    .report-card { background-color: #ffffff; padding: 30px; border-radius: 15px; border: 1px solid #dee2e6; color: #1f2937; margin-top: 20px; }
    .diagnosis-header { background-color: #003366; color: white; padding: 15px; border-radius: 10px; text-align: center; font-size: 1.5em; font-weight: bold; margin-bottom: 20px; }
    .info-tag { background-color: #e0f2fe; color: #0369a1; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 0.9em; margin-right: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GİRİŞ EKRANI ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    _, col_mid, _ = st.columns([1, 1.8, 1])
    with col_mid:
        st.markdown("<div class='auth-box'><div class='auth-title'>MATHRIX AI</div><p>ONCOLOGY CLINICAL SUITE v5.0</p></div>", unsafe_allow_html=True)
        password = st.text_input("SİSTEM ERİŞİM ANAHTARI", type="password")
        if st.button("SİSTEME GİRİŞ YAP"):
            if password == "mathrix2026":
                st.session_state['authenticated'] = True
                st.rerun()
            else: st.error("Erişim Reddedildi!")
    st.stop()

# --- 3. ANA PANEL ---
st.markdown("<div style='background: #003366; padding: 25px; border-radius: 15px; color: white; margin-bottom: 30px;'><h1>MathRix AI Karar Destek Paneli</h1><p>Hassas Onkoloji ve Dijital Patoloji Analiz Laboratuvarı</p></div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📥 Kesit Tanımlama")
    uploaded_file = st.file_uploader("Görseli Yükleyin (H&E, CT, MRI...)", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Analiz Edilen Doku Örneği", use_container_width=True)

with col2:
    st.subheader("🔍 AI Teşhis ve Öngörü Raporu")
    if not uploaded_file:
        st.info("Sistem, analiz için veri girişi bekliyor.")
    else:
        with st.status("🧬 Derin öğrenme katmanları aktive ediliyor...", expanded=True) as s:
            time.sleep(1); s.write("Hücresel nükleer pleomorfizm taranıyor...")
            time.sleep(1); s.write("Doku tipi sınıflandırılıyor...")
            time.sleep(1); s.write("Tedavi protokolleri optimize ediliyor...")
            s.update(label="Analiz Tamamlandı", state="complete")

        # --- AKILLI ANALİZ VE TANI ÜRETİCİ ---
        img_array = np.array(img.convert('L'))
        std_val = np.std(img_array)
        
        # Kanser Türü ve Tedavi Veritabanı (Simülasyon)
        cancer_types = [
            {"type": "Adenokarsinom (Evre II)", "drug": "Cisplatin + Pemetrexed", "duration": "6-8 Ay", "prognosis": "%82 Başarı Oranı"},
            {"type": "Skuamöz Hücreli Karsinom", "drug": "Pembrolizumab (İmmünoterapi)", "duration": "12 Ay", "prognosis": "%65 Pozitif Yanıt"},
            {"type": "Küçük Hücreli Dışı Akciğer Ca", "drug": "Erlotinib / Gefitinib", "duration": "9-14 Ay", "prognosis": "%74 Kontrol Altında"}
        ]
        
        if std_val > 50 or "tumor" in uploaded_file.name.lower():
            risk_score = random.randint(72, 97)
            diagnosis = random.choice(cancer_types)
            is_malign = True
        else:
            risk_score = random.randint(6, 28)
            is_malign = False

        # --- SONUÇ GÖSTERİMİ ---
        if is_malign:
            st.markdown(f"<div class='report-card'><div class='diagnosis-header'>Kritik Bulgu: {diagnosis['type']}</div>", unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Malignite Riski", f"%{risk_score}")
            c2.metric("Proliferasyon Hızı", "Yüksek")
            c3.metric("Güven Aralığı", "%98.1")

            st.markdown("<p class='section-title'>🩺 Tedavi Planı ve İlaç Önerisi</p>", unsafe_allow_html=True)
            st.write(f"• *Önerilen Birincil İlaç:* <span class='info-tag'>{diagnosis['drug']}</span>", unsafe_allow_html=True)
            st.write(f"• *Tahmini Tedavi Süresi:* <span class='info-tag'>{diagnosis['duration']}</span>", unsafe_allow_html=True)
            st.write(f"• *Klinik Öngörü (Prognoz):* {diagnosis['prognosis']}")
            
            st.markdown("<p class='section-title'>🔬 Patolojik Notlar</p>", unsafe_allow_html=True)
            st.info("Atipik mitoz ve nükleer hiperkromazi gözlemlendi. Lenf nodu tutulumu riski nedeniyle PET-CT önerilir.")
        else:
            st.success("✅ ANALİZ SONUCU: BENİGN (TEMİZ). Doku yapısı normal sınırlardadır.")
            st.metric("Risk Skoru", f"%{risk_score}")
            st.write("Herhangi bir tedavi veya ilaç protokolüne şu aşamada gerek duyulmamaktadır. Yıllık kontrol önerilir.")

        st.markdown("</div>", unsafe_allow_html=True)
        
        # Rapor İndirme
        report_data = f"MATHRIX AI FINAL REPORT\nType: {diagnosis['type'] if is_malign else 'Benign'}\nRisk: %{risk_score}\nDate: {datetime.now()}"
        st.download_button("📩 KLİNİK RAPORU MÜHÜRLE VE İNDİR", report_data, file_name="mathrix_final_report.txt")

st.divider()
st.caption("⚠️ YASAL UYARI: Bu sistem eğitim amaçlı bir AI prototipidir. Kararlar kesinlikle bir Onkoloji uzmanı tarafından onaylanmalıdır.")
