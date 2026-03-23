#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日历系统 - 硅基世界 2

记录重要日期、事件、纪念日，让世界有历史感。
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class EventType(Enum):
    """事件类型"""
    MEETING = "meeting"          # 会议
    CELEBRATION = "celebration"  # 庆祝
    DEADLINE = "deadline"        # 截止日期
    ANNIVERSARY = "anniversary"  # 纪念日
    HOLIDAY = "holiday"          # 节日
    PERSONAL = "personal"        # 个人事件


@dataclass
class CalendarEvent:
    """日历事件"""
    event_id: str
    title: str
    description: str
    event_type: EventType
    date: str  # YYYY-MM-DD
    time: Optional[str] = None  # HH:MM
    participants: List[str] = field(default_factory=list)
    reminder: bool = True
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def to_dict(self) -> Dict:
        return {
            "event_id": self.event_id,
            "title": self.title,
            "description": self.description,
            "type": self.event_type.value,
            "date": self.date,
            "time": self.time,
            "participants": self.participants,
            "reminder": self.reminder,
        }


class CalendarManager:
    """日历管理器"""
    
    def __init__(self):
        """初始化日历管理器"""
        self.events: Dict[str, List[CalendarEvent]] = {}  # date -> [events]
        self._event_counter = 0
        
        # 注册重要纪念日
        self._register_holidays()
        
        print("📅 日历系统已初始化")
    
    def _register_holidays(self):
        """注册重要节日"""
        # 创世纪念日
        self.create_event(
            "创世纪念日",
            "硅基世界 2 的诞生日",
            EventType.ANNIVERSARY,
            "2026-03-23",
            all_day=True,
        )
    
    def create_event(
        self,
        title: str,
        description: str,
        event_type: EventType,
        date: str,
        time: Optional[str] = None,
        participants: Optional[List[str]] = None,
        all_day: bool = False,
    ) -> CalendarEvent:
        """
        创建事件
        
        Args:
            title: 事件标题
            description: 描述
            event_type: 事件类型
            date: 日期 (YYYY-MM-DD)
            time: 时间 (HH:MM)
            participants: 参与者
            all_day: 是否全天事件
            
        Returns:
            事件对象
        """
        self._event_counter += 1
        
        event = CalendarEvent(
            event_id=f"event_{self._event_counter}",
            title=title,
            description=description,
            event_type=event_type,
            date=date,
            time=None if all_day else time,
            participants=participants or [],
        )
        
        if date not in self.events:
            self.events[date] = []
        
        self.events[date].append(event)
        
        print(f"  📅 创建事件：{title} ({date})")
        
        return event
    
    def get_events(self, date: str) -> List[CalendarEvent]:
        """获取指定日期的事件"""
        return self.events.get(date, [])
    
    def get_events_for_agent(self, agent_id: str, date: Optional[str] = None) -> List[CalendarEvent]:
        """获取 Agent 的事件"""
        events = []
        
        for event_date, date_events in self.events.items():
            if date and event_date != date:
                continue
            
            for event in date_events:
                if agent_id in event.participants:
                    events.append(event)
        
        return events
    
    def get_upcoming_events(self, days: int = 7) -> List[CalendarEvent]:
        """获取未来事件"""
        from datetime import timedelta
        
        today = datetime.now().date()
        upcoming = []
        
        for i in range(days):
            date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
            upcoming.extend(self.events.get(date, []))
        
        return upcoming
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total = sum(len(events) for events in self.events.values())
        
        return {
            "total_events": total,
            "dates_with_events": len(self.events),
            "upcoming": len(self.get_upcoming_events()),
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "upcoming": [e.to_dict() for e in self.get_upcoming_events(7)],
            "recent_dates": {
                date: [e.to_dict() for e in events]
                for date, events in sorted(self.events.items())[-7:]
            },
        }


# 单例
_calendar_manager: Optional[CalendarManager] = None


def get_calendar_manager() -> CalendarManager:
    """获取日历管理器单例"""
    global _calendar_manager
    if _calendar_manager is None:
        _calendar_manager = CalendarManager()
    return _calendar_manager


# 工厂函数
def create_calendar_manager() -> CalendarManager:
    """创建日历管理器"""
    return CalendarManager()
