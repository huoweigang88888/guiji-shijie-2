# MEMORY.md - Long-Term Memory

**Last Updated**: 2026-03-06

---

## 📋 Important Projects

### 1. AI 分身集群 (Multi-Agent System)
- **描述**: 多个 specialized agents 协作完成复杂任务
- **状态**: ✅ 框架已搭建
- **代理**: 
  - agent-coordinator (✅ active)
  - message-aggregator (⏳ pending config)
  - research-assistant (✅ active)
- **位置**: `skills/ultimate-agent/agents/`

### 2. 全平台消息聚合 (Message Aggregator)
- **描述**: 一个入口管所有聊天（微信/WhatsApp/Telegram/Slack）
- **状态**: ⏳ 需要用户配置消息平台
- **待办**: 连接 WhatsApp/Telegram/Slack 等

### 3. 自动研究助手 (Research Assistant)
- **描述**: 自动搜索、整理、总结某个主题的最新进展
- **状态**: ✅ 框架已搭建
- **待办**: 集成真实 web_search API

---

## 🤖 Installed Skills

| Skill | Version | Status | Description |
|-------|---------|--------|-------------|
| `ultimate-agent` | 1.0.0 | ✅ Active | 整合主动工作、自我改进、代理创建 |
| `fluid-memory` | - | ✅ Active | 流体认知架构记忆系统 |
| `elite-longterm-memory` | 1.2.0 | ✅ Active | 精英长期记忆系统（WAL + 向量搜索 + git-notes） |
| `autonomous-tasks` | - | ✅ Active | 自主任务执行 |
| `parallel-ai-search` | - | ✅ Active | 并行 AI 搜索 |

---

## 🧠 Memory System

### Architecture
```
SESSION-STATE.md → MEMORY.md → memory/daily-logs
     (HOT)          (WARM)        (RAW)
```

### Files
- `SESSION-STATE.md` - 活动工作记忆（WAL 协议）
- `MEMORY.md` - 长期记忆（本文件）
- `memory/YYYY-MM-DD.md` - 每日日志

### Tools
- `skills/elite-longterm-memory/memory_manager.py` - 记忆管理工具

---

## 📝 Todo

- [ ] 配置消息平台（WhatsApp/Telegram）
- [ ] 集成真实 web_search API 到 research-assistant
- [ ] 设置定期心跳检查
- [ ] 配置 LanceDB 向量搜索（可选）
- [ ] 配置 Git-Notes 知识图谱（可选）

---

## 💡 Notes

- **Workspace**: `C:\Users\97RPZ8T\.openclaw\workspace`
- **Channel**: webchat (primary)
- **Model**: bailian/qwen3.5-plus
- **Timezone**: Asia/Shanghai

---

*Elite Longterm Memory System*
