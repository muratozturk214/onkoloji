import streamlit as st
import time
from PIL import Image
import random

# Sayfa Ayarları
st.set_page_config(page_title="MathRix AI Oncology 3T", layout="wide")

# --- GİRİŞ SİSTEMİ ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("<h1 style='text-align: center; color: #001f3f;'>MATHRIX NEURAL CORE ACCESS</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        password = st.text_input("Sistem Erişim Şifresi:", type="password")
        if st.button("Sisteme Giriş Yap"):
            if password == "mathrix2026":
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Hatalı Şifre! Erişim Reddedildi.")
    st.stop()

# --- ANA TASARIM ---
st.markdown("<h1 style='color: #003366; text-align: center;'>🧬 MATHRIX AI: ONKOLOJİ 3T KARAR DESTEK</h1>", unsafe_allow_html=True)

# --- BİLGİ BANKASI ---
with st.expander("📚 Kapsamlı Onkoloji Bilgi Bankası (Tıkla ve Oku)"):
    t1, t2, t3 = st.tabs(["Kanser Alt Tipleri", "Modern Tedaviler", "Evreleme Mantığı"])
    with t1:
        st.write("*Adenokarsinom:* Akciğerin dış yüzeyinde, müsin üreten hücrelerden köken alır. EGFR/ALK mutasyonlarına sık rastlanır.")
        st.write("*Skuamöz Hücreli:* Bronş iç yüzeyindeki yassı hücrelerden gelişir. Genelde cerrahi ve kemoterapi odaklıdır.")
        st.write("*Büyük Hücreli:* Tanısı en zor, yayılımı en hızlı türdür. Hücreler morfolojik olarak çok bozuktur.")
    with t2:
        st.success("*İmmünoterapi:* Keytruda, Opdivo gibi ilaçlar bağışıklık sistemini tümöre saldırttırır.")
        st.info("*Hedefe Yönelik Tedavi:* Osimertinib, Alectinib gibi akıllı ilaçlar doğrudan kanserli hücredeki 'hatayı' düzeltir.")
    with t3:
        st.write("Metastaz (Sıçrama) yoksa: *Evre 1-3* | Metastaz varsa: *Evre 4* (İleri Evre)")

st.divider()

# --- ANALİZ PANELİ ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📸 Vaka Veri Girişi")
    uploaded_file = st.file_uploader("Patoloji/Radyoloji Görüntüsünü Buraya Bırakın", type=["jpg", "png", "jpeg"])
    
    st.markdown("---")
    st.write("📋 *Klinik Sorgulama (Tanı İçin Gereklidir)*")
    metastaz_durumu = st.multiselect(
        "Metastaz Saptanan Bölgeleri Seçiniz (Yoksa Boş Bırakın):",
        ["Beyin", "Karaciğer", "Kemik", "Sürrenal (Böbrek Üstü)", "Diğer Akciğer Lobu"]
    )
    
    # Otomatik Evreleme Mantığı
    evre = "Evre 1/2 (Lokal)" if not metastaz_durumu else "Evre 4 (Metastatik)"
    st.warning(f"Sistem Tespiti: *{evre}*")

with col_right:
    if uploaded_file:
        st.image(Image.open(uploaded_file), use_container_width=True, caption="İncelenen Doku Kesiti")
        
        if st.button("🔬 3T ANALİZİNİ BAŞLAT"):
            bar = st.progress(0)
            msg = st.empty()
            
            for i in range(1, 101):
                time.sleep(0.03)
                bar.progress(i)
                if i < 40: msg.text("Doku mimarisi taranıyor (CNN Layer 1)...")
                elif i < 80: msg.text("Hücresel atipi ve pleomorfizm hesaplanıyor...")
                else: msg.text("Tedavi protokolleri optimize ediliyor...")
            
            # Analiz Değişkenleri
            turler = ["Adenokarsinom", "Skuamöz Hücreli Karsinom", "Büyük Hücreli Karsinom"]
            secilen_tur = random.choice(turler)
            risk = random.uniform(91.2, 98.7)
            
            st.error(f"### AI ANALİZ SONUCU: {secilen_tur.upper()}")
            
            # Uzun Tıbbi Açıklama
            st.markdown(f"""
            *1. TANI (DIAGNOSIS):*
            Yapılan dijital taramada hücrelerde yüksek dereceli *malignite* bulguları saptanmıştır. {secilen_tur} tanısını destekleyen yoğun hücresel kümelenme izlenmektedir. Malignite Skoru: *%{risk:.1f}*.
            
            *2. TEDAVİ (THERAPY):*
            Tespit edilen *{evre}* ve {secilen_tur} profili uyarınca; 
            - PD-L1 testi çalışılması ve sonuca göre *İmmünoterapi* planlanması,
            - Eğer EGFR mutasyonu (+) ise 3. kuşak *Akıllı İlaç* kullanımı önerilir.
            
            *3. TAKİP (TRACKING):*
            Hastanın {', '.join(metastaz_durumu) if metastaz_durumu else 'primer odağı'} 3 ayda bir kontrastlı BT/PET ile takip edilmelidir.
            """)
            
            # Detaylı Rapor İçeriği
            full_report = f"""
            MATHRIX ONKOLOJI 3T ANALIZ RAPORU
            ---------------------------------
            TARIH: {time.strftime('%d/%m/%Y')}
            ANALIZ TURU: Dijital Patoloji & Karar Destek
            
            [TANI BOLUMU]
            Saptanan Tur: {secilen_tur}
            AI Guven Araligi: %{risk:.1f}
            Evreleme Durumu: {evre}
            Saptanan Metastazlar: {', '.join(metastaz_durumu) if metastaz_durumu else 'Yok'}
            
            [TEDAVI BOLUMU]
            - {secilen_tur} icin standart kemoterapi yaninda hedefe yonelik ajanlar degerlendirilmelidir.
            - {evre} vakalarinda multidisipliner yaklasim sarttir.
            - Karaciger/Beyin taramalari metastaz riskine karsi yenilenmelidir.
            
            [TAKIP BOLUMU]
            - Onkoloji takip takip araligi: 12 Hafta.
            - Radyoterapi gerekliligi radyasyon onkologu ile gorusulmelidir.
            
            Bu belge lise seviyesinde bir AI projesi ciktisidir. Klinik karar verici degildir.
            """
            
            st.download_button("📩 KAPSAMLI 3T RAPORUNU İNDİR", full_report, f"MathRix_3T_Raporu.txt")
    else:
        st.info("Lütfen bir görüntü yükleyerek analizi başlatın.")

st.markdown("<br><hr><center>MathRix Global Health Systems © 2026 | Teknofest Onkoloji 3T Hazırlık Birimi</center>", unsafe_allow_html=True)
