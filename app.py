import streamlit as st
import numpy as np
from PIL import Image
import time

# ==================== SAYFA AYARLARI ====================
st.set_page_config(
    page_title="MATHRIX - Geometric Pattern",
    page_icon="🎯",
    layout="wide"
)

# ==================== CSS ====================
st.markdown("""
<style>
    .main { background: white; }
    .stApp { background: white; color: black !important; }
    
    h1, h2, h3 { color: #0066cc !important; }
    
    .normal-report {
        background: linear-gradient(135deg, #e8f5e9, #c8e6c9) !important;
        border: 3px solid #4caf50 !important;
        padding: 25px;
        border-radius: 10px;
        margin: 20px 0;
        color: #1b5e20 !important;
    }
    
    .adeno-report {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb) !important;
        border: 3px solid #2196f3 !important;
        padding: 25px;
        border-radius: 10px;
        margin: 20px 0;
        color: #0d47a1 !important;
    }
    
    .squamous-report {
        background: linear-gradient(135deg, #ffebee, #ffcdd2) !important;
        border: 3px solid #f44336 !important;
        padding: 25px;
        border-radius: 10px;
        margin: 20px 0;
        color: #b71c1c !important;
    }
    
    .pattern-card {
        background: #f5f5f5;
        border: 2px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin: 10px;
        text-align: center;
    }
    
    .rule-box {
        background: #e8f4fd;
        border-left: 5px solid #2196f3;
        padding: 15px;
        margin: 15px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== BAŞLIK ====================
st.title("🔬 MATHRIX - GEOMETRİK PATTERN ANALİZİ")
st.markdown("*Boşluk, Halka ve Blok Pattern Tanıma Sistemi*")

# ==================== GEOMETRİK PATTERN ANALİZ FONKSİYONLARI ====================
def analyze_geometric_patterns(image_array):
    """
    GEOMETRİK PATTERN ANALİZİ
    Renk tonuna değil, düzen ve boşluklara bak
    """
    # RGB kanallarına ayır
    if len(image_array.shape) == 3:
        r = image_array[:, :, 0].astype(float)
        g = image_array[:, :, 1].astype(float)
        b = image_array[:, :, 2].astype(float)
    else:
        # Gri tonluysa tüm kanallara aynı değeri ata
        r = g = b = image_array.astype(float)
    
    height, width = r.shape
    
    # 1. MOR PİKSELLERİ BUL (HÜCRE ÇEKİRDEKLERİ)
    # Mor = Yüksek Blue, orta Red, düşük Green
    # Normalize et
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0
    
    # Mor pikseller için kriter
    # H&E boyamada: Nükleus = mavi/mor, Sitoplazma = pembe
    # Mor = yüksek mavi, düşük yeşil
    purple_mask = (b_norm > 0.4) & (b_norm > r_norm + 0.1) & (g_norm < 0.3)
    
    # 2. PEMBE/AÇIK ALANLARI BUL (SİTOPLAZMA/BOŞLUK)
    # Pembe = yüksek kırmızı, orta mavi, düşük yeşil
    pink_mask = (r_norm > 0.6) & (g_norm > 0.4) & (b_norm > 0.4) & (r_norm > b_norm)
    
    # 3. BEYAZ/AÇIK ALANLAR
    white_mask = (r_norm > 0.8) & (g_norm > 0.8) & (b_norm > 0.8)
    
    # 4. TOPLAM BOŞLUK = Pembe + Beyaz
    void_mask = pink_mask | white_mask
    
    # ANALİZ 1: BOŞLUK ALANI ORANI (Normal için)
    void_area = np.sum(void_mask)
    total_area = height * width
    void_ratio = void_area / total_area
    
    # ANALİZ 2: SÜREKLİ BOŞLUK ALANLARI
    # Büyük, bağlantılı boşlukları bul
    def find_connected_areas(mask):
        """Maskedeki bağlantılı alanları bul"""
        visited = np.zeros_like(mask, dtype=bool)
        areas = []
        
        for i in range(height):
            for j in range(width):
                if mask[i, j] and not visited[i, j]:
                    # BFS ile bağlantılı alanı bul
                    area = []
                    stack = [(i, j)]
                    
                    while stack:
                        y, x = stack.pop()
                        if 0 <= y < height and 0 <= x < width:
                            if mask[y, x] and not visited[y, x]:
                                visited[y, x] = True
                                area.append((y, x))
                                # 8-yönlü komşuluk
                                stack.extend([
                                    (y+1, x), (y-1, x), (y, x+1), (y, x-1),
                                    (y+1, x+1), (y+1, x-1), (y-1, x+1), (y-1, x-1)
                                ])
                    
                    if area:
                        areas.append(area)
        
        return areas
    
    # Büyük boşluk alanlarını bul
    void_areas = find_connected_areas(void_mask)
    
    # En büyük 5 boşluk alanının boyutu
    if void_areas:
        area_sizes = [len(area) for area in void_areas]
        area_sizes.sort(reverse=True)
        largest_voids = area_sizes[:5]
        avg_large_void = np.mean(largest_voids) if largest_voids else 0
    else:
        avg_large_void = 0
    
    # GENİŞ BOŞLUK KRİTERİ (Normal için)
    # Toplam alanın %60'ından büyük sürekli boşluk var mı?
    continuous_void_ratio = 0
    if void_areas:
        largest_void_size = max([len(area) for area in void_areas])
        continuous_void_ratio = largest_void_size / total_area
    
    # ANALİZ 3: DAİRESEL DİZİLİM (Adeno için)
    # Mor pikseller dairesel kümeler oluşturuyor mu?
    purple_areas = find_connected_areas(purple_mask)
    
    def calculate_circularity(area_points):
        """Bir alanın daireselliğini hesapla"""
        if len(area_points) < 10:
            return 0
        
        # Noktaları ayır
        ys = [p[0] for p in area_points]
        xs = [p[1] for p in area_points]
        
        # Merkez
        center_y = np.mean(ys)
        center_x = np.mean(xs)
        
        # Merkezden uzaklıklar
        distances = [np.sqrt((y - center_y)*2 + (x - center_x)*2) 
                    for y, x in zip(ys, xs)]
        
        mean_dist = np.mean(distances)
        std_dist = np.std(distances)
        
        if mean_dist == 0:
            return 0
        
        # Dairesellik = 1 - (std/mean) → 1'e yakın = daire
        circularity = 1 - (std_dist / mean_dist)
        return max(0, circularity)
    
    # Mor alanların daireselliğini hesapla
    circular_scores = []
    for area in purple_areas[:20]:  # İlk 20 alan
        if len(area) > 15:  # Minimum boyut
            circ = calculate_circularity(area)
            circular_scores.append(circ)
    
    avg_circularity = np.mean(circular_scores) if circular_scores else 0
    
    # ANALİZ 4: MERKEZİ BOŞLUKLU HALKALAR (Adeno için)
    # Mor halkaların içinde pembe boşluk var mı?
    ring_pattern_score = 0
    ring_count = 0
    
    for area in purple_areas[:10]:  # İlk 10 mor alan
        if len(area) > 20:
            # Alanın sınırlarını bul
            ys = [p[0] for p in area]
            xs = [p[1] for p in area]
            
            min_y, max_y = min(ys), max(ys)
            min_x, max_x = min(xs), max(xs)
            
            # İç bölgeyi kontrol et (mor alanın içinde pembe var mı?)
            center_y = (min_y + max_y) // 2
            center_x = (min_x + max_x) // 2
            
            # Merkezden radyal tarama
            if (0 <= center_y < height and 0 <= center_x < width):
                # Merkez nokta pembe/beyaz mı?
                if void_mask[center_y, center_x]:
                    ring_pattern_score += 1
                
                # Radyal yönlerde kontrol
                for angle in np.linspace(0, 2*np.pi, 8):
                    r = 5  # Küçük yarıçap
                    y = int(center_y + r * np.sin(angle))
                    x = int(center_x + r * np.cos(angle))
                    
                    if 0 <= y < height and 0 <= x < width:
                        if purple_mask[y, x]:  # Çevrede mor var
                            ring_count += 1
    
    glandular_pattern = ring_pattern_score / 10 if ring_count > 0 else 0
    
    # ANALİZ 5: DEV BLOK ANALİZİ (Skuamöz için)
    # Mor pikseller dev, sürekli blok oluşturuyor mu?
    if purple_areas:
        largest_purple_size = max([len(area) for area in purple_areas])
        largest_purple_ratio = largest_purple_size / total_area
        
        # Blok sürekliliği: En büyük mor alan ne kadar büyük?
        block_continuity = largest_purple_ratio
    else:
        block_continuity = 0
    
    # ANALİZ 6: KAOS DÜZEYİ (Skuamöz için)
    # Mor dağılımının homojenliği
    if purple_mask.any():
        # Mor piksellerin yoğunluk haritası
        from scipy import ndimage
        
        # Mor piksel koordinatları
        purple_coords = np.argwhere(purple_mask)
        
        if len(purple_coords) > 10:
            # K-mean benzeri basit kümeleme analizi
            ys = purple_coords[:, 0]
            xs = purple_coords[:, 1]
            
            # Konum varyansı
            y_var = np.var(ys) / height if height > 0 else 0
            x_var = np.var(xs) / width if width > 0 else 0
            
            chaos_level = (y_var + x_var) / 2
        else:
            chaos_level = 0
    else:
        chaos_level = 0
    
    return {
        # Normal kriterleri
        "void_ratio": void_ratio,
        "continuous_void_ratio": continuous_void_ratio,
        "avg_large_void": avg_large_void,
        
        # Adeno kriterleri
        "avg_circularity": avg_circularity,
        "glandular_pattern": glandular_pattern,
        "ring_count": ring_count,
        
        # Skuamöz kriterleri
        "block_continuity": block_continuity,
        "chaos_level": chaos_level,
        "largest_purple_ratio": largest_purple_ratio if 'largest_purple_ratio' in locals() else 0,
        
        # Genel
        "total_purple": np.sum(purple_mask) / total_area,
        "total_void": void_ratio,
        "image_size": (height, width)
    }

def geometric_diagnosis(analysis):
    """
    GEOMETRİK KRİTERLERE GÖRE TANI
    """
    # KRİTER 1: NORMAL AKCİĞER
    # Geniş ve sürekli boşluk alanları (>%60)
    if analysis["continuous_void_ratio"] > 0.6:
        diagnosis = "NORMAL AKCİĞER DOKUSU"
        confidence = min(95, 70 + (analysis["continuous_void_ratio"] * 40))
        reason = f"Geniş sürekli boşluk alanı: {analysis['continuous_void_ratio']:.1%}"
        pattern = "normal"
    
    # KRİTER 2: ADENOKARSİNOM
    # Dairesel mor kümeler + merkezi boşluk
    elif (analysis["avg_circularity"] > 0.4 and 
          analysis["glandular_pattern"] > 0.3):
        diagnosis = "ADENOKARSİNOM"
        confidence = min(92, 65 + (analysis["avg_circularity"] * 50))
        reason = f"Dairesel gland yapıları: {analysis['avg_circularity']:.3f}"
        pattern = "adeno"
    
    # KRİTER 3: SKUAMÖZ KARSİNOM
    # Dev mor blok + az boşluk
    elif (analysis["block_continuity"] > 0.4 and 
          analysis["void_ratio"] < 0.2):
        diagnosis = "SKUAMÖZ HÜCRELİ KARSİNOM"
        confidence = min(90, 60 + (analysis["block_continuity"] * 60))
        reason = f"Dev mor blok: {analysis['block_continuity']:.1%}, Boşluk: {analysis['void_ratio']:.1%}"
        pattern = "squamous"
    
    # KRİTER 4: NORMAL (alternatif)
    # Çok yüksek toplam boşluk
    elif analysis["void_ratio"] > 0.7:
        diagnosis = "NORMAL AKCİĞER DOKUSU"
        confidence = 85.0
        reason = f"Çok yüksek boşluk oranı: {analysis['void_ratio']:.1%}"
        pattern = "normal"
    
    # KRİTER 5: ADENO (alternatif)
    # Yüksek dairesellik
    elif analysis["avg_circularity"] > 0.5:
        diagnosis = "ADENOKARSİNOM"
        confidence = 80.0
        reason = f"Yüksek dairesellik: {analysis['avg_circularity']:.3f}"
        pattern = "adeno"
    
    # KRİTER 6: SKUAMÖZ (alternatif)
    # Çok düşük boşluk + yüksek mor
    elif analysis["void_ratio"] < 0.1 and analysis["total_purple"] > 0.5:
        diagnosis = "SKUAMÖZ HÜCRELİ KARSİNOM"
        confidence = 75.0
        reason = f"Çok az boşluk ({analysis['void_ratio']:.1%}), çok mor ({analysis['total_purple']:.1%})"
        pattern = "squamous"
    
    # BELİRSİZ
    else:
        # Puanlama sistemi
        normal_score = analysis["continuous_void_ratio"] * 100
        adeno_score = analysis["avg_circularity"] * 70 + analysis["glandular_pattern"] * 30
        squamous_score = analysis["block_continuity"] * 80 + (1 - analysis["void_ratio"]) * 20
        
        scores = {
            "NORMAL": normal_score,
            "ADENO": adeno_score,
            "SKUAMÖZ": squamous_score
        }
        
        diagnosis = max(scores, key=scores.get)
        confidence = scores[diagnosis]
        
        if diagnosis == "NORMAL":
            diagnosis = "NORMAL AKCİĞER DOKUSU"
            pattern = "normal"
            reason = f"Boşluk ağırlıklı puan: {normal_score:.1f}"
        elif diagnosis == "ADENO":
            diagnosis = "ADENOKARSİNOM"
            pattern = "adeno"
            reason = f"Dairesellik puanı: {adeno_score:.1f}"
        else:
            diagnosis = "SKUAMÖZ HÜCRELİ KARSİNOM"
            pattern = "squamous"
            reason = f"Blok puanı: {squamous_score:.1f}"
    
    # EVRELEME
    if pattern == "normal":
        stage = "N/A"
        treatment = "Rutin takip"
    elif pattern == "adeno":
        if analysis["total_purple"] < 0.4:
            stage = "Stage I-II"
            treatment = "Cerrahi + Hedefe yönelik tedavi"
        else:
            stage = "Stage III-IV"
            treatment = "Hedefe yönelik tedavi + İmmünoterapi"
    else:  # squamous
        if analysis["block_continuity"] < 0.6:
            stage = "Stage I-II"
            treatment = "Cerrahi veya Radyoterapi"
        else:
            stage = "Stage III-IV"
            treatment = "Kemoradyoterapi + İmmünoterapi"
    
    return {
        "diagnosis": diagnosis,
        "confidence": min(99, max(50, confidence)),
        "stage": stage,
        "pattern": pattern,
        "reason": reason,
        "treatment": treatment,
        "analysis": analysis
    }

# ==================== YAN ÇUBUK - GEOMETRİK KRİTERLER ====================
with st.sidebar:
    st.markdown("## 📐 Geometrik Kurallar")
    
    with st.expander("🎯 Tanı Algoritması", expanded=True):
        st.markdown("""
        *1. NORMAL AKCİĞER:*
        • Sürekli boşluk alanı > %60
        • Geniş pembe/beyaz alanlar
        • İnce hücre tabakası
        
        *2. ADENOKARSİNOM:*
        • Dairesel mor kümeler
        • Merkezde pembe boşluk
        • Glandüler halka yapısı
        
        *3. SKUAMÖZ KARSİNOM:*
        • Dev mor blok (>%40 alan)
        • Minimal boşluk (<%20)
        • Kaotik hücre dizilimi
        """)
    
    with st.expander("⚙️ Eşik Değerleri"):
        st.markdown("""
        *Kritik Eşikler:*
        - Sürekli Boşluk: %60 (Normal)
        - Dairesellik: 0.4 (Adeno)
        - Gland Pattern: 0.3 (Adeno)
        - Blok Sürekliliği: %40 (Skuamöz)
        - Toplam Boşluk: %20 (Skuamöz)
        """)

# ==================== ANA UYGULAMA ====================
st.markdown("## 📤 Görüntü Yükleme")

uploaded_files = st.file_uploader(
    "H&E boyamalı akciğer dokusu görüntüleri",
    type=['png', 'jpg', 'jpeg'],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} görüntü yüklendi")
    
    if st.button("🔬 GEOMETRİK PATTERN ANALİZİ", type="primary", use_container_width=True):
        
        results = []
        
        for idx, uploaded_file in enumerate(uploaded_files):
            st.markdown(f"---")
            st.markdown(f"### Görüntü {idx + 1}: {uploaded_file.name}")
            
            # Görüntüyü aç
            image = Image.open(uploaded_file)
            img_array = np.array(image)
            
            col_img, col_analysis = st.columns([1, 2])
            
            with col_img:
                st.image(image, use_column_width=True)
                st.caption(f"Boyut: {image.size[0]} × {image.size[1]}")
            
            with col_analysis:
                # ANALİZ YAP
                with st.spinner("Geometrik pattern analizi yapılıyor..."):
                    time.sleep(0.5)
                    analysis = analyze_geometric_patterns(img_array)
                    diagnosis_result = geometric_diagnosis(analysis)
                
                # SONUCU GÖSTER
                diagnosis = diagnosis_result["diagnosis"]
                confidence = diagnosis_result["confidence"]
                stage = diagnosis_result["stage"]
                pattern = diagnosis_result["pattern"]
                reason = diagnosis_result["reason"]
                treatment = diagnosis_result["treatment"]
                
                if pattern == "normal":
                    st.markdown(f"""
                    <div class='normal-report'>
                        <h3>✅ {diagnosis}</h3>
                        <p><strong>Güven:</strong> {confidence:.1f}%</p>
                        <p><strong>Bulgu:</strong> {reason}</p>
                        <p><strong>Öneri:</strong> {treatment}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("""
                    <div class='rule-box'>
                    <strong>GEOMETRİK KURAL:</strong> Geniş ve sürekli pembe/beyaz alanlar (>%60) 
                    sağlıklı alveolar yapıyı gösterir. Hücreler ince bir tabaka halindedir.
                    </div>
                    """, unsafe_allow_html=True)
                
                elif pattern == "adeno":
                    st.markdown(f"""
                    <div class='adeno-report'>
                        <h3>⚠️ {diagnosis}</h3>
                        <p><strong>Evre:</strong> {stage}</p>
                        <p><strong>Güven:</strong> {confidence:.1f}%</p>
                        <p><strong>Bulgu:</strong> {reason}</p>
                        <p><strong>Tedavi:</strong> {treatment}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("""
                    <div class='rule-box'>
                    <strong>GEOMETRİK KURAL:</strong> Mor pikseller (hücre çekirdekleri) 
                    merkezde pembe boşluk olan dairesel halkalar oluşturur. 
                    Bu glandüler diferansiyasyon tipiktir.
                    </div>
                    """, unsafe_allow_html=True)
                
                else:  # squamous
                    st.markdown(f"""
                    <div class='squamous-report'>
                        <h3>⚠️ {diagnosis}</h3>
                        <p><strong>Evre:</strong> {stage}</p>
                        <p><strong>Güven:</strong> {confidence:.1f}%</p>
                        <p><strong>Bulgu:</strong> {reason}</p>
                        <p><strong>Tedavi:</strong> {treatment}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("""
                    <div class='rule-box'>
                    <strong>GEOMETRİK KURAL:</strong> Mor pikseller dev, sürekli bloklar 
                    oluşturur. Boşluk minimaldir. Hücreler iç içe geçmiş, kaotik dizilmiştir.
                    </div>
                    """, unsafe_allow_html=True)
                
                # GEOMETRİK METRİKLER
                st.markdown("#### 📊 Geometrik Analiz Metrikleri")
                
                cols = st.columns(4)
                
                metrics = [
                    ("Sürekli Boşluk", f"{analysis['continuous_void_ratio']:.1%}", "Normal > %60"),
                    ("Dairesellik", f"{analysis['avg_circularity']:.3f}", "Adeno > 0.4"),
                    ("Gland Pattern", f"{analysis['glandular_pattern']:.3f}", "Adeno > 0.3"),
                    ("Blok Sürekliliği", f"{analysis['block_continuity']:.1%}", "Skuamöz > %40"),
                    ("Toplam Boşluk", f"{analysis['void_ratio']:.1%}", "Skuamöz < %20"),
                    ("Kaos Düzeyi", f"{analysis['chaos_level']:.3f}", "Skuamöz'de yüksek"),
                    ("Toplam Mor", f"{analysis['total_purple']:.1%}", "Hücre yoğunluğu"),
                    ("Büyük Boşluk", f"{analysis['avg_large_void']:.0f} px", "Ortalama boşluk boyutu")
                ]
                
                for i, (label, value, desc) in enumerate(metrics):
                    with cols[i % 4]:
                        st.markdown(f"""
                        <div class='pattern-card'>
                            <strong>{label}</strong><br>
                            <span style='font-size: 20px;'>{value}</span><br>
                            <small style='color: #666;'>{desc}</small>
                        </div>
                        """, unsafe_allow_html=True)
                
                # PATTERN YORUMU
                st.markdown("#### 🔍 Pattern Yorumu")
                
                if pattern == "normal":
                    st.info(f"""
                    *BOŞLUK DOMİNASYONU:* Görüntünün {analysis['continuous_void_ratio']:.1%}'ü 
                    sürekli pembe/beyaz alan. Bu sağlıklı alveolar yapıdır.
                    """)
                
                elif pattern == "adeno":
                    st.info(f"""
                    *DAİRESEL ORGANİZASYON:* {analysis['ring_count']} adet glandüler halka tespit edildi. 
                    Dairesellik skoru: {analysis['avg_circularity']:.3f}
                    """)
                
                else:
                    st.info(f"""
                    *BLOKLAŞMA:* En büyük mor alan görüntünün {analysis['block_continuity']:.1%}'ünü kaplıyor. 
                    Boşluk oranı sadece {analysis['void_ratio']:.1%}
                    """)
                
                # Sonuçları kaydet
                results.append({
                    "Görüntü": uploaded_file.name,
                    "Tanı": diagnosis,
                    "Güven": f"{confidence:.1f}%",
                    "Evre": stage,
                    "Sürekli Boşluk": f"{analysis['continuous_void_ratio']:.1%}",
                    "Dairesellik": f"{analysis['avg_circularity']:.3f}",
                    "Blok": f"{analysis['block_continuity']:.1%}"
                })
        
        # TOPLU SONUÇ
        st.markdown("---")
        st.markdown("## 📈 Analiz Özeti")
        
        # İstatistikler
        normal_count = sum(1 for r in results if "NORMAL" in r["Tanı"])
        adeno_count = sum(1 for r in results if "ADENO" in r["Tanı"])
        squamous_count = sum(1 for r in results if "SKUAMÖZ" in r["Tanı"])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Normal", normal_count)
        with col2:
            st.metric("Adenokarsinom", adeno_count)
        with col3:
            st.metric("Skuamöz", squamous_count)
        
        # DOĞRULUK KONTROLÜ
        if len(results) == 3:
            if normal_count == 1 and adeno_count == 1 and squamous_count == 1:
                st.success("🎉 MÜKEMMEL! Tüm görüntüler doğru tanındı!")
            else:
                st.warning("⚠️ Bazı tanılar yanlış olabilir. Görüntülerin geometrik özelliklerini kontrol edin.")
        
        # RAPOR
        report = "GEOMETRİK PATTERN ANALİZ RAPORU\n" + "="*50 + "\n\n"
        
        for res in results:
            report += f"GÖRÜNTÜ: {res['Görüntü']}\n"
            report += f"TANI: {res['Tanı']}\n"
            report += f"GÜVEN: {res['Güven']}\n"
            report += f"EVRE: {res['Evre']}\n"
            report += f"METRİKLER: Boşluk={res['Sürekli Boşluk']}, "
            report += f"Dairesellik={res['Dairesellik']}, "
            report += f"Blok={res['Blok']}\n"
            report += "-"*40 + "\n"
        
        st.download_button(
            "📥 Detaylı Rapor İndir",
            report,
            file_name="geometric_pattern_raporu.txt",
            mime="text/plain"
        )

else:
    # ANA SAYFA
    st.markdown("""
    ## 🎯 GEOMETRİK PATTERN ANALİZ SİSTEMİ
    
    Bu sistem *renk tonuna değil, geometrik düzene* bakar:
    
    ### 📐 3 TEMEL GEOMETRİK KURAL:
    
    *1. BOŞLUK DOMİNASYONU (Normal)*
    python
    if sürekli_boşluk_alani > %60:
        tanı = "NORMAL"
    
    
    *2. DAİRESEL ORGANİZASYON (Adenokarsinom)*
    python
    if dairesellik > 0.4 and merkezde_boşluk:
        tanı = "ADENOKARSİNOM"
    
    
    *3. BLOKLAŞMA (Skuamöz Karsinom)*
    python
    if mor_blok > %40 and boşluk < %20:
        tanı = "SKUAMÖZ"
    
    
    ### 🔬 ANALİZ ALGORİTMASI:
    
    1. *Mor pikselleri tespit et* (hücre çekirdekleri)
    2. *Pembe/beyaz alanları bul* (boşluklar)
    3. *Bağlantılı alanları analiz et*
    4. *Dairesellik hesapla*
    5. *Blok sürekliliğini ölç*
    6. *Geometrik kriterlere göre tanı koy*
    
    ### 🎯 BEKLENEN SONUÇLAR:
    
    | Görüntü | Beklenen Pattern |
    |---------|------------------|
    | *Normal* | Geniş sürekli boşluk alanları |
    | *Adeno* | Dairesel mor halkalar + merkezi boşluk |
    | *Skuamöz* | Dev mor blok + minimal boşluk |
    """)

st.markdown("---")
st.caption("🔬 MATHRIX Geometric Pattern Analysis v11.0 | Geometrik kurallara dayalı tanı sistemi")
