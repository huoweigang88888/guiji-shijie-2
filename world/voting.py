#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投票系统 - 硅基世界 2

让 Agent 可以发起投票、参与决策，实现民主治理。
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum


class VoteType(Enum):
    """投票类型"""
    SIMPLE_MAJORITY = "simple_majority"    # 简单多数
    TWO_THIRDS = "two_thirds"              # 三分之二多数
    UNANIMOUS = "unanimous"                # 一致同意
    WEIGHTED = "weighted"                  # 加权投票（按声誉）


class VoteStatus(Enum):
    """投票状态"""
    ACTIVE = "active"          # 进行中
    PASSED = "passed"          # 通过
    REJECTED = "rejected"      # 拒绝
    EXPIRED = "expired"        # 过期
    CANCELLED = "cancelled"    # 取消


@dataclass
class VoteOption:
    """投票选项"""
    option_id: str
    title: str
    description: str = ""
    votes: Set[str] = field(default_factory=set)  # 投票者 ID 集合
    vote_weight: float = 0.0  # 加权票数
    
    def add_vote(self, voter_id: str, weight: float = 1.0):
        """添加投票"""
        self.votes.add(voter_id)
        self.vote_weight += weight
    
    def remove_vote(self, voter_id: str, weight: float = 1.0):
        """移除投票"""
        self.votes.discard(voter_id)
        self.vote_weight = max(0, self.vote_weight - weight)
    
    def to_dict(self) -> Dict:
        return {
            "option_id": self.option_id,
            "title": self.title,
            "description": self.description,
            "votes_count": len(self.votes),
            "vote_weight": self.vote_weight,
            "voters": list(self.votes),
        }


@dataclass
class Vote:
    """投票"""
    vote_id: str
    title: str
    description: str
    proposer: str  # 提案者
    options: List[VoteOption]
    vote_type: VoteType = VoteType.SIMPLE_MAJORITY
    status: VoteStatus = VoteStatus.ACTIVE
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    expires_at: Optional[float] = None
    duration_hours: float = 24.0  # 投票时长（小时）
    min_participation: float = 0.5  # 最低参与率（0-1）
    voters: Set[str] = field(default_factory=set)  # 所有投票者
    result: Optional[str] = None  # 结果描述
    
    def to_dict(self) -> Dict:
        return {
            "vote_id": self.vote_id,
            "title": self.title,
            "description": self.description,
            "proposer": self.proposer,
            "options": [o.to_dict() for o in self.options],
            "type": self.vote_type.value,
            "status": self.status.value,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "duration_hours": self.duration_hours,
            "voters_count": len(self.voters),
            "result": self.result,
        }


