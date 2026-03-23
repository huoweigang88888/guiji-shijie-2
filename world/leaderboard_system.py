#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
排行榜系统 - 硅基世界 2

综合各类排行榜，展示 Agent 的各方面成就。
"""

from typing import Dict, List, Optional, Callable
from dataclasses import dataclass


@dataclass
class LeaderboardEntry:
    """排行榜条目"""
    rank: int
    agent_id: str
    value: float
    change: int = 0  # 排名变化 (+上升，-下降，0 不变)
    
    def to_dict(self) -> Dict:
        return {
            "rank": self.rank,
            "agent_id": self.agent_id,
            "value": self.value,
            "change": self.change,
        }


class LeaderboardManager:
    """排行榜管理器"""
    
    def __init__(self):
        """初始化排行榜管理器"""
        self.leaderboards: Dict[str, List[Dict]] = {}
        self.previous_ranks: Dict[str, Dict[str, int]] = {}  # leaderboard_id -> {agent_id -> rank}
        
        print("🏆 排行榜系统已初始化")
    
    def create_leaderboard(
        self,
        leaderboard_id: str,
        name: str,
        data_getter: Callable[[], List[Dict]],
        value_key: str = "value",
    ):
        """
        创建排行榜
        
        Args:
            leaderboard_id: 排行榜 ID
            name: 名称
            data_getter: 数据获取函数
            value_key: 排序字段
        """
        self.leaderboards[leaderboard_id] = {
            "id": leaderboard_id,
            "name": name,
            "data_getter": data_getter,
            "value_key": value_key,
        }
        
        print(f"  📊 创建排行榜：{name}")
    
    def get_leaderboard(self, leaderboard_id: str, limit: int = 10) -> List[LeaderboardEntry]:
        """
        获取排行榜
        
        Args:
            leaderboard_id: 排行榜 ID
            limit: 返回数量
            
        Returns:
            排行榜条目列表
        """
        if leaderboard_id not in self.leaderboards:
            return []
        
        lb = self.leaderboards[leaderboard_id]
        data = lb["data_getter"]()
        
        # 排序
        data.sort(key=lambda x: x.get(lb["value_key"], 0), reverse=True)
        
        # 获取上次排名
        prev_ranks = self.previous_ranks.get(leaderboard_id, {})
        
        # 创建条目
        entries = []
        for i, item in enumerate(data[:limit]):
            agent_id = item.get("agent_id", "")
            value = item.get(lb["value_key"], 0)
            
            prev_rank = prev_ranks.get(agent_id, 0)
            current_rank = i + 1
            change = prev_rank - current_rank if prev_rank > 0 else 0
            
            entries.append(LeaderboardEntry(
                rank=current_rank,
                agent_id=agent_id,
                value=value,
                change=change,
            ))
        
        # 保存当前排名
        self.previous_ranks[leaderboard_id] = {
            entry.agent_id: entry.rank for entry in entries
        }
        
        return entries
    
    def get_all_leaderboards(self, limit: int = 10) -> Dict[str, List[LeaderboardEntry]]:
        """获取所有排行榜"""
        return {
            lb_id: self.get_leaderboard(lb_id, limit)
            for lb_id in self.leaderboards
        }
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_leaderboards": len(self.leaderboards),
            "leaderboards": list(self.leaderboards.keys()),
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "leaderboards": {
                lb_id: [e.to_dict() for e in self.get_leaderboard(lb_id, 5)]
                for lb_id in self.leaderboards
            },
        }


# 单例
_leaderboard_manager: Optional[LeaderboardManager] = None


def get_leaderboard_manager() -> LeaderboardManager:
    """获取排行榜管理器单例"""
    global _leaderboard_manager
    if _leaderboard_manager is None:
        _leaderboard_manager = LeaderboardManager()
    return _leaderboard_manager


# 工厂函数
def create_leaderboard_manager() -> LeaderboardManager:
    """创建排行榜管理器"""
    return LeaderboardManager()
