#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多代理协作机制

功能:
- 任务分发
- 代理间通信
- 结果汇总
- 协作流程管理
"""

import asyncio
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import json
from pathlib import Path

# 添加项目路径
import sys
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents.registry import registry, AgentRegistry


class Task:
    """任务对象"""
    
    def __init__(self, task_id: str, description: str, assigned_to: str = None, 
                 priority: int = 5, timeout: int = 300):
        self.id = task_id
        self.description = description
        self.assigned_to = assigned_to
        self.priority = priority  # 1-10, 10 最高
        self.timeout = timeout  # 秒
        self.status = 'pending'  # pending, running, completed, failed
        self.result = None
        self.error = None
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.subtasks = []
        self.parent_task = None
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'description': self.description,
            'assigned_to': self.assigned_to,
            'priority': self.priority,
            'timeout': self.timeout,
            'status': self.status,
            'result': self.result,
            'error': self.error,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'subtasks': [st.to_dict() for st in self.subtasks]
        }
    
    def __repr__(self):
        return f"Task(id={self.id}, status={self.status}, assigned_to={self.assigned_to})"


class CollaborationEngine:
    """多代理协作引擎"""
    
    def __init__(self):
        self.registry = registry
        self.tasks: Dict[str, Task] = {}
        self.task_queue: List[Task] = []
        self.callbacks: Dict[str, List[Callable]] = {}
        self.execution_log = []
    
    def create_task(self, description: str, assigned_to: str = None, 
                   priority: int = 5, timeout: int = 300, 
                   subtasks: List[Dict] = None) -> Task:
        """创建任务"""
        task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.tasks)}"
        task = Task(task_id, description, assigned_to, priority, timeout)
        
        if subtasks:
            for i, st in enumerate(subtasks):
                subtask = Task(
                    f"{task_id}_st_{i}",
                    st.get('description', st.get('title', '')),
                    st.get('assigned_to'),
                    priority=priority - 1,
                    timeout=st.get('timeout', timeout // len(subtasks))
                )
                subtask.parent_task = task_id
                task.subtasks.append(subtask)
        
        self.tasks[task_id] = task
        self.task_queue.append(task)
        
        print(f"[Collaboration] ✅ 创建任务：{task_id}")
        print(f"  描述：{description}")
        print(f"  分配给：{assigned_to or '待定'}")
        print(f"  优先级：{priority}")
        
        return task
    
    def assign_task(self, task_id: str, agent_name: str):
        """分配任务给代理"""
        if task_id not in self.tasks:
            raise ValueError(f"任务不存在：{task_id}")
        
        task = self.tasks[task_id]
        task.assigned_to = agent_name
        task.status = 'assigned'
        
        print(f"[Collaboration] 📤 分配任务 {task_id} 给代理：{agent_name}")
    
    async def execute_task(self, task_id: str) -> Any:
        """执行任务"""
        if task_id not in self.tasks:
            raise ValueError(f"任务不存在：{task_id}")
        
        task = self.tasks[task_id]
        agent_name = task.assigned_to
        
        if not agent_name:
            # 自动分配合适的代理
            agent_name = self._find_best_agent(task.description)
            task.assigned_to = agent_name
        
        agent = self.registry.get(agent_name)
        if not agent:
            raise ValueError(f"代理不存在：{agent_name}")
        
        # 更新任务状态
        task.status = 'running'
        task.started_at = datetime.now()
        
        print(f"[Collaboration] ▶️ 执行任务：{task_id} by {agent_name}")
        
        try:
            # 执行任务
            if hasattr(agent, 'execute'):
                result = await asyncio.wait_for(
                    self._execute_agent_task(agent, task),
                    timeout=task.timeout
                )
            else:
                result = {"status": "success", "result": None}
            
            task.result = result
            task.status = 'completed'
            task.completed_at = datetime.now()
            
            # 更新统计
            self.registry.update_stats(agent_name, success=True)
            
            print(f"[Collaboration] ✅ 任务完成：{task_id}")
            
            # 触发回调
            await self._trigger_callbacks('task_completed', task)
            
            return result
            
        except asyncio.TimeoutError:
            task.error = "任务超时"
            task.status = 'failed'
            self.registry.update_stats(agent_name, success=False)
            print(f"[Collaboration] ❌ 任务超时：{task_id}")
            raise
            
        except Exception as e:
            task.error = str(e)
            task.status = 'failed'
            self.registry.update_stats(agent_name, success=False)
            print(f"[Collaboration] ❌ 任务失败：{task_id} - {e}")
            raise
        
        finally:
            # 记录执行日志
            self.execution_log.append({
                'task_id': task_id,
                'agent': agent_name,
                'status': task.status,
                'timestamp': datetime.now().isoformat()
            })
    
    async def _execute_agent_task(self, agent, task) -> Any:
        """执行代理任务"""
        if asyncio.iscoroutinefunction(agent.execute):
            return await agent.execute(task.description)
        else:
            return agent.execute(task.description)
    
    def _find_best_agent(self, task_description: str) -> str:
        """根据任务描述找到最合适的代理"""
        # 简单的关键词匹配（实际应该用 AI 分析）
        keywords_to_agents = {
            '搜索': 'researcher',
            '研究': 'researcher',
            '分析': 'analyst',
            '数据': 'analyst',
            '通知': 'notifier',
            '报告': 'reporter',
            '协调': 'coordinator',
            '任务': 'coordinator'
        }
        
        for keyword, agent_name in keywords_to_agents.items():
            if keyword in task_description:
                if self.registry.get(agent_name):
                    return agent_name
        
        # 默认返回 coordinator
        return 'coordinator'
    
    async def execute_workflow(self, workflow: List[Dict]) -> List[Any]:
        """执行工作流（多个任务的序列）"""
        results = []
        
        for i, task_def in enumerate(workflow):
            task = self.create_task(
                description=task_def.get('description', task_def.get('title', '')),
                assigned_to=task_def.get('assigned_to'),
                priority=task_def.get('priority', 5),
                timeout=task_def.get('timeout', 300)
            )
            
            try:
                result = await self.execute_task(task.id)
                results.append({
                    'task_id': task.id,
                    'status': 'success',
                    'result': result
                })
            except Exception as e:
                results.append({
                    'task_id': task.id,
                    'status': 'failed',
                    'error': str(e)
                })
                
                # 根据工作流策略决定是否继续
                if task_def.get('stop_on_failure', True):
                    break
        
        return results
    
    def register_callback(self, event: str, callback: Callable):
        """注册回调函数"""
        if event not in self.callbacks:
            self.callbacks[event] = []
        self.callbacks[event].append(callback)
        print(f"[Collaboration] 🔔 注册回调：{event}")
    
    async def _trigger_callbacks(self, event: str, *args):
        """触发回调"""
        if event in self.callbacks:
            for callback in self.callbacks[event]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(*args)
                    else:
                        callback(*args)
                except Exception as e:
                    print(f"[Collaboration] ⚠️ 回调执行失败 {event}: {e}")
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务"""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> Dict[str, Task]:
        """获取所有任务"""
        return self.tasks.copy()
    
    def get_task_status(self, task_id: str) -> Optional[str]:
        """获取任务状态"""
        task = self.tasks.get(task_id)
        return task.status if task else None
    
    def get_statistics(self) -> Dict:
        """获取协作引擎统计"""
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for t in self.tasks.values() if t.status == 'completed')
        failed_tasks = sum(1 for t in self.tasks.values() if t.status == 'failed')
        running_tasks = sum(1 for t in self.tasks.values() if t.status == 'running')
        pending_tasks = sum(1 for t in self.tasks.values() if t.status == 'pending')
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'failed_tasks': failed_tasks,
            'running_tasks': running_tasks,
            'pending_tasks': pending_tasks,
            'success_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            'registry_stats': self.registry.get_statistics()
        }
    
    def get_execution_log(self, limit: int = 100) -> List[Dict]:
        """获取执行日志"""
        return self.execution_log[-limit:]


