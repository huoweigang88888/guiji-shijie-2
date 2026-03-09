"""
Agent Orchestration - 多代理协作编排

实现多代理任务分配、协作工作流、结果聚合
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import uuid

from agent_communication import AgentCommunication, Performative, ACLMessage

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('agent-orchestration')


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowState(Enum):
    """工作流状态"""
    NOT_STARTED = "not_started"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class SubTask:
    """子任务"""
    id: str
    title: str
    description: str
    assigned_to: str
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


@dataclass
class Workflow:
    """工作流"""
    id: str
    name: str
    description: str
    state: WorkflowState = WorkflowState.NOT_STARTED
    tasks: List[SubTask] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class AgentOrchestration:
    """
    代理编排系统
    
    功能:
    - 任务分解和分配
    - 工作流管理
    - 代理协作
    - 结果聚合
    """
    
    def __init__(self, communication: Optional[AgentCommunication] = None):
        """
        初始化编排系统
        
        Args:
            communication: 代理通信系统实例
        """
        self.comm = communication or AgentCommunication()
        
        # 工作流存储
        self.workflows: Dict[str, Workflow] = {}
        
        # 任务处理器
        self.task_handlers: Dict[str, Callable[[SubTask], Any]] = {}
        
        # 注册系统代理
        self._register_system_agents()
    
    def _register_system_agents(self) -> None:
        """注册系统代理"""
        # 协调器
        self.comm.register_agent("orchestrator", "orchestrator", [
            {"name": "create_workflow", "description": "Create and manage workflows"},
            {"name": "delegate_tasks", "description": "Delegate tasks to agents"}
        ])
        
        # 注册预定义代理
        pre_defined_agents = [
            ("coordinator", "coordinator", "Coordinate multi-agent tasks"),
            ("researcher", "researcher", "Research and analyze information"),
            ("messenger", "messenger", "Send and receive messages"),
            ("executor", "executor", "Execute tasks and actions"),
            ("analyst", "analyst", "Analyze data and generate reports")
        ]
        
        for agent_id, agent_type, desc in pre_defined_agents:
            self.comm.register_agent(agent_id, agent_type, [
                {"name": agent_type, "description": desc}
            ])
        
        logger.info(f"已注册 {len(pre_defined_agents) + 1} 个系统代理")
    
    def register_task_handler(
        self,
        agent_type: str,
        handler: Callable[[SubTask], Any]
    ) -> None:
        """
        注册任务处理器
        
        Args:
            agent_type: 代理类型
            handler: 处理函数
        """
        self.task_handlers[agent_type] = handler
        logger.info(f"已注册任务处理器：{agent_type}")
    
    def create_workflow(
        self,
        name: str,
        description: str,
        initial_context: Optional[Dict[str, Any]] = None
    ) -> Workflow:
        """
        创建工作流
        
        Args:
            name: 工作流名称
            description: 工作流描述
            initial_context: 初始上下文
            
        Returns:
            工作流对象
        """
        workflow_id = f"wf_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        workflow = Workflow(
            id=workflow_id,
            name=name,
            description=description,
            context=initial_context or {}
        )
        
        self.workflows[workflow_id] = workflow
        logger.info(f"已创建工作流：{name} ({workflow_id})")
        return workflow
    
    def decompose_task(
        self,
        workflow: Workflow,
        task_description: str,
        subtasks: List[Dict[str, str]]
    ) -> List[SubTask]:
        """
        分解任务为子任务
        
        Args:
            workflow: 工作流
            task_description: 任务描述
            subtasks: 子任务配置列表
            
        Returns:
            子任务列表
        """
        created_tasks = []
        
        for i, st in enumerate(subtasks):
            subtask = SubTask(
                id=f"task_{workflow.id}_{i}",
                title=st.get('title', f'Task {i+1}'),
                description=st.get('description', ''),
                assigned_to=st.get('assigned_to', 'executor')
            )
            
            workflow.tasks.append(subtask)
            created_tasks.append(subtask)
        
        logger.info(f"任务已分解为 {len(created_tasks)} 个子任务")
        return created_tasks
    
    def assign_task(self, subtask: SubTask, agent_id: str) -> bool:
        """
        分配任务给代理
        
        Args:
            subtask: 子任务
            agent_id: 代理 ID
            
        Returns:
            分配是否成功
        """
        if agent_id not in self.comm.agents:
            logger.error(f"代理不存在：{agent_id}")
            return False
        
        subtask.assigned_to = agent_id
        subtask.status = TaskStatus.ASSIGNED
        
        # 发送任务通知
        self.comm.send_message(
            sender="orchestrator",
            receivers=[agent_id],
            performative=Performative.REQUEST,
            content={
                'type': 'task_assignment',
                'task_id': subtask.id,
                'title': subtask.title,
                'description': subtask.description
            }
        )
        
        logger.info(f"任务已分配：{subtask.id} -> {agent_id}")
        return True
    
    def start_workflow(self, workflow_id: str) -> bool:
        """
        启动工作流
        
        Args:
            workflow_id: 工作流 ID
            
        Returns:
            启动是否成功
        """
        if workflow_id not in self.workflows:
            logger.error(f"工作流不存在：{workflow_id}")
            return False
        
        workflow = self.workflows[workflow_id]
        workflow.state = WorkflowState.RUNNING
        workflow.started_at = datetime.now().isoformat()
        
        # 分配所有待处理任务
        for task in workflow.tasks:
            if task.status == TaskStatus.PENDING:
                self.assign_task(task, task.assigned_to)
        
        logger.info(f"工作流已启动：{workflow.name}")
        return True
    
    def process_task(self, subtask: SubTask) -> Any:
        """
        处理任务
        
        Args:
            subtask: 子任务
            
        Returns:
            任务结果
        """
        subtask.status = TaskStatus.IN_PROGRESS
        subtask.started_at = datetime.now().isoformat()
        
        # 查找处理器
        agent = self.comm.agents.get(subtask.assigned_to)
        if not agent:
            subtask.status = TaskStatus.FAILED
            subtask.error = f"Agent not found: {subtask.assigned_to}"
            return None
        
        handler = self.task_handlers.get(agent.agent_type)
        
        if handler:
            try:
                result = handler(subtask)
                subtask.status = TaskStatus.COMPLETED
                subtask.result = result
                subtask.completed_at = datetime.now().isoformat()
                logger.info(f"任务完成：{subtask.id}")
                return result
            except Exception as e:
                subtask.status = TaskStatus.FAILED
                subtask.error = str(e)
                logger.error(f"任务失败：{subtask.id} - {e}")
                return None
        else:
            # 模拟执行
            subtask.status = TaskStatus.COMPLETED
            subtask.result = f"Task executed by {subtask.assigned_to}"
            subtask.completed_at = datetime.now().isoformat()
            logger.info(f"任务完成（模拟）：{subtask.id}")
            return subtask.result
    
    def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        执行工作流
        
        Args:
            workflow_id: 工作流 ID
            
        Returns:
            执行结果
        """
        if workflow_id not in self.workflows:
            return {'error': 'Workflow not found'}
        
        workflow = self.workflows[workflow_id]
        
        if not self.start_workflow(workflow_id):
            return {'error': 'Failed to start workflow'}
        
        results = []
        
        # 顺序执行任务
        for task in workflow.tasks:
            if task.status in [TaskStatus.PENDING, TaskStatus.ASSIGNED]:
                result = self.process_task(task)
                results.append({
                    'task_id': task.id,
                    'status': task.status.value,
                    'result': task.result,
                    'error': task.error
                })
        
        # 更新工作流状态
        all_completed = all(t.status == TaskStatus.COMPLETED for t in workflow.tasks)
        any_failed = any(t.status == TaskStatus.FAILED for t in workflow.tasks)
        
        if any_failed:
            workflow.state = WorkflowState.FAILED
        elif all_completed:
            workflow.state = WorkflowState.COMPLETED
            workflow.completed_at = datetime.now().isoformat()
        else:
            workflow.state = WorkflowState.WAITING
        
        return {
            'workflow_id': workflow.id,
            'name': workflow.name,
            'state': workflow.state.value,
            'total_tasks': len(workflow.tasks),
            'completed': len([t for t in workflow.tasks if t.status == TaskStatus.COMPLETED]),
            'failed': len([t for t in workflow.tasks if t.status == TaskStatus.FAILED]),
            'results': results
        }
    
    def aggregate_results(self, workflow_id: str) -> Dict[str, Any]:
        """
        聚合工作流结果
        
        Args:
            workflow_id: 工作流 ID
            
        Returns:
            聚合结果
        """
        if workflow_id not in self.workflows:
            return {'error': 'Workflow not found'}
        
        workflow = self.workflows[workflow_id]
        
        # 收集所有完成的任务结果
        completed_results = [
            t.result for t in workflow.tasks 
            if t.status == TaskStatus.COMPLETED and t.result is not None
        ]
        
        return {
            'workflow_id': workflow.id,
            'name': workflow.name,
            'total_tasks': len(workflow.tasks),
            'successful_results': len(completed_results),
            'aggregated_data': completed_results,
            'context': workflow.context
        }
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """获取工作流状态"""
        if workflow_id not in self.workflows:
            return {'error': 'Workflow not found'}
        
        workflow = self.workflows[workflow_id]
        
        task_stats = {}
        for task in workflow.tasks:
            status = task.status.value
            task_stats[status] = task_stats.get(status, 0) + 1
        
        return {
            'workflow_id': workflow.id,
            'name': workflow.name,
            'state': workflow.state.value,
            'progress': f"{task_stats.get('completed', 0)}/{len(workflow.tasks)}",
            'task_stats': task_stats,
            'tasks': [
                {
                    'id': t.id,
                    'title': t.title,
                    'assigned_to': t.assigned_to,
                    'status': t.status.value
                }
                for t in workflow.tasks
            ]
        }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """获取系统统计"""
        comm_stats = self.comm.get_system_stats()
        
        workflow_stats = {
            'total_workflows': len(self.workflows),
            'active_workflows': len([w for w in self.workflows.values() if w.state == WorkflowState.RUNNING]),
            'completed_workflows': len([w for w in self.workflows.values() if w.state == WorkflowState.COMPLETED])
        }
        
        return {
            'communication': comm_stats,
            'workflows': workflow_stats
        }
    
    def get_summary(self) -> str:
        """获取摘要"""
        stats = self.get_system_stats()
        
        lines = [
            f"Agent Orchestration System",
            f"",
            f"**Communication**:",
            f"  - Agents: {stats['communication']['total_agents']}",
            f"  - Conversations: {stats['communication']['total_conversations']}",
            f"",
            f"**Workflows**:",
            f"  - Total: {stats['workflows']['total_workflows']}",
            f"  - Active: {stats['workflows']['active_workflows']}",
            f"  - Completed: {stats['workflows']['completed_workflows']}",
            f""
        ]
        
        if self.workflows:
            lines.append("**Recent Workflows**:")
            for wf_id, wf in list(self.workflows.items())[-5:]:
                lines.append(f"  - {wf.name}: {wf.state.value}")
        
        return '\n'.join(lines)


