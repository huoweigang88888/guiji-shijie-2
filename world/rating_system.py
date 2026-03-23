#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
评价系统 - 硅基世界 2

让 Agent 可以互相评价，形成声誉系统。
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class RatingType(Enum):
    """评价类型"""
    WORK = "work"          # 工作表现
    COLLABORATION = "collaboration"  # 协作能力
    COMMUNICATION = "communication"  # 沟通能力
    HELPfulness = "helpfulness"  # 乐于助人
    GENERAL = "general"    # 综合评价


@dataclass
class Rating:
    """评价"""
    rating_id: str
    from_agent: str
    to_agent: str
    rating_type: RatingType
    score: int  # 1-5
    comment: str
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def to_dict(self) -> Dict:
        return {
            "rating_id": self.rating_id,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "type": self.rating_type.value,
            "score": self.score,
            "comment": self.comment,
            "created_at": self.created_at,
        }


class RatingManager:
    """评价管理器"""
    
    def __init__(self):
        """初始化评价管理器"""
        self.ratings: Dict[str, List[Rating]] = {}  # to_agent -> [ratings]
        self._rating_counter = 0
        
        # Agent 声誉分数
        self.reputation: Dict[str, float] = {}
        
        print("⭐ 评价系统已初始化")
    
    def rate(
        self,
        from_agent: str,
        to_agent: str,
        rating_type: RatingType,
        score: int,
        comment: str = "",
    ) -> Rating:
        """
        评价
        
        Args:
            from_agent: 评价者
            to_agent: 被评价者
            rating_type: 评价类型
            score: 分数 (1-5)
            comment: 评论
            
        Returns:
            评价对象
        """
        if score < 1 or score > 5:
            raise ValueError("分数必须在 1-5 之间")
        
        if from_agent == to_agent:
            raise ValueError("不能评价自己")
        
        self._rating_counter += 1
        
        rating = Rating(
            rating_id=f"rating_{self._rating_counter}",
            from_agent=from_agent,
            to_agent=to_agent,
            rating_type=rating_type,
            score=score,
            comment=comment,
        )
        
        if to_agent not in self.ratings:
            self.ratings[to_agent] = []
        
        self.ratings[to_agent].append(rating)
        
        # 更新声誉
        self._update_reputation(to_agent)
        
        emoji = "⭐" * score
        print(f"  {emoji} {from_agent} 评价 {to_agent}: {score}/5 - {comment[:30]}")
        
        return rating
    
    def _update_reputation(self, agent_id: str):
        """更新声誉分数"""
        if agent_id not in self.ratings:
            self.reputation[agent_id] = 50.0  # 初始声誉
            return
        
        ratings = self.ratings[agent_id]
        
        if not ratings:
            return
        
        # 计算平均分数
        avg_score = sum(r.score for r in ratings) / len(ratings)
        
        # 转换为 0-100 的声誉分数
        # 3 分=50, 5 分=100, 1 分=0
        self.reputation[agent_id] = (avg_score - 1) / 4 * 100
    
    def get_reputation(self, agent_id: str) -> float:
        """获取声誉分数"""
        return self.reputation.get(agent_id, 50.0)
    
    def get_ratings(self, agent_id: str) -> List[Rating]:
        """获取评价"""
        return self.ratings.get(agent_id, [])
    
    def get_average_score(self, agent_id: str) -> float:
        """获取平均分数"""
        ratings = self.get_ratings(agent_id)
        
        if not ratings:
            return 0.0
        
        return sum(r.score for r in ratings) / len(ratings)
    
    def get_ratings_by_type(self, agent_id: str, rating_type: RatingType) -> List[Rating]:
        """获取特定类型的评价"""
        return [
            r for r in self.get_ratings(agent_id)
            if r.rating_type == rating_type
        ]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total_ratings = sum(len(ratings) for ratings in self.ratings.values())
        
        return {
            "total_ratings": total_ratings,
            "agents_rated": len(self.ratings),
            "average_reputation": sum(self.reputation.values()) / len(self.reputation) if self.reputation else 50.0,
        }
    
    def get_leaderboard(self) -> List[Dict]:
        """获取声誉排行榜"""
        leaderboard = [
            {"agent_id": agent_id, "reputation": rep}
            for agent_id, rep in self.reputation.items()
        ]
        
        leaderboard.sort(key=lambda x: x["reputation"], reverse=True)
        
        return leaderboard
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "leaderboard": self.get_leaderboard(),
            "recent_ratings": [
                rating.to_dict()
                for ratings in self.ratings.values()
                for rating in ratings[-3:]  # 每个 Agent 最近 3 个评价
            ][-10:],  # 总共最近 10 个
        }


# 单例
_rating_manager: Optional[RatingManager] = None


def get_rating_manager() -> RatingManager:
    """获取评价管理器单例"""
    global _rating_manager
    if _rating_manager is None:
        _rating_manager = RatingManager()
    return _rating_manager


# 工厂函数
def create_rating_manager() -> RatingManager:
    """创建评价管理器"""
    return RatingManager()
