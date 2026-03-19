"""
CEO Coordinator Agent - 首席执行官/协调者代理

负责战略决策、任务分发、资源协调和多代理协作管理
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ceo-coordinator')


class CEOCoordinatorAgent:
    """
    CEO 协调者代理
    
    职责:
    - 战略规划与目标设定
    - 任务分解与分发
    - 资源协调与调度
    - 进度跟踪与风险管理
    - 多代理协作编排
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "configs" / "company-agents.json"
        
        self.config_path = config_path
        self.config = self._load_config()
        
        self.workspace_dir = Path(__file__).parent.parent / "workspaces" / "main"
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        
        self.agent_registry = self._build_agent_registry()
        logger.info(f"CEO 协调者代理初始化完成，管理 {len(self.agent_registry)} 个代理")
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _build_agent_registry(self) -> Dict[str, Dict[str, Any]]:
        """构建代理注册表"""
        registry = {}
        for agent in self.config.get('agents', []):
            registry[agent['id']] = {
                'name': agent['name'],
                'role': agent['role'],
                'capabilities': agent['capabilities'],
                'workspace': agent.get('workspace', ''),
                'status': 'idle',
                'current_task': None
            }
        return registry
    
    def receive_task(self, task_description: str, priority: str = 'normal') -> Dict[str, Any]:
        """
        接收任务并分解分发
        
        Args:
            task_description: 任务描述
            priority: 优先级 (high/normal/low)
        
        Returns:
            任务分解结果
        """
        logger.info(f"接收新任务：{task_description[:50]}...")
        
        # 分析任务类型
        task_type = self._analyze_task_type(task_description)
        
        # 选择合适的 workflow
        workflow = self._select_workflow(task_type)
        
        if workflow:
            # 按工作流分解任务
            return self._execute_workflow(workflow, task_description)
        else:
            # 自定义任务分解
            return self._decompose_custom_task(task_description)
    
    def _analyze_task_type(self, task: str) -> str:
        """分析任务类型"""
        task_lower = task.lower()
        
        if any(kw in task_lower for kw in ['需求', '产品', 'prd', '用户']):
            return 'product'
        elif any(kw in task_lower for kw in ['开发', '代码', '实现', '功能']):
            return 'development'
        elif any(kw in task_lower for kw in ['设计', 'ui', '界面', '原型']):
            return 'design'
        elif any(kw in task_lower for kw in ['测试', 'bug', '质量']):
            return 'qa'
        elif any(kw in task_lower for kw in ['部署', '运维', '监控']):
            return 'devops'
        elif any(kw in task_lower for kw in ['数据', '分析', '报表']):
            return 'data'
        elif any(kw in task_lower for kw in ['招聘', 'hr', '人力']):
            return 'hr'
        elif any(kw in task_lower for kw in ['财务', '预算', '成本']):
            return 'finance'
        elif any(kw in task_lower for kw in ['市场', '营销', '推广']):
            return 'marketing'
        else:
            return 'general'
    
    def _select_workflow(self, task_type: str) -> Optional[Dict[str, Any]]:
        """选择合适的工作流"""
        workflow_map = {
            'product': 'workflow-new-product',
            'development': 'workflow-new-product',
            'design': 'workflow-new-product',
            'qa': 'workflow-bug-fix',
            'devops': 'workflow-bug-fix',
        }
        
        workflow_id = workflow_map.get(task_type)
        if workflow_id:
            for wf in self.config.get('workflows', []):
                if wf['id'] == workflow_id:
                    return wf
        return None
    
    def _execute_workflow(self, workflow: Dict[str, Any], task: str) -> Dict[str, Any]:
        """执行工作流"""
        logger.info(f"执行工作流：{workflow['name']}")
        
        steps = []
        for step in workflow.get('steps', []):
            agent_id = step['agent']
            agent_info = self.agent_registry.get(agent_id, {})
            
            steps.append({
                'step': step['task'],
                'agent': agent_info.get('name', agent_id),
                'status': 'pending'
            })
        
        result = {
            'success': True,
            'workflow': workflow['name'],
            'task': task,
            'steps': steps,
            'message': f"任务已分解为 {len(steps)} 个步骤，准备执行"
        }
        
        self._write_to_log('task_decomposed', result)
        return result
    
    def _decompose_custom_task(self, task: str) -> Dict[str, Any]:
        """自定义任务分解"""
        # 简单实现，实际应该用 AI 分析
        result = {
            'success': True,
            'workflow': 'custom',
            'task': task,
            'steps': [
                {'step': '分析需求', 'agent': '产品经理代理', 'status': 'pending'},
                {'step': '技术方案', 'agent': '架构师代理', 'status': 'pending'},
                {'step': '开发实现', 'agent': '高级开发代理', 'status': 'pending'},
                {'step': '测试验证', 'agent': '测试工程师代理', 'status': 'pending'}
            ],
            'message': "任务已分解，等待执行"
        }
        
        self._write_to_log('custom_task_decomposed', result)
        return result
    
    def get_agent_status(self) -> Dict[str, Any]:
        """获取所有代理状态"""
        status = {}
        for agent_id, info in self.agent_registry.items():
            status[agent_id] = {
                'name': info['name'],
                'role': info['role'],
                'status': info['status'],
                'current_task': info['current_task']
            }
        return status
    
    def assign_task_to_agent(self, agent_id: str, task: str) -> Dict[str, Any]:
        """分配任务给指定代理"""
        if agent_id not in self.agent_registry:
            return {'success': False, 'error': f'未知代理：{agent_id}'}
        
        self.agent_registry[agent_id]['status'] = 'busy'
        self.agent_registry[agent_id]['current_task'] = task
        
        result = {
            'success': True,
            'agent': self.agent_registry[agent_id]['name'],
            'task': task,
            'message': f"任务已分配给 {self.agent_registry[agent_id]['name']}"
        }
        
        self._write_to_log('task_assigned', result)
        return result
    
    def _write_to_log(self, key: str, value: Any) -> None:
        """写入日志"""
        log_file = self.workspace_dir / "ceo-log.md"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n## {timestamp} - {key}\n")
            f.write(f"```json\n{json.dumps(value, ensure_ascii=False, indent=2)}\n```\n")


def main():
    print("="*60)
    print("CEO 协调者代理测试")
    print("="*60)
    
    agent = CEOCoordinatorAgent()
    
    # 测试任务接收
    result = agent.receive_task("开发一个新的电商小程序，包含商品展示、购物车、支付功能")
    print(f"\n任务分解结果：{result['message']}")
    print(f"工作流：{result['workflow']}")
    print(f"步骤数：{len(result['steps'])}")
    
    # 获取代理状态
    status = agent.get_agent_status()
    print(f"\n活跃代理数：{len(status)}")


if __name__ == '__main__':
    main()
