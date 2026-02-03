import os
import numpy as np
import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
import torch.optim as optim
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

# ============================================
# 1. ÖN İŞLEME VE RENK DEĞİŞMEZLİĞİ
# ============================================

class StainNormalizer:
    """Macenko yöntemi ile boya normalizasyonu"""
    def _init_(self):
        self.reference_he = np.array([[0.5626, 0.2159],
                                      [0.7201, 0.8012],
                                      [0.4062, 0.5581]])
    
    def normalize(self, image):
        # Basitleştirilmiş Macenko implementasyonu
        # Tam implementasyon için stain-tools kütüphanesi önerilir
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
        return image

class PreprocessPipeline:
    def _init_(self, img_size=512):
        self.img_size = img_size
        self.stain_norm = StainNormalizer()
        
    def _call_(self, image):
        # Boya normalizasyonu
        normalized = self.stain_norm.normalize(image)
        
        # Gri tonlama
        gray = cv2.cvtColor(normalized, cv2.COLOR_BGR2GRAY)
        
        # CLAHE ile kontrast artırma
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Gaussian blur
        blurred = cv2.GaussianBlur(enhanced, (3,3), 0)
        
        # Sobel edge detection
        sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
        sobel = np.sqrt(sobelx*2 + sobely*2)
        sobel = np.uint8(sobel / sobel.max() * 255)
        
        # Kenarları vurgulamak için orijinal ile birleştir
        combined = cv2.addWeighted(enhanced, 0.7, sobel, 0.3, 0)
        
        # Yeniden boyutlandır
        resized = cv2.resize(combined, (self.img_size, self.img_size))
        
        # 3 kanala çevir (CNN için)
        three_channel = np.stack([resized]*3, axis=-1)
        
        return three_channel

# ============================================
# 2. MATEMATİKSEL ÖZNİTELİK MÜHENDİSLİĞİ
# ============================================

class MathematicalFeatures:
    @staticmethod
    def calculate_lacunarity(binary_image, box_sizes=None):
        """Boşluk analizi için lacunarity hesaplama"""
        if box_sizes is None:
            box_sizes = [2, 4, 8, 16, 32]
        
        lacunarities = []
        image = (binary_image > 128).astype(np.uint8)
        
        for size in box_sizes:
            if size > min(image.shape):
                continue
            
            mass_values = []
            for i in range(0, image.shape[0] - size + 1, size):
                for j in range(0, image.shape[1] - size + 1, size):
                    box = image[i:i+size, j:j+size]
                    mass = np.sum(box)
                    mass_values.append(mass)
            
            if len(mass_values) > 1:
                mean_mass = np.mean(mass_values)
                std_mass = np.std(mass_values)
                lac = (std_mass / mean_mass) ** 2 if mean_mass > 0 else 0
                lacunarities.append(lac)
        
        return np.mean(lacunarities) if lacunarities else 0
    
    @staticmethod
    def calculate_fractal_dimension(binary_image):
        """Fraktal boyut hesaplama - box counting method"""
        image = (binary_image > 128).astype(np.uint8)
        
        scales = np.logspace(0.5, 3, num=10, dtype=int)
        scales = scales[scales <= min(image.shape)]
        scales = scales[scales > 1]
        
        Ns = []
        for scale in scales:
            # Resmi scale faktörüyle yeniden boyutlandır
            h, w = image.shape
            new_h, new_w = h//scale, w//scale
            if new_h == 0 or new_w == 0:
                continue
            
            resized = cv2.resize(image, (new_w, new_h))
            
            # Box sayısını hesapla
            boxes = (resized > 0).sum()
            Ns.append(boxes)
        
        if len(Ns) < 2:
            return 1.0
        
        # Log-log gradyanı fraktal boyutu verir
        coeffs = np.polyfit(np.log(scales[:len(Ns)]), np.log(Ns), 1)
        return -coeffs[0]
    
    @staticmethod
    def detect_circular_structures(gray_image):
        """Dairesel yapıları tespit et (lümen için)"""
        circles = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, dp=1, 
                                  minDist=50, param1=50, param2=30,
                                  minRadius=10, maxRadius=100)
        return len(circles[0]) if circles is not None else 0
    
    @staticmethod
    def calculate_glcm_features(gray_image):
        """GLCM öznitelikleri hesaplama"""
        from skimage.feature import graycomatrix, graycoprops
        
        # 8-bit'e dönüştür
        gray = (gray_image / gray_image.max() * 255).astype(np.uint8)
        
        # GLCM hesapla
        glcm = graycomatrix(gray, distances=[1], angles=[0], symmetric=True, normed=True)
        
        # Öznitelikleri çıkar
        features = {
            'contrast': graycoprops(glcm, 'contrast')[0, 0],
            'dissimilarity': graycoprops(glcm, 'dissimilarity')[0, 0],
            'homogeneity': graycoprops(glcm, 'homogeneity')[0, 0],
            'energy': graycoprops(glcm, 'energy')[0, 0],
            'correlation': graycoprops(glcm, 'correlation')[0, 0],
            'ASM': graycoprops(glcm, 'ASM')[0, 0]
        }
        return features

