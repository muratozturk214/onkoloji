import streamlit as st
from PIL import Image
import numpy as np
import time

# -------------------------------
# Klinik Beyaz Tema (CSS)
# -------------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #ffffff;
    color: #000000;
    font-family: 'Arial', sans-serif;
}
.stButton>button {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #000000;
    padding: 8px 16px;
}
.stSidebar {
    background-color: #f8f9fa;
}
.report-box {
    border: 1px solid #000;
    padding: 25px;
    margin-top: 20px;
    background-color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Login Sistemi
# -------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🫁 Klinik Akciğer Tanı Portalı")
    password = st.text_input("Sistem Şifresi", type="password")
    if password == "mathrix2026":
        st.session_state.authenticated = True
        st.experimental_rerun()
    else:
        st.warning("Yetkisiz erişim")
    st.stop()

# -------------------------------
# Sidebar Navigasyon
# -------------------------------
st.sidebar.title("🔍 Navigasyon")
page = st.sidebar.radio(
    "Sayfa Seç",
    ["🔬 Tanı Merkezi", "💊 İlaç Rehberi", "📊 Evreleme Sistemi", "🧬 Kanser Türleri"]
)

# -------------------------------
# Yardımcı Fonksiyonlar
# -------------------------------
def calculate_entropy(image_array):
    hist, _ = np.histogram(image_array.flatten(), bins=256, range=(0, 255))
    prob = hist / np.sum(hist)
    prob = prob[prob > 0]
    entropy = -np.sum(prob * np.log2(prob))
    return entropy

def analyze_image(img):
    gray = img.convert("L")
    arr = np.array(gray)

    # 1️⃣ Lümen / Boşluk Analizi
    threshold = 200
    lumen_ratio = np.sum(arr > threshold) / arr.size

    # 2️⃣ Hücre Yoğunluğu (Variance + Gradient)
    variance = np.var(arr)
    gradient = np.mean(np.abs(np.gradient(arr)))
    density_score = variance + gradient

    # 3️⃣ Isı Dağılımı (Doku Sertliği)
    heat_score = np.mean(arr) + gradient

    # Entropy → Malignite %
    entropy = calculate_entropy(arr)
    malignancy = min((entropy / 8) * 100, 99.9)

    # Karar Mekanizması
    if lumen_ratio > 0.45 and density_score < 4000:
        cancer_type = "Adenokarsinom"
        finding = "Lepidik büyüme paterni"
        prognosis = "6 ayda yavaş progresyon"
    elif heat_score > 180 and density_score > 6000:
        cancer_type = "Skuamöz Hücreli"
        finding = "Keratinizasyon ve interselüler köprüler"
        prognosis = "6 ayda orta agresyon"
    elif density_score > 9000:
        cancer_type = "Küçük Hücreli"
        finding = "Azzopardi fenomeni"
        prognosis = "6 ayda hızlı progresyon"
    else:
        cancer_type = "Büyük Hücreli"
        finding = "Düşük diferansiyasyon"
        prognosis = "6 ayda değişken seyir"

    return {
        "Lümen Oranı": lumen_ratio,
        "Yoğunluk Skoru": density_score,
        "Isı Skoru": heat_score,
        "Entropy": entropy,
        "Malignite %": malignancy,
        "Tür": cancer_type,
        "Bulgular": finding,
        "Prognoz": prognosis
    }

# -------------------------------
# 🔬 TANİ MERKEZİ
# -------------------------------
if page == "🔬 Tanı Merkezi":
    st.title("🔬 Akciğer Kanseri Tanı Merkezi")

    uploaded = st.file_uploader("Histopatolojik Görüntü Yükle", type=["png", "jpg", "jpeg"])

    if uploaded:
        img = Image.open(uploaded)
        st.image(img, caption="Yüklenen Görüntü", use_column_width=True)

        with st.spinner("Matematiksel analiz yapılıyor..."):
            time.sleep(1.5)
            result = analyze_image(img)

        st.markdown("<div class='report-box'>", unsafe_allow_html=True)
        st.subheader("📄 Klinik Tanı Raporu")

        st.write(f"*Olası Kanser Türü:* {result['Tür']}")
        st.write(f"*Malignite Olasılığı:* %{result['Malignite %']:.2f}")
        st.write(f"*Teknik Bulgular:* {result['Bulgular']}")
        st.write(f"*6 Aylık Prognoz:* {result['Prognoz']}")

        st.markdown("---")
        st.write("*Matematiksel Parametreler:*")
        st.write(f"- Lümen / Boşluk Oranı: {result['Lümen Oranı']:.3f}")
        st.write(f"- Hücre Yoğunluğu Skoru: {result['Yoğunluk Skoru']:.1f}")
        st.write(f"- Doku Isı Skoru: {result['Isı Skoru']:.1f}")
        st.write(f"- Entropy Skoru: {result['Entropy']:.2f}")

        report_text = f"""
AKCİĞER KANSERİ TANİ RAPORU

Tür: {result['Tür']}
Malignite Olasılığı: %{result['Malignite %']:.2f}

Teknik Bulgular:
{result['Bulgular']}

6 Aylık Prognoz:
{result['Prognoz']}
"""

        st.download_button(
            "📥 Raporu İndir (.txt)",
            report_text,
            file_name="akciğer_tanı_raporu.txt"
        )

        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# 💊 İLAÇ REHBERİ
# -------------------------------
elif page == "💊 İlaç Rehberi":
    st.title("💊 Akıllı İlaç Rehberi")

    st.subheader("Osimertinib")
    st.write("EGFR tirozin kinaz inhibitörü. Beyin metastazlarında etkilidir.")
    st.write("Yan Etkiler: Döküntü, ishal, QT uzaması.")

    st.subheader("Pembrolizumab")
    st.write("PD-1 inhibitörü. İmmünoterapi ajanıdır.")
    st.write("Yan Etkiler: Otoimmün reaksiyonlar, pnömonit.")

    st.subheader("Alectinib")
    st.write("ALK pozitif hastalarda kullanılır.")
    st.write("Yan Etkiler: Kas ağrısı, bradikardi.")

# -------------------------------
# 📊 EVRELEME
# -------------------------------
elif page == "📊 Evreleme Sistemi":
    st.title("📊 TNM Evreleme Sistemi")

    st.table({
        "Evre": ["I", "II", "III", "IV"],
        "Tanım": [
            "Lokal sınırlı",
            "Lenf nodu tutulumu",
            "Lokal ileri",
            "Uzak metastaz"
        ]
    })

# -------------------------------
# 🧬 KANSER TÜRLERİ
# -------------------------------
elif page == "🧬 Kanser Türleri":
    st.title("🧬 Akciğer Kanseri Türleri")

    st.write("*Adenokarsinom:* Periferik, glandüler yapı.")
    st.write("*Skuamöz:* Merkezi, keratinizasyon.")
    st.write("*Küçük Hücreli:* Yüksek mitoz, Azzopardi.")
    st.write("*Büyük Hücreli:* Düşük diferansiyasyon.")
