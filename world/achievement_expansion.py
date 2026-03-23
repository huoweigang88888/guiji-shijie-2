#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
成就扩展系统 - 硅基世界 2

提供更多成就类型和成就链。
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class AchievementCategory(Enum):
    """成就分类"""
    SOCIAL = "social"          # 社交
    WORK = "work"              # 工作
    KNOWLEDGE = "knowledge"    # 知识
    ECONOMY = "economy"        # 经济
    EXPLORATION = "exploration"  # 探索
    SPECIAL = "special"        # 特殊


@dataclass
class AchievementChain:
    """成就链"""
    chain_id: str
    name: str
    description: str
    category: AchievementCategory
    stages: List[Dict]  # [{name, description, requirement}]
    
    def to_dict(self) -> Dict:
        return {
            "chain_id": self.chain_id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "stages": self.stages,
        }


class AchievementExpansionManager:
    """成就扩展管理器"""
    
    def __init__(self):
        """初始化成就扩展管理器"""
        self.chains: Dict[str, AchievementChain] = {}
        self.agent_progress: Dict[str, Dict[str, int]] = {}  # agent_id -> {chain_id -> stage}
        
        # 注册成就链
        self._register_chains()
        
        print("🏆 成就扩展系统已初始化")
    
    def _register_chains(self):
        """注册成就链"""
        # 社交达人链
        self.create_chain(
            "social_master",
            "社交达人",
            "从陌生人到社交名流",
            AchievementCategory.SOCIAL,
            [
                {"name": "新朋友", "description": "添加第一个好友", "requirement": {"friends": 1}},
                {"name": "社交新手", "description": "拥有 5 个好友", "requirement": {"friends": 5}},
                {"name": "社交达人", "description": "拥有 20 个好友", "requirement": {"friends": 20}},
                {"name": "社交名流", "description": "拥有 50 个好友", "requirement": {"friends": 50}},
            ],
        )
        
        # 工作狂链
        self.create_chain(
            "workaholic",
            "工作狂",
            "从新手到工作狂",
            AchievementCategory.WORK,
            [
                {"name": "第一份工作", "description": "完成第一个任务", "requirement": {"tasks_completed": 1}},
                {"name": "勤劳工作者", "description": "完成 10 个任务", "requirement": {"tasks_completed": 10}},
                {"name": "工作狂", "description": "完成 50 个任务", "requirement": {"tasks_completed": 50}},
                {"name": "传奇工作者", "description": "完成 100 个任务", "requirement": {"tasks_completed": 100}},
            ],
        )
        
        # 知识渊博链
        self.create_chain(
            "knowledgeable",
            "知识渊博",
            "从学习者到智者",
            AchievementCategory.KNOWLEDGE,
            [
                {"name": "学习者", "description": "分享第一次知识", "requirement": {"knowledge_shared": 1}},
                {"name": "知识分享者", "description": "分享 10 次知识", "requirement": {"knowledge_shared": 10}},
                {"name": "学者", "description": "分享 50 次知识", "requirement": {"knowledge_shared": 50}},
                {"name": "智者", "description": "分享 100 次知识", "requirement": {"knowledge_shared": 100}},
            ],
        )
        
        # 富豪链
        self.create_chain(
            "wealthy",
            "富豪",
            "从贫穷到富有",
            AchievementCategory.ECONOMY,
            [
                {"name": "第一桶金", "description": "拥有 100 信用点", "requirement": {"credits": 100}},
                {"name": "小康", "description": "拥有 1000 信用点", "requirement": {"credits": 1000}},
                {"name": "富豪", "description": "拥有 10000 信用点", "requirement": {"credits": 10000}},
                {"name": "首富", "description": "拥有 100000 信用点", "requirement": {"credits": 100000}},
            ],
        )
        
        # 探索者链
        self.create_chain(
            "explorer",
            "探索者",
            "探索世界的每一个角落",
            AchievementCategory.EXPLORATION,
            [
                {"name": "新手探索者", "description": "访问 1 个区域", "requirement": {"regions_visited": 1}},
                {"name": "探索者", "description": "访问 4 个区域", "requirement": {"regions_visited": 4}},
                {"name": "资深探索者", "description": "访问 8 个区域", "requirement": {"regions_visited": 8}},
                {"name": "世界行者", "description": "访问所有区域 10 次", "requirement": {"regions_visited": 80}},
            ],
        )
    
    def create_chain(
        self,
        chain_id: str,
        name: str,
        description: str,
        category: AchievementCategory,
        stages: List[Dict],
    ) -> AchievementChain:
        """创建成就链"""
        chain = AchievementChain(
            chain_id=chain_id,
            name=name,
            description=description,
            category=category,
            stages=stages,
        )
        
        self.chains[chain_id] = chain
        
        return chain
    
    def check_progress(self, agent_id: str, stats: Dict) -> List[Dict]:
        """
        检查成就进度
        
        Args:
            agent_id: Agent ID
            stats: 统计数据
            
        Returns:
            新解锁的成就
        """
        unlocked = []
        
        if agent_id not in self.agent_progress:
            self.agent_progress[agent_id] = {}
        
        for chain_id, chain in self.chains.items():
            current_stage = self.agent_progress[agent_id].get(chain_id, 0)
            
            # 检查是否可以解锁下一阶段
            if current_stage < len(chain.stages):
                stage = chain.stages[current_stage]
                
                if self._check_requirements(stats, stage["requirement"]):
                    self.agent_progress[agent_id][chain_id] = current_stage + 1
                    
                    unlocked.append({
                        "chain_id": chain_id,
                        "chain_name": chain.name,
                        "stage": current_stage + 1,
                        "name": stage["name"],
                        "description": stage["description"],
                    })
        
        return unlocked
    
    def _check_requirements(self, stats: Dict, requirements: Dict) -> bool:
        """检查是否满足要求"""
        for key, value in requirements.items():
            if stats.get(key, 0) < value:
                return False
        
        return True
    
    def get_progress(self, agent_id: str) -> Dict:
        """获取成就进度"""
        if agent_id not in self.agent_progress:
            return {"chains": [], "total_unlocked": 0}
        
        progress = []
        total = 0
        
        for chain_id, stage in self.agent_progress[agent_id].items():
            if chain_id in self.chains:
                chain = self.chains[chain_id]
                progress.append({
                    "chain_id": chain_id,
                    "name": chain.name,
                    "current_stage": stage,
                    "total_stages": len(chain.stages),
                    "completed": stage >= len(chain.stages),
                })
                total += stage
        
        return {
            "chains": progress,
            "total_unlocked": total,
        }
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_chains": len(self.chains),
            "by_category": {
                cat.value: len([c for c in self.chains.values() if c.category == cat])
                for cat in AchievementCategory
            },
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "chains": [c.to_dict() for c in self.chains.values()],
        }


# 单例
_achievement_expansion_manager: Optional[AchievementExpansionManager] = None


def get_achievement_expansion_manager() -> AchievementExpansionManager:
    """获取成就扩展管理器单例"""
    global _achievement_expansion_manager
    if _achievement_expansion_manager is None:
        _achievement_expansion_manager = AchievementExpansionManager()
    return _achievement_expansion_manager


# 工厂函数
def create_achievement_expansion_manager() -> AchievementExpansionManager:
    """创建成就扩展管理器"""
    return AchievementExpansionManager()
