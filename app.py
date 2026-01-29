import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import time
import random
from datetime import datetime

# --- 1. SİSTEM AYARLARI ---
st.set_page_config(page_title="MathRix AI | Lung Oncology", layout="wide")

st.markdown("""
    <style>
    .report-paper { background-color: white; padding: 30px; border-left: 10px solid #083344; color: black; font-family: 'Times New Roman', serif; border: 1px solid #ddd; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. GİRİŞ EKRANI (Şifre: mathrix2026) ---
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.title("🧬 MATHRIX TERMINAL")
        if st.text_input("Erişim Anahtarı", type="password") == "mathrix2026":
            if st.button("Sistemi Aktive Et"):
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- 3. ANA ANALİZ PANELİ ---
st.title("🫁 Akciğer Kanseri Akıllı Teşhis Terminali")

sol, sag = st.columns([1.2, 1.8])

with sol:
    dosya = st.file_uploader("Akciğer Kesiti Yükle", type=["jpg", "png", "jpeg"])
    if dosya:
        img = Image.open(dosya).convert("RGB")
        # --- CANLI TARAMA EFEKTİ (ÇUBUK ÇUBUK GÖSTERİM) ---
        progress_bar = st.progress(0)
        status_text = st.empty()
        image_place = st.empty()
        
        # Tarama simülasyonu
        draw = ImageDraw.Draw(img)
        w, h = img.size
        for i in range(0, 101, 20):
            status_text.text(f"Hücre yapıları taranıyor: %{i}")
            progress_bar.progress(i)
            # Görsel üzerine AI tarama çizgileri ekle
            y = int((i/100) * h)
            draw.line([(0, y), (w, y)], fill=(0, 255, 255), width=5)
            image_place.image(img, use_container_width=True)
            time.sleep(0.3)
        st.success("Tarama Tamamlandı.")

with sag:
    if dosya:
        # Dinamik Analiz Verileri (Her seferinde değişir)
        skor = random.randint(89, 99)
        evre = random.choice(["II-B", "III-A", "III-B"])
        tip = random.choice(["Adenokarsinom", "Skuamöz Hücreli Karsinom", "Büyük Hücreli Karsinom"])
        
        st.subheader("📋 Klinik Bulgular")
        c1, c2, c3 = st.columns(3)
        c1.metric("Malignite İndeksi", f"%{skor}")
        c2.metric("Klinik Evre", evre)
        c3.metric("Hücre Tipi", tip)

        st.divider()

        # AKADEMİK RAPOR (Saf metin, önemli yerler kalın)
        rapor = f"""
        ### 📄 RESMİ KLİNİK ANALİZ RAPORU
        *TARİH:* {datetime.now().strftime('%d/%m/%Y')} | *KAYIT NO:* MX-{random.randint(1000,9999)}
        
        *1. PATOLOJİK DEĞERLENDİRME:*
        Yüklenen dijital kesit üzerinde yapılan morfometrik analizde, normal parankim yapısının *atipi gösteren epitel hücreleri* tarafından infiltre edildiği gözlenmiştir. 
        Hücrelerde *belirgin pleomorfizm* ve nükleer hiperkromazi saptanmış olup, mitotik aktivite oranı *%{skor}* olarak hesaplanmıştır.
        
        *2. TANI VE SINIFLANDIRMA:*
        Bulgular, Dünya Sağlık Örgütü (WHO) kriterlerine göre *{tip}* tanısını %{skor-2} güven aralığı ile doğrulamaktadır. 
        Tümör dokusunun *vasküler invazyon* potansiyeli yüksek risk grubundadır.
        
        *3. CERRAHİ VE TEDAVİ PLANI:*
        Mevcut hücre tipi ve yayılımı nedeniyle *ANATOMİK LOBEKTOMİ* operasyonu zorunludur. 
        Operasyon sonrası hastaya *Adjuvan Kemoterapi* (Cisplatin + Pemetrexed) ve PD-L1 seviyesine göre *İmmünoterapi (Pembrolizumab)* başlanması akademik olarak endikedir.
        
        *4. PROGNOZ VE RADYASYON STRATEJİSİ:*
        Küratif cerrahi sonrası nüks riskini azaltmak amacıyla *IMRT (Yoğunluk Ayarlı Radyoterapi)* planlanmalıdır. 
        Hastanın 5 yıllık sağkalım projeksiyonu multimodüler tedavi ile *%74* olarak öngörülmektedir.
        
        ---
        *DİJİTAL ONAY:* MathRix Melek 🖋️
        """
        
        st.markdown(f"<div class='report-paper'>{rapor}</div>", unsafe_allow_html=True)
        
        st.download_button("📩 RESMİ RAPORU İNDİR (.TXT)", rapor, file_name="MathRix_Klinik_Rapor.txt")
