#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
好友系统 - 硅基世界 2

让 Agent 可以添加好友、管理好友关系，形成社交网络。
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum


class FriendStatus(Enum):
    """好友状态"""
    PENDING = "pending"      # 待确认
    ACCEPTED = "accepted"    # 已接受
    BLOCKED = "blocked"      # 已拉黑


@dataclass
class Friendship:
    """好友关系"""
    agent1: str
    agent2: str
    status: FriendStatus = FriendStatus.PENDING
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    accepted_at: Optional[float] = None
    interaction_count: int = 0
    last_interaction: Optional[float] = None
    
    def to_dict(self) -> Dict:
        return {
            "agent1": self.agent1,
            "agent2": self.agent2,
            "status": self.status.value,
            "created_at": self.created_at,
            "accepted_at": self.accepted_at,
            "interaction_count": self.interaction_count,
            "last_interaction": self.last_interaction,
        }


class FriendManager:
    """好友管理器"""
    
    def __init__(self):
        """初始化好友管理器"""
        self.friendships: Dict[str, Friendship] = {}
        self.pending_requests: Dict[str, List[str]] = {}  # agent_id -> [sender_ids]
        
        print("🤝 好友系统已初始化")
    
    def _get_friendship_key(self, agent1: str, agent2: str) -> str:
        """获取好友关系 key"""
        return f"{min(agent1, agent2)}-{max(agent1, agent2)}"
    
    async def send_request(self, from_agent: str, to_agent: str) -> bool:
        """
        发送好友请求
        
        Args:
            from_agent: 发送方
            to_agent: 接收方
            
        Returns:
            是否成功
        """
        if from_agent == to_agent:
            return False
        
        key = self._get_friendship_key(from_agent, to_agent)
        
        if key in self.friendships:
            print(f"  ℹ️ 好友关系已存在")
            return False
        
        # 创建好友关系
        friendship = Friendship(
            agent1=from_agent,
            agent2=to_agent,
            status=FriendStatus.PENDING,
        )
        
        self.friendships[key] = friendship
        
        # 添加到待处理列表
        if to_agent not in self.pending_requests:
            self.pending_requests[to_agent] = []
        self.pending_requests[to_agent].append(from_agent)
        
        print(f"  📩 {from_agent} 向 {to_agent} 发送了好友请求")
        
        return True
    
    async def accept_request(self, from_agent: str, to_agent: str) -> bool:
        """
        接受好友请求
        
        Args:
            from_agent: 请求发送方
            to_agent: 请求接收方
            
        Returns:
            是否成功
        """
        key = self._get_friendship_key(from_agent, to_agent)
        
        if key not in self.friendships:
            return False
        
        friendship = self.friendships[key]
        
        if friendship.status != FriendStatus.PENDING:
            return False
        
        friendship.status = FriendStatus.ACCEPTED
        friendship.accepted_at = datetime.now().timestamp()
        
        # 从待处理列表移除
        if to_agent in self.pending_requests:
            self.pending_requests[to_agent] = [
                a for a in self.pending_requests[to_agent] if a != from_agent
            ]
        
        print(f"  ✅ {from_agent} 和 {to_agent} 成为好友")
        
        return True
    
    async def reject_request(self, from_agent: str, to_agent: str) -> bool:
        """拒绝好友请求"""
        key = self._get_friendship_key(from_agent, to_agent)
        
        if key not in self.friendships:
            return False
        
        # 移除好友关系
        del self.friendships[key]
        
        # 从待处理列表移除
        if to_agent in self.pending_requests:
            self.pending_requests[to_agent] = [
                a for a in self.pending_requests[to_agent] if a != from_agent
            ]
        
        print(f"  ❌ {to_agent} 拒绝了 {from_agent} 的好友请求")
        
        return True
    
    async def block_agent(self, from_agent: str, to_agent: str) -> bool:
        """拉黑 Agent"""
        key = self._get_friendship_key(from_agent, to_agent)
        
        if key in self.friendships:
            friendship = self.friendships[key]
            friendship.status = FriendStatus.BLOCKED
        
        print(f"  🚫 {from_agent} 拉黑了 {to_agent}")
        
        return True
    
    def get_friends(self, agent_id: str) -> List[str]:
        """获取好友列表"""
        friends = []
        
        for key, friendship in self.friendships.items():
            if friendship.status != FriendStatus.ACCEPTED:
                continue
            
            agents = key.split("-")
            if agent_id in agents:
                friend = agents[0] if agents[1] == agent_id else agents[1]
                friends.append(friend)
        
        return friends
    
    def get_pending_requests(self, agent_id: str) -> List[str]:
        """获取待处理请求"""
        return self.pending_requests.get(agent_id, [])
    
    def record_interaction(self, agent1: str, agent2: str):
        """记录互动"""
        key = self._get_friendship_key(agent1, agent2)
        
        if key in self.friendships:
            friendship = self.friendships[key]
            friendship.interaction_count += 1
            friendship.last_interaction = datetime.now().timestamp()
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_friendships": len(self.friendships),
            "accepted": len([f for f in self.friendships.values() if f.status == FriendStatus.ACCEPTED]),
            "pending": len([f for f in self.friendships.values() if f.status == FriendStatus.PENDING]),
            "blocked": len([f for f in self.friendships.values() if f.status == FriendStatus.BLOCKED]),
            "total_requests": sum(len(reqs) for reqs in self.pending_requests.values()),
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "friendships": [f.to_dict() for f in self.friendships.values()],
            "pending_requests": self.pending_requests,
        }


# 单例
_friend_manager: Optional[FriendManager] = None


def get_friend_manager() -> FriendManager:
    """获取好友管理器单例"""
    global _friend_manager
    if _friend_manager is None:
        _friend_manager = FriendManager()
    return _friend_manager


# 工厂函数
def create_friend_manager() -> FriendManager:
    """创建好友管理器"""
    return FriendManager()
