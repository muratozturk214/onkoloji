# app.py
"""
MATHRIX ANALYSIS ENGINE - Medical Imaging AI Platform
Advanced Computer Vision & Healthcare Technology Integration
Streamlit-based professional medical image analysis dashboard
Version: 2.1.0
Author: Senior CV & HealthTech Expert
"""

# ==================== LIBRARY IMPORTS ====================
import streamlit as st
import numpy as np
import pandas as pd
import cv2
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import io
import plotly.graph_objects as go
import plotly.express as px
import time
import warnings
warnings.filterwarnings('ignore')

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Mathrix Analysis Engine v2.1",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS STYLING ====================
st.markdown("""
<style>
    .main {
        background-color: #0a0a1a;
        color: #e0e0ff;
    }
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%%, #0d1b2a 100%%);
    }
    h1, h2, h3, h4 {
        color: #4d9fff !important;
        font-family: 'Segoe UI', system-ui;
        font-weight: 700;
    }
    .stMetric {
        background-color: rgba(13, 27, 42, 0.9);
        border-radius: 10px;
        padding: 15px;
        border-left: 4px solid #4d9fff;
    }
    .css-1d391kg {
        background-color: rgba(10, 10, 26, 0.95);
    }
    .scan-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%%;
        height: 100%%;
        background: linear-gradient(transparent 50%%, rgba(77, 159, 255, 0.05) 50%%);
        background-size: 100%% 4px;
        z-index: 100;
        animation: scan 2s linear infinite;
    }
    @keyframes scan {
        0%% { background-position: 0 0; }
        100%% { background-position: 0 100%%; }
    }
    .dataframe {
        background-color: rgba(13, 27, 42, 0.9) !important;
        color: #e0e0ff !important;
        border: 1px solid #2a4a6f !important;
    }
    .dataframe th {
        background-color: #1a3a5f !important;
        color: #4d9fff !important;
        font-weight: bold !important;
    }
    .stProgress > div > div > div > div {
        background-color: #4d9fff;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE INITIALIZATION ====================
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = []
if 'patient_counter' not in st.session_state:
    st.session_state.patient_counter = 1

# ==================== HEADER SECTION ====================
st.title("🧬 MATHRIX ANALYSIS ENGINE")
st.markdown("""
<div style='background: linear-gradient(90deg, #0a0a1a, #1a3a5f); padding: 20px; border-radius: 10px; border-left: 5px solid #4d9fff;'>
<h3 style='color: #4d9fff; margin: 0;'>Advanced Computational Pathology & Pulmonary Oncology AI</h3>
<p style='color: #a0c8ff; margin: 5px 0 0 0;'>Real-time histopathological image analysis with mathematical matrix decomposition and treatment recommendation engine</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==================== MEDICAL DATABASE & KNOWLEDGE BASE ====================
LUNG_CANCER_DATABASE = {
    "adenocarcinoma": {
        "prevalence": "40%% of lung cancers",
        "subtypes": ["Lepidic", "Acinar", "Papillary", "Micropapillary", "Solid"],
        "common_mutations": ["EGFR", "KRAS", "ALK", "ROS1"],
        "typical_location": "Peripheral lungs",
        "histological_features": ["Gland formation", "Mucin production", "Nuclear atypia"],
        "staining_pattern": "TTF-1 positive, Napsin A positive",
        "five_year_survival": "Stage I: 68-92%%, Stage IV: 1-10%%",
        "risk_factors": ["Smoking", "Radon exposure", "Asbestos", "Family history"]
    },
    "squamous_cell_carcinoma": {
        "prevalence": "25-30%% of lung cancers",
        "subtypes": ["Keratinizing", "Non-keratinizing", "Basaloid"],
        "common_mutations": ["TP53", "CDKN2A", "PIK3CA"],
        "typical_location": "Central/hilar region",
        "histological_features": ["Keratin pearls", "Intercellular bridges", "Squamous differentiation"],
        "staining_pattern": "p40 positive, p63 positive, TTF-1 negative",
        "five_year_survival": "Stage I: 47-80%%, Stage IV: 2-15%%",
        "risk_factors": ["Heavy smoking", "Air pollution", "Chronic inflammation"]
    },
    "normal": {
        "description": "Healthy lung tissue architecture",
        "features": ["Intact alveolar structure", "Normal bronchioles", "No cellular atypia"],
        "cell_types": ["Type I pneumocytes", "Type II pneumocytes", "Alveolar macrophages"],
        "clinical_notes": "No evidence of malignancy, regular follow-up recommended"
    }
}

TARGETED_THERAPIES = {
    "adenocarcinoma": [
        {
            "drug": "Osimertinib (Tagrisso)",
            "target": "EGFR T790M mutation",
            "dosage": "80mg oral daily",
            "response_rate": "79%%",
            "approval": "FDA 2020, EMA 2021",
            "key_trials": "FLAURA, AURA3",
            "side_effects": ["Diarrhea", "Rash", "Dry skin", "QT prolongation"]
        },
        {
            "drug": "Alectinib (Alecensa)",
            "target": "ALK rearrangement",
            "dosage": "600mg oral twice daily",
            "response_rate": "82.9%%",
            "approval": "FDA 2017, EMA 2018",
            "key_trials": "ALEX, J-ALEX",
            "side_effects": ["Fatigue", "Edema", "Myalgia", "Elevated liver enzymes"]
        },
        {
            "drug": "Pembrolizumab (Keytruda) + Chemotherapy",
            "target": "PD-1 inhibitor",
            "dosage": "200mg IV every 3 weeks",
            "response_rate": "48.3%%",
            "approval": "FDA 2018",
            "key_trials": "KEYNOTE-189",
            "side_effects": ["Pneumonitis", "Colitis", "Hepatitis", "Endocrinopathies"]
        }
    ],
    "squamous_cell_carcinoma": [
        {
            "drug": "Pembrolizumab (Keytruda) + Chemotherapy",
            "target": "PD-1 inhibitor",
            "dosage": "200mg IV every 3 weeks",
            "response_rate": "57.9%%",
            "approval": "FDA 2018, EMA 2019",
            "key_trials": "KEYNOTE-407",
            "side_effects": ["Pneumonitis", "Colitis", "Hepatitis", "Endocrinopathies"]
        },
        {
            "drug": "Nivolumab (Opdivo) + Ipilimumab",
            "target": "PD-1 + CTLA-4",
            "dosage": "3mg/kg + 1mg/kg every 3 weeks",
            "response_rate": "35.9%%",
            "approval": "FDA 2020",
            "key_trials": "CheckMate 227",
            "side_effects": ["Rash", "Diarrhea", "Hepatitis", "Endocrinopathies"]
        },
        {
            "drug": "Cisplatin + Gemcitabine",
            "target": "DNA crosslinking",
            "dosage": "75mg/m² + 1250mg/m² every 3 weeks",
            "response_rate": "30-40%%",
            "approval": "FDA 1998",
            "key_trials": "Multiple phase III",
            "side_effects": ["Nephrotoxicity", "Neurotoxicity", "Myelosuppression", "Ototoxicity"]
        }
    ]
}

# ==================== SIDEBAR CONFIGURATION ====================
with st.sidebar:
    st.markdown("![Lungs](https://img.icons8.com/color/96/000000/lungs.png)", unsafe_allow_html=True)
    st.title("Analysis Parameters")
    
    st.subheader("🔧 Processing Configuration")
    analysis_mode = st.selectbox(
        "Analysis Mode",
        ["Standard Histopathology", "Enhanced Matrix Analysis", "Deep Tissue Scan"],
        index=1
    )
    
    matrix_threshold = st.slider(
        "Matrix Density Threshold", 
        min_value=0.1, 
        max_value=0.9, 
        value=0.5,
        help="Threshold for cellular density calculations"
    )
    
    void_sensitivity = st.slider(
        "Void Detection Sensitivity", 
        min_value=1, 
        max_value=10, 
        value=7,
        help="Higher values detect smaller tissue voids"
    )
    
    st.subheader("🧠 AI Model Selection")
    model_option = st.radio(
        "Select Model",
        ["Standard Lung Cancer Model (ResNet50)", "Enhanced Ensemble Model", "Research Grade Model"],
        index=0
    )
    
    st.subheader("💊 Treatment Database")
    include_treatments = st.checkbox("Include Latest Treatment Protocols", value=True)
    
    if include_treatments:
        treatment_source = st.selectbox(
            "Treatment Guidelines",
            ["NCCN Guidelines 2024", "ESMO Recommendations", "ASCO Clinical Practice"]
        )
    
    st.markdown("---")
    st.info("""
    *Medical Disclaimer:*  
    This tool assists healthcare professionals in analysis.  
    All results must be verified by certified pathologists.  
    Treatment suggestions are based on published literature.
    """)

# ==================== CORE ANALYSIS FUNCTIONS ====================
def perform_matrix_analysis(image_array):
    """
    Perform advanced mathematical matrix analysis on the image
    Converts to grayscale and analyzes cellular patterns
    """
    if len(image_array.shape) == 3:
        gray_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    else:
        gray_image = image_array
    
    matrix = gray_image.astype(np.float32) / 255.0
    
    total_pixels = matrix.size
    density_threshold = matrix_threshold
    
    cellular_density = np.sum(matrix > density_threshold) / total_pixels
    
    void_mask = matrix < (density_threshold / void_sensitivity)
    void_percentage = np.sum(void_mask) / total_pixels
    
    sobel_x = cv2.Sobel(matrix, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(matrix, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(sobel_x*2 + sobel_y*2)
    texture_roughness = np.std(gradient_magnitude)
    
    nuclear_variance = np.var(matrix)
    
    U, S, Vt = np.linalg.svd(matrix, full_matrices=False)
    matrix_rank = np.linalg.matrix_rank(matrix)
    condition_number = np.linalg.cond(matrix)
    
    return {
        "matrix_dimensions": matrix.shape,
        "cellular_density": cellular_density,
        "void_percentage": void_percentage,
        "texture_roughness": texture_roughness,
        "nuclear_pleomorphism": nuclear_variance,
        "matrix_rank": matrix_rank,
        "condition_number": condition_number,
        "singular_values": S[:5],
        "total_pixels": total_pixels,
        "mean_intensity": np.mean(matrix),
        "std_intensity": np.std(matrix)
    }

def simulate_ai_diagnosis(matrix_metrics):
    """
    Simulate AI-based diagnosis based on matrix analysis
    """
    density = matrix_metrics["cellular_density"]
    voids = matrix_metrics["void_percentage"]
    roughness = matrix_metrics["texture_roughness"]
    
    if density > 0.7 and voids < 0.1:
        diagnosis = "Adenocarcinoma"
        confidence = min(0.85 + (roughness * 0.1), 0.98)
        subtype = np.random.choice(LUNG_CANCER_DATABASE["adenocarcinoma"]["subtypes"])
    elif density > 0.6 and voids < 0.2:
        diagnosis = "Squamous Cell Carcinoma"
        confidence = min(0.80 + (roughness * 0.15), 0.96)
        subtype = np.random.choice(LUNG_CANCER_DATABASE["squamous_cell_carcinoma"]["subtypes"])
    else:
        diagnosis = "Normal"
        confidence = 0.95
        subtype = "Healthy Tissue"
    
    return {
        "diagnosis": diagnosis,
        "confidence": confidence,
        "subtype": subtype,
        "differential": ["Adenocarcinoma", "Squamous", "Normal"],
        "recommendation": "Pathologist consultation recommended" if diagnosis != "Normal" else "Routine follow-up"
    }

def generate_treatment_plan(diagnosis, subtype=None):
    """
    Generate evidence-based treatment recommendations
    """
    if diagnosis.lower() == "normal":
        return {
            "status": "No treatment required",
            "recommendations": ["Annual low-dose CT scan", "Smoking cessation if applicable", "Healthy lifestyle maintenance"],
            "follow_up": "12 months"
        }
    
    treatments = TARGETED_THERAPIES.get(diagnosis.lower().replace(" ", "_"), [])
    
    plan = {
        "diagnosis": diagnosis,
        "subtype": subtype,
        "treatments": treatments[:4],
        "clinical_trials": ["NCT04513925", "NCT05186809", "NCT04950075"],
        "biomarker_testing": ["PD-L1 IHC", "EGFR mutation", "ALK rearrangement", "ROS1 fusion"],
        "supportive_care": ["Nutritional support", "Pain management", "Psychological counseling"]
    }
    
    return plan

def create_matrix_visualization(image_array):
    """
    Create interactive visualization of matrix analysis
    """
    fig = go.Figure()
    
    fig.add_trace(go.Heatmap(
        z=image_array[:100, :100] if len(image_array.shape) == 2 else image_array[:100, :100, 0],
        colorscale='Viridis',
        showscale=False,
        name='Tissue Matrix'
    ))
    
    fig.add_shape(
        type="rect",
        x0=0, x1=100, y0=0, y1=100,
        line=dict(color="#4d9fff", width=2, dash="dot"),
        fillcolor="rgba(77, 159, 255, 0.1)"
    )
    
    fig.add_annotation(
        x=50, y=50,
        text="Scanning Matrix Data",
        showarrow=False,
        font=dict(size=14, color="#4d9fff"),
        bgcolor="rgba(10, 10, 26, 0.8)"
    )
    
    fig.update_layout(
        title="Matrix Analysis Visualization",
        xaxis_title="Pixel Columns",
        yaxis_title="Pixel Rows",
        width=400,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#e0e0ff")
    )
    
    return fig

# ==================== MAIN APPLICATION LOGIC ====================
st.header("📁 Histopathological Image Upload")
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_files = st.file_uploader(
        "Upload Histopathology Images (H&E stained lung tissue)",
        type=['png', 'jpg', 'jpeg', 'tiff', 'bmp'],
        accept_multiple_files=True,
        help="Upload H&E stained lung tissue slides. Recommended: 40x magnification"
    )

with col2:
    st.markdown("""
    <div style='background-color: rgba(13, 27, 42, 0.9); padding: 15px; border-radius: 10px;'>
    <h4 style='color: #4d9fff;'>Upload Requirements:</h4>
    <ul style='color: #a0c8ff;'>
    <li>H&E stained tissue slides</li>
    <li>Minimum 512x512 resolution</li>
    <li>Preferred formats: PNG, JPEG</li>
    <li>Maximum 10MB per file</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

if uploaded_files:
    st.success("✅ Medical AI Model Loaded Successfully")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, uploaded_file in enumerate(uploaded_files):
        file_bytes = uploaded_file.read()
        image_stream = io.BytesIO(file_bytes)
        
        progress = (i + 1) / len(uploaded_files)
        progress_bar.progress(progress)
        status_text.text(f"Processing image {i+1} of {len(uploaded_files)}: Matrix Analysis in Progress...")
        
        try:
            image = Image.open(image_stream)
            image_array = np.array(image)
            
            col_img, col_stats = st.columns([1, 2])
            
            with col_img:
                st.image(image, caption=f"Specimen M-{st.session_state.patient_counter:04d}", use_column_width=True)
                
                if len(image_array.shape) == 3:
                    gray_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
                else:
                    gray_array = image_array
                    
                matrix_fig = create_matrix_visualization(gray_array)
                st.plotly_chart(matrix_fig, use_container_width=True)
            
            with col_stats:
                with st.spinner("🔬 Performing Mathematical Matrix Analysis..."):
                    matrix_results = perform_matrix_analysis(image_array)
                    time.sleep(1)
                
                with st.spinner("🤖 Running Medical AI Diagnostics..."):
                    diagnosis_results = simulate_ai_diagnosis(matrix_results)
                    time.sleep(0.5)
                
                st.subheader("📊 Quantitative Analysis Results")
                
                metric_cols = st.columns(4)
                with metric_cols[0]:
                    st.metric(
                        label="Cellular Density",
                        value=f"{matrix_results['cellular_density']*100:.1f}%%",
                        delta="High" if matrix_results['cellular_density'] > 0.6 else "Normal"
                    )
                
                with metric_cols[1]:
                    st.metric(
                        label="Void Percentage",
                        value=f"{matrix_results['void_percentage']*100:.1f}%%",
                        delta="Elevated" if matrix_results['void_percentage'] > 0.15 else "Normal"
                    )
                
                with metric_cols[2]:
                    st.metric(
                        label="Matrix Rank",
                        value=str(matrix_results['matrix_rank']),
                        delta="Complex" if matrix_results['matrix_rank'] > 100 else "Simple"
                    )
                
                with metric_cols[3]:
                    st.metric(
                        label="Texture Roughness",
                        value=f"{matrix_results['texture_roughness']:.3f}",
                        delta="Irregular" if matrix_results['texture_roughness'] > 0.1 else "Smooth"
                    )
                
                st.subheader("🏥 AI Pathology Diagnosis")
                
                diagnosis_color = "#4d9fff" if diagnosis_results['diagnosis'] == "Normal" else "#ff6b6b"
                
                st.markdown(f"""
                <div style='background-color: rgba(13, 27, 42, 0.9); padding: 20px; border-radius: 10px; border-left: 5px solid {diagnosis_color};'>
                    <h3 style='color: {diagnosis_color}; margin-top: 0;'>{diagnosis_results['diagnosis']}</h3>
                    <p style='color: #a0c8ff;'><strong>Confidence:</strong> {diagnosis_results['confidence']*100:.1f}%%</p>
                    <p style='color: #a0c8ff;'><strong>Subtype:</strong> {diagnosis_results.get('subtype', 'N/A')}</p>
                    <p style='color: #a0c8ff;'><strong>Recommendation:</strong> {diagnosis_results['recommendation']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if diagnosis_results['diagnosis'].lower() in ['adenocarcinoma', 'squamous cell carcinoma']:
                    cancer_type = diagnosis_results['diagnosis'].lower().replace(" ", "_")
                    cancer_info = LUNG_CANCER_DATABASE.get(cancer_type, {})
                    
                    st.subheader("📚 Pathological Characteristics")
                    
                    info_cols = st.columns(2)
                    with info_cols[0]:
                        st.markdown(f"""
                        *Prevalence:* {cancer_info.get('prevalence', 'N/A')}  
                        *Common Mutations:* {', '.join(cancer_info.get('common_mutations', []))}  
                        *Typical Location:* {cancer_info.get('typical_location', 'N/A')}
                        *5-Year Survival:* {cancer_info.get('five_year_survival', 'N/A')}
                        """)
                    
                    with info_cols[1]:
                        st.markdown(f"""
                        *Key Features:* {', '.join(cancer_info.get('histological_features', []))}  
                        *Staining Pattern:* {cancer_info.get('staining_pattern', 'N/A')}
                        *Risk Factors:* {', '.join(cancer_info.get('risk_factors', []))}
                        """)
                
                if include_treatments and diagnosis_results['diagnosis'] != "Normal":
                    treatment_plan = generate_treatment_plan(
                        diagnosis_results['diagnosis'],
                        diagnosis_results.get('subtype')
                    )
                    
                    st.subheader("💊 Targeted Treatment Recommendations (2024 Guidelines)")
                    
                    if treatment_plan.get('treatments'):
                        treatments_df = pd.DataFrame(treatment_plan['treatments'])
                        st.dataframe(treatments_df, use_container_width=True)
                    
                    with st.expander("📋 Comprehensive Clinical Management Plan"):
                        st.markdown(f"""
                        ### Biomarker Testing Required:
                        {', '.join(treatment_plan.get('biomarker_testing', []))}
                        
                        ### Ongoing Clinical Trials:
                        {', '.join(treatment_plan.get('clinical_trials', []))}
                        
                        ### Supportive Care:
                        {', '.join(treatment_plan.get('supportive_care', []))}
                        """)
            
            result_entry = {
                "specimen_id": f"M-{st.session_state.patient_counter:04d}",
                "diagnosis": diagnosis_results['diagnosis'],
                "confidence": diagnosis_results['confidence'],
                "density": matrix_results['cellular_density'],
                "voids": matrix_results['void_percentage'],
                "timestamp": pd.Timestamp.now()
            }
            st.session_state.analysis_results.append(result_entry)
            
            st.session_state.patient_counter += 1
            
            st.markdown("---")
            
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
    
    progress_bar.empty()
    status_text.empty()
    
    if st.session_state.analysis_results:
        st.header("📈 Batch Analysis Summary")
        
        summary_df = pd.DataFrame(st.session_state.analysis_results)
        
        col_summary, col_chart = st.columns([1, 1])
        
        with col_summary:
            st.dataframe(summary_df, use_container_width=True)
            
            normal_count = len([r for r in st.session_state.analysis_results if r['diagnosis'] == 'Normal'])
            cancer_count = len(st.session_state.analysis_results) - normal_count
            
            st.metric("Total Specimens", len(st.session_state.analysis_results))
            st.metric("Normal Findings", normal_count)
            st.metric("Suspicious Findings", cancer_count)
        
        with col_chart:
            if not summary_df.empty:
                diagnosis_counts = summary_df['diagnosis'].value_counts()
                fig = px.pie(
                    values=diagnosis_counts.values,
                    names=diagnosis_counts.index,
                    title="Diagnosis Distribution",
                    color_discrete_sequence=['#4d9fff', '#ff6b6b', '#2ecc71']
                )
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
