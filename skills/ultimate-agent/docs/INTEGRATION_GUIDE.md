# OpenClaw Ultimate Agent 整合指南

**版本**: 1.0  
**创建时间**: 2026-03-17  
**状态**: 🚧 实施中

---

## 📋 目录

1. [整合概述](#整合概述)
2. [快速开始](#快速开始)
3. [架构说明](#架构说明)
4. [角色配置](#角色配置)
5. [工作流使用](#工作流使用)
6. [心跳机制](#心跳机制)
7. [技能管理](#技能管理)
8. [最佳实践](#最佳实践)

---

## 整合概述

本整合方案结合了**头条文章 OpenClaw 多智能体架构**和**Ultimate Agent 子代理系统**的优势，形成最强 AI 协作系统。

### 核心特性

| 特性 | 来源 | 状态 |
|------|------|------|
| 业务角色（产品/设计/架构/开发） | 头条文章 | ✅ 已实现 |
| 子代理会话隔离 | Ultimate Agent | ✅ 已实现 |
| 阶段式工作流 | 头条文章 | ✅ 已实现 |
| 并行执行 | Ultimate Agent | ✅ 已实现 |
| Heartbeat 心跳 | 头条文章 | ✅ 已配置 |
| WAL 协议 | 头条文章 | ⏳ 实施中 |
| ClawHub 技能 | 头条文章 | ✅ 已配置 |

---

## 快速开始

### 1. 系统要求

- OpenClaw v2.6+
- Python 3.11+
- Node.js 18+

### 2. 安装步骤

```bash
# 进入工作空间
cd ~/.openclaw/workspace/skills/ultimate-agent

# 查看系统状态
python main.py status

# 查看可用角色
python main.py roles
```

### 3. 第一个项目

```bash
# 启动软件开发工作流
python main.py workflow software_development "开发一个待办事项应用"
```

---

## 架构说明

### 整体架构

```
┌─────────────────────────────────────────┐
│         GuijiWorld2 主系统               │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌───────────────┐       ┌───────────────┐
│ 业务角色代理   │       │ 功能代理       │
│ (5 个)          │       │ (13+)         │
└───────────────┘       └───────────────┘
```

### 文件结构

```
ultimate-agent/
├── workspaces/              # 虚拟工作空间
│   ├── main/               # 主协调员
│   ├── product-manager/    # 产品经理
│   ├── ui-designer/        # UI 设计师
│   ├── architect/          # 架构师
│   └── senior-dev/         # 开发工程师
│
├── agents/                  # 代理模块
│   ├── business_roles/     # 业务角色
│   └── ...                 # 功能代理
│
├── configs/                 # 配置文件
│   ├── heartbeat.json      # 心跳配置
│   ├── workflows.json      # 工作流配置
│   └── skills.json         # 技能配置
│
└── docs/                    # 文档
```

---

## 角色配置

### 主协调员

**职责**: 统筹全流程，调度各角色  
**心跳频率**: 15 分钟  
**工作空间**: `workspaces/main/`

### 产品经理

**职责**: 需求分析，产出 PRD  
**心跳频率**: 30 分钟  
**工作空间**: `workspaces/product-manager/`

### UI 设计师

**职责**: 视觉设计，产出设计稿  
**心跳频率**: 60 分钟  
**工作空间**: `workspaces/ui-designer/`

### 架构师

**职责**: 技术选型，产出技术方案  
**心跳频率**: 30 分钟  
**工作空间**: `workspaces/architect/`

### 开发工程师

**职责**: 代码实现，产出源代码  
**心跳频率**: 30 分钟  
**工作空间**: `workspaces/senior-dev/`

---

## 工作流使用

### 串行模式（软件开发）

```json
{
  "name": "software_development",
  "mode": "serial",
  "stages": [
    "需求分析 → PRD",
    "视觉设计 → 设计稿",
    "架构设计 → 技术方案",
    "编码实现 → 源代码"
  ]
}
```

**使用**:
```bash
python main.py workflow software_development "项目描述"
```

### 并行模式（研究报告）

```json
{
  "name": "research_report",
  "mode": "parallel",
  "tasks": [
    "信息收集",
    "数据分析",
    "报告生成"
  ]
}
```

**使用**:
```bash
python main.py workflow research_report "研究主题"
```

---

## 心跳机制

### 配置位置

`configs/heartbeat.json`

### 全局配置

```json
{
  "enabled": true,
  "global": {
    "every": "30m",
    "activeHours": "08:00-24:00",
    "timeout": "10s"
  }
}
```

### 角色配置

每个角色有独立的心跳频率和任务清单。

### 查看心跳状态

```bash
python main.py heartbeat status
```

---

## 技能管理

### 内置技能

默认启用 13+ 个内置功能代理。

### ClawHub 技能

**安装**:
```bash
clawhub install proactive-agent
```

**审查**:
所有外部技能需经过安全审查。

### 技能配置

`configs/skills.json` 管理启用/禁用技能。

---

## 最佳实践

### 1. 阶段确认

在串行工作流中，每个阶段完成后用户确认再进入下一阶段。

### 2. WAL 协议

关键决策先写入 `SESSION-STATE.md`，防止上下文丢失。

### 3. 心跳监控

定期检查各角色状态，及时发现阻塞。

### 4. 技能审查

安装 ClawHub 技能前阅读 SKILL.md，检查风险命令。

---

## 附录

### A. 配置文件说明

- `heartbeat.json` - 心跳配置
- `workflows.json` - 工作流定义
- `skills.json` - 技能管理

### B. 常见问题

**Q: 如何切换工作流模式？**  
A: 在 `workflows.json` 中修改 `mode` 字段。

**Q: 心跳不执行怎么办？**  
A: 检查 `heartbeat.json` 中 `enabled` 是否为 `true`。

### C. 相关文档

- [角色文档](docs/roles/)
- [工作流文档](docs/workflows/)
- [API 文档](docs/api/)

---

*最后更新：2026-03-17*
