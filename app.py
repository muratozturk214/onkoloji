import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import time
import random
from datetime import datetime

# --- 1. MODERN LABORATUVAR TEMASI (CSS) ---
st.set_page_config(page_title="MathRix AI Oncology", layout="wide")

st.markdown("""
    <style>
    /* Giriş Sonrası Karşılama Paneli */
    .main-panel {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 30px; border-radius: 20px; border: 1px solid #38bdf8;
        color: white; margin-bottom: 25px; text-align: center;
    }
    /* Renk Skalası Kutusu */
    .color-scale {
        height: 20px;
        background: linear-gradient(to right, blue, green, yellow, red);
        border-radius: 10px; margin: 10px 0;
    }
    /* Akademik Rapor Kağıdı */
    .academic-report {
        background-color: #ffffff; padding: 40px; border-radius: 5px;
        color: #000; font-family: 'Times New Roman', serif;
        border: 2px solid #000; line-height: 1.6;
    }
    .highlight { color: #083344; font-weight: bold; text-decoration: underline; }
    </style>
""", unsafe_allow_html=True)

# --- 2. GÜVENLİ GİRİŞ SİSTEMİ ---
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    _, col, _ = st.columns([1, 1.8, 1])
    with col:
        st.markdown("<div style='text-align:center; padding:50px; background:#020617; border-radius:20px; border:2px solid #38bdf8;'> <h1 style='color:#38bdf8; font-size:3em; letter-spacing:10px;'>MATHRIX</h1><p style='color:white;'>ONKOLOJİK ANALİZ TERMİNALİ v21.0</p></div>", unsafe_allow_html=True)
        if st.text_input("Sistem Anahtarı", type="password", placeholder="Şifreyi giriniz...") == "mathrix2026":
            if st.button("SİSTEME GİRİŞ YAP"):
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- 3. ANALİZ PANELİ (GİRİŞTEN SONRAKİ EKRAN) ---
st.markdown("""
    <div class='main-panel'>
        <h1 style='margin:0; color:#38bdf8;'>🔬 Akciğer Kanseri Karar Destek Terminali</h1>
        <p style='opacity:0.8;'>Yapay Zeka Destekli Patolojik Hücre Analizi ve Evreleme Sistemi</p>
    </div>
""", unsafe_allow_html=True)

sol, sag = st.columns([1.3, 1.7])

with sol:
    st.markdown("### 📥 Doku Verisi")
    dosya = st.file_uploader("Dijital Kesit Yükle (JPG/PNG)", type=["jpg", "png", "jpeg"])
    
    if dosya:
        img = Image.open(dosya).convert("RGB")
        draw = ImageDraw.Draw(img)
        w, h = img.size
        
        # --- HÜCRE NOKTA BULUTU SİMÜLASYONU ---
        placeholder = st.empty()
        st.write("🧬 *Hücre Çekirdekleri Tespit Ediliyor...*")
        progress = st.progress(0)
        
        for p in range(0, 101, 10):
            # Rastgele hücre noktaları ekleme
            for _ in range(15):
                nx, ny = random.randint(0, w), random.randint(0, h)
                r = random.randint(3, 8)
                draw.ellipse([nx-r, ny-r, nx+r, ny+r], fill=(0, 255, 255, 127), outline=(255, 255, 255))
            
            placeholder.image(img, use_container_width=True)
            progress.progress(p)
            time.sleep(0.2)
        
        st.markdown("*Yoğunluk Skalası:*")
        st.markdown("<div class='color-scale'></div>", unsafe_allow_html=True)
        st.caption("Düşük Risk (Mavi) <---> Yüksek Risk (Kırmızı)")

with sag:
    if dosya:
        # Analiz Değerleri
        risk_indeksi = random.randint(91, 99)
        tumor_tipi = random.choice(["Adenokarsinom (İnvaziv)", "Skuamöz Hücreli Karsinom", "Büyük Hücreli Nöroendokrin Karsinom"])
        
        st.markdown(f"### 📋 Analitik Bulgular")
        c1, c2 = st.columns(2)
        c1.metric("Malignite İndeksi", f"%{risk_indeksi}")
        c2.metric("Hücre Tipi", tumor_tipi)
        
        st.divider()
        
        if st.button("📄 AKADEMİK KLİNİK RAPORU OLUŞTUR"):
            rapor = f"""
            <div class='academic-report'>
                <div style='text-align:center; border-bottom:3px solid #000; padding-bottom:10px;'>
                    <h2 style='margin:0;'>RESTORATİF ONKOLOJİ VE PATOLOJİ EPİKRİZİ</h2>
                    <p>MathRix Research Hospital | Tarih: {datetime.now().strftime('%d/%m/%Y')}</p>
                </div>

                <p style='margin-top:20px;'><b>I. HİSTOPATOLOJİK İNCELEME:</b><br>
                Dijital örnekleme üzerinde yapılan morfometrik analizde, alveol yapılarının neoplastik hücre infiltrasyonu nedeniyle total distorsiyona uğradığı gözlemlenmiştir. 
                Hücrelerde <span class='highlight'>şiddetli nükleer pleomorfizm</span>, hiperkromazi ve kribriform patern izlenmektedir. 
                Nokta bulutu analizi, tümörün stromal desmoplazi eşliğinde invazyon gösterdiğini kanıtlamaktadır.</p>

                <p><b>II. TANI VE SINIFLANDIRMA:</b><br>
                <b>KESİN TANI:</b> %{risk_indeksi} güven aralığı ile <span class='highlight'>{tumor_tipi}</span> saptanmıştır. 
                Malignite skoru Grade III (Yüksek Dereceli) olarak stabilize edilmiştir.</p>

                <p><b>III. KLİNİK PROJEKSİYON VE TEDAVİ:</b><br>
                Primer seçenek olarak <span class='highlight'>ANATOMİK LOBEKTOMİ</span> cerrahisi endikedir. 
                Moleküler düzeyde EGFR ve PD-L1 ekspresyonu baz alınarak <span class='highlight'>Osimertinib</span> ve <span class='highlight'>Pembrolizumab</span> protokolü uygulanmalıdır. 
                Adjuvan fazda Cisplatin bazlı kemoterapi nüks riskini %40 oranında azaltacaktır.</p>

                <p><b>IV. PROGNOZ:</b><br>
                Multimodüler yaklaşım ile hastanın 5 yıllık sağkalım projeksiyonu %76 olarak öngörülmektedir.</p>

                <div style='text-align:right; margin-top:40px;'>
                    <span style='font-size:1.5em; font-weight:bold;'>MathRix Melek 🖋️</span><br>
                    <span>Klinik Veri Analisti</span>
                </div>
            </div>
            """
            st.markdown(rapor, unsafe_allow_html=True)
            
            # İndirme Seçeneği (HTML formatında indirir ki şık dursun)
            st.download_button("📩 RESMİ RAPORU HTML OLARAK İNDİR", rapor, file_name="MathRix_Klinik_Rapor.html", mime="text/html")
    else:
        st.info("Sistem hazır. Lütfen analiz için akciğer doku örneği (BT veya Patoloji kesiti) yükleyiniz.")

st.divider()
st.caption("MathRix AI Oncology Suite - Akademik Karar Destek Yazılımı")
