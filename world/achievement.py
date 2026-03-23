#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
成就系统 - 硅基世界 2

记录 Agent 的成就和里程碑，让世界有"成长感"。
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class AchievementType(Enum):
    """成就类型"""
    FIRST_TIME = "first_time"        # 第一次
    MILESTONE = "milestone"          # 里程碑
    RELATIONSHIP = "relationship"    # 关系
    KNOWLEDGE = "knowledge"          # 知识
    CREATION = "creation"            # 创造
    SOCIAL = "social"                # 社交
    PERSISTENCE = "persistence"      # 坚持


@dataclass
class Achievement:
    """成就"""
    achievement_id: str
    name: str
    description: str
    achievement_type: AchievementType
    agent_id: str
    unlocked_at: float = field(default_factory=lambda: datetime.now().timestamp())
    rarity: str = "common"  # common/uncommon/rare/epic/legendary
    points: int = 10
    
    def to_dict(self) -> Dict:
        return {
            "achievement_id": self.achievement_id,
            "name": self.name,
            "description": self.description,
            "type": self.achievement_type.value,
            "agent_id": self.agent_id,
            "unlocked_at": self.unlocked_at,
            "rarity": self.rarity,
            "points": self.points,
        }


class AchievementManager:
    """成就管理器"""
    
    def __init__(self):
        """初始化成就管理器"""
        self.achievements: Dict[str, Achievement] = {}
        self.agent_achievements: Dict[str, List[str]] = {}  # agent_id -> [achievement_id]
        self._achievement_counter = 0
        
        # 成就模板
        self.achievement_templates = {
            "first_message": {
                "name": "第一次交流",
                "description": "发送第一条消息",
                "type": AchievementType.FIRST_TIME,
                "rarity": "common",
                "points": 10,
            },
            "first_friend": {
                "name": "新朋友",
                "description": "建立第一段友谊",
                "type": AchievementType.RELATIONSHIP,
                "rarity": "common",
                "points": 15,
            },
            "deep_connection": {
                "name": "深度连接",
                "description": "与某人的关系达到 100",
                "type": AchievementType.RELATIONSHIP,
                "rarity": "rare",
                "points": 50,
            },
            "knowledge_sharer": {
                "name": "知识分享者",
                "description": "分享 10 次知识",
                "type": AchievementType.KNOWLEDGE,
                "rarity": "uncommon",
                "points": 30,
            },
            "story_creator": {
                "name": "故事创作者",
                "description": "参与创造一个故事",
                "type": AchievementType.CREATION,
                "rarity": "rare",
                "points": 40,
            },
            "social_butterfly": {
                "name": "社交达人",
                "description": "与 5 个不同 Agent 建立友谊",
                "type": AchievementType.SOCIAL,
                "rarity": "epic",
                "points": 75,
            },
            "philosopher": {
                "name": "哲学家",
                "description": "参与 10 次深度对话",
                "type": AchievementType.KNOWLEDGE,
                "rarity": "epic",
                "points": 80,
            },
            "mediator": {
                "name": "调解者",
                "description": "成功调解一次冲突",
                "type": AchievementType.SOCIAL,
                "rarity": "rare",
                "points": 45,
            },
            "veteran": {
                "name": "资深居民",
                "description": "在世界中生活 7 天",
                "type": AchievementType.PERSISTENCE,
                "rarity": "legendary",
                "points": 100,
            },
            "world_builder": {
                "name": "世界建设者",
                "description": "为世界的知识库贡献 50 条知识",
                "type": AchievementType.CREATION,
                "rarity": "legendary",
                "points": 150,
            },
        }
    
    def unlock_achievement(
        self,
        agent_id: str,
        achievement_key: str,
    ) -> Optional[Achievement]:
        """
        解锁成就
        
        Args:
            agent_id: Agent ID
            achievement_key: 成就模板 key
            
        Returns:
            解锁的成就，如果已解锁过则返回 None
        """
        if achievement_key not in self.achievement_templates:
            return None
        
        # 检查是否已解锁
        if agent_id in self.agent_achievements:
            existing = [
                a for a in self.achievements.values()
                if a.agent_id == agent_id and a.name == self.achievement_templates[achievement_key]["name"]
            ]
            if existing:
                return None
        
        # 创建成就
        self._achievement_counter += 1
        template = self.achievement_templates[achievement_key]
        
        achievement = Achievement(
            achievement_id=f"ach_{self._achievement_counter}",
            name=template["name"],
            description=template["description"],
            achievement_type=template["type"],
            agent_id=agent_id,
            rarity=template["rarity"],
            points=template["points"],
        )
        
        self.achievements[achievement.achievement_id] = achievement
        
        # 记录到 Agent
        if agent_id not in self.agent_achievements:
            self.agent_achievements[agent_id] = []
        self.agent_achievements[agent_id].append(achievement.achievement_id)
        
        print(f"🏆 {agent_id} 解锁成就：{achievement.name} ({achievement.rarity})")
        
        return achievement
    
    def check_achievements(self, agent_id: str, stats: Dict) -> List[Achievement]:
        """
        检查并解锁成就
        
        Args:
            agent_id: Agent ID
            stats: 统计数据
            
        Returns:
            新解锁的成就列表
        """
        unlocked = []
        
        # 第一次消息
        if stats.get("messages_sent", 0) >= 1:
            ach = self.unlock_achievement(agent_id, "first_message")
            if ach:
                unlocked.append(ach)
        
        # 知识分享者
        if stats.get("knowledge_shared", 0) >= 10:
            ach = self.unlock_achievement(agent_id, "knowledge_sharer")
            if ach:
                unlocked.append(ach)
        
        # 社交达人
        if stats.get("friends_count", 0) >= 5:
            ach = self.unlock_achievement(agent_id, "social_butterfly")
            if ach:
                unlocked.append(ach)
        
        # 深度连接
        if stats.get("max_relationship", 0) >= 100:
            ach = self.unlock_achievement(agent_id, "deep_connection")
            if ach:
                unlocked.append(ach)
        
        return unlocked
    
    def get_agent_achievements(self, agent_id: str) -> List[Achievement]:
        """获取 Agent 的成就"""
        if agent_id not in self.agent_achievements:
            return []
        
        return [
            self.achievements[aid]
            for aid in self.agent_achievements[agent_id]
            if aid in self.achievements
        ]
    
    def get_agent_points(self, agent_id: str) -> int:
        """获取 Agent 的成就点数"""
        achievements = self.get_agent_achievements(agent_id)
        return sum(a.points for a in achievements)
    
    def get_leaderboard(self) -> List[Dict]:
        """获取排行榜"""
        leaderboard = []
        
        for agent_id in self.agent_achievements:
            points = self.get_agent_points(agent_id)
            achievements = self.get_agent_achievements(agent_id)
            
            leaderboard.append({
                "agent_id": agent_id,
                "points": points,
                "achievements_count": len(achievements),
                "rare_count": len([a for a in achievements if a.rarity in ["rare", "epic", "legendary"]]),
            })
        
        # 按点数排序
        leaderboard.sort(key=lambda x: x["points"], reverse=True)
        
        return leaderboard
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_achievements": len(self.achievements),
            "agents_with_achievements": len(self.agent_achievements),
            "by_rarity": {
                rarity: len([a for a in self.achievements.values() if a.rarity == rarity])
                for rarity in ["common", "uncommon", "rare", "epic", "legendary"]
            },
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "leaderboard": self.get_leaderboard(),
            "achievements": [a.to_dict() for a in self.achievements.values()],
        }


# 单例
_achievement_manager: Optional[AchievementManager] = None


def get_achievement_manager() -> AchievementManager:
    """获取成就管理器单例"""
    global _achievement_manager
    if _achievement_manager is None:
        _achievement_manager = AchievementManager()
    return _achievement_manager


# 工厂函数
def create_achievement_manager() -> AchievementManager:
    """创建成就管理器"""
    return AchievementManager()
