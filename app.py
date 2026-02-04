import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import tempfile
import os
import json
from datetime import datetime
import pytesseract
from pdf2image import convert_from_bytes
import io
import base64
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Mathrix AI - Medical Pathology Analyzer",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = []
if 'current_file_index' not in st.session_state:
    st.session_state.current_file_index = 0

# Medical database - Fuhrman Grading with therapy recommendations
FUHRMAN_GRADING = {
    1: {
        "description": "Nuclei round, uniform, approximately 10 μm diameter. Inconspicuous or absent nucleoli at 400x magnification.",
        "therapy": ["Active Surveillance", "Partial Nephrectomy"],
        "morphology": "Small, round nuclei with smooth nuclear membrane"
    },
    2: {
        "description": "Nuclei slightly irregular, approximately 15 μm diameter. Nucleoli visible at 400x magnification but not prominent.",
        "therapy": ["Partial Nephrectomy", "Radical Nephrectomy"],
        "morphology": "Moderately irregular nuclei with visible nucleoli"
    },
    3: {
        "description": "Nuclei obviously irregular, approximately 20 μm diameter. Large, prominent nucleoli visible at 100x magnification.",
        "therapy": ["Sunitinib", "Pazopanib", "Radical Nephrectomy + Targeted Therapy"],
        "morphology": "Markedly irregular nuclei with prominent nucleoli"
    },
    4: {
        "description": "Nuclei pleomorphic, giant cells, approximately 25+ μm diameter. Macronucleoli, bizarre nuclear shapes.",
        "therapy": ["Nivolumab", "Ipilimumab", "Cabozantinib", "Lenvatinib + Everolimus"],
        "morphology": "Extreme nuclear pleomorphism with macronucleoli"
    }
}

def process_image(image_file):
    """Process a single pathology image and extract features"""
    try:
        # Convert to OpenCV format
        image = Image.open(image_file)
        img_array = np.array(image)
        
        if len(img_array.shape) == 2:  # Grayscale
            img_gray = img_array
        else:
            img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Basic image quality check
        if is_blurry(img_gray):
            return {"error": "Image quality insufficient for analysis"}
        
        # Extract features
        features = extract_nuclear_features(img_gray)
        
        # Determine Fuhrman grade
        grade = determine_fuhrmann_grade(features)
        
        # Get therapy recommendations
        therapy = FUHRMAN_GRADING[grade]["therapy"]
        
        return {
            "patient_id": os.path.splitext(image_file.name)[0],
            "detected_grade": grade,
            "mean_nuclear_diameter": features.get("mean_diameter", 0),
            "recommended_medication": ", ".join(therapy),
            "morphology": FUHRMAN_GRADING[grade]["morphology"],
            "description": FUHRMAN_GRADING[grade]["description"],
            "image_data": img_array,
            "features": features
        }
        
    except Exception as e:
        return {"error": f"Image processing error: {str(e)}"}

def process_pdf(pdf_file):
    """Extract text from PDF clinical reports"""
    try:
        # Convert PDF to images
        images = convert_from_bytes(pdf_file.read())
        
        extracted_text = ""
        for image in images:
            # Convert PIL image to OpenCV
            img_array = np.array(image)
            if len(img_array.shape) == 3:
                img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                img_gray = img_array
            
            # Use OCR to extract text
            text = pytesseract.image_to_string(img_gray)
            extracted_text += text + "\n"
        
        # Simple parsing for demonstration
        # In production, use more sophisticated NLP
        lines = extracted_text.split('\n')
        patient_info = {}
        
        for line in lines:
            if "patient" in line.lower() or "id" in line.lower():
                patient_info["patient_id"] = line.strip()
            elif "grade" in line.lower():
                # Try to extract grade from text
                for grade_num in [1, 2, 3, 4]:
                    if str(grade_num) in line:
                        patient_info["detected_grade"] = grade_num
                        break
        
        if "detected_grade" not in patient_info:
            patient_info["detected_grade"] = 2  # Default if not found
        
        # Generate mock data for PDF
        grade = patient_info["detected_grade"]
        return {
            "patient_id": patient_info.get("patient_id", pdf_file.name),
            "detected_grade": grade,
            "mean_nuclear_diameter": [10, 15, 20, 25][grade-1],
            "recommended_medication": ", ".join(FUHRMAN_GRADING[grade]["therapy"]),
            "morphology": FUHRMAN_GRADING[grade]["morphology"],
            "description": FUHRMAN_GRADING[grade]["description"],
            "source": "PDF Report"
        }
        
    except Exception as e:
        return {"error": f"PDF processing error: {str(e)}"}