# ============================================
# 3. VERİ SETİ SINIFI
# ============================================

class LungDataset(Dataset):
    def _init_(self, root_dir, transform=None, img_size=512):
        self.root_dir = root_dir
        self.transform = transform
        self.img_size = img_size
        self.preprocessor = PreprocessPipeline(img_size)
        self.feature_extractor = MathematicalFeatures()
        
        self.classes = ['lung_n', 'lung_aca', 'lung_scc']
        self.class_to_idx = {c: i for i, c in enumerate(self.classes)}
        
        self.samples = []
        for class_name in self.classes:
            class_dir = os.path.join(root_dir, class_name)
            if not os.path.exists(class_dir):
                continue
                
            class_idx = self.class_to_idx[class_name]
            for img_name in os.listdir(class_dir):
                if img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff')):
                    img_path = os.path.join(class_dir, img_name)
                    self.samples.append((img_path, class_idx))
    
    def _len_(self):
        return len(self.samples)
    
    def _getitem_(self, idx):
        img_path, label = self.samples[idx]
        
        # Görüntüyü yükle
        image = cv2.imread(img_path)
        if image is None:
            # Alternatif okuma yöntemi
            image = np.array(Image.open(img_path).convert('RGB'))
            if len(image.shape) == 2:
                image = np.stack([image]*3, axis=-1)
        
        # Ön işleme
        processed = self.preprocessor(image)
        
        # Matematiksel öznitelikleri çıkar
        gray = cv2.cvtColor(processed, cv2.COLOR_RGB2GRAY)
        
        # Lacunarity ve fraktal boyut
        lacunarity = self.feature_extractor.calculate_lacunarity(gray)
        fractal_dim = self.feature_extractor.calculate_fractal_dimension(gray)
        
        # Dairesel yapı sayısı
        circles = self.feature_extractor.detect_circular_structures(gray)
        
        # Matematiksel öznitelikleri birleştir
        math_features = np.array([lacunarity, fractal_dim, circles], dtype=np.float32)
        
        # Torch tensörüne çevir
        image_tensor = transforms.ToTensor()(processed)
        
        if self.transform:
            image_tensor = self.transform(image_tensor)
        
        return {
            'image': image_tensor,
            'math_features': torch.FloatTensor(math_features),
            'label': torch.tensor(label, dtype=torch.long)
        }

# ============================================
# 4. MODEL MİMARİSİ
# ============================================

class SpatialAttention(nn.Module):
    def _init_(self, in_channels):
        super()._init_()
        self.conv = nn.Conv2d(in_channels, 1, kernel_size=1)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        attention = self.conv(x)
        attention = self.sigmoid(attention)
        return x * attention

