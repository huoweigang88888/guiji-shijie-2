# 子代理模式实现指南

**创建时间**: 2026-03-17  
**版本**: 1.0.0  
**状态**: 🆕 新增功能

---

## 📋 概述

子代理模式允许主代理动态创建和管理隔离的子会话，用于：

- **任务隔离** - 不同任务在不同会话中执行
- **专业化** - 为特定任务类型创建专用子代理
- **并行处理** - 多个子代理同时工作
- **上下文管理** - 避免主会话上下文污染

---

## 🎯 两种运行时模式

### 1. Subagent 模式 (runtime="subagent")

**用途**: 创建 OpenClaw 内部子代理会话

**特点**:
- 使用 `agents_list` 中的 agentId
- 隔离的会话状态
- 可通过 `sessions_send` 通信
- 适合长期运行的任务

**示例**:
```python
{
    "runtime": "subagent",
    "agentId": "research-assistant",  # 从 agents_list 获取
    "mode": "session",  # 或 "run"
    "task": "研究 AI 发展趋势"
}
```

### 2. ACP 模式 (runtime="acp")

**用途**: 调用外部 AI 编码代理（Codex、Claude Code、Pi 等）

**特点**:
- 使用 `acp.allowedAgents` 中的 agentId
- 需要显式指定 agentId（除非配置了 acp.defaultAgent）
- 适合编码任务
- 在 Discord 上默认使用 thread-bound 持久会话

**示例**:
```python
{
    "runtime": "acp",
    "agentId": "codex",  # 从 acp.allowedAgents 获取
    "mode": "session",
    "thread": true,  # Discord 线程绑定
    "task": "实现一个新功能"
}
```

---

## 🚀 实现步骤

### 步骤 1: 创建子代理管理器

在 `ultimate-agent/agents/` 目录下创建 `subagent_manager.py`:

