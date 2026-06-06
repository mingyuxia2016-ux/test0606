import os
import re
import sys
from pathlib import Path

import httpx


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_SOURCE_DIR = PROJECT_ROOT / "app/src/main/java/com/example/aicicd"
OUTPUT_PATH = PROJECT_ROOT / "app/src/test/java/com/example/aicicd/GeneratedAiTest.java"


SYSTEM_PROMPT = """You generate Java JUnit 4 unit tests for an Android project.
Return only valid Java code, with no Markdown fences and no explanations.
The test class package must be com.example.aicicd.
The test class name must be GeneratedAiTest.
Use org.junit.Test and org.junit.Assert.
Tests must be local JVM unit tests and must not use Android device APIs, emulator APIs, network, files, time, randomness, or external services.
Add short Chinese comments above each test method to explain the test purpose.
Only test public behavior visible in the provided source code.
"""


def strip_markdown_code_block(text: str) -> str:
    match = re.search(r"```(?:java)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip() + "\n"
    return text.strip() + "\n"


def read_sources() -> str:
    parts = []
    for path in sorted(MAIN_SOURCE_DIR.glob("*.java")):
        parts.append(f"===== {path.name} =====\n{path.read_text(encoding='utf-8')}")
    return "\n\n".join(parts)


def call_deepseek(prompt: str) -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("DEEPSEEK_API_KEY is not set. Skipping DeepSeek Android test generation.")
        sys.exit(0)

    base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").rstrip("/")
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    try:
        response = httpx.post(
            f"{base_url}/chat/completions",
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
        return response.json()["choices"][0]["message"]["content"]
    except (httpx.HTTPError, KeyError, IndexError) as exc:
        print(f"DeepSeek Android test generation failed: {exc}")
        sys.exit(0)


def main() -> None:
    sources = read_sources()
    if not sources:
        print("No Android Java source files found. Skipping AI test generation.")
        return

    prompt = (
        "请根据下面的 Android Java 源码生成本地 JVM 单元测试。"
        "只输出 GeneratedAiTest.java 的完整 Java 源码。\n\n"
        f"{sources}"
    )
    generated_code = strip_markdown_code_block(call_deepseek(prompt))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(generated_code, encoding="utf-8")
    print(f"DeepSeek-generated Android tests written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
