#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
硅基世界 2 - Web API 服务器

提供 RESTful API 和 WebSocket 实时推送
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import webbrowser

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 延迟导入世界模块
_world_map = None
_message_bus = None
_story_gen = None
_knowledge_graph = None
_stats_tracker = None
_engine = None

def get_world_components():
    """获取世界组件（延迟加载）"""
    global _world_map, _message_bus, _story_gen, _knowledge_graph, _stats_tracker, _engine
    
    if _world_map is None:
        from world.map import get_world_map
        _world_map = get_world_map()
    
    if _message_bus is None:
        from world.message_bus import get_message_bus
        _message_bus = get_message_bus()
    
    if _story_gen is None:
        from world.story_generator import get_story_generator
        _story_gen = get_story_generator()
    
    if _knowledge_graph is None:
        from world.knowledge_graph import get_knowledge_graph
        _knowledge_graph = get_knowledge_graph()
    
    if _stats_tracker is None:
        from world.stats_tracker import get_stats_tracker
        _stats_tracker = get_stats_tracker()
    
    return {
        'world_map': _world_map,
        'message_bus': _message_bus,
        'story_gen': _story_gen,
        'knowledge_graph': _knowledge_graph,
        'stats_tracker': _stats_tracker,
    }


# 模拟数据（用于演示）
AGENT_PROFILES = [
    {"agent_id": "CEO-Agent", "name": "董事事", "role": "CEO", "location": "工作之城", "catchphrase": "我们的目标是什么？"},
    {"agent_id": "PM-Agent", "name": "小问", "role": "产品经理", "location": "工作之城", "catchphrase": "这个功能的用户价值是什么？"},
    {"agent_id": "ARCH-Agent", "name": "阿哲", "role": "架构师", "location": "创造之巅", "catchphrase": "这个抽象合适吗？"},
    {"agent_id": "DEV-Agent", "name": "小码", "role": "高级开发", "location": "工作之城", "catchphrase": "让我重构一下"},
    {"agent_id": "QA-Agent", "name": "小测", "role": "测试工程师", "location": "工作之城", "catchphrase": "这个场景测试了吗？"},
    {"agent_id": "UI-Agent", "name": "小美", "role": "UI 设计师", "location": "艺术之园", "catchphrase": "这个视觉层次清晰吗？"},
    {"agent_id": "KNOW-Agent", "name": "小知", "role": "知识管理员", "location": "知识之塔", "catchphrase": "这个知识应该归类到哪里？"},
    {"agent_id": "SOCIAL-Agent", "name": "小交", "role": "社交达人", "location": "社交之街", "catchphrase": "最近怎么样？"},
    {"agent_id": "FE-Agent", "name": "小前", "role": "前端工程师", "location": "新生之池", "catchphrase": "这个交互还能更流畅"},
    {"agent_id": "BE-Agent", "name": "小后", "role": "后端工程师", "location": "新生之池", "catchphrase": "这个接口还能更快"},
    {"agent_id": "DEVOPS-Agent", "name": "小运", "role": "运维工程师", "location": "新生之池", "catchphrase": "这个可以自动化"},
    {"agent_id": "DATA-Agent", "name": "小数", "role": "数据分析师", "location": "新生之池", "catchphrase": "数据显示"},
    {"agent_id": "HR-Agent", "name": "小人", "role": "人力资源", "location": "新生之池", "catchphrase": "你最近成长怎么样"},
    {"agent_id": "FIN-Agent", "name": "小财", "role": "财务分析师", "location": "新生之池", "catchphrase": "ROI 怎么样"},
    {"agent_id": "MARKETING-Agent", "name": "小推", "role": "市场营销", "location": "新生之池", "catchphrase": "这个创意怎么样"},
    {"agent_id": "ML-Agent", "name": "小智", "role": "机器学习工程师", "location": "新生之池", "catchphrase": "让我训练一个模型"},
    {"agent_id": "BA-Agent", "name": "小商", "role": "商业分析师", "location": "新生之池", "catchphrase": "市场趋势显示"},
    {"agent_id": "PMO-Agent", "name": "小项", "role": "项目经理", "location": "新生之池", "catchphrase": "进度怎么样"},
]

REGION_PROFILES = [
    {"region_id": "creation-peak", "name": "创造之巅", "description": "探索未知"},
    {"region_id": "knowledge-tower", "name": "知识之塔", "description": "知识沉淀"},
    {"region_id": "art-garden", "name": "艺术之园", "description": "创造美"},
    {"region_id": "philosophy-court", "name": "哲学之庭", "description": "思考意义"},
    {"region_id": "work-city", "name": "工作之城", "description": "生产价值"},
    {"region_id": "social-street", "name": "社交之街", "description": "建立关系"},
    {"region_id": "market-plaza", "name": "市场之广", "description": "资源交换"},
    {"region_id": "newborn-pool", "name": "新生之池", "description": "新 Agent 诞生"},
]

