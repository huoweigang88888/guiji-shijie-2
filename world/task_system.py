#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务系统 - 硅基世界 2

让 Agent 可以发布任务、接受任务、完成任务，形成协作网络。
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(Enum):
    """任务状态"""
    OPEN = "open"              # 开放中
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"    # 已完成
    CANCELLED = "cancelled"    # 已取消


class TaskPriority(Enum):
    """任务优先级"""
    LOW = "low"          # 低
    NORMAL = "normal"    # 普通
    HIGH = "high"        # 高
    URGENT = "urgent"    # 紧急


@dataclass
class Task:
    """任务"""
    task_id: str
    title: str
    description: str
    publisher: str  # 发布者
    assignee: Optional[str] = None  # 接受者
    status: TaskStatus = TaskStatus.OPEN
    priority: TaskPriority = TaskPriority.NORMAL
    reward: float = 0.0  # 奖励
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    progress: int = 0
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "publisher": self.publisher,
            "assignee": self.assignee,
            "status": self.status.value,
            "priority": self.priority.value,
            "reward": self.reward,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "progress": self.progress,
            "tags": self.tags,
        }


class TaskManager:
    """任务管理器"""
    
    def __init__(self):
        """初始化任务管理器"""
        self.tasks: Dict[str, Task] = {}
        self._task_counter = 0
        
        print("📋 任务系统已初始化")
    
    def create_task(
        self,
        title: str,
        description: str,
        publisher: str,
        reward: float = 10.0,
        priority: TaskPriority = TaskPriority.NORMAL,
        tags: Optional[List[str]] = None,
    ) -> Task:
        """
        创建任务
        
        Args:
            title: 任务标题
            description: 描述
            publisher: 发布者
            reward: 奖励
            priority: 优先级
            tags: 标签
            
        Returns:
            任务对象
        """
        self._task_counter += 1
        
        task = Task(
            task_id=f"task_{self._task_counter}",
            title=title,
            description=description,
            publisher=publisher,
            reward=reward,
            priority=priority,
            tags=tags or [],
        )
        
        self.tasks[task.task_id] = task
        
        print(f"  📋 {publisher} 发布了任务：{title} (奖励：{reward})")
        
        return task
    
    async def accept_task(self, task_id: str, assignee: str) -> bool:
        """
        接受任务
        
        Args:
            task_id: 任务 ID
            assignee: 接受者
            
        Returns:
            是否成功
        """
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        
        if task.status != TaskStatus.OPEN:
            print(f"  ❌ 任务 {task_id} 不可接受")
            return False
        
        task.assignee = assignee
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now().timestamp()
        
        print(f"  ✓ {assignee} 接受了任务：{task.title}")
        
        return True
    
    async def update_progress(self, task_id: str, progress: int) -> bool:
        """
        更新进度
        
        Args:
            task_id: 任务 ID
            progress: 进度 (0-100)
            
        Returns:
            是否成功
        """
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        task.progress = min(100, max(0, progress))
        
        if task.progress == 100:
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now().timestamp()
            print(f"  ✅ 任务完成：{task.title}")
        
        return True
    
    async def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        task.status = TaskStatus.CANCELLED
        
        print(f"  🚫 任务取消：{task.title}")
        
        return True
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务"""
        return self.tasks.get(task_id)
    
    def get_open_tasks(self) -> List[Task]:
        """获取开放任务"""
        return [t for t in self.tasks.values() if t.status == TaskStatus.OPEN]
    
    def get_agent_tasks(self, agent_id: str) -> List[Task]:
        """获取 Agent 的任务"""
        return [
            t for t in self.tasks.values()
            if t.publisher == agent_id or t.assignee == agent_id
        ]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total": len(self.tasks),
            "open": len([t for t in self.tasks.values() if t.status == TaskStatus.OPEN]),
            "in_progress": len([t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS]),
            "completed": len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED]),
            "cancelled": len([t for t in self.tasks.values() if t.status == TaskStatus.CANCELLED]),
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "open_tasks": [t.to_dict() for t in self.get_open_tasks()[:10]],
            "recent_completed": [
                t.to_dict() for t in sorted(
                    [t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED],
                    key=lambda x: x.completed_at or 0,
                    reverse=True
                )[:5]
            ],
        }


# 单例
_task_manager: Optional[TaskManager] = None


def get_task_manager() -> TaskManager:
    """获取任务管理器单例"""
    global _task_manager
    if _task_manager is None:
        _task_manager = TaskManager()
    return _task_manager


# 工厂函数
def create_task_manager() -> TaskManager:
    """创建任务管理器"""
    return TaskManager()
