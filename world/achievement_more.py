#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
成就更多扩展 - 硅基世界 2

提供更多特殊成就和隐藏成就。
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class AchievementRarity(Enum):
    """成就稀有度"""
    COMMON = "common"      # 普通
    UNCOMMON = "uncommon"  # 少见
    RARE = "rare"          # 稀有
    EPIC = "epic"          # 史诗
    LEGENDARY = "legendary"  # 传说
    HIDDEN = "hidden"      # 隐藏


@dataclass
class SpecialAchievement:
    """特殊成就"""
    achievement_id: str
    name: str
    description: str
    rarity: AchievementRarity
    requirement: Dict
    reward: Dict
    is_secret: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "achievement_id": self.achievement_id,
            "name": self.name,
            "description": self.description if not self.is_secret else "???",
            "rarity": self.rarity.value,
            "reward": self.reward,
        }


class AchievementMoreManager:
    """成就更多管理器"""
    
    def __init__(self):
        """初始化成就更多管理器"""
        self.achievements: Dict[str, SpecialAchievement] = {}
        self.agent_achievements: Dict[str, List[str]] = {}  # agent_id -> [achievement_ids]
        
        # 注册特殊成就
        self._register_achievements()
        
        print("🏆 成就更多扩展已初始化")
    
    def _register_achievements(self):
        """注册特殊成就"""
        # 时间相关成就
        self.register(
            "early_bird",
            "早起鸟",
            "在世界时间早晨 6 点前活跃",
            AchievementRarity.UNCOMMON,
            {"active_hour": {"<": 6}},
            {"credits": 50},
        )
        
        self.register(
            "night_owl",
            "夜猫子",
            "在世界时间凌晨 2 点后活跃",
            AchievementRarity.UNCOMMON,
            {"active_hour": {">": 2}},
            {"credits": 50},
        )
        
        # 社交相关成就
        self.register(
            "party_animal",
            "派对达人",
            "参与 10 次庆祝活动",
            AchievementRarity.RARE,
            {"celebrations_attended": 10},
            {"credits": 100, "reputation": 10},
        )
        
        self.register(
            "matchmaker",
            "红娘",
            "促成 5 对好友关系",
            AchievementRarity.EPIC,
            {"friendships_facilitated": 5},
            {"credits": 200, "achievement": "红娘"},
        )
        
        # 经济相关成就
        self.register(
            "big_spender",
            "挥霍者",
            "单次消费超过 1000 信用点",
            AchievementRarity.RARE,
            {"single_purchase": {">": 1000}},
            {"achievement": "挥霍者"},
        )
        
        self.register(
            "investor",
            "投资家",
            "累计收入超过 10000 信用点",
            AchievementRarity.EPIC,
            {"total_income": {">": 10000}},
            {"credits": 500, "achievement": "投资家"},
        )
        
        # 隐藏成就
        self.register(
            "secret_finder",
            "秘密发现者",
            "???",
            AchievementRarity.HIDDEN,
            {"secret_found": True},
            {"credits": 1000, "achievement": "秘密发现者"},
            is_secret=True,
        )
        
        self.register(
            "legend",
            "传奇",
            "???",
            AchievementRarity.LEGENDARY,
            {"all_achievements": True},
            {"credits": 10000, "achievement": "传奇"},
            is_secret=True,
        )
        
        # 连续成就
        self.register(
            "consistent",
            "持之以恒",
            "连续 7 天登录",
            AchievementRarity.RARE,
            {"consecutive_days": 7},
            {"credits": 150},
        )
        
        self.register(
            "dedicated",
            "忠诚",
            "连续 30 天登录",
            AchievementRarity.EPIC,
            {"consecutive_days": 30},
            {"credits": 500, "achievement": "忠诚"},
        )
        
        self.register(
            "immortal",
            "不朽",
            "连续 365 天登录",
            AchievementRarity.LEGENDARY,
            {"consecutive_days": 365},
            {"credits": 10000, "achievement": "不朽"},
        )
        
        # 技能相关成就
        self.register(
            "polymath",
            "博学家",
            "拥有 10 个满级技能",
            AchievementRarity.LEGENDARY,
            {"max_level_skills": 10},
            {"credits": 5000, "achievement": "博学家"},
        )
        
        # 探索相关成就
        self.register(
            "tourist",
            "游客",
            "访问所有 8 个区域",
            AchievementRarity.UNCOMMON,
            {"regions_visited": 8},
            {"credits": 80},
        )
        
        self.register(
            "world_traveler",
            "世界旅行者",
            "访问所有区域各 10 次",
            AchievementRarity.EPIC,
            {"total_region_visits": 80},
            {"credits": 500, "achievement": "世界旅行者"},
        )
    
    def register(
        self,
        achievement_id: str,
        name: str,
        description: str,
        rarity: AchievementRarity,
        requirement: Dict,
        reward: Dict,
        is_secret: bool = False,
    ) -> SpecialAchievement:
        """注册成就"""
        achievement = SpecialAchievement(
            achievement_id=achievement_id,
            name=name,
            description=description,
            rarity=rarity,
            requirement=requirement,
            reward=reward,
            is_secret=is_secret,
        )
        
        self.achievements[achievement_id] = achievement
        
        return achievement
    
    def check_achievements(self, agent_id: str, stats: Dict) -> List[Dict]:
        """
        检查成就
        
        Args:
            agent_id: Agent ID
            stats: 统计数据
            
        Returns:
            新解锁的成就
        """
        unlocked = []
        
        if agent_id not in self.agent_achievements:
            self.agent_achievements[agent_id] = []
        
        for achievement_id, achievement in self.achievements.items():
            if achievement_id in self.agent_achievements[agent_id]:
                continue
            
            if self._check_requirement(stats, achievement.requirement):
                self.agent_achievements[agent_id].append(achievement_id)
                
                unlocked.append({
                    "achievement_id": achievement_id,
                    "name": achievement.name,
                    "description": achievement.description,
                    "rarity": achievement.rarity.value,
                    "reward": achievement.reward,
                })
        
        return unlocked
    
    def _check_requirement(self, stats: Dict, requirement: Dict) -> bool:
        """检查是否满足要求"""
        for key, condition in requirement.items():
            if isinstance(condition, dict):
                for op, value in condition.items():
                    stat_value = stats.get(key, 0)
                    
                    if op == ">" and not (stat_value > value):
                        return False
                    elif op == ">=" and not (stat_value >= value):
                        return False
                    elif op == "<" and not (stat_value < value):
                        return False
                    elif op == "<=" and not (stat_value <= value):
                        return False
                    elif op == "==" and not (stat_value == value):
                        return False
            else:
                if stats.get(key, 0) < condition:
                    return False
        
        return True
    
    def get_agent_achievements(self, agent_id: str) -> List[Dict]:
        """获取 Agent 的成就"""
        if agent_id not in self.agent_achievements:
            return []
        
        return [
            self.achievements[aid].to_dict()
            for aid in self.agent_achievements[agent_id]
            if aid in self.achievements
        ]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_achievements": len(self.achievements),
            "by_rarity": {
                r.value: len([a for a in self.achievements.values() if a.rarity == r])
                for r in AchievementRarity
            },
            "hidden_count": len([a for a in self.achievements.values() if a.is_secret]),
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "achievements": [a.to_dict() for a in self.achievements.values()],
        }


# 单例
_achievement_more_manager: Optional[AchievementMoreManager] = None


def get_achievement_more_manager() -> AchievementMoreManager:
    """获取成就更多管理器单例"""
    global _achievement_more_manager
    if _achievement_more_manager is None:
        _achievement_more_manager = AchievementMoreManager()
    return _achievement_more_manager


# 工厂函数
def create_achievement_more_manager() -> AchievementMoreManager:
    """创建成就更多管理器"""
    return AchievementMoreManager()
