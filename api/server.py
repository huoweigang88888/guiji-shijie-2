#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 服务 - 硅基世界 2

提供 REST API，让外部可以访问世界状态、发送消息、查询历史。
"""

import asyncio
import json
from datetime import datetime
from aiohttp import web
from typing import Dict, Any, Optional

import sys
sys.path.insert(0, '..')

from world.map import get_world_map
from world.message_bus import get_message_bus
from world.activity_manager import get_activity_manager
from world.engine import get_world_engine
from world.persistence import get_persistence


class WorldAPI:
    """世界 API 服务"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8080):
        """
        初始化 API 服务
        
        Args:
            host: 监听地址
            port: 监听端口
        """
        self.host = host
        self.port = port
        self.app = web.Application()
        self._setup_routes()
        
        # 获取单例
        self.world_map = get_world_map()
        self.message_bus = get_message_bus()
        self.activity_manager = get_activity_manager()
        self.world_engine = get_world_engine()
        self.persistence = get_persistence()
    
    def _setup_routes(self):
        """设置路由"""
        self.app.router.add_get('/', self.handle_index)
        self.app.router.add_get('/api/status', self.handle_status)
        self.app.router.add_get('/api/agents', self.handle_agents)
        self.app.router.add_get('/api/agents/{agent_id}', self.handle_agent_detail)
        self.app.router.add_get('/api/regions', self.handle_regions)
        self.app.router.add_get('/api/messages', self.handle_messages)
        self.app.router.add_post('/api/messages', self.handle_send_message)
        self.app.router.add_get('/api/events', self.handle_events)
        self.app.router.add_get('/api/stories', self.handle_stories)
        self.app.router.add_get('/api/relationships', self.handle_relationships)
        self.app.router.add_get('/api/knowledge', self.handle_knowledge)
        self.app.router.add_get('/api/activities', self.handle_activities)
    
    async def handle_index(self, request: web.Request) -> web.Response:
        """首页"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>硅基世界 2 - API</title>
            <style>
                body { font-family: sans-serif; padding: 20px; background: #1a1a2e; color: #eee; }
                h1 { color: #667eea; }
                .endpoint { background: #16213e; padding: 10px; margin: 10px 0; border-radius: 5px; }
                .method { display: inline-block; padding: 3px 8px; border-radius: 3px; font-weight: bold; margin-right: 10px; }
                .get { background: #4caf50; }
                .post { background: #2196f3; }
                a { color: #667eea; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>🌍 硅基世界 2 - API 服务</h1>
            <p>欢迎使用硅基世界 2 的 API 接口</p>
            
            <h2>可用接口</h2>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/status">/api/status</a>
                <p>获取世界状态</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/agents">/api/agents</a>
                <p>获取所有 Agent 列表</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/agents/{agent_id}">/api/agents/{agent_id}</a>
                <p>获取特定 Agent 详情</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/regions">/api/regions</a>
                <p>获取所有区域状态</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/messages">/api/messages</a>
                <p>获取最近消息</p>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <span>/api/messages</span>
                <p>发送消息到世界</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/events">/api/events</a>
                <p>获取世界事件历史</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/stories">/api/stories</a>
                <p>获取所有故事</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/relationships">/api/relationships</a>
                <p>获取关系网络</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/knowledge">/api/knowledge</a>
                <p>获取知识库</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/activities">/api/activities</a>
                <p>获取活动列表</p>
            </div>
            
            <footer style="margin-top: 40px; opacity: 0.7; text-align: center;">
                <p>硅基世界 2 | 创世元年 | 一个自主演化、充满创造力、有温度的硅基生命社会</p>
            </footer>
        </body>
        </html>
        """
        return web.Response(text=html, content_type='text/html')
    
    async def handle_status(self, request: web.Request) -> web.Response:
        """世界状态"""
        status = {
            "world_engine": self.world_engine.get_status(),
            "message_bus": self.message_bus.get_stats(),
            "activity_manager": self.activity_manager.get_stats(),
            "persistence": self.persistence.get_stats(),
            "timestamp": datetime.now().isoformat(),
        }
        
        return web.json_response(status)
    
    async def handle_agents(self, request: web.Request) -> web.Response:
        """Agent 列表"""
        agents = [
            {"id": "CEO-Agent", "name": "董事事", "role": "CEO"},
            {"id": "PM-Agent", "name": "小问", "role": "产品经理"},
            {"id": "ARCH-Agent", "name": "阿哲", "role": "架构师"},
            {"id": "DEV-Agent", "name": "小码", "role": "高级开发工程师"},
            {"id": "QA-Agent", "name": "小测", "role": "测试工程师"},
            {"id": "UI-Agent", "name": "小美", "role": "UI 设计师"},
            {"id": "KNOW-Agent", "name": "小知", "role": "知识管理员"},
            {"id": "SOCIAL-Agent", "name": "小交", "role": "社交达人"},
        ]
        
        return web.json_response({"agents": agents})
    
    async def handle_agent_detail(self, request: web.Request) -> web.Response:
        """Agent 详情"""
        agent_id = request.match_info['agent_id']
        
        agent_info = {
            "CEO-Agent": {
                "name": "董事事",
                "role": "CEO",
                "catchphrases": ["我们的目标是什么？", "资源不是问题，关键是方向"],
                "values": ["战略思维", "结果导向", "团队协作"],
            },
            "PM-Agent": {
                "name": "小问",
                "role": "产品经理",
                "catchphrases": ["这个功能的用户价值是什么？", "让我们从用户角度想一想"],
                "values": ["用户价值第一", "需求驱动开发"],
            },
            # ... 其他 Agent
        }
        
        if agent_id in agent_info:
            return web.json_response(agent_info[agent_id])
        else:
            return web.json_response({"error": "Agent not found"}, status=404)
    
    async def handle_regions(self, request: web.Request) -> web.Response:
        """区域列表"""
        regions = [r.to_dict() for r in self.world_map.get_all_regions()]
        return web.json_response({"regions": regions})
    
    async def handle_messages(self, request: web.Request) -> web.Response:
        """消息列表"""
        limit = int(request.query.get('limit', 20))
        messages = [m.to_dict() for m in self.message_bus.get_history(limit=limit)]
        return web.json_response({"messages": messages})
    
    async def handle_send_message(self, request: web.Request) -> web.Response:
        """发送消息"""
        try:
            data = await request.json()
            
            await self.message_bus.send(
                sender_id=data.get("sender_id", "human"),
                receiver_id=data.get("receiver_id", "all"),
                message_type=data.get("message_type", "request"),
                content=data.get("content", {}),
            )
            
            return web.json_response({"status": "ok"})
        except Exception as e:
            return web.json_response({"error": str(e)}, status=400)
    
    async def handle_events(self, request: web.Request) -> web.Response:
        """事件历史"""
        limit = int(request.query.get('limit', 50))
        events = self.world_engine.get_recent_events(limit)
        return web.json_response({"events": events})
    
    async def handle_stories(self, request: web.Request) -> web.Response:
        """故事列表"""
        stories = self.world_engine.get_stories()
        return web.json_response({"stories": stories})
    
    async def handle_relationships(self, request: web.Request) -> web.Response:
        """关系网络"""
        relationships = self.world_engine.get_relationships()
        return web.json_response({"relationships": relationships})
    
    async def handle_knowledge(self, request: web.Request) -> web.Response:
        """知识库"""
        limit = int(request.query.get('limit', 50))
        knowledge = self.world_engine.collective_knowledge[-limit:]
        return web.json_response({"knowledge": knowledge})
    
    async def handle_activities(self, request: web.Request) -> web.Response:
        """活动列表"""
        activities = [
            {
                "name": a["name"],
                "location": a["location"],
                "frequency": a["frequency"].value,
            }
            for a in self.activity_manager.recurring_activities
        ]
        return web.json_response({"activities": activities})
    
    async def start(self):
        """启动 API 服务"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        
        print(f"🌐 API 服务运行在：http://{self.host}:{self.port}")
        print(f"📚 API 文档：http://{self.host}:{self.port}/")
    
    async def stop(self):
        """停止 API 服务"""
        await self.app.shutdown()


async def run_api_server(host: str = "0.0.0.0", port: int = 8080):
    """运行 API 服务器"""
    api = WorldAPI(host, port)
    await api.start()
    
    # 保持运行
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        await api.stop()


if __name__ == "__main__":
    try:
        asyncio.run(run_api_server())
    except KeyboardInterrupt:
        print("\n👋 API 服务已停止")