# 全局协作引擎实例
collaboration = CollaborationEngine()


async def demo_collaboration():
    """演示多代理协作"""
    print("=" * 60)
    print("多代理协作演示")
    print("=" * 60)
    
    # 自动注册代理
    from agents.registry import auto_register_specialized_agents
    auto_register_specialized_agents()
    
    # 创建工作流
    workflow = [
        {
            'title': '研究 AI 发展趋势',
            'description': '研究 2026 年 AI 技术的最新发展趋势',
            'assigned_to': 'researcher',
            'priority': 8,
            'timeout': 60
        },
        {
            'title': '分析研究结果',
            'description': '分析研究员收集的数据',
            'assigned_to': 'analyst',
            'priority': 7,
            'timeout': 60
        },
        {
            'title': '生成研究报告',
            'description': '根据分析结果生成完整报告',
            'assigned_to': 'reporter',
            'priority': 6,
            'timeout': 60
        }
    ]
    
    # 执行工作流
    print("\n🚀 执行工作流...")
    results = await collaboration.execute_workflow(workflow)
    
    # 显示结果
    print("\n📊 工作流结果:")
    for result in results:
        status_icon = "✅" if result['status'] == 'success' else "❌"
        print(f"  {status_icon} {result['task_id']}: {result['status']}")
    
    # 显示统计
    print("\n📈 统计信息:")
    stats = collaboration.get_statistics()
    print(f"  总任务数：{stats['total_tasks']}")
    print(f"  完成：{stats['completed_tasks']}")
    print(f"  失败：{stats['failed_tasks']}")
    print(f"  成功率：{stats['success_rate']:.1f}%")
    
    return results


if __name__ == "__main__":
    # 运行演示
    asyncio.run(demo_collaboration())
