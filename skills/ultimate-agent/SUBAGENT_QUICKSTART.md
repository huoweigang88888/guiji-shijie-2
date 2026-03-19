# 子代理模式快速开始

**创建时间**: 2026-03-17  
**版本**: 1.0.0

---

## 🚀 5 分钟上手子代理模式

### 1️⃣ 什么是子代理模式？

子代理模式允许你动态创建隔离的 AI 会话来完成特定任务：

- **Subagent 模式**: 使用 OpenClaw 内部的专用代理（如 research-assistant、message-aggregator）
- **ACP 模式**: 调用外部 AI 编码代理（如 Codex、Claude Code）

### 2️⃣ 快速测试

```bash
# 进入项目目录
cd ~/.openclaw/workspace/skills/ultimate-agent

# 测试子代理管理器
python agents/subagent_manager.py
```

你会看到类似输出：
```
============================================================
Subagent Manager Test
============================================================

1. Creating subagents...
   ✓ Created: Research Agent (agent=research-assistant, runtime=subagent)
   ✓ Created: Coding Agent (agent=codex, runtime=acp, thread=True)
   ✓ Created: Analysis Agent (agent=analyst, mode=run)

2. Executing subagents...
   ✓ Result: completed
   ✓ Result: completed

3. Subagent status:
   - Research Agent: completed (subagent/research-assistant)
   - Coding Agent: completed (acp/codex)
   - Analysis Agent: completed (subagent/analyst)

============================================================
Subagent Manager Summary

**Total**: 3
**Active**: 0
**Pending**: 0
**Completed**: 3
**Failed**: 0
```

### 3️⃣ 使用命令行

```bash
# 查看系统状态（包含子代理统计）
python main.py status

# 生成一个研究子代理
python main.py spawn "研究 2026 年 AI 发展趋势"

# 生成一个编码子代理（使用 ACP 模式）
python main.py spawn "编写一个 Python 爬虫" --runtime acp --agent-id codex --thread

# 列出所有子代理
python main.py subagents

# 只列出活跃的子代理
python main.py subagents --active

# 以 JSON 格式输出
python main.py subagents --json

# 执行子代理
python main.py execute-subagent sa_20260317100000_abc12345

# 清理已完成的子代理（超过 24 小时）
python main.py cleanup-subagents 24
```

### 4️⃣ 使用 Python API

```python
from main import GuijiWorld2

# 初始化系统
system = GuijiWorld2()

# 生成子代理
result = system.spawn_subagent(
    task="研究机器学习最新进展",
    runtime="subagent",      # 或 "acp"
    agent_id="research-assistant",  # 可选，自动选择
    mode="session",          # 或 "run"
    label="ML Research"
)

print(f"子代理 ID: {result['subagent_id']}")
print(f"代理：{result['agent_id']}")
print(f"任务：{result['task']}")

# 执行子代理
exec_result = system.execute_subagent(result['subagent_id'])
print(f"执行结果：{exec_result}")

# 列出所有子代理
subagents = system.list_subagents()
print(f"共有 {subagents['count']} 个子代理")

# 清理已完成的子代理
cleaned = system.cleanup_subagents(older_than_hours=24)
print(f"清理了 {cleaned['cleaned']} 个子代理")
```

### 5️⃣ 配置选项

编辑 `configs/config.json`:

```json
{
  "subagent": {
    "enabled": true,
    "default_runtime": "subagent",
    "default_mode": "session",
    "timeout_seconds": 300,
    "max_concurrent": 5,
    "auto_cleanup_hours": 24,
    "available_subagents": [
      "research-assistant",
      "message-aggregator",
      "agent-coordinator"
    ],
    "available_acp_agents": [
      "codex",
      "claude-code",
      "pi"
    ]
  }
}
```

---

## 📋 常用场景

### 场景 1: 自动研究任务

```bash
# 创建研究子代理
python main.py spawn "调查最新的量子计算突破" --runtime subagent --agent-id research-assistant

# 子代理会自动：
# 1. 搜索相关信息
# 2. 整理研究结果
# 3. 生成摘要报告
```

### 场景 2: 编码任务（ACP 模式）

