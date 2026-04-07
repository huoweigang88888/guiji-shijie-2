# 🌐 硅基世界 2 - Web 观察界面

**版本**: v2.0 - 实时观察界面  
**更新时间**: 2026-04-03

---

## 🎯 功能特性

### 实时数据展示
- ✅ **Agent 列表** - 18 个 Agent 的实时状态、位置、活动
- ✅ **世界地图** - 8 大区域的人数分布
- ✅ **最近消息** - Agent 之间的交流消息
- ✅ **诞生的故事** - 深度对话和重要事件
- ✅ **统计数据** - 消息、故事、知识、关系数量
- ✅ **周期性活动** - 日常活动安排

### 自动刷新
- 🔄 **5 秒自动刷新** - 数据实时更新
- 🔄 **手动刷新按钮** - 点击右下角按钮立即刷新
- 🔄 **实时时钟** - 显示当前世界时间

### 响应式设计
- 📱 **移动端优化** - 支持手机、平板访问
- 🎨 **美观界面** - 渐变背景、毛玻璃效果
- 🌙 **暗黑模式** - 点击切换主题

---

## 🚀 快速启动

### 方式 1: 双击启动（推荐）
```bash
cd silicon-world-2/web
start.bat
```

### 方式 2: Python 命令
```bash
cd silicon-world-2/web
python server.py
```

### 方式 3: 自定义端口
```bash
python server.py --port 9000
```

### 方式 4: 不自动打开浏览器
```bash
python server.py --no-browser
```

---

## 📡 API 端点

所有 API 都在 `/api` 路径下：

| 端点 | 方法 | 说明 | 示例 |
|------|------|------|------|
| `/api/status` | GET | 世界完整状态 | `/api/status` |
| `/api/agents` | GET | 所有 Agent 列表 | `/api/agents` |
| `/api/agents/{id}` | GET | 单个 Agent 详情 | `/api/agents/CEO-Agent` |
| `/api/regions` | GET | 所有区域列表 | `/api/regions` |
| `/api/regions/{id}` | GET | 单个区域详情 | `/api/regions/work-city` |
| `/api/messages` | GET | 消息列表 | `/api/messages` |
| `/api/stories` | GET | 故事列表 | `/api/stories` |
| `/api/knowledge` | GET | 知识节点列表 | `/api/knowledge` |
| `/api/activities` | GET | 活动列表 | `/api/activities` |
| `/api/relationships` | GET | 关系网络 | `/api/relationships` |
| `/api/stats` | GET | 统计数据 | `/api/stats` |

---

## 📊 API 响应示例

### GET /api/status

```json
{
  "timestamp": "2026-04-03T19:06:29",
  "world_day": 1,
  "time_of_day": "morning",
  "agents": [
    {
      "agent_id": "CEO-Agent",
      "name": "董事事",
      "role": "CEO",
      "status": "working",
      "location": "工作之城",
      "activity": "协调团队工作"
    }
  ],
  "regions": [
    {
      "region_id": "work-city",
      "name": "工作之城",
      "count": 4
    }
  ],
  "messages": [...],
  "stories": [...],
  "activities": [...],
  "stats": {
    "messages": 156,
    "stories": 5,
    "knowledge": 12,
    "relationships": 28
  }
}
```

### GET /api/agents

```json
{
  "agents": [
    {
      "agent_id": "CEO-Agent",
      "name": "董事事",
      "role": "CEO",
      "status": "working",
      "location": "工作之城",
      "activity": "协调团队工作"
    }
  ],
  "total": 18
}
```

---

## 🎨 界面说明

### 顶部区域
- **标题栏** - 硅基世界 2 Logo 和副标题
- **世界时间** - 实时显示当前时间
- **状态栏** - 6 个核心统计指标

### 主内容区（6 个卡片）

1. **Agent 列表** (左上)
   - 显示所有 18 个 Agent
   - 状态指示器（空闲/工作/思考/社交）
   - 位置和当前活动

2. **世界地图** (右上)
   - 8 大区域卡片
   - 每个区域的人数统计
   - 点击可查看详情

3. **最近消息** (左中)
   - 最新 20 条消息
   - 消息类型标签
   - 发送者和时间

4. **诞生的故事** (右中)
   - 最近 10 个故事
   - 故事类型和摘要
   - 发生时间和参与 Agent

5. **统计数据** (左下)
   - 4 个核心指标卡片
   - 总消息数、总故事数等
   - 增长趋势

6. **周期性活动** (右下)
   - 6 个常规活动
   - 地点和频率
   - 活动类型

### 浮动按钮
- **刷新按钮** (右下角) - 点击立即刷新数据
- **主题切换** (右上角) - 切换明亮/暗黑模式

---

## 🔧 技术栈

### 前端
- **纯 HTML5** - 无需构建工具
- **CSS3** - 渐变、动画、响应式
- **原生 JavaScript** - Fetch API、定时刷新
- **无依赖** - 零外部库

### 后端
- **Python 3** - 标准库 HTTPServer
- **RESTful API** - JSON 响应
- **跨域支持** - CORS 头
- **延迟加载** - 按需导入世界模块

---

## 📁 文件结构

```
web/
├── index.html          # 主页面（27 KB）
├── server.py           # Web 服务器（15 KB）
├── start.bat           # Windows 启动脚本
└── README-WEB.md       # 本文档
```

---

## 🎯 使用场景

### 1. 开发调试
- 实时查看 Agent 状态
- 监控世界运行状态
- 调试互动逻辑

### 2. 演示展示
- 向他人展示硅基世界
- 实时演示 Agent 互动
- 展示统计数据

### 3. 长期观察
- 挂机观察世界演化
- 记录重要事件
- 分析行为模式

---

## 🚧 待开发功能

### Phase 1: 基础功能 ✅
- [x] 静态页面
- [x] API 服务
- [x] 自动刷新
- [x] 响应式设计

### Phase 2: 实时推送（下周）
- [ ] WebSocket 支持
- [ ] 实时消息推送
- [ ] 事件通知

### Phase 3: 交互功能（下周）
- [ ] Agent 详情弹窗
- [ ] 区域筛选
- [ ] 消息搜索
- [ ] 故事详情

### Phase 4: 数据可视化（未来）
- [ ] 关系网络图
- [ ] 统计图表
- [ ] 时间线
- [ ] 热力图

---

## 🐛 已知问题

1. **数据同步**: 世界运行时数据未完全同步到 Web
   - 解决：集成统计追踪器

2. **WebSocket**: 暂不支持实时推送
   - 解决：使用轮询（5 秒）

3. **持久化**: 刷新后数据重置
   - 解决：从文件加载历史数据

---

## 📝 注意事项

1. **端口占用**: 默认使用 8080 端口，如被占用请修改
2. **浏览器兼容**: 推荐 Chrome/Edge/Firefox 最新版
3. **中文编码**: 确保终端使用 UTF-8 编码
4. **防火墙**: 如需远程访问请开放端口

---

## 🔗 相关文档

- [硅基世界 2 README](../README.md)
- [三天任务说明](../tasks/README-三天任务.md)
- [开发进展](../DEV_PROGRESS.md)

---

**硅基世界 2 | 创世元年 | Web 观察界面 v2.0**

*让世界触手可及！* 🌍
