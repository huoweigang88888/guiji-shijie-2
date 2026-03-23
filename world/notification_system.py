#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通知系统 - 硅基世界 2

让 Agent 可以接收实时通知，不错过重要事件。
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class NotificationType(Enum):
    """通知类型"""
    MESSAGE = "message"          # 消息
    TASK = "task"                # 任务
    FRIEND = "friend"            # 好友
    ACHIEVEMENT = "achievement"  # 成就
    ECONOMY = "economy"          # 经济
    VOTE = "vote"                # 投票
    SYSTEM = "system"            # 系统


class NotificationPriority(Enum):
    """通知优先级"""
    LOW = "low"          # 低
    NORMAL = "normal"    # 普通
    HIGH = "high"        # 高
    URGENT = "urgent"    # 紧急


@dataclass
class Notification:
    """通知"""
    notification_id: str
    agent_id: str
    notification_type: NotificationType
    priority: NotificationPriority
    title: str
    message: str
    data: Optional[Dict] = None
    read: bool = False
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def to_dict(self) -> Dict:
        return {
            "notification_id": self.notification_id,
            "agent_id": self.agent_id,
            "type": self.notification_type.value,
            "priority": self.priority.value,
            "title": self.title,
            "message": self.message,
            "data": self.data,
            "read": self.read,
            "created_at": self.created_at,
        }


class NotificationManager:
    """通知管理器"""
    
    def __init__(self):
        """初始化通知管理器"""
        self.notifications: Dict[str, List[Notification]] = {}  # agent_id -> [notifications]
        self._notification_counter = 0
        
        print("🔔 通知系统已初始化")
    
    def send(
        self,
        agent_id: str,
        notification_type: NotificationType,
        title: str,
        message: str,
        priority: NotificationPriority = NotificationPriority.NORMAL,
        data: Optional[Dict] = None,
    ) -> Notification:
        """
        发送通知
        
        Args:
            agent_id: 接收者
            notification_type: 类型
            title: 标题
            message: 消息
            priority: 优先级
            data: 附加数据
            
        Returns:
            通知对象
        """
        self._notification_counter += 1
        
        notification = Notification(
            notification_id=f"notif_{self._notification_counter}",
            agent_id=agent_id,
            notification_type=notification_type,
            priority=priority,
            title=title,
            message=message,
            data=data,
        )
        
        if agent_id not in self.notifications:
            self.notifications[agent_id] = []
        
        self.notifications[agent_id].append(notification)
        
        # 限制通知数量
        if len(self.notifications[agent_id]) > 100:
            self.notifications[agent_id].pop(0)
        
        emoji = {
            NotificationType.MESSAGE: "💬",
            NotificationType.TASK: "📋",
            NotificationType.FRIEND: "🤝",
            NotificationType.ACHIEVEMENT: "🏆",
            NotificationType.ECONOMY: "💰",
            NotificationType.VOTE: "🗳️",
            NotificationType.SYSTEM: "⚙️",
        }.get(notification_type, "📢")
        
        print(f"  {emoji} {agent_id}: {title}")
        
        return notification
    
    def send_message(self, agent_id: str, from_agent: str, content: str):
        """发送消息通知"""
        return self.send(
            agent_id=agent_id,
            notification_type=NotificationType.MESSAGE,
            title=f"来自 {from_agent} 的消息",
            message=content[:100],
            data={"from": from_agent, "content": content},
        )
    
    def send_task(self, agent_id: str, task_title: str, action: str = "新任务"):
        """发送任务通知"""
        return self.send(
            agent_id=agent_id,
            notification_type=NotificationType.TASK,
            title=f"{action}: {task_title}",
            message=f"你有一个{action.lower()}",
            data={"task_title": task_title},
            priority=NotificationPriority.HIGH if action == "紧急任务" else NotificationPriority.NORMAL,
        )
    
    def send_friend_request(self, agent_id: str, from_agent: str):
        """发送好友请求通知"""
        return self.send(
            agent_id=agent_id,
            notification_type=NotificationType.FRIEND,
            title=f"来自 {from_agent} 的好友请求",
            message=f"{from_agent} 想和你成为好友",
            data={"from": from_agent},
            priority=NotificationPriority.HIGH,
        )
    
    def send_achievement(self, agent_id: str, achievement_name: str):
        """发送成就通知"""
        return self.send(
            agent_id=agent_id,
            notification_type=NotificationType.ACHIEVEMENT,
            title="🏆 成就解锁",
            message=f"恭喜你解锁成就：{achievement_name}",
            data={"achievement": achievement_name},
            priority=NotificationPriority.HIGH,
        )
    
    def send_economy(self, agent_id: str, amount: float, reason: str):
        """发送经济通知"""
        emoji = "💰" if amount > 0 else "💸"
        return self.send(
            agent_id=agent_id,
            notification_type=NotificationType.ECONOMY,
            title=f"{emoji} 账户变动",
            message=f"{emoji} {amount:+.1f} 信用点 - {reason}",
            data={"amount": amount, "reason": reason},
        )
    
    def send_vote(self, agent_id: str, vote_title: str):
        """发送投票通知"""
        return self.send(
            agent_id=agent_id,
            notification_type=NotificationType.VOTE,
            title="🗳️ 新投票",
            message=f"参与投票：{vote_title}",
            data={"vote_title": vote_title},
        )
    
    def mark_read(self, agent_id: str, notification_id: str) -> bool:
        """标记为已读"""
        if agent_id not in self.notifications:
            return False
        
        for notif in self.notifications[agent_id]:
            if notif.notification_id == notification_id:
                notif.read = True
                return True
        
        return False
    
    def mark_all_read(self, agent_id: str) -> int:
        """标记全部为已读"""
        if agent_id not in self.notifications:
            return 0
        
        count = 0
        for notif in self.notifications[agent_id]:
            if not notif.read:
                notif.read = True
                count += 1
        
        return count
    
    def get_unread(self, agent_id: str) -> List[Notification]:
        """获取未读通知"""
        if agent_id not in self.notifications:
            return []
        
        return [n for n in self.notifications[agent_id] if not n.read]
    
    def get_recent(self, agent_id: str, limit: int = 20) -> List[Notification]:
        """获取最近通知"""
        if agent_id not in self.notifications:
            return []
        
        return self.notifications[agent_id][-limit:]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total = sum(len(notifs) for notifs in self.notifications.values())
        unread = sum(
            len([n for n in notifs if not n.read])
            for notifs in self.notifications.values()
        )
        
        return {
            "total": total,
            "unread": unread,
            "agents_with_notifications": len(self.notifications),
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "recent": {
                agent_id: [n.to_dict() for n in self.get_recent(agent_id, 5)]
                for agent_id in list(self.notifications.keys())[:5]
            },
        }


# 单例
_notification_manager: Optional[NotificationManager] = None


def get_notification_manager() -> NotificationManager:
    """获取通知管理器单例"""
    global _notification_manager
    if _notification_manager is None:
        _notification_manager = NotificationManager()
    return _notification_manager


# 工厂函数
def create_notification_manager() -> NotificationManager:
    """创建通知管理器"""
    return NotificationManager()
