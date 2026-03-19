#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务队列优化器 - Task Queue Optimizer

功能：
- 优先级队列
- 任务依赖管理
- 并发控制
- 任务重试机制

提供高效的任务调度和执行管理。
"""

import json
import logging
import time
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass, asdict, field
from enum import Enum
import heapq

logger = logging.getLogger('task-queue')


class TaskPriority(Enum):
    """任务优先级"""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    URGENT = 3


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskDependency(Enum):
    """依赖类型"""
    NONE = "none"
    SEQUENTIAL = "sequential"  # 顺序执行
    PARALLEL = "parallel"      # 并行执行
    CONDITIONAL = "conditional"  # 条件执行


@dataclass(order=True)
class Task:
    """任务对象"""
    priority: int
    task_id: str = field(compare=False)
    title: str = field(compare=False)
    description: str = field(compare=False, default="")
    status: str = field(compare=False, default=TaskStatus.PENDING.value)
    handler: str = field(compare=False, default="")
    params: Dict[str, Any] = field(compare=False, default=None)
    dependencies: List[str] = field(compare=False, default=None)
    dependency_type: str = field(compare=False, default=TaskDependency.NONE.value)
    retry_count: int = field(compare=False, default=0)
    max_retries: int = field(compare=False, default=3)
    created_at: str = field(compare=False, default=None)
    started_at: str = field(compare=False, default=None)
    completed_at: str = field(compare=False, default=None)
    error: Optional[str] = field(compare=False, default=None)
    result: Any = field(compare=False, default=None)
    
    def __post_init__(self):
        if self.params is None:
            self.params = {}
        if self.dependencies is None:
            self.dependencies = []
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """从字典创建"""
        return cls(**data)


class TaskQueue:
    """
    优先级任务队列
    
    支持：
    - 优先级排序
    - 任务依赖
    - 并发控制
    - 自动重试
    """
    
    def __init__(self, max_concurrent: int = 5, persist_dir: Path = None):
        self.max_concurrent = max_concurrent
        self.persist_dir = persist_dir or Path(__file__).parent.parent / "task-queue"
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        
        # 任务存储
        self.tasks: Dict[str, Task] = {}
        self.priority_queue: List[Task] = []
        self.completed_tasks: Set[str] = set()
        self.failed_tasks: Set[str] = set()
        
        # 执行器
        self.handlers: Dict[str, Callable] = {}
        self.running_tasks: Set[str] = set()
        
        # 锁
        self.lock = threading.RLock()
        
        # 状态
        self._running = False
        self._worker_thread: Optional[threading.Thread] = None
        
        # 统计
        self.stats = {
            "total_submitted": 0,
            "total_completed": 0,
            "total_failed": 0,
            "total_retried": 0
        }
        
        self._load_state()
    
    def _load_state(self):
        """加载持久化状态"""
        state_file = self.persist_dir / "queue_state.json"
        if state_file.exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for task_data in data.get('tasks', []):
                    task = Task.from_dict(task_data)
                    self.tasks[task.task_id] = task
                    
                    if task.status == TaskStatus.COMPLETED.value:
                        self.completed_tasks.add(task.task_id)
                    elif task.status == TaskStatus.FAILED.value:
                        self.failed_tasks.add(task.task_id)
                
                self.stats = data.get('stats', self.stats)
                logger.info(f"已加载 {len(self.tasks)} 个任务")
            except Exception as e:
                logger.error(f"加载状态失败：{e}")
    
    def _save_state(self):
        """保存持久化状态"""
        state_file = self.persist_dir / "queue_state.json"
        data = {
            'tasks': [task.to_dict() for task in self.tasks.values()],
            'stats': self.stats,
            'saved_at': datetime.now().isoformat()
        }
        
        try:
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存状态失败：{e}")
    
    def register_handler(self, name: str, handler: Callable):
        """注册任务处理器"""
        self.handlers[name] = handler
        logger.info(f"已注册处理器：{name}")
    
    def submit(self, task: Task) -> str:
        """
        提交任务
        
        Args:
            task: 任务对象
            
        Returns:
            任务 ID
        """
        with self.lock:
            # 生成任务 ID
            if not task.task_id:
                task.task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.tasks)}"
            
            # 设置优先级
            if task.priority is None:
                task.priority = TaskPriority.NORMAL.value
            
            # 保存任务
            self.tasks[task.task_id] = task
            self.stats["total_submitted"] += 1
            
            # 加入队列
            if task.status == TaskStatus.PENDING.value:
                task.status = TaskStatus.QUEUED.value
                heapq.heappush(self.priority_queue, task)
            
            self._save_state()
            logger.info(f"任务已提交：{task.task_id} (优先级：{task.priority})")
            
            return task.task_id
    
    def submit_batch(self, tasks: List[Task]) -> List[str]:
        """批量提交任务"""
        return [self.submit(task) for task in tasks]
    
    def _can_execute(self, task: Task) -> bool:
        """检查任务是否可以执行"""
        # 检查依赖
        for dep_id in task.dependencies:
            if dep_id not in self.completed_tasks:
                return False
        
        # 检查并发限制
        if len(self.running_tasks) >= self.max_concurrent:
            return False
        
        return True
    
    def _execute_task(self, task: Task):
        """执行任务"""
        task.status = TaskStatus.RUNNING.value
        task.started_at = datetime.now().isoformat()
        self.running_tasks.add(task.task_id)
        
        logger.info(f"执行任务：{task.task_id} - {task.title}")
        
        try:
            # 获取处理器
            if not task.handler or task.handler not in self.handlers:
                raise ValueError(f"未知处理器：{task.handler}")
            
            handler = self.handlers[task.handler]
            
            # 执行
            result = handler(task.params)
            
            # 成功
            task.status = TaskStatus.COMPLETED.value
            task.result = result
            task.completed_at = datetime.now().isoformat()
            self.completed_tasks.add(task.task_id)
            self.stats["total_completed"] += 1
            
            logger.info(f"任务完成：{task.task_id}")
            
        except Exception as e:
            task.error = str(e)
            task.retry_count += 1
            self.stats["total_retried"] += 1
            
            if task.retry_count < task.max_retries:
                # 重试
                task.status = TaskStatus.QUEUED.value
                logger.warning(f"任务失败，将重试 ({task.retry_count}/{task.max_retries}): {task.task_id}")
            else:
                # 失败
                task.status = TaskStatus.FAILED.value
                task.completed_at = datetime.now().isoformat()
                self.failed_tasks.add(task.task_id)
                self.stats["total_failed"] += 1
                logger.error(f"任务失败：{task.task_id} - {e}")
        
        finally:
            self.running_tasks.remove(task.task_id)
            self._save_state()
    
    def _worker_loop(self):
        """工作线程循环"""
        logger.info("任务队列工作线程启动")
        
        while self._running:
            executed = False
            
            with self.lock:
                # 尝试执行任务
                temp_queue = []
                
                while self.priority_queue:
                    task = heapq.heappop(self.priority_queue)
                    
                    if self._can_execute(task):
                        # 启动执行
                        threading.Thread(target=self._execute_task, args=(task,)).start()
                        executed = True
                        break
                    else:
                        # 暂时不能执行，稍后重试
                        temp_queue.append(task)
                
                # 恢复队列
                for task in temp_queue:
                    heapq.heappush(self.priority_queue, task)
            
            if not executed:
                time.sleep(0.5)  # 避免空转
        
        logger.info("任务队列工作线程停止")
    
    def start(self):
        """启动队列"""
        if not self._running:
            self._running = True
            self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
            self._worker_thread.start()
            logger.info("任务队列已启动")
    
    def stop(self):
        """停止队列"""
        self._running = False
        if self._worker_thread:
            self._worker_thread.join(timeout=5)
        logger.info("任务队列已停止")
    
    def cancel(self, task_id: str) -> bool:
        """取消任务"""
        with self.lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                if task.status in [TaskStatus.PENDING.value, TaskStatus.QUEUED.value]:
                    task.status = TaskStatus.CANCELLED.value
                    task.completed_at = datetime.now().isoformat()
                    self._save_state()
                    logger.info(f"任务已取消：{task_id}")
                    return True
        return False
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务"""
        return self.tasks.get(task_id)
    
    def get_queue_status(self) -> Dict[str, Any]:
        """获取队列状态"""
        with self.lock:
            pending = sum(1 for t in self.tasks.values() if t.status == TaskStatus.QUEUED.value)
            running = len(self.running_tasks)
            completed = len(self.completed_tasks)
            failed = len(self.failed_tasks)
            
            return {
                "pending": pending,
                "running": running,
                "completed": completed,
                "failed": failed,
                "total": len(self.tasks),
                "max_concurrent": self.max_concurrent,
                "stats": self.stats
            }
    
    def clear_completed(self):
        """清理已完成的任务"""
        with self.lock:
            to_remove = [tid for tid in self.completed_tasks if tid in self.tasks]
            for tid in to_remove:
                del self.tasks[tid]
            self.completed_tasks.clear()
            self._save_state()
            logger.info(f"已清理 {len(to_remove)} 个已完成任务")


