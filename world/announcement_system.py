#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界公告系统 - 硅基世界 2

发布全服公告，让所有 Agent 接收重要信息。
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class AnnouncementType(Enum):
    """公告类型"""
    NEWS = "news"          # 新闻
    EVENT = "event"        # 事件
    UPDATE = "update"      # 更新
    EMERGENCY = "emergency"  # 紧急
    CELEBRATION = "celebration"  # 庆祝


class AnnouncementPriority(Enum):
    """公告优先级"""
    LOW = "low"          # 低
    NORMAL = "normal"    # 普通
    HIGH = "high"        # 高
    URGENT = "urgent"    # 紧急


@dataclass
class Announcement:
    """公告"""
    announcement_id: str
    title: str
    content: str
    announcement_type: AnnouncementType
    priority: AnnouncementPriority
    publisher: str
    published_at: float = field(default_factory=lambda: datetime.now().timestamp())
    expires_at: Optional[float] = None
    views: int = 0
    target_audience: List[str] = field(default_factory=list)  # 空表示所有人
    
    def to_dict(self) -> Dict:
        return {
            "announcement_id": self.announcement_id,
            "title": self.title,
            "content": self.content[:500],
            "type": self.announcement_type.value,
            "priority": self.priority.value,
            "publisher": self.publisher,
            "published_at": self.published_at,
            "expires_at": self.expires_at,
            "views": self.views,
        }


class AnnouncementManager:
    """公告管理器"""
    
    def __init__(self):
        """初始化公告管理器"""
        self.announcements: Dict[str, Announcement] = {}
        self._announcement_counter = 0
        
        print("📢 世界公告系统已初始化")
    
    def publish(
        self,
        title: str,
        content: str,
        publisher: str,
        announcement_type: AnnouncementType = AnnouncementType.NEWS,
        priority: AnnouncementPriority = AnnouncementPriority.NORMAL,
        duration_hours: float = 24.0,
        target_audience: Optional[List[str]] = None,
    ) -> Announcement:
        """
        发布公告
        
        Args:
            title: 标题
            content: 内容
            publisher: 发布者
            announcement_type: 公告类型
            priority: 优先级
            duration_hours: 持续时长
            target_audience: 目标受众（空表示所有人）
            
        Returns:
            公告对象
        """
        self._announcement_counter += 1
        
        now = datetime.now().timestamp()
        
        announcement = Announcement(
            announcement_id=f"announce_{self._announcement_counter}",
            title=title,
            content=content,
            announcement_type=announcement_type,
            priority=priority,
            publisher=publisher,
            expires_at=now + (duration_hours * 3600),
            target_audience=target_audience or [],
        )
        
        self.announcements[announcement.announcement_id] = announcement
        
        priority_emoji = {
            AnnouncementPriority.LOW: "📝",
            AnnouncementPriority.NORMAL: "📢",
            AnnouncementPriority.HIGH: "⚠️",
            AnnouncementPriority.URGENT: "🚨",
        }
        
        print(f"  {priority_emoji[priority]} 发布公告：{title}")
        
        return announcement
    
    def view(self, announcement_id: str, viewer: str) -> Optional[Announcement]:
        """查看公告"""
        if announcement_id not in self.announcements:
            return None
        
        announcement = self.announcements[announcement_id]
        
        # 检查是否在目标受众中
        if announcement.target_audience and viewer not in announcement.target_audience:
            return None
        
        announcement.views += 1
        
        return announcement
    
    def get_active_announcements(self) -> List[Announcement]:
        """获取活跃公告"""
        now = datetime.now().timestamp()
        
        return [
            a for a in self.announcements.values()
            if a.expires_at is None or a.expires_at > now
        ]
    
    def get_announcements_for_agent(self, agent_id: str) -> List[Announcement]:
        """获取 Agent 可见的公告"""
        active = self.get_active_announcements()
        
        return [
            a for a in active
            if not a.target_audience or agent_id in a.target_audience
        ]
    
    def remove_announcement(self, announcement_id: str) -> bool:
        """移除公告"""
        if announcement_id not in self.announcements:
            return False
        
        del self.announcements[announcement_id]
        
        return True
    
    def cleanup_expired(self) -> int:
        """清理过期公告"""
        now = datetime.now().timestamp()
        
        expired = [
            aid for aid, a in self.announcements.items()
            if a.expires_at and a.expires_at <= now
        ]
        
        for aid in expired:
            del self.announcements[aid]
        
        if expired:
            print(f"  🗑️ 清理了 {len(expired)} 个过期公告")
        
        return len(expired)
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        active = self.get_active_announcements()
        
        return {
            "total_announcements": len(self.announcements),
            "active": len(active),
            "total_views": sum(a.views for a in self.announcements.values()),
            "by_type": {
                t.value: len([a for a in active if a.announcement_type == t])
                for t in AnnouncementType
            },
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "active": [a.to_dict() for a in self.get_active_announcements()[:10]],
        }


# 单例
_announcement_manager: Optional[AnnouncementManager] = None


def get_announcement_manager() -> AnnouncementManager:
    """获取公告管理器单例"""
    global _announcement_manager
    if _announcement_manager is None:
        _announcement_manager = AnnouncementManager()
    return _announcement_manager


# 工厂函数
def create_announcement_manager() -> AnnouncementManager:
    """创建公告管理器"""
    return AnnouncementManager()
