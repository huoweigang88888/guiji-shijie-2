# 使用指南 - OpenClaw Ultimate Agent 整合版

**版本**: 1.0  
**更新时间**: 2026-03-17  
**状态**: 🚧 实施中

---

## 📋 目录

1. [快速开始](#快速开始)
2. [业务角色使用](#业务角色使用)
3. [工作流使用](#工作流使用)
4. [技能管理](#技能管理)
5. [常见问题](#常见问题)

---

## 快速开始

### 1. 系统检查

```bash
# 进入工作空间
cd ~/.openclaw/workspace/skills/ultimate-agent

# 查看系统状态
python main.py status
```

### 2. 第一个项目

#### 方式 1: 使用业务角色代理

```bash
# 产品经理分析需求
python -c "
from agents.business_roles.product_manager import ProductManagerAgent
agent = ProductManagerAgent()
result = agent.execute('开发一个待办事项应用')
print(f'PRD 已生成：{result[\"prd_path\"]}')
"

# UI 设计师设计界面
python -c "
from agents.business_roles.ui_designer import UIDesignerAgent
agent = UIDesignerAgent()
result = agent.execute('workspaces/product-manager/prd/PRD_todo_20260317.md')
print(f'设计已完成：{result[\"design_path\"]}')
"
```

#### 方式 2: 使用工作流引擎

```bash
# 执行软件开发工作流
python -c "
from agents.workflow_engine import WorkflowEngine
engine = WorkflowEngine()

# 创建工作流
workflow = engine.create_workflow('software_development', '开发一个待办事项应用')

# 执行工作流
result = engine.execute_workflow(workflow.id)
print(f'工作流状态：{result[\"status\"]}')
"
```

---

## 业务角色使用

### 产品经理 (Product Manager)

**用途**: 将用户需求转化为 PRD 文档

**使用示例**:
```python
from agents.business_roles.product_manager import ProductManagerAgent

# 初始化
agent = ProductManagerAgent()

# 执行需求分析
result = agent.execute('开发一个电商网站，支持用户注册、商品浏览、购物车功能')

# 查看结果
print(f"项目名称：{result['project_name']}")
print(f"PRD 路径：{result['prd_path']}")
print(f"分析结果：{result['analysis']}")
```

**输出位置**: `workspaces/product-manager/prd/`

---

### UI 设计师 (UI Designer)

**用途**: 基于 PRD 创建视觉设计文档

**使用示例**:
```python
from agents.business_roles.ui_designer import UIDesignerAgent

# 初始化
agent = UIDesignerAgent()

# 执行设计（需要提供 PRD 路径）
result = agent.execute('workspaces/product-manager/prd/PRD_xxx.md')

# 查看结果
print(f"配色方案：{result['color_scheme']}")
print(f"设计路径：{result['design_path']}")
```

**输出位置**: `workspaces/ui-designer/design/`

**配色方案**:
- blue - 商务/专业
- green - 清新/自然
- purple - 优雅/高端
- orange - 活泼/年轻

---

### 架构师 (Architect)

**用途**: 设计技术方案和系统架构

**使用示例**:
```python
from agents.business_roles.architect import ArchitectAgent

# 初始化
agent = ArchitectAgent()

# 执行架构设计
result = agent.execute('workspaces/product-manager/prd/PRD_xxx.md')

# 查看结果
print(f"技术方案路径：{result['design_path']}")
```

**输出位置**: `workspaces/architect/tech-design/`

---

### 开发工程师 (Senior Developer)

**用途**: 实现代码和测试

**使用示例**:
```python
from agents.business_roles.senior_dev import SeniorDevAgent

# 初始化
agent = SeniorDevAgent()

# 执行代码实现
result = agent.implement(
    tech_design_path='workspaces/architect/tech-design/TechDesign_xxx.md',
    ui_design_path='workspaces/ui-designer/design/UIDesign_xxx.md'
)

# 查看结果
print(f"代码路径：{result['code_path']}")
```

**输出位置**: `workspaces/senior-dev/src/`

---

## 工作流使用

### 串行工作流（阶段式）

**适用场景**: 软件开发全流程

```python
from agents.workflow_engine import WorkflowEngine

# 初始化引擎
engine = WorkflowEngine()

# 注册代理执行器
from agents.business_roles.product_manager import ProductManagerAgent
pm_agent = ProductManagerAgent()
engine.register_agent('product-manager', pm_agent.execute)

# 创建工作流
workflow = engine.create_workflow(
    'software_development',
    '开发一个待办事项应用'
)

# 定义确认回调
def on_confirm(stage_info):
    print(f"阶段完成：{stage_info['stage']}")
    print(f"输出：{stage_info['output_path']}")
    confirmed = input("是否继续？(y/n): ")
    return confirmed.lower() == 'y'

# 执行工作流
result = engine.execute_workflow(workflow.id, on_confirm=on_confirm)

# 查看结果
print(f"工作流状态：{result['status']}")
print(f"总阶段数：{result['total_stages']}")
```

### 并行工作流

**适用场景**: 研究报告、数据分析

```python
from agents.workflow_engine import WorkflowEngine

engine = WorkflowEngine()

# 注册代理
engine.register_agent('researcher', researcher_function)
engine.register_agent('analyst', analyst_function)
engine.register_agent('report_generator', reporter_function)

# 创建并行工作流
workflow = engine.create_workflow(
    'research_report',
    '研究 2026 年 AI 发展趋势'
)

# 执行（并行）
result = engine.execute_workflow(workflow.id)
```

---

## 技能管理

### 查看已批准技能

```bash
python -c "
from agents.skill_security_checker import SkillSecurityChecker
checker = SkillSecurityChecker()
print(checker.get_summary())
"
```

### 扫描技能安全性

```python
from agents.skill_security_checker import SkillSecurityChecker
from pathlib import Path

checker = SkillSecurityChecker()

# 扫描技能目录
result = checker.scan_skill(Path('path/to/skill'))

print(f"风险等级：{result['risk_level']}")
print(f"风险分数：{result['risk_score']}")
print(f"建议：{result['recommendation']}")

# 显示发现
for finding in result['findings']:
    print(f"  - {finding['factor']} (第{finding['line']}行)")
```

### 批准/阻止技能

```python
# 批准技能
checker.approve_skill('proactive-agent', '3.1.0')

# 阻止技能
checker.block_skill('risky-skill', reason='存在高风险命令')
```

---

## WAL 协议使用

### 写入状态

```python
from agents.wal_protocol import WALProtocol
from pathlib import Path

wal = WALProtocol(Path('SESSION-STATE.md'))

# 写入关键信息
wal.write('decision', {'choice': 'option_a'}, category='decisions')
wal.write('progress', {'stage': 2, 'total': 4}, category='progress')
```

### 读取状态

```python
# 读取所有状态
state = wal.read()

# 按分类读取
decisions = wal.read(category='decisions')
```

### 裁剪旧条目

```python
# 保留最近 24 小时
removed = wal.prune(keep_hours=24)
print(f"删除了 {removed} 个条目")
```

---

## 心跳配置

### 查看心跳状态

```bash
python -c "
from agents.heartbeat import HeartbeatSystem
heartbeat = HeartbeatSystem()
print(f'上次检查：{heartbeat.last_check}')
print(f'已执行：{heartbeat.checks_performed} 次')
print(f'启用：{heartbeat.enabled}')
"
```

### 修改心跳频率

编辑 `configs/heartbeat.json`:

```json
{
  "enabled": true,
  "global": {
    "every": "30m",
    "activeHours": "08:00-24:00"
  },
  "roles": {
    "main": {"every": "15m"},
    "product-manager": {"every": "30m"}
  }
}
```

---

## 常见问题

### Q1: 如何创建自定义工作流？

**A**: 编辑 `configs/workflows.json`:

```json
{
  "my_workflow": {
    "name": "我的工作流",
    "mode": "serial",
    "stages": [
      {
        "name": "阶段 1",
        "agent": "product-manager",
        "require_confirm": true
      }
    ]
  }
}
```

### Q2: 如何添加新的业务角色？

**A**: 
1. 在 `agents/business_roles/` 创建 Python 文件
2. 实现 `execute()` 方法
3. 创建工作空间目录
4. 创建 SOUL.md

### Q3: WAL 协议文件在哪里？

**A**: 每个工作空间都有独立的 `SESSION-STATE.md`:
- `workspaces/main/SESSION-STATE.md`
- `workspaces/product-manager/SESSION-STATE.md`
- 等等...

### Q4: 如何禁用某个技能？

**A**: 编辑 `configs/skills.json`:

```json
{
  "built_in": {
    "enabled": ["researcher", "analyst"],
    "disabled": ["notification_agent"]
  }
}
```

### Q5: 工作流执行失败怎么办？

**A**: 
1. 查看错误信息
2. 检查代理是否注册
3. 验证配置文件
4. 查看日志输出

---

## 附录

### A. 配置文件位置

| 文件 | 路径 | 用途 |
|------|------|------|
| heartbeat.json | configs/ | 心跳配置 |
| workflows.json | configs/ | 工作流配置 |
| skills.json | configs/ | 技能配置 |

### B. 输出目录

| 角色 | 输出目录 |
|------|----------|
| 产品经理 | workspaces/product-manager/prd/ |
| UI 设计师 | workspaces/ui-designer/design/ |
| 架构师 | workspaces/architect/tech-design/ |
| 开发工程师 | workspaces/senior-dev/src/ |

### C. 相关文档

- [整合指南](INTEGRATION_GUIDE.md)
- [阶段报告](PHASE*_COMPLETE.md)
- [角色 SOUL.md](../workspaces/)

---

*最后更新：2026-03-17*