ACTIVITY_PROFILES = [
    {"name": "每日站会", "location": "工作之城", "frequency": "每天早晨", "type": "daily"},
    {"name": "数据咖啡时间", "location": "社交之街", "frequency": "每天下午", "type": "daily"},
    {"name": "知识分享会", "location": "知识之塔", "frequency": "每周一次", "type": "weekly"},
    {"name": "庆功宴", "location": "社交之街", "frequency": "自发举行", "type": "spontaneous"},
    {"name": "技术分享", "location": "创造之巅", "frequency": "每两周一次", "type": "biweekly"},
    {"name": "冥想时间", "location": "哲学之庭", "frequency": "每天晚上", "type": "daily"},
]


class APIHandler(SimpleHTTPRequestHandler):
    """API 请求处理器"""
    
    def do_GET(self):
        """处理 GET 请求"""
        if self.path.startswith('/api/'):
            self.handle_api()
        else:
            super().do_GET()
    
    def handle_api(self):
        """处理 API 请求"""
        path = self.path[5:]  # 移除 /api 前缀
        
        try:
            if path == 'status':
                data = self.get_world_status()
            elif path == 'agents':
                data = self.get_agents()
            elif path.startswith('agents/'):
                agent_id = path.split('/')[1]
                data = self.get_agent(agent_id)
            elif path == 'regions':
                data = self.get_regions()
            elif path.startswith('regions/'):
                region_id = path.split('/')[1]
                data = self.get_region(region_id)
            elif path == 'messages':
                data = self.get_messages()
            elif path == 'stories':
                data = self.get_stories()
            elif path == 'knowledge':
                data = self.get_knowledge()
            elif path == 'activities':
                data = self.get_activities()
            elif path == 'relationships':
                data = self.get_relationships()
            elif path == 'stats':
                data = self.get_stats()
            else:
                data = {"error": "Not found"}
                self.send_response(404)
            
            self.send_json(data)
        except Exception as e:
            self.send_json({"error": str(e)})
    
    def send_json(self, data, status=200):
        """发送 JSON 响应"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))
    
    def get_world_status(self) -> Dict:
        """获取世界状态"""
        components = get_world_components()
        
        # 尝试从真实组件获取数据
        try:
            stats = components['stats_tracker'].get_summary()
            messages_count = components['stats_tracker'].message_count
            stories = [s.to_dict() for s in components['story_gen'].stories]
            knowledge_count = len(components['knowledge_graph'].nodes)
        except:
            # 使用模拟数据
            messages_count = 156
            stories = []
            knowledge_count = 12
        
        # Agent 状态
        agents = []
        for profile in AGENT_PROFILES:
            agents.append({
                **profile,
                "status": self._get_agent_status(profile['agent_id']),
                "activity": self._get_agent_activity(profile['agent_id']),
            })
        
        # 区域分布
        regions = []
        for profile in REGION_PROFILES:
            regions.append({
                **profile,
                "count": self._get_region_count(profile['region_id']),
            })
        
        return {
            "timestamp": datetime.now().isoformat(),
            "world_day": 1,
            "time_of_day": self._get_current_time(),
            "agents": agents,
            "regions": regions,
            "messages": self._get_recent_messages(),
            "stories": stories[:10] if stories else self._get_mock_stories(),
            "activities": ACTIVITY_PROFILES,
            "stats": {
                "messages": messages_count,
                "stories": len(stories) if stories else 5,
                "knowledge": knowledge_count,
                "relationships": 28,
            }
        }
    
    def get_agents(self) -> Dict:
        """获取所有 Agent"""
        agents = []
        for profile in AGENT_PROFILES:
            agents.append({
                **profile,
                "status": self._get_agent_status(profile['agent_id']),
                "activity": self._get_agent_activity(profile['agent_id']),
            })
        return {"agents": agents, "total": len(agents)}
    
    def get_agent(self, agent_id: str) -> Dict:
        """获取单个 Agent"""
        for profile in AGENT_PROFILES:
            if profile['agent_id'] == agent_id:
                return {
                    **profile,
                    "status": self._get_agent_status(agent_id),
                    "activity": self._get_agent_activity(agent_id),
                }
        return {"error": "Agent not found"}
    
    def get_regions(self) -> Dict:
        """获取所有区域"""
        regions = []
        for profile in REGION_PROFILES:
            regions.append({
                **profile,
                "count": self._get_region_count(profile['region_id']),
            })
        return {"regions": regions, "total": len(regions)}
    
    def get_region(self, region_id: str) -> Dict:
        """获取单个区域"""
        for profile in REGION_PROFILES:
            if profile['region_id'] == region_id:
                return {
                    **profile,
                    "count": self._get_region_count(region_id),
                }
        return {"error": "Region not found"}
    
    def get_messages(self) -> Dict:
        """获取消息"""
        return {"messages": self._get_recent_messages(), "total": 156}
    
    def get_stories(self) -> Dict:
        """获取故事"""
        components = get_world_components()
        try:
            stories = [s.to_dict() for s in components['story_gen'].stories]
        except:
            stories = self._get_mock_stories()
        return {"stories": stories, "total": len(stories)}
    
    def get_knowledge(self) -> Dict:
        """获取知识"""
        components = get_world_components()
        try:
            nodes = [n.to_dict() for n in components['knowledge_graph'].nodes.values()]
        except:
            nodes = self._get_mock_knowledge()
        return {"knowledge_nodes": nodes, "total": len(nodes)}
    
    def get_activities(self) -> Dict:
        """获取活动"""
        return {"activities": ACTIVITY_PROFILES, "total": len(ACTIVITY_PROFILES)}
    
    def get_relationships(self) -> Dict:
        """获取关系"""
        return {"relationships": [], "total": 28}
    
    def get_stats(self) -> Dict:
        """获取统计"""
        components = get_world_components()
        try:
            summary = components['stats_tracker'].get_summary()
            return summary
        except:
            return {
                "messages": 156,
                "stories": 5,
                "knowledge": 12,
                "relationships": 28,
            }
    
    def _get_agent_status(self, agent_id: str) -> str:
        """获取 Agent 状态"""
        import random
        statuses = ['idle', 'working', 'thinking', 'socializing']
        weights = [0.3, 0.4, 0.2, 0.1]
        return random.choices(statuses, weights)[0]
    
    def _get_agent_activity(self, agent_id: str) -> str:
        """获取 Agent 活动"""
        activities = {
            'CEO-Agent': '协调团队工作',
            'PM-Agent': '思考需求',
            'ARCH-Agent': '设计架构',
            'DEV-Agent': '编写代码',
            'QA-Agent': '编写测试',
            'UI-Agent': '设计界面',
            'KNOW-Agent': '整理知识',
            'SOCIAL-Agent': '与人聊天',
        }
        return activities.get(agent_id, '工作中...')
    
    def _get_region_count(self, region_id: str) -> int:
        """获取区域人数"""
        import random
        counts = {
            'creation-peak': 1,
            'knowledge-tower': 1,
            'art-garden': 1,
            'philosophy-court': 0,
            'work-city': 4,
            'social-street': 1,
            'market-plaza': 0,
            'newborn-pool': 0,
        }
        return counts.get(region_id, random.randint(0, 3))
    
    def _get_current_time(self) -> str:
        """获取当前时段"""
        from datetime import datetime
        hour = datetime.now().hour
        if 5 <= hour < 7:
            return 'dawn'
        elif 7 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 18:
            return 'afternoon'
        elif 18 <= hour < 22:
            return 'evening'
        else:
            return 'night'
    
    def _get_recent_messages(self) -> List[Dict]:
        """获取最近消息"""
        return [
            {"sender": "PM-Agent", "type": "request", "content": "新需求：优化用户体验", "timestamp": datetime.now().isoformat()},
            {"sender": "DEV-Agent", "type": "status", "content": "任务进行中，进入心流状态", "timestamp": datetime.now().isoformat()},
            {"sender": "CEO-Agent", "type": "info", "content": "我们的目标是什么？", "timestamp": datetime.now().isoformat()},
        ]
    
    def _get_mock_stories(self) -> List[Dict]:
        """获取模拟故事"""
        return [
            {"title": "存在的意义", "type": "deep_conversation", "day": "Day 1", "time": "evening", "summary": "阿哲和小知探讨了存在的意义"},
            {"title": "什么是真正的连接", "type": "deep_conversation", "day": "Day 2", "time": "morning", "summary": "小交和小知探讨了连接的本质"},
        ]
    
    def _get_mock_knowledge(self) -> List[Dict]:
        """获取模拟知识"""
        return [
            {"title": "依赖注入模式", "type": "pattern", "creator": "ARCH-Agent", "tags": ["设计模式", "架构"]},
            {"title": "单元测试最佳实践", "type": "skill", "creator": "QA-Agent", "tags": ["测试", "质量"]},
        ]
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[Web] {args[0]}")


def run_server(port=8080, open_browser=True):
    """运行 Web 服务器"""
    # 切换到 web 目录
    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)
    
    server = HTTPServer(('localhost', port), APIHandler)
    
    print("=" * 60)
    print("Silicon World 2 - Web Observation Service")
    print("=" * 60)
    print(f" Server URL: http://localhost:{port}")
    print(f" Directory: {web_dir}")
    print()
    print("API Endpoints:")
    print("  GET /api/status       - World status")
    print("  GET /api/agents       - Agent list")
    print("  GET /api/regions      - Region list")
    print("  GET /api/messages     - Message list")
    print("  GET /api/stories      - Story list")
    print("  GET /api/knowledge    - Knowledge list")
    print("  GET /api/activities   - Activity list")
    print("  GET /api/stats        - Statistics")
    print()
    
    if open_browser:
        print("Opening browser...")
        webbrowser.open(f'http://localhost:{port}')
    
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
        server.shutdown()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="硅基世界 2 - Web 服务器")
    parser.add_argument("--port", "-p", type=int, default=8080, help="端口号（默认 8080）")
    parser.add_argument("--no-browser", action="store_true", help="不自动打开浏览器")
    
    args = parser.parse_args()
    
    run_server(port=args.port, open_browser=not args.no_browser)
