import streamlit as st
import numpy as np
from PIL import Image
import time
import cv2
import io
from collections import deque
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

# ==================== SAYFA AYARLARI ====================
st.set_page_config(
    page_title="MATHRIX - Geometric Pathology AI",
    page_icon="🔬",
    layout="wide"
)

# ==================== CSS - PROFESYONEL RAPOR STİLİ ====================
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        color: #212529 !important;
    }
    
    p, div, span, label, .stMarkdown, .stText {
        color: #212529 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #0d6efd !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 600;
    }
    
    .report-card {
        background-color: #ffffff !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 8px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .normal-card {
        background-color: #d1e7dd !important;
        border: 2px solid #198754 !important;
        border-left: 8px solid #198754 !important;
        border-radius: 8px;
        padding: 25px;
        margin: 15px 0;
        color: #0f5132 !important;
    }
    
    .adeno-card {
        background-color: #cfe2ff !important;
        border: 2px solid #0d6efd !important;
        border-left: 8px solid #0d6efd !important;
        border-radius: 8px;
        padding: 25px;
        margin: 15px 0;
        color: #052c65 !important;
    }
    
    .squamous-card {
        background-color: #f8d7da !important;
        border: 2px solid #dc3545 !important;
        border-left: 8px solid #dc3545 !important;
        border-radius: 8px;
        padding: 25px;
        margin: 15px 0;
        color: #842029 !important;
    }
    
    .metric-card {
        background-color: #ffffff !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        margin: 10px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ==================== BAŞLIK ====================
st.markdown("""
<div class='report-card' style='text-align: center;'>
    <h1>🔬 MATHRIX - GEOMETRIC PATHOLOGY ANALYSIS</h1>
    <h4>Structure-Based Lung Tissue Classification (Color-Blind Architecture)</h4>
    <p style='color: #6c757d !important;'>Version 9.0 | Geometric & Topological Analysis Engine</p>
</div>
""", unsafe_allow_html=True)

# ==================== YENİ ANALİZ FONKSİYONLARI ====================
def preprocess_image_color_blind(image_array):
    """
    Renk körü ön işleme: Görüntüyü yapısal analiz için hazırla
    """
    # 1. Gri tonlamaya çevir (renk bilgisini atmak için)
    if len(image_array.shape) == 3:
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = image_array
    
    # 2. CLAHE ile kontrast sınırlı adaptif histogram eşitleme
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray_clahe = clahe.apply(gray)
    
    # 3. Gaussian blur ile gürültüyü azalt
    blurred = cv2.GaussianBlur(gray_clahe, (5, 5), 0)
    
    # 4. Sobel kenar tespiti
    sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    sobel_magnitude = np.sqrt(sobelx*2 + sobely*2)
    sobel_magnitude = np.uint8(sobel_magnitude / sobel_magnitude.max() * 255)
    
    # 5. Binary threshold (Otsu)
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 6. Morfolojik işlemler
    kernel = np.ones((3, 3), np.uint8)
    opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
    
    return {
        'gray': gray,
        'clahe': gray_clahe,
        'blurred': blurred,
        'sobel': sobel_magnitude,
        'binary': binary,
        'morph': closed
    }

def calculate_geometric_features(preprocessed):
    """
    Geometrik ve topolojik özellikleri hesapla
    """
    binary = preprocessed['binary']
    gray = preprocessed['gray']
    
    # 1. LACUNARITY (Boşlukluluk) - Normal doku için
    def calculate_lacunarity(binary_image, box_sizes=[2, 4, 8, 16]):
        """Lacunarity hesapla: yüksek değer = daha boşluklu"""
        lacunarities = []
        for box_size in box_sizes:
            if box_size >= min(binary_image.shape):
                continue
            
            # Sliding window
            lac = []
            for i in range(0, binary_image.shape[0] - box_size, box_size//2):
                for j in range(0, binary_image.shape[1] - box_size, box_size//2):
                    window = binary_image[i:i+box_size, j:j+box_size]
                    if window.size == 0:
                        continue
                    # Koyu piksellerin oranı
                    dark_ratio = np.sum(window < 128) / window.size
                    lac.append(dark_ratio)
            
            if lac:
                mean_lac = np.mean(lac)
                std_lac = np.std(lac)
                lacunarity = std_lac / (mean_lac + 1e-10) if mean_lac > 0 else 0
                lacunarities.append(lacunarity)
        
        return np.mean(lacunarities) if lacunarities else 0
    
    lacunarity = calculate_lacunarity(binary)
    
    # 2. FRACTAL DIMENSION (Kendine benzerlik) - SCC için
    def calculate_fractal_dimension(binary_image):
        """Box-counting method ile fraktal boyut"""
        sizes = [2, 4, 8, 16, 32, 64]
        counts = []
        
        for size in sizes:
            if size >= min(binary_image.shape):
                continue
            
            # Grid üzerinde say
            count = 0
            for i in range(0, binary_image.shape[0], size):
                for j in range(0, binary_image.shape[1], size):
                    window = binary_image[i:min(i+size, binary_image.shape[0]), 
                                         j:min(j+size, binary_image.shape[1])]
                    if np.any(window < 128):  # Koyu pikseller varsa
                        count += 1
            counts.append(count)
        
        if len(counts) > 1:
            # Log-log regression
            sizes = sizes[:len(counts)]
            coeffs = np.polyfit(np.log(sizes), np.log(counts), 1)
            return -coeffs[0]  # Fractal dimension
        return 1.0
    
    fractal_dim = calculate_fractal_dimension(binary)
    
    # 3. CIRCULARITY & LUMEN DETECTION (Adeno için)
    def detect_circular_structures(binary_image):
        """Dairesel yapıları tespit et (glandüler yapılar)"""
        # Kontur bul
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        circularities = []
        lumen_areas = []
        
        for contour in contours:
            if len(contour) < 5:
                continue
            
            # Alan ve çevre
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            
            # Dairesellik
            if perimeter > 0:
                circularity = 4 * np.pi * area / (perimeter * perimeter)
                circularities.append(circularity)
            
            # Minimum sınırlayıcı daire
            (x, y), radius = cv2.minEnclosingCircle(contour)
            circle_area = np.pi * radius * radius
            
            # Lümen oranı (iç boşluk)
            if circle_area > 0:
                lumen_ratio = area / circle_area
                lumen_areas.append(lumen_ratio)
        
        avg_circularity = np.mean(circularities) if circularities else 0
        avg_lumen_ratio = np.mean(lumen_areas) if lumen_areas else 0
        num_circular = len([c for c in circularities if c > 0.7])  # Yüksek dairesellik
        
        return avg_circularity, avg_lumen_ratio, num_circular
    
    circularity, lumen_ratio, num_circular = detect_circular_structures(binary)
    
    # 4. VOID ANALYSIS (Boşluk analizi) - Normal için
    def calculate_void_percentage(binary_image):
        """Geniş, sürekli boşluk alanlarını bul"""
        # Ters binary (boşluklar = beyaz)
        inverted = 255 - binary_image
        
        # Bağlantılı bileşen analizi
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(inverted, connectivity=8)
        
        if num_labels > 1:
            # En büyük boşluk alanlarını bul (top 5)
            areas = stats[1:, cv2.CC_STAT_AREA]
            if len(areas) > 0:
                top_areas = np.sort(areas)[-min(5, len(areas)):]
                total_void_area = np.sum(top_areas)
                total_area = binary_image.shape[0] * binary_image.shape[1]
                return total_void_area / total_area
        
        return 0
    
    void_percentage = calculate_void_percentage(binary)
    
    # 5. CELLULAR SOLIDITY (SCC için) - Katılık/kompaklık
    def calculate_solidity(binary_image):
        """Hücrelerin ne kadar sıkı paketlendiği"""
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        solidities = []
        for contour in contours:
            area = cv2.contourArea(contour)
            hull = cv2.convexHull(contour)
            hull_area = cv2.contourArea(hull)
            
            if hull_area > 0:
                solidity = area / hull_area
                solidities.append(solidity)
        
        return np.mean(solidities) if solidities else 0
    
    solidity = calculate_solidity(binary)
    
    # 6. TEXTURE ENTROPY (Doku karmaşıklığı)
    def calculate_texture_entropy(gray_image):
        """GLCM benzeri doku entropisi"""
        from skimage.feature import graycomatrix, graycoprops
        
        # 8-bit quantization
        gray_quantized = (gray_image // 32).astype(np.uint8)
        
        # GLCM hesapla
        glcm = graycomatrix(gray_quantized, distances=[1], angles=[0], symmetric=True, normed=True)
        
        # Entropy
        glcm_matrix = glcm[:, :, 0, 0]
        glcm_matrix = glcm_matrix / np.sum(glcm_matrix)
        entropy = -np.sum(glcm_matrix * np.log2(glcm_matrix + 1e-10))
        
        return entropy
    
    texture_entropy = calculate_texture_entropy(gray)
    
    # 7. NUCLEAR PLEOMORPHISM (Çekirdek düzensizliği)
    def calculate_nuclear_variance(binary_image):
        """Çekirdek boyutlarının varyansı"""
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 1:
            areas = [cv2.contourArea(c) for c in contours]
            return np.var(areas) / (np.mean(areas) + 1e-10)
        return 0
    
    nuclear_variance = calculate_nuclear_variance(binary)
    
    return {
        'lacunarity': lacunarity,
        'fractal_dimension': fractal_dim,
        'circularity': circularity,
        'lumen_ratio': lumen_ratio,
        'num_circular_structures': num_circular,
        'void_percentage': void_percentage,
        'solidity': solidity,
        'texture_entropy': texture_entropy,
        'nuclear_variance': nuclear_variance,
        'total_cells': len(cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0])
    }

def structural_diagnosis(features):
    """
    Yapısal özelliklere göre tanı koy
    """
    # 1. NORMAL Mİ? (Geniş boşluklar, yüksek lacunarity)
    if features['void_percentage'] > 0.6 and features['lacunarity'] > 0.8:
        return {
            'diagnosis': 'NORMAL LUNG TISSUE',
            'confidence': min(95, 85 + features['void_percentage'] * 15),
            'stage': 'N/A',
            'reasoning': f"High void percentage ({features['void_percentage']:.1%}) and lacunarity ({features['lacunarity']:.2f}) indicate healthy alveolar structure"
        }
    
    # 2. ADENOCARCINOMA Mİ? (Dairesel yapılar, lumen)
    adenocarcinoma_score = (
        features['circularity'] * 2.0 +
        features['lumen_ratio'] * 1.5 +
        (features['num_circular_structures'] / 10) * 1.0 -
        features['solidity'] * 0.5
    )
    
    # 3. SQUAMOUS Mİ? (Yüksek solidity, fraktal boyut)
    squamous_score = (
        features['solidity'] * 2.0 +
        features['fractal_dimension'] * 1.5 +
        features['texture_entropy'] * 1.0 -
        features['void_percentage'] * 2.0
    )
    
    # KARAR
    if adenocarcinoma_score > squamous_score and adenocarcinoma_score > 1.5:
        # Evreleme
        if features['nuclear_variance'] < 0.5:
            stage = "Stage I"
        elif features['nuclear_variance'] < 1.0:
            stage = "Stage II"
        elif features['nuclear_variance'] < 2.0:
            stage = "Stage III"
        else:
            stage = "Stage IV"
        
        confidence = min(95, 70 + adenocarcinoma_score * 10)
        
        return {
            'diagnosis': 'ADENOCARCINOMA',
            'confidence': confidence,
            'stage': stage,
            'reasoning': f"Circular structures detected (circularity: {features['circularity']:.2f}, lumen ratio: {features['lumen_ratio']:.2f})",
            'scores': {
                'adenocarcinoma': adenocarcinoma_score,
                'squamous': squamous_score
            }
        }
    else:
        # Evreleme
        if features['solidity'] < 0.8:
            stage = "Stage I-II"
        elif features['solidity'] < 0.9:
            stage = "Stage III"
        else:
            stage = "Stage IV"
        
        confidence = min(95, 70 + squamous_score * 10)
        
        return {
            'diagnosis': 'SQUAMOUS CELL CARCINOMA',
            'confidence': confidence,
            'stage': stage,
            'reasoning': f"High cellular solidity ({features['solidity']:.2f}) and fractal dimension ({features['fractal_dimension']:.2f})",
            'scores': {
                'adenocarcinoma': adenocarcinoma_score,
                'squamous': squamous_score
            }
        }

# ==================== YAN ÇUBUK ====================
with st.sidebar:
    st.markdown("## 🧠 Geometric Analysis Guide")
    
    with st.expander("📐 Structural Features", expanded=True):
        st.markdown("""
        *NORMAL (Dantel):*
        • High Lacunarity (>0.8)
        • High Void Percentage (>60%)
        • Low Fractal Dimension (<1.3)
        
        *ADENOCARCINOMA (Halka):*
        • High Circularity (>0.7)
        • Lumen Detection
        • Medium Solidty (0.4-0.7)
        
        *SQUAMOUS (Mozaik):*
        • High Solidity (>0.8)
        • High Fractal Dimension (>1.5)
        • Low Void Percentage (<20%)
        """)
    
    with st.expander("🔍 Analysis Pipeline"):
        st.markdown("""
        1. *Color-Blind Conversion:* RGB → Grayscale
        2. *Contrast Enhancement:* CLAHE
        3. *Edge Detection:* Sobel Filter
        4. *Morphological Processing*
        5. *Geometric Feature Extraction*
        6. **Topological Pattern Recognition
        """)

# ==================== ANA UYGULAMA ====================
st.markdown("## 📤 Upload Microscopic Images")

uploaded_files = st.file_uploader(
    "Upload H&E stained lung tissue images",
    type=['png', 'jpg', 'jpeg', 'tiff', 'bmp'],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} image(s) loaded")
    
    if st.button("🔍 PERFORM STRUCTURAL ANALYSIS", type="primary", use_container_width=True):
        
        all_results = []
        all_predictions = []
        all_true_labels = []  # Manuel etiketleme için
        
        for idx, uploaded_file in enumerate(uploaded_files):
            progress = (idx + 1) / len(uploaded_files)
            st.progress(progress, text=f"Analyzing structure of image {idx + 1}/{len(uploaded_files)}")
            
            # Görüntüyü aç
            image = Image.open(uploaded_file)
            image_array = np.array(image)
            
            sample_id = f"GS-{1000 + idx:04d}"
            
            st.markdown(f"### 📋 Structural Analysis: {sample_id}")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("#### 🔬 Original Image")
                st.image(image, caption=f"Sample: {sample_id}", use_column_width=True)
                
                # Manuel etiketleme (test için)
                true_label = st.selectbox(
                    f"Actual Diagnosis for {sample_id}",
                    ["Select", "Normal", "Adenocarcinoma", "Squamous"],
                    key=f"label_{idx}"
                )
                
                if true_label != "Select":
                    all_true_labels.append(true_label)
            
            with col2:
                # ÖN İŞLEME
                with st.spinner("Preprocessing (color-blind conversion)..."):
                    preprocessed = preprocess_image_color_blind(image_array)
                
                # ÖZELLİK ÇIKARMA
                with st.spinner("Extracting geometric features..."):
                    features = calculate_geometric_features(preprocessed)
                
                # TANI
                with st.spinner("Performing structural diagnosis..."):
                    diagnosis_results = structural_diagnosis(features)
                
                # SONUÇ
                diagnosis = diagnosis_results['diagnosis']
                confidence = diagnosis_results['confidence']
                stage = diagnosis_results['stage']
                
                if "NORMAL" in diagnosis:
                    st.markdown(f"""
                    <div class='normal-card'>
                        <h4>✅ {diagnosis}</h4>
                        <p><strong>Structural Confidence:</strong> {confidence:.1f}%</p>
                        <p><strong>Key Geometric Feature:</strong> High Void Percentage</p>
                        <p><strong>Pattern:</strong> Lace-like alveolar structure</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                elif "ADENOCARCINOMA" in diagnosis:
                    st.markdown(f"""
                    <div class='adeno-card'>
                        <h4>⚠️ {diagnosis}</h4>
                        <p><strong>Structural Stage:</strong> {stage}</p>
                        <p><strong>Geometric Confidence:</strong> {confidence:.1f}%</p>
                        <p><strong>Pattern:</strong> Circular glandular formations</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                elif "SQUAMOUS" in diagnosis:
                    st.markdown(f"""
                    <div class='squamous-card'>
                        <h4>⚠️ {diagnosis}</h4>
                        <p><strong>Structural Stage:</strong> {stage}</p>
                        <p><strong>Geometric Confidence:</strong> {confidence:.1f}%</p>
                        <p><strong>Pattern:</strong> Solid cellular mosaic</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # GEOMETRİK ÖZELLİKLER
                st.markdown("#### 📐 Geometric Feature Matrix")
                
                # Özelliklerin görselleştirilmesi
                feature_data = [
                    ("Lacunarity", features['lacunarity'], "Normal" if features['lacunarity'] > 0.7 else "Tumor"),
                    ("Fractal Dimension", features['fractal_dimension'], "Squamous" if features['fractal_dimension'] > 1.4 else "Other"),
                    ("Circularity", features['circularity'], "Adeno" if features['circularity'] > 0.6 else "Other"),
                    ("Lumen Ratio", features['lumen_ratio'], "Adeno" if features['lumen_ratio'] > 0.3 else "Other"),
                    ("Void %", features['void_percentage']*100, "Normal" if features['void_percentage'] > 0.6 else "Tumor"),
                    ("Solidity", features['solidity']*100, "Squamous" if features['solidity'] > 0.7 else "Other"),
                    ("Texture Entropy", features['texture_entropy'], "Complex" if features['texture_entropy'] > 3 else "Simple"),
                    ("Nuclear Variance", features['nuclear_variance'], "High" if features['nuclear_variance'] > 0.5 else "Low")
                ]
                
                cols = st.columns(4)
                for i, (name, value, indicator) in enumerate(feature_data):
                    with cols[i % 4]:
                        # İndikatöre göre renk
                        if "Normal" in indicator:
                            color = "#198754"
                        elif "Adeno" in indicator:
                            color = "#0d6efd"
                        elif "Squamous" in indicator:
                            color = "#dc3545"
                        else:
                            color = "#6c757d"
                        
                        st.markdown(f"""
                        <div class='metric-card'>
                            <h4>{name}</h4>
                            <h3 style='color: {color};'>{value:.3f}</h3>
                            <p style='color: #6c757d !important; font-size: 0.9em;'>{indicator}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # GÖRSELLEŞTİRME
                st.markdown("#### 🔍 Structural Visualization")
                
                viz_cols = st.columns(4)
                with viz_cols[0]:
                    st.image(preprocessed['clahe'], caption="CLAHE Enhanced", use_column_width=True)
                with viz_cols[1]:
                    st.image(preprocessed['sobel'], caption="Sobel Edges", use_column_width=True)
                with viz_cols[2]:
                    st.image(preprocessed['binary'], caption="Binary Mask", use_column_width=True)
                with viz_cols[3]:
                    # Kontur çizimi
                    binary = preprocessed['binary']
                    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    contour_img = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
                    cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 1)
                    st.image(contour_img, caption="Detected Structures", use_column_width=True)
                
                # Sonuçları kaydet
                all_results.append({
                    'Sample': sample_id,
                    'Diagnosis': diagnosis,
                    'Confidence': f"{confidence:.1f}%",
                    'Stage': stage,
                    'Lacunarity': f"{features['lacunarity']:.3f}",
                    'Void %': f"{features['void_percentage']*100:.1f}%",
                    'Circularity': f"{features['circularity']:.3f}",
                    'Solidity': f"{features['solidity']*100:.1f}%"
                })
                
                # Tahmini kaydet
                pred_label = diagnosis.split()[0].upper()
                if "NORMAL" in pred_label:
                    all_predictions.append("Normal")
                elif "ADENOCARCINOMA" in pred_label:
                    all_predictions.append("Adenocarcinoma")
                elif "SQUAMOUS" in pred_label:
                    all_predictions.append("Squamous")
            
            st.markdown("---")
        
        # PERFORMANS ANALİZİ (manuel etiketler varsa)
        if len(all_true_labels) == len(all_predictions) and len(all_true_labels) > 0:
            st.markdown("## 📊 Model Performance Analysis")
            
            # Confusion Matrix
            st.markdown("#### 🎯 Confusion Matrix")
            
            # Etiketleri standartlaştır
            labels = ["Normal", "Adenocarcinoma", "Squamous"]
            
            # Sadece seçilmiş etiketleri kullan
            valid_indices = [i for i, label in enumerate(all_true_labels) if label in labels]
            y_true = [all_true_labels[i] for i in valid_indices]
            y_pred = [all_predictions[i] for i in valid_indices]
            
            if len(y_true) > 0:
                cm = confusion_matrix(y_true, y_pred, labels=labels)
                
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                           xticklabels=labels, yticklabels=labels,
                           ax=ax)
                ax.set_xlabel('Predicted')
                ax.set_ylabel('Actual')
                ax.set_title('Confusion Matrix - Structural Analysis')
                st.pyplot(fig)
                
                # Classification Report
                st.markdown("#### 📈 Classification Report")
                report = classification_report(y_true, y_pred, target_names=labels, output_dict=True)
                
                # Report'u tablo olarak göster
                report_data = []
                for label in labels:
                    report_data.append({
                        'Class': label,
                        'Precision': f"{report[label]['precision']:.3f}",
                        'Recall': f"{report[label]['recall']:.3f}",
                        'F1-Score': f"{report[label]['f1-score']:.3f}",
                        'Support': report[label]['support']
                    })
                
                st.table(report_data)
                
                # Genel doğruluk
                accuracy = report['accuracy']
                st.metric("Overall Accuracy", f"{accuracy*100:.1f}%")
        
        # TOPLU RAPOR
        if all_results:
            st.markdown("## 📈 Batch Structural Analysis Report")
            
            # İstatistikler
            normal_count = len([r for r in all_results if "NORMAL" in r["Diagnosis"]])
            adeno_count = len([r for r in all_results if "ADENOCARCINOMA" in r["Diagnosis"]])
            squamous_count = len([r for r in all_results if "SQUAMOUS" in r["Diagnosis"]])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Normal (Lace)", normal_count)
            with col2:
                st.metric("Adeno (Ring)", adeno_count)
            with col3:
                st.metric("Squamous (Mosaic)", squamous_count)
            
            # Rapor oluştur
            report_lines = []
            report_lines.append("=" * 70)
            report_lines.append("MATHRIX GEOMETRIC PATHOLOGY REPORT")
            report_lines.append("=" * 70)
            report_lines.append(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            report_lines.append(f"Total Samples: {len(all_results)}")
            report_lines.append("\nSTRUCTURAL FINDINGS:")
            report_lines.append("-" * 50)
            
            for result in all_results:
                report_lines.append(f"\nSample: {result['Sample']}")
                report_lines.append(f"Diagnosis: {result['Diagnosis']}")
                report_lines.append(f"Geometric Confidence: {result['Confidence']}")
                report_lines.append(f"Lacunarity: {result['Lacunarity']}")
                report_lines.append(f"Void Percentage: {result['Void %']}")
                report_lines.append(f"Circularity: {result['Circularity']}")
                report_lines.append(f"Solidity: {result['Solidity']}")
                report_lines.append("-" * 30)
            
            report_lines.append("\n" + "=" * 70)
            report_lines.append("GEOMETRIC INTERPRETATION:")
            report_lines.append("=" * 70)
            
            if normal_count > 0:
                report_lines.append("\n• LACE PATTERN (Normal): High lacunarity and void percentage")
                report_lines.append("  indicates preserved alveolar architecture.")
            
            if adeno_count > 0:
                report_lines.append("\n• RING PATTERN (Adenocarcinoma): Circular structures")
                report_lines.append("  suggest glandular differentiation with lumen formation.")
            
            if squamous_count > 0:
                report_lines.append("\n• MOSAIC PATTERN (Squamous): High solidity and fractal")
                report_lines.append("  dimension indicate tightly packed cellular sheets.")
            
            report_text = "\n".join(report_lines)
            
            # İndirme butonu
            st.download_button(
                label="📄 Download Geometric Analysis Report",
                data=report_text,
                file_name=f"geometric_report_{time.strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

else:
    # ANA SAYFA
    st.markdown("""
    <div class='report-card' style='text-align: center;'>
        <h2>Welcome to Geometric Pathology Analysis</h2>
        <p style='color: #6c757d !important; font-size: 1.1em;'>
        Color-blind analysis focusing on structural patterns rather than color
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # PATTERN AÇIKLAMALARI
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: #d1e7dd; padding: 20px; border-radius: 10px; border-left: 6px solid #198754;'>
            <h4>🔗 Lace Pattern (Normal)</h4>
            <p><strong>Geometric Signature:</strong></p>
            <ul style='text-align: left;'>
                <li>High Lacunarity (>0.8)</li>
                <li>Void Percentage > 60%</li>
                <li>Low Fractal Dimension</li>
            </ul>
            <p>Delicate alveolar network</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #cfe2ff; padding: 20px; border-radius: 10px; border-left: 6px solid #0d6efd;'>
            <h4>⭕ Ring Pattern (Adeno)</h4>
            <p><strong>Geometric Signature:</strong></p>
            <ul style='text-align: left;'>
                <li>High Circularity (>0.7)</li>
                <li>Lumen Detection</li>
                <li>Medium Solidity</li>
            </ul>
            <p>Glandular formations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: #f8d7da; padding: 20px; border-radius: 10px; border-left: 6px solid #dc3545;'>
            <h4>🧱 Mosaic Pattern (Squamous)</h4>
            <p><strong>Geometric Signature:</strong></p>
            <ul style='text-align: left;'>
                <li>High Solidity (>0.8)</li>
                <li>High Fractal Dimension</li>
                <li>Low Void Percentage</li>
            </ul>
            <p>Tight cellular sheets</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; padding: 20px; border-top: 1px solid #dee2e6;'>
    <p><strong>MATHRIX Geometric Pathology v9.0</strong></p>
    <p>Structure-Based Analysis | Color-Blind Architecture</p>
    <p style='font-size: 0.9em;'><em>Analyzing patterns, not colors. Focusing on geometry, not hue.</em></p>
</div>
""", unsafe_allow_html=True)