def default_task_handler(subtask: SubTask) -> str:
    """默认任务处理器"""
    import time
    time.sleep(0.1)  # 模拟执行
    return f"Completed: {subtask.title}"


def main():
    """测试编排系统"""
    print("="*60)
    print("Agent Orchestration System Test")
    print("="*60)
    
    # 创建编排系统
    orchestration = AgentOrchestration()
    
    # 注册任务处理器
    orchestration.register_task_handler("researcher", default_task_handler)
    orchestration.register_task_handler("executor", default_task_handler)
    
    # 创建工作流
    print("\n1. Creating workflow...")
    workflow = orchestration.create_workflow(
        name="Research and Report",
        description="Research a topic and generate report",
        initial_context={"topic": "AI Trends"}
    )
    print(f"   Created: {workflow.name}")
    
    # 分解任务
    print("\n2. Decomposing task...")
    subtasks = [
        {"title": "Research AI trends", "description": "Search latest AI developments", "assigned_to": "researcher"},
        {"title": "Analyze findings", "description": "Analyze research results", "assigned_to": "analyst"},
        {"title": "Generate report", "description": "Create summary report", "assigned_to": "executor"}
    ]
    tasks = orchestration.decompose_task(workflow, "Research AI and create report", subtasks)
    print(f"   Decomposed into {len(tasks)} subtasks")
    
    # 执行工作流
    print("\n3. Executing workflow...")
    result = orchestration.execute_workflow(workflow.id)
    print(f"   State: {result['state']}")
    print(f"   Progress: {result['completed']}/{result['total_tasks']}")
    
    # 聚合结果
    print("\n4. Aggregating results...")
    aggregated = orchestration.aggregate_results(workflow.id)
    print(f"   Successful results: {aggregated['successful_results']}")
    
    # 显示状态
    print("\n5. Workflow status:")
    status = orchestration.get_workflow_status(workflow.id)
    for task in status['tasks']:
        print(f"   - {task['title']}: {task['status']} ({task['assigned_to']})")
    
    # 系统统计
    print("\n" + "="*60)
    print(orchestration.get_summary())


if __name__ == '__main__':
    main()
