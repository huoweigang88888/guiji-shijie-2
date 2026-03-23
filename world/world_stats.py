#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界统计系统 - 硅基世界 2

提供详细的世界统计数据，用于分析和展示。
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class DailyStats:
    """每日统计"""
    date: str
    messages_sent: int = 0
    tasks_completed: int = 0
    knowledge_shared: int = 0
    conflicts_resolved: int = 0
    achievements_earned: int = 0
    friendships_formed: int = 0
    total_transactions: float = 0.0


class WorldStatsManager:
    """世界统计管理器"""
    
    def __init__(self):
        """初始化世界统计管理器"""
        self.daily_stats: Dict[str, DailyStats] = {}
        self.start_time = datetime.now()
        
        # 累计统计
        self.total = {
            "messages": 0,
            "tasks": 0,
            "knowledge": 0,
            "conflicts": 0,
            "achievements": 0,
            "friendships": 0,
            "transactions": 0.0,
        }
        
        print("📊 世界统计系统已初始化")
    
    def record_message(self):
        """记录消息"""
        self._increment("messages")
    
    def record_task(self):
        """记录任务"""
        self._increment("tasks")
    
    def record_knowledge(self):
        """记录知识分享"""
        self._increment("knowledge")
    
    def record_conflict(self):
        """记录冲突"""
        self._increment("conflicts")
    
    def record_achievement(self):
        """记录成就"""
        self._increment("achievements")
    
    def record_friendship(self):
        """记录好友关系"""
        self._increment("friendships")
    
    def record_transaction(self, amount: float):
        """记录交易"""
        self.total["transactions"] += amount
        self._get_today_stats().total_transactions += amount
    
    def _increment(self, key: str):
        """增加计数"""
        self.total[key] = self.total.get(key, 0) + 1
        today_stats = self._get_today_stats()
        setattr(today_stats, f"{key}_sent" if key == "messages" else f"{key}_completed" if key == "tasks" else key + ("_shared" if key == "knowledge" else "_resolved" if key == "conflicts" else "_earned" if key == "achievements" else "_formed"), 
                getattr(today_stats, f"{key}_sent" if key == "messages" else f"{key}_completed" if key == "tasks" else key + ("_shared" if key == "knowledge" else "_resolved" if key == "conflicts" else "_earned" if key == "achievements" else "_formed"), 0) + 1)
    
    def _get_today_stats(self) -> DailyStats:
        """获取今日统计"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in self.daily_stats:
            self.daily_stats[today] = DailyStats(date=today)
        
        return self.daily_stats[today]
    
    def get_summary(self) -> Dict:
        """获取统计摘要"""
        uptime = datetime.now() - self.start_time
        
        return {
            "uptime_seconds": uptime.total_seconds(),
            "uptime_human": str(uptime),
            "total": self.total,
            "today": {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "messages": self._get_today_stats().messages_sent,
                "tasks": self._get_today_stats().tasks_completed,
                "knowledge": self._get_today_stats().knowledge_shared,
            },
        }
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.get_summary()
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "summary": self.get_summary(),
            "recent_days": [
                {
                    "date": stats.date,
                    "messages": stats.messages_sent,
                    "tasks": stats.tasks_completed,
                    "knowledge": stats.knowledge_shared,
                }
                for stats in list(self.daily_stats.values())[-7:]
            ],
        }


# 单例
_world_stats_manager: Optional[WorldStatsManager] = None


def get_world_stats_manager() -> WorldStatsManager:
    """获取世界统计管理器单例"""
    global _world_stats_manager
    if _world_stats_manager is None:
        _world_stats_manager = WorldStatsManager()
    return _world_stats_manager


# 工厂函数
def create_world_stats_manager() -> WorldStatsManager:
    """创建世界统计管理器"""
    return WorldStatsManager()
