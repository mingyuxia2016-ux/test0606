# CI/CD + DeepSeek 自动化测试 Demo

这个仓库包含两个学习型项目：

- `FastAPI` 接口自动化测试 Demo
- `Android` APK 自动构建 + AI 生成测试 + UI 自动化测试 Demo

目标是演示：提交代码后，GitHub Actions 自动构建、自动测试、调用 DeepSeek 生成用例，并在 Actions Summary 中输出中文测试报告。

## 仓库结构

```text
app/                         FastAPI 示例服务
tests/                       FastAPI 人工接口测试
scripts/                     FastAPI 测试生成、报告汇总脚本
android-ai-cicd-demo/        Android APK CI/CD Demo
.github/workflows/ci.yml     FastAPI CI
.github/workflows/android-ci.yml  Android APK CI
```

## FastAPI Demo

提供接口：

```text
GET  /health
POST /api/calculate
POST /api/summarize
POST /api/reverse
```

本地安装依赖：

```bash
pip install -r requirements.txt
```

启动服务：

```bash
uvicorn app.main:app --reload
```

接口文档：

```text
http://127.0.0.1:8000/docs
```

运行人工接口测试：

```bash
python -m pytest tests --junitxml=reports/junit-base.xml
```

导出 OpenAPI：

```bash
python scripts/export_openapi.py
```

调用 DeepSeek 生成接口测试：

```bash
python scripts/generate_ai_tests.py
```

运行 AI 生成的接口测试：

```bash
python -m pytest generated_tests --junitxml=reports/junit-ai.xml
```

## Android APK Demo

Android 项目位于：

```text
android-ai-cicd-demo/
```

它会在 GitHub Actions 中自动执行：

1. 安装 JDK、Android SDK、Gradle。
2. 调用 DeepSeek 根据 Android Java 源码生成 JUnit 测试。
3. 运行本地单元测试：`gradle :app:testDebugUnitTest`。
4. 构建 Debug APK：`gradle :app:assembleDebug`。
5. 启动 Android 模拟器并运行 UI 自动化测试：`gradle :app:connectedDebugAndroidTest`。
6. 在 Actions Summary 显示中文测试报告。
7. 在 Actions Summary 显示 DeepSeek 生成的测试用例。
8. 上传 APK、单元测试报告、UI 测试报告和 AI 生成用例。

APK artifact 名称：

```text
android-ai-cicd-artifacts
```

APK 在 artifact 中的位置：

```text
app/build/outputs/apk/debug/app-debug.apk
```

## GitHub Actions

FastAPI workflow：

```text
CI
```

Android workflow：

```text
Android APK CI
```

查看地址：

```text
https://github.com/mingyuxia2016-ux/test0606/actions
```

看测试报告：

1. 打开 Actions。
2. 点最新一次运行。
3. 查看页面里的 `Summary`。
4. Summary 会显示测试统计、失败用例和 DeepSeek 生成的测试代码。

下载 APK：

1. 打开 `Android APK CI` 的运行详情。
2. 在页面底部找到 `Artifacts`。
3. 下载 `android-ai-cicd-artifacts`。
4. 解压后找到 `app-debug.apk`。

## DeepSeek 配置

仓库需要配置 GitHub Secret：

```text
DEEPSEEK_API_KEY
```

默认环境变量：

```text
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

如果没有配置 `DEEPSEEK_API_KEY`，AI 生成测试步骤会跳过，但已有测试和构建仍会运行。

## 说明

- AI 生成测试用于辅助发现问题，生成内容会展示在 Actions Summary。
- Android UI 自动化测试需要启动 GitHub 云端模拟器，速度较慢，也可能偶发 emulator offline。这类问题属于 CI 运行环境波动，不一定代表 App 或测试代码有问题。
- 当前 Android App 是学习 Demo，界面很简单，重点是 CI/CD、APK 构建、AI 生成测试和测试报告链路。
