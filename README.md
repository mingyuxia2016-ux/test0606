# FastAPI CI/CD + DeepSeek API Test Demo

这是一个学习型 Demo，用来串起 FastAPI、接口自动化测试、GitHub Actions CI，以及 DeepSeek 自动生成接口测试用例和失败总结。

## 功能

- FastAPI 示例服务：
  - `GET /health`
  - `POST /api/calculate`
- 人工维护的 pytest 接口测试。
- 从 FastAPI 导出 OpenAPI 文档。
- 调用 DeepSeek 根据 OpenAPI 生成临时 pytest 用例。
- CI 中运行人工测试和 AI 生成测试。
- 测试失败时调用 DeepSeek 输出失败总结。

## 本地运行

安装依赖：

```bash
pip install -r requirements.txt
```

启动服务：

```bash
uvicorn app.main:app --reload
```

访问接口文档：

```text
http://127.0.0.1:8000/docs
```

## 运行基础接口测试

```bash
pytest tests --junitxml=reports/junit-base.xml
```

## 导出 OpenAPI

```bash
python scripts/export_openapi.py
```

导出文件位置：

```text
reports/openapi.json
```

## 使用 DeepSeek 生成接口测试

配置环境变量：

```bash
export DEEPSEEK_API_KEY=你的DeepSeek密钥
export DEEPSEEK_BASE_URL=https://api.deepseek.com
export DEEPSEEK_MODEL=deepseek-chat
```

Windows PowerShell：

```powershell
$env:DEEPSEEK_API_KEY="你的DeepSeek密钥"
$env:DEEPSEEK_BASE_URL="https://api.deepseek.com"
$env:DEEPSEEK_MODEL="deepseek-chat"
```

生成测试：

```bash
python scripts/generate_ai_tests.py
```

运行生成的测试：

```bash
pytest generated_tests --junitxml=reports/junit-ai.xml
```

如果没有配置 `DEEPSEEK_API_KEY`，生成步骤会自动跳过，不影响基础测试。

## GitHub Actions 配置

在 GitHub 仓库中添加 Secret：

```text
DEEPSEEK_API_KEY
```

流水线会在 `push` 和 `pull_request` 时自动执行：

1. 安装依赖。
2. 运行人工接口测试。
3. 导出 OpenAPI。
4. 调用 DeepSeek 生成临时接口测试。
5. 运行 AI 生成测试。
6. 上传测试报告和生成用例。
7. 测试失败时调用 DeepSeek 输出失败总结。

每次向 `main` 分支提交代码，GitHub Actions 都会自动触发这条流水线。

## 接口示例

```bash
curl -X POST http://127.0.0.1:8000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"left": 10, "right": 5, "operation": "divide"}'
```

返回：

```json
{"result":2.0}
```