class HybridLungModel(nn.Module):
    def _init_(self, num_classes=3, backbone='efficientnet'):
        super()._init_()
        
        # Backbone seçimi
        if backbone == 'efficientnet':
            base_model = models.efficientnet_b3(pretrained=True)
            in_features = base_model.classifier[1].in_features
            self.backbone = nn.Sequential(*list(base_model.children())[:-2])
        else:  # resnet
            base_model = models.resnet50(pretrained=True)
            in_features = base_model.fc.in_features
            self.backbone = nn.Sequential(*list(base_model.children())[:-2])
        
        # Spatial Attention
        self.attention = SpatialAttention(2048 if backbone == 'resnet' else 1536)
        
        # Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d(1)
        
        # Matematiksel öznitelikler için branch
        self.math_branch = nn.Sequential(
            nn.Linear(3, 32),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(32, 64)
        )
        
        # Birleştirilmiş öznitelikler
        total_features = in_features + 64
        self.classifier = nn.Sequential(
            nn.Linear(total_features, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )
        
        # Grad-CAM için
        self.gradients = None
        self.activations = None
    
    def activations_hook(self, grad):
        self.gradients = grad
    
    def forward(self, image, math_features):
        # Görsel öznitelikler
        x = self.backbone(image)
        
        # Grad-CAM için aktivasyonları kaydet
        if x.requires_grad:
            h = x.register_hook(self.activations_hook)
        self.activations = x
        
        # Spatial Attention
        x = self.attention(x)
        
        # Global pooling
        x = self.gap(x)
        x = x.view(x.size(0), -1)
        
        # Matematiksel öznitelikler
        math_x = self.math_branch(math_features)
        
        # Birleştirme
        combined = torch.cat([x, math_x], dim=1)
        
        # Sınıflandırma
        output = self.classifier(combined)
        
        return output
    
    def get_activations_gradient(self):
        return self.gradients
    
    def get_activations(self):
        return self.activations

# ============================================
# 5. GRAD-CAM SINIFI
# ============================================

class GradCAM:
    def _init_(self, model):
        self.model = model
        self.gradients = None
        self.activations = None
        
    def save_gradient(self, grad):
        self.gradients = grad
    
    def _call_(self, x, math_features):
        # Forward pass
        output = self.model(x, math_features)
        
        # Backward için hook
        h = self.model.activations.register_hook(self.save_gradient)
        
        # En yüksek skorlu sınıf için gradient
        one_hot = torch.zeros(output.size())
        one_hot[0, output.argmax()] = 1
        
        # Backward pass
        self.model.zero_grad()
        output.backward(gradient=one_hot.to(x.device), retain_graph=True)
        
        # Gradients ve activations
        gradients = self.gradients.detach().cpu().numpy()[0]
        activations = self.model.activations.detach().cpu().numpy()[0]
        
        # Ağırlıkları hesapla
        weights = np.mean(gradients, axis=(1, 2))
        
        # CAM oluştur
        cam = np.zeros(activations.shape[1:], dtype=np.float32)
        for i, w in enumerate(weights):
            cam += w * activations[i]
        
        # ReLU uygula
        cam = np.maximum(cam, 0)
        
        # Normalize et
        cam = cam / (cam.max() + 1e-10)
        
        return cam, output

# ============================================
# 6. EĞİTİM FONKSİYONU
# ============================================

def train_model(model, dataloaders, criterion, optimizer, num_epochs=50, device='cuda'):
    train_loader, val_loader = dataloaders
    
    history = {'train_loss': [], 'val_loss': [], 'train_acc': [], 'val_acc': []}
    
    for epoch in range(num_epochs):
        print(f'Epoch {epoch+1}/{num_epochs}')
        print('-' * 50)
        
        # Her epoch için train ve validation
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()
                loader = train_loader
            else:
                model.eval()
                loader = val_loader
            
            running_loss = 0.0
            running_corrects = 0
            
            for batch in loader:
                images = batch['image'].to(device)
                math_features = batch['math_features'].to(device)
                labels = batch['label'].to(device)
                
                optimizer.zero_grad()
                
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(images, math_features)
                    loss = criterion(outputs, labels)
                    
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()
                
                # İstatistikler
                running_loss += loss.item() * images.size(0)
                _, preds = torch.max(outputs, 1)
                running_corrects += torch.sum(preds == labels.data)
            
            epoch_loss = running_loss / len(loader.dataset)
            epoch_acc = running_corrects.double() / len(loader.dataset)
            
            print(f'{phase.capitalize()} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')
            
            # History'yi güncelle
            if phase == 'train':
                history['train_loss'].append(epoch_loss)
                history['train_acc'].append(epoch_acc.cpu())
            else:
                history['val_loss'].append(epoch_loss)
                history['val_acc'].append(epoch_acc.cpu())
        
        print()
    
    return history, model

# ============================================
# 7. DEĞERLENDİRME FONKSİYONLARI
# ============================================

def evaluate_model(model, test_loader, device='cuda'):
    model.eval()
    
    all_preds = []
    all_labels = []
    all_probs = []
    
    with torch.no_grad():
        for batch in test_loader:
            images = batch['image'].to(device)
            math_features = batch['math_features'].to(device)
            labels = batch['label'].to(device)
            
            outputs = model(images, math_features)
            probs = F.softmax(outputs, dim=1)
            _, preds = torch.max(outputs, 1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())
    
    # Confusion Matrix
    cm = confusion_matrix(all_labels, all_preds)
    
    # Classification Report
    report = classification_report(all_labels, all_preds, 
                                   target_names=['NORMAL', 'ACA', 'SCC'])
    
    return cm, report, all_probs

def plot_confusion_matrix(cm, class_names):
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.show()

# ============================================
# 8. ANA FONKSİYON
# ============================================

def main():
    # Parametreler
    DATA_DIR = './lung_dataset'  # Klasör yapısı: lung_n, lung_aca, lung_scc
    BATCH_SIZE = 8
    NUM_EPOCHS = 30
    IMG_SIZE = 512
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    print(f"Using device: {DEVICE}")
    
    # Veri setlerini oluştur
    print("Loading datasets...")
    
    # Data augmentation
    train_transform = transforms.Compose([
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.5),
        transforms.RandomRotation(30),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    # Dataset ve DataLoader'ları oluştur
    train_dataset = LungDataset(os.path.join(DATA_DIR, 'train'), 
                                transform=train_transform, img_size=IMG_SIZE)
    val_dataset = LungDataset(os.path.join(DATA_DIR, 'val'), 
                              transform=val_transform, img_size=IMG_SIZE)
    test_dataset = LungDataset(os.path.join(DATA_DIR, 'test'), 
                               transform=val_transform, img_size=IMG_SIZE)
    
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, 
                              shuffle=True, num_workers=4)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, 
                            shuffle=False, num_workers=4)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, 
                             shuffle=False, num_workers=4)
    
    print(f"Train samples: {len(train_dataset)}")
    print(f"Val samples: {len(val_dataset)}")
    print(f"Test samples: {len(test_dataset)}")
    
    # Modeli oluştur
    print("\nCreating model...")
    model = HybridLungModel(num_classes=3, backbone='efficientnet')
    model = model.to(DEVICE)
    
    # Loss function ve optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-4)
    
    # Eğitim
    print("\nStarting training...")
    history, trained_model = train_model(
        model, 
        (train_loader, val_loader), 
        criterion, 
        optimizer, 
        num_epochs=NUM_EPOCHS, 
        device=DEVICE
    )
    
    # Test değerlendirmesi
    print("\nEvaluating on test set...")
    cm, report, probs = evaluate_model(trained_model, test_loader, DEVICE)
    
    print("\nClassification Report:")
    print(report)
    
    # Confusion Matrix'i göster
    plot_confusion_matrix(cm, ['NORMAL', 'ACA', 'SCC'])
    
    # Grad-CAM örneği
    print("\nGenerating Grad-CAM visualization for a sample...")
    grad_cam = GradCAM(trained_model)
    
    # Test setinden bir örnek al
    sample = test_dataset[0]
    image = sample['image'].unsqueeze(0).to(DEVICE)
    math_features = sample['math_features'].unsqueeze(0).to(DEVICE)
    
    # Grad-CAM hesapla
    cam, output = grad_cam(image, math_features)
    
    # Görselleştirme
    plt.figure(figsize=(12, 4))
    
    # Orijinal görüntü
    plt.subplot(1, 3, 1)
    orig_img = sample['image'].permute(1, 2, 0).cpu().numpy()
    orig_img = (orig_img - orig_img.min()) / (orig_img.max() - orig_img.min())
    plt.imshow(orig_img)
    plt.title(f'True: {sample["label"].item()}')
    plt.axis('off')
    
    # Heatmap
    plt.subplot(1, 3, 2)
    cam_resized = cv2.resize(cam, (IMG_SIZE, IMG_SIZE))
    plt.imshow(cam_resized, cmap='jet')
    plt.title('Grad-CAM Heatmap')
    plt.axis('off')
    
    # Overlay
    plt.subplot(1, 3, 3)
    plt.imshow(orig_img)
    plt.imshow(cam_resized, cmap='jet', alpha=0.5)
    plt.title('Overlay')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # Modeli kaydet
    torch.save({
        'model_state_dict': trained_model.state_dict(),
        'history': history,
        'config': {
            'img_size': IMG_SIZE,
            'backbone': 'efficientnet',
            'num_classes': 3
        }
    }, 'lung_classification_model.pth')
    
    print("\nModel saved as 'lung_classification_model.pth'")
    
    # Öznitelik analizi
    print("\nFeature Analysis:")
    print("-" * 30)
    
    # Her sınıf için ortalama matematiksel öznitelikler
    class_features = {0: [], 1: [], 2: []}
    
    for batch in test_loader:
        for i in range(len(batch['label'])):
            label = batch['label'][i].item()
            features = batch['math_features'][i].numpy()
            class_features[label].append(features)
    
    for class_idx, class_name in enumerate(['NORMAL', 'ACA', 'SCC']):
        if class_features[class_idx]:
            avg_features = np.mean(class_features[class_idx], axis=0)
            print(f"{class_name}:")
            print(f"  Lacunarity: {avg_features[0]:.4f}")
            print(f"  Fractal Dimension: {avg_features[1]:.4f}")
            print(f"  Circular Structures: {avg_features[2]:.1f}")
            print()

if _name_ == "_main_":
    main()
