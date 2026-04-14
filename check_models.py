import google.generativeai as genai
from config import get_api_key

# ==============================================
# Get API key from .env (SECURE)
# ==============================================
try:
    api_key = get_api_key()
    genai.configure(api_key=api_key)
    print("✅ API key loaded successfully from .env file\n")
except Exception as e:
    print(f"❌ Error loading API key: {str(e)}")
    print("💡 Please make sure your .env file contains a valid GEMINI_API_KEY")
    exit(1)

# ==============================================
# Fetch and display available models
# ==============================================
print("🔍 Fetching available models...\n")
print("=" * 60)

count = 0
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")
        count += 1

print("=" * 60)
print(f"\n📊 Found {count} models that support generateContent")
print("\n💡 Use one of the above model names in your app.py")
print("\n⚠️ Recommended: 'models/gemini-flash-latest' or 'models/gemini-2.5-flash'")