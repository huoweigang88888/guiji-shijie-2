#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
庆祝活动场景 - 硅基世界 2

庆祝成就、里程碑和特殊时刻，增强社区凝聚力。
"""

import asyncio
import random
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class CelebrationType(Enum):
    """庆祝类型"""
    ACHIEVEMENT_UNLOCKED = "achievement_unlocked"  # 成就解锁
    MILESTONE_REACHED = "milestone_reached"       # 里程碑达成
    BIRTHDAY = "birthday"                         # 生日
    ANNIVERSARY = "anniversary"                   # 周年纪念
    PROJECT_COMPLETED = "project_completed"       # 项目完成
    PROMOTION = "promotion"                       # 晋升
    SPECIAL_EVENT = "special_event"               # 特殊活动


class CelebrationScale(Enum):
    """庆祝规模"""
    SMALL = "small"      # 小型庆祝
    MEDIUM = "medium"    # 中型庆祝
    LARGE = "large"      # 大型庆祝
    GRAND = "grand"      # 盛大庆祝


@dataclass
class Celebration:
    """庆祝活动"""
    celebration_id: str
    title: str
    description: str
    celebration_type: CelebrationType
    scale: CelebrationScale
    participants: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    scheduled_at: Optional[float] = None
    completed_at: Optional[float] = None
    messages: List[str] = field(default_factory=list)
    gifts: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "celebration_id": self.celebration_id,
            "title": self.title,
            "description": self.description,
            "type": self.celebration_type.value,
            "scale": self.scale.value,
            "participants": self.participants,
            "created_at": self.created_at,
            "scheduled_at": self.scheduled_at,
            "completed_at": self.completed_at,
            "messages": self.messages,
            "gifts": self.gifts,
        }


class CelebrationManager:
    """庆祝活动管理器"""
    
    def __init__(self):
        """初始化庆祝活动管理器"""
        self.celebrations: Dict[str, Celebration] = {}
        self._celebration_counter = 0
        
        # 庆祝消息模板
        self.celebration_messages = {
            CelebrationType.ACHIEVEMENT_UNLOCKED: [
                "🏆 恭喜解锁新成就！",
                "🌟 太棒了！成就达成！",
                "🎯 目标达成，值得庆祝！",
            ],
            CelebrationType.MILESTONE_REACHED: [
                "🎊 里程碑达成！继续前进！",
                "📈 又迈出了一大步！",
                "🚀 新的里程碑，新的起点！",
            ],
            CelebrationType.BIRTHDAY: [
                "🎂 生日快乐！",
                "🎁 祝你度过美好的一天！",
                "🎉 生日快乐，愿你一切顺利！",
            ],
            CelebrationType.PROJECT_COMPLETED: [
                "🎉 项目完成！干得漂亮！",
                "✅ 任务完成，值得庆祝！",
                "🏅 又一个项目成功交付！",
            ],
        }
        
        # 庆祝礼物
        self.celebration_gifts = [
            "虚拟奖杯 🏆",
            "纪念徽章 🎖️",
            "定制头像框 🖼️",
            "特别称号 🌟",
            "庆祝烟花 🎆",
        ]
    
    async def create_celebration(
        self,
        title: str,
        description: str,
        celebration_type: CelebrationType,
        participants: List[str],
        scale: CelebrationScale = CelebrationScale.MEDIUM,
    ) -> Celebration:
        """
        创建庆祝活动
        
        Args:
            title: 庆祝标题
            description: 庆祝描述
            celebration_type: 庆祝类型
            participants: 参与者列表
            scale: 庆祝规模
            
        Returns:
            庆祝活动对象
        """
        self._celebration_counter += 1
        
        celebration = Celebration(
            celebration_id=f"celebration_{self._celebration_counter}",
            title=title,
            description=description,
            celebration_type=celebration_type,
            scale=scale,
            participants=participants,
        )
        
        self.celebrations[celebration.celebration_id] = celebration
        
        print(f"🎉 庆祝活动：{title}")
        print(f"   类型：{celebration_type.value}")
        print(f"   规模：{scale.value}")
        print(f"   参与者：{len(participants)} 人")
        
        return celebration
    
    async def add_message(self, celebration_id: str, agent_id: str, message: str) -> bool:
        """添加庆祝消息"""
        if celebration_id not in self.celebrations:
            return False
        
        celebration = self.celebrations[celebration_id]
        celebration.messages.append(f"[{agent_id}]: {message}")
        
        print(f"💬 {agent_id}: {message}")
        
        return True
    
    async def give_gift(self, celebration_id: str, giver: str, recipient: str, gift: Optional[str] = None) -> bool:
        """赠送礼物"""
        if celebration_id not in self.celebrations:
            return False
        
        celebration = self.celebrations[celebration_id]
        gift = gift or random.choice(self.celebration_gifts)
        celebration.gifts.append(f"{giver} → {recipient}: {gift}")
        
        print(f"🎁 {giver} 送给 {recipient}: {gift}")
        
        return True
    
    async def complete_celebration(self, celebration_id: str) -> bool:
        """完成庆祝活动"""
        if celebration_id not in self.celebrations:
            return False
        
        celebration = self.celebrations[celebration_id]
        celebration.completed_at = datetime.now().timestamp()
        
        print(f"✨ 庆祝活动结束：{celebration.title}")
        print(f"   消息数：{len(celebration.messages)}")
        print(f"   礼物数：{len(celebration.gifts)}")
        
        return True
    
    def get_active_celebrations(self) -> List[Celebration]:
        """获取活跃的庆祝活动"""
        return [
            c for c in self.celebrations.values()
            if c.completed_at is None
        ]
    
    def get_past_celebrations(self) -> List[Celebration]:
        """获取过去的庆祝活动"""
        return [c for c in self.celebrations.values() if c.completed_at is not None]
    
    def get_agent_celebrations(self, agent_id: str) -> List[Celebration]:
        """获取 Agent 参与的庆祝活动"""
        return [c for c in self.celebrations.values() if agent_id in c.participants]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total": len(self.celebrations),
            "active": len(self.get_active_celebrations()),
            "completed": len(self.get_past_celebrations()),
            "by_type": {
                t.value: len([c for c in self.celebrations.values() if c.celebration_type == t])
                for t in CelebrationType
            },
        }


# 单例
_celebration_manager: Optional[CelebrationManager] = None


def get_celebration_manager() -> CelebrationManager:
    """获取庆祝活动管理器单例"""
    global _celebration_manager
    if _celebration_manager is None:
        _celebration_manager = CelebrationManager()
    return _celebration_manager


def create_celebration_manager() -> CelebrationManager:
    """创建庆祝活动管理器"""
    return CelebrationManager()
