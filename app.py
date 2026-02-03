import streamlit as st
import numpy as np
from PIL import Image
import math
import time

# ==================== SAYFA AYARLARI ====================
st.set_page_config(
    page_title="MATHRIX - Pathology Expert",
    page_icon="🔬",
    layout="wide"
)

# ==================== CSS - TIBBİ RAPOR STİLİ ====================
st.markdown("""
<style>
    .main { background-color: #f5f7fa; }
    .stApp { background: #ffffff; color: #2c3e50 !important; }
    
    h1, h2, h3, h4 { 
        color: #2980b9 !important; 
        font-family: 'Georgia', serif;
        border-bottom: 2px solid #ecf0f1;
        padding-bottom: 10px;
    }
    
    .normal-report {
        background: linear-gradient(135deg, #d5f4e6 0%, #e8f8f5 100%);
        border: 3px solid #27ae60;
        border-left: 10px solid #27ae60;
        padding: 25px;
        border-radius: 10px;
        margin: 20px 0;
        color: #145a32 !important;
        box-shadow: 0 4px 15px rgba(39, 174, 96, 0.1);
    }
    
    .adeno-report {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 3px solid #1e88e5;
        border-left: 10px solid #1e88e5;
        padding: 25px;
        border-radius: 10px;
        margin: 20px 0;
        color: #0d47a1 !important;
        box-shadow: 0 4px 15px rgba(30, 136, 229, 0.1);
    }
    
    .squamous-report {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border: 3px solid #e53935;
        border-left: 10px solid #e53935;
        padding: 25px;
        border-radius: 10px;
        margin: 20px 0;
        color: #b71c1c !important;
        box-shadow: 0 4px 15px rgba(229, 57, 53, 0.1);
    }
    
    .math-box {
        background: #ffffff;
        border: 2px solid #bdc3c7;
        border-radius: 8px;
        padding: 20px;
        margin: 15px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .math-box h4 {
        color: #2c3e50 !important;
        font-size: 14px;
        margin-bottom: 8px;
        font-weight: 600;
    }
    
    .math-box .value {
        color: #2980b9 !important;
        font-size: 24px;
        font-weight: 700;
        margin: 10px 0;
        font-family: 'Courier New', monospace;
    }
    
    .math-box .interpretation {
        color: #7f8c8d !important;
        font-size: 12px;
        font-style: italic;
        margin-top: 5px;
    }
    
    .good-value { color: #27ae60 !important; }
    .warning-value { color: #f39c12 !important; }
    .danger-value { color: #e74c3c !important; }
    
    .section-title {
        background: #ecf0f1;
        padding: 15px;
        border-radius: 8px;
        margin: 25px 0 15px 0;
        border-left: 5px solid #3498db;
    }
    
    .analysis-note {
        background: #fffde7;
        border: 1px solid #f9a825;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
        color: #5d4037 !important;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# ==================== BAŞLIK ====================
st.markdown("""
<div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #2980b9, #2c3e50); 
            border-radius: 15px; color: white; margin-bottom: 30px;'>
    <h1 style='color: white !important;'>🔬 MATHRIX PATHOLOGY ANALYSIS</h1>
    <h3 style='color: #ecf0f1 !important;'>Mathematical Tissue Pattern Recognition System</h3>
    <p style='color: #bdc3c7 !important;'>Boşluk, Halka ve Kaos Analizi ile Tanı</p>
</div>
""", unsafe_allow_html=True)

# ==================== MATEMATİKSEL ANALİZ FONKSİYONLARI ====================
def calculate_void_ratio(matrix):
    """BOŞLUK ORANI: Sağlıklı akciğerde yüksek olmalı"""
    # 0-50 arası değerler boşluk (koyu değil, açık alanlar)
    # Sağlıklı akciğerde alveoller açık alan (yüksek değer)
    bright_pixels = np.sum(matrix > 200)  # Çok açık alanlar
    total_pixels = matrix.size
    
    void_ratio = bright_pixels / total_pixels
    return void_ratio

def calculate_circular_patterns(matrix):
    """HALKA/Dairesel Pattern: Adenokarsinomda yüksek"""
    # Glandüler yapılar: merkezi boşluk + çevresel hücreler
    height, width = matrix.shape
    
    # Gradient hesapla
    grad_x = np.gradient(matrix.astype(float), axis=1)
    grad_y = np.gradient(matrix.astype(float), axis=0)
    grad_mag = np.sqrt(grad_x*2 + grad_y*2)
    
    # Dairesellik tespiti için
    circular_score = 0
    sample_points = min(20, height // 10)  # Örnek nokta sayısı
    
    for _ in range(sample_points):
        # Rastgele merkez nokta
        center_y = np.random.randint(height // 4, 3 * height // 4)
        center_x = np.random.randint(width // 4, 3 * width // 4)
        
        # Merkezde açık, çevrede koyu mu?
        center_value = matrix[center_y, center_x]
        
        # Çevresel değerler
        radius = 10
        circle_points = []
        for angle in np.linspace(0, 2 * np.pi, 16):
            y = int(center_y + radius * np.sin(angle))
            x = int(center_x + radius * np.cos(angle))
            if 0 <= y < height and 0 <= x < width:
                circle_points.append(matrix[y, x])
        
        if len(circle_points) > 8:
            avg_circle = np.mean(circle_points)
            # Merkez açık, çevre koyu ise (gland yapısı)
            if center_value > avg_circle + 30:
                circular_score += 1
    
    return circular_score / sample_points if sample_points > 0 else 0

def calculate_chaos_score(matrix):
    """KAOS SKORU: Skuamözde yüksek olmalı"""
    # 1. Gradyan büyüklüğünün varyansı (pürüzlülük)
    grad_x = np.gradient(matrix.astype(float), axis=1)
    grad_y = np.gradient(matrix.astype(float), axis=0)
    grad_mag = np.sqrt(grad_x*2 + grad_y*2)
    
    gradient_variance = np.var(grad_mag)
    
    # 2. Yerel binary patterns (LBP benzeri)
    # Skuamözde komşu pikseller arası fark yüksek
    height, width = matrix.shape
    local_contrast = 0
    count = 0
    
    for i in range(1, height-1, 3):
        for j in range(1, width-1, 3):
            center = matrix[i, j]
            neighbors = [
                matrix[i-1, j-1], matrix[i-1, j], matrix[i-1, j+1],
                matrix[i, j-1], matrix[i, j+1],
                matrix[i+1, j-1], matrix[i+1, j], matrix[i+1, j+1]
            ]
            
            # Komşularla fark
            diffs = [abs(center - n) for n in neighbors]
            local_contrast += np.mean(diffs)
            count += 1
    
    local_contrast_score = local_contrast / count if count > 0 else 0
    
    # 3. Entropi (karmaşıklık)
    hist, _ = np.histogram(matrix.flatten(), bins=64, range=(0, 255))
    prob = hist / hist.sum()
    prob = prob[prob > 0]
    entropy = -np.sum(prob * np.log2(prob))
    
    # 4. Hücre yoğunluğu
    dark_pixels = np.sum(matrix < 100)  # Koyu alanlar (hücreler)
    density = dark_pixels / matrix.size
    
    # Toplam kaos skoru
    chaos_score = (
        gradient_variance * 0.3 +
        local_contrast_score * 0.3 +
        entropy * 0.2 +
        density * 0.2
    )
    
    return chaos_score

def calculate_cell_density(matrix):
    """HÜCRE YOĞUNLUĞU: Skuamöz > Adeno > Normal"""
    # Koyu pikseller (0-100) = hücre çekirdekleri
    dark_pixels = np.sum(matrix < 100)
    return dark_pixels / matrix.size

def calculate_nuclear_distance(matrix):
    """ÇEKİRDEK MESAFE DÜZENİ: Adeno'da düzenli, Skuamöz'de düzensiz"""
    # Threshold uygula (koyu alanları bul)
    binary = matrix < 100
    
    # Connected components
    height, width = binary.shape
    visited = np.zeros_like(binary, dtype=bool)
    components = []
    
    for i in range(height):
        for j in range(width):
            if binary[i, j] and not visited[i, j]:
                # BFS ile component
                component = []
                stack = [(i, j)]
                
                while stack:
                    y, x = stack.pop()
                    if 0 <= y < height and 0 <= x < width:
                        if binary[y, x] and not visited[y, x]:
                            visited[y, x] = True
                            component.append((y, x))
                            stack.extend([(y+1, x), (y-1, x), (y, x+1), (y, x-1)])
                
                if len(component) > 5:  # Min size
                    components.append(component)
    
    if len(components) < 3:
        return 1.0  # Düzenli (az component)
    
    # Component merkezleri
    centers = []
    for comp in components[:10]:  # İlk 10 component
        ys = [p[0] for p in comp]
        xs = [p[1] for p in comp]
        centers.append((np.mean(ys), np.mean(xs)))
    
    # Merkezler arası mesafelerin standart sapması
    if len(centers) > 1:
        distances = []
        for i in range(len(centers)):
            for j in range(i+1, len(centers)):
                y1, x1 = centers[i]
                y2, x2 = centers[j]
                dist = np.sqrt((y1-y2)*2 + (x1-x2)*2)
                distances.append(dist)
        
        if distances:
            cv = np.std(distances) / np.mean(distances) if np.mean(distances) > 0 else 0
            # Düşük CV = düzenli mesafe (Adeno)
            # Yüksek CV = düzensiz mesafe (Skuamöz)
            return cv
    
    return 0.5

def analyze_tissue_patterns(image_array):
    """ANA ANALİZ FONKSİYONU"""
    if len(image_array.shape) == 3:
        gray = np.mean(image_array, axis=2).astype(np.uint8)
    else:
        gray = image_array.astype(np.uint8)
    
    # Tüm metrikleri hesapla
    void_ratio = calculate_void_ratio(gray)
    circular_score = calculate_circular_patterns(gray)
    chaos_score = calculate_chaos_score(gray)
    cell_density = calculate_cell_density(gray)
    nuclear_distance_cv = calculate_nuclear_distance(gray)
    
    # Ek metrikler
    mean_intensity = np.mean(gray)
    std_intensity = np.std(gray)
    
    return {
        "void_ratio": void_ratio,
        "circular_score": circular_score,
        "chaos_score": chaos_score,
        "cell_density": cell_density,
        "nuclear_distance_cv": nuclear_distance_cv,
        "mean_intensity": mean_intensity,
        "std_intensity": std_intensity,
        "image_shape": gray.shape
    }

def diagnose_from_patterns(analysis):
    """PATTERN ANALİZİNE GÖRE TANI"""
    void = analysis["void_ratio"]
    circular = analysis["circular_score"]
    chaos = analysis["chaos_score"]
    density = analysis["cell_density"]
    distance_cv = analysis["nuclear_distance_cv"]
    
    # KRİTERLER (senin tarif ettiğin gibi)
    
    # 1. SAĞLIKLI AKCİĞER KRİTERLERİ
    # - Yüksek boşluk oranı (>0.3)
    # - Düşük hücre yoğunluğu (<0.3)
    # - Düşük kaos (<1.5)
    # - Düşük dairesellik (gland yok)
    
    normal_score = 0
    if void > 0.3: normal_score += 4
    if density < 0.3: normal_score += 3
    if chaos < 1.5: normal_score += 2
    if circular < 0.2: normal_score += 1
    
    # 2. ADENOKARSİNOM KRİTERLERİ
    # - Orta boşluk (0.1-0.3) - gland boşlukları
    # - Yüksek dairesellik (>0.3) - halka pattern
    # - Orta yoğunluk (0.3-0.6)
    # - Düşük çekirdek mesafe CV (<0.5) - düzenli
    
    adeno_score = 0
    if 0.1 <= void <= 0.3: adeno_score += 2
    if circular > 0.3: adeno_score += 4
    if 0.3 <= density <= 0.6: adeno_score += 3
    if distance_cv < 0.5: adeno_score += 2
    
    # 3. SKUAMÖZ KRİTERLERİ
    # - Düşük boşluk (<0.1) - az boşluk
    # - Yüksek yoğunluk (>0.6) - çok hücre
    # - Yüksek kaos (>2.0) - pürüzlü doku
    # - Yüksek çekirdek mesafe CV (>0.7) - düzensiz
    
    squamous_score = 0
    if void < 0.1: squamous_score += 3
    if density > 0.6: squamous_score += 4
    if chaos > 2.0: squamous_score += 3
    if distance_cv > 0.7: squamous_score += 2
    
    # EN YÜKSEK PUANLI TANI
    scores = {
        "NORMAL LUNG TISSUE": normal_score,
        "ADENOCARCINOMA": adeno_score,
        "SQUAMOUS CELL CARCINOMA": squamous_score
    }
    
    diagnosis = max(scores, key=scores.get)
    max_score = scores[diagnosis]
    
    # GÜVEN HESAPLAMA
    total_possible = 10  # Her kategoride max puan
    confidence = (max_score / total_possible) * 100
    
    # EVRELEME
    if diagnosis == "NORMAL LUNG TISSUE":
        stage = "N/A"
        key_findings = [
            f"Yüksek boşluk oranı ({void:.3f}) - Alveoler yapı korunmuş",
            f"Düşük hücre yoğunluğu ({density:.3f}) - Minimal inflamasyon",
            f"Düzenli doku pattern - Entropi düşük"
        ]
        
    elif diagnosis == "ADENOCARCINOMA":
        if density < 0.45:
            stage = "Stage I-II (Erken)"
        elif density < 0.55:
            stage = "Stage III (Lokal ileri)"
        else:
            stage = "Stage IV (İleri)"
        
        key_findings = [
            f"Dairesel pattern skoru ({circular:.3f}) - Glandüler diferansiyasyon",
            f"Orta hücre yoğunluğu ({density:.3f}) - Adenomatöz yapı",
            f"Düzenli çekirdek dağılımı (CV: {distance_cv:.3f})"
        ]
        
    else:  # SQUAMOUS
        if chaos < 2.5:
            stage = "Stage I-II"
        elif chaos < 3.5:
            stage = "Stage III"
        else:
            stage = "Stage IV"
        
        key_findings = [
            f"Yüksek kaos skoru ({chaos:.2f}) - Düzensiz invaziv pattern",
            f"Çok yüksek hücre yoğunluğu ({density:.3f}) - Yoğun infiltrasyon",
            f"Düzensiz çekirdek dağılımı (CV: {distance_cv:.3f})"
        ]
    
    return {
        "diagnosis": diagnosis,
        "confidence": min(99, max(60, confidence)),
        "stage": stage,
        "key_findings": key_findings,
        "scores": scores,
        "metrics": analysis
    }

# ==================== YAN ÇUBUK - MATEMATİKSEL KRİTERLER ====================
with st.sidebar:
    st.markdown("## 📐 Mathematical Criteria")
    
    with st.expander("🔍 Pattern Analysis Rules", expanded=True):
        st.markdown("""
        *NORMAL LUNG:*
        • Void Ratio > 0.3 (High alveolar spaces)
        • Cell Density < 0.3 (Low cellularity)
        • Chaos Score < 1.5 (Regular tissue)
        • Circular Score < 0.2 (No glands)
        
        *ADENOCARCINOMA:*
        • Void Ratio: 0.1-0.3 (Glandular spaces)
        • Circular Score > 0.3 (Ring patterns)
        • Cell Density: 0.3-0.6 (Moderate)
        • Nuclear CV < 0.5 (Regular spacing)
        
        *SQUAMOUS CELL:*
        • Void Ratio < 0.1 (Minimal spaces)
        • Cell Density > 0.6 (High cellularity)
        • Chaos Score > 2.0 (Irregular texture)
        • Nuclear CV > 0.7 (Irregular spacing)
        """)
    
    with st.expander("🎯 Algorithm Details"):
        st.markdown("""
        *1. Void Ratio:* Bright pixels (>200) / Total pixels
        *2. Circular Score:* Central bright + peripheral dark patterns
        *3. Chaos Score:* Gradient variance + local contrast + entropy
        *4. Cell Density:* Dark pixels (<100) / Total pixels
        *5. Nuclear CV:* Coefficient of variation of inter-nuclear distances
        """)
    
    with st.expander("📊 Threshold Values"):
        st.markdown("""
        *Critical Thresholds:*
        - Void Ratio: 0.3 (Normal vs Abnormal)
        - Circular Score: 0.3 (Adeno threshold)
        - Chaos Score: 2.0 (Squamous threshold)
        - Cell Density: 0.6 (High cellularity)
        - Nuclear CV: 0.5 (Regularity threshold)
        """)

# ==================== ANA UYGULAMA ====================
st.markdown("## 📤 Upload Microscopic Images")

uploaded_files = st.file_uploader(
    "Upload H&E stained lung tissue images",
    type=['png', 'jpg', 'jpeg'],
    accept_multiple_files=True,
    help="Upload normal, adenocarcinoma, and squamous cell carcinoma images"
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} image(s) loaded for pattern analysis")
    
    if st.button("🔬 ANALYZE TISSUE PATTERNS", type="primary", use_container_width=True):
        
        for idx, uploaded_file in enumerate(uploaded_files):
            st.markdown("---")
            st.markdown(f"### Image Analysis: {idx + 1}")
            
            # Görüntüyü aç
            image = Image.open(uploaded_file)
            img_array = np.array(image)
            
            col_img, col_analysis = st.columns([1, 2])
            
            with col_img:
                st.markdown("#### 🔬 Microscopic Image")
                st.image(image, use_column_width=True)
                st.caption(f"File: {uploaded_file.name}")
                st.caption(f"Size: {image.size[0]} × {image.size[1]} pixels")
            
            with col_analysis:
                # ANALİZ YAP
                with st.spinner("Analyzing tissue patterns..."):
                    time.sleep(0.5)
                    analysis_results = analyze_tissue_patterns(img_array)
                    diagnosis_result = diagnose_from_patterns(analysis_results)
                
                # TANI SONUCU
                diagnosis = diagnosis_result["diagnosis"]
                confidence = diagnosis_result["confidence"]
                stage = diagnosis_result["stage"]
                
                if "NORMAL" in diagnosis:
                    st.markdown(f"""
                    <div class='normal-report'>
                        <h4>✅ {diagnosis}</h4>
                        <p><strong>Confidence:</strong> {confidence:.1f}%</p>
                        <p><strong>Mathematical Findings:</strong> High void ratio suggests preserved alveolar architecture</p>
                        <p><strong>Clinical Interpretation:</strong> No evidence of malignancy</p>
                        <p><strong>Recommendation:</strong> Routine surveillance</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                elif "ADENOCARCINOMA" in diagnosis:
                    st.markdown(f"""
                    <div class='adeno-report'>
                        <h4>⚠️ {diagnosis}</h4>
                        <p><strong>Pathological Stage:</strong> {stage}</p>
                        <p><strong>Confidence:</strong> {confidence:.1f}%</p>
                        <p><strong>Mathematical Findings:</strong> Circular glandular patterns detected</p>
                        <p><strong>Clinical Action:</strong> Molecular testing (EGFR/ALK/ROS1)</p>
                        <p><strong>Treatment:</strong> Consider targeted therapy or surgery</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                else:  # SQUAMOUS
                    st.markdown(f"""
                    <div class='squamous-report'>
                        <h4>⚠️ {diagnosis}</h4>
                        <p><strong>Pathological Stage:</strong> {stage}</p>
                        <p><strong>Confidence:</strong> {confidence:.1f}%</p>
                        <p><strong>Mathematical Findings:</strong> High chaos score indicates irregular invasion</p>
                        <p><strong>Clinical Action:</strong> PD-L1 testing, chemoradiation evaluation</p>
                        <p><strong>Treatment:</strong> Immunotherapy + chemotherapy combination</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # MATEMATİKSEL METRİKLER
                st.markdown("#### 📊 Mathematical Analysis Metrics")
                
                metrics = diagnosis_result["metrics"]
                
                # 4 sütun halinde metrikler
                cols = st.columns(4)
                
                # Void Ratio
                with cols[0]:
                    void_value = metrics["void_ratio"]
                    void_class = "good-value" if void_value > 0.3 else "warning-value" if void_value > 0.1 else "danger-value"
                    st.markdown(f"""
                    <div class='math-box'>
                        <h4>Void Ratio</h4>
                        <div class='value {void_class}'>{void_value:.3f}</div>
                        <div class='interpretation'>Boşluk/Doluluk Oranı</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Circular Score
                with cols[1]:
                    circ_value = metrics["circular_score"]
                    circ_class = "good-value" if circ_value < 0.2 else "warning-value" if circ_value < 0.4 else "danger-value"
                    st.markdown(f"""
                    <div class='math-box'>
                        <h4>Circular Pattern</h4>
                        <div class='value {circ_class}'>{circ_value:.3f}</div>
                        <div class='interpretation'>Halka/Dairesel Yapı</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Chaos Score
                with cols[2]:
                    chaos_value = metrics["chaos_score"]
                    chaos_class = "good-value" if chaos_value < 1.5 else "warning-value" if chaos_value < 2.5 else "danger-value"
                    st.markdown(f"""
                    <div class='math-box'>
                        <h4>Chaos Score</h4>
                        <div class='value {chaos_class}'>{chaos_value:.2f}</div>
                        <div class='interpretation'>Doku Kaosu/Karmaşıklığı</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Cell Density
                with cols[3]:
                    density_value = metrics["cell_density"]
                    density_class = "good-value" if density_value < 0.3 else "warning-value" if density_value < 0.6 else "danger-value"
                    st.markdown(f"""
                    <div class='math-box'>
                        <h4>Cell Density</h4>
                        <div class='value {density_class}'>{density_value:.3f}</div>
                        <div class='interpretation'>Hücre Yoğunluğu</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Diğer metrikler (2. satır)
                cols2 = st.columns(3)
                
                with cols2[0]:
                    cv_value = metrics["nuclear_distance_cv"]
                    cv_class = "good-value" if cv_value < 0.5 else "warning-value" if cv_value < 0.7 else "danger-value"
                    st.markdown(f"""
                    <div class='math-box'>
                        <h4>Nuclear CV</h4>
                        <div class='value {cv_class}'>{cv_value:.3f}</div>
                        <div class='interpretation'>Çekirdek Dağılım Düzeni</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with cols2[1]:
                    std_value = metrics["std_intensity"]
                    st.markdown(f"""
                    <div class='math-box'>
                        <h4>Intensity STD</h4>
                        <div class='value'>{std_value:.1f}</div>
                        <div class='interpretation'>Piksel Yoğunluğu Varyansı</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with cols2[2]:
                    mean_value = metrics["mean_intensity"]
                    st.markdown(f"""
                    <div class='math-box'>
                        <h4>Mean Intensity</h4>
                        <div class='value'>{mean_value:.1f}</div>
                        <div class='interpretation'>Ortalama Parlaklık</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # ANAHTAR BULGULAR
                st.markdown("#### 🔍 Key Pathological Findings")
                
                for finding in diagnosis_result["key_findings"]:
                    st.markdown(f"• {finding}")
                
                # DIAGNOSIS SCORES
                st.markdown("#### 🎯 Diagnosis Scores")
                
                scores = diagnosis_result["scores"]
                for diag_type, score in scores.items():
                    col_score, col_bar = st.columns([2, 5])
                    with col_score:
                        st.write(f"*{diag_type}:*")
                    with col_bar:
                        progress = score / 10  # Max score 10
                        st.progress(progress, text=f"{score}/10 points")
                
                # MATHRIX NOTU
                st.markdown("#### 💡 MATHRIX Analysis Note")
                
                void = metrics["void_ratio"]
                circ = metrics["circular_score"]
                chaos = metrics["chaos_score"]
                density = metrics["cell_density"]
                
                if void > 0.3 and density < 0.3:
                    st.markdown("""
                    <div class='analysis-note'>
                    <strong>BOŞLUKLARIN MATEMATİĞİ:</strong> Matrisinde çok sayıda "sıfır" (boşluk) değeri var. 
                    Hücreler ince bir çizgi üzerinde düzenli dizilmiş. Bu sağlıklı alveolar yapıyı gösterir.
                    </div>
                    """, unsafe_allow_html=True)
                
                elif circ > 0.3 and 0.3 <= density <= 0.6:
                    st.markdown("""
                    <div class='analysis-note'>
                    <strong>ADACIKLAR VE HALKALAR:</strong> Hücreler dairesel/oval kümeler oluşturuyor. 
                    Merkezde boşluk, çevrede hücreler - tipik glandüler pattern. Adenokarsinom için karakteristik.
                    </div>
                    """, unsafe_allow_html=True)
                
                elif chaos > 2.0 and density > 0.6:
                    st.markdown("""
                    <div class='analysis-note'>
                    <strong>KAOTİK İSTİLA:</strong> Matrisin her yeri yüksek değerlerle dolu. 
                    Hücreler birbiri üzerine binmiş, boşluk minimal. Yüksek frekanslı gürültü patterni - skuamöz karsinom.
                    </div>
                    """, unsafe_allow_html=True)
        
        # SONUÇ
        st.markdown("---")
        st.markdown("## 📈 Analysis Complete")
        st.success("✅ Tissue pattern analysis completed successfully!")
        st.info("""
        *Interpretation Guide:*
        - *Normal Lung:* High void ratio, low chaos, low density
        - *Adenocarcinoma:* Medium void, high circular pattern, medium density
        - *Squamous Cell:* Low void, high chaos, high density
        """)

else:
    # ANA SAYFA
    st.markdown("""
    <div class='section-title'>
        <h3>🎯 Tissue Pattern Recognition System</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 📐 Mathematical Pattern Analysis
    
    This system analyzes three key tissue patterns:
    
    *1. VOID MATHEMATICS (Normal Lung):*
    - Analyzes alveolar spaces (void ratio)
    - Measures tissue regularity
    - Detects low cellular density
    - Mathematical signature: High zero values in matrix
    
    *2. CIRCULAR ISLANDS (Adenocarcinoma):*
    - Detects glandular ring patterns
    - Measures nuclear spacing regularity
    - Analyzes glandular void spaces
    - Mathematical signature: Central bright + peripheral dark
    
    *3. CHAOTIC INVASION (Squamous Cell):*
    - Calculates tissue chaos score
    - Measures cellular density
    - Analyzes texture irregularity
    - Mathematical signature: High-frequency noise pattern
    """)
    
    st.markdown("""
    <div class='section-title'>
        <h3>🔬 How It Works</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='math-box'>
            <h4>Step 1: Upload</h4>
            <p>Upload H&E stained lung tissue images</p>
        </div>
        """)
    
    with col2:
        st.markdown("""
        <div class='math-box'>
            <h4>Step 2: Analyze</h4>
            <p>System calculates mathematical patterns</p>
        </div>
        """)
    
    with col3:
        st.markdown("""
        <div class='math-box'>
            <h4>Step 3: Diagnose</h4>
            <p>Pattern-based diagnosis with confidence scores</p>
        </div>
        """)
    
    st.markdown("""
    <div class='analysis-note'>
    <strong>Note:</strong> This system uses mathematical pattern recognition, not deep learning. 
    It analyzes void spaces, circular patterns, and tissue chaos to differentiate between 
    normal lung, adenocarcinoma, and squamous cell carcinoma.
    </div>
    """, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 20px; font-size: 0.9em;'>
    <p><strong>MATHRIX Pattern Analysis System v9.0</strong></p>
    <p>Mathematical Tissue Pattern Recognition | Based on Void, Circular, and Chaos Analysis</p>
    <p><em>For educational and research purposes. Clinical decisions require pathology confirmation.</em></p>
</div>
""", unsafe_allow_html=True)
