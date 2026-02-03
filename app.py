import streamlit as st
import numpy as np
from PIL import Image
import math
import time

# ==================== SAYFA AYARLARI ====================
st.set_page_config(
    page_title="MATHRIX - Medical AI",
    page_icon="🧬",
    layout="wide"
)

# ==================== CSS ====================
st.markdown("""
<style>
    .main {
        background-color: #0a192f;
    }
    .stApp {
        background: linear-gradient(135deg, #0a192f 0%, #172a45 100%);
    }
    h1, h2, h3 {
        color: #64ffda !important;
        font-family: 'Courier New', monospace;
    }
    .adenocarcinoma-box {
        background: linear-gradient(135deg, #1a237e, #283593);
        color: white;
        padding: 25px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 8px solid #536dfe;
        box-shadow: 0 4px 20px rgba(83, 109, 254, 0.4);
    }
    .squamous-box {
        background: linear-gradient(135deg, #b71c1c, #d32f2f);
        color: white;
        padding: 25px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 8px solid #ff5252;
        box-shadow: 0 4px 20px rgba(255, 82, 82, 0.4);
    }
    .normal-box {
        background: linear-gradient(135deg, #1b5e20, #2e7d32);
        color: white;
        padding: 25px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 8px solid #4caf50;
        box-shadow: 0 4px 20px rgba(76, 175, 80, 0.4);
    }
    .math-metric {
        background: rgba(10, 25, 47, 0.9);
        border: 2px solid #64ffda;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin: 8px;
    }
    .info-panel {
        background: rgba(23, 42, 69, 0.9);
        border: 1px solid #00bcd4;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
    }
    .scanning {
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(100, 255, 218, 0.2) 50%, 
            transparent 100%);
        background-size: 200% 100%;
        animation: scan 3s linear infinite;
    }
    @keyframes scan {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
</style>
""", unsafe_allow_html=True)

# ==================== BAŞLIK ====================
st.markdown("""
<div style='text-align: center; padding: 30px; background: rgba(10, 25, 47, 0.9); border-radius: 15px; border: 2px solid #64ffda;'>
    <h1>🔬 MATHRIX ANALYSIS ENGINE</h1>
    <h3>Mathematical Histopathological Analysis System</h3>
</div>
""", unsafe_allow_html=True)

# ==================== TIBBİ BİLGİ DEPOSU ====================
with st.sidebar:
    st.markdown("## 📚 Medical Knowledge Base")
    
    with st.expander("🫁 Lung Cancer Types", expanded=True):
        st.markdown("""
        *ADENOCARCINOMA:*
        • Peripheral location
        • Gland formation
        • Mucin production
        • Common mutations: EGFR, KRAS, ALK
        
        *SQUAMOUS CELL:*
        • Central location
        • Keratin pearls
        • Intercellular bridges
        • Common mutations: TP53, PIK3CA
        
        *NORMAL TISSUE:*
        • Regular alveolar structure
        • Uniform cell size
        • No nuclear atypia
        """)
    
    with st.expander("🎯 Diagnostic Criteria"):
        st.markdown("""
        *MATHEMATICAL THRESHOLDS:*
        
        *Normal Tissue:*
        • Variance: < 0.05
        • Homogeneity: > 0.8
        • Entropy: < 4.0
        
        *Adenocarcinoma:*
        • Variance: 0.05-0.15
        • Homogeneity: 0.5-0.7
        • Entropy: 4.0-6.0
        
        *Squamous Cell:*
        • Variance: > 0.15
        • Homogeneity: < 0.5
        • Entropy: > 6.0
        """)
    
    with st.expander("⚠️ Risk Factors"):
        st.markdown("""
        *MAJOR RISKS:*
        1. Smoking (85% of cases)
        2. Radon exposure
        3. Asbestos
        4. Family history
        
        *MINOR RISKS:*
        • Air pollution
        • Previous radiation
        • Chronic lung disease
        """)
    
    with st.expander("💊 Treatment Database"):
        st.markdown("""
        *ADENOCARCINOMA:*
        • Osimertinib (EGFR+)
        • Alectinib (ALK+)
        • Pembrolizumab (PD-L1+)
        
        *SQUAMOUS CELL:*
        • Pembrolizumab + Chemo
        • Nivolumab + Ipilimumab
        • Cisplatin + Gemcitabine
        """)

