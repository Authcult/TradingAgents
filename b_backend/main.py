"""
TradingAgents FastAPI Backend
主应用程序入口
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from datetime import datetime
from contextlib import asynccontextmanager

from b_backend.config import settings

# 设置日志
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("tradingagents-api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("=" * 60)
    logger.info("🚀 TradingAgents API 启动中...")
    logger.info(f"📋 版本: {settings.APP_VERSION}")
    logger.info(f"🔧 调试模式: {settings.DEBUG}")
    logger.info(f"🌐 服务地址: http://{settings.HOST}:{settings.PORT}")
    logger.info("=" * 60)
    
    yield
    
    logger.info("🛑 TradingAgents API 关闭中...")


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="TradingAgents Multi-Agent Trading Framework API",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"❌ 全局异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# 导入路由
from b_backend.routers import analysis, health

# 注册路由
app.include_router(health.router, prefix="/api/health", tags=["健康检查"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["股票分析"])


# 根路由
@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "docs": "/docs"
    }


@app.get("/api")
async def api_root():
    return {
        "message": "Welcome to TradingAgents API",
        "version": settings.APP_VERSION,
        "endpoints": {
            "health": "/api/health",
            "analysis": "/api/analysis",
            "docs": "/docs"
        }
    }


def main():
    """启动服务器"""
    uvicorn.run(
        "b_backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info"
    )


if __name__ == "__main__":
    main()
