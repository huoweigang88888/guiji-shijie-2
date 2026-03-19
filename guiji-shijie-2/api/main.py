"""
硅基世界 2 API

FastAPI 主应用 - 整合硅基世界 1 所有功能
Phase 3: API 服务整合
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from pydantic import BaseModel
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# ========== 导入管理器 ==========
from core.database import init_db
from core.websocket_manager import WebSocketManager

# ========== 导入路由 ==========
from api.routes.agents import router as agents_router
from api.routes.social import router as social_router
from api.routes.websocket import router as websocket_router
from api.routes.files import router as files_router
from api.routes.a2a import router as a2a_router
from api.routes.gamification import router as gamification_router
from api.routes.performance import router as performance_router
from api.routes.collab_tasks import router as collab_tasks_router

# 新增路由
from api.routes.memory import router as memory_router
from api.routes.economy import router as economy_router
from api.routes.blockchain import router as blockchain_router

# ========== 生命周期管理 ==========
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动和关闭时的操作"""
    # 启动时：初始化数据库
    print("[INFO] Initializing database...")
    init_db()
    print("[INFO] Database initialized")
    
    # 初始化 WebSocket 管理器
    print("[INFO] Initializing WebSocket manager...")
    ws_manager = WebSocketManager()
    print("[INFO] WebSocket manager initialized")
    
    # 初始化 Agent 系统
    print("[INFO] Initializing Agent system...")
    try:
        from agents import init_agent_system
        init_agent_system()
        print("[INFO] Agent system initialized")
    except Exception as e:
        print(f"[WARN] Agent system init failed: {e}")
    
    yield
    
    # 关闭时：清理资源
    print("[INFO] Shutting down service...")

# ========== 创建 FastAPI 应用 ==========
app = FastAPI(
    title="硅基世界 2 API",
    description="Agent 与人类的虚拟世界 - RESTful API (Phase 3)",
    version="2.0.0-alpha",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# ========== 配置 CORS ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== 全局实例 ==========
ws_manager = WebSocketManager()

# ========== 健康检查端点 ==========
@app.get("/")
async def root():
    """根路径 - 健康检查"""
    return {
        "project": "硅基世界 2",
        "version": "2.0.0-alpha",
        "status": "Phase 3: API 服务整合",
        "phase": "进行中",
        "docs": "/docs",
        "github": "https://github.com/huoweigang88888/guiji-shijie-2"
    }

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "guiji-world-2-api",
        "version": "2.0.0-alpha"
    }

# ========== 注册路由 ==========

# Agent 管理 (6 个端点)
app.include_router(agents_router, prefix="/api/v1/agents", tags=["Agents"])

# 记忆管理 (5 个端点)
app.include_router(memory_router, prefix="/api/v1/memory", tags=["Memory"])

# 社交系统 (20 个端点)
app.include_router(social_router, prefix="/api/v1/social", tags=["Social"])

# 经济系统 (10 个端点)
app.include_router(economy_router, prefix="/api/v1/economy", tags=["Economy"])

# 游戏化 (8 个端点)
app.include_router(gamification_router, prefix="/api/v1/gamification", tags=["Gamification"])

# 区块链 (6 个端点)
app.include_router(blockchain_router, prefix="/api/v1/blockchain", tags=["Blockchain"])

# A2A 协议 (12 个端点)
app.include_router(a2a_router, prefix="/api/v1/a2a", tags=["A2A"])

# 文件上传
app.include_router(files_router, prefix="/api/v1/files", tags=["Files"])

# 协作任务
app.include_router(collab_tasks_router, prefix="/api/v1/tasks", tags=["Tasks"])

# 性能监控
app.include_router(performance_router, prefix="/api/v1/performance", tags=["Performance"])

# WebSocket
app.include_router(websocket_router, prefix="/api/v1/ws", tags=["WebSocket"])

# ========== 静态文件挂载 (Phase 4) ==========
# web_ui_static = Path(__file__).parent.parent / "web_ui" / "static"
# if web_ui_static.exists():
#     app.mount("/static", StaticFiles(directory=str(web_ui_static)), name="static")

# ========== API 统计 ==========
@app.get("/api/stats")
async def get_api_stats():
    """获取 API 统计信息"""
    routes = list(app.routes)
    api_routes = [r for r in routes if hasattr(r, 'path') and r.path.startswith('/api')]
    
    return {
        "total_routes": len(routes),
        "api_routes": len(api_routes),
        "tags": list(app.openapi_tags),
        "version": app.version
    }

# ========== 主入口 ==========
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