```python
"""
Subagent Manager - 子代理管理器

负责创建、管理和监控子代理会话
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid

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
    created_at: str = ""
    status: str = "pending"
    result: Optional[Any] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class SubagentManager:
    """
    子代理管理器
    
    功能:
    - 创建子代理会话
    - 监控执行状态
    - 收集结果
    - 清理资源
    """
    
    def __init__(self):
        """初始化子代理管理器"""
        self.subagents: Dict[str, SubagentConfig] = {}
        self.history: List[Dict[str, Any]] = []
        
        # 从配置加载可用的 agentId 列表
        self._load_available_agents()
    
    def _load_available_agents(self) -> None:
        """加载可用的代理列表"""
        # TODO: 通过 OpenClaw API 获取 agents_list
        self.subagent_agents = [
            "research-assistant",
            "message-aggregator",
            "agent-coordinator"
        ]
        
        # TODO: 通过 OpenClaw API 获取 acp.allowedAgents
        self.acp_agents = [
            "codex",
            "claude-code",
            "pi"
        ]
        
        logger.info(f"已加载 {len(self.subagent_agents)} 个子代理和 {len(self.acp_agents)} 个 ACP 代理")
    
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
        """
        # 验证运行时类型
        try:
            runtime_enum = SubagentRuntime(runtime)
        except ValueError:
            raise ValueError(f"无效的运行时类型：{runtime}")
        
        # 自动选择 agent_id 如果未提供
        if agent_id is None:
            if runtime_enum == SubagentRuntime.SUBAGENT:
                agent_id = self._select_subagent_for_task(task)
            else:
                agent_id = self._select_acp_for_task(task)
        
        # 验证 agent_id
        if not self._validate_agent_id(agent_id, runtime_enum):
            raise ValueError(f"无效的 agent_id: {agent_id} (runtime={runtime})")
        
        # 生成唯一 ID
        subagent_id = f"sa_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        # 创建配置
        config = SubagentConfig(
            id=subagent_id,
            name=label or f"Subagent {len(self.subagents) + 1}",
            runtime=runtime_enum,
            agent_id=agent_id,
            mode=SubagentMode(mode),
            task=task,
            thread=thread,
            timeout_seconds=timeout_seconds
        )
        
        self.subagents[subagent_id] = config
        logger.info(f"已创建子代理：{config.name} ({subagent_id})")
        
        return config
    
    def _select_subagent_for_task(self, task: str) -> str:
        """根据任务类型选择子代理"""
        task_lower = task.lower()
        
        # 简单关键词匹配
        if any(kw in task_lower for kw in ['研究', '搜索', '调查', 'research']):
            return 'research-assistant'
        elif any(kw in task_lower for kw in ['消息', '通知', 'message']):
            return 'message-aggregator'
        else:
            return 'agent-coordinator'
    
    def _select_acp_for_task(self, task: str) -> str:
        """根据任务类型选择 ACP 代理"""
        task_lower = task.lower()
        
        # 编码相关任务
        if any(kw in task_lower for kw in ['代码', '编程', '开发', 'code', 'develop']):
            return 'codex'
        else:
            return 'pi'
    
    def _validate_agent_id(self, agent_id: str, runtime: SubagentRuntime) -> bool:
        """验证 agent_id 是否有效"""
        if runtime == SubagentRuntime.SUBAGENT:
            return agent_id in self.subagent_agents
        else:
            return agent_id in self.acp_agents
    
    def execute_subagent(self, subagent_id: str) -> Dict[str, Any]:
        """
        执行子代理
        
        Args:
            subagent_id: 子代理 ID
            
        Returns:
            执行结果
        """
        if subagent_id not in self.subagents:
            return {'error': 'Subagent not found'}
        
        config = self.subagents[subagent_id]
        config.status = 'running'
        
        logger.info(f"开始执行子代理：{config.name}")
        
        # TODO: 调用 OpenClaw sessions_spawn API
        # 这里模拟执行
        result = {
            'status': 'completed',
            'subagent_id': subagent_id,
            'result': f'模拟结果：{config.task}',
            'completed_at': datetime.now().isoformat()
        }
        
        config.status = 'completed'
        config.result = result
        
        # 记录历史
        self.history.append({
            'subagent_id': subagent_id,
            'task': config.task,
            'status': 'completed',
            'completed_at': result['completed_at']
        })
        
        return result
    
    def get_status(self, subagent_id: str) -> Dict[str, Any]:
        """获取子代理状态"""
        if subagent_id not in self.subagents:
            return {'error': 'Subagent not found'}
        
        config = self.subagents[subagent_id]
        
        return {
            'id': config.id,
            'name': config.name,
            'runtime': config.runtime.value,
            'agent_id': config.agent_id,
            'mode': config.mode.value,
            'status': config.status,
            'task': config.task,
            'created_at': config.created_at,
            'result': config.result
        }
    
    def list_subagents(self, active_only: bool = False) -> List[Dict[str, Any]]:
        """列出所有子代理"""
        subagents = []
        for sa_id, config in self.subagents.items():
            if active_only and config.status not in ['pending', 'running']:
                continue
            subagents.append(self.get_status(sa_id))
        return subagents
    
    def cleanup_completed(self, older_than_hours: int = 24) -> int:
        """清理已完成的子代理"""
        cleaned = 0
        now = datetime.now()
        
        for sa_id in list(self.subagents.keys()):
            config = self.subagents[sa_id]
            if config.status == 'completed':
                # 检查是否超过指定时间
                created = datetime.fromisoformat(config.created_at)
                age_hours = (now - created).total_seconds() / 3600
                if age_hours > older_than_hours:
                    del self.subagents[sa_id]
                    cleaned += 1
        
        logger.info(f"已清理 {cleaned} 个已完成的子代理")
        return cleaned
    
    def get_summary(self) -> str:
        """获取摘要"""
        total = len(self.subagents)
        active = len([s for s in self.subagents.values() if s.status == 'running'])
        completed = len([s for s in self.subagents.values() if s.status == 'completed'])
        
        lines = [
            f"Subagent Manager Summary",
            f"",
            f"**Total**: {total}",
            f"**Active**: {active}",
            f"**Completed**: {completed}",
            f""
        ]
        
        if self.subagents:
            lines.append("**Recent Subagents**:")
            for sa_id, config in list(self.subagents.items())[-5:]:
                lines.append(f"  - {config.name}: {config.status} ({config.runtime.value})")
        
        return '\n'.join(lines)


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
    print(f"   Created: {sa1.name} (agent={sa1.agent_id})")
    
    sa2 = manager.create_subagent(
        task="编写一个 Python 脚本",
        runtime="acp",
        agent_id="codex",
        thread=True,
        label="Coding Agent"
    )
    print(f"   Created: {sa2.name} (agent={sa2.agent_id}, thread={sa2.thread})")
    
    # 执行子代理
    print("\n2. Executing subagents...")
    result1 = manager.execute_subagent(sa1.id)
    print(f"   Result: {result1['status']}")
    
    result2 = manager.execute_subagent(sa2.id)
    print(f"   Result: {result2['status']}")
    
    # 显示状态
    print("\n3. Subagent status:")
    for sa in manager.list_subagents():
        print(f"   - {sa['name']}: {sa['status']}")
    
    # 摘要
    print("\n" + "="*60)
    print(manager.get_summary())


if __name__ == '__main__':
    main()
```

