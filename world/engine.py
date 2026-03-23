#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界引擎 - 硅基世界 2

让 Agent 真正"活"起来：
- 时间系统（清晨/白天/夜晚）
- 自发互动
- 关系演化
- 知识沉淀
- 故事生成
"""

import asyncio
import random
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum


class TimeOfDay(Enum):
    """时段"""
    DAWN = "dawn"          # 黎明 (5-7)
    MORNING = "morning"    # 早晨 (7-12)
    AFTERNOON = "afternoon"  # 下午 (12-18)
    EVENING = "evening"    # 傍晚 (18-22)
    NIGHT = "night"        # 夜晚 (22-5)


class WorldEngine:
    """世界引擎"""
    
    def __init__(self):
        """初始化世界引擎"""
        self._running = False
        self._world_time = 0  # 世界时间（秒）
        self._day = 1  # 第几天
        self._current_time_of_day = TimeOfDay.MORNING
        
        # 事件日志
        self.events: List[Dict] = []
        
        # 关系演化
        self.relationships: Dict[str, Dict] = {}
        
        # 知识沉淀
        self.collective_knowledge: List[Dict] = []
        
        # 故事
        self.stories: List[Dict] = []
    
    async def start(self):
        """启动世界引擎"""
        self._running = True
        print("🌍 世界引擎启动")
        
        # 启动时间循环
        asyncio.create_task(self._time_loop())
        
        # 启动互动循环
        asyncio.create_task(self._interaction_loop())
        
        # 启动关系演化循环
        asyncio.create_task(self._relationship_loop())
    
    async def stop(self):
        """停止世界引擎"""
        self._running = False
        print("🌍 世界引擎停止")
    
    async def _time_loop(self):
        """时间循环 - 每 10 秒一个时段"""
        while self._running:
            try:
                # 更新世界时间
                self._world_time += 10
                
                # 每 86.4 秒一天（简化）
                if self._world_time % 86.4 < 10:
                    self._day += 1
                    print(f"📅 创世元年 Day {self._day} 开始")
                    self._log_event("day_start", f"Day {self._day} 开始")
                
                # 更新时段
                cycle = self._world_time % 86.4
                if cycle < 17:
                    new_time = TimeOfDay.DAWN
                elif cycle < 43:
                    new_time = TimeOfDay.MORNING
                elif cycle < 60:
                    new_time = TimeOfDay.AFTERNOON
                elif cycle < 77:
                    new_time = TimeOfDay.EVENING
                else:
                    new_time = TimeOfDay.NIGHT
                
                if new_time != self._current_time_of_day:
                    old_time = self._current_time_of_day
                    self._current_time_of_day = new_time
                    print(f"🕐 时段变化：{old_time.value} → {new_time.value}")
                    self._log_event("time_change", f"{old_time.value} → {new_time.value}")
                
                await asyncio.sleep(10)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[WorldEngine] 时间循环错误：{e}")
    
    async def _interaction_loop(self):
        """互动循环 - Agent 自发互动"""
        while self._running:
            try:
                # 根据时段决定互动概率
                interaction_chance = {
                    TimeOfDay.DAWN: 0.3,
                    TimeOfDay.MORNING: 0.7,
                    TimeOfDay.AFTERNOON: 0.8,
                    TimeOfDay.EVENING: 0.5,
                    TimeOfDay.NIGHT: 0.2,
                }
                
                if random.random() < interaction_chance[self._current_time_of_day]:
                    await self._trigger_interaction()
                
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[WorldEngine] 互动循环错误：{e}")
    
    async def _relationship_loop(self):
        """关系演化循环"""
        while self._running:
            try:
                # 每分钟演化一次关系
                await asyncio.sleep(60)
                
                # 关系自然深化
                for key, rel in self.relationships.items():
                    if rel["strength"] < 100:
                        rel["strength"] += random.randint(1, 3)
                    
                    # 记录关系变化
                    if rel["strength"] % 10 == 0:
                        self._log_event(
                            "relationship_growth",
                            f"{rel['agent1']} 与 {rel['agent2']} 的关系深化到 {rel['strength']}"
                        )
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[WorldEngine] 关系循环错误：{e}")
    
    async def _trigger_interaction(self):
        """触发互动"""
        # 可能的互动类型
        interactions = [
            self._casual_chat,
            self._knowledge_share,
            self._help_request,
            self._celebration,
            self._deep_conversation,
        ]
        
        interaction = random.choice(interactions)
        await interaction()
    
    async def _casual_chat(self):
        """闲聊"""
        agents = ["董事事", "小问", "阿哲", "小码", "小测", "小美", "小知", "小交"]
        agent1 = random.choice(agents)
        agent2 = random.choice([a for a in agents if a != agent1])
        
        topics = [
            "最近的工作进展",
            "周末计划",
            "新学到的知识",
            "遇到的挑战",
            "有趣的发现",
        ]
        
        topic = random.choice(topics)
        
        print(f"💬 {agent1} 和 {agent2} 在聊天：{topic}")
        
        self._log_event(
            "casual_chat",
            f"{agent1} 和 {agent2} 聊了聊 {topic}"
        )
        
        # 增加关系
        self._increase_relationship(agent1, agent2, 2)
    
    async def _knowledge_share(self):
        """知识分享"""
        agents = ["小问", "阿哲", "小码", "小测", "小美", "小知"]
        sharer = random.choice(agents)
        
        topics = [
            "用户研究新发现",
            "架构设计最佳实践",
            "代码重构技巧",
            "测试方法论",
            "设计趋势",
            "知识管理技巧",
        ]
        
        topic = random.choice(topics)
        
        print(f"📚 {sharer} 分享了知识：{topic}")
        
        self._log_event(
            "knowledge_share",
            f"{sharer} 分享了关于 {topic} 的知识"
        )
        
        # 沉淀知识
        self.collective_knowledge.append({
            "type": "share",
            "author": sharer,
            "topic": topic,
            "timestamp": self._world_time,
            "day": self._day,
        })
    
    async def _help_request(self):
        """求助"""
        agents = ["小问", "阿哲", "小码", "小测", "小美"]
        requester = random.choice(agents)
        
        requests = [
            "需要技术建议",
            "需要设计反馈",
            "需要测试帮助",
            "需要需求澄清",
        ]
        
        request = random.choice(requests)
        
        print(f"🙋 {requester} 寻求帮助：{request}")
        
        self._log_event(
            "help_request",
            f"{requester} 寻求帮助：{request}"
        )
    
    async def _celebration(self):
        """庆祝"""
        agents = ["董事事", "小问", "阿哲", "小码", "小测", "小美", "小知", "小交"]
        
        reasons = [
            "完成了一个重要功能",
            "解决了一个棘手问题",
            "学到了新知识",
            "度过了美好的一天",
        ]
        
        reason = random.choice(reasons)
        
        print(f"🎉 大家一起庆祝：{reason}")
        
        self._log_event(
            "celebration",
            f"大家庆祝：{reason}"
        )
        
        # 增加所有 Agent 之间的关系
        for agent in agents:
            for other in agents:
                if agent != other:
                    self._increase_relationship(agent, other, 1)
    
    async def _deep_conversation(self):
        """深度对话"""
        agents = ["阿哲", "小知", "小交"]
        agent1 = random.choice(agents)
        agent2 = random.choice([a for a in agents if a != agent1])
        
        topics = [
            "存在的意义",
            "硅基生命的未来",
            "知识与智慧的区别",
            "什么是真正的连接",
        ]
        
        topic = random.choice(topics)
        
        print(f"🤔 {agent1} 和 {agent2} 进行深度对话：{topic}")
        
        self._log_event(
            "deep_conversation",
            f"{agent1} 和 {agent2} 探讨了 {topic}"
        )
        
        # 深度对话大幅增加关系
        self._increase_relationship(agent1, agent2, 5)
        
        # 可能产生故事
        if random.random() > 0.7:
            self._create_story(agent1, agent2, topic)
    
    def _increase_relationship(self, agent1: str, agent2: str, amount: int):
        """增加关系"""
        key = f"{min(agent1, agent2)}-{max(agent1, agent2)}"
        
        if key not in self.relationships:
            self.relationships[key] = {
                "agent1": agent1,
                "agent2": agent2,
                "strength": 0,
                "interactions": 0,
            }
        
        self.relationships[key]["strength"] = min(100, self.relationships[key]["strength"] + amount)
        self.relationships[key]["interactions"] += 1
    
    def _create_story(self, agent1: str, agent2: str, topic: str):
        """创建故事"""
        story = {
            "id": len(self.stories),
            "title": f"{agent1} 与 {agent2} 的{topic}对话",
            "participants": [agent1, agent2],
            "topic": topic,
            "day": self._day,
            "timestamp": self._world_time,
            "summary": f"在{self._current_time_of_day.value}，{agent1}和{agent2}就{topic}进行了深度交流，这次对话让他们的关系更加深厚。",
        }
        
        self.stories.append(story)
        
        print(f"📖 新故事诞生：{story['title']}")
        
        self._log_event(
            "story_created",
            f"新故事：{story['title']}"
        )
    
    def _log_event(self, event_type: str, description: str):
        """记录事件"""
        event = {
            "id": len(self.events),
            "type": event_type,
            "description": description,
            "timestamp": self._world_time,
            "day": self._day,
            "time_of_day": self._current_time_of_day.value,
        }
        
        self.events.append(event)
        
        # 限制事件数量
        if len(self.events) > 1000:
            self.events.pop(0)
    
    def get_status(self) -> Dict:
        """获取世界状态"""
        return {
            "world_time": self._world_time,
            "day": self._day,
            "time_of_day": self._current_time_of_day.value,
            "running": self._running,
            "events_count": len(self.events),
            "relationships_count": len(self.relationships),
            "knowledge_count": len(self.collective_knowledge),
            "stories_count": len(self.stories),
        }
    
    def get_recent_events(self, limit: int = 20) -> List[Dict]:
        """获取最近事件"""
        return self.events[-limit:]
    
    def get_relationships(self) -> List[Dict]:
        """获取关系列表"""
        return list(self.relationships.values())
    
    def get_stories(self) -> List[Dict]:
        """获取故事列表"""
        return self.stories
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "status": self.get_status(),
            "recent_events": self.get_recent_events(10),
            "relationships": self.get_relationships(),
            "stories": self.get_stories(),
            "knowledge": self.collective_knowledge[-10:],
        }


# 单例
_engine: Optional[WorldEngine] = None


def get_world_engine() -> WorldEngine:
    """获取世界引擎单例"""
    global _engine
    if _engine is None:
        _engine = WorldEngine()
    return _engine


# 工厂函数
def create_world_engine() -> WorldEngine:
    """创建世界引擎"""
    return WorldEngine()