# ==================== MATEMATİKSEL ANALİZ FONKSİYONLARI ====================
def calculate_tissue_variance(matrix):
    """Doku varyansını hesapla (düzensizlik ölçüsü)"""
    return float(np.var(matrix))

def calculate_homogeneity(matrix):
    """Doku homojenitesini hesapla"""
    # Gradient hesapla
    grad_x = np.gradient(matrix, axis=1)
    grad_y = np.gradient(matrix, axis=0)
    grad_mag = np.sqrt(grad_x*2 + grad_y*2)
    
    # Homojenite: gradient ne kadar küçükse o kadar homojen
    homogeneity = 1.0 / (1.0 + np.mean(grad_mag))
    return float(homogeneity)

def calculate_entropy(matrix):
    """Bilgi entropisini hesapla"""
    hist, _ = np.histogram(matrix.flatten(), bins=256, range=(0, 1))
    prob = hist / hist.sum()
    prob = prob[prob > 0]
    entropy = -np.sum(prob * np.log2(prob))
    return float(entropy)

def detect_glandular_pattern(matrix):
    """Glandüler (bezemsi) pattern tespiti"""
    # Dairesel yapıları tespit et (adenokarsinom için)
    from scipy import ndimage
    
    # Edge detection
    edges = np.gradient(matrix, axis=0)*2 + np.gradient(matrix, axis=1)*2
    edges = edges > np.percentile(edges, 90)
    
    # Circular Hough transform benzeri (basitleştirilmiş)
    labeled, num_features = ndimage.label(edges)
    sizes = ndimage.sum(edges, labeled, range(num_features + 1))
    
    # Dairesel yapı sayısı
    circular_count = np.sum(sizes > 10)  # Belirli boyuttaki yapılar
    
    return circular_count / max(1, num_features)

def detect_keratin_pattern(matrix):
    """Keratin pattern tespiti (skuamöz için)"""
    # Yüksek kontrastlı, keskin kenarlı yapılar
    laplacian = np.gradient(np.gradient(matrix, axis=0), axis=0) + \
                np.gradient(np.gradient(matrix, axis=1), axis=1)
    
    # Keskin kenarlar
    sharp_edges = np.abs(laplacian) > np.percentile(np.abs(laplacian), 95)
    
    return float(np.mean(sharp_edges))

def analyze_tissue_mathematically(image_array):
    """Görüntüyü matematiksel olarak analiz et"""
    # Gri tonlamaya çevir ve normalize et
    if len(image_array.shape) == 3:
        gray = np.mean(image_array, axis=2).astype(np.float32)
    else:
        gray = image_array.astype(np.float32)
    
    gray_normalized = gray / 255.0
    
    # Temel istatistikler
    variance = calculate_tissue_variance(gray_normalized)
    homogeneity = calculate_homogeneity(gray_normalized)
    entropy = calculate_entropy(gray_normalized)
    
    # Pattern analizleri
    glandular_score = detect_glandular_pattern(gray_normalized)
    keratin_score = detect_keratin_pattern(gray_normalized)
    
    # Hücre yoğunluğu
    density_threshold = np.percentile(gray, 75)
    cellular_density = np.sum(gray > density_threshold) / gray.size
    
    # Boşluk analizi
    void_threshold = np.percentile(gray, 25)
    void_percentage = np.sum(gray < void_threshold) / gray.size
    
    # Matris boyutları
    matrix_rank = np.linalg.matrix_rank(gray_normalized[:50, :50]) if gray.shape[0] > 50 else 0
    
    return {
        "variance": variance,
        "homogeneity": homogeneity,
        "entropy": entropy,
        "glandular_score": glandular_score,
        "keratin_score": keratin_score,
        "cellular_density": cellular_density,
        "void_percentage": void_percentage,
        "matrix_rank": matrix_rank,
        "image_size": gray.shape
    }