---

### 步骤 2: 集成到主系统

在 `main.py` 中添加子代理命令:

```python
# 在 main.py 的 GuijiWorld2 类中添加方法

def spawn_subagent(
    self,
    task: str,
    runtime: str = "subagent",
    agent_id: Optional[str] = None,
    mode: str = "session",
    **kwargs
):
    """生成子代理"""
    from agents.subagent_manager import SubagentManager
    
    manager = SubagentManager()
    config = manager.create_subagent(
        task=task,
        runtime=runtime,
        agent_id=agent_id,
        mode=mode,
        **kwargs
    )
    
    # 使用 OpenClaw sessions_spawn API
    # 这里需要调用实际的 OpenClaw API
    print(f"生成子代理：{config.name}")
    print(f"运行时：{config.runtime.value}")
    print(f"代理 ID: {config.agent_id}")
    print(f"任务：{config.task}")
    
    return manager.execute_subagent(config.id)


def list_subagents(self, active_only: bool = False):
    """列出子代理"""
    from agents.subagent_manager import SubagentManager
    
    manager = SubagentManager()
    return manager.list_subagents(active_only)
```

---

### 步骤 3: 添加 CLI 命令

在 `main.py` 的命令行接口中添加:

```python
# 在 if __name__ == '__main__': 部分添加

elif command == 'spawn':
    # 生成子代理
    task = ' '.join(sys.argv[2:])
    if not task:
        print("用法：python main.py spawn <任务描述>")
        sys.exit(1)
    
    result = system.spawn_subagent(task)
    print(f"结果：{result}")

elif command == 'subagents':
    # 列出子代理
    active = '--active' in sys.argv
    subagents = system.list_subagents(active_only=active)
    
    if not subagents:
        print("没有子代理")
    else:
        print(f"{'ID':<20} {'名称':<20} {'状态':<15} {'代理':<15}")
        print("-" * 70)
        for sa in subagents:
            print(f"{sa['id']:<20} {sa['name']:<20} {sa['status']:<15} {sa['agent_id']:<15}")
```

---

### 步骤 4: 实际调用 OpenClaw API

使用 OpenClaw 的 `sessions_spawn` 工具:

```python
"""
实际调用 OpenClaw sessions_spawn API 的示例
"""

def call_openclaw_spawn(
    task: str,
    runtime: str = "subagent",
    agent_id: Optional[str] = None,
    mode: str = "session",
    thread: bool = False,
    timeout_seconds: Optional[int] = None,
    label: Optional[str] = None
):
    """
    调用 OpenClaw sessions_spawn
    
    这是伪代码，实际需要通过 OpenClaw 的工具系统调用
    """
    
    # 构建参数
    params = {
        "task": task,
        "runtime": runtime,
        "mode": mode,
        "thinking": "off"  # 或 "on"
    }
    
    if agent_id:
        params["agentId"] = agent_id
    
    if thread:
        params["thread"] = True
    
    if timeout_seconds:
        params["timeoutSeconds"] = timeout_seconds
    
    if label:
        params["label"] = label
    
    # 调用 sessions_spawn 工具
    # 这需要在 OpenClaw 的上下文中执行
    result = sessions_spawn(**params)
    
    return result
```

