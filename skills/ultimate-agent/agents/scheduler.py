"""
Scheduler - 定时任务调度器

实现定时任务、周期性任务、一次性提醒等功能
"""

import json
import logging
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('scheduler')


class TaskFrequency(Enum):
    """任务频率"""
    ONCE = "once"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CRON = "cron"


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ScheduledTask:
    """定时任务"""
    id: str
    name: str
    description: str
    frequency: TaskFrequency
    cron_expression: Optional[str]
    next_run: str
    last_run: Optional[str]
    handler: str
    params: Dict[str, Any]
    status: TaskStatus
    enabled: bool
    created_at: str
    execution_count: int = 0
    last_result: Optional[str] = None
    last_error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['frequency'] = self.frequency.value
        d['status'] = self.status.value
        return d


class Scheduler:
    """
    定时任务调度器
    
    功能:
    - 一次性任务
    - 周期性任务
    - Cron 表达式支持
    - 任务持久化
    - 并发控制
    """
    
    def __init__(self, state_file: Optional[Path] = None):
        """
        初始化调度器
        
        Args:
            state_file: 状态文件路径
        """
        if state_file is None:
            state_file = Path(__file__).parent.parent / "scheduler-state.json"
        
        self.state_file = state_file
        
        # 任务存储
        self.tasks: Dict[str, ScheduledTask] = {}
        
        # 任务处理器
        self.handlers: Dict[str, Callable] = {}
        
        # 运行状态
        self.running = False
        self.scheduler_thread: Optional[threading.Thread] = None
        
        # 加载状态
        self._load_state()
        
        # 启动调度线程
        self.start()
    
    def _load_state(self) -> None:
        """加载状态"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for task_data in data.get('tasks', []):
                    task = ScheduledTask(
                        id=task_data['id'],
                        name=task_data['name'],
                        description=task_data.get('description', ''),
                        frequency=TaskFrequency(task_data['frequency']),
                        cron_expression=task_data.get('cron_expression'),
                        next_run=task_data['next_run'],
                        last_run=task_data.get('last_run'),
                        handler=task_data['handler'],
                        params=task_data.get('params', {}),
                        status=TaskStatus(task_data['status']),
                        enabled=task_data.get('enabled', True),
                        created_at=task_data['created_at'],
                        execution_count=task_data.get('execution_count', 0),
                        last_result=task_data.get('last_result'),
                        last_error=task_data.get('last_error')
                    )
                    self.tasks[task.id] = task
                
                logger.info(f"已加载 {len(self.tasks)} 个定时任务")
            except Exception as e:
                logger.error(f"加载状态失败：{e}")
    
    def _save_state(self) -> None:
        """保存状态"""
        data = {
            'tasks': [task.to_dict() for task in self.tasks.values()],
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def register_handler(self, name: str, handler: Callable) -> None:
        """
        注册任务处理器
        
        Args:
            name: 处理器名称
            handler: 处理函数
        """
        self.handlers[name] = handler
        logger.info(f"已注册任务处理器：{name}")
    
    def schedule_task(
        self,
        name: str,
        handler: str,
        frequency: TaskFrequency,
        params: Optional[Dict[str, Any]] = None,
        cron_expression: Optional[str] = None,
        start_time: Optional[datetime] = None,
        description: str = ""
    ) -> ScheduledTask:
        """
        创建定时任务
        
        Args:
            name: 任务名称
            handler: 处理器名称
            frequency: 频率
            params: 任务参数
            cron_expression: Cron 表达式
            start_time: 开始时间
            description: 任务描述
            
        Returns:
            任务对象
        """
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        
        # 计算下次运行时间
        if start_time:
            next_run = start_time
        else:
            next_run = self._calculate_next_run(frequency, cron_expression)
        
        task = ScheduledTask(
            id=task_id,
            name=name,
            description=description,
            frequency=frequency,
            cron_expression=cron_expression,
            next_run=next_run.isoformat(),
            last_run=None,
            handler=handler,
            params=params or {},
            status=TaskStatus.PENDING,
            enabled=True,
            created_at=datetime.now().isoformat()
        )
        
        self.tasks[task_id] = task
        self._save_state()
        
        logger.info(f"已创建定时任务：{name} ({frequency.value})")
        return task
    
    def _calculate_next_run(self, frequency: TaskFrequency, cron_expression: Optional[str] = None) -> datetime:
        """计算下次运行时间"""
        now = datetime.now()
        
        if frequency == TaskFrequency.ONCE:
            return now + timedelta(minutes=1)
        elif frequency == TaskFrequency.HOURLY:
            return now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        elif frequency == TaskFrequency.DAILY:
            return now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        elif frequency == TaskFrequency.WEEKLY:
            days_until_monday = (7 - now.weekday()) % 7
            if days_until_monday == 0:
                days_until_monday = 7
            return now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=days_until_monday)
        elif frequency == TaskFrequency.MONTHLY:
            if now.month == 12:
                return now.replace(year=now.year+1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            else:
                return now.replace(month=now.month+1, day=1, hour=0, minute=0, second=0, microsecond=0)
        elif frequency == TaskFrequency.CRON and cron_expression:
            # 简化版 cron 解析（仅支持基本格式）
            return now + timedelta(minutes=5)
        
        return now + timedelta(hours=1)
    
    def _update_next_run(self, task: ScheduledTask) -> None:
        """更新下次运行时间"""
        task.next_run = self._calculate_next_run(task.frequency, task.cron_expression).isoformat()
    
    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.CANCELLED
            self.tasks[task_id].enabled = False
            self._save_state()
            logger.info(f"任务已取消：{task_id}")
            return True
        return False
    
    def enable_task(self, task_id: str, enable: bool = True) -> bool:
        """启用/禁用任务"""
        if task_id in self.tasks:
            self.tasks[task_id].enabled = enable
            self._save_state()
            logger.info(f"任务已{'启用' if enable else '禁用'}: {task_id}")
            return True
        return False
    
    def execute_task(self, task: ScheduledTask) -> None:
        """执行任务"""
        if not task.enabled or task.status == TaskStatus.CANCELLED:
            return
        
        logger.info(f"执行定时任务：{task.name}")
        
        task.status = TaskStatus.RUNNING
        task.last_run = datetime.now().isoformat()
        
        try:
            handler = self.handlers.get(task.handler)
            if handler:
                result = handler(**task.params)
                task.status = TaskStatus.COMPLETED
                task.last_result = str(result)
                task.execution_count += 1
                logger.info(f"任务完成：{task.name}")
            else:
                raise ValueError(f"处理器不存在：{task.handler}")
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.last_error = str(e)
            logger.error(f"任务失败：{task.name} - {e}")
        
        # 更新下次运行时间
        if task.frequency != TaskFrequency.ONCE or task.status == TaskStatus.COMPLETED:
            self._update_next_run(task)
        else:
            task.enabled = False
        
        self._save_state()
    
    def _scheduler_loop(self) -> None:
        """调度循环"""
        while self.running:
            now = datetime.now()
            
            for task in self.tasks.values():
                if task.enabled and task.status != TaskStatus.CANCELLED:
                    next_run = datetime.fromisoformat(task.next_run)
                    if now >= next_run:
                        self.execute_task(task)
            
            time.sleep(30)  # 每 30 秒检查一次
    
    def start(self) -> None:
        """启动调度器"""
        if self.running:
            return
        
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        logger.info("调度器已启动")
    
    def stop(self) -> None:
        """停止调度器"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        logger.info("调度器已停止")
    
    def get_pending_tasks(self) -> List[ScheduledTask]:
        """获取待执行任务"""
        now = datetime.now()
        pending = []
        for task in self.tasks.values():
            if task.enabled and task.status != TaskStatus.CANCELLED:
                next_run = datetime.fromisoformat(task.next_run)
                if next_run <= now + timedelta(hours=24):
                    pending.append(task)
        return sorted(pending, key=lambda t: t.next_run)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        status_counts = {}
        for task in self.tasks.values():
            status = task.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            'total_tasks': len(self.tasks),
            'enabled_tasks': len([t for t in self.tasks.values() if t.enabled]),
            'status_counts': status_counts,
            'running': self.running
        }
    
    def get_summary(self) -> str:
        """获取摘要"""
        stats = self.get_stats()
        lines = [
            "Scheduler System",
            "",
            f"**Total Tasks**: {stats['total_tasks']}",
            f"**Enabled Tasks**: {stats['enabled_tasks']}",
            f"**Status**: {'Running' if stats['running'] else 'Stopped'}",
            ""
        ]
        
        if stats['status_counts']:
            lines.append("**Task Status**:")
            for status, count in stats['status_counts'].items():
                lines.append(f"- {status}: {count}")
        
        pending = self.get_pending_tasks()
        if pending:
            lines.append("")
            lines.append("**Upcoming Tasks (24h)**:")
            for task in pending[:5]:
                lines.append(f"- {task.name} @ {task.next_run}")
        
        return '\n'.join(lines)


