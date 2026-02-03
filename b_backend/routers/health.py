"""
健康检查路由
"""

from fastapi import APIRouter
from datetime import datetime
import platform
import sys

router = APIRouter()


@router.get("")
@router.get("/")
async def health_check():
    """健康检查端点"""
    return {
        "success": True,
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "TradingAgents API"
    }


@router.get("/status")
async def detailed_status():
    """详细状态信息"""
    return {
        "success": True,
        "data": {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "system": {
                "platform": platform.system(),
                "platform_version": platform.version(),
                "python_version": sys.version,
                "architecture": platform.machine()
            },
            "services": {
                "api": "running",
                "analysis_engine": "available"
            }
        }
    }


@router.get("/ping")
async def ping():
    """简单的ping端点"""
    return {"pong": True, "timestamp": datetime.utcnow().isoformat()}
