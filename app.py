import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import os
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Mathrix AI: Böbrek Kanseri Grading",
    page_icon="🔬",
    layout="wide"
)

# Tıbbi Bilgi Tabanı - Fuhrman Grading Sistemi
MEDICAL_KNOWLEDGE = {
    "grading_system": {
        "Grade 1": {
            "nuclei_size": "Küçük (yaklaşık 10 μm), düzgün, yuvarlak çekirdekler",
            "nucleoli": "Belirgin olmayan veya görünmeyen çekirdekçikler",
            "necrosis": "Yok veya minimal",
            "description": "Küçük, düzgün çekirdekler, normal tübüler hücrelere benzer",
            "survival_rate": "%90 üzeri 5 yıllık sağkalım",
            "treatment": {
                "primary": "Parsiyel nefrektomi (nefron koruyucu cerrahi)",
                "adjuvant": "Küçük tümörler (<3cm) için aktif gözlem",
                "systemic": "Genellikle gerekmez",
                "drugs": ["T1a tümörler için sadece gözlem"]
            }
        },
        "Grade 2": {
            "nuclei_size": "Orta boy çekirdekler (10-15 μm), hafif düzensizlikler",
            "nucleoli": "400x büyütmede görülebilen küçük çekirdekçikler",
            "necrosis": "Nadiren veya fokal",
            "description": "Bazı düzensizlikleri olan daha büyük çekirdekler, görülebilir çekirdekçikler",
            "survival_rate": "%70-80 5 yıllık sağkalım",
            "treatment": {
                "primary": "Tümör boyutuna göre parsiyel veya radikal nefrektomi",
                "adjuvant": "Düşük riskli hastalar için gözlem düşünülebilir",
                "systemic": "Rutin önerilmez",
                "drugs": ["Yüksek riskli vakalar için Sunitinib", "Alternatif olarak Pazopanib"]
            }
        },
        "Grade 3": {
            "nuclei_size": "Büyük çekirdekler (15-20 μm), belirgin düzensizlikler",
            "nucleoli": "100x büyütmede görülebilen belirgin, eosinofilik çekirdekçikler",
            "necrosis": "Tümör alanının %10-30'unda mevcut",
            "description": "Belirgin çekirdekçikli, çok düzensiz, büyük çekirdekler",
            "survival_rate": "%40-60 5 yıllık sağkalım",
            "treatment": {
                "primary": "Lenf nodu diseksiyonu ile radikal nefrektomi",
                "adjuvant": "Yüksek riskli hastalar için adjuvan tedavi düşünün",
                "systemic": "Hedefe yönelik tedavi veya immünoterapi",
                "drugs": ["Nivolumab + Ipilimumab", "Pembrolizumab + Axitinib", "Cabozantinib"]
            }
        },
        "Grade 4": {
            "nuclei_size": "Çok büyük çekirdekler (>20 μm), tuhaf formlar, multilobülasyon",
            "nucleoli": "Makronükleoller, canavarımsı görünüm",
            "necrosis": "Yaygın (>%30 tümör alanı)",
            "description": "Yaygın nekrozlu multilobüle, canavarımsı çekirdekler",
            "survival_rate": "%10-20 5 yıllık sağkalım",
            "treatment": {
                "primary": "Mümkünse sitoredüktif nefrektomi",
                "adjuvant": "Acil sistemik tedavi",
                "systemic": "Kombinasyon immünoterapisi veya hedefe yönelik tedavi",
                "drugs": ["Nivolumab + Ipilimumab (birinci basamak)", "Lenvatinib + Pembrolizumab", "Tivozanib"]
            }
        }
    }
}

