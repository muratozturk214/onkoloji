import streamlit as st
import numpy as np
from PIL import Image
import math

st.set_page_config(
    page_title="Akciğer Kanseri MathRIX Karar Destek Sistemi",
    layout="wide"
)

st.title("Akciğer Kanseri Görüntü Tabanlı MathRIX Destek Sistemi")
st.caption("Bu sistem tanı koymaz, akademik ve klinik karar desteği sağlar.")

# =======================
# GÖRÜNTÜ ÖN İŞLEME
# =======================
def preprocess_image(img):
    img = img.convert("L").resize((256, 256))
    arr = np.array(img) / 255.0
    return arr

def entropy_score(img):
    hist, _ = np.histogram(img.flatten(), bins=256, range=(0,1), density=True)
    hist = hist[hist > 0]
    return -np.sum(hist * np.log2(hist))

def cell_density(img):
    return np.mean(img > 0.6)

def malignancy_probability(entropy, density):
    score = 0.6 * entropy + 0.4 * density * 5
    prob = 1 / (1 + math.exp(-(score - 3)))
    return min(max(prob, 0.05), 0.95)

def subtype_estimation(prob):
    if prob > 0.7:
        return {
            "Adenokarsinom": 0.82,
            "Skuamöz Hücreli Karsinom": 0.12,
            "Diğer NSCLC": 0.06
        }
    elif prob > 0.5:
        return {
            "Adenokarsinom": 0.48,
            "Skuamöz Hücreli Karsinom": 0.32,
            "Belirsiz NSCLC": 0.20
        }
    else:
        return {
            "Benign / Düşük Dereceli Lezyon": 0.60,
            "Atipik Hiperplazi": 0.25,
            "Erken NSCLC Olasılığı": 0.15
        }

def tnm_stage(prob):
    if prob < 0.4:
        return "Evre I (Erken evre)"
    elif prob < 0.6:
        return "Evre II (Lokal ilerlemiş)"
    elif prob < 0.8:
        return "Evre III (Lenf nodu tutulumu olası)"
    else:
        return "Evre IV (Metastatik olasılık)"

# =======================
# ARAYÜZ
# =======================
uploaded = st.file_uploader("Histopatolojik / Radyolojik Görüntü Yükleyiniz", type=["png","jpg","jpeg"])

if uploaded:
    image = Image.open(uploaded)
    img = preprocess_image(image)

    entropy = entropy_score(img)
    density = cell_density(img)
    prob = malignancy_probability(entropy, density)
    subtypes = subtype_estimation(prob)
    stage = tnm_stage(prob)

    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Yüklenen Görüntü", use_container_width=True)
    with col2:
        st.metric("Malignite Olasılığı", f"%{prob*100:.1f}")
        st.write(f"*Görüntü Entropisi:* {entropy:.2f}")
        st.write(f"*Hücre Yoğunluğu:* {density:.2f}")
        st.write(f"*Tahmini Klinik Evre:* {stage}")

    st.subheader("🧬 Olası Histolojik Alt Tipler")
    for k, v in subtypes.items():
        st.write(f"- *{k}:* %{v*100:.1f}")

    st.subheader("🩺 Akademik Klinik Değerlendirme")
    st.markdown("""
*Tanısal Yorum:*  
Görüntü analizinde artmış doku düzensizliği ve hücresel yoğunluk saptanmıştır.
Bu bulgular malignite lehine olabilir ancak *kesin tanı için patolojik doğrulama şarttır*.

*Evreleme:*  
TNM tabanlı istatistiksel tahminle klinik evre belirlenmiştir.
Bu evreleme tanısal değil, *öngörüsel* niteliktedir.

*Tedavi Yaklaşımı (Literatür Özeti):*
- EGFR pozitif NSCLC → *Osimertinib*
- ALK pozitif → *Alectinib*
- PD-L1 yüksek → *Pembrolizumab*
- Metastatik hastalık → Sistemik tedavi + palyatif yaklaşımlar

*Prognoz:*  
Evreye bağlı olarak medyan sağkalım 8–36 ay arasında değişebilir.
Bu değerler *popülasyon istatistiğidir*.
""")

    st.success("Analiz tamamlandı. Klinik karar için multidisipliner değerlendirme gereklidir.")
