import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime
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

def is_blurry(image, threshold=100):
    """Check if image is blurry using Laplacian variance"""
    try:
        if image is None or len(image.shape) < 2:
            return True
        
        # Ensure image is uint8
        if image.dtype != np.uint8:
            image = image.astype(np.uint8)
        
        laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
        return laplacian_var < threshold
    except:
        return True

def extract_nuclear_features(image):
    """Extract nuclear features from pathology image"""
    try:
        if image is None or len(image.shape) < 2:
            return {"mean_diameter": 10, "nuclear_count": 0}
        
        # Convert to uint8 if needed
        if image.dtype != np.uint8:
            image = image.astype(np.uint8)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        
        # Apply adaptive thresholding
        binary = cv2.adaptiveThreshold(blurred, 255, 
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY_INV, 11, 2)
        
        # Morphological operations to clean up
        kernel = np.ones((3, 3), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours or len(contours) < 5:
            return {"mean_diameter": 10, "nuclear_count": 0}
        
        # Filter contours by area (remove too small or too large)
        diameters = []
        valid_contours = []
        
        for contour in contours[:100]:  # Limit for performance
            area = cv2.contourArea(contour)
            if 20 < area < 500:  # Reasonable nuclear size range
                # Get bounding circle
                (x, y), radius = cv2.minEnclosingCircle(contour)
                diameter = radius * 2
                diameters.append(diameter)
                valid_contours.append(contour)
        
        if diameters:
            mean_diameter = np.mean(diameters)
            # Convert pixels to micrometers (assuming 1 pixel = 0.25 μm at 40x magnification)
            mean_diameter_um = mean_diameter * 0.25
            diameter_std = np.std(diameters)
        else:
            mean_diameter_um = 10
            diameter_std = 0
        
        return {
            "mean_diameter": round(mean_diameter_um, 2),
            "nuclear_count": len(valid_contours),
            "diameter_std": round(diameter_std, 2),
            "contours": valid_contours
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

def process_image(image_file):
    """Process a single pathology image and extract features"""
    try:
        # Convert to PIL Image
        image = Image.open(image_file)
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        img_array = np.array(image)
        
        # Convert to grayscale for processing
        if len(img_array.shape) == 3:
            img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            img_gray = img_array
        
        # Resize if too large for performance
        height, width = img_gray.shape
        if height > 1000 or width > 1000:
            scale = 1000 / max(height, width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            img_gray = cv2.resize(img_gray, (new_width, new_height))
        
        # Check image quality
        if is_blurry(img_gray):
            return {
                "patient_id": os.path.splitext(image_file.name)[0],
                "detected_grade": "N/A",
                "mean_nuclear_diameter": 0,
                "recommended_medication": "Image quality insufficient",
                "morphology": "Blurry image - cannot analyze",
                "description": "Image quality insufficient for nuclear analysis",
                "image_data": img_array,
                "error": "Blurry image"
            }
        
        # Extract features
        features = extract_nuclear_features(img_gray)
        
        # Determine Fuhrman grade
        if "error" in features:
            grade = 2  # Default grade
        else:
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
            "features": features,
            "filename": image_file.name
        }
        
    except Exception as e:
        return {
            "patient_id": os.path.splitext(image_file.name)[0] if hasattr(image_file, 'name') else "Unknown",
            "detected_grade": "Error",
            "mean_nuclear_diameter": 0,
            "recommended_medication": "Processing error",
            "morphology": f"Error: {str(e)}",
            "description": f"Error processing image: {str(e)}",
            "error": f"Image processing error: {str(e)}"
        }

def create_summary_dataframe(processed_data):
    """Create summary DataFrame from processed data"""
    records = []
    for item in processed_data:
        if item and isinstance(item, dict):
            records.append({
                "Patient ID": item.get("patient_id", "Unknown"),
                "Detected Grade": item.get("detected_grade", "N/A"),
                "Mean Nuclear Diameter (μm)": item.get("mean_nuclear_diameter", 0),
                "Recommended Medication": item.get("recommended_medication", "N/A"),
                "Morphology": item.get("morphology", "N/A"),
                "Filename": item.get("filename", "Unknown"),
                "Processing Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    if records:
        return pd.DataFrame(records)
    else:
        return pd.DataFrame(columns=["Patient ID", "Detected Grade", "Mean Nuclear Diameter (μm)", 
                                     "Recommended Medication", "Morphology", "Filename", "Processing Date"])

def plot_nuclear_analysis(image, features, grade):
    """Create visualization for nuclear analysis"""
    try:
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        
        # Original image
        if image is not None and len(image.shape) >= 2:
            if len(image.shape) == 2:
                axes[0].imshow(image, cmap='gray')
            else:
                axes[0].imshow(image)
            axes[0].set_title(f'Pathology Image - Grade {grade}')
            axes[0].axis('off')
        else:
            axes[0].text(0.5, 0.5, 'No image available', 
                        horizontalalignment='center', verticalalignment='center')
            axes[0].axis('off')
        
        # Grade distribution chart
        grades = [1, 2, 3, 4]
        diameters = [10, 15, 20, 25]
        colors = ['green', 'yellow', 'orange', 'red']
        
        axes[1].bar(grades, diameters, color=colors, alpha=0.6)
        current_diameter = features.get("mean_diameter", 10)
        axes[1].axhline(y=current_diameter, color='r', 
                        linestyle='--', label=f'Detected: {current_diameter:.1f}μm')
        axes[1].set_xlabel('Fuhrman Grade')
        axes[1].set_ylabel('Mean Nuclear Diameter (μm)')
        axes[1].set_title('Fuhrman Grading Scale')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        # Features summary
        axes[2].axis('off')
        feature_text = f"""
        Analysis Results:
        -----------------
        Grade: {grade}
        Mean Diameter: {current_diameter:.1f} μm
        Nuclear Count: {features.get('nuclear_count', 0)}
        Diameter STD: {features.get('diameter_std', 0):.2f}
        """
        axes[2].text(0.1, 0.5, feature_text, fontsize=10, 
                    verticalalignment='center', 
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        return fig
    except Exception as e:
        # Return empty figure if plotting fails
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, f'Visualization error: {str(e)}', 
                horizontalalignment='center', verticalalignment='center')
        ax.axis('off')
        return fig

def process_pdf_simple(pdf_file):
    """Simple PDF processing (mock implementation)"""
    try:
        # Mock processing - in real app, use PyPDF2 or pdf2image
        return {
            "patient_id": os.path.splitext(pdf_file.name)[0],
            "detected_grade": 2,  # Default grade for PDF
            "mean_nuclear_diameter": 15.5,
            "recommended_medication": "Partial Nephrectomy, Radical Nephrectomy",
            "morphology": "PDF clinical report - manual review required",
            "description": "Clinical report analysis pending",
            "source": "PDF Report",
            "filename": pdf_file.name,
            "note": "PDF processing requires additional libraries (PyPDF2/pdf2image/pytesseract)"
        }
    except:
        return {
            "patient_id": pdf_file.name,
            "detected_grade": "N/A",
            "mean_nuclear_diameter": 0,
            "recommended_medication": "Manual review required",
            "morphology": "PDF processing error",
            "description": "Could not process PDF file",
            "error": "PDF processing failed"
        }

# Main application
def main():
    st.title("🏥 Mathrix AI - Pathology Analysis System")
    st.markdown("### Advanced Medical Intelligence for Renal Cell Carcinoma Grading")
    
    # Sidebar for clinical inputs
    with st.sidebar:
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
                        progress = (i + 1) / len(uploaded_files)
                        progress_bar.progress(progress)
                        
                        try:
                            if file.type.startswith('image'):
                                result = process_image(file)
                            elif file.type == 'application/pdf':
                                result = process_pdf_simple(file)
                            else:
                                result = {"error": f"Unsupported file type: {file.type}"}
                            
                            processed_results.append(result)
                        except Exception as e:
                            processed_results.append({
                                "filename": file.name,
                                "error": f"Processing error: {str(e)}"
                            })
                    
                    st.session_state.processed_data = processed_results
                    progress_bar.empty()
                    
                    # Count successful processes
                    successful = len([d for d in processed_results if "error" not in d])
                    st.success(f"✅ Processed {successful}/{len(uploaded_files)} file(s) successfully!")
    
    with col2:
        st.subheader("⚙️ Batch Processing Status")
        if st.session_state.processed_data:
            successful = len([d for d in st.session_state.processed_data if "error" not in d])
            total = len(st.session_state.processed_data)
            
            st.metric("Successfully Processed", f"{successful}/{total}")
            
            if successful > 0:
                grades = []
                for d in st.session_state.processed_data:
                    if "error" not in d and "detected_grade" in d:
                        grade = d["detected_grade"]
                        if isinstance(grade, (int, float)) and grade > 0:
                            grades.append(grade)
                
                if grades:
                    avg_grade = np.mean(grades)
                    st.metric("Average Grade", f"{avg_grade:.1f}")
    
    # Display results if available
    if st.session_state.processed_data:
        st.markdown("---")
        st.subheader("📊 Analysis Results")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📈 Detailed View", "📋 Summary Table", "📥 Export Data"])
        
        with tab1:
            # Navigation for multiple files
            if len(st.session_state.processed_data) > 1:
                col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
                with col_nav2:
                    file_options = []
                    for i, data in enumerate(st.session_state.processed_data):
                        name = data.get("filename", f"File {i+1}")
                        if "error" in data:
                            name += " ⚠️"
                        file_options.append((i, name))
                    
                    selected_index = st.selectbox(
                        "Select File to View",
                        range(len(st.session_state.processed_data)),
                        format_func=lambda x: st.session_state.processed_data[x].get("filename", f"File {x+1}"),
                        index=st.session_state.current_file_index
                    )
                    st.session_state.current_file_index = selected_index
            
            current_data = st.session_state.processed_data[st.session_state.current_file_index]
            
            if "error" in current_data:
                st.error(f"❌ Error: {current_data['error']}")
            else:
                # Display in two columns
                col_img, col_info = st.columns([1, 1])
                
                with col_img:
                    if "image_data" in current_data and current_data["image_data"] is not None:
                        try:
                            st.image(current_data["image_data"], 
                                    caption=f"Pathology Image - {current_data.get('patient_id', 'Unknown')}",
                                    use_column_width=True)
                        except:
                            st.info("Image display not available")
                    
                    # Show visualization
                    if "features" in current_data:
                        try:
                            image_for_plot = current_data.get("image_data")
                            if image_for_plot is not None and len(image_for_plot.shape) == 3:
                                # Convert to grayscale for plotting
                                image_for_plot = cv2.cvtColor(image_for_plot, cv2.COLOR_RGB2GRAY)
                            
                            fig = plot_nuclear_analysis(
                                image_for_plot,
                                current_data["features"],
                                current_data.get("detected_grade", 0)
                            )
                            st.pyplot(fig)
                        except Exception as e:
                            st.warning(f"Could not generate visualization: {str(e)}")
                
                with col_info:
                    st.markdown(f"### Patient: {current_data.get('patient_id', 'Unknown')}")
                    
                    # Grade display with color coding
                    grade = current_data.get("detected_grade", 0)
                    if isinstance(grade, (int, float)):
                        grade_colors = {1: "🟢", 2: "🟡", 3: "🟠", 4: "🔴"}
                        grade_symbol = grade_colors.get(int(grade), "⚪")
                        st.markdown(f"### Fuhrman Grade: {grade_symbol} *Grade {grade}*")
                    else:
                        st.markdown(f"### Grade: {grade}")
                    
                    # Display metrics
                    col_metrics1, col_metrics2 = st.columns(2)
                    with col_metrics1:
                        diameter = current_data.get("mean_nuclear_diameter", 0)
                        if diameter > 0:
                            st.metric("Mean Nuclear Diameter", f"{diameter} μm")
                        else:
                            st.metric("Mean Nuclear Diameter", "N/A")
                    
                    with col_metrics2:
                        morphology = current_data.get("morphology", "N/A")
                        if len(morphology) > 30:
                            morphology = morphology[:30] + "..."
                        st.metric("Morphology", morphology)
                    
                    # Therapy recommendations
                    st.markdown("#### 💊 Targeted Therapy Recommendations")
                    therapy = current_data.get("recommended_medication", "")
                    if therapy:
                        if ", " in therapy:
                            meds = therapy.split(", ")
                        else:
                            meds = [therapy]
                        
                        for med in meds:
                            if med and med != "N/A":
                                st.info(f"• *{med}*")
                    else:
                        st.warning("No therapy recommendations available")
                    
                    # Morphological description
                    st.markdown("#### 🔬 Morphological Description")
                    description = current_data.get("description", "No description available")
                    st.write(description)
        
        with tab2:
            # Create and display summary table
            df_summary = create_summary_dataframe(st.session_state.processed_data)
            
            if not df_summary.empty:
                st.dataframe(df_summary, use_container_width=True)
                
                # Statistics
                st.subheader("📈 Batch Statistics")
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                
                with col_stat1:
                    if "Detected Grade" in df_summary.columns:
                        try:
                            # Convert to numeric, ignoring non-numeric values
                            grades_numeric = pd.to_numeric(df_summary["Detected Grade"], errors='coerce')
                            grades_numeric = grades_numeric.dropna()
                            if not grades_numeric.empty:
                                grade_counts = grades_numeric.value_counts().sort_index()
                                st.write("*Grade Distribution:*")
                                for grade, count in grade_counts.items():
                                    st.write(f"Grade {int(grade)}: {int(count)} cases")
                        except:
                            st.write("Grade distribution not available")
                
                with col_stat2:
                    if "Mean Nuclear Diameter (μm)" in df_summary.columns:
                        try:
                            diameters = pd.to_numeric(df_summary["Mean Nuclear Diameter (μm)"], errors='coerce')
                            diameters = diameters.dropna()
                            if not diameters.empty:
                                avg_diameter = diameters.mean()
                                st.metric("Average Diameter", f"{avg_diameter:.1f} μm")
                        except:
                            st.metric("Average Diameter", "N/A")
                
                with col_stat3:
                    if "Detected Grade" in df_summary.columns:
                        try:
                            grades_numeric = pd.to_numeric(df_summary["Detected Grade"], errors='coerce')
                            grades_numeric = grades_numeric.dropna()
                            if not grades_numeric.empty:
                                mode_result = grades_numeric.mode()
                                if not mode_result.empty:
                                    st.metric("Most Common Grade", f"Grade {int(mode_result.iloc[0])}")
                        except:
                            st.metric("Most Common Grade", "N/A")
            
            else:
                st.warning("No valid data to display in summary table.")
        
        with tab3:
            st.subheader("📥 Export Analysis Results")
            
            if st.session_state.processed_data:
                df_export = create_summary_dataframe(st.session_state.processed_data)
                
                if not df_export.empty:
                    # Excel download
                    try:
                        excel_buffer = io.BytesIO()
                        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                            df_export.to_excel(writer, index=False, sheet_name='Analysis_Summary')
                            
                            # Add grading reference sheet
                            grading_ref = pd.DataFrame([
                                {"Grade": g, 
                                 "Description": FUHRMAN_GRADING[g]["description"],
                                 "Recommended Therapy": ", ".join(FUHRMAN_GRADING[g]["therapy"])}
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
                        # Filter out None values and non-serializable objects
                        export_data = []
                        for d in st.session_state.processed_data:
                            if d and isinstance(d, dict):
                                clean_dict = {}
                                for key, value in d.items():
                                    if key != "image_data" and key != "contours":
                                        clean_dict[key] = value
                                export_data.append(clean_dict)
                        
                        json_data = json.dumps(export_data, indent=2, default=str)
                        
                        st.download_button(
                            label="🔧 Download JSON Data",
                            data=json_data,
                            file_name=f"Mathrix_AI_Data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json",
                            use_container_width=True
                        )
                        
                        st.info("💡 *Note:* Excel report contains both analysis summary and grading reference sheets.")
                        
                    except Exception as e:
                        st.error(f"Error creating export files: {str(e)}")
                        # Fallback to CSV only
                        csv_data = df_export.to_csv(index=False)
                        st.download_button(
                            label="📄 Download CSV Report (Fallback)",
                            data=csv_data,
                            file_name=f"Mathrix_AI_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                else:
                    st.warning("No data available for export.")
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
