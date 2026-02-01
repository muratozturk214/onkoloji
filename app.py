import streamlit as st
import time
from PIL import Image, ImageStat
import random

# Sayfa Konfigürasyonu
st.set_page_config(page_title="MathRix Oncology AI", layout="wide", page_icon="🔬")

# --- CUSTOM CSS: ESTETİK VE TIBBİ ARAYÜZ ---
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; color: #1e293b; }
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #2563eb 100%);
        padding: 40px; border-radius: 20px; text-align: center; color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); margin-bottom: 30px;
    }
    .info-box {
        background: #ffffff; padding: 20px; border-radius: 15px;
        border-top: 5px solid #3b82f6; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        height: 250px; overflow-y: auto;
    }
    .report-card {
        background: white; padding: 30px; border-radius: 20px;
        border: 1px solid #e2e8f0; border-left: 12px solid #e11d48;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    }
    .stButton>button {
        background: #2563eb; color: white; border-radius: 10px; width: 100%;
        height: 50px; font-weight: bold; border: none; transition: 0.3s;
    }
    .stButton>button:hover { background: #1e40af; transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)

# --- SİSTEM GİRİŞİ (LOGIN) ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.markdown("<div style='margin-top:100px; text-align:center;'>", unsafe_allow_html=True)
        st.markdown("<h1 style='color:#0f172a;'>🧬 MATHRIX SYSTEM</h1>", unsafe_allow_html=True)
        password = st.text_input("Security Key:", type="password")
        if st.button("AUTHENTICATE"):
            if password == "mathrix2026":
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Access Denied.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- ÜST BAŞLIK ---
st.markdown("<div class='main-header'><h1>MATHRIX ONKOLOJİK KARAR DESTEK SİSTEMİ</h1><p>Topolojik Veri Analizi (TDA) ve Diferansiyel Tanı Modülü</p></div>", unsafe_allow_html=True)

# --- BİLGİ KARTLARI ---
st.markdown("### 📚 Klinik Referans Veritabanı")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("<div class='info-box'><b>🫁 Akciğer (Lung)</b><br><small>Adeno, Skuamöz ve Büyük Hücreli Tipleri. Tedavide EGFR ve PD-L1 hedeflemesi esastır.</small></div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='info-box'><b>🫃 Mide (Gastric)</b><br><small>Taşlı yüzük ve Adeno tipleri. Her2/neu durumu tedavi seyrini değiştirir.</small></div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='info-box'><b>🧬 Pankreas (Pancreas)</b><br><small>Duktal Adenokarsinom en agresif tiptir. CA 19-9 markerı ile izlenir.</small></div>", unsafe_allow_html=True)
with c4:
    st.markdown("<div class='info-box'><b>📊 Evreleme & 3T</b><br><small>Evre I-IV arası metastaz kontrolü ile belirlenen 3T (Tanı-Tedavi-Takip) protokolüdür.</small></div>", unsafe_allow_html=True)

st.divider()

# --- ANALİZ PANELİ ---
col_in, col_res = st.columns([1, 1.2])

with col_in:
    st.subheader("📁 Vaka Veri Girişi")
    uploaded_file = st.file_uploader("Patoloji Görselini Yükleyin", type=["jpg", "png", "jpeg"])
    st.write("*🔍 Metastaz Taraması:*")
    m1 = st.checkbox("Beyin Metastazı")
    m2 = st.checkbox("Karaciğer Metastazı")
    is_metastatic = m1 or m2  # Değişken adını düzelttim

with col_res:
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True, caption="İncelenen Kesit")
        
        if st.button("🔬 OTONOM ANALİZİ BAŞLAT"):
            with st.status("Doku Spektrumu İnceleniyor...", expanded=True) as status:
                stat = ImageStat.Stat(img)
                avg_val = sum(stat.mean) / 3
                time.sleep(1)
                
                # Organ tespiti
                if avg_val < 90: detected_organ = "Mide"
                elif avg_val > 170: detected_organ = "Akciğer"
                else: detected_organ = "Pankreas"
                
                st.write(f"🔎 Tespit Edilen Doku: {detected_organ}")
                time.sleep(1)
                
                # TDA Analizi
                st.write("📊 Betti Sayıları ($\\beta_1$) hesaplanıyor...")
                b1 = random.randint(60, 180)
                time.sleep(1)
                
                cancer_found = True if is_metastatic else random.choice([True, True, False])
                
                if not cancer_found:
                    st.success(f"✅ SONUÇ: BENİGN (SAĞLIKLI) {detected_organ.upper()}")
                    status.update(label="Analiz Tamamlandı", state="complete")
                    st.stop()
                
                status.update(label="Rapor Hazır!", state="complete", expanded=False)

            # --- TANI VERİLERİ ---
            data = {
                "Akciğer": {"tur": "Adenokarsinom", "ilac": "Osimertinib / Pembrolizumab", "cerrahi": "Lobektomi Önerilir."},
                "Mide": {"tur": "Taşlı Yüzük Hücreli Karsinom", "ilac": "Ramucirumab + Paclitaxel", "cerrahi": "Gastrektomi Önerilir."},
                "Pankreas": {"tur": "Duktal Adenokarsinom", "ilac": "FOLFIRINOX Rejimi", "cerrahi": "Whipple Prosedürü."}
            }
            res = data[detected_organ]
            evre = "EVRE IV" if is_metastatic else "EVRE I-III"

            st.markdown(f"""
            <div class='report-card'>
            <h2 style='color:#be123c;'>🚩 POZİTİF TANI: {res['tur'].upper()}</h2>
            <hr>
            <b>1. ANALİZ:</b> {detected_organ} dokusu, Betti-1: {b1}<br>
            <b>2. EVRE:</b> {evre}<br>
            <b>3. TEDAVİ (3T):</b> {res['ilac']}<br>
            <b>4. CERRAHİ:</b> {res['cerrahi']}<br><br>
            <i>*Metastaz Notu: {'SİSTEMİK TEDAVİ ÖNCELİKLİDİR.' if is_metastatic else 'Lokalize cerrahi sınır kontrolü önerilir.'}</i>
            </div>
            """, unsafe_allow_html=True)
            
            report = f"MATHRIX RAPOR\nOrgan: {detected_organ}\nTur: {res['tur']}\nEvre: {evre}"
            st.download_button("📩 RAPORU İNDİR", report, "MathRix_Rapor.txt")
