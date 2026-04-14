import streamlit as st
import google.generativeai as genai
import PIL.Image
import io
from config import get_api_key
from datetime import datetime

# ==============================================
# PAGE CONFIGURATION
# ==============================================
st.set_page_config(
    page_title="VitalLogic AI - Medical Image Analysis",
    page_icon="🏥",
    layout="wide"
)

# ==============================================
# HEADER SECTION
# ==============================================
st.title("🏥 VitalLogic AI")
st.subheader("AI-Powered Medical Image Analysis for Rural Ethiopia")
st.markdown("---")

# ==============================================
# SIDEBAR FOR INFO (NO API KEY INPUT NEEDED)
# ==============================================
with st.sidebar:
    st.header("🏥 VitalLogic AI")
    st.markdown("---")
    st.markdown("### 📋 About")
    st.markdown("""
    **VitalLogic AI** helps rural healthcare workers:
    - Upload medical images (Ultrasound, X-ray, CT)
    - Get instant AI analysis
    - Receive clear, simple recommendations
    """)
    
    st.markdown("---")
    st.markdown("✅ **Status:** AI Engine Ready")
    st.markdown("🔒 **Secure:** API key stored safely")
    
    st.markdown("---")
    st.markdown("⚠️ **Disclaimer:** This is an AI assistant. Always consult a medical professional.")

# ==============================================
# CONFIGURE GEMINI (USING SECURE API KEY FROM .ENV)
# ==============================================
try:
    api_key = get_api_key()
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-flash-latest')
except Exception as e:
    st.error(f"Error configuring API: {str(e)}")
    st.info("💡 Please make sure your .env file contains a valid GEMINI_API_KEY")
    st.stop()

# ==============================================
# IMAGE UPLOAD SECTION
# ==============================================
col1, col2 = st.columns(2)

with col1:
    st.header("📤 Upload Medical Image")
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["jpg", "jpeg", "png", "dcm"],
        help="Upload ultrasound, X-ray, or CT scan images"
    )

with col2:
    st.header("⚙️ Analysis Settings")
    analysis_depth = st.select_slider(
        "Analysis Detail Level",
        options=["Basic (Quick)", "Standard", "Detailed (Comprehensive)"],
        value="Standard"
    )
    
    analyze_button = st.button("🔍 ANALYZE IMAGE", type="primary", use_container_width=True)

# ==============================================
# IMAGE DISPLAY
# ==============================================
if uploaded_file is not None:
    # Open and display the image
    image = PIL.Image.open(uploaded_file)
    
    st.markdown("---")
    st.header("🖼️ Uploaded Image")
    st.image(image, caption="Medical Image for Analysis", use_container_width=True)

# ==============================================
# ANALYSIS SECTION
# ==============================================
if analyze_button and uploaded_file is not None:
    with st.spinner("🧠 VitalLogic AI is analyzing the image..."):
        try:
            # Customize prompt based on detail level
            if analysis_depth == "Basic (Quick)":
                prompt = """
You are VitalLogic AI, a medical diagnostic assistant for rural Ethiopia.

Analyze this medical image and provide a QUICK assessment:
1. What type of image is this?
2. Any obvious abnormalities?
3. One sentence recommendation for the healthcare worker.

Keep it VERY SHORT and simple.
"""
            elif analysis_depth == "Detailed (Comprehensive)":
                prompt = """
You are VitalLogic AI, a medical diagnostic assistant for rural Ethiopia.

Analyze this medical image and provide a COMPREHENSIVE report:
1. Image type and quality assessment
2. Anatomical structures visible
3. Detailed analysis of any abnormalities or normal findings
4. Specific clinical recommendations
5. Any follow-up actions needed

Be thorough but keep language clear for a nurse.
"""
            else:  # Standard
                prompt = """
You are VitalLogic AI, a medical diagnostic assistant for rural Ethiopia.

Analyze this medical image and provide:
1. What type of image is this (ultrasound, X-ray, CT scan)?
2. What anatomical structures do you see?
3. Are there any visible abnormalities?
4. What should the healthcare worker do next?

Keep your answer SIMPLE and CLEAR. A nurse with basic training must understand it.
"""
            
            # Get analysis from Gemini
            response = model.generate_content([prompt, image])
            
            # Display results
            st.markdown("---")
            st.header("📋 Diagnostic Report")
            
            # Create a nice card for the result
            with st.container():
                st.markdown("""
                <style>
                .diagnostic-card {
                    background-color: #f0f2f6;
                    padding: 20px;
                    border-radius: 10px;
                    border-left: 5px solid #2ecc71;
                }
                </style>
                """, unsafe_allow_html=True)
                
                st.markdown('<div class="diagnostic-card">', unsafe_allow_html=True)
                st.markdown("#### 🤖 VitalLogic AI Analysis")
                st.write(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Add a timestamp
            st.caption(f"Analysis completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            st.info("💡 Tip: Make sure your API key is valid and you have internet connection.")

elif analyze_button and uploaded_file is None:
    st.warning("⚠️ Please upload a medical image first.")

# ==============================================
# FOOTER
# ==============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 12px;">
    <p>VitalLogic AI - Transforming Legacy Medical Hardware into AI-Powered Diagnostic Tools</p>
    <p>For rural Ethiopia | SDG 3 (Good Health) | SDG 9 (Innovation)</p>
</div>
""", unsafe_allow_html=True)