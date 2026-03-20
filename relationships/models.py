#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关系系统 - 硅基世界 2

硅基关系模型：
- 工作关系：同事、上下级、合作伙伴
- 社交关系：朋友、挚友、恋人
- 兴趣关系：兴趣小组、俱乐部

关系可以建立、深化、修复、疏远
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum


class RelationshipType(Enum):
    """关系类型"""
    # 工作关系
    COLLEAGUE = "colleague"           # 同事
    SUPERIOR_SUBORDINATE = "superior_subordinate"  # 上下级
    PARTNER = "partner"               # 合作伙伴
    
    # 社交关系
    ACQUAINTANCE = "acquaintance"     # 认识
    FRIEND = "friend"                 # 朋友
    CLOSE_FRIEND = "close_friend"     # 挚友
    MENTOR = "mentor"                 # 导师
    MENTEE = "mentee"                 # 学生
    
    # 特殊关系
    RIVAL = "rival"                   # 对手
    CONFLICT = "conflict"             # 冲突中


@dataclass
class Relationship:
    """关系"""
    agent_a: str
    agent_b: str
    type: RelationshipType
    strength: float = 0.0    # 关系强度 0-100
    trust: float = 0.0       # 信任度 0-100
    
    # 关系历史
    history: List[Dict] = field(default_factory=list)
    
    # 建立时间
    established_at: datetime = field(default_factory=datetime.now)
    
    # 最后互动时间
    last_interaction: datetime = field(default_factory=datetime.now)
    
    def add_interaction(self, event: Dict):
        """添加互动记录"""
        self.history.append({
            **event,
            "timestamp": datetime.now().isoformat(),
        })
        self.last_interaction = datetime.now()
    
    def deepen(self, amount: float = 5.0):
        """深化关系"""
        self.strength = min(100, self.strength + amount)
        self.trust = min(100, self.trust + amount * 0.5)
    
    def damage(self, amount: float = 10.0):
        """损害关系"""
        self.strength = max(0, self.strength - amount)
        self.trust = max(0, self.trust - amount)
    
    def repair(self, amount: float = 5.0):
        """修复关系"""
        self.strength = min(100, self.strength + amount)
        self.trust = min(100, self.trust + amount * 0.8)
    
    def can_evolve(self) -> bool:
        """是否可以进化到下一阶段"""
        return self.strength >= 80 and self.trust >= 70
    
    def evolve_type(self) -> Optional[RelationshipType]:
        """进化关系类型"""
        if not self.can_evolve():
            return None
        
        if self.type == RelationshipType.ACQUAINTANCE:
            return RelationshipType.FRIEND
        elif self.type == RelationshipType.FRIEND:
            return RelationshipType.CLOSE_FRIEND
        elif self.type == RelationshipType.COLLEAGUE:
            return RelationshipType.PARTNER
        
        return None
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "agent_a": self.agent_a,
            "agent_b": self.agent_b,
            "type": self.type.value,
            "strength": self.strength,
            "trust": self.trust,
            "established_at": self.established_at.isoformat(),
            "last_interaction": self.last_interaction.isoformat(),
            "interaction_count": len(self.history),
        }


class RelationshipNetwork:
    """关系网络"""
    
    def __init__(self, agent_id: str):
        """
        初始化关系网络
        
        Args:
            agent_id: Agent ID
        """
        self.agent_id = agent_id
        self.relationships: Dict[str, Relationship] = {}
    
    def add_relationship(self, other_agent_id: str, 
                        rel_type: RelationshipType = RelationshipType.ACQUAINTANCE):
        """
        添加关系
        
        Args:
            other_agent_id: 另一个 Agent ID
            rel_type: 关系类型
        """
        if other_agent_id not in self.relationships:
            self.relationships[other_agent_id] = Relationship(
                agent_a=self.agent_id,
                agent_b=other_agent_id,
                type=rel_type,
            )
    
    def get_relationship(self, other_agent_id: str) -> Optional[Relationship]:
        """获取关系"""
        return self.relationships.get(other_agent_id)
    
    def deepen_relationship(self, other_agent_id: str, amount: float = 5.0):
        """深化关系"""
        rel = self.get_relationship(other_agent_id)
        if rel:
            rel.deepen(amount)
    
    def damage_relationship(self, other_agent_id: str, amount: float = 10.0):
        """损害关系"""
        rel = self.get_relationship(other_agent_id)
        if rel:
            rel.damage(amount)
    
    def repair_relationship(self, other_agent_id: str, amount: float = 5.0):
        """修复关系"""
        rel = self.get_relationship(other_agent_id)
        if rel:
            rel.repair(amount)
    
    def get_friends(self) -> List[str]:
        """获取朋友列表"""
        return [
            agent_id for agent_id, rel in self.relationships.items()
            if rel.type in [RelationshipType.FRIEND, RelationshipType.CLOSE_FRIEND]
            and rel.strength >= 50
        ]
    
    def get_colleagues(self) -> List[str]:
        """获取同事列表"""
        return [
            agent_id for agent_id, rel in self.relationships.items()
            if rel.type in [RelationshipType.COLLEAGUE, RelationshipType.PARTNER]
        ]
    
    def get_strangers(self) -> List[str]:
        """获取陌生人列表"""
        return [
            agent_id for agent_id, rel in self.relationships.items()
            if rel.type == RelationshipType.ACQUAINTANCE
            and rel.strength < 20
        ]
    
    def get_network_stats(self) -> Dict:
        """获取网络统计"""
        return {
            "total": len(self.relationships),
            "friends": len(self.get_friends()),
            "colleagues": len(self.get_colleagues()),
            "strangers": len(self.get_strangers()),
            "avg_strength": sum(r.strength for r in self.relationships.values()) / len(self.relationships) if self.relationships else 0,
            "avg_trust": sum(r.trust for r in self.relationships.values()) / len(self.relationships) if self.relationships else 0,
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "agent_id": self.agent_id,
            "stats": self.get_network_stats(),
            "relationships": [
                rel.to_dict() for rel in self.relationships.values()
            ],
        }
