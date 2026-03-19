"""
Subagent Manager - 子代理管理器

负责创建、管理和监控子代理会话

功能:
- 创建子代理会话 (subagent 和 ACP 两种模式)
- 监控执行状态
- 收集结果
- 清理资源
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid
import sys

# 添加父目录到路径以便导入其他模块
sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('subagent-manager')


class SubagentMode(Enum):
    """子代理模式"""
    RUN = "run"      # 一次性执行
    SESSION = "session"  # 持久会话


class SubagentRuntime(Enum):
    """运行时类型"""
    SUBAGENT = "subagent"
    ACP = "acp"


@dataclass
class SubagentConfig:
    """子代理配置"""
    id: str
    name: str
    runtime: SubagentRuntime
    agent_id: str
    mode: SubagentMode
    task: str
    thread: bool = False
    timeout_seconds: Optional[int] = None
    label: Optional[str] = None
    created_at: str = ""
    status: str = "pending"
    result: Optional[Any] = None
    error: Optional[str] = None
    session_key: Optional[str] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'runtime': self.runtime.value,
            'agent_id': self.agent_id,
            'mode': self.mode.value,
            'task': self.task,
            'thread': self.thread,
            'timeout_seconds': self.timeout_seconds,
            'label': self.label,
            'created_at': self.created_at,
            'status': self.status,
            'result': self.result,
            'error': self.error,
            'session_key': self.session_key
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SubagentConfig':
        """从字典创建"""
        return cls(
            id=data['id'],
            name=data['name'],
            runtime=SubagentRuntime(data['runtime']),
            agent_id=data['agent_id'],
            mode=SubagentMode(data['mode']),
            task=data['task'],
            thread=data.get('thread', False),
            timeout_seconds=data.get('timeout_seconds'),
            label=data.get('label'),
            created_at=data.get('created_at', ''),
            status=data.get('status', 'pending'),
            result=data.get('result'),
            error=data.get('error'),
            session_key=data.get('session_key')
        )


class SubagentManager:
    """
    子代理管理器
    
    功能:
    - 创建子代理会话
    - 监控执行状态
    - 收集结果
    - 清理资源
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        初始化子代理管理器
        
        Args:
            config_path: 配置文件路径，默认为 configs/config.json
        """
        self.subagents: Dict[str, SubagentConfig] = {}
        self.history: List[Dict[str, Any]] = []
        self.config_path = config_path or (Path(__file__).parent.parent / "configs" / "config.json")
        
        # 从配置加载可用的 agentId 列表
        self.subagent_agents: List[str] = []
        self.acp_agents: List[str] = []
        
        self._load_config()
        self._load_state()
    
    def _load_config(self) -> None:
        """加载配置文件"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # 加载子代理配置
                subagent_config = config.get('subagent', {})
                
                # 预定义的可用代理
                self.subagent_agents = subagent_config.get('available_subagents', [
                    'research-assistant',
                    'message-aggregator',
                    'agent-coordinator',
                    'analyst',
                    'executor'
                ])
                
                self.acp_agents = subagent_config.get('available_acp_agents', [
                    'codex',
                    'claude-code',
                    'pi'
                ])
                
                logger.info(f"已加载配置：{len(self.subagent_agents)} 个子代理，{len(self.acp_agents)} 个 ACP 代理")
            except Exception as e:
                logger.warning(f"加载配置失败：{e}，使用默认值")
                self._set_default_agents()
        else:
            logger.warning("配置文件不存在，使用默认值")
            self._set_default_agents()
    
    def _set_default_agents(self) -> None:
        """设置默认代理列表"""
        self.subagent_agents = [
            'research-assistant',
            'message-aggregator',
            'agent-coordinator',
            'analyst',
            'executor'
        ]
        self.acp_agents = ['codex', 'claude-code', 'pi']
    
    def _load_state(self) -> None:
        """从持久化文件加载状态"""
        state_file = Path(__file__).parent.parent / "task-queue" / "subagents-state.json"
        
        if state_file.exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                
                # 加载子代理
                for sa_data in state.get('subagents', []):
                    try:
                        config = SubagentConfig.from_dict(sa_data)
                        self.subagents[config.id] = config
                    except Exception as e:
                        logger.error(f"加载子代理配置失败 {sa_data.get('id')}: {e}")
                
                # 加载历史
                self.history = state.get('history', [])
                
                logger.info(f"已恢复 {len(self.subagents)} 个子代理和 {len(self.history)} 条历史记录")
            except Exception as e:
                logger.error(f"加载状态失败：{e}")
    
    def _save_state(self) -> None:
        """保存状态到持久化文件"""
        state_file = Path(__file__).parent.parent / "task-queue" / "subagents-state.json"
        
        try:
            # 确保目录存在
            state_file.parent.mkdir(parents=True, exist_ok=True)
            
            state = {
                'subagents': [sa.to_dict() for sa in self.subagents.values()],
                'history': self.history,
                'updated_at': datetime.now().isoformat()
            }
            
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"已保存状态到 {state_file}")
        except Exception as e:
            logger.error(f"保存状态失败：{e}")
    
    def _select_subagent_for_task(self, task: str) -> str:
        """根据任务类型选择子代理"""
        task_lower = task.lower()
        
        # 关键词匹配
        if any(kw in task_lower for kw in ['研究', '搜索', '调查', 'research', 'search']):
            return 'research-assistant'
        elif any(kw in task_lower for kw in ['消息', '通知', '发送', 'message', 'notify']):
            return 'message-aggregator'
        elif any(kw in task_lower for kw in ['分析', 'analyze', 'report']):
            return 'analyst'
        elif any(kw in task_lower for kw in ['执行', '任务', 'execute', 'task']):
            return 'executor'
        else:
            return 'agent-coordinator'
    
    def _select_acp_for_task(self, task: str) -> str:
        """根据任务类型选择 ACP 代理"""
        task_lower = task.lower()
        
        # 编码相关任务
        if any(kw in task_lower for kw in ['代码', '编程', '开发', '实现', 'code', 'develop', 'implement']):
            return 'codex'
        elif any(kw in task_lower for kw in ['refactor', 'review', 'PR']):
            return 'claude-code'
        else:
            return 'pi'
    
    def _validate_agent_id(self, agent_id: str, runtime: SubagentRuntime) -> bool:
        """验证 agent_id 是否有效"""
        if runtime == SubagentRuntime.SUBAGENT:
            return agent_id in self.subagent_agents
        else:
            return agent_id in self.acp_agents
    
    def create_subagent(
        self,
        task: str,
        runtime: str = "subagent",
        agent_id: Optional[str] = None,
        mode: str = "session",
        thread: bool = False,
        timeout_seconds: Optional[int] = None,
        label: Optional[str] = None
    ) -> SubagentConfig:
        """
        创建子代理
        
        Args:
            task: 任务描述
            runtime: 运行时类型 (subagent/acp)
            agent_id: 代理 ID（可选，自动选择如果为 None）
            mode: 模式 (run/session)
            thread: 是否绑定到线程（仅 ACP + Discord）
            timeout_seconds: 超时时间（秒）
            label: 会话标签
            
        Returns:
            子代理配置对象
            
        Raises:
            ValueError: 如果参数无效
        """
        # 验证运行时类型
        try:
            runtime_enum = SubagentRuntime(runtime)
        except ValueError:
            raise ValueError(f"无效的运行时类型：{runtime}。有效值：subagent, acp")
        
        # 验证模式
        try:
            mode_enum = SubagentMode(mode)
        except ValueError:
            raise ValueError(f"无效的模式：{mode}。有效值：run, session")
        
        # 自动选择 agent_id 如果未提供
        if agent_id is None:
            if runtime_enum == SubagentRuntime.SUBAGENT:
                agent_id = self._select_subagent_for_task(task)
            else:
                agent_id = self._select_acp_for_task(task)
            logger.info(f"自动选择 agent_id: {agent_id}")
        
        # 验证 agent_id
        if not self._validate_agent_id(agent_id, runtime_enum):
            available = self.subagent_agents if runtime_enum == SubagentRuntime.SUBAGENT else self.acp_agents
            raise ValueError(f"无效的 agent_id: {agent_id}。可用值：{available}")
        
        # 生成唯一 ID
        subagent_id = f"sa_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        # 创建配置
        config = SubagentConfig(
            id=subagent_id,
            name=label or f"Subagent {len(self.subagents) + 1}",
            runtime=runtime_enum,
            agent_id=agent_id,
            mode=mode_enum,
            task=task,
            thread=thread,
            timeout_seconds=timeout_seconds,
            label=label
        )
        
        self.subagents[subagent_id] = config
        self._save_state()
        
        logger.info(f"已创建子代理：{config.name} ({subagent_id})")
        return config
    
    def execute_subagent(self, subagent_id: str) -> Dict[str, Any]:
        """
        执行子代理
        
        Args:
            subagent_id: 子代理 ID
            
        Returns:
            执行结果
        """
        if subagent_id not in self.subagents:
            return {'error': 'Subagent not found', 'subagent_id': subagent_id}
        
        config = self.subagents[subagent_id]
        
        if config.status == 'running':
            logger.warning(f"子代理已在运行：{subagent_id}")
            return {'error': 'Subagent already running', 'subagent_id': subagent_id}
        
        config.status = 'running'
        self._save_state()
        
        logger.info(f"开始执行子代理：{config.name} (task={config.task})")
        
        # TODO: 调用 OpenClaw sessions_spawn API
        # 这里模拟执行
        try:
            result = self._simulate_execution(config)
            
            config.status = 'completed'
            config.result = result
            config.error = None
            
            # 记录历史
            self.history.append({
                'subagent_id': subagent_id,
                'task': config.task,
                'status': 'completed',
                'completed_at': datetime.now().isoformat(),
                'result': result
            })
            
            self._save_state()
            
            logger.info(f"子代理执行完成：{subagent_id}")
            return result
            
        except Exception as e:
            config.status = 'failed'
            config.error = str(e)
            self._save_state()
            
            logger.error(f"子代理执行失败：{subagent_id} - {e}")
            return {
                'error': 'Execution failed',
                'subagent_id': subagent_id,
                'message': str(e)
            }
    
    def _simulate_execution(self, config: SubagentConfig) -> Dict[str, Any]:
        """
        模拟执行子代理
        
        在实际实现中，这里应该调用 OpenClaw 的 sessions_spawn API
        """
        import time
        time.sleep(0.1)  # 模拟执行延迟
        
        return {
            'status': 'completed',
            'subagent_id': config.id,
            'session_key': f"agent:{config.agent_id}:{config.id}",
            'result': f'模拟结果：{config.task}',
            'runtime': config.runtime.value,
            'mode': config.mode.value,
            'completed_at': datetime.now().isoformat()
        }
    
    def get_status(self, subagent_id: str) -> Dict[str, Any]:
        """获取子代理状态"""
        if subagent_id not in self.subagents:
            return {'error': 'Subagent not found', 'subagent_id': subagent_id}
        
        config = self.subagents[subagent_id]
        return config.to_dict()
    
    def list_subagents(self, active_only: bool = False) -> List[Dict[str, Any]]:
        """
        列出所有子代理
        
        Args:
            active_only: 是否只列出活跃的子代理
            
        Returns:
            子代理列表
        """
        subagents = []
        for sa_id, config in self.subagents.items():
            if active_only and config.status not in ['pending', 'running']:
                continue
            subagents.append(config.to_dict())
        
        # 按创建时间排序
        subagents.sort(key=lambda x: x['created_at'], reverse=True)
        return subagents
    
    def cleanup_completed(self, older_than_hours: int = 24) -> int:
        """
        清理已完成的子代理
        
        Args:
            older_than_hours: 清理超过多少小时的已完成子代理
            
        Returns:
            清理的数量
        """
        cleaned = 0
        now = datetime.now()
        
        for sa_id in list(self.subagents.keys()):
            config = self.subagents[sa_id]
            if config.status == 'completed':
                # 检查是否超过指定时间
                created = datetime.fromisoformat(config.created_at)
                age_hours = (now - created).total_seconds() / 3600
                if age_hours > older_than_hours:
                    # 移到历史后删除
                    self.history.append(config.to_dict())
                    del self.subagents[sa_id]
                    cleaned += 1
        
        if cleaned > 0:
            self._save_state()
        
        logger.info(f"已清理 {cleaned} 个已完成的子代理")
        return cleaned
    
    def get_summary(self) -> str:
        """获取摘要"""
        total = len(self.subagents)
        active = len([s for s in self.subagents.values() if s.status == 'running'])
        pending = len([s for s in self.subagents.values() if s.status == 'pending'])
        completed = len([s for s in self.subagents.values() if s.status == 'completed'])
        failed = len([s for s in self.subagents.values() if s.status == 'failed'])
        
        lines = [
            f"Subagent Manager Summary",
            f"",
            f"**Total**: {total}",
            f"**Active**: {active}",
            f"**Pending**: {pending}",
            f"**Completed**: {completed}",
            f"**Failed**: {failed}",
            f""
        ]
        
        if self.subagents:
            lines.append("**Recent Subagents**:")
            for sa_id, config in list(self.subagents.items())[-5:]:
                lines.append(f"  - {config.name}: {config.status} ({config.runtime.value}/{config.agent_id})")
        
        return '\n'.join(lines)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        total = len(self.subagents)
        status_counts = {}
        runtime_counts = {}
        
        for config in self.subagents.values():
            # 状态统计
            status_counts[config.status] = status_counts.get(config.status, 0) + 1
            
            # 运行时统计
            runtime_counts[config.runtime.value] = runtime_counts.get(config.runtime.value, 0) + 1
        
        return {
            'total': total,
            'by_status': status_counts,
            'by_runtime': runtime_counts,
            'history_count': len(self.history)
        }


