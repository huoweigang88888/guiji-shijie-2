# 世界状态持久化系统使用指南

## 概述

世界状态持久化系统允许你保存和加载硅基世界的完整状态，包括：
- 世界时间（秒数和天数）
- 时段（清晨/白天/夜晚）
- 所有事件日志
- Agent 关系网络
- 集体知识库
- 故事列表
- 统计数据

## 文件结构

```
saves/
├── {slot}_world_state.json      # 世界状态（时间、事件、统计）
├── {slot}_agents_state.json     # Agent 状态（关系、知识、故事）
├── {slot}_relationships.json    # 关系网络（单独备份）
└── {slot}_metadata.json         # 元数据（版本、保存时间等）
```

## API 使用

### 基本保存/加载

```python
from world.engine import get_world_engine

engine = get_world_engine()

# 保存状态（使用默认槽位 "default"）
engine.save_state()

# 保存到指定槽位
engine.save_state("my_save")

# 加载状态（使用默认槽位）
engine.load_state()

# 从指定槽位加载
engine.load_state("my_save")
```

### 手动保存/加载

```python
# 手动保存
engine.manual_save("manual_001")

# 手动加载
engine.manual_load("manual_001")
```

### 自动保存

自动保存默认每 60 秒执行一次，保存到 "auto" 槽位。

```python
# 设置自动保存间隔（秒）
engine.set_auto_save_interval(30)  # 每 30 秒保存一次

# 自动保存在引擎启动时自动开启
await engine.start()

# 自动保存在引擎停止时自动关闭
await engine.stop()
```

### 存档管理

```python
# 列出所有存档
saves = engine.list_saves()
for save in saves:
    print(f"槽位：{save['slot']}")
    print(f"保存时间：{save['saved_at']}")
    print(f"世界时间：{save['world_time']}秒")
    print(f"天数：{save['day']}")

# 删除存档
engine.delete_save("old_save")
```

## 使用场景

### 1. 游戏会话保存

```python
# 玩家退出时保存
async def on_player_logout():
    engine = get_world_engine()
    engine.save_state("session_" + datetime.now().strftime("%Y%m%d"))
    await engine.stop()

# 玩家加入时加载
async def on_player_join():
    engine = get_world_engine()
    
    # 尝试加载最近的存档
    saves = engine.list_saves()
    if saves:
        latest_save = saves[0]
        engine.load_state(latest_save['slot'])
    
    await engine.start()
```

### 2. 定期备份

```python
# 每天保存一次
async def daily_backup():
    engine = get_world_engine()
    slot = "daily_" + datetime.now().strftime("%Y%m%d")
    engine.save_state(slot)
    print(f"每日备份完成：{slot}")
```

### 3. 实验/测试

```python
# 保存当前状态
engine.save_state("before_experiment")

# ... 进行实验 ...

# 如果需要恢复
engine.load_state("before_experiment")
```

### 4. 分支剧情

```python
# 在关键决策点保存
engine.save_state("branch_point_1")

# 玩家选择 A
# ... 剧情发展 ...

# 如果玩家想回到分支点
engine.load_state("branch_point_1")

# 玩家选择 B
# ... 不同的剧情发展 ...
```

## 数据完整性

持久化系统保证以下数据的完整性：

| 数据类型 | 保存 | 加载 | 验证 |
|---------|------|------|------|
| 世界时间 | ✓ | ✓ | ✓ |
| 天数 | ✓ | ✓ | ✓ |
| 时段 | ✓ | ✓ | ✓ |
| 事件日志 | ✓ | ✓ | ✓ |
| 关系网络 | ✓ | ✓ | ✓ |
| 集体知识 | ✓ | ✓ | ✓ |
| 故事列表 | ✓ | ✓ | ✓ |
| 统计数据 | ✓ | ✓ | ✓ |

## 测试

运行测试脚本验证持久化系统：

```bash
cd silicon-world-2
python world/test_persistence.py
```

测试包括：
1. 保存世界状态
2. 验证文件创建
3. 加载世界状态
4. 验证数据完整性
5. 测试存档列表
6. 测试自动保存功能

## 注意事项

1. **存档槽位命名**：使用字母、数字和下划线，避免特殊字符
2. **自动保存间隔**：建议不少于 10 秒，避免频繁 I/O
3. **磁盘空间**：定期清理旧存档，避免占用过多空间
4. **并发访问**：避免同时保存和加载同一个槽位
5. **版本兼容**：存档包含版本号，未来版本可能不兼容旧格式

## 故障排除

### 保存失败
- 检查 `saves/` 目录是否存在
- 检查磁盘空间
- 检查文件权限

### 加载失败
- 确认槽位存在（使用 `list_saves()` 检查）
- 检查存档文件是否完整
- 验证 JSON 格式是否正确

### 自动保存未运行
- 确认引擎已启动（`_running = True`）
- 检查自动保存线程是否正常
- 调整保存间隔（可能太短导致问题）

## 扩展

如需添加新的数据字段到存档中：

1. 在 `save_state()` 中添加新字段到相应的字典
2. 在 `load_state()` 中恢复新字段（提供默认值以兼容旧存档）
3. 更新 `metadata.json` 中的版本号
4. 更新测试脚本验证新字段

---

**版本**: 1.0  
**最后更新**: 2026-04-07
