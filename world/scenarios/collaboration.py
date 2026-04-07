#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务协作场景 - 硅基世界 2

Agent 之间如何协作完成任务，展现团队合作精神。
"""

import asyncio
import random
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class CollaborationType(Enum):
    """协作类型"""
    PAIR_PROGRAMMING = "pair_programming"  # 结对编程
    CODE_REVIEW = "code_review"           # 代码审查
    BRAINSTORMING = "brainstorming"       # 头脑风暴
    PAIR_DEBUGGING = "pair_debugging"     # 结对调试
    KNOWLEDGE_TRANSFER = "knowledge_transfer"  # 知识传递


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    REVIEWING = "reviewing"
    COMPLETED = "completed"
    BLOCKED = "blocked"


@dataclass
class CollaborativeTask:
    """协作任务"""
    task_id: str
    name: str
    description: str
    collaborators: List[str]
    status: TaskStatus = TaskStatus.PENDING
    progress: int = 0  # 0-100
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    completed_at: Optional[float] = None
    notes: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "name": self.name,
            "description": self.description,
            "collaborators": self.collaborators,
            "status": self.status.value,
            "progress": self.progress,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "notes": self.notes,
        }


class CollaborationManager:
    """协作管理器"""
    
    def __init__(self):
        """初始化协作管理器"""
        self.tasks: Dict[str, CollaborativeTask] = {}
        self._task_counter = 0
        
        # 协作模板
        self.collaboration_templates = {
            CollaborationType.PAIR_PROGRAMMING: {
                "name": "结对编程",
                "description": "两名 Agent 一起编写代码，实时协作",
                "min_collaborators": 2,
            },
            CollaborationType.CODE_REVIEW: {
                "name": "代码审查",
                "description": "审查彼此的代码，提供改进建议",
                "min_collaborators": 2,
            },
            CollaborationType.BRAINSTORMING: {
                "name": "头脑风暴",
                "description": "集思广益，产生创新想法",
                "min_collaborators": 3,
            },
            CollaborationType.PAIR_DEBUGGING: {
                "name": "结对调试",
                "description": "一起定位和解决 bug",
                "min_collaborators": 2,
            },
            CollaborationType.KNOWLEDGE_TRANSFER: {
                "name": "知识传递",
                "description": "经验丰富的 Agent 传授知识给新手",
                "min_collaborators": 2,
            },
        }
    
    async def create_task(
        self,
        name: str,
        description: str,
        collaborators: List[str],
        collab_type: Optional[CollaborationType] = None,
    ) -> CollaborativeTask:
        """
        创建协作任务
        
        Args:
            name: 任务名称
            description: 任务描述
            collaborators: 协作者列表
            collab_type: 协作类型
            
        Returns:
            协作任务对象
        """
        self._task_counter += 1
        
        task = CollaborativeTask(
            task_id=f"collab_task_{self._task_counter}",
            name=name,
            description=description,
            collaborators=collaborators,
            status=TaskStatus.IN_PROGRESS,
        )
        
        self.tasks[task.task_id] = task
        
        collab_name = collab_type.value if collab_type else "general"
        print(f"🤝 协作任务创建：{name} ({collab_name})")
        print(f"   参与者：{', '.join(collaborators)}")
        
        return task
    
    async def update_progress(self, task_id: str, progress: int, note: Optional[str] = None) -> bool:
        """
        更新任务进度
        
        Args:
            task_id: 任务 ID
            progress: 进度 (0-100)
            note: 备注
            
        Returns:
            是否成功
        """
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        task.progress = min(100, max(0, progress))
        
        if note:
            task.notes.append(f"[{datetime.now().strftime('%H:%M')}] {note}")
        
        if task.progress >= 100:
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now().timestamp()
            print(f"✅ 协作任务完成：{task.name}")
        else:
            print(f"📊 任务进度更新：{task.name} - {task.progress}%")
        
        return True
    
    async def add_collaborator(self, task_id: str, agent_id: str) -> bool:
        """添加协作者"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        if agent_id not in task.collaborators:
            task.collaborators.append(agent_id)
            print(f"➕ {agent_id} 加入协作任务：{task.name}")
        
        return True
    
    async def complete_task(self, task_id: str, summary: str) -> bool:
        """完成任务"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        task.status = TaskStatus.COMPLETED
        task.progress = 100
        task.completed_at = datetime.now().timestamp()
        task.notes.append(f"✅ 完成总结：{summary}")
        
        print(f"🎉 协作任务完成：{task.name}")
        print(f"   总结：{summary}")
        
        return True
    
    def get_active_tasks(self) -> List[CollaborativeTask]:
        """获取活跃任务"""
        return [
            t for t in self.tasks.values()
            if t.status in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS, TaskStatus.REVIEWING]
        ]
    
    def get_completed_tasks(self) -> List[CollaborativeTask]:
        """获取已完成任务"""
        return [t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED]
    
    def get_agent_tasks(self, agent_id: str) -> List[CollaborativeTask]:
        """获取 Agent 参与的任务"""
        return [t for t in self.tasks.values() if agent_id in t.collaborators]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total": len(self.tasks),
            "active": len(self.get_active_tasks()),
            "completed": len(self.get_completed_tasks()),
            "by_type": "collaboration",
        }


# 单例
_collaboration_manager: Optional[CollaborationManager] = None


def get_collaboration_manager() -> CollaborationManager:
    """获取协作管理器单例"""
    global _collaboration_manager
    if _collaboration_manager is None:
        _collaboration_manager = CollaborationManager()
    return _collaboration_manager


def create_collaboration_manager() -> CollaborationManager:
    """创建协作管理器"""
    return CollaborationManager()