def is_blurry(image, threshold=100):
    """Check if image is blurry using Laplacian variance"""
    if image is None:
        return True
    laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
    return laplacian_var < threshold

def extract_nuclear_features(image):
    """Extract nuclear features from pathology image"""
    try:
        # Apply thresholding
        _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Find contours (representing nuclei)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return {"mean_diameter": 10, "nuclear_count": 0}
        
        # Calculate features from contours
        diameters = []
        for contour in contours[:50]:  # Limit to first 50 contours for performance
            if len(contour) >= 5:  # Need at least 5 points for ellipse fitting
                ellipse = cv2.fitEllipse(contour)
                major_axis = max(ellipse[1])
                diameters.append(major_axis)
        
        if diameters:
            mean_diameter = np.mean(diameters)
            # Convert pixels to micrometers (assuming 1 pixel = 0.25 μm at 40x magnification)
            mean_diameter_um = mean_diameter * 0.25
        else:
            mean_diameter_um = 10  # Default
        
        return {
            "mean_diameter": round(mean_diameter_um, 2),
            "nuclear_count": len(contours),
            "diameter_std": np.std(diameters) if diameters else 0
        }
        
    except Exception as e:
        return {"mean_diameter": 10, "nuclear_count": 0, "error": str(e)}

def determine_fuhrmann_grade(features):
    """Determine Fuhrman grade based on nuclear features"""
    mean_diameter = features.get("mean_diameter", 10)
    
    if mean_diameter < 12:
        return 1
    elif mean_diameter < 18:
        return 2
    elif mean_diameter < 23:
        return 3
    else:
        return 4

def create_summary_dataframe(processed_data):
    """Create summary DataFrame from processed data"""
    records = []
    for item in processed_data:
        if "error" not in item:
            records.append({
                "Patient ID": item.get("patient_id", "Unknown"),
                "Detected Grade": item.get("detected_grade", "N/A"),
                "Mean Nuclear Diameter (μm)": item.get("mean_nuclear_diameter", 0),
                "Recommended Medication": item.get("recommended_medication", "N/A"),
                "Morphology": item.get("morphology", "N/A"),
                "Processing Date": datetime.now().strftime("%Y-%m-%d")
            })
    
    return pd.DataFrame(records)