---

## 📝 使用示例

### 示例 1: 创建研究子代理

```bash
python main.py spawn "研究 2026 年 AI 发展趋势"
```

### 示例 2: 创建编码子代理 (ACP)

```bash
python main.py spawn --runtime acp --agent-id codex --thread "实现一个 Web 爬虫"
```

### 示例 3: 列出所有子代理

```bash
python main.py subagents
```

### 示例 4: 只列出活跃的子代理

```bash
python main.py subagents --active
```

---

## 🔧 配置选项

在 `configs/config.json` 中添加:

```json
{
  "subagent": {
    "default_runtime": "subagent",
    "default_mode": "session",
    "timeout_seconds": 300,
    "max_concurrent": 5,
    "auto_cleanup_hours": 24,
    "preferred_agents": {
      "research": "research-assistant",
      "coding": "codex",
      "message": "message-aggregator"
    }
  }
}
```

---

## 🎯 最佳实践

### 1. 任务分解

将复杂任务分解为子任务，每个子任务交给专门的子代理:

```python
# 主代理接收复杂任务
complex_task = "研究 AI 趋势并生成报告"

# 分解为子任务
subtasks = [
    {"task": "搜索最新的 AI 研究论文", "agent": "research-assistant"},
    {"task": "分析研究结果", "agent": "analyst"},
    {"task": "生成 Markdown 报告", "agent": "report-generator"}
]

# 为每个子任务创建子代理
for subtask in subtasks:
    spawn_subagent(**subtask)
```

### 2. 结果聚合

子代理完成后，聚合结果:

```python
results = []
for subagent_id in subagent_ids:
    result = get_subagent_result(subagent_id)
    results.append(result)

# 整合结果
final_report = synthesize_results(results)
```

### 3. 错误处理

处理子代理失败:

```python
try:
    result = spawn_subagent(task)
    if result['status'] == 'failed':
        # 重试或降级处理
        retry_result = spawn_subagent(task, agent_id='backup-agent')
except Exception as e:
    logger.error(f"子代理执行失败：{e}")
```

### 4. 资源管理

定期清理已完成的子代理:

```python
# 每天清理超过 24 小时的已完成子代理
cleanup_completed(older_than_hours=24)
```

---

## 🚨 注意事项

### 1. AgentId 来源

- **Subagent 模式**: 使用 `agents_list` 获取可用 agentId
- **ACP 模式**: 使用 `acp.allowedAgents` 获取可用 agentId
- **不要混用**: 两种模式的 agentId 不通用

### 2. 会话隔离

- 每个子代理有独立的会话状态
- 主代理和子代理之间通过 `sessions_send` 通信
- 子代理之间不直接通信

### 3. Discord 线程

- ACP 模式在 Discord 上默认使用 `thread: true`
- 这会在 Discord 中创建持久线程
- 子代理的所有输出都在该线程中

### 4. 超时设置

- 设置合理的 `timeout_seconds` 避免无限等待
- 长时间任务使用 `mode: "session"` 而非 `mode: "run"`
- 监控子代理状态，及时处理超时

---

## 📊 监控和调试

### 查看子代理状态

```bash
python main.py subagents --json
```

### 查看子代理历史

```bash
python main.py subagents --history
```

### 调试模式

```bash
python main.py spawn --debug "任务描述"
```

---

## 🔮 未来扩展

1. **自动任务分解** - AI 自动将复杂任务分解为子任务
2. **动态负载均衡** - 根据子代理负载自动分配任务
3. **结果缓存** - 缓存子代理结果避免重复计算
4. **可视化仪表板** - Web UI 显示子代理状态和进度

---

## 📚 相关文档

- [OpenClaw Sessions](https://docs.openclaw.ai/concepts/session)
- [OpenClaw CLI Sessions](https://docs.openclaw.ai/cli/sessions)
- [Ultimate Agent README](../README.md)

---

*最后更新：2026-03-17*  
*作者：三二 🐱*
