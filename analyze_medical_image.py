import google.generativeai as genai
import PIL.Image
import os

# ==============================================
# STEP 1: Enter your API key here
# ==============================================
# Replace "YOUR_API_KEY_HERE" with the key you copied from Google AI Studio
# Example: genai.configure(api_key="AIzaSyD1234567890abcdef")
genai.configure(api_key="AIzaSyCZc3iDDsw94yyz34Ol-7sjClfnCbH3i3A")

# ==============================================
# STEP 2: Load the Gemini model
# ==============================================
model = genai.GenerativeModel('models/gemini-flash-latest')

# ==============================================
# STEP 3: Function to analyze medical images
# ==============================================
def analyze_medical_image(image_path):
    """
    This function takes a medical image and returns AI analysis
    """
    try:
        # Load the image
        img = PIL.Image.open(image_path)
        
        # Create the prompt for the AI
        prompt = """
You are VitalLogic AI, a medical diagnostic assistant for rural Ethiopia.

Analyze this medical image and provide:
1. What type of image is this (ultrasound, X-ray, CT scan)?
2. What anatomical structures do you see?
3. Are there any visible abnormalities?
4. What should the healthcare worker do next?

Keep your answer SIMPLE and CLEAR. A nurse with basic training must understand it.
Be honest if you cannot see something clearly.
"""
        
        # Send to Gemini for analysis
        response = model.generate_content([prompt, img])
        
        return response.text
        
    except Exception as e:
        return f"Error: {str(e)}"

# ==============================================
# STEP 4: Run the analysis
# ==============================================
if __name__ == "__main__":
    # Ask user for image file path
    image_path = input("Enter the path to your medical image: ")
    
    if os.path.exists(image_path):
        print("\n🔍 Analyzing image... This may take 5-10 seconds.\n")
        result = analyze_medical_image(image_path)
        print("=" * 50)
        print("VITALLOGIC AI - DIAGNOSTIC ASSISTANT")
        print("=" * 50)
        print(result)
        print("=" * 50)
        print("\n⚠️ DISCLAIMER: This is an AI assistant. Always consult a medical professional.")
    else:
        print("File not found. Please check the path and try again.")