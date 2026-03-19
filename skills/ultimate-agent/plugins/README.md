# Plugin Directory

此目录用于存放所有插件。

## 目录结构

```
plugins/
├── __init__.py          # 包初始化
├── plugin_manager.py    # 插件管理器（已在 web_ui 目录）
└── plugins/
    ├── example_plugin/  # 示例插件
    │   ├── __init__.py
    │   └── plugin.py
    └── your_plugin/     # 你的插件
        ├── __init__.py
        └── plugin.py
```

## 创建插件

1. 在 `plugins/plugins/` 目录下创建新文件夹
2. 创建 `__init__.py` 和 `plugin.py`
3. 继承 `Plugin` 基类
4. 实现所需方法

## 插件模板

```python
from plugin_manager import Plugin

name = "my_plugin"
version = "1.0.0"
description = "我的插件"
author = "Your Name"

class Plugin(Plugin):
    def on_load(self):
        print(f"{self.name} 已加载")
    
    def on_unload(self):
        print(f"{self.name} 已卸载")
    
    def on_event(self, event_type, data):
        if event_type == 'user_login':
            print(f"用户 {data.get('username')} 登录")
```

## 可用事件

- `user_login` - 用户登录
- `user_logout` - 用户登出
- `task_create` - 任务创建
- `task_complete` - 任务完成
- `config_change` - 配置变更
- `system_start` - 系统启动
- `system_stop` - 系统停止

## API 端点

```
GET  /api/plugins           - 获取插件列表
GET  /api/plugins/<name>    - 获取插件信息
POST /api/plugins/<name>/enable   - 启用插件
POST /api/plugins/<name>/disable  - 禁用插件
POST /api/plugins/<name>/reload   - 重新加载插件
```
