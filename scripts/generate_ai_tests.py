import json
import os
import re
import sys
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


OPENAPI_PATH = Path("reports/openapi.json")
OUTPUT_PATH = Path("generated_tests/test_ai_generated_api.py")


SYSTEM_PROMPT = """You generate pytest tests for a FastAPI application.
Return only valid Python code, with no Markdown fences and no explanations.
The test file must import TestClient from fastapi.testclient and app from app.main.
Use client = TestClient(app).
Tests must be deterministic and must not require a live server or network.
Include happy-path, validation-error, and boundary-style cases when the OpenAPI schema supports them.
Do not test undocumented endpoints.
"""


def strip_markdown_code_block(text: str) -> str:
    match = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip() + "\n"
    return text.strip() + "\n"


def build_prompt(openapi_spec: dict) -> str:
    return (
        "Generate pytest API tests for this FastAPI OpenAPI document.\n"
        "Use only the public contract shown here.\n\n"
        f"{json.dumps(openapi_spec, ensure_ascii=False, indent=2)}"
    )


def call_deepseek(prompt: str) -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("DEEPSEEK_API_KEY is not set. Skipping DeepSeek test generation.")
        sys.exit(0)

    base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").rstrip("/")
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    url = f"{base_url}/chat/completions"

    response = httpx.post(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.1,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


def main() -> None:
    if not OPENAPI_PATH.exists():
        raise FileNotFoundError(f"OpenAPI file not found: {OPENAPI_PATH}")

    openapi_spec = json.loads(OPENAPI_PATH.read_text(encoding="utf-8"))
    generated_code = strip_markdown_code_block(call_deepseek(build_prompt(openapi_spec)))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(generated_code, encoding="utf-8")
    print(f"DeepSeek-generated tests written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
