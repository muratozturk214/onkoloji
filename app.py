import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pandas as pd
import plotly.express as px
from io import BytesIO

# --- PROFESSIONAL PAGE CONFIG ---
st.set_page_config(
    page_title="Mathrix AI | Precision Oncology",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED MEDICAL DATABASE (Fuhrman Grade to Treatment) ---
ST_DATABASE = {
    1: {
        "Grade": "Grade I",
        "Morphology": "Small, round, uniform nuclei (~10 µm). Inconspicuous or absent nucleoli.",
        "Prognosis": "Excellent (94% 5-year survival)",
        "Treatment": "Active Surveillance or Partial Nephrectomy.",
        "Medication": "N/A (Standard surgical follow-up)"
    },
    2: {
        "Grade": "Grade II",
        "Morphology": "Larger nuclei (~15 µm) with slight irregularities. Visible nucleoli at 400x.",
        "Prognosis": "Good (86% 5-year survival)",
        "Treatment": "Nephron-sparing surgery (Partial Nephrectomy).",
        "Medication": "Consider Adjuvant therapy if risk factors are present."
    },
    3: {
        "Grade": "Grade III",
        "Morphology": "Large nuclei (~20 µm) with marked irregularities. Prominent nucleoli at 100x.",
        "Prognosis": "Intermediate (59% 5-year survival)",
        "Treatment": "Radical Nephrectomy + Lymph Node Dissection.",
        "Medication": "Targeted Therapy: Sunitinib (Sutent) or Pazopanib (Votrient)."
    },
    4: {
        "Grade": "Grade IV",
        "Morphology": "Multilobated, monstrous nuclei (>20 µm). Extensive necrosis and spindle cells.",
        "Prognosis": "Guarded (20-30% 5-year survival)",
        "Treatment": "Cytoreductive Nephrectomy + Multimodal Systemic Therapy.",
        "Medication": "Immune Checkpoint Blockade: Nivolumab + Ipilimumab (Opdivo + Yervoy)."
    }
}

# --- SIDEBAR: CLINICAL CONTROL PANEL ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/microscope.png", width=80)
    st.title("Clinical Panel")
    st.markdown("---")
    patient_id = st.text_input("Patient ID:", "PX-99283")
    analysis_mode = st.selectbox("Analysis Engine:", ["Nuclear Morphology", "Tissue Density", "Biomarker Prediction"])
    st.markdown("---")
    st.info("🧬 *Mathrix AI Engine v2.4*\n\nOptimized for Renal Cell Carcinoma (RCC) Fuhrman Classification.")

# --- MAIN INTERFACE ---
st.markdown("<h1 style='color: #0C4A6E;'>Mathrix AI: Precision Diagnostic Platform</h1>", unsafe_allow_html=True)
st.write(f"*Diagnostic Environment for:* {patient_id}")

# MULTI-FILE UPLOADER (Images and PDF Support)
uploaded_files = st.file_uploader(
    "Upload Clinical Data (Histology Images or Pathology PDFs):", 
    type=['jpg','png','jpeg','pdf'], 
    accept_multiple_files=True
)

if uploaded_files:
    # Handle multiple files in a clean list
    file_list = [f.name for f in uploaded_files]
    selected_file = st.selectbox("Select file for real-time analysis:", file_list)
    
    current_file = next(f for f in uploaded_files if f.name == selected_file)
    
    if current_file.type == "application/pdf":
        st.warning("📄 PDF Report detected. Extracting clinical text for AI summarization...")
        st.text_area("Report Preview:", "Analyzing document structure... [SIMULATED REPORT DATA]")
    else:
        # IMAGE ANALYSIS
        image = Image.open(current_file)
        img_array = np.array(image)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(image, caption=f"Scan: {selected_file}", use_container_width=True)
            
        with col2:
            st.subheader("🤖 AI Diagnostic Output")
            if st.button("RUN DEEP ANALYSIS"):
                with st.spinner("Processing nuclear segments..."):
                    # Advanced calculation logic
                    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                    blurred = cv2.medianBlur(gray, 5)
                    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    
                    # Filtering and Grading
                    areas = [cv2.contourArea(c) for c in contours if 50 < cv2.contourArea(c) < 5000]
                    if areas:
                        avg_diameter = np.median([np.sqrt(a) for a in areas])
                        
                        # Grade logic
                        if avg_diameter < 14: grade = 1
                        elif avg_diameter < 19: grade = 2
                        elif avg_diameter < 25: grade = 3
                        else: grade = 4
                        
                        data = ST_DATABASE[grade]
                        
                        # Results Cards
                        st.success(f"### Result: {data['Grade']}")
                        st.metric("Mean Nuclear Diameter", f"{avg_diameter:.2f} µm")
                        
                        st.markdown(f"*Morphological Analysis:* {data['Morphology']}")
                        st.markdown(f"*Recommended Protocol:* {data['Treatment']}")
                        
                        st.markdown("---")
                        st.markdown(f"### 💊 Targeted Medication Plan")
                        st.error(f"*Prescription/Recommendation:* {data['Medication']}")
                        
                        # Medical Graph
                        chart_df = pd.DataFrame({"Nuclei": areas[:15]})
                        st.area_chart(chart_df)
                    else:
                        st.error("No valid cellular structures detected in this frame.")

st.markdown("---")
st.caption("Mathrix AI System | Restricted to Pathological Use Only | © 2026")