```bash
# 在 Discord 线程中创建编码子代理
python main.py spawn "实现一个 REST API" --runtime acp --agent-id codex --thread --label "API Development"

# 这会：
# 1. 在 Discord 创建持久线程
# 2. Codex 在 thread 中工作
# 3. 所有输出都在该线程中可见
```

### 场景 3: 多代理协作

```python
# 创建多个子代理协作完成复杂任务
tasks = [
    {"task": "研究 AI 伦理问题", "agent": "research-assistant"},
    {"task": "分析研究结果", "agent": "analyst"},
    {"task": "生成报告", "agent": "report_generator"}
]

subagent_ids = []
for task_config in tasks:
    result = system.spawn_subagent(**task_config)
    subagent_ids.append(result['subagent_id'])

# 等待所有子代理完成
for sa_id in subagent_ids:
    result = system.execute_subagent(sa_id)
    print(f"{sa_id}: {result['status']}")
```

---

## 🎯 最佳实践

### ✅ 推荐做法

1. **为不同任务类型使用专用子代理**
   - 研究任务 → research-assistant
   - 编码任务 → codex (ACP)
   - 消息任务 → message-aggregator

2. **设置合理的超时时间**
   ```bash
   # 长时间任务设置 600 秒超时
   python main.py spawn "复杂分析" --timeout 600
   ```

3. **定期清理已完成的子代理**
   ```bash
   # 每天清理超过 24 小时的子代理
   python main.py cleanup-subagents 24
   ```

4. **使用标签标识重要子代理**
   ```bash
   python main.py spawn "关键任务" --label "Critical-Task-001"
   ```

### ❌ 避免的做法

1. **不要创建过多并发子代理**
   - 默认限制 5 个并发
   - 过多会消耗大量资源

2. **不要忘记清理**
   - 已完成的子代理会占用存储空间
   - 设置自动清理或定期手动清理

3. **不要在子代理中处理敏感信息**
   - 子代理会话可能被持久化
   - 避免传递密码、密钥等敏感数据

---

## 🔧 故障排查

### 问题 1: "无效的 agent_id"

**错误**: `无效的 agent_id: xxx。可用值：[...]`

**解决**: 
- 检查 `configs/config.json` 中的 `available_subagents` 和 `available_acp_agents`
- 确保使用的 agent_id 在列表中
- 或者不指定 `--agent-id` 让系统自动选择

### 问题 2: 子代理一直处于 "pending" 状态

**可能原因**:
- 达到最大并发数（默认 5）
- 系统资源不足

**解决**:
```bash
# 查看活跃子代理
python main.py subagents --active

# 清理一些已完成的子代理
python main.py cleanup-subagents 0

# 或者增加超时时间
python main.py spawn "任务" --timeout 600
```

### 问题 3: ACP 模式不工作

**可能原因**:
- 未配置 ACP 代理
- agentId 不正确

**解决**:
- 确认 `acp.allowedAgents` 配置
- 检查 OpenClaw 配置文件中 ACP 设置
- 使用 `--runtime subagent` 作为备选

---

## 📊 监控和统计

### 查看系统状态

```bash
python main.py status
```

输出包含子代理统计：
```json
{
  "components": {
    "subagent": {
      "total": 10,
      "by_status": {
        "completed": 7,
        "running": 2,
        "pending": 1
      },
      "by_runtime": {
        "subagent": 6,
        "acp": 4
      },
      "history_count": 25
    }
  }
}
```

### 查看子代理历史

子代理状态保存在 `task-queue/subagents-state.json`

```bash
# 查看原始状态文件
cat task-queue/subagents-state.json | jq
```

---

## 📚 进阶阅读

- [子代理模式详细指南](SUBAGENT_MODE.md)
- [子代理管理器源码](agents/subagent_manager.py)
- [OpenClaw Sessions 文档](https://docs.openclaw.ai/concepts/session)

---

## 🎉 下一步

现在你已经掌握了子代理模式的基础！尝试：

1. 创建一个研究子代理调查你感兴趣的主题
2. 创建一个编码子代理帮你写代码
3. 配置多个子代理协作完成复杂任务
4. 设置定时清理保持系统整洁

**Happy Agenting! 🤖**

---

*最后更新：2026-03-17*  
*作者：三二 🐱*
