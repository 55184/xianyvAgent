# 🐟 xianyvAgent - 闲鱼AI智能客服

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

闲鱼平台 AI 自动回复机器人，基于大模型实现多专家协同决策、智能砍价和上下文感知对话。

## 功能

- **智能路由** — 自动识别砍价/技术/售后等意图，分发到对应专家Agent
- **阶梯砍价** — 多轮议价策略，先问价→梯度让步→底线拒绝
- **上下文记忆** — SQLite 持久化对话历史，跨会话保持连贯
- **人工接管** — 输入关键词切换人工模式，灵活干预
- **安全过滤** — 自动屏蔽微信/QQ/线下交易等敏感引导

## 快速开始

```bash
# 1. 克隆
git clone https://github.com/55184/xianyvAgent.git
cd xianyvAgent

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置
cp .env.example .env
# 编辑 .env，填入 API_KEY 和 COOKIES_STR

# 4. 运行
python main.py
```

## 配置说明

`.env` 文件关键配置：

| 变量 | 说明 | 示例 |
|------|------|------|
| `API_KEY` | LLM API Key | sk-xxx |
| `COOKIES_STR` | 闲鱼网页Cookie | 从浏览器F12获取 |
| `MODEL_BASE_URL` | 模型接口地址 | 见下方推荐 |
| `MODEL_NAME` | 模型名称 | qwen-max |
| `PROXY_ENABLED` | 是否启用代理 | true/false |

### 免费API推荐

| 平台 | 额度 | 地址 |
|------|------|------|
| 硅基流动 | 2000万tokens | cloud.siliconflow.cn |
| DeepSeek | 500万tokens | platform.deepseek.com |
| 阿里百炼 | 免费额度 | bailian.console.aliyun.com |

## 自定义提示词

编辑 `prompts/` 目录下的 `_example.txt` 文件，复制去掉 `_example` 后缀即可生效：

- `classify_prompt.txt` — 意图分类
- `price_prompt.txt` — 砍价策略
- `tech_prompt.txt` — 技术咨询
- `default_prompt.txt` — 默认回复

## 项目结构

```
├── main.py              # WebSocket监听 + 消息路由
├── XianyuAgent.py       # LLM多专家决策引擎
├── XianyuApis.py        # 闲鱼API封装
├── context_manager.py   # SQLite对话上下文管理
├── prompts/             # 提示词模板
├── utils/               # 工具函数
├── .env.example         # 配置模板
└── requirements.txt     # Python依赖
```

## 安全提醒

- `.env` 文件包含密钥，已通过 `.gitignore` 排除，切勿提交
- `prompts/*_prompt.txt` 自定义策略文件同样不会提交
- 运行产生的 `data/` 目录（含聊天记录）不会提交

## 鸣谢

基于 [XianyuAutoAgent](https://github.com/shaxiu/XianyuAutoAgent) 优化改造。
