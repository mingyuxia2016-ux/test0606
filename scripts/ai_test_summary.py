import os
import sys
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


DEFAULT_REPORTS = [
    Path("reports/junit-base.xml"),
    Path("reports/junit-ai.xml"),
]


SYSTEM_PROMPT = """You are a senior QA automation engineer.
Summarize pytest/JUnit XML failures in concise Chinese.
Include failed tests, likely causes, and concrete fix suggestions.
"""


def read_reports(paths: list[Path]) -> str:
    contents = []
    for path in paths:
        if path.exists():
            contents.append(f"===== {path} =====\n{path.read_text(encoding='utf-8', errors='ignore')}")
    return "\n\n".join(contents)


def call_deepseek(report_text: str) -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return "DEEPSEEK_API_KEY is not set. Skipping DeepSeek failure summary."

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
                    {"role": "user", "content": report_text},
                ],
                "temperature": 0.2,
            },
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except (httpx.HTTPError, KeyError, IndexError) as exc:
        return f"DeepSeek failure summary could not be generated: {exc}"


def main() -> None:
    paths = [Path(arg) for arg in sys.argv[1:]] or DEFAULT_REPORTS
    report_text = read_reports(paths)
    if not report_text:
        print("No test reports found. Nothing to summarize.")
        return

    print(call_deepseek(report_text))


if __name__ == "__main__":
    main()
