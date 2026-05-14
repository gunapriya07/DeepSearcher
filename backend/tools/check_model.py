"""Check a Google Generative AI model availability using configured API key.

Usage:
  python backend/tools/check_model.py --model gemini-2.0-pro

If no --model is provided, the script uses the `llm_model` from core.config.settings.
"""
import argparse
import sys
import os

# Ensure the `backend` package root is on sys.path so imports like `core.config` work
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Load environment variables from backend/.env so pydantic Settings can find keys
from dotenv import load_dotenv
load_dotenv(os.path.join(ROOT, ".env"))

from langchain_google_genai import ChatGoogleGenerativeAI
from core.config import settings


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", help="Model name to test (overrides settings.llm_model)")
    p.add_argument("--auto", action="store_true", help="Auto-probe common Gemini models and update backend/.env on success")
    args = p.parse_args()

    if args.auto:
        candidates = [
            "gemini-2.0-pro",
            "gemini-1.5-pro",
            "gemini-2.0-flash",
            "gemini-1.5-flash",
        ]
        print("Auto-probing models:", candidates)
        for candidate in candidates:
            print(f"Trying {candidate}...")
            try:
                llm = ChatGoogleGenerativeAI(model=candidate, google_api_key=settings.google_api_key)
                res = llm.invoke("ping")
                print(f"OK: {candidate} responded")
                if update_env_model(os.path.join(ROOT, ".env"), candidate):
                    print(f"Wrote LLM_MODEL={candidate} to backend/.env")
                sys.exit(0)
            except Exception as e:
                print(f"{candidate} failed: {e}")
        print("No candidate models succeeded.")
        sys.exit(3)

    model = args.model or settings.llm_model
    print(f"Testing model: {model}")

    try:
        llm = ChatGoogleGenerativeAI(model=model, google_api_key=settings.google_api_key)
        # Some wrappers provide .invoke() that raises descriptive exceptions
        res = llm.invoke("ping")
        print("OK: model responded")
        if hasattr(res, "content"):
            print("Response content:")
            print(res.content)
        sys.exit(0)
    except Exception as e:
        print("ERROR:")
        print(e)
        sys.exit(2)


def update_env_model(env_path: str, model_name: str) -> bool:
    """Update or append LLM_MODEL in the .env file. Returns True if written."""
    try:
        lines = []
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

        key = "LLM_MODEL"
        updated = False
        for i, line in enumerate(lines):
            if line.strip().upper().startswith(key + "="):
                lines[i] = f"{key}={model_name}\n"
                updated = True
                break

        if not updated:
            lines.append(f"{key}={model_name}\n")

        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        return True
    except Exception as e:
        print(f"Failed to update .env: {e}")
        return False


if __name__ == "__main__":
    main()
