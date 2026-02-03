"""
股票分析路由
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import logging
import uuid
import asyncio

router = APIRouter()
logger = logging.getLogger("tradingagents-api")

# 内存存储分析任务（生产环境应使用数据库）
analysis_tasks: Dict[str, Dict[str, Any]] = {}


# 请求模型
class AnalysisRequest(BaseModel):
    """分析请求模型"""
    symbol: str = Field(..., description="股票代码，如 NVDA, AAPL")
    analysis_date: Optional[str] = Field(
        default=None, 
        description="分析日期，格式 YYYY-MM-DD"
    )
    research_depth: int = Field(
        default=1, 
        ge=1, 
        le=3, 
        description="研究深度：1=快速, 2=标准, 3=深度"
    )
    selected_analysts: List[str] = Field(
        default=["market", "news", "fundamentals"],
        description="选择的分析师团队"
    )


class BatchAnalysisRequest(BaseModel):
    """批量分析请求"""
    symbols: List[str] = Field(..., description="股票代码列表")
    analysis_date: Optional[str] = None
    research_depth: int = Field(default=1, ge=1, le=3)
    selected_analysts: List[str] = Field(
        default=["market", "news", "fundamentals"]
    )


# 响应模型
class AnalysisResponse(BaseModel):
    """分析响应模型"""
    success: bool
    task_id: str
    message: str


class TaskStatusResponse(BaseModel):
    """任务状态响应"""
    task_id: str
    status: str  # pending, running, completed, failed
    progress: int
    message: str
    result: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: str


# 分析师信息
ANALYSTS_INFO = {
    "market": {
        "name": "市场分析师",
        "icon": "📈",
        "description": "分析股票价格走势、技术指标"
    },
    "social": {
        "name": "社媒分析师",
        "icon": "📱",
        "description": "分析社交媒体情绪和舆论"
    },
    "news": {
        "name": "新闻分析师",
        "icon": "📰",
        "description": "分析相关新闻和行业动态"
    },
    "fundamentals": {
        "name": "基本面分析师",
        "icon": "📊",
        "description": "分析公司财务状况和基本面"
    }
}


async def run_analysis_task(task_id: str, request: AnalysisRequest):
    """执行分析任务（异步后台任务）"""
    try:
        logger.info(f"🚀 开始分析任务: {task_id}, 股票: {request.symbol}")
        
        # 更新任务状态
        analysis_tasks[task_id]["status"] = "running"
        analysis_tasks[task_id]["progress"] = 10
        analysis_tasks[task_id]["message"] = "正在初始化分析引擎..."
        analysis_tasks[task_id]["updated_at"] = datetime.utcnow().isoformat()
        
        await asyncio.sleep(1)  # 模拟处理时间
        
        # 尝试导入并使用 TradingAgents
        try:
            from tradingagents.graph.trading_graph import TradingAgentsGraph
            from tradingagents.default_config import DEFAULT_CONFIG
            
            # 更新进度
            analysis_tasks[task_id]["progress"] = 20
            analysis_tasks[task_id]["message"] = "正在配置分析参数..."
            analysis_tasks[task_id]["updated_at"] = datetime.utcnow().isoformat()
            
            await asyncio.sleep(0.5)
            
            # 创建配置
            config = DEFAULT_CONFIG.copy()
            config["max_debate_rounds"] = request.research_depth
            
            # 更新进度
            analysis_tasks[task_id]["progress"] = 30
            analysis_tasks[task_id]["message"] = "正在初始化AI智能体..."
            analysis_tasks[task_id]["updated_at"] = datetime.utcnow().isoformat()
            
            await asyncio.sleep(0.5)
            
            # 初始化图
            ta = TradingAgentsGraph(
                selected_analysts=request.selected_analysts,
                debug=True,
                config=config
            )
            
            # 更新进度
            analysis_tasks[task_id]["progress"] = 50
            analysis_tasks[task_id]["message"] = "AI分析师团队正在分析中..."
            analysis_tasks[task_id]["updated_at"] = datetime.utcnow().isoformat()
            
            # 确定分析日期
            analysis_date = request.analysis_date or date.today().strftime("%Y-%m-%d")
            
            # 执行分析（这是同步操作，在真实场景中应该使用线程池）
            loop = asyncio.get_event_loop()
            _, decision = await loop.run_in_executor(
                None, 
                lambda: ta.propagate(request.symbol, analysis_date)
            )
            
            # 更新进度
            analysis_tasks[task_id]["progress"] = 90
            analysis_tasks[task_id]["message"] = "正在生成分析报告..."
            analysis_tasks[task_id]["updated_at"] = datetime.utcnow().isoformat()
            
            await asyncio.sleep(0.5)
            
            # 完成分析
            analysis_tasks[task_id]["status"] = "completed"
            analysis_tasks[task_id]["progress"] = 100
            analysis_tasks[task_id]["message"] = "分析完成"
            analysis_tasks[task_id]["result"] = {
                "symbol": request.symbol,
                "analysis_date": analysis_date,
                "decision": decision,
                "analysts_used": request.selected_analysts,
                "research_depth": request.research_depth
            }
            analysis_tasks[task_id]["updated_at"] = datetime.utcnow().isoformat()
            
            logger.info(f"✅ 分析任务完成: {task_id}")
            
        except ImportError as e:
            logger.warning(f"⚠️ TradingAgents 导入失败，使用模拟数据: {e}")
            
            # 模拟分析过程
            steps = [
                (20, "正在获取股票数据..."),
                (40, "市场分析师正在分析技术指标..."),
                (60, "新闻分析师正在分析相关新闻..."),
                (80, "基本面分析师正在分析财务数据..."),
                (90, "研究团队正在讨论和辩论..."),
                (95, "正在生成最终决策...")
            ]
            
            for progress, message in steps:
                analysis_tasks[task_id]["progress"] = progress
                analysis_tasks[task_id]["message"] = message
                analysis_tasks[task_id]["updated_at"] = datetime.utcnow().isoformat()
                await asyncio.sleep(1.5)
            
            # 生成模拟结果
            analysis_date = request.analysis_date or date.today().strftime("%Y-%m-%d")
            analysis_tasks[task_id]["status"] = "completed"
            analysis_tasks[task_id]["progress"] = 100
            analysis_tasks[task_id]["message"] = "分析完成"
            analysis_tasks[task_id]["result"] = {
                "symbol": request.symbol,
                "analysis_date": analysis_date,
                "decision": {
                    "action": "HOLD",
                    "confidence": 0.75,
                    "summary": f"基于对 {request.symbol} 的综合分析，AI 分析师团队建议持有观望。技术指标显示股价处于盘整阶段，基本面稳健，建议密切关注市场动态后再做决策。",
                    "technical_analysis": "技术指标显示RSI处于中性区间，MACD呈现弱多头信号，短期均线与长期均线接近交叉。",
                    "fundamental_analysis": "公司财务状况良好，营收增长稳定，但估值相对较高。",
                    "news_sentiment": "近期新闻情绪偏中性，没有重大利好或利空消息。",
                    "risk_assessment": "当前市场波动性较高，建议控制仓位，设置止损位。"
                },
                "analysts_used": request.selected_analysts,
                "research_depth": request.research_depth,
                "is_simulated": True
            }
            analysis_tasks[task_id]["updated_at"] = datetime.utcnow().isoformat()
            
            logger.info(f"✅ 分析任务完成（模拟）: {task_id}")
            
    except Exception as e:
        logger.error(f"❌ 分析任务失败: {task_id}, 错误: {e}", exc_info=True)
        analysis_tasks[task_id]["status"] = "failed"
        analysis_tasks[task_id]["message"] = f"分析失败: {str(e)}"
        analysis_tasks[task_id]["updated_at"] = datetime.utcnow().isoformat()


@router.post("/single", response_model=Dict[str, Any])
async def submit_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks
):
    """提交单股分析任务"""
    try:
        logger.info(f"📊 收到分析请求: {request.symbol}")
        
        # 创建任务ID
        task_id = str(uuid.uuid4())
        
        # 初始化任务记录
        analysis_tasks[task_id] = {
            "task_id": task_id,
            "status": "pending",
            "progress": 0,
            "message": "任务已创建，等待处理...",
            "request": request.model_dump(),
            "result": None,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        # 添加后台任务
        background_tasks.add_task(run_analysis_task, task_id, request)
        
        return {
            "success": True,
            "data": {
                "task_id": task_id,
                "status": "pending",
                "message": "分析任务已提交"
            }
        }
        
    except Exception as e:
        logger.error(f"❌ 提交分析任务失败: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tasks/{task_id}/status")
async def get_task_status(task_id: str):
    """获取任务状态"""
    if task_id not in analysis_tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task = analysis_tasks[task_id]
    return {
        "success": True,
        "data": {
            "task_id": task["task_id"],
            "status": task["status"],
            "progress": task["progress"],
            "message": task["message"],
            "created_at": task["created_at"],
            "updated_at": task["updated_at"]
        }
    }


@router.get("/tasks/{task_id}/result")
async def get_task_result(task_id: str):
    """获取任务结果"""
    if task_id not in analysis_tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task = analysis_tasks[task_id]
    
    if task["status"] != "completed":
        return {
            "success": False,
            "message": f"任务尚未完成，当前状态: {task['status']}",
            "data": {
                "task_id": task["task_id"],
                "status": task["status"],
                "progress": task["progress"]
            }
        }
    
    return {
        "success": True,
        "data": task["result"]
    }


@router.get("/tasks")
async def list_tasks(
    status: Optional[str] = None,
    limit: int = 20
):
    """获取任务列表"""
    tasks = list(analysis_tasks.values())
    
    # 按状态筛选
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    
    # 按创建时间排序（最新的在前）
    tasks.sort(key=lambda x: x["created_at"], reverse=True)
    
    # 限制数量
    tasks = tasks[:limit]
    
    return {
        "success": True,
        "data": {
            "tasks": tasks,
            "total": len(tasks)
        }
    }


@router.get("/analysts")
async def get_analysts():
    """获取可用的分析师列表"""
    return {
        "success": True,
        "data": ANALYSTS_INFO
    }


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """删除任务"""
    if task_id not in analysis_tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    del analysis_tasks[task_id]
    
    return {
        "success": True,
        "message": "任务已删除"
    }
