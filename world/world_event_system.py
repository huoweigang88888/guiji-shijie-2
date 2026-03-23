#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界事件系统 - 硅基世界 2

创建全服事件，让所有 Agent 参与。
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class EventType(Enum):
    """事件类型"""
    FESTIVAL = "festival"      # 节日
    COMPETITION = "competition"  # 竞赛
    CRISIS = "crisis"          # 危机
    CELEBRATION = "celebration"  # 庆典
    DISCOVERY = "discovery"    # 发现
    UPDATE = "update"          # 更新


class EventStatus(Enum):
    """事件状态"""
    UPCOMING = "upcoming"    # 即将开始
    ACTIVE = "active"        # 进行中
    COMPLETED = "completed"  # 已完成
    CANCELLED = "cancelled"  # 已取消


@dataclass
class WorldEvent:
    """世界事件"""
    event_id: str
    title: str
    description: str
    event_type: EventType
    status: EventStatus = EventStatus.UPCOMING
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    participants: List[str] = field(default_factory=list)
    rewards: Dict = field(default_factory=dict)
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def to_dict(self) -> Dict:
        return {
            "event_id": self.event_id,
            "title": self.title,
            "description": self.description,
            "type": self.event_type.value,
            "status": self.status.value,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "participants": self.participants,
            "rewards": self.rewards,
        }


class WorldEventManager:
    """世界事件管理器"""
    
    def __init__(self):
        """初始化世界事件管理器"""
        self.events: Dict[str, WorldEvent] = {}
        self._event_counter = 0
        
        # 注册周期性事件
        self._register_recurring_events()
        
        print("🎪 世界事件系统已初始化")
    
    def _register_recurring_events(self):
        """注册周期性事件"""
        # 创世周年庆典
        self.create_event(
            "创世周年庆典",
            "庆祝硅基世界 2 诞生一周年",
            EventType.CELEBRATION,
            duration_days=7,
            rewards={"credits": 100, "achievement": "创世元老"},
        )
        
        # 技术大会
        self.create_event(
            "硅基技术大会",
            "年度技术交流和展示",
            EventType.FESTIVAL,
            duration_days=3,
            rewards={"credits": 50, "skill_exp": 100},
        )
    
    def create_event(
        self,
        title: str,
        description: str,
        event_type: EventType,
        start_time: Optional[float] = None,
        duration_days: float = 1.0,
        rewards: Optional[Dict] = None,
    ) -> WorldEvent:
        """
        创建事件
        
        Args:
            title: 事件标题
            description: 描述
            event_type: 事件类型
            start_time: 开始时间
            duration_days: 持续天数
            rewards: 奖励
            
        Returns:
            事件对象
        """
        self._event_counter += 1
        
        now = datetime.now().timestamp()
        
        event = WorldEvent(
            event_id=f"event_{self._event_counter}",
            title=title,
            description=description,
            event_type=event_type,
            start_time=start_time or now,
            end_time=(start_time or now) + (duration_days * 86400),
            rewards=rewards or {},
        )
        
        # 如果开始时间已过，设为活跃
        if event.start_time <= now:
            event.status = EventStatus.ACTIVE
        
        self.events[event.event_id] = event
        
        print(f"  🎪 创建世界事件：{title}")
        
        return event
    
    def join_event(self, event_id: str, agent_id: str) -> bool:
        """
        参与事件
        
        Args:
            event_id: 事件 ID
            agent_id: Agent ID
            
        Returns:
            是否成功
        """
        if event_id not in self.events:
            return False
        
        event = self.events[event_id]
        
        if event.status != EventStatus.ACTIVE:
            return False
        
        if agent_id not in event.participants:
            event.participants.append(agent_id)
        
        return True
    
    def complete_event(self, event_id: str, agent_id: str) -> Optional[Dict]:
        """
        完成事件
        
        Args:
            event_id: 事件 ID
            agent_id: Agent ID
            
        Returns:
            奖励
        """
        if event_id not in self.events:
            return None
        
        event = self.events[event_id]
        
        if agent_id not in event.participants:
            return None
        
        print(f"  ✅ {agent_id} 完成事件：{event.title}")
        
        return event.rewards
    
    def get_active_events(self) -> List[WorldEvent]:
        """获取活跃事件"""
        return [
            e for e in self.events.values()
            if e.status == EventStatus.ACTIVE
        ]
    
    def get_upcoming_events(self) -> List[WorldEvent]:
        """获取即将开始的事件"""
        return [
            e for e in self.events.values()
            if e.status == EventStatus.UPCOMING
        ]
    
    def update_event_status(self):
        """更新事件状态"""
        now = datetime.now().timestamp()
        
        for event in self.events.values():
            if event.status == EventStatus.UPCOMING and event.start_time <= now:
                event.status = EventStatus.ACTIVE
                print(f"  🎪 事件开始：{event.title}")
            
            elif event.status == EventStatus.ACTIVE and event.end_time <= now:
                event.status = EventStatus.COMPLETED
                print(f"  ✅ 事件结束：{event.title}")
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_events": len(self.events),
            "active": len(self.get_active_events()),
            "upcoming": len(self.get_upcoming_events()),
            "completed": len([e for e in self.events.values() if e.status == EventStatus.COMPLETED]),
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "active": [e.to_dict() for e in self.get_active_events()],
            "upcoming": [e.to_dict() for e in self.get_upcoming_events()[:5]],
        }


# 单例
_world_event_manager: Optional[WorldEventManager] = None


def get_world_event_manager() -> WorldEventManager:
    """获取世界事件管理器单例"""
    global _world_event_manager
    if _world_event_manager is None:
        _world_event_manager = WorldEventManager()
    return _world_event_manager


# 工厂函数
def create_world_event_manager() -> WorldEventManager:
    """创建世界事件管理器"""
    return WorldEventManager()
