"""List available Google Generative AI models for the configured API key.

Usage:
  python backend/tools/list_models.py

If a usable text generation model is found, the script prints it.
"""
import os
import sys
from dotenv import load_dotenv

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# load env
load_dotenv(os.path.join(ROOT, ".env"))

try:
    from core.config import settings
except Exception:
    # fallback to env var
    class settings:
        google_api_key = os.environ.get("GOOGLE_API_KEY")

if not settings.google_api_key:
    print("No GOOGLE_API_KEY found in environment or .env")
    sys.exit(2)

try:
    import google.generativeai as genai
except Exception as e:
    print("google.generativeai package not installed:", e)
    sys.exit(3)

try:
    genai.configure(api_key=settings.google_api_key)
    models = genai.list_models()
    print("Retrieved models:")
    for m in models:
        # each m is typically a dict-like object
        print(m)
    # try to find a text generation model candidate
    candidates = []
    for m in models:
        name = m.get("name") if isinstance(m, dict) else getattr(m, "name", None)
        if not name:
            continue
        # prefer models that support 'generate' or 'chat'
        if "generate" in str(m) or "chat" in str(m) or "text" in name:
            candidates.append(name)
    if candidates:
        print("\nSuggested candidates:")
        for c in candidates:
            print(c)
    else:
        print("No obvious generation-capable models found in list output.")
except Exception as e:
    print("Error calling list_models:", e)
    sys.exit(4)
