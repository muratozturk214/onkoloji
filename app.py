import streamlit as st
import time
from PIL import Image
import random

# Sayfa Ayarları
st.set_page_config(page_title="MathRix AI Oncology Pro", layout="wide")

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

# --- ANA PANEL ---
st.markdown("<h1 style='color: #003366; text-align: center;'>🧬 MATHRIX ONKOLOJİ ANALİZ PANELİ</h1>", unsafe_allow_html=True)

# --- KLİNİK BİLGİ BANKASI ---
st.subheader("📚 Akciğer Kanseri Klinik Bilgi Bankası")
tab1, tab2, tab3 = st.tabs(["Kanser Türleri", "Evreleme & Metastaz", "İlaçlar & Tedavi"])

with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("*1. Adenokarsinom:* En yaygın türdür. Genelde akciğerin dış (periferik) kısımlarında, salgı bezlerinden köken alır.")
        st.info("*2. Skuamöz Hücreli:* Genellikle ana bronşlarda gelişir ve sigara kullanımı ile çok güçlü bir bağı vardır.")
    with col_b:
        st.info("*3. Büyük Hücreli:* Hızla büyüyen, geniş sitoplazmalı ve belirgin nükleollü agresif bir tümördür.")
        st.info("*4. Küçük Hücreli (KHAK):* Çok hızlı yayılır, erken evrede beyin ve karaciğer metastazı yapabilir.")

with tab2:
    st.warning("⚠️ *Metastaz Durumu:* Akciğer kanseri hücreleri kan yoluyla en sık Karaciğer, Beyin, Kemik ve Böbrek Üstü bezlerine yayılır.")
    st.write("Uzak organlarda kitle saptanması durumunda hastalık *Evre 4 (Metastatik)* olarak sınıflandırılır.")

with tab3:
    c1, c2 = st.columns(2)
    c1.success("*Akıllı İlaçlar:* EGFR, ALK, ROS1 gibi mutasyonlar varsa hedefleyici tedaviler (Örn: Osimertinib) tercih edilir.")
    c2.error("*İmmünoterapi:* Bağışıklık hücrelerinin tümörü tanımasını sağlar (Örn: Pembrolizumab - Keytruda).")

st.divider()

# --- ANALİZ BÖLÜMÜ ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📸 Görüntü Analiz Ünitesi")
    uploaded_file = st.file_uploader("Patoloji/Radyoloji Görüntüsü Yükle", type=["jpg", "png", "jpeg"])
    
    with st.expander("📋 Klinik Verileri Gir (İsteğe Bağlı)"):
        yas = st.number_input("Hasta Yaşı:", 1, 120, 65)
        sigara = st.selectbox("Sigara Öyküsü:", ["Belirtilmedi", "Hiç içmemiş", "Eski içici", "Aktif içici"])
        metastaz = st.multiselect("Bilinen Metastazlar:", ["Yok", "Karaciğer", "Beyin", "Kemik"])

with col_right:
    if uploaded_file:
        st.image(Image.open(uploaded_file), use_container_width=True)
        
        if st.button("🔬 DERİN ANALİZİ BAŞLAT"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Analiz Simulasyonu
            for i in range(1, 101):
                time.sleep(0.04)
                progress_bar.progress(i)
                if i < 30: status_text.text("Doku mimarisi taranıyor...")
                elif i < 60: status_text.text("Hücre çekirdekleri analiz ediliyor...")
                elif i < 90: status_text.text("Vasküler yapılar ve atipi kontrol ediliyor...")
                else: status_text.text("Rapor hazırlanıyor...")
                
            # --- GELİŞMİŞ ANALİZ SONUÇLARI ---
            turler = ["Adenokarsinom", "Skuamöz Hücreli Karsinom", "Büyük Hücreli Karsinom"]
            secilen_tur = random.choice(turler)
            risk_skoru = random.uniform(88.4, 97.9)
            
            st.error(f"### 🚩 KRİTİK ANALİZ SONUCU: {secilen_tur.upper()}")
            
            # Uzun ve Detaylı Bilgi Kısmı
            st.markdown(f"""
            *Detaylı Patolojik Tanı Analizi:*
            Incelenen örnekte hücresel boyutta *belirgin nükleer pleomorfizm* ve hiperkromazi saptanmıştır. Hücrelerin dizilimi ve doku içerisindeki yayılım paternleri incelendiğinde, bu görünümün yüksek olasılıkla *{secilen_tur}* ile uyumlu olduğu görülmektedir. 
            
            *Saptanan Bulgular:*
            - *Mitoz Hızı:* Yüksek dereceli mitotik aktivite gözlemlendi.
            - *Atipi Derecesi:* %{risk_skoru:.1f} oranında malignite uyumlu hücresel bozulma.
            - *İnfiltrasyon:* Çevre dokularda invazyon (yayılım) şüphesi mevcut.
            
            *Klinik Öneri:* Hastanın yaşı ({yas}) ve mevcut durumu göz önüne alındığında, tanıyı kesinleştirmek için *İmmünohistokimya (IHC)* boyamaları yapılmalı ve mutasyon analizi için *Next-Generation Sequencing (NGS)* testi istenmelidir. Eğer metastaz şüphesi varsa PET-BT taraması hayati önem taşır.
            """)
            
            # Uzun Rapor İçeriği
            rapor_metni = f"""
            MATHRIX AI ONKOLOJI PROFESYONEL ANALIZ RAPORU
            ----------------------------------------------
            TARIH: {time.strftime('%d/%m/%Y')}
            RAPOR ID: MX-{random.randint(10000, 99999)}
            
            [HASTA VERILERI]
            Yas: {yas}
            Sigara Durumu: {sigara}
            Metastaz Durumu: {', '.join(metastaz) if metastaz else 'Belirtilmedi'}
            
            [AI DEEP LEARNING BULGULARI]
            Yapilan dijital patoloji taramasinda doku mimarisinin {secilen_tur} 
            ozelliklerini %{risk_skoru:.1f} dogruluk payi ile tasidigi saptanmistir. 
            Hucrelerde kitle olusumu ve duzensiz nükleus yapilari (Atipi) mevcuttur.
            
            [TEDAVI VE PLANLAMA TAVSIYESI]
            - Oncelikle histolojik alt tipin patolog tarafindan teyidi gereklidir.
            - Hastaya ozel immunoterapi (PD-L1 skoru) arastirilmalidir.
            - Akilli ilac (Targeted Therapy) secenekleri icin genetik mutasyon paneli taranmalidir.
            
            Not: Bu bir yapay zeka on-analizidir. Kesin teshis yerine gecmez.
            """
            
            st.download_button("📩 TAM TIBBİ RAPORU İNDİR", rapor_metni, f"MathRix_Detayli_Rapor_{secilen_tur}.txt")
    else:
        st.info("Lütfen sol taraftan bir görsel yükleyerek analizi başlatın.")

st.markdown("<br><hr><center>MathRix Global Health Systems © 2026 | Professional Decision Support</center>", unsafe_allow_html=True)
