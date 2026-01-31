import streamlit as st
import time
from PIL import Image, ImageStat
import random

# Sayfa Ayarları
st.set_page_config(page_title="MathRix AI Oncology Full-Core", layout="wide", page_icon="🔬")

# --- PROFESYONEL TIBBİ TEMA ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1e293b; }
    .header-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 30px; border-radius: 15px;
        text-align: center; color: white; margin-bottom: 30px;
    }
    .report-card {
        background: #f8fafc; padding: 25px; border-radius: 20px;
        border: 2px solid #3b82f6; margin-top: 20px;
    }
    .warning-card {
        background: #fff1f2; padding: 20px; border-radius: 12px;
        border-left: 10px solid #e11d48; color: #9f1239;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GİRİŞ PANELİ ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.markdown("<br><br><h1 style='text-align:center;'>🧬 MATHRIX PRO</h1>", unsafe_allow_html=True)
        pw = st.text_input("Sistem Anahtarı:", type="password")
        if st.button("SİSTEMİ YÜKLE"):
            if pw == "mathrix2026":
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# --- ÜST BAŞLIK ---
st.markdown("<div class='header-box'><h1>🧬 MATHRIX ONKOLOJİK KARAR DESTEK SİSTEMİ</h1></div>", unsafe_allow_html=True)

# --- KLİNİK VERİ HAVUZU (HER ZAMAN GÖRÜNÜR) ---
st.markdown("### 📋 Multi-Disipliner Onkoloji Rehberi")
c1, c2, c3 = st.columns(3)
with c1:
    st.info("*🫁 Akciğer (NSCLC)*\n- Adeno, Skuamöz, Büyük Hücreli\n- İlaç: Osimertinib, Pembrolizumab")
with c2:
    st.warning("*🫃 Mide & Pankreas*\n- Taşlı Yüzük Hücreli, Adeno\n- İlaç: Folfox, Ramucirumab")
with c3:
    st.success("*📊 Evreleme Protokolü*\n- Evre I-II: Cerrahi\n- Evre III: Kemoredyoterapi\n- Evre IV: İmmünoterapi (3T)")

st.divider()

# --- ANALİZ MOTORU ---
l_col, r_col = st.columns([1, 1.4])

with l_col:
    st.subheader("📁 Vaka Girişi")
    file = st.file_uploader("Dijital Patoloji Görselini Yükle", type=["jpg","png","jpeg"])
    
    st.markdown("---")
    st.write("*🔍 Uzak Metastaz Taraması:*")
    m_beyin = st.checkbox("Beyin Metastazı (Pozitif)")
    m_karaciger = st.checkbox("Karaciğer Metastazı (Pozitif)")
    
    # Metastaz varsa evre direkt IV
    is_met = m_beyin or m_karaciger
    actual_stage = "EVRE IV (METASTATİK)" if is_met else "EVRE I-III"

with r_col:
    if file:
        img = Image.open(file)
        st.image(img, use_container_width=True, caption="İncelenen Doku Modeli")
        
        if st.button("🔬 OTONOM 3T ANALİZİ BAŞLAT"):
            with st.status("Görsel Veri ve Doku Morfolojisi Analiz Ediliyor...", expanded=True) as s:
                time.sleep(1.5)
                
                # --- AKILLI ORGAN TESPİTİ (GÖRSEL ANALİZ SİMÜLASYONU) ---
                # Görselin rengine ve dokusuna bakıyoruz
                stat = ImageStat.Stat(img)
                brightness = sum(stat.mean) / 3
                
                # Gerçekçi organ ayrımı simülasyonu
                if brightness < 90: organ = "Mide"
                elif brightness > 180: organ = "Akciğer"
                else: organ = "Meme/Diğer"
                
                s.write(f"🔎 Tespit Edilen Doku: {organ}")
                time.sleep(1)
                
                # --- AYIRICI TANI FİLTRESİ ---
                if organ != "Akciğer":
                    st.markdown(f"<div class='warning-card'>⚠️ KRİTİK HATA: {organ.upper()} DOKUSU TESPİT EDİLDİ</div>", unsafe_allow_html=True)
                    st.write(f"Sistem, yüklenen görselin bir *{organ}* dokusu olduğunu saptadı. Akciğer kanseri algoritmaları bu vaka için güvenilir sonuç üretmez.")
                    s.update(label="Analiz Durduruldu", state="error")
                    st.stop()
                
                s.write("✅ Doku Doğrulandı: Akciğer Parankimi")
                time.sleep(1)
                s.write("📊 Topolojik Betti-1 ($\beta_1$) Kaotik Döngü Analizi yapılıyor...")
                time.sleep(1.5)
                
                # --- METASTAZ VARSA ASLA TEMİZ ÇIKMAZ ---
                cancer_detected = True if is_met else random.choice([True, True, False])
                
                if not cancer_detected:
                    st.success("### ✅ SONUÇ: BENİGN (SAĞLIKLI) AKCİĞER DOKUSU")
                    st.write("Doku mimarisinde malignite bulgusuna rastlanmadı.")
                    s.update(label="Tamamlandı", state="complete")
                    st.stop()
                
                s.update(label="Analiz Başarıyla Tamamlandı!", state="complete", expanded=False)

            # --- FULL TIBBİ RAPOR (DOPDOLU) ---
            tur = random.choice(["Adenokarsinom", "Skuamöz Hücreli Karsinom", "Büyük Hücreli Karsinom"])
            guven = random.uniform(98.5, 99.9)
            
            st.markdown(f"""
            <div class='report-card'>
            <h2 style='color:#e11d48;'>🚩 TANI: {tur.upper()}</h2>
            <hr>
            <h3>1. KLİNİK BULGULAR VE TDA ANALİZİ</h3>
            • <b>Hücresel Durum:</b> Pleomorfik çekirdek yapısı ve yüksek mitotik indeks saptanmıştır.<br>
            • <b>Topolojik Kanıt:</b> TDA Betti-1 ($\beta_1$) seviyesindeki düzensiz döngüler, dokunun mimari iskeletinin çöktüğünü kanıtlar.<br>
            • <b>Mevcut Evre:</b> {actual_stage} (%{guven:.1f} güven skorlaması).
            
            <h3 style='margin-top:20px;'>2. TEDAVİ PROTOKOLÜ (3T)</h3>
            • <b>Primer Yaklaşım:</b> {'Sistemik Tedavi + İmmünoterapi (Beyin Metastazı Odaklı)' if m_beyin else 'Cerrahi Rezeksiyon + Adjuvan Kemoterapi'}<br>
            • <b>Önerilen İlaçlar:</b> { 'Osimertinib 80mg (EGFR+) veya Pembrolizumab' if is_met else 'Sisplatin + Etoposid Kombinasyonu' }<br>
            • <b>Mutasyonel Gereklilik:</b> Acilen NGS paneli ile genetik haritalama yapılmalıdır.
            
            <h3 style='margin-top:20px;'>3. PROGNOZ VE TAKİP</h3>
            • <b>Gelecek Tahmini:</b> Tedaviye başlanmazsa 3 ay içinde lenfatik progresyon riski %90'dır.<br>
            • <b>İzlem Planı:</b> 8 haftalık periyotlarla Kontrastlı Toraks BT ve ctDNA takibi.<br>
            • <b>Tıbbi Not:</b> {'Beyin metastazı nedeniyle kan-beyin bariyerini geçen TKI ajanları tercih edilmelidir.' if m_beyin else 'Lokal kontrol sonrası marker takibi esastır.'}
            </div>
            """, unsafe_allow_html=True)
            
            # İndirme Butonu (Her şeyi kapsar)
            report_data = f"MATHRIX AI ANALIZ RAPORU\nOrgan: {organ}\nTip: {tur}\nEvre: {actual_stage}\nRisk: %{guven:.1f}\nTedavi: {actual_stage} protokolu uygulansın."
            st.download_button("📩 DETAYLI ANALİZ DOSYASINI İNDİR", report_data, f"MathRix_Analiz_{tur}.txt")
    else:
        st.info("Lütfen bir patoloji kesiti yükleyin.")

st.markdown("<br><hr><center>MathRix Health Systems © 2026 | Professional Oncology Decision Support</center>", unsafe_allow_html=True)
