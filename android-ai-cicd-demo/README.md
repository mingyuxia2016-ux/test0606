# Android AI CI/CD Demo

这个项目演示 Android 应用提交代码后，在 GitHub Actions 中自动构建 APK、调用 DeepSeek 生成本地单元测试、运行测试，并在 Actions Summary 中输出中文测试报告和 AI 生成的用例。

## CI/CD 流程

每次修改 `android-ai-cicd-demo/**` 并 push 后，会触发 `Android APK CI`：

1. 拉取代码。
2. 安装 JDK、Android SDK、Gradle。
3. 调用 DeepSeek 根据 Android Java 源码生成 JUnit 测试。
4. 执行 `gradle :app:testDebugUnitTest`。
5. 执行 `gradle :app:assembleDebug` 构建 APK。
6. 在 GitHub Actions Summary 显示中文测试报告。
7. 在 Summary 显示 DeepSeek 生成的测试用例代码。
8. 上传 APK、测试报告、AI 生成测试文件。

## GitHub Secret

仓库需要配置：

```text
DEEPSEEK_API_KEY
```

如果没有配置，DeepSeek 生成测试步骤会跳过，但 APK 构建和已有测试仍然会运行。

## 构建产物

GitHub Actions 的 artifact 名称：

```text
android-ai-cicd-artifacts
```

APK 位置：

```text
app/build/outputs/apk/debug/app-debug.apk
```

## 本地运行

如果本机安装了 Android SDK 和 Gradle：

```bash
gradle :app:testDebugUnitTest
gradle :app:assembleDebug
```

本地生成 AI 测试：

```bash
python scripts/generate_ai_android_tests.py
```
