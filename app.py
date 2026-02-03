import streamlit as st
import numpy as np
from PIL import Image
import time

# ==================== SAYFA AYARLARI ====================
st.set_page_config(
    page_title="MATHRIX - Medical AI",
    page_icon="🧬",
    layout="wide"
)

# ==================== CSS - YAZILAR GÖRÜNSÜN DİYE ====================
st.markdown("""
<style>
    /* Ana arka plan */
    .main {
        background-color: #0a192f;
    }
    
    /* Tüm yazılar beyaz olsun */
    .stApp {
        background: linear-gradient(135deg, #0a192f 0%, #172a45 100%);
        color: #ffffff !important;
    }
    
    /* Streamlit'in varsayılan yazı rengi */
    p, div, span, label {
        color: #ffffff !important;
    }
    
    /* Başlıklar */
    h1, h2, h3, h4 {
        color: #64ffda !important;
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }
    
    /* Metric kartları */
    .stMetric {
        background-color: rgba(23, 42, 69, 0.9) !important;
        color: white !important;
    }
    
    .stMetric label {
        color: #89cff0 !important;
    }
    
    .stMetric div {
        color: #64ffda !important;
        font-size: 24px !important;
    }
    
    /* Adenokarsinom kutusu */
    .adenocarcinoma-box {
        background: linear-gradient(135deg, #1a237e, #283593);
        color: white !important;
        padding: 25px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 8px solid #536dfe;
        box-shadow: 0 4px 20px rgba(83, 109, 254, 0.4);
    }
    
    /* Skuamöz kutusu */
    .squamous-box {
        background: linear-gradient(135deg, #b71c1c, #d32f2f);
        color: white !important;
        padding: 25px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 8px solid #ff5252;
        box-shadow: 0 4px 20px rgba(255, 82, 82, 0.4);
    }
    
    /* Normal kutusu */
    .normal-box {
        background: linear-gradient(135deg, #1b5e20, #2e7d32);
        color: white !important;
        padding: 25px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 8px solid #4caf50;
        box-shadow: 0 4px 20px rgba(76, 175, 80, 0.4);
    }
    
    /* Matematik metrikleri */
    .math-metric {
        background: rgba(10, 25, 47, 0.9);
        border: 2px solid #64ffda;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin: 8px;
        color: white !important;
    }
    
    .math-metric h4 {
        color: #89cff0 !important;
        font-size: 14px;
        margin-bottom: 5px;
    }
    
    .math-metric h3 {
        color: #64ffda !important;
        font-size: 20px;
        margin: 5px 0;
    }
    
    /* Sidebar yazıları */
    .css-1d391kg {
        background-color: #0a192f !important;
    }
    
    .css-1d391kg p, 
    .css-1d391kg div,
    .css-1d391kg span {
        color: #ffffff !important;
    }
    
    /* File uploader */
    .stFileUploader {
        background-color: rgba(23, 42, 69, 0.9) !important;
        border: 2px dashed #64ffda !important;
        border-radius: 10px !important;
    }
    
    /* Butonlar */
    .stButton button {
        background: linear-gradient(90deg, #0066cc, #0099ff) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: #64ffda !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: rgba(23, 42, 69, 0.9) !important;
        color: #64ffda !important;
        font-weight: bold !important;
    }
    
    /* Tablo */
    .dataframe {
        background-color: rgba(23, 42, 69, 0.9) !important;
        color: white !important;
    }
    
    .dataframe th {
        background-color: #1a237e !important;
        color: #64ffda !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== BAŞLIK ====================
st.markdown("""
<div style='text-align: center; padding: 30px; background: rgba(10, 25, 47, 0.9); border-radius: 15px; border: 2px solid #64ffda;'>
    <h1 style='color: #64ffda !important;'>🔬 MATHRIX ANALYSIS ENGINE</h1>
    <h3 style='color: #89cff0 !important;'>Mathematical Histopathological Analysis System</h3>
    <p style='color: #b0e0e6 !important;'>Advanced computational pathology for lung cancer detection</p>
</div>
""", unsafe_allow_html=True)

# ==================== YAN ÇUBUK - BİLGİ DEPOSU ====================
with st.sidebar:
    st.markdown("## 📚 Medical Knowledge Base")
    
    with st.expander("🫁 Lung Cancer Types", expanded=True):
        st.markdown("""
        <div style='color: white !important;'>
        <p><strong style='color: #536dfe !important;'>ADENOCARCINOMA:</strong></p>
        <ul>
        <li>Peripheral location</li>
        <li>Gland formation</li>
        <li>Mucin production</li>
        <li>Common mutations: EGFR, KRAS, ALK</li>
        </ul>
        
        <p><strong style='color: #ff5252 !important;'>SQUAMOUS CELL:</strong></p>
        <ul>
        <li>Central location</li>
        <li>Keratin pearls</li>
        <li>Intercellular bridges</li>
        <li>Common mutations: TP53, PIK3CA</li>
        </ul>
        
        <p><strong style='color: #4caf50 !important;'>NORMAL TISSUE:</strong></p>
        <ul>
        <li>Regular alveolar structure</li>
        <li>Uniform cell size</li>
        <li>No nuclear atypia</li>
        <li>No mitosis</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("🎯 Diagnostic Criteria"):
        st.markdown("""
        <div style='color: white !important;'>
        <p><strong>MATHEMATICAL THRESHOLDS:</strong></p>
        
        <p style='color: #4caf50 !important;'><strong>Normal Tissue:</strong></p>
        <ul>
        <li>Variance: < 0.05</li>
        <li>Homogeneity: > 0.8</li>
        <li>Entropy: < 4.0</li>
        </ul>
        
        <p style='color: #536dfe !important;'><strong>Adenocarcinoma:</strong></p>
        <ul>
        <li>Variance: 0.05-0.15</li>
        <li>Homogeneity: 0.5-0.7</li>
        <li>Entropy: 4.0-6.0</li>
        </ul>
        
        <p style='color: #ff5252 !important;'><strong>Squamous Cell:</strong></p>
        <ul>
        <li>Variance: > 0.15</li>
        <li>Homogeneity: < 0.5</li>
        <li>Entropy: > 6.0</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("⚠️ Risk Factors"):
        st.markdown("""
        <div style='color: white !important;'>
        <p><strong>MAJOR RISKS:</strong></p>
        <ol>
        <li>Smoking (85% of cases)</li>
        <li>Radon exposure</li>
        <li>Asbestos</li>
        <li>Family history</li>
        </ol>
        
        <p><strong>MINOR RISKS:</strong></p>
        <ul>
        <li>Air pollution</li>
        <li>Previous radiation</li>
        <li>Chronic lung disease</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("💊 Treatment Database"):
        st.markdown("""
        <div style='color: white !important;'>
        <p style='color: #536dfe !important;'><strong>ADENOCARCINOMA:</strong></p>
        <ul>
        <li>Osimertinib (EGFR+)</li>
        <li>Alectinib (ALK+)</li>
        <li>Pembrolizumab (PD-L1+)</li>
        <li>Surgery for early stage</li>
        </ul>
        
        <p style='color: #ff5252 !important;'><strong>SQUAMOUS CELL:</strong></p>
        <ul>
        <li>Pembrolizumab + Chemo</li>
        <li>Nivolumab + Ipilimumab</li>
        <li>Cisplatin + Gemcitabine</li>
        <li>Radiation therapy</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# ==================== MATEMATİKSEL ANALİZ FONKSİYONLARI (SCIPY OLMADAN) ====================
def calculate_tissue_variance(matrix):
    """Doku varyansını hesapla"""
    return float(np.var(matrix))

def calculate_homogeneity(matrix):
    """Doku homojenitesini hesapla"""
    # Gradient hesapla (numpy ile)
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

def detect_circular_patterns(matrix):
    """Dairesel pattern tespiti (adenokarsinom için) - scipy olmadan"""
    # Edge detection (basit gradient)
    edges = np.gradient(matrix, axis=0)*2 + np.gradient(matrix, axis=1)*2
    edge_threshold = np.percentile(edges, 90)
    binary_edges = edges > edge_threshold
    
    # Connected components (basit versiyon)
    visited = np.zeros_like(binary_edges, dtype=bool)
    components = []
    
    def dfs(i, j, component):
        stack = [(i, j)]
        while stack:
            x, y = stack.pop()
            if 0 <= x < binary_edges.shape[0] and 0 <= y < binary_edges.shape[1]:
                if binary_edges[x, y] and not visited[x, y]:
                    visited[x, y] = True
                    component.append((x, y))
                    stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
    
    for i in range(binary_edges.shape[0]):
        for j in range(binary_edges.shape[1]):
            if binary_edges[i, j] and not visited[i, j]:
                component = []
                dfs(i, j, component)
                if len(component) > 5:  # Minimum size
                    components.append(component)
    
    # Dairesellik hesaplama
    circular_components = 0
    for component in components:
        if len(component) > 10:
            # Basit dairesellik kontrolü
            xs = [p[0] for p in component]
            ys = [p[1] for p in component]
            mean_x, mean_y = np.mean(xs), np.mean(ys)
            distances = [np.sqrt((x - mean_x)*2 + (y - mean_y)*2) for x, y in zip(xs, ys)]
            std_distance = np.std(distances)
            mean_distance = np.mean(distances)
            
            # Dairesellik oranı
            if mean_distance > 0 and std_distance / mean_distance < 0.5:
                circular_components += 1
    
    return circular_components / max(1, len(components))

def detect_sharp_edges(matrix):
    """Keskin kenar tespiti (skuamöz için)"""
    # Laplacian (ikinci türev)
    laplacian = np.zeros_like(matrix)
    for i in range(1, matrix.shape[0]-1):
        for j in range(1, matrix.shape[1]-1):
            laplacian[i, j] = (matrix[i+1, j] + matrix[i-1, j] + 
                              matrix[i, j+1] + matrix[i, j-1] - 4*matrix[i, j])
    
    sharp_edges = np.abs(laplacian) > np.percentile(np.abs(laplacian), 95)
    return float(np.mean(sharp_edges))

def analyze_tissue_mathematically(image_array):
    """Görüntüyü matematiksel olarak analiz et"""
    # 1. ÖNCE KANSER Mİ DEĞİL Mİ BAKALIM
    # Gri tonlamaya çevir
    if len(image_array.shape) == 3:
        gray = np.mean(image_array, axis=2).astype(np.float32)
    else:
        gray = image_array.astype(np.float32)
    
    gray_normalized = gray / 255.0
    
    # Temel istatistikler
    variance = calculate_tissue_variance(gray_normalized)
    homogeneity = calculate_homogeneity(gray_normalized)
    entropy = calculate_entropy(gray_normalized)
    
    # Pattern analizleri (sadece kanser şüphesi varsa)
    glandular_score = 0.0
    keratin_score = 0.0
    
    # KANSER ŞÜPHESİ VARSA PATTERN ANALİZİ YAP
    if not (variance < 0.05 and homogeneity > 0.8 and entropy < 4.0):
        # Kanser şüphesi var, pattern analizi yap
        glandular_score = detect_circular_patterns(gray_normalized)
        keratin_score = detect_sharp_edges(gray_normalized)
    
    # Hücre yoğunluğu
    density_threshold = np.percentile(gray, 75)
    cellular_density = np.sum(gray > density_threshold) / gray.size
    
    # Boşluk analizi
    void_threshold = np.percentile(gray, 25)
    void_percentage = np.sum(gray < void_threshold) / gray.size
    
    return {
        "variance": variance,
        "homogeneity": homogeneity,
        "entropy": entropy,
        "glandular_score": glandular_score,
        "keratin_score": keratin_score,
        "cellular_density": cellular_density,
        "void_percentage": void_percentage,
        "image_size": gray.shape,
        "is_normal": (variance < 0.05 and homogeneity > 0.8 and entropy < 4.0)
    }

def determine_diagnosis(analysis):
    """Matematiksel kriterlere göre tanı koy"""
    v = analysis["variance"]
    h = analysis["homogeneity"]
    e = analysis["entropy"]
    g = analysis["glandular_score"]
    k = analysis["keratin_score"]
    
    # 1. ÖNCE NORMAL Mİ BAK
    if analysis["is_normal"]:
        diagnosis = "NORMAL LUNG TISSUE"
        confidence = (1 - v*10) * h * (1 - e/5) * 100
        confidence = min(98, max(90, confidence))
        stage = "N/A"
    
    # 2. ADENOKARSİNOM
    elif 0.05 <= v <= 0.20 and h >= 0.4 and e >= 3.5:
        # Glandüler pattern varsa adenokarsinom
        if g > 0.2:
            diagnosis = "ADENOCARCINOMA"
            confidence = (v * 4) * (h) * (e/7) * (1 + g) * 100
            if v < 0.1:
                stage = "Stage I"
            elif v < 0.15:
                stage = "Stage II"
            elif v < 0.2:
                stage = "Stage III"
            else:
                stage = "Stage IV"
        else:
            diagnosis = "SUSPICIOUS - NEEDS FURTHER TESTING"
            confidence = 60.0
            stage = "Unknown"
    
    # 3. SKUAMÖZ KARSİNOM
    elif v > 0.1 and h < 0.6 and e > 4.0:
        # Keratin pattern varsa skuamöz
        if k > 0.15:
            diagnosis = "SQUAMOUS CELL CARCINOMA"
            confidence = (v * 3) * (1 - h) * (e/8) * (1 + k*2) * 100
            if v < 0.15:
                stage = "Stage I-II"
            elif v < 0.25:
                stage = "Stage III"
            else:
                stage = "Stage IV"
        else:
            diagnosis = "ATYPICAL - PATHOLOGY REVIEW NEEDED"
            confidence = 55.0
            stage = "Unknown"
    
    # 4. BELİRSİZ
    else:
        diagnosis = "UNCERTAIN - MANUAL REVIEW REQUIRED"
        confidence = 50.0
        stage = "Unknown"
    
    return {
        "diagnosis": diagnosis,
        "confidence": min(99.0, max(30.0, confidence)),
        "stage": stage,
        "variance": v,
        "homogeneity": h,
        "entropy": e,
        "glandular_score": g,
        "keratin_score": k,
        "cellular_density": analysis["cellular_density"],
        "void_percentage": analysis["void_percentage"]
    }

# ==================== ANA UYGULAMA ====================
st.markdown("## 📤 Multiple Image Upload & Analysis")

uploaded_files = st.file_uploader(
    "Upload lung tissue images (PNG, JPG, JPEG)",
    type=['png', 'jpg', 'jpeg'],
    accept_multiple_files=True,
    help="You can upload normal, adenocarcinoma, and squamous cell carcinoma images"
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} image(s) loaded successfully")
    
    if st.button("🚀 START MATHRIX ANALYSIS", type="primary", use_container_width=True):
        
        results_summary = []
        
        for idx, uploaded_file in enumerate(uploaded_files):
            # Progress
            progress = (idx + 1) / len(uploaded_files)
            st.progress(progress, text=f"Analyzing image {idx + 1} of {len(uploaded_files)}")
            
            # Görüntüyü aç
            image = Image.open(uploaded_file)
            image_array = np.array(image)
            
            # Hasta ID
            patient_id = f"PT-{1000 + idx:04d}"
            
            st.markdown(f"### 📋 Analysis for: {patient_id}")
            
            col_img, col_analysis = st.columns([1, 2])
            
            with col_img:
                st.image(image, caption=f"Specimen: {patient_id}", use_column_width=True)
                st.caption(f"Dimensions: {image.size[0]} x {image.size[1]} pixels")
                st.caption(f"File: {uploaded_file.name}")
            
            with col_analysis:
                # SCANNING ANIMASYONU
                scanning_placeholder = st.empty()
                scanning_placeholder.markdown("""
                <div style='background: linear-gradient(90deg, transparent, rgba(100, 255, 218, 0.2), transparent);
                         background-size: 200% 100%; 
                         animation: scan 2s linear infinite;
                         padding: 20px; 
                         border-radius: 10px;
                         text-align: center;
                         border: 1px solid #64ffda;'>
                    <h4 style='color: #64ffda;'>SCANNING TISSUE MATRIX...</h4>
                    <p style='color: #89cff0;'>Mathematical analysis in progress</p>
                </div>
                """, unsafe_allow_html=True)
                
                time.sleep(1)  # Simüle edilmiş analiz süresi
                
                # ANALİZ YAP
                with st.spinner("Calculating mathematical parameters..."):
                    analysis_results = analyze_tissue_mathematically(image_array)
                
                scanning_placeholder.empty()
                
                # TANI KOY
                diagnosis_results = determine_diagnosis(analysis_results)
                
                # SONUÇLARI GÖSTER
                diagnosis = diagnosis_results["diagnosis"]
                confidence = diagnosis_results["confidence"]
                
                if "NORMAL" in diagnosis:
                    st.markdown(f"""
                    <div class='normal-box'>
                        <h3>✅ {diagnosis}</h3>
                        <p><strong>Confidence:</strong> {confidence:.1f}%</p>
                        <p><strong>Variance:</strong> {diagnosis_results['variance']:.4f} (Low - Normal tissue)</p>
                        <p><strong>Recommendation:</strong> Routine follow-up in 12 months</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                elif "ADENOCARCINOMA" in diagnosis:
                    st.markdown(f"""
                    <div class='adenocarcinoma-box'>
                        <h3>⚠️ {diagnosis}</h3>
                        <p><strong>Stage:</strong> {diagnosis_results['stage']}</p>
                        <p><strong>Confidence:</strong> {confidence:.1f}%</p>
                        <p><strong>Glandular Pattern Score:</strong> {diagnosis_results['glandular_score']:.3f}</p>
                        <p><strong>Recommendation:</strong> Immediate EGFR/ALK testing, surgical consultation</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                elif "SQUAMOUS" in diagnosis:
                    st.markdown(f"""
                    <div class='squamous-box'>
                        <h3>⚠️ {diagnosis}</h3>
                        <p><strong>Stage:</strong> {diagnosis_results['stage']}</p>
                        <p><strong>Confidence:</strong> {confidence:.1f}%</p>
                        <p><strong>Keratin Pattern Score:</strong> {diagnosis_results['keratin_score']:.3f}</p>
                        <p><strong>Recommendation:</strong> PD-L1 testing, chemoradiation evaluation</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                else:
                    st.warning(f"*{diagnosis}* (Confidence: {confidence:.1f}%)")
                    st.info("This sample requires manual pathology review for definitive diagnosis.")
                
                # MATEMATİKSEL METRİKLER
                st.markdown("##### 📊 Mathematical Analysis Parameters")
                
                cols = st.columns(4)
                metrics = [
                    ("Variance", f"{diagnosis_results['variance']:.4f}", 
                     "Low" if diagnosis_results['variance'] < 0.05 else "High"),
                    ("Homogeneity", f"{diagnosis_results['homogeneity']:.3f}", 
                     "High" if diagnosis_results['homogeneity'] > 0.7 else "Low"),
                    ("Entropy", f"{diagnosis_results['entropy']:.2f} bits", 
                     "Low" if diagnosis_results['entropy'] < 4.0 else "High"),
                    ("Cellular Density", f"{diagnosis_results['cellular_density']*100:.1f}%",
                     "High" if diagnosis_results['cellular_density'] > 0.6 else "Normal"),
                    ("Void Percentage", f"{diagnosis_results['void_percentage']*100:.1f}%",
                     "Many voids" if diagnosis_results['void_percentage'] > 0.3 else "Few voids"),
                    ("Glandular Pattern", f"{diagnosis_results['glandular_score']:.3f}",
                     "Present" if diagnosis_results['glandular_score'] > 0.2 else "Absent"),
                    ("Keratin Pattern", f"{diagnosis_results['keratin_score']:.3f}",
                     "Present" if diagnosis_results['keratin_score'] > 0.15 else "Absent"),
                    ("Image Size", f"{analysis_results['image_size'][0]}x{analysis_results['image_size'][1]}",
                     "Pixels")
                ]
                
                for i, (label, value, status) in enumerate(metrics):
                    with cols[i % 4]:
                        st.markdown(f"""
                        <div class='math-metric'>
                            <h4>{label}</h4>
                            <h3>{value}</h3>
                            <p style='color: #89cff0; font-size: 0.9em;'>{status}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Sonuçları kaydet
                results_summary.append({
                    "Patient": patient_id,
                    "Diagnosis": diagnosis,
                    "Confidence": f"{confidence:.1f}%",
                    "Stage": diagnosis_results["stage"],
                    "Variance": f"{diagnosis_results['variance']:.4f}",
                    "File": uploaded_file.name
                })
            
            st.markdown("---")
        
        # TOPLU SONUÇLAR
        if results_summary:
            st.markdown("## 📈 Batch Analysis Summary")
            
            # İstatistikler
            col1, col2, col3, col4 = st.columns(4)
            
            normal_count = len([r for r in results_summary if "NORMAL" in r["Diagnosis"]])
            adeno_count = len([r for r in results_summary if "ADENOCARCINOMA" in r["Diagnosis"]])
            squamous_count = len([r for r in results_summary if "SQUAMOUS" in r["Diagnosis"]])
            other_count = len(results_summary) - normal_count - adeno_count - squamous_count
            
            with col1:
                st.metric("Total Images", len(results_summary))
            with col2:
                st.metric("Normal", normal_count)
            with col3:
                st.metric("Adenocarcinoma", adeno_count)
            with col4:
                st.metric("Squamous", squamous_count)
            
            # Rapor oluştur
            report_text = "MATHRIX ANALYSIS REPORT\n" + "="*50 + "\n\n"
            report_text += f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            report_text += f"Total Images: {len(results_summary)}\n"
            report_text += f"Normal: {normal_count}, Adenocarcinoma: {adeno_count}, Squamous: {squamous_count}\n\n"
            
            for result in results_summary:
                report_text += f"Patient: {result['Patient']}\n"
                report_text += f"File: {result['File']}\n"
                report_text += f"Diagnosis: {result['Diagnosis']}\n"
                report_text += f"Confidence: {result['Confidence']}\n"
                report_text += f"Stage: {result['Stage']}\n"
                report_text += f"Variance: {result['Variance']}\n"
                report_text += "-"*40 + "\n"
            
            report_text += "\n*DISCLAIMER:* This is an AI-assisted analysis. All results must be confirmed by a certified pathologist.\n"
            
            st.download_button(
                label="📥 Download Full Report",
                data=report_text,
                file_name=f"mathrix_report_{time.strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

else:
    # ANA SAYFA
    st.markdown("""
    <div style='text-align: center; padding: 40px;'>
        <h2 style='color: #64ffda !important;'>Welcome to MATHRIX Analysis Engine</h2>
        <p style='color: #89cff0 !important; font-size: 1.1em;'>
        Advanced mathematical analysis system for lung tissue histopathology
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <div style='font-size: 48px; color: #64ffda;'>🔢</div>
            <h4 style='color: #64ffda !important;'>Mathematical Analysis</h4>
            <p style='color: white !important;'>Variance, entropy, homogeneity calculations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_info2:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <div style='font-size: 48px; color: #64ffda;'>🎯</div>
            <h4 style='color: #64ffda !important;'>Precise Differentiation</h4>
            <p style='color: white !important;'>Normal vs Adenocarcinoma vs Squamous</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_info3:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <div style='font-size: 48px; color: #64ffda;'>📊</div>
            <h4 style='color: #64ffda !important;'>Pattern Recognition</h4>
            <p style='color: white !important;'>Glandular and keratin pattern detection</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.info("""
    *HOW TO USE:*
    
    1. *Upload* H&E stained lung tissue images (multiple files supported)
    2. *Click* "START MATHRIX ANALYSIS" button
    3. *View* mathematical analysis results for each image
    4. *Check* diagnostic classification with confidence scores
    5. *Download* comprehensive report
    
    *SUPPORTED IMAGE TYPES:* PNG, JPG, JPEG
    *BATCH PROCESSING:* Yes, multiple images at once
    *ANALYSIS DEPTH:* Mathematical variance, homogeneity, entropy, pattern detection
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #89cff0; padding: 20px;'>
    <p><strong>MATHRIX Analysis Engine v7.0</strong> | Mathematical Pathology System</p>
    <p>© 2024 Computational Pathology Lab | For educational and research purposes</p>
    <p><em style='color: #b0e0e6;'>All analyses require pathological confirmation. Not for diagnostic use.</em></p>
</div>
""", unsafe_allow_html=True)