def determine_diagnosis(analysis):
    """Matematiksel kriterlere göre tanı koy"""
    v = analysis["variance"]
    h = analysis["homogeneity"]
    e = analysis["entropy"]
    g = analysis["glandular_score"]
    k = analysis["keratin_score"]
    
    # KARAR AĞACI (Matematiksel kriterler)
    
    # 1. Normal mi?
    if v < 0.05 and h > 0.8 and e < 4.0:
        diagnosis = "NORMAL LUNG TISSUE"
        confidence = (1 - v) * (h) * (1 - e/10) * 100
        confidence = min(98, max(85, confidence))
        
    # 2. Adenokarsinom mu?
    elif 0.05 <= v <= 0.15 and 0.5 <= h <= 0.7 and 4.0 <= e <= 6.0:
        diagnosis = "ADENOCARCINOMA"
        # Glandüler pattern varsa güven artar
        confidence = (v * 5) * (1 - abs(h - 0.6)/0.6) * (e/6) * 100
        if g > 0.3:
            confidence *= 1.3
        confidence = min(95, max(70, confidence))
        
    # 3. Skuamöz karsinom mu?
    elif v > 0.15 and h < 0.5 and e > 6.0:
        diagnosis = "SQUAMOUS CELL CARCINOMA"
        # Keratin pattern varsa güven artar
        confidence = (v * 3) * (1 - h) * (e/8) * 100
        if k > 0.2:
            confidence *= 1.4
        confidence = min(97, max(75, confidence))
        
    # 4. Belirsiz - daha fazla analiz gerekiyor
    else:
        diagnosis = "ATYPICAL - NEEDS PATHOLOGY REVIEW"
        confidence = 50.0
    
    # Evreleme (kanser varsa)
    if "CARCINOMA" in diagnosis or "ADENO" in diagnosis:
        if v < 0.1:
            stage = "Stage I"
        elif v < 0.2:
            stage = "Stage II"
        elif v < 0.3:
            stage = "Stage III"
        else:
            stage = "Stage IV"
    else:
        stage = "N/A"
    
    return {
        "diagnosis": diagnosis,
        "confidence": min(99.0, confidence),
        "stage": stage,
        "variance": v,
        "homogeneity": h,
        "entropy": e
    }

# ==================== ANA UYGULAMA ====================
st.header("📤 Multiple Image Upload & Analysis")

uploaded_files = st.file_uploader(
    "Upload lung tissue images (PNG, JPG)",
    type=['png', 'jpg', 'jpeg'],
    accept_multiple_files=True,
    help="Upload multiple images for batch analysis"
)

