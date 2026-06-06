from pathlib import Path


GENERATED_TEST_PATH = Path("generated_tests/test_ai_generated_api.py")


def main() -> None:
    print("# DeepSeek 生成的接口测试用例\n")

    if not GENERATED_TEST_PATH.exists():
        print("本次流水线没有生成 AI 接口测试用例。")
        return

    generated_code = GENERATED_TEST_PATH.read_text(encoding="utf-8", errors="ignore").strip()
    if not generated_code:
        print("AI 接口测试文件为空。")
        return

    print("下面是 DeepSeek 根据 OpenAPI 自动生成的 pytest 用例代码：\n")
    print("```python")
    print(generated_code)
    print("```")


if __name__ == "__main__":
    main()
