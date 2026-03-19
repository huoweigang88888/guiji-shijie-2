# 🚀 硅基世界 2 - 快速启动指南

**5 分钟上手你的 AI 代理系统！**

---

## ⚡ 快速开始（3 步搞定）

### 第 1 步：安装依赖

```bash
cd C:\Users\97RPZ8T\.openclaw\workspace\skills\ultimate-agent

# 基础依赖（必需）
pip install requests

# 完整依赖（推荐）
pip install -r requirements.txt
```

### 第 2 步：测试系统

```bash
# 查看系统状态
python main.py status

# 运行心跳检查
python main.py heartbeat

# 查看改进建议
python main.py improvements
```

### 第 3 步：启动 Web UI（可选）

```bash
# 安装 Flask
pip install flask

# 启动 Web 仪表板
python main.py webui

# 访问 http://127.0.0.1:5000
```

---

## 📋 常用命令

### 系统管理

```bash
# 查看系统状态
python main.py status

# 心跳检查
python main.py heartbeat

# 查看改进建议
python main.py improvements

# 执行待处理任务
python main.py exec-tasks

# 进入交互模式
python main.py interactive
```

### 任务管理

```bash
# 执行任务
python main.py task "研究 AI 发展趋势"

# 创建目标
# （在交互模式中使用 goal 命令）
```

### 研究功能

```bash
# 研究主题
python main.py research "机器学习最新进展"

# 生成研究报告
python main.py research-report "深度学习应用" markdown

# 查看报告列表
python main.py reports
```

### 通知功能

```bash
# 发送通知
python main.py notify "系统警告" "CPU 使用率过高" console high

# 查看通知统计
python main.py notify-stats
```

### 报告生成

```bash
# 生成简单报告
python main.py report "项目进度报告" markdown

# 生成 HTML 报告
python main.py report "月度总结" html

# 查看已有报告
python main.py reports
```

### Web UI

```bash
# 启动 Web 仪表板（默认端口 5000）
python main.py webui

# 自定义端口
python main.py webui 0.0.0.0 8080

# 调试模式
python main.py webui --debug
```

---

## 🌐 Web UI 页面

启动 Web UI 后，可以访问以下页面：

| 页面 | 地址 | 功能 |
|------|------|------|
| 📊 仪表板 | `/` | 系统总览、代理状态、任务统计 |
| 🤖 代理管理 | `/agents.html` | 查看所有代理状态 |
| 📋 任务队列 | `/tasks.html` | 任务列表和进度 |
| 🕸️ 知识图谱 | `/graph.html` | 交互式图谱可视化 |
| 📜 系统日志 | `/logs.html` | 实时日志查看 |

---

## 🧪 测试示例

### 示例 1：执行研究任务

```bash
python main.py interactive
```

然后输入：
```
research 2026 年 AI 发展趋势
```

### 示例 2：添加知识节点

```bash
python main.py interactive
```

然后输入：
```
g-add Python Python 是一种编程语言 language programming
```

### 示例 3：发送通知

```bash
python main.py notify "测试通知" "这是一条测试消息" console normal
```

---

## 📁 项目结构

```
ultimate-agent/
├── agents/                  # 代理模块
│   ├── coordinator.py       # 协调器
│   ├── researcher.py        # 研究员
│   ├── notification_agent.py # 通知代理
│   ├── report_generator.py  # 报告生成器
│   ├── api_integration.py   # API 集成
│   ├── task_queue.py        # 任务队列
│   ├── config_manager.py    # 配置管理
│   └── ...
├── web_ui/                  # Web 界面
│   ├── app.py               # Flask 应用
│   └── templates/           # HTML 模板
├── main.py                  # 主入口
├── requirements.txt         # 依赖包
├── QUICKSTART.md            # 本文档
└── ...
```

---

## 🔧 常见问题

### Q: Flask 安装失败？

**A**: 尝试使用国内镜像：
```bash
pip install flask -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: 端口被占用？

**A**: 使用其他端口：
```bash
python main.py webui 127.0.0.1 8080
```

### Q: 如何停止 Web UI？

**A**: 按 `Ctrl+C` 终止服务

### Q: 日志在哪里？

**A**: 查看 `logs/` 目录或在 Web UI 的"系统日志"页面查看

### Q: 如何配置 API 密钥？

**A**: 编辑 `api-configs/apis.json` 文件

---

## 📖 更多文档

- `README.md` - 项目说明
- `USAGE_GUIDE.md` - 详细使用指南
- `PHASE5_COMPLETE.md` - Phase 5 完成报告
- `PHASE6_SUMMARY.md` - Phase 6 完成报告
- `CHANGELOG.md` - 版本变更记录

---

## 🎯 下一步

1. ✅ 完成快速启动
2. ✅ 测试基本功能
3. 📚 阅读详细文档
4. 🔧 配置消息平台
5. 🚀 开始使用！

---

**遇到问题？** 查看 `USAGE_GUIDE.md` 或提交 Issue！

**版本**: v3.2.0  
**更新时间**: 2026-03-11
