#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
硅基世界 2 - Web 观察服务

一个简单的 HTTP 服务，让人类可以通过浏览器观察 Agent 们的生活。
"""

import asyncio
import json
import http.server
import socketserver
import threading
from datetime import datetime
from typing import Dict, Any, List, Optional

import sys
sys.path.insert(0, '..')

from world.map import get_world_map
from world.message_bus import get_message_bus
from world.activity_manager import get_activity_manager


# 全局状态
_world_map = get_world_map()
_message_bus = get_message_bus()
_activity_manager = get_activity_manager()

# 在线 Agent 状态
_online_agents: Dict[str, Dict] = {}


class WorldObserver:
    """世界观察器"""
    
    def __init__(self):
        self._running = False
        self._tasks: List[asyncio.Task] = []
    
    async def start(self):
        """启动观察器"""
        self._running = True
        
        # 创建观察任务
        self._tasks.append(asyncio.create_task(self._observe_loop()))
    
    async def stop(self):
        """停止观察器"""
        self._running = False
        for task in self._tasks:
            task.cancel()
        self._tasks.clear()
    
    async def _observe_loop(self):
        """观察循环"""
        while self._running:
            try:
                # 更新在线 Agent 状态
                self._update_agent_states()
                
                # 等待
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[WorldObserver] 错误：{e}")
    
    def _update_agent_states(self):
        """更新 Agent 状态"""
        # 这里可以从实际运行的 Agent 获取状态
        # 简化实现：返回示例状态
        pass
    
    def get_world_state(self) -> Dict:
        """获取世界状态"""
        return {
            "timestamp": datetime.now().isoformat(),
            "agents": [
                {
                    "agent_id": agent_id,
                    "name": agent_profile.name,
                    "role": agent_profile.role,
                    "status": "online",
                    "location": _world_map.get_agent_location(agent_id),
                    "emotions": {"mood": "calm"},
                }
                for agent_id, agent_profile in [
                    ("CEO-Agent", create_ceo_agent().profile),
                    ("PM-Agent", create_pm_agent().profile),
                    ("ARCH-Agent", create_arch_agent().profile),
                    ("DEV-Agent", create_dev_agent().profile),
                    ("QA-Agent", create_qa_agent().profile),
                ]
            ],
            "regions": [
                {
                    "id": region.region_id,
                    "name": region.name,
                    "count": len(region.current_agents),
                    "atmosphere": region.atmosphere,
                }
                for region in _world_map.get_all_regions()
            ],
            "messages": {
                "total": _message_bus.get_stats()["total_messages"],
                "history": [m.to_dict() for m in _message_bus.get_history(limit=10)],
            },
            "activities": {
                "stats": _activity_manager.get_stats(),
                "recurring": [
                    {
                        "name": a["name"],
                        "location": a["location"],
                        "frequency": a["frequency"].value,
                    }
                    for a in _activity_manager.recurring_activities
                ],
            },
        }


# 创建观察器
_world_observer = WorldObserver()


class WorldHandler(http.server.BaseHTTPRequestHandler):
    """Web 请求处理器"""
    
    def do_GET(self):
        """处理 GET 请求"""
        if self.path == "/":
            self.send_world_status()
        elif self.path == "/api/state":
            self.send_json(_world_observer.get_world_state())
        elif self.path == "/api/messages":
            self.send_json({
                "total": _message_bus.get_stats()["total_messages"],
                "history": [m.to_dict() for m in _message_bus.get_history(limit=20)],
            })
        elif self.path == "/api/agents":
            self.send_json({
                "agents": [
                    {
                        "agent_id": agent_id,
                        "name": agent_profile.name,
                        "role": agent_profile.role,
                        "catchphrases": agent_profile.catchphrases,
                    }
                    for agent_id, agent_profile in [
                        ("CEO-Agent", create_ceo_agent().profile),
                        ("PM-Agent", create_pm_agent().profile),
                        ("ARCH-Agent", create_arch_agent().profile),
                        ("DEV-Agent", create_dev_agent().profile),
                        ("QA-Agent", create_qa_agent().profile),
                    ]
                ]
            })
        elif self.path.startswith("/api/agent/"):
            agent_id = self.path.split("/")[-1]
            agent = {
                "CEO-Agent": create_ceo_agent(),
                "PM-Agent": create_pm_agent(),
                "ARCH-Agent": create_arch_agent(),
                "DEV-Agent": create_dev_agent(),
                "QA-Agent": create_qa_agent(),
            }.get(agent_id)
            
            if agent:
                self.send_json(agent.get_status())
            else:
                self.send_error(404, f"Agent {agent_id} not found")
        else:
            self.send_error(404)
    
    def do_POST(self):
        """处理 POST 请求"""
        if self.path == "/api/message":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            try:
                data = json.loads(body.decode('utf-8'))
                
                # 模拟发送消息
                asyncio.create_task(_message_bus.send(
                    sender_id=data.get("sender_id", "human"),
                    receiver_id=data.get("receiver_id", "all"),
                    message_type=data.get("message_type", "request"),
                    content=data.get("content", {}),
                ))
                
                self.send_json({"status": "ok"})
            except Exception as e:
                self.send_error(400, str(e))
        else:
            self.send_error(404)
    
    def send_json(self, data: Dict):
        """发送 JSON 响应"""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def send_world_status(self):
        """发送世界状态页面"""
        content = self._create_status_page()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))
    
    def _create_status_page(self) -> str:
        """创建状态页面"""
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>硅基世界 2 - 观察界面</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        .card {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }}
        .card h2 {{
            margin-top: 0;
            border-bottom: 1px solid rgba(255,255,255,0.2);
            padding-bottom: 10px;
        }}
        .agent {{
            background: rgba(255, 255, 255, 0.15);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
        }}
        .agent .name {{
            font-weight: bold;
            font-size: 1.2em;
        }}
        .agent .role {{
            color: #e0e0e0;
            font-size: 0.9em;
        }}
        .agent .catchphrase {{
            font-style: italic;
            color: #a0a0a0;
            margin-top: 5px;
        }}
        .region {{
            background: rgba(255, 255, 255, 0.15);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
        }}
        .region .count {{
            font-size: 1.5em;
            font-weight: bold;
            color: #ffd700;
        }}
        .status {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.9em;
            margin-right: 5px;
        }}
        .status.idle {{
            background: #4caf50;
        }}
        .status.working {{
            background: #2196f3;
        }}
        .status.thinking {{
            background: #ff9800;
        }}
        .atmosphere {{
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }}
        .atmosphere div {{
            background: rgba(0,0,0,0.3);
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.9em;
        }}
        .atmosphere .energy {{ color: #ff6b6b; }}
        .atmosphere .warmth {{ color: #feca57; }}
        .atmosphere .creativity {{ color: #48dbfb; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌍 硅基世界 2 - 观察界面</h1>
        <p style="text-align: center;">观察者模式 | 有温度的世界 | 多元而包容</p>
        
        <div class="grid">
            <div class="card">
                <h2>👥 Agent 列表</h2>
                {self._render_agents()}
            </div>
            
            <div class="card">
                <h2>🏛️ 世界地图</h2>
                {self._render_regions()}
            </div>
            
            <div class="card">
                <h2>📅 活动</h2>
                {self._render_activities()}
            </div>
        </div>
        
        <div class="card" style="margin-top: 20px;">
            <h2>💬 最近消息</h2>
            {self._render_messages()}
        </div>
    </div>
    
    <script>
        async function updateStatus() {{
            try {{
                const response = await fetch('/api/state');
                const state = await response.json();
                
                // 更新 Agent 状态
                const agentsDiv = document.querySelector('.card:nth-child(1)');
                if (state.agents) {{
                    agentsDiv.innerHTML = `
                        <h2>👥 Agent 列表</h2>
                        {self._render_agents()}
                    `;
                }}
                
                // 更新消息
                if (state.messages) {{
                    const messagesDiv = document.querySelector('.card:last-child');
                    if (messagesDiv) {{
                        messagesDiv.innerHTML = `
                            <h2>💬 最近消息</h2>
                            {self._render_messages()}
                        `;
                    }}
                }}
            }} catch (e) {{
                console.error('更新失败:', e);
            }}
        }}
        
        setInterval(updateStatus, 5000);
    </script>
</body>
</html>"""
    
    def _render_agents(self) -> str:
        """渲染 Agent 列表"""
        agents = [
            ("CEO-Agent", "董事事", "CEO", "我们的目标是什么？"),
            ("PM-Agent", "小问", "产品经理", "这个功能的用户价值是什么？"),
            ("ARCH-Agent", "阿哲", "架构师", "这个抽象合适吗？"),
            ("DEV-Agent", "小码", "高级开发工程师", "让我重构一下"),
            ("QA-Agent", "小测", "测试工程师", "这个场景测试了吗？"),
            ("UI-Agent", "小美", "UI 设计师", "这个视觉层次清晰吗？"),
            ("KNOW-Agent", "小知", "知识管理员", "这个知识应该归类到哪里？"),
            ("SOCIAL-Agent", "小交", "社交达人", "最近怎么样？"),
        ]
        
        html = ""
        for agent_id, name, role, catchphrase in agents:
            html += f"""
            <div class="agent">
                <div class="name">{name}</div>
                <div class="role">{role}</div>
                <div class="catchphrase">"{catchphrase}"</div>
            </div>"""
        
        return html
    
    def _render_regions(self) -> str:
        """渲染区域"""
        regions = _world_map.get_all_regions()
        
        html = ""
        for region in regions:
            html += f"""
            <div class="region">
                <div class="name">{region.name}</div>
                <div class="count">{len(region.current_agents)}人在场</div>
                <div class="atmosphere">
                    <div class="energy">⚡ 能量: {region.atmosphere['energy']:.0f}</div>
                    <div class="warmth">❤️ 温暖: {region.atmosphere['warmth']:.0f}</div>
                    <div class="creativity">✨ 创造力: {region.atmosphere['creativity']:.0f}</div>
                </div>
            </div>"""
        
        return html
    
    def _render_activities(self) -> str:
        """渲染活动"""
        stats = _activity_manager.get_stats()
        
        return f"""
        <div style="padding: 10px;">
            <p>今日活动：{stats['scheduled']} 个待开始，{stats['ongoing']} 个进行中</p>
            <p>周期性活动模板：{stats['recurring_templates']} 个</p>
            <ul>
                <li>每日站会 - 每天早上</li>
                <li>数据咖啡时间 - 每天下午</li>
                <li>知识分享会 - 每周一次</li>
                <li>庆功宴 - 自发举行</li>
                <li>技术分享 - 每两周一次</li>
                <li>冥想时间 - 每天晚上</li>
            </ul>
        </div>"""
    
    def _render_messages(self) -> str:
        """渲染消息"""
        history = _message_bus.get_history(limit=10)
        
        if not history:
            return "<p style='padding: 10px;'>暂无消息</p>"
        
        html = ""
        for msg in history:
            content = msg.content.get('subject', msg.content.get('title', '...'))
            html += f"""
            <div style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.1);">
                <span style="font-weight: bold;">{msg.sender_id}</span> → 
                <span>{msg.receiver_id}</span>
                <div style="font-size: 0.9em; margin-top: 3px;">[{msg.message_type}] {content[:40]}...</div>
            </div>"""
        
        return html


def run_server(port: int = 8080):
    """运行服务器"""
    with socketserver.TCPServer(("", port), WorldHandler) as httpd:
        print(f"🌐 硅基世界 2 Web 服务运行在: http://localhost:{port}")
        print("👁️  打开浏览器，观察 Agent 们的生活吧！")
        httpd.serve_forever()


if __name__ == "__main__":
    import threading
    
    # 在后台运行观察器
    async def background_observer():
        await _world_observer.start()
    
    # 启动服务器
    server_thread = threading.Thread(target=lambda: run_server(8080))
    server_thread.daemon = True
    server_thread.start()
    
    # 运行观察器
    try:
        asyncio.run(background_observer())
    except KeyboardInterrupt:
        print("\n👋 观察服务已停止")
