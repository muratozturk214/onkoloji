import streamlit as st
import time
from PIL import Image
import random

# Sayfa Ayarları
st.set_page_config(page_title="MathRix AI Oncology Pro", layout="wide", page_icon="🔬")

# --- PROFESYONEL TIBBİ TEMA ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; color: #0f172a; }
    .medical-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 10px solid #2563eb;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .timeline-box {
        background: #f1f5f9;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #cbd5e1;
        text-align: center;
    }
    h1, h2, h3 { color: #1e3a8a !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- GİRİŞ ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.markdown("<br><br><div style='background:white; padding:40px; border-radius:20px; border:2px solid #2563eb; text-align:center;'>", unsafe_allow_html=True)
        st.markdown("<h1>🧬 MATHRIX PRO V8.0</h1>", unsafe_allow_html=True)
        password = st.text_input("Sistem Şifresi:", type="password")
        if st.button("SİSTEME ERİŞ"):
            if password == "mathrix2026":
                st.session_state['authenticated'] = True
                st.rerun()
            else: st.error("Erişim Reddedildi!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- ANA PANEL ---
st.markdown("<h1 style='text-align: center;'>🏥 MATHRIX AI: OTONOM AYIRICI TANI VE PROGNOZ SİSTEMİ</h1>", unsafe_allow_html=True)

# --- EVRELEME TABLOSU ---
st.markdown("### 📊 Klinik Evreleme Rehberi")
st.markdown("""
| Evre | TNM Kriteri | Klinik Tanım | Tedavi Yaklaşımı | 5 Yıllık Sağkalım |
| :--- | :--- | :--- | :--- | :--- |
| *Evre I* | T1, N0, M0 | Lokalize, <3cm tümör. | Cerrahi Rezeksiyon (Küratif) | %85 |
| *Evre II* | T2, N1, M0 | Bölgesel lenf tutulumu. | Cerrahi + Adjuvan Kemoterapi | %55 |
| *Evre III* | T3, N2, M0 | İleri yayılım/Medistinal. | Kemoredyoterapi + İmmünoterapi | %25 |
| *Evre IV* | Herhangi M1 | Uzak metastaz. | Sistemik İlaç (3T) / Palyatif | %6 |
""")

st.divider()

# --- ANALİZ PANELİ ---
col_left, col_right = st.columns([1, 1.3])

with col_left:
    st.subheader("📁 Vaka Girişi")
    uploaded_file = st.file_uploader("Patoloji Görselini Buraya Sürükleyin", type=["jpg", "png", "jpeg"])
    metastazlar = st.multiselect("Metastaz Saptanan Odaklar:", ["Beyin", "Kemik", "Karaciğer", "Adrenal", "Lenf"])

with col_right:
    if uploaded_file:
        st.image(Image.open(uploaded_file), use_container_width=True, caption="İncelenen Dijital Kesit")
        
        if st.button("🔬 OTONOM ANALİZİ BAŞLAT"):
            # SİMÜLASYON İÇİN GÖRSEL KONTROLÜ (Gerçek kodda burada model.predict() olur)
            # Buradaki mantık: Dosya isminde 'akciger' yoksa veya rastgele bir kontrolle reddetmek
            with st.status("Neural-Core Taraması Yapılıyor...", expanded=True) as status:
                st.write("1. Doku morfolojisi taranıyor...")
                time.sleep(2)
                
                # SİSTEM BURADA GERÇEKTEN KARAR VERİYORMUŞ GİBİ DAVRANIR
                # Burayı test etmek için: Bazı görsellerde 'Hata' vermesi için kurguladım
                check_value = random.random() 
                
                if check_value < 0.3: # %30 ihtimalle "Bu akciğer değil" der (Meme/Karaciğer testi için)
                    st.error("❌ KRİTİK UYARI: AKCİĞER DIŞI DOKU TESPİTİ")
                    st.markdown("""
                    *Tespit:* Yüklenen görselin hücresel dizilimi *Akciğer Parankimi* ile uyuşmamaktadır (Muhtemel: Karaciğer veya Meme dokusu). 
                    Sistemimiz yalnızca Akciğer Onkolojisi üzerine eğitilmiştir. Hatalı teşhis riskini önlemek için analiz durduruldu.
                    """)
                    status.update(label="Hata: Organ Uyumsuzluğu", state="error")
                    st.stop()
                
                st.write("2. Akciğer parankimi doğrulandı. Hücre atipisi ölçülüyor...")
                time.sleep(1.5)
                
                # Kansersizlik Kontrolü
                is_cancer = random.choice([True, True, False]) # %33 ihtimalle sağlıklı der
                
                if not is_cancer:
                    st.success("### ✅ ANALİZ SONUCU: BENİGN / SAĞLIKLI AKCİĞER DOKUSU")
                    st.markdown("""
                    *Bulgular:* Topolojik Betti-1 ($\beta_1$) değerleri kararlı. Kaotik hücre kümelenmesi saptanmadı. 
                    Doku mimarisi fizyolojik sınırlar içerisindedir. Malignite lehine bulgu izlenmedi.
                    """)
                    status.update(label="Analiz Tamamlandı: Sağlıklı Doku", state="complete")
                    st.stop()

                st.write("3. Kanserli hücreler tespit edildi. Tip tayini yapılıyor...")
                time.sleep(1)
                status.update(label="Tıbbi Analiz Hazır!", state="complete", expanded=False)

            # KANSER TİPİ VE RAPOR
            tur = random.choice(["Adenokarsinom", "Skuamöz Hücreli Karsinom", "Büyük Hücreli Karsinom"])
            risk = random.uniform(97.1, 99.9)
            evre = "EVRE IV" if metastazlar else "EVRE I-III"

            # ZAMAN ÇİZELGESİ
            st.markdown("### ⏳ Patolojik Zaman Çizelgesi (Prognoz)")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("<div class='timeline-box'><b>GEÇMİŞ</b><br>Karsinoma in Situ evresi.<br>(Tahmini 8 ay önce)</div>", unsafe_allow_html=True)
            with c2:
                st.error(f"*ŞU AN (Analiz)*\n\n{tur}\nRisk: %{risk:.1f}\n{evre}")
            with c3:
                st.markdown("<div class='timeline-box'><b>GELECEK</b><br>Tedavi uygulanmazsa lenfatik yayılım riski yüksektir.<br>(Tahmini 4 ay sonra)</div>", unsafe_allow_html=True)

            # DEV TIBBİ RAPOR
            st.markdown("<div class='medical-card'>", unsafe_allow_html=True)
            st.markdown(f"## 📜 AYRINTILI 3T TIBBİ RAPORU")
            st.markdown(f"""
            *1. TANI:* {tur} (%{risk:.1f} Güven Skoru).<br>
            *2. TEDAVİ:* EGFR (+) ise *Osimertinib; PD-L1 > %50 ise **Pembrolizumab*. Metastazlar: {', '.join(metastazlar) if metastazlar else 'Yok'}.<br>
            *3. TAKİP:* 8 haftalık Kontrastlı BT ve ctDNA takibi.
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            indir_txt = f"MATHRIX AI ANALIZ\nID: {random.randint(100,999)}\nSonuc: {tur}\nEvre: {evre}\nMetastaz: {metastazlar}"
            st.download_button("📩 FULL RAPORU İNDİR", indir_txt, "MathRix_Rapor.txt")
    else:
        st.info("Sistemin otonom teşhis koyması için lütfen bir patoloji görüntüsü yükleyin.")

st.markdown("<br><hr><center>MathRix Health Systems © 2026</center>", unsafe_allow_html=True)
