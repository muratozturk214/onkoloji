import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image

# Tema ayarları
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MathrixApp(ctk.CTk):
    def _init_(self):
        super()._init_()

        self.title("MATHRIX - Medical Analysis System")
        self.geometry("900x700")

        # Giriş Ekranı
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(expand=True, fill="both")

        self.label = ctk.CTkLabel(self.login_frame, text="MATHRIX SYSTEM", font=("Orbitron", 32, "bold"))
        self.label.pack(pady=40)

        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*", width=250)
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.check_password)
        self.login_button.pack(pady=20)

    def check_password(self):
        if self.password_entry.get() == "mathrix2026":
            self.login_frame.destroy()
            self.main_interface()
        else:
            messagebox.showerror("Error", "Incorrect Password!")

    def main_interface(self):
        # Ana Dashboard
        self.tabview = ctk.CTkTabview(self, width=850, height=650)
        self.tabview.pack(pady=20, padx=20)

        self.tabview.add("Cancer Database")
        self.tabview.add("Microscopic Analysis")

        # --- 1. Kanser Bilgi Sekmesi ---
        self.setup_database_tab()

        # --- 2. Analiz Sekmesi ---
        self.setup_analysis_tab()

    def setup_database_tab(self):
        scroll_frame = ctk.CTkScrollableFrame(self.tabview.tab("Cancer Database"), width=800, height=550)
        scroll_frame.pack(pady=10, padx=10)

        cancer_data = {
            "Lung Cancer": "Types: Adenocarcinoma, Squamous Cell Carcinoma.\nDrugs: Cisplatin, Pembrolizumab.\nInfo: Main cause is smoking/pollutants.",
            "Gastric Cancer": "Types: Adenocarcinoma, Lymphoma.\nDrugs: 5-FU, Oxaliplatin.\nInfo: Often starts in mucus-producing cells.",
            "Breast Cancer": "Types: IDC, ILC.\nDrugs: Tamoxifen, Herceptin.\nInfo: Early detection increases survival by 90%."
        }

        for cancer, info in cancer_data.items():
            card = ctk.CTkFrame(scroll_frame)
            card.pack(fill="x", pady=5, padx=5)
            
            lbl_title = ctk.CTkLabel(card, text=cancer, font=("Arial", 18, "bold"), text_color="#1f538d")
            lbl_title.pack(anchor="w", padx=10, pady=5)
            
            lbl_info = ctk.CTkLabel(card, text=info, justify="left")
            lbl_info.pack(anchor="w", padx=10, pady=5)

    def setup_analysis_tab(self):
        tab = self.tabview.tab("Microscopic Analysis")
        
        self.upload_btn = ctk.CTkButton(tab, text="Upload Microscopic Image", command=self.upload_and_analyze)
        self.upload_btn.pack(pady=20)

        self.result_box = ctk.CTkTextbox(tab, width=700, height=300, font=("Consolas", 14))
        self.result_box.pack(pady=10)
        self.result_box.insert("0.0", "System ready for analysis...\nPlease upload a histological slide image.")

    def upload_and_analyze(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # Burada normalde bir AI modeli (TensorFlow/PyTorch) çalışır. 
            # Şu an için simülasyon sonuçları veriyoruz:
            self.result_box.delete("0.0", "end")
            analysis_text = (
                "--- ANALYSIS REPORT ---\n"
                "Tissue Type: Gastric (Mide)\n"
                "Status: MALIGNANT (Kanserli)\n"
                "Type: Adenocarcinoma\n"
                "Cell Count: 1.240.000 / mm2\n"
                "Stage: Stage II\n\n"
                "Suggested Treatment: Surgical resection followed by chemotherapy (FOLFOX regimen).\n"
                "Note: Please correlate with clinical findings."
            )
            self.result_box.insert("0.0", analysis_text)

if _name_ == "_main_":
    app = MathrixApp()
    app.mainloop()
