import google.generativeai as genai

# Configure with your API key
genai.configure(api_key="AIzaSyCZc3iDDsw94yyz34OI-7sjClfnCbH3i3A")

print("🔍 Fetching available models...\n")
print("=" * 60)

count = 0
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")
        count += 1

print("=" * 60)
print(f"\nFound {count} models that support generateContent")
print("\nUse one of the above model names in your app.py")