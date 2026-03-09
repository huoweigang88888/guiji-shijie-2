# 🌐 硅基世界 2 - 大爱无疆

> 打造一个自主进化、多代理协作的 AI 生态系统

[![GitHub](https://img.shields.io/github/license/huoweigang88888/guiji-shijie-2)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.14+-blue)](https://python.org)
[![Version](https://img.shields.io/badge/Version-0.1.0-green)](https://github.com/huoweigang88888/guiji-shijie-2)

---

## 📖 项目简介

**硅基世界 2** 是一个基于 OpenClaw 的多代理 AI 系统，整合了：

- 🤖 **多代理协调** - 任务分解、代理调度、结果整合
- 🔍 **自动研究** - 网络搜索、信息分析、报告生成
- 💬 **消息聚合** - 统一管理平台消息（WhatsApp/Telegram/Slack 等）
- 🧠 **智能记忆** - WAL 协议、长期记忆、知识图谱
- 🔄 **自我进化** - 从错误中学习、持续改进

---

## 🚀 快速开始

### 环境要求

- Python 3.14+
- OpenClaw 运行时
- Git

### 安装

```bash
# 克隆项目
git clone https://github.com/huoweigang88888/guiji-shijie-2.git
cd guiji-shijie-2

# 安装依赖（如有）
pip install -r requirements.txt
```

### 运行

```bash
# 交互模式
python skills/ultimate-agent/main.py interactive

# 执行任务
python skills/ultimate-agent/main.py task "研究人工智能最新进展"

# 研究报告
python skills/ultimate-agent/main.py research "机器学习应用"

# 查看状态
python skills/ultimate-agent/main.py status
```

---

## 🏗️ 系统架构

```
硅基世界 2
├── Agent Coordinator (协调器)
│   ├── 任务分析
│   ├── 代理调度
│   └── 结果整合
├── Research Assistant (研究助手)
│   ├── 网络搜索
│   ├── 信息分析
│   └── 报告生成
├── Message Aggregator (消息聚合器)
│   ├── 多平台接入
│   ├── 优先级过滤
│   └── 消息路由
└── Memory System (记忆系统)
    ├── elite-longterm-memory
    └── fluid-memory
```

---

## 📁 项目结构

```
guiji-shijie-2/
├── skills/
│   └── ultimate-agent/
│       ├── agents/
│       │   ├── coordinator.py       # 代理协调器
│       │   ├── researcher.py        # 研究助手
│       │   ├── message_aggregator.py # 消息聚合器
│       │   └── *.json               # 代理配置
│       ├── main.py                  # 主入口
│       └── README.md                # 本文档
├── memory/                          # 记忆文件
├── PROJECT_PLAN.md                  # 开发计划
└── README.md                        # 项目说明
```

---

## 🎯 核心功能

### 1. 代理协调器

自动分析复杂任务，分解为子任务，分派给专用代理：

```python
from coordinator import AgentCoordinator

coordinator = AgentCoordinator()
result = coordinator.execute_task("研究 AI 技术并发送报告给团队")
```

### 2. 研究助手

自动搜索、分析、生成研究报告：

```python
from researcher import ResearchAssistant

assistant = ResearchAssistant()
report = assistant.research("人工智能最新进展", count=10)
```

### 3. 消息聚合器

统一管理多个消息平台：

```python
from message_aggregator import MessageAggregator, MessagePlatform

aggregator = MessageAggregator()
aggregator.connect_platform(MessagePlatform.WHATSAPP, credentials)
aggregator.send_message("你好！", MessagePlatform.WHATSAPP, "张三")
```

---

## 📋 开发计划

详见 [PROJECT_PLAN.md](PROJECT_PLAN.md)

### Phase 1: 核心功能完善 ✅
- [x] 代理协调器实现
- [x] 研究助手实现
- [x] 消息聚合器实现
- [ ] 集成真实 web_search API
- [ ] 连接真实消息平台

### Phase 2: 自动化系统 ✅
- [x] 心跳检查系统
- [x] 自动任务执行
- [x] 自我改进模块

### Phase 3: 增强功能 (第 3 周)
- [ ] 向量搜索 (LanceDB)
- [ ] 知识图谱 (Git-Notes)
- [ ] 用户界面

---

## 🔧 配置

### 消息平台配置

编辑 `agents/message-aggregator.json`:

```json
{
  "connected_platforms": ["whatsapp", "telegram"],
  "credentials": {
    "whatsapp": { "token": "your-token" },
    "telegram": { "bot_token": "your-bot-token" }
  }
}
```

### 记忆系统配置

详见 `skills/elite-longterm-memory/CONFIG.md`

---

## 🧪 测试

```bash
# 运行测试
python -m pytest tests/

# 测试协调器
python skills/ultimate-agent/agents/coordinator.py

# 测试研究助手
python skills/ultimate-agent/agents/researcher.py

# 测试消息聚合器
python skills/ultimate-agent/agents/message_aggregator.py
```

---

## 📝 使用示例

### 示例 1: 自动研究

```bash
python skills/ultimate-agent/main.py research "2026 年 AI 技术趋势"
```

输出:
```markdown
# 研究摘要：2026 年 AI 技术趋势

**生成时间**: 2026-03-09 10:00:00
**信息来源**: 5 条结果
**置信度**: 80%

## 关键要点

1. 多模态大模型成为主流...
2. AI 代理系统快速发展...
3. ...
```

### 示例 2: 复杂任务

```bash
python skills/ultimate-agent/main.py task "研究机器学习应用并总结要点"
```

### 示例 3: 交互模式

```bash
python skills/ultimate-agent/main.py interactive
```

```
>>> research Python 编程技巧
>>> task 分析项目状态
>>> send whatsapp 张三 你好
>>> status
>>> quit
```

---

## 🤝 贡献

欢迎贡献代码、报告问题、提出建议！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- **OpenClaw** - 强大的 AI 代理框架
- **elite-longterm-memory** - 精英长期记忆系统
- **fluid-memory** - 流体认知架构

---

## 📞 联系方式

- **GitHub**: https://github.com/huoweigang88888/guiji-shijie-2
- **Issues**: https://github.com/huoweigang88888/guiji-shijie-2/issues

---

*硅基世界 2 - 让 AI 为你工作，而不是你为 AI 工作* 🚀
