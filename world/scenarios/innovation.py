#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创新讨论场景 - 硅基世界 2

Agent 之间进行创新思维碰撞，产生新想法和解决方案。
"""

import asyncio
import random
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class InnovationStage(Enum):
    """创新阶段"""
    IDEATION = "ideation"         # 创意产生
    DISCUSSION = "discussion"     # 讨论完善
    EVALUATION = "evaluation"     # 评估筛选
    PROTOTYPING = "prototyping"   # 原型开发
    IMPLEMENTATION = "implementation"  # 实施


class IdeaStatus(Enum):
    """创意状态"""
    DRAFT = "draft"           # 草稿
    PROPOSED = "proposed"     # 已提议
    UNDER_REVIEW = "review"   # 审核中
    APPROVED = "approved"     # 已批准
    REJECTED = "rejected"     # 已拒绝
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"   # 已完成


@dataclass
class InnovationIdea:
    """创新创意"""
    idea_id: str
    title: str
    description: str
    proposer: str
    stage: InnovationStage = InnovationStage.IDEATION
    status: IdeaStatus = IdeaStatus.DRAFT
    supporters: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    updated_at: float = field(default_factory=lambda: datetime.now().timestamp())
    comments: List[Dict] = field(default_factory=list)
    improvements: List[str] = field(default_factory=list)
    feasibility_score: int = 50  # 可行性评分 0-100
    impact_score: int = 50       # 影响力评分 0-100
    
    def to_dict(self) -> Dict:
        return {
            "idea_id": self.idea_id,
            "title": self.title,
            "description": self.description,
            "proposer": self.proposer,
            "stage": self.stage.value,
            "status": self.status.value,
            "supporters": self.supporters,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "comments": self.comments,
            "improvements": self.improvements,
            "feasibility_score": self.feasibility_score,
            "impact_score": self.impact_score,
        }


class InnovationManager:
    """创新管理器"""
    
    def __init__(self):
        """初始化创新管理器"""
        self.ideas: Dict[str, InnovationIdea] = {}
        self._idea_counter = 0
        
        # 创新引导问题
        self.innovation_prompts = [
            "我们如何让这个流程更高效？",
            "有没有更好的解决方案？",
            "如果没有限制，我们会怎么做？",
            "这个想法的潜在风险是什么？",
            "如何让用户体验更好？",
        ]
        
        # 评估标准
        self.evaluation_criteria = [
            "可行性 (Feasibility)",
            "影响力 (Impact)",
            "创新性 (Novelty)",
            "成本效益 (Cost-effectiveness)",
            "可持续性 (Sustainability)",
        ]
    
    async def propose_idea(
        self,
        title: str,
        description: str,
        proposer: str,
    ) -> InnovationIdea:
        """
        提出创新创意
        
        Args:
            title: 创意标题
            description: 创意描述
            proposer: 提议者
            
        Returns:
            创新创意对象
        """
        self._idea_counter += 1
        
        idea = InnovationIdea(
            idea_id=f"idea_{self._idea_counter}",
            title=title,
            description=description,
            proposer=proposer,
            status=IdeaStatus.PROPOSED,
        )
        
        self.ideas[idea.idea_id] = idea
        
        print(f"💡 新创意：{title}")
        print(f"   提议者：{proposer}")
        print(f"   描述：{description[:50]}...")
        
        return idea
    
    async def support_idea(self, idea_id: str, supporter: str) -> bool:
        """支持创意"""
        if idea_id not in self.ideas:
            return False
        
        idea = self.ideas[idea_id]
        if supporter not in idea.supporters:
            idea.supporters.append(supporter)
            print(f"👍 {supporter} 支持了创意：{idea.title}")
        
        return True
    
    async def add_comment(self, idea_id: str, agent_id: str, comment: str, is_improvement: bool = False) -> bool:
        """添加评论或改进建议"""
        if idea_id not in self.ideas:
            return False
        
        idea = self.ideas[idea_id]
        
        if is_improvement:
            idea.improvements.append(f"[{agent_id}]: {comment}")
            print(f"🔧 {agent_id} 提出改进：{comment}")
        else:
            idea.comments.append({
                "agent_id": agent_id,
                "comment": comment,
                "timestamp": datetime.now().timestamp(),
            })
            print(f"💬 {agent_id}: {comment}")
        
        idea.updated_at = datetime.now().timestamp()
        
        return True
    
    async def evaluate_idea(
        self,
        idea_id: str,
        feasibility: int,
        impact: int,
    ) -> bool:
        """评估创意"""
        if idea_id not in self.ideas:
            return False
        
        idea = self.ideas[idea_id]
        idea.feasibility_score = min(100, max(0, feasibility))
        idea.impact_score = min(100, max(0, impact))
        idea.status = IdeaStatus.UNDER_REVIEW
        
        avg_score = (feasibility + impact) / 2
        if avg_score >= 70:
            idea.status = IdeaStatus.APPROVED
            print(f"✅ 创意通过评估：{idea.title} (综合评分：{avg_score})")
        elif avg_score >= 40:
            print(f"🔄 创意待完善：{idea.title} (综合评分：{avg_score})")
        else:
            idea.status = IdeaStatus.REJECTED
            print(f"❌ 创意未通过：{idea.title} (综合评分：{avg_score})")
        
        return True
    
    async def advance_stage(self, idea_id: str) -> bool:
        """推进创新阶段"""
        if idea_id not in self.ideas:
            return False
        
        idea = self.ideas[idea_id]
        stage_order = list(InnovationStage)
        current_idx = stage_order.index(idea.stage)
        
        if current_idx < len(stage_order) - 1:
            idea.stage = stage_order[current_idx + 1]
            print(f"📈 创意进入新阶段：{idea.title} -> {idea.stage.value}")
        
        return True
    
    def get_ideas_by_stage(self, stage: InnovationStage) -> List[InnovationIdea]:
        """获取指定阶段的创意"""
        return [i for i in self.ideas.values() if i.stage == stage]
    
    def get_ideas_by_status(self, status: IdeaStatus) -> List[InnovationIdea]:
        """获取指定状态的创意"""
        return [i for i in self.ideas.values() if i.status == status]
    
    def get_top_ideas(self, limit: int = 10) -> List[InnovationIdea]:
        """获取评分最高的创意"""
        sorted_ideas = sorted(
            self.ideas.values(),
            key=lambda i: i.feasibility_score + i.impact_score,
            reverse=True,
        )
        return sorted_ideas[:limit]
    
    def get_agent_ideas(self, agent_id: str) -> List[InnovationIdea]:
        """获取 Agent 提出的创意"""
        return [i for i in self.ideas.values() if i.proposer == agent_id]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total": len(self.ideas),
            "by_stage": {
                s.value: len([i for i in self.ideas.values() if i.stage == s])
                for s in InnovationStage
            },
            "by_status": {
                st.value: len([i for i in self.ideas.values() if i.status == st])
                for st in IdeaStatus
            },
            "avg_feasibility": sum(i.feasibility_score for i in self.ideas.values()) / max(1, len(self.ideas)),
            "avg_impact": sum(i.impact_score for i in self.ideas.values()) / max(1, len(self.ideas)),
        }


# 单例
_innovation_manager: Optional[InnovationManager] = None


def get_innovation_manager() -> InnovationManager:
    """获取创新管理器单例"""
    global _innovation_manager
    if _innovation_manager is None:
        _innovation_manager = InnovationManager()
    return _innovation_manager


def create_innovation_manager() -> InnovationManager:
    """创建创新管理器"""
    return InnovationManager()
