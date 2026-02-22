# GitHub Trending Daily Summary

每日自动抓取 GitHub 热门项目，通过 LLM 生成中英文摘要，并通过 Resend 发送到指定邮箱。

## 工作流程

```
GitHub Search API → 获取热门仓库 → LLM 生成摘要 → Resend 发送邮件
```

## 项目结构

```
├── config.py             # 加载 .env 配置
├── github_trending.py    # 通过 GitHub Search API 获取热门仓库
├── summarizer.py         # 调用 LLM 生成 HTML 摘要
├── emailer.py            # 通过 Resend 发送邮件
├── main.py               # 入口文件
├── requirements.txt      # Python 依赖
└── .env.example          # 配置模板
```

## 配置说明

| 变量 | 必填 | 说明 |
|---|---|---|
| `GITHUB_TOKEN` | 否 | GitHub Personal Access Token，可提高 API 速率限制 |
| `LLM_BASE_URL` | 是 | OpenAI 兼容的 API 地址 |
| `LLM_API_KEY` | 是 | LLM API Key |
| `LLM_MODEL` | 否 | 模型名称 |
| `RESEND_API_KEY` | 是 | Resend API Key |
| `EMAIL_FROM` | 是 | 发件人地址（需在 Resend 中验证域名） |
| `EMAIL_TO` | 是 | 收件人邮箱 |
| `TRENDING_DAYS` | 否 | 搜索最近 N 天创建的仓库，默认 `7` |
| `TRENDING_COUNT` | 否 | 获取仓库数量，默认 `15` |

LLM 支持任何 OpenAI 格式的 API，包括 OpenAI、SiliconFlow、DeepSeek、Groq、本地 Ollama 等。

## 本地运行

```bash
# 1. 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 填入实际的 API Key 等配置

# 4. 运行
python main.py
```

## 部署到 Ubuntu 服务器

### 1. 克隆项目
```
git clone https://github.com/iqiang111/Tredings.git /opt/tredings
```

### 2. 初始化环境

```bash
cd /opt/tredings
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. 配置

```bash
cp .env.example .env
nano .env   # 填入实际配置
```

### 4. 测试运行

```bash
cd /opt/tredings && .venv/bin/python main.py
```

### 5. 配置定时任务（每 3 天执行一次）

```bash
crontab -e
```

添加以下内容：

```cron
0 8 */3 * * cd /opt/tredings && .venv/bin/python main.py >> /opt/tredings/cron.log 2>&1
```

每 3 天早上 8:00 自动执行，日志写入 `cron.log`。

管理定时任务：

```bash
crontab -l                            # 查看当前定时任务
tail -f /opt/tredings/cron.log        # 查看运行日志
```