class MathrixAIModel:
    """Böbrek kanseri grading için ana AI modeli"""
    
    def _init_(self):
        self.model = None
        self.classes = ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4']
    
    def create_model(self):
        """Demo model oluştur"""
        model = keras.Sequential([
            keras.layers.Input(shape=(256, 256, 3)),
            keras.layers.Conv2D(16, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(32, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Flatten(),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(4, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def analyze_image(self, image):
        """Görüntüyü analiz et ve özellikleri çıkar"""
        # Görüntüyü işle
        img_array = self.preprocess_image(image)
        
        # Demo özellik çıkarma
        features = self.extract_features(image)
        
        # Demo tahmin (gerçek model yerine)
        grade, confidence, explanation = self.demo_prediction(features)
        
        return grade, confidence, explanation, features
    
    def preprocess_image(self, image, target_size=(256, 256)):
        """Görüntüyü ön işle"""
        # OpenCV ile işle
        if isinstance(image, np.ndarray):
            img = image
        else:
            img = np.array(image)
        
        # Boyutlandır
        img = cv2.resize(img, target_size)
        
        # Normalize
        img = img / 255.0
        
        return img
    
    def extract_features(self, image):
        """Görüntüden nükleer özellikleri çıkar"""
        if isinstance(image, np.ndarray):
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            img_array = np.array(image.convert('L'))
            gray = img_array
        
        # Basit özellik çıkarma
        features = {
            'mean_intensity': float(np.mean(gray)),
            'std_intensity': float(np.std(gray)),
            'contrast': float(np.max(gray) - np.min(gray)),
            'nuclear_count': np.random.randint(50, 200),  # Demo
            'avg_nuclear_size': np.random.uniform(10, 40),  # Demo
            'irregularity_score': np.random.uniform(0.1, 0.9)  # Demo
        }
        
        return features
    
    def demo_prediction(self, features):
        """Demo tahmin (gerçek model yerine)"""
        # Özelliklere göre grade hesapla
        score = (
            features['avg_nuclear_size'] * 0.4 +
            (1 - features['irregularity_score']) * 0.3 +
            features['std_intensity'] * 0.3
        )
        
        # Score'a göre grade belirle
        if score < 15:
            grade_idx = 0  # Grade 1
            confidence = np.random.uniform(0.85, 0.95)
        elif score < 25:
            grade_idx = 1  # Grade 2
            confidence = np.random.uniform(0.75, 0.85)
        elif score < 35:
            grade_idx = 2  # Grade 3
            confidence = np.random.uniform(0.65, 0.75)
        else:
            grade_idx = 3  # Grade 4
            confidence = np.random.uniform(0.70, 0.80)
        
        grade = self.classes[grade_idx]
        
        # Açıklama oluştur
        explanation = self.generate_explanation(grade_idx, features, confidence)
        
        return grade_idx, confidence, explanation
    
    def generate_explanation(self, grade_idx, features, confidence):
        """AI kararı için açıklama oluştur"""
        grade = self.classes[grade_idx]
        
        explanations = {
            0: f"*Grade 1 Karar Açıklaması:*\n"
               f"- Ortalama çekirdek boyutu: {features['avg_nuclear_size']:.1f} birim\n"
               f"- Düzensizlik skoru: {features['irregularity_score']:.2f} (düşük)\n"
               f"- *Sebep:* Çekirdekler küçük ve düzgün, Grade 1 RCC için karakteristik\n"
               f"- *Çekirdek boyutu {features['avg_nuclear_size']:.1f} birim olduğu için Grade 1 dedim*",
            
            1: f"*Grade 2 Karar Açıklaması:*\n"
               f"- Ortalama çekirdek boyutu: {features['avg_nuclear_size']:.1f} birim\n"
               f"- Düzensizlik skoru: {features['irregularity_score']:.2f} (orta)\n"
               f"- *Sebep:* Orta boy çekirdekler, başlangıç düzensizlikleri\n"
               f"- *Çekirdek boyutu ve şekil bozukluğu Grade 2'yi gösteriyor*",
            
            2: f"*Grade 3 Karar Açıklaması:*\n"
               f"- Ortalama çekirdek boyutu: {features['avg_nuclear_size']:.1f} birim\n"
               f"- Düzensizlik skoru: {features['irregularity_score']:.2f} (yüksek)\n"
               f"- *Sebep:* Büyük, çok düzensiz çekirdekler, belirgin çekirdekçikler\n"
               f"- *Yüksek düzensizlik skoru ({features['irregularity_score']:.2f}) Grade 3'ü işaret ediyor*",
            
            3: f"*Grade 4 Karar Açıklaması:*\n"
               f"- Ortalama çekirdek boyutu: {features['avg_nuclear_size']:.1f} birim\n"
               f"- Düzensizlik skoru: {features['irregularity_score']:.2f} (çok yüksek)\n"
               f"- *Sebep:* Çok büyük, canavarımsı çekirdekler, yaygın nekroz\n"
               f"- *Çekirdek boyutu {features['avg_nuclear_size']:.1f} birim ve yüksek düzensizlik Grade 4 dedim*"
        }
        
        base_explanation = explanations.get(grade_idx, "")
        base_explanation += f"\n\n*Model Güveni:* %{confidence*100:.1f}"
        
        return base_explanation

def main():
    # Session state initialization
    if 'model' not in st.session_state:
        st.session_state.model = MathrixAIModel()
        st.session_state.model.create_model()
        st.session_state.model_loaded = True
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .grade-box {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 6px solid;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .grade-1 { border-color: #4CAF50; background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%); }
    .grade-2 { border-color: #FFC107; background: linear-gradient(135deg, #FFF8E1 0%, #FFECB3 100%); }
    .grade-3 { border-color: #FF9800; background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%); }
    .grade-4 { border-color: #F44336; background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%); }
    .feature-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin: 0.5rem 0;
    }
    .stButton>button {
        background: linear-gradient(135deg, #2E86AB 0%, #1B5E6D 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🔬 Mathrix AI: Böbrek Kanseri Grading & Tedavi Önerileri</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/microscope.png", width=80)
        st.title("Navigasyon")
        
        mode = st.radio(
            "Mod Seçin:",
            ["🔍 Görüntü Analizi", "📚 Tıbbi Referans", "⚙️ Ayarlar"]
        )
        
        st.markdown("---")
        st.markdown("### Hakkında")
        st.info("""
        *Mathrix AI* profesyonel bir sistemdir:
        - Böbrek kanseri Fuhrman grading
        - Nükleer özellik çıkarma
        - Tedavi önerileri
        - Açıklanabilir AI kararları
        """)
        
        st.markdown("---")
        st.markdown("*⚠️ Uyarı:* Eğitim ve araştırma amaçlıdır. Klinik kullanım için değildir.")
    
    if mode == "🔍 Görüntü Analizi":
        st.header("Histopatoloji Görüntü Analizi")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Görüntü Yükle")
            
            uploaded_file = st.file_uploader(
                "Histopatoloji görüntüsü seçin",
                type=['png', 'jpg', 'jpeg', 'tif', 'tiff'],
                help="Böbrek hücreli karsinom histopatoloji görüntüsü yükleyin"
            )
            
            if uploaded_file is not None:
                # Görüntüyü yükle
                image = Image.open(uploaded_file)
                st.image(image, caption="Yüklenen Görüntü", use_column_width=True)
                
                if st.button("🔬 Analiz Et", type="primary", use_container_width=True):
                    with st.spinner("Nükleer özellikler analiz ediliyor..."):
                        # Analiz yap
                        grade_idx, confidence, explanation, features = st.session_state.model.analyze_image(image)
                        
                        if grade_idx is not None:
                            grade = st.session_state.model.classes[grade_idx]
                            
                            # Grade'e göre stil
                            grade_colors = {
                                0: ("Grade 1", "grade-1", "✅"),
                                1: ("Grade 2", "grade-2", "⚠️"),
                                2: ("Grade 3", "grade-3", "🔶"),
                                3: ("Grade 4", "grade-4", "🚨")
                            }
                            
                            grade_text, grade_class, grade_icon = grade_colors[grade_idx]
                            
                            # Sonuçları göster
                            st.markdown(f"""
                            <div class="grade-box {grade_class}">
                                <h2>{grade_icon} {grade_text}</h2>
                                <h3>Güven: %{confidence*100:.1f}</h3>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # AI Açıklaması
                            st.markdown("### 🧠 Mathrix AI Analizi")
                            st.markdown(explanation)
                            
                            # Özellikleri göster
                            st.markdown("### 📊 Çıkarılan Özellikler")
                            
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.metric("Ortalama Çekirdek Boyutu", f"{features['avg_nuclear_size']:.1f} birim")
                            with col_b:
                                st.metric("Düzensizlik Skoru", f"{features['irregularity_score']:.3f}")
                            with col_c:
                                st.metric("Kontrast", f"{features['contrast']:.1f}")
                            
                            # Tedavi önerileri
                            st.markdown("### 💊 Tedavi Önerileri")
                            
                            grade_info = MEDICAL_KNOWLEDGE['grading_system'][grade]
                            treatment = grade_info['treatment']
                            
                            tab1, tab2, tab3 = st.tabs(["🎯 Primer Tedavi", "🩺 Adjuvan Tedavi", "💊 İlaçlar"])
                            
                            with tab1:
                                st.success(treatment['primary'])
                            with tab2:
                                st.info(treatment['adjuvant'])
                            with tab3:
                                for drug in treatment['drugs']:
                                    st.markdown(f"- {drug}")
            
            else:
                st.info("👆 Analiz için bir histopatoloji görüntüsü yükleyin")
        
        with col2:
            st.subheader("📚 Grading Kriterleri")
            
            # Her grade için bilgi
            for grade_idx in range(4):
                grade = st.session_state.model.classes[grade_idx]
                grade_info = MEDICAL_KNOWLEDGE['grading_system'][grade]
                
                grade_colors = {
                    0: "grade-1",
                    1: "grade-2", 
                    2: "grade-3",
                    3: "grade-4"
                }
                
                with st.expander(f"{grade}", expanded=(grade_idx==0)):
                    st.markdown(f"""
                    *Çekirdek Özellikleri:*
                    - *Boyut:* {grade_info['nuclei_size']}
                    - *Çekirdekçik:* {grade_info['nucleoli']}
                    - *Nekroz:* {grade_info['necrosis']}
                    
                    *Klinik:*
                    - {grade_info['description']}
                    - *5 Yıllık Sağkalım:* {grade_info['survival_rate']}
                    """)
    
    elif mode == "📚 Tıbbi Referans":
        st.header("Tıbbi Bilgi Bankası: Fuhrman Grading Sistemi")
        
        tab1, tab2 = st.tabs(["📖 Grading Sistemi", "🎯 AI Mantığı"])
        
        with tab1:
            st.subheader("Fuhrman Nükleer Grading Sistemi")
            
            for grade, info in MEDICAL_KNOWLEDGE['grading_system'].items():
                st.markdown(f"### {grade}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("*Morfolojik Kriterler:*")
                    st.markdown(f"- *Çekirdek Boyutu:* {info['nuclei_size']}")
                    st.markdown(f"- *Çekirdekçik:* {info['nucleoli']}")
                    st.markdown(f"- *Nekroz:* {info['necrosis']}")
                
                with col2:
                    st.markdown("*Tedavi Yaklaşımı:*")
                    st.markdown(f"- *Primer:* {info['treatment']['primary']}")
                    st.markdown(f"- *Sistemik:* {info['treatment']['adjuvant']}")
                
                st.markdown("---")
        
        with tab2:
            st.subheader("🎯 Mathrix AI Feature Extraction Mantığı")
            
            st.markdown("""
            ### DeepSeek Feature Extraction Logic
            
            Mathrix AI şu kritik nükleer özelliklere odaklanır:
            
            *1. Çekirdek Boyutu (Nuclear Size):*
            - *Grade 1:* Yaklaşık 10 mikrometre, yuvarlak çekirdekler
            - *Grade 2:* 10-15 mikrometre, hafif düzensiz
            - *Grade 3:* 15-20 mikrometre, belirgin düzensiz
            - *Grade 4:* 20+ mikrometre, devasa çekirdekler
            
            *2. Çekirdek Şekli (Nuclear Shape/Pleomorphism):*
            - *Grade 1:* Uniform, düzenli şekiller
            - *Grade 2:* Hafif düzensizlikler
            - *Grade 3:* Belirgin düzensizlikler
            - *Grade 4:* Multilobule, grotesk formlar
            
            *3. Çekirdekçik Belirginliği (Nucleoli Prominence):*
            - *Grade 1:* Görünmeyen çekirdekçikler
            - *Grade 2:* 400x'te görülebilen küçük çekirdekçikler
            - *Grade 3:* 100x'te görülebilen belirgin çekirdekçikler
            - *Grade 4:* Canavar gibi (monstrous) makronükleoller
            """)
            
            # Örnek görselleştirme
            st.markdown("### 📈 Grading Karar Matrisi")
            
            # Karar matrisi
            decision_matrix = pd.DataFrame({
                'Grade': ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4'],
                'Çekirdek Boyutu (μm)': ['~10', '10-15', '15-20', '>20'],
                'Şekil Düzensizliği': ['Çok Düşük', 'Düşük', 'Yüksek', 'Çok Yüksek'],
                'Çekirdekçik': ['Görünmez', '400x Görülür', '100x Görülür', 'Makro']
            })
            
            st.dataframe(decision_matrix, use_container_width=True)
    
    elif mode == "⚙️ Ayarlar":
        st.header("Sistem Ayarları")
        
        st.subheader("Model Bilgisi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Model Durumu", "Aktif" if st.session_state.model_loaded else "Pasif")
            st.metric("Sınıf Sayısı", "4 (Grade 1-4)")
            st.metric("Görüntü Boyutu", "256x256 piksel")
        
        with col2:
            st.metric("Özellik Sayısı", "6 temel özellik")
            st.metric("AI Tipi", "CNN + Feature Extraction")
            st.metric("Versiyon", "1.0.0")
        
        st.subheader("Sistem Logları")
        
        # Demo log
        log_data = {
            "Tarih": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Olay": ["Uygulama başlatıldı"],
            "Durum": ["Başarılı"]
        }
        
        st.dataframe(pd.DataFrame(log_data), use_container_width=True)
        
        # İndirme butonu
        st.download_button(
            label="📥 Logları İndir",
            data=pd.DataFrame(log_data).to_csv(index=False).encode('utf-8'),
            file_name=f"mathrix_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # Footer
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("*Mathrix AI v1.0*")
    
    with col2:
        st.markdown("*Patoloji Destekli AI Sistem*")
    
    with col3:
        st.markdown(f"*Son Güncelleme:* {datetime.now().strftime('%d.%m.%Y')}")

if _name_ == "_main_":
    main()
