#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
群组系统 - 硅基世界 2

让 Agent 可以创建和加入群组，形成社群。
"""

from datetime import datetime
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum


class GroupType(Enum):
    """群组类型"""
    WORK = "work"          # 工作群
    SOCIAL = "social"      # 社交群
    INTEREST = "interest"  # 兴趣群
    PROJECT = "project"    # 项目组
    CLUB = "club"          # 俱乐部


class GroupRole(Enum):
    """群组角色"""
    OWNER = "owner"      # 群主
    ADMIN = "admin"      # 管理员
    MEMBER = "member"    # 成员


@dataclass
class Group:
    """群组"""
    group_id: str
    name: str
    description: str
    group_type: GroupType
    owner: str
    members: Dict[str, GroupRole] = field(default_factory=dict)
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    max_members: int = 50
    is_public: bool = True
    
    def to_dict(self) -> Dict:
        return {
            "group_id": self.group_id,
            "name": self.name,
            "description": self.description,
            "type": self.group_type.value,
            "owner": self.owner,
            "member_count": len(self.members),
            "max_members": self.max_members,
            "is_public": self.is_public,
        }


class GroupManager:
    """群组管理器"""
    
    def __init__(self):
        """初始化群组管理器"""
        self.groups: Dict[str, Group] = {}
        self._group_counter = 0
        
        print("👥 群组系统已初始化")
    
    def create_group(
        self,
        name: str,
        description: str,
        owner: str,
        group_type: GroupType = GroupType.SOCIAL,
        max_members: int = 50,
        is_public: bool = True,
    ) -> Group:
        """
        创建群组
        
        Args:
            name: 群组名称
            description: 描述
            owner: 群主
            group_type: 群组类型
            max_members: 最大成员数
            is_public: 是否公开
            
        Returns:
            群组对象
        """
        self._group_counter += 1
        
        group = Group(
            group_id=f"group_{self._group_counter}",
            name=name,
            description=description,
            group_type=group_type,
            owner=owner,
            max_members=max_members,
            is_public=is_public,
        )
        
        # 群主自动加入
        group.members[owner] = GroupRole.OWNER
        
        self.groups[group.group_id] = group
        
        print(f"  👥 {owner} 创建了群组：{name}")
        
        return group
    
    def join_group(self, group_id: str, agent_id: str) -> bool:
        """
        加入群组
        
        Args:
            group_id: 群组 ID
            agent_id: Agent ID
            
        Returns:
            是否成功
        """
        if group_id not in self.groups:
            return False
        
        group = self.groups[group_id]
        
        if len(group.members) >= group.max_members:
            return False
        
        if agent_id in group.members:
            return False
        
        group.members[agent_id] = GroupRole.MEMBER
        
        print(f"  ✓ {agent_id} 加入了群组：{group.name}")
        
        return True
    
    def leave_group(self, group_id: str, agent_id: str) -> bool:
        """退出群组"""
        if group_id not in self.groups:
            return False
        
        group = self.groups[group_id]
        
        if agent_id not in group.members:
            return False
        
        if group.members[agent_id] == GroupRole.OWNER:
            # 群主退出需要转移
            return False
        
        del group.members[agent_id]
        
        print(f"  ✓ {agent_id} 退出了群组：{group.name}")
        
        return True
    
    def set_role(self, group_id: str, agent_id: str, role: GroupRole) -> bool:
        """设置成员角色"""
        if group_id not in self.groups:
            return False
        
        group = self.groups[group_id]
        
        if agent_id not in group.members:
            return False
        
        group.members[agent_id] = role
        
        return True
    
    def get_group(self, group_id: str) -> Optional[Group]:
        """获取群组"""
        return self.groups.get(group_id)
    
    def get_agent_groups(self, agent_id: str) -> List[Group]:
        """获取 Agent 加入的群组"""
        return [
            g for g in self.groups.values()
            if agent_id in g.members
        ]
    
    def get_public_groups(self) -> List[Group]:
        """获取公开群组"""
        return [g for g in self.groups.values() if g.is_public]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_groups": len(self.groups),
            "total_memberships": sum(len(g.members) for g in self.groups.values()),
            "by_type": {
                t.value: len([g for g in self.groups.values() if g.group_type == t])
                for t in GroupType
            },
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "public_groups": [g.to_dict() for g in self.get_public_groups()[:10]],
        }


# 单例
_group_manager: Optional[GroupManager] = None


def get_group_manager() -> GroupManager:
    """获取群组管理器单例"""
    global _group_manager
    if _group_manager is None:
        _group_manager = GroupManager()
    return _group_manager


# 工厂函数
def create_group_manager() -> GroupManager:
    """创建群组管理器"""
    return GroupManager()
