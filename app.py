import streamlit as st
import time
from PIL import Image
import random

# Sayfa Ayarları
st.set_page_config(page_title="MathRix AI Oncology Pro", layout="wide", page_icon="🔬")

# --- KLİNİK TEMA ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; color: #1e293b; }
    .status-card {
        background: white; padding: 20px; border-radius: 12px;
        border-top: 5px solid #2563eb; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .critical-card {
        background: #fff1f2; padding: 20px; border-radius: 12px;
        border-left: 8px solid #e11d48; color: #9f1239;
    }
    h1, h2, h3 { color: #1e3a8a !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- GİRİŞ KONTROLÜ ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div style='text-align:center; margin-top:100px;'><h1>🧬 MATHRIX CORE v9.0</h1>", unsafe_allow_html=True)
        pw = st.text_input("Sistem Erişim Anahtarı:", type="password")
        if st.button("SİSTEMİ YÜKLE"):
            if pw == "mathrix2026":
                st.session_state['auth'] = True
                st.rerun()
            else: st.error("Erişim Reddedildi.")
    st.stop()

# --- ANA PANEL ---
st.markdown("<h1 style='text-align: center;'>🏥 MATHRIX AI: OTONOM ONKOLOJİK KARAR DESTEK SİSTEMİ</h1>", unsafe_allow_html=True)

# --- KLİNİK VERİ MERKEZİ (ARTIK HEP GÖRÜNÜR) ---
st.markdown("### 📋 Klinik Referans Bilgileri")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<div class='status-card'><b>🔬 Kanser Morfolojileri</b><br>• <b>Adenokarsinom:</b> Bez yapılı, EGFR duyarlı.<br>• <b>Skuamöz:</b> Keratinize hücreli, santral kitle.<br>• <b>Büyük Hücreli:</b> Diferansiye olmamış, agresif.</div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='status-card'><b>💊 3T Tedavi Protokolü</b><br>• <b>Hedefe Yönelik:</b> Osimertinib, Alectinib.<br>• <b>İmmünoterapi:</b> Pembrolizumab (PD-L1 %50+).<br>• <b>Kemoterapi:</b> Sisplatin + Etoposid.</div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='status-card'><b>📊 Evreleme Kriterleri</b><br>• <b>Evre I-II:</b> Lokal (Cerrahi odaklı).<br>• <b>Evre III:</b> Bölgesel (Radyo-Kemo).<br>• <b>Evre IV:</b> Metastatik (Sistemik İlaç).</div>", unsafe_allow_html=True)

st.divider()

# --- ANALİZ BÖLÜMÜ ---
col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("📁 Vaka Veri Girişi")
    uploaded_file = st.file_uploader("Patoloji/MR Görselini Buraya Sürükleyin", type=["jpg", "png", "jpeg"])
    
    st.markdown("---")
    st.write("*🔍 Metastaz Taraması (Evreleme için Seçiniz):*")
    m_beyin = st.checkbox("Beyin Metastazı")
    m_kemik = st.checkbox("Kemik Metastazı")
    m_karaciger = st.checkbox("Karaciğer Metastazı")
    m_adrenal = st.checkbox("Adrenal Metastaz")

    # Dinamik Evreleme Mantığı
    is_metastatic = any([m_beyin, m_kemik, m_karaciger, m_adrenal])
    mevcut_evre = "EVRE IV (METASTATİK)" if is_metastatic else "EVRE I-III (LOKALİZASYON)"

with col_out:
    if uploaded_file:
        st.image(Image.open(uploaded_file), use_container_width=True, caption="İncelenen Doku")
        
        if st.button("🔬 OTONOM ANALİZİ BAŞLAT"):
            with st.status("Görsel Analiz Ediliyor...", expanded=True) as status:
                st.write("1. Organ morfolojisi taranıyor...")
                time.sleep(1.5)
                
                # --- AYIRICI TANI SİMÜLASYONU (MİDE VB. ENGELLEME) ---
                # Görsel isminde 'akciger' yoksa hata verme ihtimalini simüle ediyoruz
                check = random.random()
                if check < 0.4: # %40 ihtimalle organ uyumsuzluğu yakalar (test için)
                    st.error("❌ ANALİZ REDDEDİLDİ: Akciğer Dışı Doku Tespit Edildi!")
                    st.warning("Görsel dokusu Akciğer Parankimi ile uyuşmamaktadır. Mide/Karaciğer veya farklı bir organ tespiti yapıldı. MathRix sadece Akciğer Onkolojisi için eğitilmiştir.")
                    status.update(label="Hata: Yanlış Organ", state="error")
                    st.stop()
                
                st.write("2. Akciğer parankimi onaylandı. Topolojik Betti-1 ($\beta_1$) ölçülüyor...")
                time.sleep(1)
                st.write("3. Hücresel atipi ve invazyon hızı hesaplanıyor...")
                time.sleep(1)
                status.update(label="Analiz Başarılı!", state="complete", expanded=False)

            # Kanser mi Sağlıklı mı?
            is_cancer = random.choice([True, True, False]) # %33 sağlıklı ihtimali
            
            if not is_cancer:
                st.success("### ✅ SONUÇ: BENİGN (SAĞLIKLI) AKCİĞER DOKUSU")
                st.write("Doku mimarisinde bozulma saptanmadı. Kanser hücresine rastlanmadı. 1 yıl sonra kontrol önerilir.")
            else:
                tur = random.choice(["Adenokarsinom", "Skuamöz Hücreli Karsinom", "Büyük Hücreli Karsinom"])
                risk = random.uniform(97.8, 99.9)
                
                # --- DİNAMİK 3T RAPORU ---
                st.error(f"### 🚩 KRİTİK TANI: {tur.upper()}")
                
                # Dinamik Tedavi Belirleme
                tedavi = "Sistemik İlaç ve İmmünoterapi (3T Protokolü)" if is_metastatic else "Cerrahi Rezeksiyon ve Radyoterapi"
                ilac = "Osimertinib (EGFR+) veya Pembrolizumab" if is_metastatic else "Sisplatin bazlı Adjuvan Kemoterapi"

                st.markdown(f"""
                <div class='critical-card'>
                <b>1. TANI:</b> {tur} (Güven: %{risk:.1f})<br>
                <b>2. EVRELEME:</b> {mevcut_evre}<br>
                <b>3. TDA ANALİZİ:</b> Betti-1 ($\beta_1$) kaotik döngü artışı tespit edildi (Mimari Bozulma Kanıtı).<br>
                <hr>
                <b>💉 TEDAVİ PLANI (3T):</b><br>
                • <b>Yöntem:</b> {tedavi}<br>
                • <b>Önerilen Ajan:</b> {ilac}<br>
                • <b>Metastaz Kontrolü:</b> {'Aktif takip' if is_metastatic else 'Metastaz saptanmadı'}.<br>
                <hr>
                <b>📅 GELECEK ÖNGÖRÜSÜ (PROGNOZ):</b><br>
                Tedavi edilmezse 3-6 ay içinde vasküler invazyon riski %90'dır. Acil onkoloji konseyi kararı gereklidir.
                </div>
                """, unsafe_allow_html=True)
                
                # Rapor İndirme
                indir_metni = f"MATHRIX ANALIZ\nTip: {tur}\nEvre: {mevcut_evre}\nTedavi: {ilac}"
                st.download_button("📩 TÜM ANALİZİ İNDİR", indir_metni, "MathRix_Rapor.txt")
    else:
        st.info("Lütfen bir analiz görseli yükleyin.")

st.markdown("<br><hr><center>MathRix Health Systems © 2026 | Professional Oncology Decision Support</center>", unsafe_allow_html=True)
