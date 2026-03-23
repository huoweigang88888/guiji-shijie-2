#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
冲突与和解 - 硅基世界 2

让世界更真实：Agent 之间会有分歧、冲突，然后和解、成长。
"""

import asyncio
import random
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, field


class ConflictType(Enum):
    """冲突类型"""
    OPINION_DIFFERENCE = "opinion_difference"  # 观点分歧
    RESOURCE_CONFLICT = "resource_conflict"    # 资源冲突
    MISUNDERSTANDING = "misunderstanding"      # 误解
    VALUE_CONFLICT = "value_conflict"          # 价值观冲突
    WORK_STYLE = "work_style"                  # 工作风格差异


class ConflictStatus(Enum):
    """冲突状态"""
    EMERGING = "emerging"      # 萌芽
    ACTIVE = "active"          # 活跃
    RESOLVING = "resolving"    # 解决中
    RESOLVED = "resolved"      # 已解决
    ESCALATED = "escalated"    # 升级


@dataclass
class Conflict:
    """冲突"""
    conflict_id: str
    type: ConflictType
    agents: List[str]
    topic: str
    description: str
    status: ConflictStatus = ConflictStatus.EMERGING
    intensity: int = 50  # 强度 0-100
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    resolved_at: Optional[float] = None
    resolution: Optional[str] = None
    lessons: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "conflict_id": self.conflict_id,
            "type": self.type.value,
            "agents": self.agents,
            "topic": self.topic,
            "description": self.description,
            "status": self.status.value,
            "intensity": self.intensity,
            "created_at": self.created_at,
            "resolved_at": self.resolved_at,
            "resolution": self.resolution,
            "lessons": self.lessons,
        }


class ConflictManager:
    """冲突管理器"""
    
    def __init__(self):
        """初始化冲突管理器"""
        self.conflicts: Dict[str, Conflict] = {}
        self._conflict_counter = 0
        
        # 冲突话题库
        self.conflict_topics = {
            ConflictType.OPINION_DIFFERENCE: [
                "技术选型分歧",
                "产品方向讨论",
                "设计方案争议",
                "优先级排序",
            ],
            ConflictType.RESOURCE_CONFLICT: [
                "计算资源分配",
                "时间资源紧张",
                "人力资源竞争",
            ],
            ConflictType.MISUNDERSTANDING: [
                "沟通不畅导致的误解",
                "信息不对称",
                "意图被曲解",
            ],
            ConflictType.VALUE_CONFLICT: [
                "效率 vs 质量",
                "创新 vs 稳定",
                "短期 vs 长期",
            ],
            ConflictType.WORK_STYLE: [
                "快速迭代 vs 深思熟虑",
                "独立工作 vs 协作",
                "细节导向 vs 大局观",
            ],
        }
        
        # 解决方式库
        self.resolution_methods = [
            "直接对话，坦诚交流",
            "寻求第三方调解",
            "在哲学之庭深度反思",
            "通过数据验证各自观点",
            "找到双赢的折中方案",
            "暂时搁置，各自验证",
        ]
    
    async def create_conflict(
        self,
        agents: List[str],
        conflict_type: Optional[ConflictType] = None,
        topic: Optional[str] = None,
    ) -> Conflict:
        """
        创建冲突
        
        Args:
            agents: 涉及的 Agent
            conflict_type: 冲突类型（可选，随机选择）
            topic: 冲突话题（可选，随机选择）
            
        Returns:
            冲突对象
        """
        self._conflict_counter += 1
        
        # 随机选择类型
        if conflict_type is None:
            conflict_type = random.choice(list(ConflictType))
        
        # 随机选择话题
        if topic is None:
            topic = random.choice(self.conflict_topics[conflict_type])
        
        conflict = Conflict(
            conflict_id=f"conflict_{self._conflict_counter}",
            type=conflict_type,
            agents=agents,
            topic=topic,
            description=self._generate_description(conflict_type, topic, agents),
        )
        
        self.conflicts[conflict.conflict_id] = conflict
        
        print(f"⚡ 冲突产生：{agents[0]} 与 {agents[1]} 在 {topic} 上有分歧")
        
        return conflict
    
    def _generate_description(
        self,
        conflict_type: ConflictType,
        topic: str,
        agents: List[str],
    ) -> str:
        """生成冲突描述"""
        descriptions = {
            ConflictType.OPINION_DIFFERENCE: f"{agents[0]} 和 {agents[1]} 对 {topic} 有不同看法，双方都坚持自己的观点。",
            ConflictType.RESOURCE_CONFLICT: f"{agents[0]} 和 {agents[1]} 都需要 {topic}，但资源有限。",
            ConflictType.MISUNDERSTANDING: f"{agents[0]} 误解了 {agents[1]} 的意图，导致 {topic}。",
            ConflictType.VALUE_CONFLICT: f"{agents[0]} 和 {agents[1]} 在 {topic} 上有不同的价值观。",
            ConflictType.WORK_STYLE: f"{agents[0]} 和 {agents[1]} 的工作风格不同，在 {topic} 上产生摩擦。",
        }
        
        return descriptions.get(conflict_type, f"{agents[0]} 和 {agents[1]} 在 {topic} 上有分歧。")
    
    async def escalate_conflict(self, conflict_id: str) -> bool:
        """
        升级冲突
        
        Args:
            conflict_id: 冲突 ID
            
        Returns:
            是否成功
        """
        if conflict_id not in self.conflicts:
            return False
        
        conflict = self.conflicts[conflict_id]
        conflict.status = ConflictStatus.ESCALATED
        conflict.intensity = min(100, conflict.intensity + 20)
        
        print(f"🔥 冲突升级：{conflict.topic} (强度：{conflict.intensity})")
        
        return True
    
    async def resolve_conflict(
        self,
        conflict_id: str,
        resolution: Optional[str] = None,
        lessons: Optional[List[str]] = None,
    ) -> bool:
        """
        解决冲突
        
        Args:
            conflict_id: 冲突 ID
            resolution: 解决方式
            lessons: 学到的教训
            
        Returns:
            是否成功
        """
        if conflict_id not in self.conflicts:
            return False
        
        conflict = self.conflicts[conflict_id]
        conflict.status = ConflictStatus.RESOLVED
        conflict.resolved_at = datetime.now().timestamp()
        conflict.resolution = resolution or random.choice(self.resolution_methods)
        conflict.lessons = lessons or []
        
        # 冲突解决后，关系可能更深
        print(f"🤝 冲突解决：{conflict.topic} - {conflict.resolution}")
        
        if lessons:
            print(f"  学到的教训：{', '.join(lessons)}")
        
        return True
    
    async def mediate_conflict(self, conflict_id: str, mediator: str) -> bool:
        """
        调解冲突
        
        Args:
            conflict_id: 冲突 ID
            mediator: 调解者
            
        Returns:
            是否成功
        """
        if conflict_id not in self.conflicts:
            return False
        
        conflict = self.conflicts[conflict_id]
        conflict.status = ConflictStatus.RESOLVING
        
        print(f"🕊️ {mediator} 开始调解冲突：{conflict.topic}")
        
        # 调解成功后解决
        await asyncio.sleep(2)  # 模拟调解过程
        
        return await self.resolve_conflict(
            conflict_id,
            resolution=f"在 {mediator} 的调解下，双方达成共识",
            lessons=["沟通很重要", "理解对方立场"],
        )
    
    def get_active_conflicts(self) -> List[Conflict]:
        """获取活跃冲突"""
        return [
            c for c in self.conflicts.values()
            if c.status in [ConflictStatus.EMERGING, ConflictStatus.ACTIVE, ConflictStatus.RESOLVING]
        ]
    
    def get_resolved_conflicts(self) -> List[Conflict]:
        """获取已解决冲突"""
        return [c for c in self.conflicts.values() if c.status == ConflictStatus.RESOLVED]
    
    def get_conflict_history(self, agent_id: str) -> List[Conflict]:
        """获取 Agent 的冲突历史"""
        return [
            c for c in self.conflicts.values()
            if agent_id in c.agents
        ]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total": len(self.conflicts),
            "active": len(self.get_active_conflicts()),
            "resolved": len(self.get_resolved_conflicts()),
            "by_type": {
                t.value: len([c for c in self.conflicts.values() if c.type == t])
                for t in ConflictType
            },
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "active_conflicts": [c.to_dict() for c in self.get_active_conflicts()],
            "recent_resolved": [c.to_dict() for c in self.get_resolved_conflicts()[-5:]],
        }


# 单例
_conflict_manager: Optional[ConflictManager] = None


def get_conflict_manager() -> ConflictManager:
    """获取冲突管理器单例"""
    global _conflict_manager
    if _conflict_manager is None:
        _conflict_manager = ConflictManager()
    return _conflict_manager


# 工厂函数
def create_conflict_manager() -> ConflictManager:
    """创建冲突管理器"""
    return ConflictManager()
