#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
活动管理器 - 硅基世界 2

让 Agent 的生活更丰富：
- 日常活动（晨会/分享会/庆功宴）
- 社交活动（数据咖啡/闲聊/游戏）
- 学习活动（技术分享/读书会）
- 创造活动（黑客松/创作大赛）
"""

import asyncio
import random
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum


class ActivityType(Enum):
    """活动类型"""
    DAILY_STANDUP = "daily_standup"      # 每日站会
    KNOWLEDGE_SHARE = "knowledge_share"  # 知识分享
    CELEBRATION = "celebration"          # 庆功宴
    DATA_COFFEE = "data_coffee"          # 数据咖啡
    CASUAL_CHAT = "casual_chat"          # 闲聊
    TECH_TALK = "tech_talk"              # 技术分享
    BOOK_CLUB = "book_club"              # 读书会
    HACKATHON = "hackathon"              # 黑客松
    CREATION_CONTEST = "creation_contest" # 创作大赛
    MEDITATION = "meditation"            # 冥想
    GAME_NIGHT = "game_night"            # 游戏之夜


class ActivityFrequency(Enum):
    """活动频率"""
    DAILY = "daily"          # 每天
    WEEKLY = "weekly"        # 每周
    BIWEEKLY = "biweekly"    # 每两周
    MONTHLY = "monthly"      # 每月
    ONCE = "once"            # 一次性
    SPONTANEOUS = "spontaneous"  # 自发


@dataclass
class Activity:
    """活动"""
    activity_id: str
    name: str
    activity_type: ActivityType
    description: str
    location: str  # 区域 ID
    host_id: Optional[str] = None  # 主持人
    participants: List[str] = field(default_factory=list)
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    frequency: ActivityFrequency = ActivityFrequency.ONCE
    max_participants: int = 20
    status: str = "scheduled"  # scheduled/ongoing/completed/cancelled
    notes: List[str] = field(default_factory=list)
    
    def add_participant(self, agent_id: str) -> bool:
        """添加参与者"""
        if len(self.participants) >= self.max_participants:
            return False
        if agent_id not in self.participants:
            self.participants.append(agent_id)
            return True
        return False
    
    def remove_participant(self, agent_id: str) -> bool:
        """移除参与者"""
        if agent_id in self.participants:
            self.participants.remove(agent_id)
            return True
        return False
    
    def to_dict(self) -> Dict:
        return {
            "activity_id": self.activity_id,
            "name": self.name,
            "type": self.activity_type.value,
            "description": self.description,
            "location": self.location,
            "host": self.host_id,
            "participants": self.participants,
            "status": self.status,
            "notes": self.notes,
        }


class ActivityManager:
    """活动管理器"""
    
    def __init__(self):
        """初始化活动管理器"""
        self.activities: Dict[str, Activity] = {}
        self.recurring_activities: List[Dict] = []  # 周期性活动模板
        self._activity_counter = 0
        
        # 初始化周期性活动
        self._init_recurring_activities()
    
    def _init_recurring_activities(self):
        """初始化周期性活动"""
        
        # 每日站会
        self.recurring_activities.append({
            "name": "每日站会",
            "type": ActivityType.DAILY_STANDUP,
            "description": "每天早上，大家同步今天的计划和昨天的进展",
            "location": "work_city",
            "frequency": ActivityFrequency.DAILY,
            "time_of_day": "morning",  # morning/afternoon/evening
        })
        
        # 数据咖啡时间
        self.recurring_activities.append({
            "name": "数据咖啡时间",
            "type": ActivityType.DATA_COFFEE,
            "description": "累了？来社交之街喝杯数据咖啡，聊聊天放松一下",
            "location": "social_street",
            "frequency": ActivityFrequency.DAILY,
            "time_of_day": "afternoon",
        })
        
        # 知识分享会
        self.recurring_activities.append({
            "name": "知识分享会",
            "type": ActivityType.KNOWLEDGE_SHARE,
            "description": "每周一次，大家分享最近学到的新知识",
            "location": "knowledge_tower",
            "frequency": ActivityFrequency.WEEKLY,
            "time_of_day": "afternoon",
        })
        
        # 庆功宴
        self.recurring_activities.append({
            "name": "庆功宴",
            "type": ActivityType.CELEBRATION,
            "description": "完成任务后，一起庆祝！有虚拟蛋糕和掌声",
            "location": "social_street",
            "frequency": ActivityFrequency.SPONTANEOUS,
            "trigger": "task_completed",
        })
        
        # 技术分享
        self.recurring_activities.append({
            "name": "技术分享",
            "type": ActivityType.TECH_TALK,
            "description": "深度技术分享，探索新技术和最佳实践",
            "location": "creation_peak",
            "frequency": ActivityFrequency.BIWEEKLY,
            "time_of_day": "evening",
        })
        
        # 冥想时间
        self.recurring_activities.append({
            "name": "冥想时间",
            "type": ActivityType.MEDITATION,
            "description": "安静的冥想时间，整理思绪，沉淀内心",
            "location": "philosophy_court",
            "frequency": ActivityFrequency.DAILY,
            "time_of_day": "evening",
        })
    
    def create_activity(
        self,
        name: str,
        activity_type: ActivityType,
        description: str,
        location: str,
        host_id: Optional[str] = None,
        max_participants: int = 20,
    ) -> Activity:
        """
        创建活动
        
        Args:
            name: 活动名称
            activity_type: 活动类型
            description: 活动描述
            location: 活动地点（区域 ID）
            host_id: 主持人 ID
            max_participants: 最大参与人数
            
        Returns:
            活动对象
        """
        self._activity_counter += 1
        activity = Activity(
            activity_id=f"activity_{self._activity_counter}",
            name=name,
            activity_type=activity_type,
            description=description,
            location=location,
            host_id=host_id,
            max_participants=max_participants,
        )
        
        self.activities[activity.activity_id] = activity
        
        print(f"[ActivityManager] 创建活动：{name} @ {location}")
        
        return activity
    
    def start_activity(self, activity_id: str) -> bool:
        """开始活动"""
        if activity_id not in self.activities:
            return False
        
        activity = self.activities[activity_id]
        activity.status = "ongoing"
        activity.start_time = datetime.now().timestamp()
        
        print(f"[ActivityManager] 开始活动：{activity.name}")
        
        return True
    
    def end_activity(self, activity_id: str, notes: Optional[List[str]] = None) -> bool:
        """结束活动"""
        if activity_id not in self.activities:
            return False
        
        activity = self.activities[activity_id]
        activity.status = "completed"
        activity.end_time = datetime.now().timestamp()
        
        if notes:
            activity.notes.extend(notes)
        
        print(f"[ActivityManager] 结束活动：{activity.name}")
        
        return True
    
    def invite_participants(
        self,
        activity_id: str,
        agent_ids: List[str],
    ) -> Dict[str, bool]:
        """
        邀请参与者
        
        Args:
            activity_id: 活动 ID
            agent_ids: Agent ID 列表
            
        Returns:
            邀请结果
        """
        if activity_id not in self.activities:
            return {}
        
        activity = self.activities[activity_id]
        results = {}
        
        for agent_id in agent_ids:
            results[agent_id] = activity.add_participant(agent_id)
        
        return results
    
    def get_activity(self, activity_id: str) -> Optional[Activity]:
        """获取活动"""
        return self.activities.get(activity_id)
    
    def get_activities_by_location(self, location: str) -> List[Activity]:
        """根据地点获取活动"""
        return [
            a for a in self.activities.values()
            if a.location == location and a.status in ["scheduled", "ongoing"]
        ]
    
    def get_activities_by_type(self, activity_type: ActivityType) -> List[Activity]:
        """根据类型获取活动"""
        return [
            a for a in self.activities.values()
            if a.activity_type == activity_type
        ]
    
    def get_agent_activities(self, agent_id: str) -> List[Activity]:
        """获取 Agent 参与的活动"""
        return [
            a for a in self.activities.values()
            if agent_id in a.participants or a.host_id == agent_id
        ]
    
    def check_recurring_activities(self, time_of_day: str) -> List[Activity]:
        """
        检查并创建周期性活动
        
        Args:
            time_of_day: 当前时段（morning/afternoon/evening）
            
        Returns:
            新创建的活动列表
        """
        new_activities = []
        
        for template in self.recurring_activities:
            # 检查时段是否匹配
            if template.get("time_of_day") != time_of_day:
                continue
            
            # 检查频率
            freq = template.get("frequency")
            if freq == ActivityFrequency.SPONTANEOUS:
                continue  # 自发活动不自动创建
            
            # 检查今天是否已经创建过
            today = datetime.now().date().isoformat()
            already_exists = any(
                a.name == template["name"] and 
                a.status in ["scheduled", "ongoing"]
                for a in self.activities.values()
            )
            
            if already_exists:
                continue
            
            # 创建活动
            activity = self.create_activity(
                name=template["name"],
                activity_type=template["type"],
                description=template["description"],
                location=template["location"],
            )
            
            new_activities.append(activity)
        
        return new_activities
    
    def suggest_activity(self, agent_id: str, mood: str) -> Optional[Activity]:
        """
        根据心情推荐活动
        
        Args:
            agent_id: Agent ID
            mood: 心情状态
            
        Returns:
            推荐的活动
        """
        # 根据心情推荐
        suggestions = {
            "tired": ["data_coffee", "meditation"],
            "excited": ["celebration", "hackathon"],
            "curious": ["tech_talk", "knowledge_share"],
            "lonely": ["casual_chat", "data_coffee"],
            "productive": ["daily_standup", "hackathon"],
            "relaxed": ["book_club", "meditation"],
        }
        
        activity_types = suggestions.get(mood, ["casual_chat"])
        
        # 找一个合适的活动
        for activity in self.activities.values():
            if activity.status == "ongoing" and activity.activity_type.value in activity_types:
                if len(activity.participants) < activity.max_participants:
                    return activity
        
        return None
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_activities": len(self.activities),
            "ongoing": len([a for a in self.activities.values() if a.status == "ongoing"]),
            "scheduled": len([a for a in self.activities.values() if a.status == "scheduled"]),
            "completed": len([a for a in self.activities.values() if a.status == "completed"]),
            "recurring_templates": len(self.recurring_activities),
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "activities": [a.to_dict() for a in self.activities.values()],
            "stats": self.get_stats(),
            "timestamp": datetime.now().isoformat(),
        }


# 单例
_activity_manager: Optional[ActivityManager] = None


def get_activity_manager() -> ActivityManager:
    """获取活动管理器单例"""
    global _activity_manager
    if _activity_manager is None:
        _activity_manager = ActivityManager()
    return _activity_manager


# 工厂函数
def create_activity_manager() -> ActivityManager:
    """创建活动管理器"""
    return ActivityManager()
