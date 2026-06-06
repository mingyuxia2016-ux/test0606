from pathlib import Path


GENERATED_TEST_PATH = Path("app/src/test/java/com/example/aicicd/GeneratedAiTest.java")


def main() -> None:
    print("# DeepSeek 生成的 Android 测试用例\n")

    if not GENERATED_TEST_PATH.exists():
        print("本次流水线没有生成 AI Android 测试用例。")
        return

    generated_code = GENERATED_TEST_PATH.read_text(encoding="utf-8", errors="ignore").strip()
    if not generated_code:
        print("AI Android 测试文件为空。")
        return

    print("下面是 DeepSeek 根据 Android 源码自动生成的 JUnit 用例：\n")
    print("```java")
    print(generated_code)
    print("```")


if __name__ == "__main__":
    main()
