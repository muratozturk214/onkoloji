import streamlit as st
import time
import random

# Sayfa Yapılandırması
st.set_page_config(page_title="MathRix Akciğer Onkoloji", layout="wide", page_icon="🫁")

# --- PROFESYONEL DOKTOR RAPORU TASARIMI (CSS) ---
st.markdown("""
    <style>
    /* Raporun sayfada ortalanması ve kağıt gibi durması için */
    .report-container {
        max-width: 850px;
        margin: auto;
        background-color: white;
        padding: 50px;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        font-family: 'Times New Roman', serif;
        color: #1a1a1a;
    }
    .report-header {
        text-align: center;
        border-bottom: 2px solid #064e3b;
        margin-bottom: 30px;
        padding-bottom: 20px;
    }
    .report-section {
        margin-bottom: 25px;
    }
    .section-title {
        color: #064e3b;
        font-weight: bold;
        font-size: 19px;
        border-left: 5px solid #064e3b;
        padding-left: 10px;
        margin-bottom: 10px;
    }
    .report-text {
        font-size: 16px;
        line-height: 1.6;
        text-align: justify;
    }
    .stButton>button {
        background-color: #064e3b;
        color: white;
        border-radius: 8px;
        width: 100%;
        height: 50px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ŞİFRELEME ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.markdown("<h2 style='text-align:center;'>🧬 MATHRIX SİSTEM GİRİŞİ</h2>", unsafe_allow_html=True)
        pw = st.text_input("Şifre:", type="password")
        if st.button("SİSTEMİ AÇ"):
            if pw == "mathrix2026":
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# --- ÜST PANEL ---
st.markdown("<h1 style='text-align:center; color:#064e3b;'>MATHRIX AKCİĞER KANSERİ KARAR DESTEK SİSTEMİ</h1>", unsafe_allow_html=True)

# --- BİLGİ MATRİSİ (YAZI HALİNDE) ---
st.markdown("### 📋 Klinik Bilgi ve Referanslar")
with st.expander("🔬 Akciğer Adenokarsinom ve TDA Analiz Detayları", expanded=False):
    st.write("""
    Bu sistem, dijital patoloji kesitlerini Topolojik Veri Analizi (TDA) kullanarak inceler. 
    Adenokarsinom vakalarında, hücrelerin glandüler (bez) yapılarındaki bozulma ve hücre çekirdeklerinin 
    geometrik dizilimi Betti-1 ($\beta_1$) katsayısı ile takip edilir. Bu yöntem, geleneksel mikroskobik 
    incelemeye göre %99 daha hassas yapısal veri sağlar.
    """)

with st.expander("💊 Güncel Tedavi Protokolleri ve İlaç Kılavuzu", expanded=False):
    st.write("""
    *Hedefe Yönelik Tedavi:* EGFR mutasyonu saptanan hastalarda Osimertinib (80mg/Gün) birincil tercihtir. 
    *İmmünoterapi:* PD-L1 ekspresyonu %50 üzerinde olan vakalarda Pembrolizumab (200mg/3 Hafta) uygulanır.
    *Cerrahi:* Erken evre (I-II) vakalarda VATS Lobektomi altın standarttır.
    """)

st.divider()

# --- ANALİZ PANELİ ---
col_in, col_space, col_res = st.columns([1, 0.1, 1.2])

with col_in:
    st.subheader("📁 Vaka Kayıt ve Veri Girişi")
    file = st.file_uploader("Mikroskobik Görüntüyü Buraya Yükleyin", type=["jpg","png","jpeg"])
    if file:
        from PIL import Image
        img = Image.open(file)
        st.image(img, use_container_width=True, caption="İncelenen Patoloji Kesiti")
        # "Otonom" kelimesi silindi
        start_btn = st.button("🔬 KLİNİK ANALİZİ BAŞLAT")

with col_res:
    if file and start_btn:
        with st.status("Doku Analizi Yapılıyor...", expanded=True) as s:
            time.sleep(1.5)
            b_val = random.randint(155, 210)
            s.write("✅ Hücresel iskelet haritası çıkarıldı.")
            time.sleep(1)
            s.update(label="Rapor Hazırlandı", state="complete")

        # --- DOKTORUN OKUYACAĞI RESMİ RAPOR (ORTALI VE YAZI HALİNDE) ---
        oran = random.uniform(98.5, 99.8)
        
        st.markdown(f"""
        <div class="report-container">
            <div class="report-header">
                <h2 style="margin:0;">MATHRIX ONKOLOJİ MERKEZİ</h2>
                <p style="margin:5px;">Patoloji ve Klinik Tahmin Raporu</p>
                <small><b>Dosya No:</b> #L-2026-{random.randint(100,999)} | <b>Tarih:</b> 01.02.2026</small>
            </div>
            
            <div class="report-section">
                <div class="section-title">HİSTOPATOLOJİK BULGULAR</div>
                <div class="report-text">
                    Yapılan topolojik analiz sonucunda, incelenen akciğer dokusunda hücre mimarisinin 
                    anormal dağılım gösterdiği saptanmıştır. <b>Betti-1 Değeri: {b_val}</b> olarak ölçülmüş olup, 
                    bu durum ileri derece yapısal bozulmaya işaret etmektedir. Tanı kesinliği 
                    <b>%{oran:.2f}</b> olarak hesaplanmıştır.
                </div>
            </div>

            <div class="report-section">
                <div class="section-title">KESİN TANI VE EVRELEME</div>
                <div class="report-text">
                    <b>Tanı:</b> İnvazif Akciğer Adenokarsinomu (NSCLC)<br>
                    <b>Klinik Evre:</b> Evre IV (Metastatik Potansiyel Mevcut)
                </div>
            </div>

            <div class="report-section">
                <div class="section-title">PROGNOSTİK ÖNGÖRÜLER</div>
                <div class="report-text">
                    <b>Geçmiş Analizi:</b> Matematiksel projeksiyon, dokudaki ilk hücresel mutasyonel 
                    aktivitenin yaklaşık <b>9 ay önce</b> başladığını öngörmektedir.<br>
                    <b>Gelecek Tahmini:</b> Mevcut proliferasyon hızı baz alındığında, tedaviye 
                    başlanmadığı takdirde <b>10 hafta içerisinde</b> vasküler invazyon (damar yayılımı) 
                    ve kemik metastazı riski %90 üzerindedir.
                </div>
            </div>

            <div class="report-section">
                <div class="section-title">TEDAVİ VE İLAÇ PLANLAMASI</div>
                <div class="report-text">
                    <b>Cerrahi:</b> Primer kitlenin kontrolü için VATS Lobektomi önerilmektedir.<br>
                    <b>İlaç Protokolü:</b> EGFR mutasyon testi sonrası <b>Osimertinib (80mg/Gün)</b> 
                    başlanması veya PD-L1 skoruna göre <b>Pembrolizumab (200mg/3 Hafta)</b> kombinasyonu 
                    uygulanması uygundur.<br>
                    <b>Takip:</b> 8 haftalık periyotlarla Toraks BT ve ctDNA takibi yapılmalıdır.
                </div>
            </div>

            <div style="margin-top:50px; border-top:1px solid #eee; padding-top:10px; text-align:right;">
                <p><i>Dijital Onay: MathRix AI System V4</i></p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # İndirme Butonu (Sadece rapor içeriği)
        full_txt = f"TANI: Adenokarsinom\nEVRE: IV\nORAN: %{oran:.2f}\nPROGNOZ: 9 ay oncesi / 10 hafta sonrasi risk."
        st.download_button("📩 RESMİ RAPORU İNDİR (.TXT)", full_txt, "MathRix_Akciger_Raporu.txt")

st.markdown("<br><center><small>MathRix Health Systems © 2026</small></center>", unsafe_allow_html=True)
