#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆系统 - 硅基世界 2

硅基记忆模型：
- 短期记忆：最近互动
- 长期记忆：重要经历
- 程序记忆：技能和知识
- 情景记忆：具体事件

记忆可以：
- 强化（经常回忆）
- 淡化（长期不用）
- 关联（与其他记忆连接）
- 提取（回忆）
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import json


class MemoryType(Enum):
    """记忆类型"""
    SHORT_TERM = "short_term"      # 短期记忆
    LONG_TERM = "long_term"        # 长期记忆
    PROCEDURAL = "procedural"      # 程序记忆（技能）
    EPISODIC = "episodic"          # 情景记忆（事件）
    SEMANTIC = "semantic"          # 语义记忆（知识）


@dataclass
class Memory:
    """记忆"""
    id: str
    type: MemoryType
    content: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    importance: float = 0.0  # 重要度 0-100
    associations: List[str] = field(default_factory=list)  # 关联记忆 ID
    
    def access(self):
        """访问记忆"""
        self.access_count += 1
        self.last_accessed = datetime.now()
    
    def strengthen(self, amount: float = 5.0):
        """强化记忆"""
        self.importance = min(100, self.importance + amount)
    
    def weaken(self, amount: float = 2.0):
        """淡化记忆"""
        self.importance = max(0, self.importance - amount)
    
    def associate(self, memory_id: str):
        """关联其他记忆"""
        if memory_id not in self.associations:
            self.associations.append(memory_id)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "id": self.id,
            "type": self.type.value,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "access_count": self.access_count,
            "importance": self.importance,
            "associations": self.associations,
        }


class AgentMemory:
    """Agent 记忆系统"""
    
    def __init__(self, agent_id: str, max_short_term: int = 100, max_long_term: int = 1000):
        """
        初始化记忆系统
        
        Args:
            agent_id: Agent ID
            max_short_term: 短期记忆最大数量
            max_long_term: 长期记忆最大数量
        """
        self.agent_id = agent_id
        self.max_short_term = max_short_term
        self.max_long_term = max_long_term
        
        # 记忆存储
        self.short_term: List[Memory] = []
        self.long_term: List[Memory] = []
        self.procedural: Dict[str, Any] = {}  # 技能
        self.semantic: Dict[str, Any] = {}    # 知识
        
        # 记忆索引
        self.memory_index: Dict[str, Memory] = {}
    
    def add_short_term(self, content: Dict[str, Any], importance: float = 50.0) -> Memory:
        """
        添加短期记忆
        
        Args:
            content: 记忆内容
            importance: 重要度
            
        Returns:
            创建的记忆
        """
        memory = Memory(
            id=f"st_{self.agent_id}_{len(self.short_term)}",
            type=MemoryType.SHORT_TERM,
            content=content,
            importance=importance,
        )
        
        self.short_term.append(memory)
        self.memory_index[memory.id] = memory
        
        # 如果超过限制，转移重要记忆到长期
        if len(self.short_term) > self.max_short_term:
            self._consolidate_memories()
        
        return memory
    
    def add_long_term(self, content: Dict[str, Any], importance: float = 80.0) -> Memory:
        """
        添加长期记忆
        
        Args:
            content: 记忆内容
            importance: 重要度
            
        Returns:
            创建的记忆
        """
        memory = Memory(
            id=f"lt_{self.agent_id}_{len(self.long_term)}",
            type=MemoryType.LONG_TERM,
            content=content,
            importance=importance,
        )
        
        self.long_term.append(memory)
        self.memory_index[memory.id] = memory
        
        # 如果超过限制，删除最不重要的记忆
        if len(self.long_term) > self.max_long_term:
            self._forget_least_important()
        
        return memory
    
    def add_procedural(self, skill_name: str, skill_data: Any):
        """
        添加程序记忆（技能）
        
        Args:
            skill_name: 技能名称
            skill_data: 技能数据
        """
        self.procedural[skill_name] = skill_data
    
    def add_semantic(self, knowledge_key: str, knowledge_data: Any):
        """
        添加语义记忆（知识）
        
        Args:
            knowledge_key: 知识键
            knowledge_data: 知识数据
        """
        self.semantic[knowledge_key] = knowledge_data
    
    def retrieve(self, query: str, limit: int = 10) -> List[Memory]:
        """
        检索记忆
        
        Args:
            query: 查询关键词
            limit: 返回数量限制
            
        Returns:
            相关记忆列表
        """
        # 简单实现：基于内容匹配
        results = []
        
        for memory in self.short_term + self.long_term:
            content_str = json.dumps(memory.content).lower()
            if query.lower() in content_str:
                memory.access()
                results.append(memory)
        
        # 按重要度和最近访问排序
        results.sort(
            key=lambda m: m.importance * 0.7 + m.access_count * 0.3,
            reverse=True
        )
        
        return results[:limit]
    
    def associate_memories(self, memory_id_1: str, memory_id_2: str):
        """关联两个记忆"""
        if memory_id_1 in self.memory_index and memory_id_2 in self.memory_index:
            self.memory_index[memory_id_1].associate(memory_id_2)
            self.memory_index[memory_id_2].associate(memory_id_1)
    
    def _consolidate_memories(self):
        """将重要的短期记忆转移到长期记忆"""
        # 找出最重要的短期记忆
        important_memories = sorted(
            self.short_term,
            key=lambda m: m.importance,
            reverse=True
        )[:10]  # 转移前 10 个
        
        for memory in important_memories:
            if memory.importance >= 70:
                # 转移到长期记忆
                memory.type = MemoryType.LONG_TERM
                self.long_term.append(memory)
                self.short_term.remove(memory)
    
    def _forget_least_important(self):
        """删除最不重要的长期记忆"""
        if not self.long_term:
            return
        
        # 找出最不重要的记忆
        least_important = min(self.long_term, key=lambda m: m.importance)
        
        # 删除
        self.long_term.remove(least_important)
        del self.memory_index[least_important.id]
    
    def get_stats(self) -> Dict:
        """获取记忆统计"""
        return {
            "short_term_count": len(self.short_term),
            "long_term_count": len(self.long_term),
            "procedural_count": len(self.procedural),
            "semantic_count": len(self.semantic),
            "total_memories": len(self.memory_index),
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "agent_id": self.agent_id,
            "stats": self.get_stats(),
            "recent_memories": [
                m.to_dict() for m in sorted(
                    self.short_term + self.long_term,
                    key=lambda m: m.created_at,
                    reverse=True
                )[:20]
            ],
        }
