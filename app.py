import streamlit as st
import google.generativeai as genai
import PIL.Image
from config import get_api_key
from datetime import datetime

# ==============================================
# PAGE CONFIGURATION
# ==============================================
st.set_page_config(
    page_title="VitalLogic AI - Nurse Assistant",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==============================================
# SIMPLE CSS - NO WHITE TEXT
# ==============================================
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Title styling */
    .big-title {
        font-size: 42px;
        font-weight: bold;
        color: #1a5d3c;
        text-align: center;
        margin-bottom: 5px;
    }
    
    /* Step boxes */
    .step-box {
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
        border-left: 5px solid #1a5d3c;
    }
    
    .step-number {
        font-size: 24px;
        font-weight: bold;
        color: #1a5d3c;
        margin-right: 12px;
    }
    
    .step-text {
        font-size: 16px;
        color: #333333;
    }
    
    /* Result card */
    .result-card {
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 6px solid #2e7d32;
    }
    
    .result-card p {
        color: #1b5e20;
        font-size: 16px;
        line-height: 1.5;
    }
    
    /* Upload box */
    .upload-box {
        border: 2px dashed #1a5d3c;
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        background-color: #fafafa;
    }
    
    .upload-box p {
        color: #555555;
    }
    
    /* Status badge */
    .status-ready {
        background-color: #4caf50;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 14px;
    }
    
    /* Guide box */
    .guide-box {
        background-color: #f0f7ff;
        padding: 12px;
        border-radius: 10px;
        margin: 5px 0;
    }
    
    .guide-box p {
        color: #333333;
        font-size: 13px;
    }
    
    /* Button styling */
    .stButton button {
        background-color: #1a5d3c;
        color: white;
        font-size: 20px;
        font-weight: bold;
        padding: 12px;
        border-radius: 40px;
        width: 100%;
    }
    
    .stButton button:hover {
        background-color: #0d3b24;
        color: white;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1a5d3c;
    }
    
    /* Text colors */
    p, li, span {
        color: #333333;
    }
    
    /* File uploader text */
    .stFileUploader p {
        color: #333333;
    }
    
    /* Offline indicator */
    .offline-badge {
        background-color: #fff3e0;
        padding: 8px;
        border-radius: 8px;
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================
# HEADER
# ==============================================
st.markdown('<div class="big-title">🏥 VitalLogic AI</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 16px; color: #555;">Simple AI for Rural Nurses</p>', unsafe_allow_html=True)
st.markdown("---")

# ==============================================
# OFFLINE MODE INDICATOR
# ==============================================
st.markdown("""
<div class="offline-badge">
    <span style="color: #e67e22;">📡 Current Mode: Online Demo</span><br>
    <span style="color: #27ae60; font-size: 12px;">🔜 Offline Mode: Coming in Phase 2</span>
</div>
""", unsafe_allow_html=True)

# ==============================================
# STATUS
# ==============================================
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown('<div style="text-align: center;"><span class="status-ready">✅ Ready</span></div>', unsafe_allow_html=True)

# ==============================================
# STEP BY STEP INSTRUCTIONS
# ==============================================
st.markdown("### 📋 How to Use")

step_col1, step_col2, step_col3 = st.columns(3)

with step_col1:
    st.markdown("""
    <div class="step-box">
        <span class="step-number">1</span>
        <span class="step-text"><strong>Upload</strong><br>Click Browse to select<br>ultrasound image</span>
    </div>
    """, unsafe_allow_html=True)

with step_col2:
    st.markdown("""
    <div class="step-box">
        <span class="step-number">2</span>
        <span class="step-text"><strong>Analyze</strong><br>Click Analyze button<br>Wait 5-10 seconds</span>
    </div>
    """, unsafe_allow_html=True)

with step_col3:
    st.markdown("""
    <div class="step-box">
        <span class="step-number">3</span>
        <span class="step-text"><strong>Read</strong><br>See AI result<br>Follow recommendation</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==============================================
# CONFIGURE GEMINI
# ==============================================
try:
    api_key = get_api_key()
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-flash-latest')
except Exception as e:
    st.error(f"System Error: {str(e)}")
    st.info("Please contact your system administrator.")
    st.stop()

# ==============================================
# UPLOAD SECTION
# ==============================================
st.markdown("### 📸 Upload Ultrasound Image")

uploaded_file = st.file_uploader(
    "Choose an image file",
    type=["jpg", "jpeg", "png"],
    help="Take a photo of the ultrasound screen"
)

# ==============================================
# PROCESS IMAGE
# ==============================================
if uploaded_file is not None:
    image = PIL.Image.open(uploaded_file)
    
    st.markdown("---")
    st.markdown("### 🖼️ Your Image")
    st.image(image, caption="Ultrasound Image", use_container_width=True)
    
    st.markdown("---")
    analyze_button = st.button("🔍 START ANALYSIS")
    
    if analyze_button:
        with st.spinner("🧠 Analyzing image... Please wait 5-10 seconds."):
            try:
                # ==========================================
                # UPDATED PROMPT - SPECIFIC ANALYSIS
                # ==========================================
                prompt = """
You are VitalLogic AI, a medical diagnostic assistant for nurses in rural Ethiopia.

Look carefully at this medical image and provide a SPECIFIC analysis:

1. What type of image is this? (ultrasound, X-ray, CT scan, or other)
2. What specific body part or area do you see? (be specific - kidney, liver, heart, baby, lung, etc.)
3. What specific findings do you observe? (describe what you actually see - size, shape, color, movement, etc.)
4. Based ONLY on what you see, are there any abnormalities? (describe them specifically)
5. What should the nurse do next? (specific action)

IMPORTANT RULES:
- Be SPECIFIC. Do NOT give generic answers.
- If you see a kidney, say "kidney". If you see a baby, say "baby".
- Describe what is UNIQUE about THIS image.
- Do NOT copy the same answer for different images.
- If you cannot see clearly, say "Image quality is poor. Please retake the photo."

Remember: Each image is different. Analyze THIS image, not a generic ultrasound.
"""
                
                response = model.generate_content([prompt, image])
                
                st.markdown("---")
                st.markdown("### 📋 Analysis Result")
                
                st.markdown(f"""
                <div class="result-card">
                    <p>📝 <strong>AI Analysis:</strong><br><br>{response.text}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Simple recommendation based on keywords
                if "abnormal" in response.text.lower() or "abnormality" in response.text.lower():
                    st.warning("⚠️ **Recommendation:** Refer this patient to a doctor for further examination.")
                else:
                    st.success("✅ **Recommendation:** Continue routine care. Monitor patient as normal.")
                
                st.caption(f"Analysis completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                st.info("Check your internet connection and try again.")
else:
    st.markdown("""
    <div class="upload-box">
        <p style="font-size: 16px;">📷 Click "Browse" to select an ultrasound image</p>
        <p style="font-size: 12px;">Supported: JPG, JPEG, PNG</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================
# QUICK GUIDE
# ==============================================
st.markdown("---")
st.markdown("### 📖 Quick Guide for Nurses")

g1, g2, g3 = st.columns(3)

with g1:
    st.markdown("""
    <div class="guide-box">
        <p><strong>📷 1. Capture</strong><br>Take photo of ultrasound screen</p>
    </div>
    """, unsafe_allow_html=True)

with g2:
    st.markdown("""
    <div class="guide-box">
        <p><strong>💻 2. Upload</strong><br>Click Browse and select photo</p>
    </div>
    """, unsafe_allow_html=True)

with g3:
    st.markdown("""
    <div class="guide-box">
        <p><strong>📋 3. Read</strong><br>See result and act</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================
# FOOTER
# ==============================================
st.markdown("---")
st.markdown("""
<p style="text-align: center; color: #777; font-size: 11px;">
⚠️ AI assistant - Always consult a doctor for final diagnosis<br>
VitalLogic AI | For rural Ethiopia
</p>
""", unsafe_allow_html=True)