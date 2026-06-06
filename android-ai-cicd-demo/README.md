# Android AI CI/CD Demo

这个项目演示 Android 应用提交代码后，GitHub Actions 自动构建 APK、调用 DeepSeek 生成测试用例、运行单元测试和 UI 自动化测试，并输出中文测试报告。

## 项目内容

```text
app/src/main/java/com/example/aicicd/MainActivity.java       Demo 界面
app/src/main/java/com/example/aicicd/Calculator.java         示例业务类
app/src/test/java/com/example/aicicd/CalculatorTest.java     人工单元测试
app/src/androidTest/java/com/example/aicicd/MainActivityUiTest.java  Espresso UI 测试
scripts/generate_ai_android_tests.py                         DeepSeek 生成 JUnit 测试
scripts/android_junit_summary.py                             测试报告汇总
scripts/generated_android_tests_summary.py                   展示 AI 生成用例
```

## App 界面

APK 打开后会显示一个简单页面：

```text
Android AI CI/CD Demo
Push code to build APK, run tests, and show reports in GitHub Actions.
```

## CI/CD 流程

每次修改 `android-ai-cicd-demo/**` 并 push 后，会触发 `Android APK CI`：

`android-build-test` job：

1. 拉取代码。
2. 安装 JDK、Android SDK、Gradle。
3. 调用 DeepSeek 根据 Java 源码生成 JUnit 测试。
4. 运行单元测试：`gradle :app:testDebugUnitTest`。
5. 构建 Debug APK：`gradle :app:assembleDebug`。
6. 在 GitHub Actions Summary 显示中文测试报告和 DeepSeek 生成的测试代码。
7. 上传 APK、单元测试报告和 AI 生成测试文件。

`android-ui-test` job：

1. 启动 GitHub 云端 Android 模拟器。
2. 运行 UI 自动化测试：`gradle :app:connectedDebugAndroidTest`。
3. 在 Summary 显示 UI 测试报告。
4. 上传 UI 测试报告。

UI job 是辅助验证，模拟器启动失败不会阻塞 APK 构建。

## GitHub Secret

仓库需要配置：

```text
DEEPSEEK_API_KEY
```

如果没有配置，DeepSeek 生成测试步骤会跳过，但 APK 构建、人工单元测试和 UI 自动化测试仍然会运行。

## 查看报告

进入：

```text
https://github.com/mingyuxia2016-ux/test0606/actions
```

然后：

1. 点最新的 `Android APK CI`。
2. 打开运行详情。
3. 查看 `Summary`。

Summary 中会显示：

- 单元测试统计。
- UI 自动化测试统计。
- 失败用例信息。
- DeepSeek 生成的测试代码。

## 下载 APK

在 `Android APK CI` 的运行详情底部找到 `Artifacts`，下载：

```text
android-ai-cicd-artifacts
```

解压后 APK 路径：

```text
app/build/outputs/apk/debug/app-debug.apk
```

## 本地运行

如果本机安装了 Android SDK 和 Gradle：

```bash
gradle :app:testDebugUnitTest
gradle :app:assembleDebug
gradle :app:connectedDebugAndroidTest
```

本地调用 DeepSeek 生成测试：

```bash
python scripts/generate_ai_android_tests.py
```

## 注意事项

- UI 自动化测试会启动 GitHub 云端 Android 模拟器，耗时比单元测试更久。
- 如果日志出现 `adb: device offline`，或长时间重复 `getprop sys.boot_completed`，通常是模拟器启动不稳定，可以重新运行 workflow。
- 当前项目是学习 Demo，重点是 CI/CD 链路，不是完整生产级 Android 应用。
