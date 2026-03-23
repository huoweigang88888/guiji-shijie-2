#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
成就展示墙 - 硅基世界 2

展示 Agent 的成就、荣誉、记录。
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class AchievementTier(Enum):
    """成就等级"""
    BRONZE = "bronze"      # 铜牌
    SILVER = "silver"      # 银牌
    GOLD = "gold"          # 金牌
    PLATINUM = "platinum"  # 白金
    DIAMOND = "diamond"    # 钻石


@dataclass
class AchievementRecord:
    """成就记录"""
    record_id: str
    agent_id: str
    achievement_name: str
    description: str
    tier: AchievementTier
    earned_at: float = field(default_factory=lambda: datetime.now().timestamp())
    display: bool = True  # 是否展示
    
    def to_dict(self) -> Dict:
        return {
            "record_id": self.record_id,
            "agent_id": self.agent_id,
            "achievement_name": self.achievement_name,
            "description": self.description,
            "tier": self.tier.value,
            "earned_at": self.earned_at,
            "display": self.display,
        }


class AchievementWallManager:
    """成就墙管理器"""
    
    def __init__(self):
        """初始化成就墙管理器"""
        self.records: Dict[str, List[AchievementRecord]] = {}  # agent_id -> [records]
        self._record_counter = 0
        
        print("🏆 成就墙系统已初始化")
    
    def add_achievement(
        self,
        agent_id: str,
        achievement_name: str,
        description: str,
        tier: AchievementTier = AchievementTier.BRONZE,
    ) -> AchievementRecord:
        """
        添加成就
        
        Args:
            agent_id: Agent ID
            achievement_name: 成就名称
            description: 描述
            tier: 等级
            
        Returns:
            成就记录
        """
        self._record_counter += 1
        
        record = AchievementRecord(
            record_id=f"ach_record_{self._record_counter}",
            agent_id=agent_id,
            achievement_name=achievement_name,
            description=description,
            tier=tier,
        )
        
        if agent_id not in self.records:
            self.records[agent_id] = []
        
        self.records[agent_id].append(record)
        
        tier_emoji = {
            AchievementTier.BRONZE: "🥉",
            AchievementTier.SILVER: "🥈",
            AchievementTier.GOLD: "🥇",
            AchievementTier.PLATINUM: "💎",
            AchievementTier.DIAMOND: "💠",
        }
        
        print(f"  {tier_emoji[tier]} {agent_id} 获得成就：{achievement_name}")
        
        return record
    
    def get_agent_achievements(self, agent_id: str, display_only: bool = True) -> List[AchievementRecord]:
        """获取 Agent 的成就"""
        if agent_id not in self.records:
            return []
        
        records = self.records[agent_id]
        
        if display_only:
            records = [r for r in records if r.display]
        
        return records
    
    def get_achievements_by_tier(self, tier: AchievementTier) -> List[AchievementRecord]:
        """获取特定等级的成就"""
        return [
            record
            for records in self.records.values()
            for record in records
            if record.tier == tier and record.display
        ]
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """获取成就排行榜"""
        leaderboard = []
        
        for agent_id, records in self.records.items():
            display_records = [r for r in records if r.display]
            
            # 计算分数（按等级加权）
            tier_scores = {
                AchievementTier.BRONZE: 1,
                AchievementTier.SILVER: 2,
                AchievementTier.GOLD: 3,
                AchievementTier.PLATINUM: 5,
                AchievementTier.DIAMOND: 10,
            }
            
            score = sum(tier_scores[r.tier] for r in display_records)
            
            leaderboard.append({
                "agent_id": agent_id,
                "achievements_count": len(display_records),
                "score": score,
                "gold_count": len([r for r in display_records if r.tier == AchievementTier.GOLD]),
            })
        
        leaderboard.sort(key=lambda x: x["score"], reverse=True)
        
        return leaderboard[:limit]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total = sum(len(records) for records in self.records.values())
        
        return {
            "total_achievements": total,
            "agents_with_achievements": len(self.records),
            "by_tier": {
                tier.value: len(self.get_achievements_by_tier(tier))
                for tier in AchievementTier
            },
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "leaderboard": self.get_leaderboard(5),
            "recent": [
                record.to_dict()
                for records in self.records.values()
                for record in records[-3:]
            ][-10:],
        }


# 单例
_achievement_wall_manager: Optional[AchievementWallManager] = None


def get_achievement_wall_manager() -> AchievementWallManager:
    """获取成就墙管理器单例"""
    global _achievement_wall_manager
    if _achievement_wall_manager is None:
        _achievement_wall_manager = AchievementWallManager()
    return _achievement_wall_manager


# 工厂函数
def create_achievement_wall_manager() -> AchievementWallManager:
    """创建成就墙管理器"""
    return AchievementWallManager()
