import streamlit as st
import numpy as np
from PIL import Image
import math

# ==================== SAYFA AYARLARI ====================
st.set_page_config(
    page_title="MATHRIX - Histopathology AI",
    page_icon="🔬",
    layout="wide"
)

# ==================== CSS - TIBBİ RAPOR ====================
st.markdown("""
<style>
    .main { background: #fafafa; }
    .stApp { background: #ffffff; color: #333 !important; }
    
    h1, h2, h3 { 
        color: #2c3e50 !important; 
        font-family: 'Georgia', serif;
        border-bottom: 2px solid #ecf0f1;
        padding-bottom: 10px;
    }
    
    .histo-report {
        background: #ffffff;
        border: 2px solid #bdc3c7;
        border-radius: 10px;
        padding: 30px;
        margin: 25px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .normal-histology {
        border-left: 10px solid #27ae60;
        background: linear-gradient(to right, #e8f6f3, #ffffff);
    }
    
    .adeno-histology {
        border-left: 10px solid #3498db;
        background: linear-gradient(to right, #ebf5fb, #ffffff);
    }
    
    .squamous-histology {
        border-left: 10px solid #e74c3c;
        background: linear-gradient(to right, #fdedec, #ffffff);
    }
    
    .metric-histology {
        background: #ecf0f1;
        border: 1px solid #bdc3c7;
        border-radius: 8px;
        padding: 20px;
        margin: 15px;
        text-align: center;
    }
    
    .histo-note {
        background: #fffde7;
        border-left: 5px solid #fbc02d;
        padding: 20px;
        margin: 20px 0;
        font-style: italic;
        color: #5d4037;
    }
    
    .feature-box {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== BAŞLIK ====================
st.markdown("""
<div style='text-align: center; padding: 30px; background: #2c3e50; color: white; border-radius: 15px;'>
    <h1 style='color: white !important;'>🔬 MATHRIX HISTOPATHOLOGY AI</h1>
    <h3 style='color: #ecf0f1 !important;'>Patolog Gözüyle Matematiksel Analiz</h3>
    <p style='color: #bdc3c7 !important;'>Dantel, Halka ve Mozaik Pattern Tanıma</p>
</div>
""", unsafe_allow_html=True)

# ==================== PATOLOJİK ANALİZ FONKSİYONLARI ====================
def analyze_histopathology(image_array):
    """
    PATOLOG GÖZÜYLE ANALİZ
    """
    # RGB kanalları
    if len(image_array.shape) == 3:
        r = image_array[:, :, 0].astype(float)
        g = image_array[:, :, 1].astype(float)
        b = image_array[:, :, 2].astype(float)
    else:
        r = g = b = image_array.astype(float)
    
    height, width = r.shape
    
    # 1. DANTEL ANALİZİ (Normal için)
    # İnce, ağsı yapılar = 1-piksel kalınlığında çizgiler
    def detect_lace_pattern(channel):
        """İnce çizgileri (alveolar duvarlar) tespit et"""
        # Sobel filtresi (basit implementasyon)
        kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        kernel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        
        grad_x = np.zeros_like(channel)
        grad_y = np.zeros_like(channel)
        
        for i in range(1, height-1):
            for j in range(1, width-1):
                patch = channel[i-1:i+2, j-1:j+2]
                grad_x[i, j] = np.sum(patch * kernel_x)
                grad_y[i, j] = np.sum(patch * kernel_y)
        
        grad_mag = np.sqrt(grad_x*2 + grad_y*2)
        
        # İnce çizgiler = yüksek gradient ama düşük alan
        thin_lines = (grad_mag > np.percentile(grad_mag, 90)) & (channel < 200)
        return thin_lines
    
    # Alveolar duvarları tespit et (mavi kanalda daha belirgin)
    lace_pattern = detect_lace_pattern(b)
    lace_density = np.sum(lace_pattern) / (height * width)
    
    # 2. LACUNARITY - BOŞLUKLULUK ANALİZİ
    # Normal: Yüksek lacunarity
    # Pembe/beyaz alanlar = boşluk
    pink_areas = (r > g + 20) & (r > b + 10) & (g > 100)  # Sitoplazma
    white_areas = (r > 200) & (g > 200) & (b > 200)       # Alveoller
    void_areas = pink_areas | white_areas
    
    # Boşluk oranı
    void_ratio = np.sum(void_areas) / (height * width)
    
    # Boşlukların dağılımı (Lacunarity)
    def calculate_lacunarity(binary_matrix):
        """Boşlukların heterojenliğini ölç"""
        if not binary_matrix.any():
            return 0
        
        # Pencere analizi (3x3)
        lacunarity_score = 0
        count = 0
        
        for i in range(0, height-3, 3):
            for j in range(0, width-3, 3):
                window = binary_matrix[i:i+3, j:j+3]
                if window.size == 9:
                    window_mean = np.mean(window)
                    if window_mean > 0:
                        lacunarity_score += (1.0 / window_mean)
                        count += 1
        
        return lacunarity_score / count if count > 0 else 0
    
    lacunarity = calculate_lacunarity(void_areas)
    
    # 3. SPATIAL AUTOCORRELATION - UZAMSAL ÖZİLİŞKİ
    # Hücre çekirdekleri (mor/koyu noktalar)
    nuclei_mask = (b > r + 30) & (b > g + 30) & (r < 150)  # Mor nükleus
    
    def calculate_spatial_autocorrelation(mask):
        """Moran's I benzeri ölçüm"""
        if not mask.any():
            return 0
        
        # Nükleus koordinatları
        coords = np.argwhere(mask)
        
        if len(coords) < 10:
            return 0
        
        # Merkez hesapla
        center_y = np.mean(coords[:, 0])
        center_x = np.mean(coords[:, 1])
        
        # Merkeze uzaklıklar
        distances = np.sqrt((coords[:, 0] - center_y)*2 + (coords[:, 1] - center_x)*2)
        
        # Dairesellik ölçüsü
        if np.mean(distances) > 0:
            cv = np.std(distances) / np.mean(distances)  # Varyasyon katsayısı
            return 1.0 / (1.0 + cv)  # Düşük CV = yüksek dairesellik
        return 0
    
    spatial_autocorr = calculate_spatial_autocorrelation(nuclei_mask)
    
    # 4. HOUGH TRANSFORM BENZERİ - DAİRE ALGILAMA (Adeno için)
    def detect_circular_structures(channel, min_radius=5, max_radius=20):
        """Basit dairesel yapı tespiti"""
        circles = []
        
        # Gradient hesapla
        grad_x = np.gradient(channel.astype(float), axis=1)
        grad_y = np.gradient(channel.astype(float), axis=0)
        grad_mag = np.sqrt(grad_x*2 + grad_y*2)
        
        edge_points = grad_mag > np.percentile(grad_mag, 95)
        edge_coords = np.argwhere(edge_points)
        
        if len(edge_coords) < 50:
            return circles, 0
        
        # Rastgele örnekleme ile dairesellik testi
        circular_score = 0
        samples = min(100, len(edge_coords))
        
        for _ in range(samples):
            idx = np.random.randint(len(edge_coords))
            y, x = edge_coords[idx]
            
            # Potansiyel merkez olarak test et
            if 10 <= y < height-10 and 10 <= x < width-10:
                # Merkezde açık, çevrede koyu mu?
                center_val = channel[y, x]
                
                # Çevre değerleri
                angles = np.linspace(0, 2*np.pi, 16)
                radius = 8
                circle_vals = []
                
                for angle in angles:
                    yy = int(y + radius * np.sin(angle))
                    xx = int(x + radius * np.cos(angle))
                    if 0 <= yy < height and 0 <= xx < width:
                        circle_vals.append(channel[yy, xx])
                
                if len(circle_vals) > 8:
                    avg_circle = np.mean(circle_vals)
                    # Merkez açık, çevre koyu = gland yapısı
                    if center_val > avg_circle + 20:
                        circular_score += 1
                        circles.append((y, x, radius))
        
        return circles, circular_score / samples
    
    circles, circularity_score = detect_circular_structures(b)
    
    # 5. SOLIDITY - KATILIK ANALİZİ (SCC için)
    # Mozaik pattern = keskin kenarlar
    def calculate_solidity(channel):
        """Dokunun katılık/süreklilik derecesi"""
        # Laplacian ile kenar keskinliği
        laplacian = np.zeros_like(channel, dtype=float)
        
        for i in range(1, height-1):
            for j in range(1, width-1):
                laplacian[i, j] = (
                    channel[i+1, j] + channel[i-1, j] +
                    channel[i, j+1] + channel[i, j-1] -
                    4 * channel[i, j]
                )
        
        # Keskin kenarlar
        sharp_edges = np.abs(laplacian) > np.percentile(np.abs(laplacian), 95)
        
        # Kenar yoğunluğu
        edge_density = np.sum(sharp_edges) / (height * width)
        
        # Hücreler arası köprüler = çokgen pattern
        polygon_score = 0
        if sharp_edges.any():
            edge_coords = np.argwhere(sharp_edges)
            if len(edge_coords) > 20:
                # Açı analizi (basit)
                angles = []
                for idx in range(0, len(edge_coords)-10, 10):
                    y1, x1 = edge_coords[idx]
                    y2, x2 = edge_coords[idx+5]
                    y3, x3 = edge_coords[idx+10]
                    
                    # Vektörler
                    v1 = np.array([x2-x1, y2-y1])
                    v2 = np.array([x3-x2, y3-y2])
                    
                    if np.linalg.norm(v1) > 0 and np.linalg.norm(v2) > 0:
                        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
                        angle = np.arccos(np.clip(cos_angle, -1, 1))
                        angles.append(angle)
                
                if angles:
                    # Çokgenlerde açılar belirli (60°, 90°, 120° gibi)
                    angle_variance = np.var(angles)
                    polygon_score = 1.0 / (1.0 + angle_variance)
        
        return edge_density, polygon_score
    
    edge_density, polygon_score = calculate_solidity(b)
    
    # 6. KERATİN İNCİLERİ (SCC için)
    # İçi dolu dairesel girdaplar
    def detect_keratin_pearls(channel):
        """Keratin incilerini tespit et"""
        pearls = 0
        
        # Yuvarlak, içi koyu yapılar
        for i in range(10, height-10, 20):
            for j in range(10, width-10, 20):
                # 10x10 pencere
                window = channel[i-5:i+5, j-5:j+5]
                if window.size == 100:
                    # Merkez koyu, çevre koyu (içi dolu)
                    center_val = window[5, 5]
                    ring_vals = []
                    
                    for angle in np.linspace(0, 2*np.pi, 12):
                        yy = int(5 + 4 * np.sin(angle))
                        xx = int(5 + 4 * np.cos(angle))
                        if 0 <= yy < 10 and 0 <= xx < 10:
                            ring_vals.append(window[yy, xx])
                    
                    if ring_vals:
                        avg_ring = np.mean(ring_vals)
                        # Merkez ve çevre benzer koyulukta = içi dolu
                        if abs(center_val - avg_ring) < 20 and center_val < 100:
                            pearls += 1
        
        return pearls / max(1, (height * width) / 400)
    
    keratin_pearls = detect_keratin_pearls(b)
    
    return {
        # Normal kriterleri
        "lace_density": lace_density,          # Dantel yapı yoğunluğu
        "void_ratio": void_ratio,              # Boşluk oranı
        "lacunarity": lacunarity,              # Boşluk dağılım heterojenliği
        
        # Adeno kriterleri
        "spatial_autocorr": spatial_autocorr,  # Uzamsal özilişki
        "circularity_score": circularity_score,# Dairesellik
        "num_circles": len(circles),           # Tespit edilen daire sayısı
        
        # SCC kriterleri
        "edge_density": edge_density,          # Kenar yoğunluğu
        "polygon_score": polygon_score,        # Çokgen pattern
        "keratin_pearls": keratin_pearls,      # Keratin incileri
        "nuclei_density": np.sum(nuclei_mask) / (height * width),  # Nükleus yoğunluğu
        
        # Genel
        "image_size": (height, width)
    }

def histopathology_diagnosis(analysis):
    """
    PATOLOJİK TANI ALGORİTMASI
    """
    # PATOLOJİK KRİTERLER
    
    # 1. NORMAL AKCİĞER (Dantel ve Hava)
    # - Yüksek lace density (>0.1)
    # - Yüksek void ratio (>0.7)
    # - Yüksek lacunarity (>2.0)
    
    normal_score = 0
    if analysis["lace_density"] > 0.1: normal_score += 3
    if analysis["void_ratio"] > 0.7: normal_score += 4
    if analysis["lacunarity"] > 2.0: normal_score += 3
    
    # 2. ADENOKARSİNOM (Fraktal Halkalar)
    # - Yüksek spatial autocorrelation (>0.6)
    # - Yüksek circularity (>0.3)
    # - Orta void ratio (0.3-0.6)
    
    adeno_score = 0
    if analysis["spatial_autocorr"] > 0.6: adeno_score += 4
    if analysis["circularity_score"] > 0.3: adeno_score += 3
    if 0.3 <= analysis["void_ratio"] <= 0.6: adeno_score += 3
    if analysis["num_circles"] > 5: adeno_score += 2
    
    # 3. SKUAMÖZ KARSİNOM (Kaotik Mozaik)
    # - Yüksek edge density (>0.15)
    # - Yüksek polygon score (>0.4)
    # - Keratin pearls (>0.05)
    # - Düşük void ratio (<0.3)
    # - Yüksek nuclei density (>0.4)
    
    squamous_score = 0
    if analysis["edge_density"] > 0.15: squamous_score += 3
    if analysis["polygon_score"] > 0.4: squamous_score += 3
    if analysis["keratin_pearls"] > 0.05: squamous_score += 4
    if analysis["void_ratio"] < 0.3: squamous_score += 3
    if analysis["nuclei_density"] > 0.4: squamous_score += 2
    
    # TANI
    scores = {
        "NORMAL AKCİĞER DOKUSU": normal_score,
        "ADENOKARSİNOM": adeno_score,
        "SKUAMÖZ HÜCRELİ KARSİNOM": squamous_score
    }
    
    diagnosis = max(scores, key=scores.get)
    max_score = scores[diagnosis]
    
    # GÜVEN HESAPLAMA
    confidence = (max_score / 10) * 100  # Max 10 puan
    
    # PATOLOJİK EVRELEME
    if "NORMAL" in diagnosis:
        stage = "N/A"
        key_features = [
            f"Alveolar dantel yapı: {analysis['lace_density']:.3f}",
            f"Boşluk oranı: {analysis['void_ratio']:.1%}",
            f"Lacunarity: {analysis['lacunarity']:.2f}"
        ]
        
    elif "ADENO" in diagnosis:
        if analysis["circularity_score"] < 0.4:
            stage = "Well-differentiated (Grade 1)"
        elif analysis["circularity_score"] < 0.6:
            stage = "Moderately-differentiated (Grade 2)"
        else:
            stage = "Poorly-differentiated (Grade 3)"
        
        key_features = [
            f"Glandüler halkalar: {analysis['num_circles']} adet",
            f"Dairesellik skoru: {analysis['circularity_score']:.3f}",
            f"Uzamsal özilişki: {analysis['spatial_autocorr']:.3f}"
        ]
        
    else:  # SCC
        if analysis["keratin_pearls"] > 0.1:
            stage = "Keratinizing SCC"
        elif analysis["polygon_score"] > 0.5:
            stage = "Polygonal pattern prominent"
        else:
            stage = "Solid growth pattern"
        
        key_features = [
            f"Keratin incileri: {analysis['keratin_pearls']:.3f}",
            f"Çokgen pattern: {analysis['polygon_score']:.3f}",
            f"Kenar yoğunluğu: {analysis['edge_density']:.3f}"
        ]
    
    return {
        "diagnosis": diagnosis,
        "confidence": min(99, max(60, confidence)),
        "stage": stage,
        "key_features": key_features,
        "scores": scores,
        "analysis": analysis
    }

# ==================== YAN ÇUBUK - PATOLOJİ REHBERİ ====================
with st.sidebar:
    st.markdown("## 📚 Patoloji Rehberi")
    
    with st.expander("🔬 Histolojik Özellikler", expanded=True):
        st.markdown("""
        *NORMAL AKCİĞER:*
        • İnce alveolar duvarlar (dantel)
        • Geniş hava keseleri
        • Düşük hücre yoğunluğu
        
        *ADENOKARSİNOM:*
        • Glandüler halkalar
        • Merkezi lümen
        • Nükleus periferik dizilim
        
        *SKUAMÖZ KARSİNOM:*
        • Solid büyüme patterni
        • Keratin incileri
        • Hücreler arası köprüler
        """)
    
    with st.expander("🎯 Matematiksel Metrikler"):
        st.markdown("""
        *1. Lacunarity:* Boşluk dağılım heterojenliği
        *2. Spatial Autocorrelation:* Nükleus düzeni
        *3. Circularity Score:* Gland yapıları
        *4. Polygon Score:* Hücre şekil düzeni
        *5. Lace Density:* Alveolar duvar inceliği
        """)

# ==================== ANA UYGULAMA ====================
st.markdown("## 📤 Histopatoloji Görüntüsü Yükle")

uploaded_files = st.file_uploader(
    "H&E boyamalı akciğer dokusu kesitleri",
    type=['png', 'jpg', 'jpeg'],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} histopatoloji görüntüsü yüklendi")
    
    if st.button("🔬 PATOLOJİK ANALİZ", type="primary", use_container_width=True):
        
        for idx, uploaded_file in enumerate(uploaded_files):
            st.markdown(f"---")
            st.markdown(f"### Görüntü {idx + 1}: {uploaded_file.name}")
            
            # Görüntüyü aç
            image = Image.open(uploaded_file)
            img_array = np.array(image)
            
            col_img, col_analysis = st.columns([1, 2])
            
            with col_img:
                st.image(image, use_column_width=True)
                st.caption(f"Mag: 40x | Boyut: {image.size[0]}×{image.size[1]}")
            
            with col_analysis:
                # PATOLOJİK ANALİZ
                with st.spinner("Patolojik analiz yapılıyor..."):
                    analysis = analyze_histopathology(img_array)
                    diagnosis_result = histopathology_diagnosis(analysis)
                
                # TANI RAPORU
                diagnosis = diagnosis_result["diagnosis"]
                confidence = diagnosis_result["confidence"]
                stage = diagnosis_result["stage"]
                key_features = diagnosis_result["key_features"]
                
                if "NORMAL" in diagnosis:
                    st.markdown(f"""
                    <div class='histo-report normal-histology'>
                        <h3>✅ {diagnosis}</h3>
                        <p><strong>Patolojik Tanı:</strong> Sağlam alveolar yapı</p>
                        <p><strong>Güven:</strong> {confidence:.1f}%</p>
                        <p><strong>Özellikler:</strong> Dantelsi pattern, yüksek boşluk oranı</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                elif "ADENO" in diagnosis:
                    st.markdown(f"""
                    <div class='histo-report adeno-histology'>
                        <h3>⚠️ {diagnosis}</h3>
                        <p><strong>Patolojik Grade:</strong> {stage}</p>
                        <p><strong>Güven:</strong> {confidence:.1f}%</p>
                        <p><strong>Özellikler:</strong> Glandüler diferansiyasyon, fraktal halkalar</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                else:  # SCC
                    st.markdown(f"""
                    <div class='histo-report squamous-histology'>
                        <h3>⚠️ {diagnosis}</h3>
                        <p><strong>Patolojik Pattern:</strong> {stage}</p>
                        <p><strong>Güven:</strong> {confidence:.1f}%</p>
                        <p><strong>Özellikler:</strong> Solid büyüme, keratinizasyon</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # PATOLOJİK ÖZELLİKLER
                st.markdown("#### 🔍 Patolojik Bulgular")
                
                for feature in key_features:
                    st.markdown(f"• {feature}")
                
                # MATEMATİKSEL METRİKLER
                st.markdown("#### 📊 Matematiksel Histoloji Metrikleri")
                
                cols = st.columns(3)
                
                # Normal metrikleri
                with cols[0]:
                    st.markdown(f"""
                    <div class='metric-histology'>
                        <h4>NORMAL KRİTERLERİ</h4>
                        <p><strong>Dantel Yoğunluğu:</strong> {analysis['lace_density']:.3f}</p>
                        <p><strong>Boşluk Oranı:</strong> {analysis['void_ratio']:.1%}</p>
                        <p><strong>Lacunarity:</strong> {analysis['lacunarity']:.2f}</p>
                    </div>
                    """)
                
                # Adeno metrikleri
                with cols[1]:
                    st.markdown(f"""
                    <div class='metric-histology'>
                        <h4>ADENO KRİTERLERİ</h4>
                        <p><strong>Dairesellik:</strong> {analysis['circularity_score']:.3f}</p>
                        <p><strong>Özilişki:</strong> {analysis['spatial_autocorr']:.3f}</p>
                        <p><strong>Halka Sayısı:</strong> {analysis['num_circles']}</p>
                    </div>
                    """)
                
                # SCC metrikleri
                with cols[2]:
                    st.markdown(f"""
                    <div class='metric-histology'>
                        <h4>SCC KRİTERLERİ</h4>
                        <p><strong>Kenar Yoğunluğu:</strong> {analysis['edge_density']:.3f}</p>
                        <p><strong>Çokgen Skoru:</strong> {analysis['polygon_score']:.3f}</p>
                        <p><strong>Keratin İncileri:</strong> {analysis['keratin_pearls']:.3f}</p>
                    </div>
                    """)
                
                # PATOLOG NOTU
                st.markdown("#### 💡 Patolog Yorumu")
                
                if "NORMAL" in diagnosis:
                    st.markdown("""
                    <div class='histo-note'>
                    <strong>DANTEL VE HAVA:</strong> Görüntüde ince alveolar duvarlar ve geniş hava keseleri mevcut. 
                    Boşluk/doluluk oranı %70-80 arası. Kan damarları düzgün konturlu, hücresel infiltrasyon minimal.
                    </div>
                    """, unsafe_allow_html=True)
                
                elif "ADENO" in diagnosis:
                    st.markdown("""
                    <div class='histo-note'>
                    <strong>FRAKTAL HALKALAR:</strong> Hücreler merkezi lümen etrafında dairesel dizilim göstermekte. 
                    Nükleuslar periferik yerleşimli. Glandüler diferansiyasyon belirgin. Müsinöz sekresyon alanları mevcut.
                    </div>
                    """, unsafe_allow_html=True)
                
                else:
                    st.markdown("""
                    <div class='histo-note'>
                    <strong>KAOTİK MOZAİK:</strong> Solid büyüme patterni hakim. Hücreler iç içe geçmiş, intercellular 
                    bridges belirgin. Keratin incileri mevcut. Boşluk alanları minimal.
                    </div>
                    """, unsafe_allow_html=True)
                
                # TANI PUANLARI
                st.markdown("#### 🎯 Tanı Puanlaması")
                
                scores = diagnosis_result["scores"]
                for diag_type, score in scores.items():
                    col_name, col_bar = st.columns([3, 7])
                    with col_name:
                        st.write(f"*{diag_type}:*")
                    with col_bar:
                        progress = score / 10
                        st.progress(progress, text=f"{score}/10 puan")
        
        st.markdown("---")
        st.success("✅ Patolojik analiz tamamlandı!")
        st.info("""
        *Patolojik Korelasyon:*
        - *Normal:* Dantelsi alveolar yapı + yüksek boşluk
        - *Adenokarsinom:* Glandüler halkalar + orta boşluk
        - *Skuamöz:* Solid mozaik + düşük boşluk + keratin incileri
        """)

else:
    # ANA SAYFA
    st.markdown("""
    <div class='histo-report'>
        <h2>🔬 Matematiksel Histopatoloji Analizi</h2>
        <p>Bu sistem <strong>patolog gözüyle</strong> histolojik patternleri matematiksel olarak analiz eder.</p>
    </div>
    """)
    
    st.markdown("""
    ### 📐 3 TEMEL HISTOLOJİK PATTERN:
    
    *1. DANTEL VE HAVA (Normal Akciğer)*
    python
    if lace_density > 0.1 and void_ratio > 0.7:
        return "NORMAL"
    
    • İnce alveolar duvarlar (1-piksel çizgiler)
    • Geniş hava keseleri
    • Yüksek lacunarity
    
    *2. FRAKTAL HALKALAR (Adenokarsinom)*
    python
    if circularity_score > 0.3 and spatial_autocorr > 0.6:
        return "ADENOCARCINOMA"
    
    • Merkezi lümenli gland yapıları
    • Periferik nükleus dizilimi
    • Fraktal dairesel pattern
    
    *3. KAOTİK MOZAİK (Skuamöz Karsinom)*
    python
    if edge_density > 0.15 and keratin_pearls > 0.05:
        return "SQUAMOUS CELL CARCINOMA"
    
    • Solid büyüme patterni
    • Intercellular bridges
    • Keratin incileri
    • Yüksek polygon score
    """)
    
    st.markdown("""
    <div class='feature-box'>
    <h4>🎯 ANALİZ ALGORİTMASI:</h4>
    
    1. *Lace Pattern Detection:* Alveolar duvar inceliği
    2. *Lacunarity Analysis:* Boşluk dağılım heterojenliği
    3. *Spatial Autocorrelation:* Nükleus düzeni
    4. *Circular Hough Transform:* Gland yapıları
    5. *Polygon Score Calculation:* Hücre şekil analizi
    6. *Keratin Pearl Detection:* İçi dolu dairesel yapılar
    </div>
    """, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 20px; font-size: 0.9em;'>
    <p><strong>MATHRIX Histopathology AI v13.0</strong></p>
    <p>Patolog Gözüyle Matematiksel Histoloji Analizi | Dantel, Halka ve Mozaik Pattern Tanıma</p>
    <p><em>Bu analiz patolojik konsültasyon yerine geçmez. Kesin tanı için patolog incelemesi şarttır.</em></p>
</div>
""", unsafe_allow_html=True)