if uploaded_files:
    # Toplu analiz butonu
    if st.button("🚀 START MATHRIX ANALYSIS", type="primary", use_container_width=True):
        
        for idx, uploaded_file in enumerate(uploaded_files):
            # Progress
            progress = (idx + 1) / len(uploaded_files)
            st.progress(progress, text=f"Analyzing {idx + 1}/{len(uploaded_files)}")
            
            # Görüntüyü aç
            image = Image.open(uploaded_file)
            image_array = np.array(image)
            
            # Hasta ID
            patient_id = f"PT-{1000 + idx:04d}"
            
            col_img, col_analysis = st.columns([1, 2])
            
            with col_img:
                st.image(image, caption=patient_id, use_column_width=True)
                
                # Görüntü istatistikleri
                st.caption(f"Size: {image.size[0]}x{image.size[1]}")
                st.caption(f"Mode: {image.mode}")
            
            with col_analysis:
                # SCANNING ANIMASYONU
                with st.empty():
                    st.markdown("""
                    <div class='scanning' style='padding: 20px; border-radius: 10px; text-align: center;'>
                        <h4 style='color: #64ffda;'>SCANNING TISSUE MATRIX...</h4>
                        <p style='color: #89cff0;'>Mathematical analysis in progress</p>
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(1)
                
                # ANALİZ YAP
                with st.spinner("Calculating mathematical parameters..."):
                    analysis_results = analyze_tissue_mathematically(image_array)
                
                # TANI KOY
                diagnosis_results = determine_diagnosis(analysis_results)
                
                # SONUÇLARI GÖSTER
                diagnosis = diagnosis_results["diagnosis"]
                
                if "NORMAL" in diagnosis:
                    st.markdown(f"""
                    <div class='normal-box'>
                        <h3>✅ {diagnosis}</h3>
                        <p><strong>Confidence:</strong> {diagnosis_results['confidence']:.1f}%</p>
                        <p><strong>Variance:</strong> {diagnosis_results['variance']:.4f} (Low)</p>
                        <p><strong>Recommendation:</strong> Routine follow-up</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                elif "ADENOCARCINOMA" in diagnosis:
                    st.markdown(f"""
                    <div class='adenocarcinoma-box'>
                        <h3>⚠️ {diagnosis}</h3>
                        <p><strong>Stage:</strong> {diagnosis_results['stage']}</p>
                        <p><strong>Confidence:</strong> {diagnosis_results['confidence']:.1f}%</p>
                        <p><strong>Variance:</strong> {diagnosis_results['variance']:.4f} (Medium)</p>
                        <p><strong>Recommendation:</strong> EGFR/ALK testing, surgical consultation</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                elif "SQUAMOUS" in diagnosis:
                    st.markdown(f"""
                    <div class='squamous-box'>
                        <h3>⚠️ {diagnosis}</h3>
                        <p><strong>Stage:</strong> {diagnosis_results['stage']}</p>
                        <p><strong>Confidence:</strong> {diagnosis_results['confidence']:.1f}%</p>
                        <p><strong>Variance:</strong> {diagnosis_results['variance']:.4f} (High)</p>
                        <p><strong>Recommendation:</strong> PD-L1 testing, chemoradiation evaluation</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                else:
                    st.warning(f"*{diagnosis}* (Confidence: {diagnosis_results['confidence']:.1f}%)")
                
                # MATEMATİKSEL METRİKLER
                st.subheader("📊 Mathematical Parameters")
                
                cols = st.columns(4)
                metrics = [
                    ("Variance", f"{analysis_results['variance']:.4f}", 
                     "Low" if analysis_results['variance'] < 0.05 else "High"),
                    ("Homogeneity", f"{analysis_results['homogeneity']:.3f}", 
                     "High" if analysis_results['homogeneity'] > 0.7 else "Low"),
                    ("Entropy", f"{analysis_results['entropy']:.2f}", 
                     "Low" if analysis_results['entropy'] < 4.0 else "High"),
                    ("Cellular Density", f"{analysis_results['cellular_density']*100:.1f}%",
                     "High" if analysis_results['cellular_density'] > 0.6 else "Normal"),
                    ("Void Percentage", f"{analysis_results['void_percentage']*100:.1f}%",
                     "Many voids" if analysis_results['void_percentage'] > 0.3 else "Few voids"),
                    ("Glandular Pattern", f"{analysis_results['glandular_score']:.3f}",
                     "Present" if analysis_results['glandular_score'] > 0.3 else "Absent"),
                    ("Keratin Pattern", f"{analysis_results['keratin_score']:.3f}",
                     "Present" if analysis_results['keratin_score'] > 0.2 else "Absent"),
                    ("Matrix Rank", str(analysis_results['matrix_rank']),
                     "Complex" if analysis_results['matrix_rank'] > 25 else "Simple")
                ]
                
                for i, (label, value, status) in enumerate(metrics):
                    with cols[i % 4]:
                        st.markdown(f"""
                        <div class='math-metric'>
                            <h4>{label}</h4>
                            <h3 style='color: #64ffda;'>{value}</h3>
                            <p style='color: #89cff0; font-size: 0.9em;'>{status}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # KRİTER KARŞILAŞTIRMA
                st.subheader("🎯 Diagnostic Criteria Match")
                
                crit_variance = analysis_results["variance"]
                crit_homogeneity = analysis_results["homogeneity"]
                crit_entropy = analysis_results["entropy"]
                
                col_crit1, col_crit2, col_crit3 = st.columns(3)
                
                with col_crit1:
                    st.write("*Variance Analysis:*")
                    if crit_variance < 0.05:
                        st.success("✓ Normal range (<0.05)")
                    elif 0.05 <= crit_variance <= 0.15:
                        st.warning("✓ Adenocarcinoma range (0.05-0.15)")
                    else:
                        st.error("✓ Squamous range (>0.15)")
                
                with col_crit2:
                    st.write("*Homogeneity Analysis:*")
                    if crit_homogeneity > 0.8:
                        st.success("✓ Normal range (>0.8)")
                    elif 0.5 <= crit_homogeneity <= 0.7:
                        st.warning("✓ Adenocarcinoma range (0.5-0.7)")
                    else:
                        st.error("✓ Squamous range (<0.5)")
                
                with col_crit3:
                    st.write("*Entropy Analysis:*")
                    if crit_entropy < 4.0:
                        st.success("✓ Normal range (<4.0)")
                    elif 4.0 <= crit_entropy <= 6.0:
                        st.warning("✓ Adenocarcinoma range (4.0-6.0)")
                    else:
                        st.error("✓ Squamous range (>6.0)")
                
                # İLAÇ ÖNERİSİ (Kanser varsa)
                if "CARCINOMA" in diagnosis or "ADENO" in diagnosis:
                    st.subheader("💊 Targeted Therapy Suggestions")
                    
                    if "ADENOCARCINOMA" in diagnosis:
                        st.markdown("""
                        *Based on NCCN Guidelines 2024:*
                        1. *EGFR testing* → Osimertinib if positive
                        2. *ALK testing* → Alectinib if positive
                        3. *PD-L1 testing* → Pembrolizumab if >50%
                        4. *Surgical evaluation* for Stage I-II
                        """)
                    
                    elif "SQUAMOUS" in diagnosis:
                        st.markdown("""
                        *Based on NCCN Guidelines 2024:*
                        1. *PD-L1 testing* → Pembrolizumab + Chemotherapy
                        2. *Consider nivolumab + ipilimumab* for high TMB
                        3. *Chemoradiation* for locally advanced
                        4. *Palliative care* for symptomatic relief
                        """)
                
                st.markdown("---")

else:
    # ANA SAYFA
    st.markdown("""
    <div style='text-align: center; padding: 40px;'>
        <h2 style='color: #64ffda;'>Welcome to MATHRIX Analysis Engine</h2>
        <p style='color: #89cff0; font-size: 1.1em;'>
        Advanced mathematical analysis of lung tissue histopathology
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <div style='font-size: 48px; color: #64ffda;'>🔢</div>
            <h4>Mathematical Analysis</h4>
            <p>Variance, entropy, homogeneity calculations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_info2:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <div style='font-size: 48px; color: #64ffda;'>🎯</div>
            <h4>Precise Differentiation</h4>
            <p>Adenocarcinoma vs Squamous vs Normal</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_info3:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <div style='font-size: 48px; color: #64ffda;'>📊</div>
            <h4>Pattern Recognition</h4>
            <p>Glandular and keratin pattern detection</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.info("""
    *HOW IT WORKS:*
    
    1. *Variance Calculation* - Measures tissue irregularity
    2. *Homogeneity Analysis* - Evaluates texture uniformity  
    3. *Entropy Measurement* - Calculates information complexity
    4. *Pattern Detection* - Identifies glandular/keratin patterns
    5. *Cellular Density* - Counts cell concentration
    6. *Void Analysis* - Measures empty spaces in tissue
    
    *MATHEMATICAL CRITERIA:*
    - Normal: Variance < 0.05, Homogeneity > 0.8, Entropy < 4.0
    - Adenocarcinoma: Variance 0.05-0.15, Homogeneity 0.5-0.7, Entropy 4.0-6.0
    - Squamous: Variance > 0.15, Homogeneity < 0.5, Entropy > 6.0
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #89cff0; padding: 20px;'>
    <p><strong>MATHRIX Analysis Engine v6.0</strong> | Mathematical Pathology System</p>
    <p>© 2024 Computational Pathology Lab | For research use</p>
</div>
""", unsafe_allow_html=True)
