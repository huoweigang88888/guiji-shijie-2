# 🚀 硅基世界 2 - 完整使用指南

> 一站式 AI 代理系统使用文档

---

## 📖 目录

1. [快速开始](#快速开始)
2. [核心功能](#核心功能)
3. [代理系统](#代理系统)
4. [高级功能](#高级功能)
5. [API 参考](#api 参考)
6. [常见问题](#常见问题)

---

## 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/huoweigang88888/guiji-shijie-2.git
cd guiji-shijie-2
```

### 运行交互模式

```bash
python skills/ultimate-agent/main.py interactive
```

### 查看系统状态

```bash
python skills/ultimate-agent/main.py status
```

---

## 核心功能

### 1. 代理协调器 (Agent Coordinator)

自动分解复杂任务并分配给专用代理。

```python
from coordinator import AgentCoordinator

coordinator = AgentCoordinator()
result = coordinator.execute_task("研究 AI 技术并生成报告")
```

### 2. 研究助手 (Research Assistant)

自动搜索、分析、生成研究报告。

```python
from researcher import ResearchAssistant

assistant = ResearchAssistant()
report = assistant.research("机器学习最新进展", count=10)
```

### 3. 消息聚合器 (Message Aggregator)

统一管理多个消息平台。

```python
from message_aggregator import MessageAggregator, MessagePlatform

aggregator = MessageAggregator()
aggregator.send_message("你好", MessagePlatform.WHATSAPP, "张三")
```

### 4. 心跳检查 (Heartbeat System)

定期系统健康检查。

```python
from heartbeat import HeartbeatSystem

system = HeartbeatSystem()
report = system.run_check()
print(report.summary)
```

### 5. 自动任务执行 (Auto Executor)

基于目标自动执行任务。

```python
from auto_executor import AutoExecutor

executor = AutoExecutor()
goal = executor.add_goal("学习 Python", "掌握 Python 编程")
executor.generate_tasks(goal.id, [
    {'title': '学习基础语法', 'priority': 'high'}
])
executor.execute_pending_tasks()
```

### 6. 自我改进 (Self Improver)

从错误中学习和改进。

```python
from self_improver import SelfImprover

improver = SelfImprover()
improver.record_error('FileNotFoundError', '文件不存在')
improvements = improver.get_high_priority_improvements()
```

---

## 代理系统

### 增强型研究代理

```python
from enhanced_researcher import EnhancedResearcher

researcher = EnhancedResearcher()

# 网络搜索
results = researcher.web_search("AI trends 2026", count=5)

# 生成报告
report = researcher.research("深度学习应用", generate_report=True)

# 主题比较
comparison = researcher.compare_topics(
    ['Machine Learning', 'Deep Learning']
)
```

### 增强型执行代理

```python
from enhanced_executor import EnhancedExecutor, TaskType

executor = EnhancedExecutor(safe_mode=True)

# 文件操作
executor.execute(TaskType.FILE_WRITE, {
    'path': 'test.txt',
    'content': 'Hello World'
})

# 执行命令
result = executor.execute(TaskType.COMMAND_RUN, {
    'command': 'python --version'
})

# 批量执行
tasks = [
    {'task_type': 'file_write', 'params': {...}},
    {'task_type': 'command_run', 'params': {...}}
]
results = executor.execute_batch(tasks)
```

### 数据分析代理

```python
from analyst_agent import AnalystAgent

analyst = AnalystAgent()

# 加载数据
data = [{'timestamp': '2026-03-01', 'value': 100}, ...]
analyst.load_dataset('sales', data)

# 统计分析
stats = analyst.calculate_statistics('sales')

# 趋势检测
trend = analyst.detect_trend('sales')

# 生成报告
report = analyst.generate_report('sales')
```

---

## 高级功能

### 多代理协作

```python
from agent_communication import AgentCommunication, Performative
from agent_orchestration import AgentOrchestration

# 创建通信系统
comm = AgentCommunication()

# 注册代理
comm.register_agent("researcher", "researcher", [...])

# 发送消息
comm.send_message(
    sender="coordinator",
    receivers=["researcher"],
    performative=Performative.REQUEST,
    content={"task": "Research AI"}
)

# 创建工作流
orchestration = AgentOrchestration(comm)
workflow = orchestration.create_workflow("Research Project", "AI Research")

# 分解任务
orchestration.decompose_task(workflow, "Research AI", [
    {"title": "Search", "assigned_to": "researcher"},
    {"title": "Analyze", "assigned_to": "analyst"},
    {"title": "Report", "assigned_to": "executor"}
])

# 执行工作流
result = orchestration.execute_workflow(workflow.id)
```

### 向量搜索

```python
from vector_search import VectorSearch

search = VectorSearch()

# 添加文档
search.add_document("memories", "Python 是编程语言", {"type": "knowledge"})

# 语义搜索
results = search.search("memories", "编程语言", limit=5)
```

### 知识图谱

```python
from knowledge_graph import KnowledgeGraph, RelationType

graph = KnowledgeGraph()

# 添加节点
node1 = graph.add_node("Python", "编程语言", "language")
node2 = graph.add_node("AI", "人工智能", "technology")

# 添加关系
graph.add_relation(node1, node2, RelationType.USED_FOR, "Python 用于 AI")

# 搜索
results = graph.search_nodes("Python")

# 推荐
recommendations = graph.get_recommendations(node1)
```

### 定时任务

```python
from scheduler import Scheduler, TaskFrequency

scheduler = Scheduler()

# 注册处理器
scheduler.register_handler('heartbeat', my_heartbeat_func)

# 创建任务
scheduler.schedule_task(
    name="Hourly Check",
    handler="heartbeat",
    frequency=TaskFrequency.HOURLY
)

# 查看状态
print(scheduler.get_summary())
```

### 系统监控

```python
from system_monitor import SystemMonitor

monitor = SystemMonitor()

# 获取指标
metrics = monitor.get_current_metrics()
print(f"CPU: {metrics.cpu_percent}%")
print(f"Memory: {metrics.memory_percent}%")

# 查看摘要
print(monitor.get_summary())
```

---

## Phase 5: 高级功能 (v3.1.0+)

### 通知代理 (Notification Agent)

支持多渠道通知推送，包括控制台、系统通知、Webhook 和邮件。

```python
from notification_agent import NotificationAgent, NotificationChannel, NotificationPriority

notifier = NotificationAgent(data_dir=Path('./notifications'))

# 发送通知
notifier.send(
    title="系统警告",
    message="CPU 使用率超过 80%",
    channel=NotificationChannel.CONSOLE,
    priority=NotificationPriority.HIGH
)

# 配置邮件通知
notifier.configure(
    smtp_server="smtp.example.com",
    smtp_port=587,
    smtp_user="user@example.com",
    smtp_password="password",
    email_from="alerts@example.com",
    email_to=["admin@example.com"]
)

# 发送到所有启用的渠道
notifier.send(
    title="重要通知",
    message="系统维护即将开始",
    channel=NotificationChannel.ALL,
    priority=NotificationPriority.URGENT
)

# 查看统计
stats = notifier.get_stats()
print(stats)
```

**命令行用法**:

```bash
# 发送通知
python main.py notify "标题" "消息内容" console normal
python main.py notify "警告" "CPU 过高" console high

# 查看通知统计
python main.py notify-stats

# 渠道选项：console, system, webhook, email, all
# 优先级选项：low, normal, high, urgent
```

### 报告生成器 (Report Generator)

支持多种格式的报告导出：Markdown、HTML、PDF、JSON、纯文本。

```python
from report_generator import ReportGenerator, ReportFormat, Report, ReportSection

generator = ReportGenerator(output_dir=Path('./reports'))

# 创建自定义报告
report = Report(
    title="项目进度报告",
    sections=[
        ReportSection(title="概述", content="项目进展顺利。", level=2),
        ReportSection(title="完成情况", content="已完成 80% 的功能。", level=2),
        ReportSection(title="下一步计划", content="继续开发剩余功能。", level=3)
    ]
)

# 生成 Markdown 报告
md_path = generator.generate(report, ReportFormat.MARKDOWN)

# 生成 HTML 报告
html_path = generator.generate(report, ReportFormat.HTML)

# 生成 PDF 报告（需要 pdfkit）
pdf_path = generator.generate(report, ReportFormat.PDF)

# 生成研究报告
research_report = generator.create_research_report(
    topic="AI 技术趋势",
    summary="2026 年 AI 技术发展迅速...",
    findings=[
        {"title": "大模型", "snippet": "...", "url": "..."}
    ]
)
```

**命令行用法**:

```bash
# 生成简单报告
python main.py report "报告标题" markdown
python main.py report "报告标题" html my-report

# 生成研究报告
python main.py research-report "AI 技术趋势" markdown

# 列出所有报告
python main.py reports

# 格式选项：markdown, html, pdf, json, text
```

### 工作流持久化

```python
from workflow_persistence import WorkflowPersistence

persistence = WorkflowPersistence()

# 保存工作流
persistence.save_workflow(workflow_data)

# 加载工作流
workflow = persistence.load_workflow('wf_001')

# 备份
backup_file = persistence.backup_all()

# 恢复
persistence.restore_from_backup(backup_file)
```

---

## API 参考

### 主系统类

| 类 | 功能 | 方法 |
|---|---|---|
| `GuijiWorld2` | 主系统 | `run_task()`, `research()`, `get_status()` |
| `AgentCoordinator` | 代理协调 | `execute_task()`, `analyze_task()` |
| `ResearchAssistant` | 研究助手 | `research()`, `search()` |
| `MessageAggregator` | 消息聚合 | `send_message()`, `receive_message()` |
| `HeartbeatSystem` | 心跳检查 | `run_check()`, `get_summary()` |
| `AutoExecutor` | 自动执行 | `add_goal()`, `execute_tasks()` |
| `SelfImprover` | 自我改进 | `record_error()`, `get_improvements()` |
| `VectorSearch` | 向量搜索 | `search()`, `add_document()` |
| `KnowledgeGraph` | 知识图谱 | `add_node()`, `search_nodes()` |
| `EnhancedResearcher` | 增强研究 | `web_search()`, `compare_topics()` |
| `EnhancedExecutor` | 增强执行 | `execute()`, `execute_batch()` |
| `AnalystAgent` | 数据分析 | `calculate_statistics()`, `generate_report()` |
| `AgentCommunication` | 代理通信 | `send_message()`, `broadcast()` |
| `AgentOrchestration` | 协作编排 | `create_workflow()`, `execute_workflow()` |
| `Scheduler` | 定时任务 | `schedule_task()`, `start()` |
| `SystemMonitor` | 系统监控 | `get_current_metrics()`, `start_monitoring()` |
| `WorkflowPersistence` | 持久化 | `save_workflow()`, `backup_all()` |
| `NotificationAgent` | 通知代理 | `send()`, `configure()`, `get_stats()` |
| `ReportGenerator` | 报告生成 | `generate()`, `create_research_report()`, `list_reports()` |

---

## 常见问题

### Q: 如何配置消息平台？

A: 编辑 `agents/message-aggregator.json`，添加平台认证信息。

### Q: 如何自定义代理？

A: 继承基类并实现 `execute()` 方法，然后注册到编排系统。

### Q: 工作流如何持久化？

A: 系统自动保存工作流到 SQLite 数据库，重启后自动恢复。

### Q: 如何添加定时任务？

A: 使用 `Scheduler.schedule_task()` 创建任务，支持 cron 表达式。

### Q: 系统监控需要安装什么？

A: 可选安装 `psutil` 获得完整监控，或使用简化版（无需额外依赖）。

---

## 项目结构

```
guiji-shijie-2/
├── skills/ultimate-agent/
│   ├── agents/              # 代理模块
│   │   ├── coordinator.py
│   │   ├── researcher.py
│   │   ├── message_aggregator.py
│   │   ├── heartbeat.py
│   │   ├── auto_executor.py
│   │   ├── self_improver.py
│   │   ├── vector_search.py
│   │   ├── knowledge_graph.py
│   │   ├── enhanced_researcher.py
│   │   ├── enhanced_executor.py
│   │   ├── analyst_agent.py
│   │   ├── agent_communication.py
│   │   ├── agent_orchestration.py
│   │   ├── scheduler.py
│   │   ├── system_monitor.py
│   │   └── workflow_persistence.py
│   ├── main.py              # 主入口
│   └── test_all.py          # 综合测试
├── memory/                  # 记忆文件
├── PROJECT_PLAN.md          # 开发计划
└── README.md                # 项目说明
```

---

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

---

## 许可证

MIT License

---

*最后更新：2026-03-09*  
*版本：3.0.0*