# 便捷函数
def create_task(
    title: str,
    handler: str,
    params: Dict[str, Any] = None,
    priority: TaskPriority = TaskPriority.NORMAL,
    dependencies: List[str] = None,
    max_retries: int = 3,
    task_id: str = None
) -> Task:
    """创建任务"""
    return Task(
        priority=priority.value,
        task_id=task_id,
        title=title,
        handler=handler,
        params=params or {},
        dependencies=dependencies or [],
        max_retries=max_retries
    )


if __name__ == "__main__":
    # 测试
    logging.basicConfig(level=logging.INFO)
    
    # 创建队列
    queue = TaskQueue(max_concurrent=3)
    
    # 注册处理器
    def sample_handler(params):
        print(f"执行任务：{params}")
        time.sleep(1)
        return {"status": "success"}
    
    queue.register_handler("sample", sample_handler)
    
    # 提交任务
    task1 = create_task("任务 1", "sample", {"id": 1})
    task2 = create_task("任务 2", "sample", {"id": 2}, priority=TaskPriority.HIGH)
    task3 = create_task("任务 3", "sample", {"id": 3}, dependencies=[task1.task_id])
    
    queue.submit(task1)
    queue.submit(task2)
    queue.submit(task3)
    
    # 启动队列
    queue.start()
    
    # 等待执行
    time.sleep(5)
    
    # 查看状态
    print("\n队列状态:")
    print(json.dumps(queue.get_queue_status(), indent=2, ensure_ascii=False))
    
    # 停止队列
    queue.stop()
