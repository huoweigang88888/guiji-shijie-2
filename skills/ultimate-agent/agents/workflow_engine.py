"""
Workflow Engine - 工作流引擎

支持并行和串行两种执行模式的工作流引擎
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('workflow-engine')


class WorkflowMode(Enum):
    """工作流模式"""
    PARALLEL = "parallel"  # 并行执行
    SERIAL = "serial"      # 串行执行（阶段式）


class StageStatus(Enum):
    """阶段状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING_CONFIRM = "waiting_confirm"


@dataclass
class Stage:
    """工作流阶段"""
    id: str
    name: str
    agent: str
    input: Any
    output: Optional[Any] = None
    output_path: Optional[str] = None
    require_confirm: bool = False
    confirmed: bool = False
    status: StageStatus = StageStatus.PENDING
    timeout_minutes: int = 30
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None


@dataclass
class Workflow:
    """工作流"""
    id: str
    name: str
    description: str
    mode: WorkflowMode
    stages: List[Stage] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    created_at: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class WorkflowEngine:
    """
    工作流引擎
    
    支持并行和串行两种执行模式
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        初始化工作流引擎
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path or (Path(__file__).parent.parent / "configs" / "workflows.json")
        self.workflows: Dict[str, Workflow] = {}
        self.agent_executors: Dict[str, Callable] = {}
        
        # 加载配置
        self.config = self._load_config()
        
        logger.info(f"工作流引擎初始化完成，配置：{self.config_path}")
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'default_mode': 'parallel', 'workflows': {}}
    
    def register_agent(self, agent_name: str, executor: Callable) -> None:
        """
        注册代理执行器
        
        Args:
            agent_name: 代理名称
            executor: 执行函数
        """
        self.agent_executors[agent_name] = executor
        logger.info(f"已注册代理：{agent_name}")
    
    def create_workflow(self, workflow_name: str, user_input: str) -> Workflow:
        """
        创建工作流
        
        Args:
            workflow_name: 工作流名称
            user_input: 用户输入
            
        Returns:
            工作流对象
        """
        workflow_config = self.config.get('workflows', {}).get(workflow_name)
        
        if not workflow_config:
            raise ValueError(f"未知的工作流：{workflow_name}")
        
        workflow_id = f"wf_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        # 创建阶段
        stages = []
        for i, stage_config in enumerate(workflow_config.get('stages', [])):
            stage = Stage(
                id=f"stage_{i}",
                name=stage_config['name'],
                agent=stage_config['agent'],
                input=stage_config.get('input', user_input),
                output_path=stage_config.get('output_path'),
                require_confirm=stage_config.get('require_confirm', False),
                timeout_minutes=stage_config.get('timeout_minutes', 30)
            )
            stages.append(stage)
        
        workflow = Workflow(
            id=workflow_id,
            name=workflow_config.get('name', workflow_name),
            description=workflow_config.get('description', ''),
            mode=WorkflowMode(workflow_config.get('mode', 'parallel')),
            stages=stages,
            context={'user_input': user_input}
        )
        
        self.workflows[workflow_id] = workflow
        logger.info(f"已创建工作流：{workflow.name} ({workflow_id})")
        
        return workflow
    
    def execute_parallel(self, workflow: Workflow) -> Dict[str, Any]:
        """
        并行执行工作流
        
        Args:
            workflow: 工作流对象
            
        Returns:
            执行结果
        """
        logger.info(f"并行执行工作流：{workflow.name}")
        
        workflow.status = "running"
        workflow.started_at = datetime.now().isoformat()
        
        results = []
        
        # 并行执行所有阶段
        for stage in workflow.stages:
            stage.status = StageStatus.RUNNING
            stage.started_at = datetime.now().isoformat()
            
            try:
                # 执行阶段
                result = self._execute_stage(stage, workflow.context)
                stage.status = StageStatus.COMPLETED
                stage.output = result
                stage.completed_at = datetime.now().isoformat()
                
                results.append({
                    'stage': stage.name,
                    'status': 'completed',
                    'result': result
                })
                
            except Exception as e:
                stage.status = StageStatus.FAILED
                stage.error = str(e)
                stage.completed_at = datetime.now().isoformat()
                
                results.append({
                    'stage': stage.name,
                    'status': 'failed',
                    'error': str(e)
                })
        
        # 更新工作流状态
        all_completed = all(s.status == StageStatus.COMPLETED for s in workflow.stages)
        any_failed = any(s.status == StageStatus.FAILED for s in workflow.stages)
        
        if any_failed:
            workflow.status = "failed"
        elif all_completed:
            workflow.status = "completed"
            workflow.completed_at = datetime.now().isoformat()
        
        return {
            'workflow_id': workflow.id,
            'name': workflow.name,
            'status': workflow.status,
            'results': results
        }
    
    def execute_serial(self, workflow: Workflow, on_confirm: Optional[Callable] = None) -> Dict[str, Any]:
        """
        串行执行工作流（阶段式）
        
        Args:
            workflow: 工作流对象
            on_confirm: 用户确认回调函数
            
        Returns:
            执行结果
        """
        logger.info(f"串行执行工作流：{workflow.name}")
        
        workflow.status = "running"
        workflow.started_at = datetime.now().isoformat()
        
        results = []
        
        # 依次执行每个阶段
        for i, stage in enumerate(workflow.stages):
            logger.info(f"执行阶段 {i+1}/{len(workflow.stages)}: {stage.name}")
            
            stage.status = StageStatus.RUNNING
            stage.started_at = datetime.now().isoformat()
            
            try:
                # 准备输入（包含前一阶段的输出）
                if i > 0:
                    prev_stage = workflow.stages[i-1]
                    if prev_stage.output:
                        stage.input = {
                            'previous_output': prev_stage.output,
                            'user_input': workflow.context.get('user_input')
                        }
                
                # 执行阶段
                result = self._execute_stage(stage, workflow.context)
                stage.output = result
                stage.status = StageStatus.COMPLETED
                stage.completed_at = datetime.now().isoformat()
                
                results.append({
                    'stage': stage.name,
                    'status': 'completed',
                    'result': result,
                    'output_path': stage.output_path
                })
                
                # 如果需要用户确认
                if stage.require_confirm:
                    stage.status = StageStatus.WAITING_CONFIRM
                    
                    if on_confirm:
                        confirmed = on_confirm({
                            'stage': stage.name,
                            'result': result,
                            'output_path': stage.output_path
                        })
                        
                        if not confirmed:
                            logger.warning(f"用户未确认阶段 {stage.name}，工作流终止")
                            workflow.status = "waiting_confirm"
                            return {
                                'workflow_id': workflow.id,
                                'status': 'waiting_confirm',
                                'current_stage': stage.name,
                                'message': '等待用户确认'
                            }
                    
                    stage.confirmed = True
                    stage.status = StageStatus.COMPLETED
                
            except Exception as e:
                stage.status = StageStatus.FAILED
                stage.error = str(e)
                stage.completed_at = datetime.now().isoformat()
                
                workflow.status = "failed"
                return {
                    'workflow_id': workflow.id,
                    'status': 'failed',
                    'failed_stage': stage.name,
                    'error': str(e),
                    'results': results
                }
        
        # 所有阶段完成
        workflow.status = "completed"
        workflow.completed_at = datetime.now().isoformat()
        
        return {
            'workflow_id': workflow.id,
            'name': workflow.name,
            'status': 'completed',
            'total_stages': len(workflow.stages),
            'results': results
        }
    
    def _execute_stage(self, stage: Stage, context: Dict[str, Any]) -> Any:
        """
        执行单个阶段
        
        Args:
            stage: 阶段对象
            context: 上下文
            
        Returns:
            执行结果
        """
        agent_name = stage.agent
        
        # 查找代理执行器
        executor = self.agent_executors.get(agent_name)
        
        if not executor:
            logger.warning(f"代理 {agent_name} 未注册，使用模拟执行")
            return self._simulate_execution(stage)
        
        # 调用代理执行器
        if callable(executor):
            return executor(stage.input)
        else:
            return self._simulate_execution(stage)
    
    def _simulate_execution(self, stage: Stage) -> Dict[str, Any]:
        """模拟执行（用于测试）"""
        return {
            'status': 'completed',
            'stage': stage.name,
            'agent': stage.agent,
            'message': f'{stage.name} 已完成（模拟）',
            'timestamp': datetime.now().isoformat()
        }
    
    def execute_workflow(self, workflow_id: str, on_confirm: Optional[Callable] = None) -> Dict[str, Any]:
        """
        执行工作流
        
        Args:
            workflow_id: 工作流 ID
            on_confirm: 用户确认回调（串行模式）
            
        Returns:
            执行结果
        """
        if workflow_id not in self.workflows:
            return {'error': 'Workflow not found'}
        
        workflow = self.workflows[workflow_id]
        
        if workflow.mode == WorkflowMode.PARALLEL:
            return self.execute_parallel(workflow)
        else:
            return self.execute_serial(workflow, on_confirm)
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """获取工作流状态"""
        if workflow_id not in self.workflows:
            return {'error': 'Workflow not found'}
        
        workflow = self.workflows[workflow_id]
        
        stage_statuses = []
        for stage in workflow.stages:
            stage_statuses.append({
                'name': stage.name,
                'status': stage.status.value,
                'confirmed': stage.confirmed,
                'error': stage.error
            })
        
        return {
            'workflow_id': workflow.id,
            'name': workflow.name,
            'status': workflow.status,
            'mode': workflow.mode.value,
            'progress': f"{sum(1 for s in self.workflows[workflow_id].stages if s.status == StageStatus.COMPLETED)}/{len(workflow.stages)}",
            'stages': stage_statuses
        }
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """列出所有工作流"""
        return [
            {
                'id': wf.id,
                'name': wf.name,
                'status': wf.status,
                'mode': wf.mode.value,
                'stages': len(wf.stages)
            }
            for wf in self.workflows.values()
        ]
    
    def get_summary(self) -> str:
        """获取摘要"""
        workflows = self.list_workflows()
        
        lines = [
            f"Workflow Engine Summary",
            f"",
            f"**Total Workflows**: {len(workflows)}",
            f"**Registered Agents**: {len(self.agent_executors)}",
            f""
        ]
        
        if workflows:
            lines.append("**Workflows**:")
            for wf in workflows:
                lines.append(f"  - {wf['name']}: {wf['status']} ({wf['mode']}, {wf['stages']} stages)")
        
        return '\n'.join(lines)


def main():
    """测试工作流引擎"""
    print("="*60)
    print("工作流引擎测试")
    print("="*60)
    
    engine = WorkflowEngine()
    
    # 注册测试代理
    def test_executor(input_data):
        return {
            'status': 'completed',
            'input': input_data,
            'timestamp': datetime.now().isoformat()
        }
    
    engine.register_agent('product-manager', test_executor)
    engine.register_agent('ui-designer', test_executor)
    engine.register_agent('architect', test_executor)
    engine.register_agent('senior-dev', test_executor)
    
    # 创建工作流
    print("\n1. 创建软件开发工作流...")
    workflow = engine.create_workflow(
        'software_development',
        '开发一个待办事项应用'
    )
    print(f"   工作流 ID: {workflow.id}")
    print(f"   模式：{workflow.mode.value}")
    print(f"   阶段数：{len(workflow.stages)}")
    
    # 执行工作流
    print("\n2. 执行工作流...")
    result = engine.execute_workflow(workflow.id)
    print(f"   状态：{result.get('status')}")
    
    # 查看状态
    print("\n3. 工作流状态:")
    status = engine.get_workflow_status(workflow.id)
    for stage in status['stages']:
        print(f"   - {stage['name']}: {stage['status']}")
    
    # 摘要
    print("\n" + "="*60)
    print(engine.get_summary())


if __name__ == '__main__':
    main()
