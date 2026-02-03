# TradingAgents Web Demo

一个基于 TradingAgents 框架的在线演示网站，让您可以通过 Web 界面体验多智能体 AI 股票分析。

## 项目结构

```
├── b_backend/          # 后端服务 (FastAPI)
│   ├── main.py         # 主应用入口
│   ├── config.py       # 配置文件
│   ├── routers/        # API 路由
│   │   ├── health.py   # 健康检查
│   │   └── analysis.py # 分析接口
│   └── requirements.txt
│
├── b_frontend/         # 前端服务 (Vue 3)
│   ├── src/
│   │   ├── views/      # 页面组件
│   │   ├── layouts/    # 布局组件
│   │   ├── router/     # 路由配置
│   │   ├── api/        # API 封装
│   │   └── styles/     # 样式文件
│   ├── package.json
│   └── vite.config.ts
│
└── tradingagents/      # TradingAgents 核心框架
```

## 快速开始

### 1. 启动后端服务

```bash
# 进入项目根目录
cd TradingAgents

# 创建虚拟环境（如果还没有）
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 安装后端依赖
pip install -r b_backend/requirements.txt

# 启动后端服务
python -m b_backend.main
```

后端服务将在 http://localhost:8000 启动

### 2. 启动前端服务

```bash
# 打开新的终端，进入前端目录
cd TradingAgents/b_frontend

# 安装依赖
npm install
# 或使用 yarn
yarn install

# 启动开发服务器
npm run dev
# 或
yarn dev
```

前端服务将在 http://localhost:3000 启动

### 3. 访问网站

打开浏览器访问 http://localhost:3000

## 功能特点

### 📊 股票分析
- 输入股票代码（如 NVDA、AAPL、TSLA）
- 选择分析深度（快速/标准/深度）
- 选择 AI 分析师团队组合
- 实时查看分析进度
- 获取详细的分析报告

### 🤖 AI 分析师团队
- **市场分析师**: 分析技术指标和价格走势
- **社媒分析师**: 分析社交媒体情绪
- **新闻分析师**: 分析新闻和行业动态
- **基本面分析师**: 分析公司财务状况

### 📋 任务管理
- 查看所有分析任务
- 按状态筛选任务
- 查看历史分析结果
- 删除不需要的任务

## 配置说明

### 后端配置

后端配置可以通过环境变量或 `.env` 文件设置：

```env
# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=true

# LLM 配置
LLM_PROVIDER=modelscope
DEEP_THINK_LLM=Qwen/Qwen2.5-72B-Instruct
QUICK_THINK_LLM=Qwen/Qwen3-235B-A22B-Instruct-2507
BACKEND_URL=https://api-inference.modelscope.cn/v1/

# API Keys (可选)
OPENAI_API_KEY=your_key
ALPHA_VANTAGE_API_KEY=your_key
```

### 前端配置

前端开发服务器配置在 `vite.config.ts` 中：

```typescript
server: {
  host: '0.0.0.0',
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

## API 文档

启动后端服务后，可以访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 技术栈

### 后端
- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic

### 前端
- Vue 3
- TypeScript
- Element Plus
- Vite
- Vue Router
- Pinia

### AI/LLM
- LangChain
- LangGraph
- OpenAI / Anthropic / ModelScope

## 注意事项

⚠️ **重要声明**

TradingAgents 框架仅供研究和学习目的。交易表现可能因多种因素而异，包括所选的底层语言模型、模型温度、交易周期、数据质量和其他非确定性因素。**本软件不构成财务、投资或交易建议。**

## 许可证

请参阅项目根目录的 LICENSE 文件。
