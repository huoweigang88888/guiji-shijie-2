"""
Agent Coordinator - 多代理协调器

负责接收复杂任务，分解为子任务，分派给专用代理，并整合结果。
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('agent-coordinator')


class AgentCoordinator:
    """
    多代理协调器
    
    职责:
    - 接收复杂任务并分解为子任务
    - 根据子任务类型分派给合适的 specialized agent
    - 收集各 agent 的输出并整合
    - 监控任务进度和状态
    """
    
    def __init__(self, agents_dir: Optional[Path] = None):
        """
        初始化协调器
        
        Args:
            agents_dir: 代理配置目录，默认为当前脚本所在目录的 agents 子目录
        """
        if agents_dir is None:
            agents_dir = Path(__file__).parent / "agents"
        
        self.agents_dir = agents_dir
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.task_history: List[Dict[str, Any]] = []
        
        # 加载已知代理配置
        self._load_agents()
    
    def _load_agents(self) -> None:
        """从配置目录加载所有代理配置"""
        if not self.agents_dir.exists():
            logger.warning(f"代理目录不存在：{self.agents_dir}")
            return
        
        for config_file in self.agents_dir.glob("*.json"):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    agent_config = json.load(f)
                    agent_name = agent_config.get('name', config_file.stem)
                    self.agents[agent_name] = agent_config
                    logger.info(f"已加载代理：{agent_name}")
            except Exception as e:
                logger.error(f"加载代理配置失败 {config_file}: {e}")
    
    def analyze_task(self, task_description: str) -> Dict[str, Any]:
        """
        分析任务并确定需要的代理类型
        
        Args:
            task_description: 任务描述
            
        Returns:
            任务分析结果，包括:
            - complexity: 任务复杂度 (simple/medium/complex)
            - required_agents: 需要的代理列表
            - subtasks: 分解后的子任务
        """
        # 简单的基于关键词的任务分析
        # TODO: 实现更智能的 NLP 分析
        
        task_lower = task_description.lower()
        
        # 判断任务类型
        required_agents = []
        subtasks = []
        
        # 研究类任务
        research_keywords = ['研究', '搜索', '调查', '分析', '调研', 'research', 'search']
        if any(kw in task_lower for kw in research_keywords):
            required_agents.append('research-assistant')
            subtasks.append({
                'type': 'research',
                'agent': 'research-assistant',
                'description': f'研究和分析：{task_description}'
            })
        
        # 消息类任务
        message_keywords = ['消息', '通知', '发送', '接收', 'whatsapp', 'telegram', 'message']
        if any(kw in task_lower for kw in message_keywords):
            required_agents.append('message-aggregator')
            subtasks.append({
                'type': 'message',
                'agent': 'message-aggregator',
                'description': f'消息处理：{task_description}'
            })
        
        # 如果没有匹配到特定代理，标记为通用任务
        if not required_agents:
            required_agents.append('agent-coordinator')
            subtasks.append({
                'type': 'general',
                'agent': 'agent-coordinator',
                'description': task_description
            })
        
        # 判断复杂度
        complexity = 'simple'
        if len(required_agents) > 1:
            complexity = 'complex'
        elif len(subtasks) > 2:
            complexity = 'medium'
        
        analysis_result = {
            'complexity': complexity,
            'required_agents': required_agents,
            'subtasks': subtasks,
            'original_task': task_description,
            'analyzed_at': datetime.now().isoformat()
        }
        
        logger.info(f"任务分析完成：复杂度={complexity}, 代理数={len(required_agents)}")
        return analysis_result
    
    def delegate_task(self, subtask: Dict[str, Any]) -> Dict[str, Any]:
        """
        将子任务分派给对应的代理
        
        Args:
            subtask: 子任务描述
            
        Returns:
            代理执行结果
        """
        agent_name = subtask.get('agent')
        
        if agent_name not in self.agents:
            logger.error(f"未知代理：{agent_name}")
            return {
                'status': 'error',
                'error': f'代理不存在：{agent_name}',
                'subtask': subtask
            }
        
        agent_config = self.agents[agent_name]
        logger.info(f"分派任务给代理：{agent_config.get('displayName', agent_name)}")
        
        # TODO: 实际调用代理执行逻辑
        # 目前返回模拟结果
        return {
            'status': 'completed',
            'agent': agent_name,
            'result': f'代理 {agent_name} 已完成任务：{subtask.get("description")}',
            'executed_at': datetime.now().isoformat()
        }
    
    def execute_task(self, task_description: str) -> Dict[str, Any]:
        """
        执行完整任务流程：分析 -> 分派 -> 整合
        
        Args:
            task_description: 任务描述
            
        Returns:
            任务执行结果
        """
        logger.info(f"开始执行任务：{task_description}")
        
        # 1. 分析任务
        analysis = self.analyze_task(task_description)
        
        # 2. 分派和执行子任务
        results = []
        for subtask in analysis['subtasks']:
            logger.info(f"执行子任务：{subtask['description']}")
            result = self.delegate_task(subtask)
            results.append(result)
        
        # 3. 整合结果
        final_result = self._synthesize_results(analysis, results)
        
        # 4. 记录任务历史
        task_record = {
            'task': task_description,
            'analysis': analysis,
            'results': results,
            'final_result': final_result,
            'completed_at': datetime.now().isoformat()
        }
        self.task_history.append(task_record)
        
        return final_result
    
    def _synthesize_results(self, analysis: Dict[str, Any], results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        整合多个代理的执行结果
        
        Args:
            analysis: 任务分析结果
            results: 各代理执行结果
            
        Returns:
            整合后的最终结果
        """
        # 检查是否有失败的任务
        failed_tasks = [r for r in results if r.get('status') == 'error']
        successful_tasks = [r for r in results if r.get('status') == 'completed']
        
        # 整合成功结果
        combined_output = []
        for result in successful_tasks:
            combined_output.append(result.get('result', ''))
        
        return {
            'status': 'failed' if failed_tasks else 'completed',
            'summary': ' | '.join(combined_output),
            'successful_tasks': len(successful_tasks),
            'failed_tasks': len(failed_tasks),
            'details': results
        }
    
    def get_status(self) -> Dict[str, Any]:
        """获取协调器当前状态"""
        return {
            'loaded_agents': list(self.agents.keys()),
            'total_tasks_executed': len(self.task_history),
            'status': 'active'
        }


def main():
    """测试协调器功能"""
    coordinator = AgentCoordinator()
    
    # 测试任务
    test_tasks = [
        "研究一下最新的 AI 技术进展",
        "发送消息给团队成员",
        "帮我分析这个项目的状态"
    ]
    
    for task in test_tasks:
        print(f"\n{'='*60}")
        print(f"任务：{task}")
        print('='*60)
        
        result = coordinator.execute_task(task)
        print(f"结果：{result['summary']}")
    
    # 显示状态
    print(f"\n{'='*60}")
    print("协调器状态:")
    print('='*60)
    status = coordinator.get_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
