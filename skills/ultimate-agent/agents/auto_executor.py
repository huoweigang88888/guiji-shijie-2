"""
Auto Executor - 自动任务执行系统

基于目标自动生成任务、执行任务、跟踪进度
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('auto-executor')


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class TaskPriority(Enum):
    """任务优先级"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Task:
    """任务对象"""
    id: str
    title: str
    description: str
    priority: TaskPriority
    status: TaskStatus
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    output: Optional[str] = None
    error: Optional[str] = None
    parent_goal: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        return cls(**data)


@dataclass
class Goal:
    """目标对象"""
    id: str
    title: str
    description: str
    status: str  # active/completed/archived
    created_at: str
    completed_at: Optional[str] = None
    tasks: List[str] = None  # 任务 ID 列表
    
    def __post_init__(self):
        if self.tasks is None:
            self.tasks = []
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Goal':
        return cls(**data)


class AutoExecutor:
    """
    自动任务执行系统
    
    职责:
    - 管理目标（Goals）
    - 根据目标生成任务
    - 执行任务
    - 跟踪进度
    - 生成报告
    """
    
    def __init__(self, state_dir: Optional[Path] = None):
        """
        初始化自动执行器
        
        Args:
            state_dir: 状态文件目录
        """
        if state_dir is None:
            state_dir = Path(__file__).parent.parent
        
        self.state_dir = state_dir
        self.goals_file = state_dir / "goals.json"
        self.tasks_file = state_dir / "tasks.json"
        self.history_file = state_dir / "task-history.json"
        
        # 目标和任务
        self.goals: Dict[str, Goal] = {}
        self.tasks: Dict[str, Task] = {}
        self.task_history: List[Dict[str, Any]] = []
        
        # 任务执行器（回调函数）
        self.task_executors: Dict[str, Callable[[Task], str]] = {}
        
        # 加载状态
        self._load_state()
    
    def _load_state(self) -> None:
        """加载状态文件"""
        # 加载目标
        if self.goals_file.exists():
            try:
                with open(self.goals_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.goals = {
                        k: Goal.from_dict(v) for k, v in data.get('goals', {}).items()
                    }
                logger.info(f"已加载 {len(self.goals)} 个目标")
            except Exception as e:
                logger.error(f"加载目标失败：{e}")
                self.goals = {}
        else:
            self.goals = {}
        
        # 加载任务
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = {
                        k: Task.from_dict(v) for k, v in data.get('tasks', {}).items()
                    }
                logger.info(f"已加载 {len(self.tasks)} 个任务")
            except Exception as e:
                logger.error(f"加载任务失败：{e}")
                self.tasks = {}
        else:
            self.tasks = {}
        
        # 加载历史
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.task_history = data.get('history', [])
            except:
                self.task_history = []
    
    def _save_state(self) -> None:
        """保存状态文件"""
        # 保存目标
        with open(self.goals_file, 'w', encoding='utf-8') as f:
            json.dump({
                'goals': {k: v.to_dict() for k, v in self.goals.items()},
                'last_updated': datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        
        # 保存任务
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump({
                'tasks': {k: v.to_dict() for k, v in self.tasks.items()},
                'last_updated': datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
    
    def _save_history(self) -> None:
        """保存任务历史"""
        # 限制历史记录数量
        if len(self.task_history) > 100:
            self.task_history = self.task_history[-100:]
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump({
                'history': self.task_history,
                'last_updated': datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
    
    def add_goal(self, title: str, description: str) -> Goal:
        """
        添加新目标
        
        Args:
            title: 目标标题
            description: 目标描述
            
        Returns:
            创建的目标对象
        """
        goal_id = f"goal_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.goals)}"
        
        goal = Goal(
            id=goal_id,
            title=title,
            description=description,
            status='active',
            created_at=datetime.now().isoformat()
        )
        
        self.goals[goal_id] = goal
        self._save_state()
        
        logger.info(f"已添加目标：{title}")
        return goal
    
    def complete_goal(self, goal_id: str) -> bool:
        """完成目标"""
        if goal_id not in self.goals:
            logger.error(f"目标不存在：{goal_id}")
            return False
        
        goal = self.goals[goal_id]
        goal.status = 'completed'
        goal.completed_at = datetime.now().isoformat()
        
        self._save_state()
        logger.info(f"目标已完成：{goal.title}")
        return True
    
    def generate_tasks(self, goal_id: str, task_descriptions: List[Dict[str, str]]) -> List[Task]:
        """
        为目标生成任务
        
        Args:
            goal_id: 目标 ID
            task_descriptions: 任务描述列表，每项包含 title/description/priority
            
        Returns:
            创建的任务列表
        """
        if goal_id not in self.goals:
            logger.error(f"目标不存在：{goal_id}")
            return []
        
        goal = self.goals[goal_id]
        created_tasks = []
        
        for desc in task_descriptions:
            task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.tasks)}"
            
            task = Task(
                id=task_id,
                title=desc.get('title', '未命名任务'),
                description=desc.get('description', ''),
                priority=TaskPriority(desc.get('priority', 'normal')),
                status=TaskStatus.PENDING,
                created_at=datetime.now().isoformat(),
                parent_goal=goal_id
            )
            
            self.tasks[task_id] = task
            goal.tasks.append(task_id)
            created_tasks.append(task)
        
        self._save_state()
        logger.info(f"已为目标 {goal.title} 生成 {len(created_tasks)} 个任务")
        return created_tasks
    
    def register_executor(self, task_type: str, executor: Callable[[Task], str]) -> None:
        """
        注册任务执行器
        
        Args:
            task_type: 任务类型
            executor: 执行函数，接收 Task 对象，返回结果字符串
        """
        self.task_executors[task_type] = executor
        logger.info(f"已注册任务执行器：{task_type}")
    
    def execute_task(self, task_id: str) -> bool:
        """
        执行单个任务
        
        Args:
            task_id: 任务 ID
            
        Returns:
            执行是否成功
        """
        if task_id not in self.tasks:
            logger.error(f"任务不存在：{task_id}")
            return False
        
        task = self.tasks[task_id]
        
        if task.status != TaskStatus.PENDING:
            logger.warning(f"任务状态不允许执行：{task.status}")
            return False
        
        # 更新状态
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now().isoformat()
        self._save_state()
        
        logger.info(f"开始执行任务：{task.title}")
        
        try:
            # 查找执行器
            executor = self.task_executors.get('default')
            
            if executor:
                result = executor(task)
                task.status = TaskStatus.COMPLETED
                task.output = result
                task.completed_at = datetime.now().isoformat()
                
                # 记录历史
                self.task_history.append({
                    'task': task.to_dict(),
                    'result': result,
                    'completed_at': task.completed_at
                })
                self._save_history()
                
                logger.info(f"任务完成：{task.title}")
            else:
                # 没有执行器，模拟完成
                task.status = TaskStatus.COMPLETED
                task.output = "任务已标记完成（无执行器）"
                task.completed_at = datetime.now().isoformat()
                logger.warning(f"任务无执行器，已标记完成：{task.title}")
            
            self._save_state()
            return True
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            self._save_state()
            logger.error(f"任务执行失败：{task.title} - {e}")
            return False
    
    def execute_pending_tasks(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        执行所有待处理任务
        
        Args:
            limit: 最大执行任务数，None 表示执行所有
            
        Returns:
            执行结果统计
        """
        pending_tasks = [
            t for t in self.tasks.values()
            if t.status == TaskStatus.PENDING
        ]
        
        # 按优先级排序
        priority_order = {
            TaskPriority.CRITICAL: 0,
            TaskPriority.HIGH: 1,
            TaskPriority.NORMAL: 2,
            TaskPriority.LOW: 3
        }
        pending_tasks.sort(key=lambda t: priority_order[t.priority])
        
        if limit:
            pending_tasks = pending_tasks[:limit]
        
        results = {
            'total': len(pending_tasks),
            'completed': 0,
            'failed': 0,
            'details': []
        }
        
        for task in pending_tasks:
            success = self.execute_task(task.id)
            if success:
                results['completed'] += 1
            else:
                results['failed'] += 1
            
            results['details'].append({
                'task_id': task.id,
                'title': task.title,
                'status': task.status.value,
                'success': success
            })
        
        return results
    
    def get_progress(self, goal_id: Optional[str] = None) -> Dict[str, Any]:
        """
        获取进度
        
        Args:
            goal_id: 目标 ID，None 表示获取总体进度
            
        Returns:
            进度信息
        """
        if goal_id:
            if goal_id not in self.goals:
                return {'error': '目标不存在'}
            
            goal = self.goals[goal_id]
            goal_tasks = [self.tasks[tid] for tid in goal.tasks if tid in self.tasks]
            
            if not goal_tasks:
                return {
                    'goal': goal.title,
                    'total': 0,
                    'completed': 0,
                    'pending': 0,
                    'progress_percent': 0
                }
            
            completed = len([t for t in goal_tasks if t.status == TaskStatus.COMPLETED])
            total = len(goal_tasks)
            
            return {
                'goal': goal.title,
                'total': total,
                'completed': completed,
                'pending': total - completed,
                'progress_percent': round(completed / total * 100, 1) if total > 0 else 0
            }
        else:
            # 总体进度
            total = len(self.tasks)
            completed = len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED])
            pending = len([t for t in self.tasks.values() if t.status == TaskStatus.PENDING])
            in_progress = len([t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS])
            failed = len([t for t in self.tasks.values() if t.status == TaskStatus.FAILED])
            
            return {
                'total': total,
                'completed': completed,
                'pending': pending,
                'in_progress': in_progress,
                'failed': failed,
                'progress_percent': round(completed / total * 100, 1) if total > 0 else 0,
                'active_goals': len([g for g in self.goals.values() if g.status == 'active'])
            }
    
    def get_summary(self) -> str:
        """获取执行摘要"""
        progress = self.get_progress()
        
        lines = [
            f"📋 自动任务执行摘要",
            f"",
            f"**总任务数**: {progress.get('total', 0)}",
            f"**已完成**: {progress.get('completed', 0)}",
            f"**待处理**: {progress.get('pending', 0)}",
            f"**进行中**: {progress.get('in_progress', 0)}",
            f"**失败**: {progress.get('failed', 0)}",
            f"**进度**: {progress.get('progress_percent', 0)}%",
            f"**活跃目标**: {progress.get('active_goals', 0)}",
            f""
        ]
        
        # 显示待处理任务
        pending = [t for t in self.tasks.values() if t.status == TaskStatus.PENDING]
        if pending:
            lines.append("**待处理任务**:")
            for task in pending[:5]:  # 最多显示 5 个
                priority_icon = "🔴" if task.priority == TaskPriority.CRITICAL else "🟠" if task.priority == TaskPriority.HIGH else "⚪"
                lines.append(f"- {priority_icon} {task.title}")
            if len(pending) > 5:
                lines.append(f"- ... 还有 {len(pending) - 5} 个任务")
        
        return '\n'.join(lines)


def default_task_executor(task: Task) -> str:
    """默认任务执行器（模拟）"""
    import time
    time.sleep(0.1)  # 模拟执行时间
    return f"任务 \"{task.title}\" 已完成"


def main():
    """测试自动执行器"""
    executor = AutoExecutor()
    
    # 注册默认执行器
    executor.register_executor('default', default_task_executor)
    
    print("="*60)
    print("🤖 硅基世界 2 - 自动任务执行系统")
    print("="*60)
    
    # 添加测试目标
    print("\n1. 添加目标...")
    goal = executor.add_goal(
        title="学习 Python 高级特性",
        description="掌握 Python 高级编程技巧"
    )
    print(f"   已添加：{goal.title}")
    
    # 生成任务
    print("\n2. 生成任务...")
    tasks = executor.generate_tasks(goal.id, [
        {'title': '学习装饰器', 'description': '理解@decorator 语法', 'priority': 'high'},
        {'title': '学习生成器', 'description': '掌握 yield 关键字', 'priority': 'normal'},
        {'title': '学习上下文管理器', 'description': '理解 with 语句', 'priority': 'normal'},
        {'title': '学习元类', 'description': '深入理解 metaclass', 'priority': 'low'},
    ])
    print(f"   已生成 {len(tasks)} 个任务")
    
    # 执行任务
    print("\n3. 执行任务...")
    results = executor.execute_pending_tasks()
    print(f"   执行完成：{results['completed']}/{results['total']}")
    
    # 显示进度
    print("\n4. 进度:")
    progress = executor.get_progress(goal.id)
    print(f"   {progress['goal']}: {progress['progress_percent']}% ({progress['completed']}/{progress['total']})")
    
    # 显示摘要
    print("\n" + "="*60)
    print(executor.get_summary())


if __name__ == '__main__':
    main()