def plot_nuclear_analysis(image, features, grade):
    """Create visualization for nuclear analysis"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # Original image
    axes[0].imshow(image, cmap='gray')
    axes[0].set_title(f'Pathology Image - Grade {grade}')
    axes[0].axis('off')
    
    # Grade distribution chart
    grades = [1, 2, 3, 4]
    diameters = [10, 15, 20, 25]
    colors = ['green', 'yellow', 'orange', 'red']
    
    axes[1].bar(grades, diameters, color=colors, alpha=0.6)
    axes[1].axhline(y=features.get("mean_diameter", 10), color='r', 
                    linestyle='--', label=f'Detected: {features.get("mean_diameter", 10):.1f}μm')
    axes[1].set_xlabel('Fuhrman Grade')
    axes[1].set_ylabel('Mean Nuclear Diameter (μm)')
    axes[1].set_title('Fuhrman Grading Scale')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

# Main application
def main():
    st.title("🏥 Mathrix AI - Pathology Analysis System")
    st.markdown("### Advanced Medical Intelligence for Renal Cell Carcinoma Grading")
    
    # Sidebar for clinical inputs
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2784/2784449.png", width=100)
        st.markdown("### Clinical Parameters")
        
        # Hospital/Clinic info
        hospital_name = st.text_input("Hospital/Clinic Name", "General Hospital")
        clinician_name = st.text_input("Clinician Name", "Dr. Smith")
        
        # Analysis parameters
        st.markdown("---")
        st.markdown("#### Analysis Settings")
        magnification = st.selectbox(
            "Microscope Magnification",
            ["20x", "40x", "60x", "100x"],
            index=1
        )
        
        analysis_mode = st.selectbox(
            "Analysis Mode",
            ["Standard", "Comprehensive", "Rapid Screening"],
            index=0
        )
        
        # Fuhrman grading reference
        st.markdown("---")
        st.markdown("#### Fuhrman Grading Reference")
        for grade in range(1, 5):
            with st.expander(f"Grade {grade}"):
                st.write(FUHRMAN_GRADING[grade]["description"])
                st.write(f"*Therapy:* {', '.join(FUHRMAN_GRADING[grade]['therapy'])}")
        
        st.markdown("---")
        st.markdown("*Version:* 2.1.0")
        st.markdown("*Last Updated:* November 2023")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📁 Multi-File Upload")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Upload Pathology Images (JPG/PNG) and/or Clinical Reports (PDF)",
            type=['jpg', 'jpeg', 'png', 'pdf'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.success(f"📄 {len(uploaded_files)} file(s) uploaded successfully!")
            
            # Process files button
            if st.button("🚀 Process All Files", type="primary", use_container_width=True):
                with st.spinner("Processing files..."):
                    progress_bar = st.progress(0)
                    processed_results = []
                    
                    for i, file in enumerate(uploaded_files):
                        progress_bar.progress((i + 1) / len(uploaded_files))
                        
                        if file.type.startswith('image'):
                            result = process_image(file)
                        elif file.type == 'application/pdf':
                            result = process_pdf(file)
                        else:
                            result = {"error": f"Unsupported file type: {file.type}"}
                        
                        result["filename"] = file.name
                        processed_results.append(result)
                    
                    st.session_state.processed_data = processed_results
                    progress_bar.empty()
                    st.success(f"✅ Processed {len(uploaded_files)} file(s)")
    
    with col2:
        st.subheader("⚙️ Batch Processing Status")
        if 'processed_data' in st.session_state and st.session_state.processed_data:
            successful = len([d for d in st.session_state.processed_data if "error" not in d])
            total = len(st.session_state.processed_data)
            
            st.metric("Successfully Processed", f"{successful}/{total}")
            
            if successful > 0:
                grades = [d.get("detected_grade") for d in st.session_state.processed_data 
                         if "error" not in d and "detected_grade" in d]
                if grades:
                    avg_grade = np.mean(grades)
                    st.metric("Average Grade", f"{avg_grade:.1f}")
    
    # Display results if available
    if 'processed_data' in st.session_state and st.session_state.processed_data:
        st.markdown("---")
        st.subheader("📊 Analysis Results")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📈 Detailed View", "📋 Summary Table", "📥 Export Data"])
        
        with tab1:
            # Navigation for multiple files
            if len(st.session_state.processed_data) > 1:
                col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
                with col_nav2:
                    file_index = st.selectbox(
                        "Select File to View",
                        range(len(st.session_state.processed_data)),
                        format_func=lambda x: st.session_state.processed_data[x].get("filename", f"File {x+1}"),
                        index=st.session_state.current_file_index
                    )
                    st.session_state.current_file_index = file_index
            
            current_data = st.session_state.processed_data[st.session_state.current_file_index]
            
            if "error" in current_data:
                st.error(f"❌ Error processing file: {current_data['error']}")
            else:
                # Display in two columns
                col_img, col_info = st.columns([1, 1])
                
                with col_img:
                    if "image_data" in current_data:
                        st.image(current_data["image_data"], 
                                caption=f"Pathology Image - {current_data.get('patient_id', 'Unknown')}",
                                use_column_width=True)
                
                with col_info:
                    st.markdown(f"### Patient: {current_data.get('patient_id', 'Unknown')}")
                    
                    # Grade display with color coding
                    grade = current_data.get("detected_grade", 0)
                    grade_colors = {1: "🟢", 2: "🟡", 3: "🟠", 4: "🔴"}
                    st.markdown(f"### Fuhrman Grade: {grade_colors.get(grade, '⚪')} *Grade {grade}*")
                    
                    # Display metrics
                    col_metrics1, col_metrics2 = st.columns(2)
                    with col_metrics1:
                        st.metric("Mean Nuclear Diameter", 
                                 f"{current_data.get('mean_nuclear_diameter', 0)} μm")
                    with col_metrics2:
                        st.metric("Morphology", 
                                 current_data.get('morphology', 'N/A'))
                    
                    # Therapy recommendations
                    st.markdown("#### 💊 Targeted Therapy Recommendations")
                    therapy = current_data.get("recommended_medication", "").split(", ")
                    for med in therapy:
                        st.info(f"• *{med}*")
                    
                    # Morphological description
                    st.markdown("#### 🔬 Morphological Description")
                    st.write(current_data.get("description", "No description available"))
                
                # Visualization
                if "image_data" in current_data and "features" in current_data:
                    st.markdown("---")
                    st.subheader("📊 Nuclear Analysis Visualization")
                    fig = plot_nuclear_analysis(
                        current_data["image_data"],
                        current_data["features"],
                        current_data.get("detected_grade", 0)
                    )
                    st.pyplot(fig)
        
        with tab2:
            # Create and display summary table
            df_summary = create_summary_dataframe(st.session_state.processed_data)
            
            if not df_summary.empty:
                st.dataframe(df_summary, use_container_width=True)
                
                # Statistics
                st.subheader("📈 Batch Statistics")
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                
                with col_stat1:
                    grade_counts = df_summary["Detected Grade"].value_counts()
                    st.write("*Grade Distribution:*")
                    for grade, count in grade_counts.items():
                        st.write(f"Grade {grade}: {count} cases")
                
                with col_stat2:
                    avg_diameter = df_summary["Mean Nuclear Diameter (μm)"].mean()
                    st.metric("Average Diameter", f"{avg_diameter:.1f} μm")
                
                with col_stat3:
                    most_common_grade = df_summary["Detected Grade"].mode()
                    if not most_common_grade.empty:
                        st.metric("Most Common Grade", f"Grade {most_common_grade.iloc[0]}")
            
            else:
                st.warning("No valid data to display in summary table.")
        
        with tab3:
            st.subheader("📥 Export Analysis Results")
            
            if st.session_state.processed_data and any("error" not in d for d in st.session_state.processed_data):
                df_export = create_summary_dataframe(st.session_state.processed_data)
                
                # Excel download
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    df_export.to_excel(writer, index=False, sheet_name='Analysis_Summary')
                    
                    # Add grading reference sheet
                    grading_ref = pd.DataFrame([
                        {"Grade": g, 
                         "Description": FUHRMAN_GRADING[g]["description"],
                         "Therapy": ", ".join(FUHRMAN_GRADING[g]["therapy"])}
                        for g in range(1, 5)
                    ])
                    grading_ref.to_excel(writer, index=False, sheet_name='Grading_Reference')
                
                excel_data = excel_buffer.getvalue()
                
                col_exp1, col_exp2 = st.columns(2)
                
                with col_exp1:
                    st.download_button(
                        label="📊 Download Excel Report",
                        data=excel_data,
                        file_name=f"Mathrix_AI_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
                with col_exp2:
                    # CSV download
                    csv_data = df_export.to_csv(index=False)
                    st.download_button(
                        label="📄 Download CSV Report",
                        data=csv_data,
                        file_name=f"Mathrix_AI_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                # JSON export option
                st.markdown("#### JSON Export")
                json_data = json.dumps(
                    [d for d in st.session_state.processed_data if "error" not in d],
                    indent=2,
                    default=str
                )
                
                st.download_button(
                    label="🔧 Download JSON Data",
                    data=json_data,
                    file_name=f"Mathrix_AI_Data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
                
                st.info("💡 *Note:* Excel report contains both analysis summary and grading reference sheets.")
            else:
                st.warning("No processed data available for export.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
        <p>Mathrix AI v2.1.0 | For Clinical Research Use Only | Consult healthcare professional for medical decisions</p>
        <p>⚠️ This system assists with preliminary analysis. All results must be validated by a qualified pathologist.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if _name_ == "_main_":
    main()