def main():
    """测试子代理管理器"""
    print("="*60)
    print("Subagent Manager Test")
    print("="*60)
    
    manager = SubagentManager()
    
    # 创建子代理
    print("\n1. Creating subagents...")
    
    sa1 = manager.create_subagent(
        task="研究最新的 AI 技术进展",
        runtime="subagent",
        label="Research Agent"
    )
    print(f"   [OK] Created: {sa1.name} (agent={sa1.agent_id}, runtime={sa1.runtime.value})")
    
    sa2 = manager.create_subagent(
        task="编写一个 Python 脚本",
        runtime="acp",
        agent_id="codex",
        thread=True,
        label="Coding Agent"
    )
    print(f"   [OK] Created: {sa2.name} (agent={sa2.agent_id}, runtime={sa2.runtime.value}, thread={sa2.thread})")
    
    sa3 = manager.create_subagent(
        task="分析项目状态",
        runtime="subagent",
        mode="run",
        label="Analysis Agent"
    )
    print(f"   [OK] Created: {sa3.name} (agent={sa3.agent_id}, mode={sa3.mode.value})")
    
    # 执行子代理
    print("\n2. Executing subagents...")
    result1 = manager.execute_subagent(sa1.id)
    print(f"   [OK] Result: {result1['status']}")
    
    result2 = manager.execute_subagent(sa2.id)
    print(f"   [OK] Result: {result2['status']}")
    
    # 显示状态
    print("\n3. Subagent status:")
    for sa in manager.list_subagents():
        print(f"   - {sa['name']}: {sa['status']} ({sa['runtime']}/{sa['agent_id']})")
    
    # 统计信息
    print("\n4. Statistics:")
    stats = manager.get_statistics()
    print(f"   Total: {stats['total']}")
    print(f"   By status: {stats['by_status']}")
    print(f"   By runtime: {stats['by_runtime']}")
    
    # 摘要
    print("\n" + "="*60)
    print(manager.get_summary())


if __name__ == '__main__':
    main()