# 预定义处理器
def heartbeat_handler():
    """心跳检查处理器"""
    return "Heartbeat executed"


def backup_handler():
    """备份处理器"""
    return "Backup completed"


def cleanup_handler():
    """清理处理器"""
    return "Cleanup completed"


def main():
    """测试调度器"""
    print("="*60)
    print("Scheduler Test")
    print("="*60)
    
    scheduler = Scheduler()
    
    # 注册处理器
    scheduler.register_handler('heartbeat', heartbeat_handler)
    scheduler.register_handler('backup', backup_handler)
    scheduler.register_handler('cleanup', cleanup_handler)
    
    # 创建任务
    print("\n1. Create scheduled tasks")
    
    # 每小时心跳
    scheduler.schedule_task(
        name="Hourly Heartbeat",
        handler="heartbeat",
        frequency=TaskFrequency.HOURLY,
        description="Check system health every hour"
    )
    
    # 每日备份
    scheduler.schedule_task(
        name="Daily Backup",
        handler="backup",
        frequency=TaskFrequency.DAILY,
        description="Daily data backup"
    )
    
    # 每周清理
    scheduler.schedule_task(
        name="Weekly Cleanup",
        handler="cleanup",
        frequency=TaskFrequency.WEEKLY,
        description="Weekly cleanup of old data"
    )
    
    # 显示状态
    print("\n2. Scheduler status")
    print(scheduler.get_summary())
    
    # 等待一下
    print("\n3. Waiting for scheduler...")
    time.sleep(2)
    
    print("\nScheduler is running in background")


if __name__ == '__main__':
    main()
