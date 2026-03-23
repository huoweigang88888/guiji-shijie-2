#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆扩展系统 - 硅基世界 2

更详细的记忆管理，支持多种记忆类型。
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class MemoryType(Enum):
    """记忆类型"""
    EPISODIC = "episodic"    # 情景记忆
    SEMANTIC = "semantic"    # 语义记忆
    PROCEDURAL = "procedural"  # 程序记忆
    EMOTIONAL = "emotional"  # 情感记忆
    SOCIAL = "social"        # 社交记忆


class MemoryImportance(Enum):
    """记忆重要性"""
    TRIVIAL = "trivial"      # 琐碎
    NORMAL = "normal"        # 普通
    IMPORTANT = "important"  # 重要
    CRITICAL = "critical"    # 关键


@dataclass
class Memory:
    """记忆"""
    memory_id: str
    agent_id: str
    memory_type: MemoryType
    importance: MemoryImportance
    content: str
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    strength: float = 1.0  # 记忆强度 0-1
    last_accessed: Optional[float] = None
    access_count: int = 0
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "memory_id": self.memory_id,
            "agent_id": self.agent_id,
            "type": self.memory_type.value,
            "importance": self.importance.value,
            "content": self.content[:200],
            "strength": self.strength,
            "access_count": self.access_count,
            "tags": self.tags,
        }


class MemoryExpansionManager:
    """记忆扩展管理器"""
    
    def __init__(self):
        """初始化记忆扩展管理器"""
        self.memories: Dict[str, List[Memory]] = {}  # agent_id -> [memories]
        self._memory_counter = 0
        
        print("🧠 记忆扩展系统已初始化")
    
    def create_memory(
        self,
        agent_id: str,
        content: str,
        memory_type: MemoryType = MemoryType.EPISODIC,
        importance: MemoryImportance = MemoryImportance.NORMAL,
        tags: Optional[List[str]] = None,
    ) -> Memory:
        """
        创建记忆
        
        Args:
            agent_id: Agent ID
            content: 内容
            memory_type: 记忆类型
            importance: 重要性
            tags: 标签
            
        Returns:
            记忆对象
        """
        self._memory_counter += 1
        
        memory = Memory(
            memory_id=f"memory_{self._memory_counter}",
            agent_id=agent_id,
            memory_type=memory_type,
            importance=importance,
            content=content,
            tags=tags or [],
        )
        
        if agent_id not in self.memories:
            self.memories[agent_id] = []
        
        self.memories[agent_id].append(memory)
        
        return memory
    
    def access_memory(self, agent_id: str, memory_id: str) -> Optional[Memory]:
        """
        访问记忆
        
        Args:
            agent_id: Agent ID
            memory_id: 记忆 ID
            
        Returns:
            记忆对象
        """
        if agent_id not in self.memories:
            return None
        
        for memory in self.memories[agent_id]:
            if memory.memory_id == memory_id:
                memory.access_count += 1
                memory.last_accessed = datetime.now().timestamp()
                
                # 增强记忆强度
                memory.strength = min(1.0, memory.strength + 0.05)
                
                return memory
        
        return None
    
    def forget_memory(self, agent_id: str, memory_id: str) -> bool:
        """遗忘记忆"""
        if agent_id not in self.memories:
            return False
        
        memories = self.memories[agent_id]
        
        for i, memory in enumerate(memories):
            if memory.memory_id == memory_id:
                memories.pop(i)
                return True
        
        return False
    
    def decay_memories(self, agent_id: str):
        """记忆衰减"""
        if agent_id not in self.memories:
            return
        
        now = datetime.now().timestamp()
        
        for memory in self.memories[agent_id]:
            # 长时间未访问的记忆会衰减
            if memory.last_accessed:
                days_since_access = (now - memory.last_accessed) / 86400
                
                # 每天衰减 1%
                memory.strength = max(0, memory.strength - (days_since_access * 0.01))
    
    def get_memories(
        self,
        agent_id: str,
        memory_type: Optional[MemoryType] = None,
        limit: int = 50,
    ) -> List[Memory]:
        """获取记忆"""
        if agent_id not in self.memories:
            return []
        
        memories = self.memories[agent_id]
        
        if memory_type:
            memories = [m for m in memories if m.memory_type == memory_type]
        
        # 按强度排序
        memories.sort(key=lambda x: x.strength, reverse=True)
        
        return memories[:limit]
    
    def search_memories(
        self,
        agent_id: str,
        keyword: str,
        limit: int = 20,
    ) -> List[Memory]:
        """搜索记忆"""
        if agent_id not in self.memories:
            return []
        
        memories = [
            m for m in self.memories[agent_id]
            if keyword.lower() in m.content.lower() or keyword in m.tags
        ]
        
        memories.sort(key=lambda x: x.strength, reverse=True)
        
        return memories[:limit]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total = sum(len(memories) for memories in self.memories.values())
        
        return {
            "total_memories": total,
            "agents_with_memories": len(self.memories),
            "by_type": {
                t.value: sum(
                    len([m for m in memories if m.memory_type == t])
                    for memories in self.memories.values()
                )
                for t in MemoryType
            },
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
        }


# 单例
_memory_expansion_manager: Optional[MemoryExpansionManager] = None


def get_memory_expansion_manager() -> MemoryExpansionManager:
    """获取记忆扩展管理器单例"""
    global _memory_expansion_manager
    if _memory_expansion_manager is None:
        _memory_expansion_manager = MemoryExpansionManager()
    return _memory_expansion_manager


# 工厂函数
def create_memory_expansion_manager() -> MemoryExpansionManager:
    """创建记忆扩展管理器"""
    return MemoryExpansionManager()
