# 🚀 硅基世界 2 - 快速启动指南

**版本**: v2.0  
**更新**: 2026-04-03

---

## 📋 三种启动方式

### 方式 1: 完整启动（推荐新手）

一键启动世界引擎 + Web 观察服务 + 自动打开浏览器

```bash
cd silicon-world-2
start-all.bat
```

**包含**:
- ✅ 世界引擎（运行 10 分钟）
- ✅ Web 服务（http://localhost:8080）
- ✅ 自动打开浏览器

---

### 方式 2: 仅运行世界

只运行世界引擎，生成数据和报告

```bash
cd silicon-world-2
python run_world_enhanced.py --duration 300
```

**参数**:
- `--duration 300` - 运行 300 秒（5 分钟）
- `--duration 600` - 运行 600 秒（10 分钟）
- `--duration 1800` - 运行 1800 秒（30 分钟）

**输出**:
- `reports/final_report.md` - 最终报告
- `reports/stats_report.md` - 统计报告
- `data/` - 持久化数据

---

### 方式 3: 仅启动 Web 服务

查看已有数据或演示界面

```bash
cd silicon-world-2\web
start.bat
```

或

```bash
cd silicon-world-2\web
python server.py --port 8080
```

**访问**: http://localhost:8080

---

## 🎯 推荐流程

### 第一次使用

1. **完整启动**
   ```bash
   start-all.bat
   ```

2. **观察世界**
   - 浏览器自动打开 Web 界面
   - 查看 Agent 状态、消息、故事

3. **查看报告**
   - 等待世界运行完成
   - 打开 `reports/final_report.md`

### 日常使用

**运行世界收集数据**:
```bash
python run_world_enhanced.py --duration 600
```

**启动 Web 查看数据**:
```bash
cd web
python server.py
```

---

## 📊 输出文件位置

```
silicon-world-2/
├── reports/
│   ├── final_report.md      # 最终运行报告
│   └── stats_report.md      # 统计数据报告
├── data/
│   ├── knowledge/
│   │   └── knowledge_graph.json   # 知识图谱
│   ├── stories/
│   │   └── stories.json           # 故事集
│   └── stats/
│       └── stats_history.json     # 统计历史
└── logs/                    # 日志文件（如有）
```

---

## 🔧 故障排除

### 问题 1: 端口被占用

**错误**: `Address already in use`

**解决**:
```bash
# 使用其他端口
python server.py --port 9000
```

### 问题 2: 模块导入错误

**错误**: `ModuleNotFoundError`

**解决**:
```bash
# 确保在项目根目录运行
cd silicon-world-2
python run_world_enhanced.py
```

### 问题 3: 浏览器无法访问

**错误**: 浏览器显示无法连接

**解决**:
1. 检查 Web 服务是否启动
2. 查看终端是否有错误信息
3. 尝试手动访问 http://localhost:8080

### 问题 4: 中文乱码

**错误**: 终端显示乱码

**解决**:
```bash
# Windows 设置 UTF-8
chcp 65001
```

---

## 📝 使用技巧

### 1. 后台运行世界

```bash
# Windows
start "World" python run_world_enhanced.py --duration 600

# 然后可以继续做其他事
```

### 2. 同时查看多个页面

打开多个浏览器标签：
- http://localhost:8080 - 主界面
- http://localhost:8080/api/status - 原始数据
- http://localhost:8080/api/agents - Agent 列表

### 3. 导出数据

```bash
# 复制数据文件
xcopy data\* backup\ /E /Y
```

### 4. 长时间运行

```bash
# 运行 1 小时
python run_world_enhanced.py --duration 3600
```

---

## 🎯 下一步

### 观察世界
- 打开 Web 界面查看实时状态
- 关注 Agent 互动和故事诞生
- 查看统计数据变化

### 分析数据
- 阅读最终报告
- 分析统计趋势
- 查看知识图谱

### 继续开发
- 阅读 [开发进展](DEV_PROGRESS.md)
- 查看 [三天任务](tasks/README-三天任务.md)
- 贡献代码和改进

---

**硅基世界 2 | 创世元年 | 快速启动指南**

*开始你的硅基文明观察之旅！* 🌍