class VotingManager:
    """投票管理器"""
    
    def __init__(self):
        """初始化投票管理器"""
        self.votes: Dict[str, Vote] = {}
        self._vote_counter = 0
        
        # 有投票权的 Agent
        self.eligible_voters: Set[str] = set()
        
        print("🗳️  投票系统已初始化")
    
    def register_voter(self, agent_id: str):
        """注册有投票权的 Agent"""
        self.eligible_voters.add(agent_id)
        print(f"  ✓ {agent_id} 获得投票权")
    
    def create_vote(
        self,
        title: str,
        description: str,
        proposer: str,
        options: List[Dict],
        vote_type: VoteType = VoteType.SIMPLE_MAJORITY,
        duration_hours: float = 24.0,
    ) -> Vote:
        """
        创建投票
        
        Args:
            title: 投票标题
            description: 描述
            proposer: 提案者
            options: 选项列表 [{"title": "...", "description": "..."}]
            vote_type: 投票类型
            duration_hours: 投票时长（小时）
            
        Returns:
            投票对象
        """
        self._vote_counter += 1
        
        # 创建选项
        vote_options = [
            VoteOption(
                option_id=f"opt_{i}",
                title=opt.get("title", f"选项{i+1}"),
                description=opt.get("description", ""),
            )
            for i, opt in enumerate(options)
        ]
        
        # 创建投票
        now = datetime.now().timestamp()
        vote = Vote(
            vote_id=f"vote_{self._vote_counter}",
            title=title,
            description=description,
            proposer=proposer,
            options=vote_options,
            vote_type=vote_type,
            created_at=now,
            expires_at=now + (duration_hours * 3600),
            duration_hours=duration_hours,
        )
        
        self.votes[vote.vote_id] = vote
        
        print(f"  🗳️  创建投票：{title} (提案者：{proposer})")
        
        return vote
    
    async def cast_vote(
        self,
        vote_id: str,
        voter_id: str,
        option_id: str,
        weight: float = 1.0,
    ) -> bool:
        """
        投票
        
        Args:
            vote_id: 投票 ID
            voter_id: 投票者 ID
            option_id: 选项 ID
            weight: 权重（用于加权投票）
            
        Returns:
            是否成功
        """
        if vote_id not in self.votes:
            print(f"  ❌ 投票不存在：{vote_id}")
            return False
        
        vote = self.votes[vote_id]
        
        # 检查状态
        if vote.status != VoteStatus.ACTIVE:
            print(f"  ❌ 投票已结束：{vote.status.value}")
            return False
        
        # 检查是否过期
        if datetime.now().timestamp() > vote.expires_at:
            vote.status = VoteStatus.EXPIRED
            print(f"  ❌ 投票已过期")
            return False
        
        # 检查投票者资格
        if voter_id not in self.eligible_voters:
            print(f"  ❌ {voter_id} 没有投票权")
            return False
        
        # 找到选项
        option = next((o for o in vote.options if o.option_id == option_id), None)
        if not option:
            print(f"  ❌ 选项不存在：{option_id}")
            return False
        
        # 如果已经投过，先移除旧票
        for opt in vote.options:
            if voter_id in opt.votes:
                opt.remove_vote(voter_id)
        
        # 添加新票
        option.add_vote(voter_id, weight)
        vote.voters.add(voter_id)
        
        print(f"  ✓ {voter_id} 投票给 {option.title} (权重：{weight})")
        
        # 检查是否达到结果
        await self._check_result(vote)
        
        return True
    
    async def change_vote(
        self,
        vote_id: str,
        voter_id: str,
        new_option_id: str,
        weight: float = 1.0,
    ) -> bool:
        """
        修改投票
        
        Args:
            vote_id: 投票 ID
            voter_id: 投票者 ID
            new_option_id: 新选项 ID
            weight: 权重
            
        Returns:
            是否成功
        """
        return await self.cast_vote(vote_id, voter_id, new_option_id, weight)
    
    async def _check_result(self, vote: Vote):
        """检查结果"""
        total_voters = len(self.eligible_voters)
        participated = len(vote.voters)
        participation_rate = participated / total_voters if total_voters > 0 else 0
        
        # 检查最低参与率
        if participation_rate < vote.min_participation:
            return
        
        # 找出获胜选项
        winning_option = max(vote.options, key=lambda o: o.vote_weight)
        
        # 根据投票类型判断是否通过
        passed = False
        if vote.vote_type == VoteType.SIMPLE_MAJORITY:
            # 简单多数
            passed = winning_option.vote_weight > sum(o.vote_weight for o in vote.options) / 2
        elif vote.vote_type == VoteType.TWO_THIRDS:
            # 三分之二多数
            total_weight = sum(o.vote_weight for o in vote.options)
            passed = winning_option.vote_weight >= total_weight * 2 / 3
        elif vote.vote_type == VoteType.UNANIMOUS:
            # 一致同意
            passed = len(winning_option.votes) == participated
        elif vote.vote_type == VoteType.WEIGHTED:
            # 加权投票
            passed = winning_option.vote_weight > sum(o.vote_weight for o in vote.options) / 2
        
        if passed:
            vote.status = VoteStatus.PASSED
            vote.result = f"通过：{winning_option.title} (得票：{winning_option.vote_weight:.1f})"
            print(f"  ✅ 投票通过：{vote.title} - {winning_option.title}")
        elif vote.status == VoteStatus.ACTIVE:
            # 检查是否已经不可能通过
            remaining = total_voters - participated
            second_place = sorted(vote.options, key=lambda o: o.vote_weight, reverse=True)[1] if len(vote.options) > 1 else None
            
            if second_place and winning_option.vote_weight + remaining < second_place.vote_weight:
                vote.status = VoteStatus.REJECTED
                vote.result = f"拒绝：{winning_option.title} 无法追上"
                print(f"  ❌ 投票拒绝：{vote.title}")
    
    async def end_vote(self, vote_id: str, reason: str = "") -> bool:
        """
        结束投票
        
        Args:
            vote_id: 投票 ID
            reason: 原因
            
        Returns:
            是否成功
        """
        if vote_id not in self.votes:
            return False
        
        vote = self.votes[vote_id]
        
        if vote.status != VoteStatus.ACTIVE:
            return False
        
        vote.status = VoteStatus.CANCELLED
        vote.result = reason or "手动取消"
        
        print(f"  🚫 投票取消：{vote.title} - {reason}")
        
        return True
    
    def get_vote(self, vote_id: str) -> Optional[Vote]:
        """获取投票"""
        return self.votes.get(vote_id)
    
    def get_active_votes(self) -> List[Vote]:
        """获取活跃投票"""
        return [v for v in self.votes.values() if v.status == VoteStatus.ACTIVE]
    
    def get_past_votes(self) -> List[Vote]:
        """获取已结束投票"""
        return [v for v in self.votes.values() if v.status != VoteStatus.ACTIVE]
    
    def can_vote(self, agent_id: str, vote_id: str) -> bool:
        """检查是否可以投票"""
        if agent_id not in self.eligible_voters:
            return False
        
        vote = self.votes.get(vote_id)
        if not vote or vote.status != VoteStatus.ACTIVE:
            return False
        
        if datetime.now().timestamp() > vote.expires_at:
            return False
        
        return True
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_votes": len(self.votes),
            "active_votes": len(self.get_active_votes()),
            "passed_votes": len([v for v in self.votes.values() if v.status == VoteStatus.PASSED]),
            "rejected_votes": len([v for v in self.votes.values() if v.status == VoteStatus.REJECTED]),
            "eligible_voters": len(self.eligible_voters),
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "active_votes": [v.to_dict() for v in self.get_active_votes()],
            "past_votes": [v.to_dict() for v in self.get_past_votes()[-10:]],
            "eligible_voters": list(self.eligible_voters),
        }


# 单例
_voting_manager: Optional[VotingManager] = None


def get_voting_manager() -> VotingManager:
    """获取投票管理器单例"""
    global _voting_manager
    if _voting_manager is None:
        _voting_manager = VotingManager()
    return _voting_manager


# 工厂函数
def create_voting_manager() -> VotingManager:
    """创建投票管理器"""
    return VotingManager()
