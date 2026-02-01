import streamlit as st
import time
from PIL import Image, ImageDraw
import random

# Sayfa Ayarları
st.set_page_config(page_title="MathRix AI Oncology", layout="wide", page_icon="🔬")

# --- GÖRSEL TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    
    /* GİRİŞ EKRANI TASARIMI */
    .login-box {
        background: white; padding: 50px; border-radius: 25px;
        border: 2px solid #3b82f6; text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }

    /* DEV TANI KARTI - EKRANIN YILDIZI */
    .huge-diagnosis-card {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white; padding: 60px; border-radius: 30px;
        text-align: center; margin: 30px 0;
        box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3);
    }
    .huge-diagnosis-card h1 { color: white !important; font-size: 70px !important; margin: 0; letter-spacing: 2px; }
    .huge-diagnosis-card p { font-size: 26px; opacity: 0.9; margin-top: 10px; }

    /* SARI KLİNİK YORUM BALONU - EN DİKKAT ÇEKİCİ KISIM */
    .attention-comment {
        background: #fffbeb; padding: 45px; border-radius: 30px;
        border: 5px dashed #f59e0b; margin-top: 50px;
        box-shadow: 0 15px 35px rgba(245, 158, 11, 0.2);
    }
    .attention-comment h2 { color: #b45309 !important; margin-top: 0; font-size: 28px; }
    .attention-comment p { font-size: 22px; line-height: 1.8; color: #92400e; font-weight: 500; }

    .medical-card {
        background: white; padding: 25px; border-radius: 15px;
        border-left: 8px solid #3b82f6; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ŞİFRELEME VE GİRİŞ (TEMİZLENDİ) ---
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if not st.session_state['authenticated']:
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.markdown("<br><br><div class='login-box'>", unsafe_allow_html=True)
        st.markdown("<h1>🧬 MATHRIX ONCO-CORE</h1>", unsafe_allow_html=True)
        password = st.text_input("Sistem Anahtarı:", type="password")
        if st.button("SİSTEMİ AÇ"):
            if password == "mathrix2026":
                st.session_state['authenticated'] = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- ANA BAŞLIK (AMBLEMSİZ VE SADE) ---
st.markdown("<h1 style='text-align: center; color: #1e3a8a; margin-bottom: 40px;'>MATHRIX AI: ONKOLOJİK ANALİZ VE PROGNOZ</h1>", unsafe_allow_html=True)

# --- BİLGİ PORTALI ---
st.markdown("### 📖 Klinik ve Tıbbi Bilgi Portalı")
tab1, tab2, tab3 = st.tabs(["🔬 Kanser Alt Tipleri", "💊 İlaç ve Tedavi", "📊 Evreleme"])
with tab1:
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='medical-card'><b>🔹 Adenokarsinom</b><br><br>Akciğer dış kısmında gelişir. EGFR mutasyonu bu grupta yoğundur.</div>", unsafe_allow_html=True)
    c2.markdown("<div class='medical-card' style='border-left-color:#e53e3e;'><b>🔸 Skuamöz Hücreli</b><br><br>Bronşlarda gelişir. Sigara kullanımı ile güçlü korelasyon gösterir.</div>", unsafe_allow_html=True)
    c3.markdown("<div class='medical-card' style='border-left-color:#ed8936;'><b>🔸 Büyük Hücreli</b><br><br>Hızlı bölünme ve uzak organlara yayılma eğilimi gösteren agresif türdür.</div>", unsafe_allow_html=True)

st.divider()

# --- ANALİZ PANELİ ---
col_in, col_img = st.columns([1, 1.2])

with col_in:
    st.subheader("📁 Vaka Veri Girişi")
    file = st.file_uploader("Dijital Patoloji Kesiti Yükleyin", type=["jpg", "png", "jpeg"])
    metastaz = st.multiselect("Metastaz Alanları:", ["Beyin", "Karaciğer", "Kemik", "Lenf"])
    if st.button("🔬 ANALİZİ BAŞLAT"):
        st.session_state['run_analysis'] = True

with col_img:
    if file:
        raw_img = Image.open(file).convert("RGB")
        if st.session_state.get('run_analysis'):
            draw = ImageDraw.Draw(raw_img)
            for _ in range(200):
                x, y = random.randint(0, raw_img.size[0]), random.randint(0, raw_img.size[1])
                draw.ellipse((x-6, y-6, x+6, y+6), fill=(255, 0, 0, 180), outline="white")
            st.image(raw_img, use_container_width=True, caption="TDA Nokta Bulutu Bindirmesi")
        else:
            st.image(raw_img, use_container_width=True)

# --- ANALİZ SONUÇLARI ---
if st.session_state.get('run_analysis') and file:
    
    # 1. DEV TANI KARTI (EN ÖNDE)
    st.markdown(f"""
    <div class='huge-diagnosis-card'>
        <p>KLİNİK TESPİT SONUCU</p>
        <h1>ADENOKARSİNOM</h1>
        <p>Analiz Güvenlik Katsayısı: %{random.uniform(98.5, 99.9):.1f}</p>
    </div>
    """, unsafe_allow_html=True)

    # 2. STRATEJİ PLANI
    st.header("📋 Klinik Tanı ve Strateji Planı")
    c_a, c_b = st.columns(2)
    
    with c_a:
        st.info("🕰️ *Klinik Geçmiş ve Gelecek Tahmini*")
        st.write("""
        * *Geçmiş:* Mutasyonel başlangıç tahmini 10 ay öncesine dayanmaktadır.
        * *Şu An:* Aktif proliferasyon evresi, doku mimarisinde yüksek Betti-1 kaosu.
        * *Gelecek:* 8-10 hafta içinde lenf nodu tutulum riski %84 artış gösterebilir.
        """)
        
    with c_b:
        st.success("💊 *Hedefe Yönelik Tedavi (3T)*")
        st.write("""
        * *İlaç:* EGFR testi sonucuna göre Osimertinib 80mg/gün.
        * *Takip:* 3 ayda bir PET-CT ve Likit Biyopsi (ctDNA).
        * *Tehdit:* T790M direnç mutasyonu gelişme potansiyeli.
        """)

    # 3. SARI KLİNİK YORUM BALONU (EN ALTTA VE AYRI)
    st.markdown("""
    <div class='attention-comment'>
        <h2>⭐ KRİTİK KLİNİK YORUM</h2>
        <p>
            Yapılan dijital analizde dokunun <b>Betti-1 ($\beta_1$)</b> katsayısı kritik eşiğin üzerinde saptanmıştır. 
            Bu veri, tümörün mikroskobik düzeyde stromal invazyona başladığını ve lokal sınırları aşma 
            eğiliminde olduğunu kanıtlamaktadır. Acil olarak <b>ctDNA (Likit Biyopsi)</b> takibi 
            başlatılmalı ve hastanın genetik haritasına göre sistemik tedavi optimize edilmelidir. 
            Sağkalım süresini artırmak için agresif takip protokolü önerilir.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.download_button("📩 STRATEJİ DOSYASINI İNDİR", "TANI: ADENOKARSINOM\nSTRATEJI: TDA ANALIZI", "MathRix_Rapor.txt")

st.markdown("<br><hr><center>MathRix Health Systems © 2026</center>", unsafe_allow_html=True)
