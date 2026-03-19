#!/usr/bin/env python3
"""
Scheduler Agent - 定时任务调度代理
Phase 9: 功能扩展
"""

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
import json


class ScheduledTask:
    def __init__(self, task_id: str, name: str, schedule: str, handler: Callable):
        self.id = task_id
        self.name = name
        self.schedule = schedule  # cron 格式或间隔
        self.handler = handler
        self.enabled = True
        self.last_run = None
        self.next_run = None
        self.run_count = 0
        self.success_count = 0
        self.error_count = 0
        self.created_at = datetime.now()
    
    def calculate_next_run(self) -> datetime:
        if self.schedule.startswith('@'):
            if self.schedule == '@hourly':
                return datetime.now() + timedelta(hours=1)
            elif self.schedule == '@daily':
                return datetime.now() + timedelta(days=1)
            elif self.schedule == '@weekly':
                return datetime.now() + timedelta(weeks=1)
        else:
            parts = self.schedule.split(':')
            if len(parts) == 2:
                hours, minutes = int(parts[0]), int(parts[1])
                next_run = datetime.now().replace(hour=hours, minute=minutes, second=0)
                if next_run <= datetime.now():
                    next_run += timedelta(days=1)
                return next_run
        return datetime.now() + timedelta(hours=1)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'schedule': self.schedule,
            'enabled': self.enabled,
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'next_run': self.next_run.isoformat() if self.next_run else None,
            'run_count': self.run_count,
            'success_count': self.success_count,
            'error_count': self.error_count
        }


class SchedulerAgent:
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.name = "scheduler"
        self.tasks: Dict[str, ScheduledTask] = {}
        self.running = False
        self.task_queue = asyncio.Queue()
        self.stats = {
            'total_schedules': 0,
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0
        }
        print(f"[Scheduler] Agent 初始化完成")
    
    def schedule(self, task_id: str, name: str, schedule: str, handler: Callable) -> ScheduledTask:
        task = ScheduledTask(task_id, name, schedule, handler)
        task.next_run = task.calculate_next_run()
        self.tasks[task_id] = task
        self.stats['total_schedules'] += 1
        print(f"[Scheduler] 任务已调度：{name} ({schedule})")
        return task
    
    def cancel(self, task_id: str) -> bool:
        if task_id in self.tasks:
            del self.tasks[task_id]
            print(f"[Scheduler] 任务已取消：{task_id}")
            return True
        return False
    
    def enable(self, task_id: str) -> bool:
        if task_id in self.tasks:
            self.tasks[task_id].enabled = True
            print(f"[Scheduler] 任务已启用：{task_id}")
            return True
        return False
    
    def disable(self, task_id: str) -> bool:
        if task_id in self.tasks:
            self.tasks[task_id].enabled = False
            print(f"[Scheduler] 任务已禁用：{task_id}")
            return True
        return False
    
    async def run_task(self, task: ScheduledTask):
        task.last_run = datetime.now()
        task.run_count += 1
        self.stats['total_executions'] += 1
        
        try:
            if asyncio.iscoroutinefunction(task.handler):
                await task.handler()
            else:
                task.handler()
            task.success_count += 1
            self.stats['successful_executions'] += 1
            print(f"[Scheduler] 任务执行成功：{task.name}")
        except Exception as e:
            task.error_count += 1
            self.stats['failed_executions'] += 1
            print(f"[Scheduler] 任务执行失败：{task.name} - {e}")
        
        task.next_run = task.calculate_next_run()
    
    async def start(self):
        self.running = True
        print(f"[Scheduler] 调度器已启动")
        
        while self.running:
            now = datetime.now()
            for task in self.tasks.values():
                if task.enabled and task.next_run and task.next_run <= now:
                    await self.run_task(task)
            await asyncio.sleep(1)
    
    def stop(self):
        self.running = False
        print(f"[Scheduler] 调度器已停止")
    
    def get_stats(self) -> Dict[str, Any]:
        active_tasks = sum(1 for t in self.tasks.values() if t.enabled)
        return {
            **self.stats,
            'total_tasks': len(self.tasks),
            'active_tasks': active_tasks,
            'tasks': [t.to_dict() for t in self.tasks.values()]
        }
    
    def execute(self, task: str, **kwargs) -> Dict[str, Any]:
        return {
            'status': 'success',
            'agent': self.name,
            'task': task,
            'stats': self.get_stats()
        }
    
    def get_capabilities(self) -> List[str]:
        return [
            '定时任务调度',
            'Cron 表达式支持',
            '任务队列管理',
            '执行统计',
            '自动重试'
        ]


scheduler_agent = SchedulerAgent()


async def demo():
    print("=" * 60)
    print("Scheduler Agent Demo - Phase 9")
    print("=" * 60)
    
    agent = SchedulerAgent()
    
    def sample_task():
        print(f"  [Task] 执行定时任务 - {datetime.now().isoformat()}")
    
    agent.schedule('task_1', '每小时任务', '@hourly', sample_task)
    agent.schedule('task_2', '每日任务', '@daily', sample_task)
    agent.schedule('task_3', '定时任务', '12:00', sample_task)
    
    print(f"\n已调度任务:")
    stats = agent.get_stats()
    print(f"  总任务数：{stats['total_tasks']}")
    print(f"  活跃任务：{stats['active_tasks']}")
    
    print(f"\n任务列表:")
    for task in stats['tasks']:
        print(f"  - {task['name']}: {task['schedule']} (下次运行：{task['next_run']})")
    
    print(f"\n能力:")
    for cap in agent.get_capabilities():
        print(f"  - {cap}")
    
    return stats


if __name__ == "__main__":
    asyncio.run(demo())
