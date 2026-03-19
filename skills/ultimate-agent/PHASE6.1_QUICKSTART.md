# Phase 6.1 WebSocket 快速启动指南

## 🚀 5 分钟启动 WebSocket 实时推送

### 1. 安装依赖 (30 秒)

```bash
pip install flask flask-socketio
```

### 2. 启动 Web UI (10 秒)

```bash
cd C:\Users\97RPZ8T\.openclaw\workspace\skills\ultimate-agent
python main.py webui
```

或者使用独立启动脚本：

```bash
python web_ui/start_dashboard.py
```

### 3. 访问仪表板 (5 秒)

打开浏览器访问：
```
http://127.0.0.1:5000
```

### 4. 验证 WebSocket 连接 (1 分钟)

1. 打开浏览器开发者工具 (F12)
2. 切换到 **Console** 标签
3. 查看日志输出：

```
🔌 正在连接 WebSocket...
✅ WebSocket 已连接
📊 收到状态更新：{...}
```

4. 查看 **Network** 标签
5. 筛选 **WS** (WebSocket)
6. 应该看到活跃的 WebSocket 连接

### 5. 测试实时推送 (可选)

打开浏览器控制台，输入：

```javascript
// 手动请求状态更新
socket.emit('request_status');

// 发送心跳
socket.emit('ping');

// 订阅特定主题
socket.emit('subscribe', { topic: 'tasks' });
```

---

## 📊 功能验证

### WebSocket 状态指示器

查看页面底部状态栏：

- 🟢 **已连接** - WebSocket 正常工作
- 🔴 **已断开** - 连接断开，正在重连
- 🟡 **连接失败** - 无法连接，使用轮询模式
- ⚪ **未连接** - 正在初始化

### 实时推送测试

在另一个终端运行系统，观察仪表板：

1. **系统状态更新** - 每 30 秒自动推送
2. **任务状态变更** - 任务创建/更新/完成时
3. **代理状态更新** - 代理激活/停用时
4. **日志流式传输** - 实时日志推送
5. **通知推送** - 新通知到达时

---

## 🔧 故障排查

### 问题 1: WebSocket 未连接

**症状**: 状态显示 🟡 或 🔴

**解决方案**:
```bash
# 1. 检查依赖
pip show flask flask-socketio

# 2. 重新安装
pip install --upgrade flask flask-socketio

# 3. 重启服务
python main.py webui
```

### 问题 2: 连接后立即断开

**可能原因**: 防火墙/代理阻止

**解决方案**:
1. 检查防火墙设置
2. 关闭代理软件
3. 使用 localhost 而非 0.0.0.0

### 问题 3: 轮询模式降级

**症状**: 状态显示 ⚪，使用轮询而非 WebSocket

**原因**: Flask-SocketIO 未正确安装

**解决方案**:
```bash
pip uninstall flask-socketio
pip install flask-socketio
```

---

## 📝 配置选项

### 自定义端口

```bash
python main.py webui 0.0.0.0 8080
```

### 调试模式

```bash
python main.py webui --debug
```

### 仅测试 UI（不加载后端）

```bash
python web_ui/start_dashboard.py --no-system
```

---

## 🎯 下一步

### Phase 6.1 扩展
- [ ] 更新 agents.html 添加 WebSocket
- [ ] 更新 tasks.html 添加 WebSocket
- [ ] 更新 logs.html 实现日志流
- [ ] 添加任务创建功能

### Phase 6.2 计划
- [ ] 代理配置界面
- [ ] 通知中心
- [ ] 报告预览
- [ ] 移动端优化

---

## 📚 相关文档

- `PHASE6.1_COMPLETE.md` - 完整完成报告
- `PHASE6.1_PROGRESS.md` - 开发记录
- `websocket_manager.py` - API 文档
- `test_websocket.py` - 测试脚本

---

**版本**: v3.2.0 - Phase 6.1 Edition  
**更新时间**: 2026-03-12  
**开发者**: 三二 🐱
