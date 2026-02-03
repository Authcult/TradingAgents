# TradingAgents Frontend

TradingAgents 多智能体股票分析平台前端

## 技术栈

- Vue 3
- TypeScript
- Element Plus
- Vite
- Vue Router

## 安装

```bash
npm install
# 或
yarn install
```

## 开发

```bash
npm run dev
# 或
yarn dev
```

## 构建

```bash
npm run build
# 或
yarn build
```

## 目录结构

```
src/
├── api/           # API 请求封装
├── layouts/       # 布局组件
├── router/        # 路由配置
├── styles/        # 全局样式
└── views/         # 页面组件
    ├── Dashboard.vue   # 仪表板
    ├── Analysis.vue    # 股票分析
    ├── Tasks.vue       # 任务列表
    └── About.vue       # 关于页面
```

## 配置

开发服务器配置在 `vite.config.ts` 中，默认代理 `/api` 到后端服务 `http://localhost:8000`。

执行后端：
cd TradingAgents
pip install -r b_backend/requirements.txt
python -m b_backend.main
再执行前端：
cd TradingAgents/b_frontend
npm install
npm run dev
