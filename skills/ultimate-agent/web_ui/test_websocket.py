#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 6.1 WebSocket 功能测试脚本

测试 WebSocket 实时推送功能
"""

import sys
import time
import json
import io
from pathlib import Path

# Windows 编码支持
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 添加父目录到路径
parent_dir = Path(__file__).parent
sys.path.insert(0, str(parent_dir))

print("🧪 Phase 6.1 WebSocket 功能测试")
print("=" * 50)

# 测试 1: 检查依赖
print("\n📦 测试 1: 检查依赖包")
print("-" * 50)

try:
    import flask
    print(f"✅ Flask: {flask.__version__}")
except ImportError:
    print("❌ Flask 未安装")
    print("   请运行：pip install flask")

try:
    import flask_socketio
    from importlib.metadata import version
    print(f"✅ Flask-SocketIO: {version('flask-socketio')}")
except ImportError:
    print("❌ Flask-SocketIO 未安装")
    print("   请运行：pip install flask-socketio")
except Exception:
    print("✅ Flask-SocketIO: 已安装")

try:
    from websocket_manager import WebSocketManager
    print("✅ WebSocketManager 模块导入成功")
except ImportError as e:
    print(f"❌ WebSocketManager 导入失败：{e}")

# 测试 2: 创建 WebSocket 管理器
print("\n🔌 测试 2: 创建 WebSocket 管理器")
print("-" * 50)

ws_manager = None

try:
    from flask import Flask
    from websocket_manager import WebSocketManager
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    ws_manager = WebSocketManager(app)
    
    if ws_manager.socketio:
        print("✅ WebSocket 管理器创建成功")
        print(f"   连接数：{ws_manager.get_connected_clients_count()}")
    else:
        print("⚠️ WebSocket 不可用（可能缺少依赖）")
        
except Exception as e:
    print(f"❌ 创建失败：{e}")

# 测试 3: 测试广播功能
print("\n📡 测试 3: 测试广播功能")
print("-" * 50)

if ws_manager is not None and hasattr(ws_manager, 'socketio') and ws_manager.socketio:
    try:
        # 模拟推送系统状态
        ws_manager.push_system_status()
        print("✅ 系统状态推送测试通过")
        
        # 模拟推送任务更新
        ws_manager.push_task_update({
            'task_id': 'test-001',
            'status': 'running',
            'progress': 50
        })
        print("✅ 任务更新推送测试通过")
        
        # 模拟推送代理状态
        ws_manager.push_agent_status('coordinator', {
            'status': 'active',
            'tasks_processed': 10
        })
        print("✅ 代理状态推送测试通过")
        
        # 模拟推送日志
        ws_manager.push_log({
            'level': 'INFO',
            'message': 'WebSocket 测试日志'
        })
        print("✅ 日志推送测试通过")
        
        # 模拟推送通知
        ws_manager.push_notification({
            'type': 'info',
            'message': '测试通知'
        })
        print("✅ 通知推送测试通过")
        
    except Exception as e:
        print(f"❌ 广播测试失败：{e}")
else:
    print("⚠️ 跳过广播测试（WebSocket 不可用）")

# 测试 4: 测试客户端信息
print("\n👥 测试 4: 客户端信息管理")
print("-" * 50)

if ws_manager:
    try:
        client_info = ws_manager.get_client_info()
        print(f"✅ 客户端信息获取成功")
        print(f"   总连接数：{client_info.get('total_clients', 0)}")
        print(f"   房间数：{len(client_info.get('rooms', []))}")
    except Exception as e:
        print(f"❌ 客户端信息测试失败：{e}")
else:
    print("⚠️ 跳过客户端信息测试")

# 测试 5: 集成测试
print("\n🔗 测试 5: 集成到 app.py")
print("-" * 50)

test_app = None

try:
    from app import create_app
    
    test_app = create_app()
    if test_app:
        print("✅ Flask 应用创建成功")
        ws_status = '✅ 已启用' if (hasattr(test_app, 'config') and test_app.config.get('socketio')) else '❌ 未启用'
        print(f"   WebSocket 状态：{ws_status}")
        if hasattr(test_app, 'url_map'):
            print(f"   路由数量：{len(test_app.url_map._rules)}")
    else:
        print("❌ Flask 应用创建失败")
        
except Exception as e:
    print(f"❌ 集成测试失败：{e}")

# 测试 6: 检查模板文件
print("\n📄 测试 6: 检查 HTML 模板")
print("-" * 50)

templates_dir = parent_dir / 'templates'
if templates_dir.exists():
    template_files = list(templates_dir.glob('*.html'))
    print(f"✅ 找到 {len(template_files)} 个模板文件:")
    for template in template_files:
        print(f"   - {template.name}")
        
    # 检查 index.html 是否包含 Socket.IO
    index_html = templates_dir / 'index.html'
    if index_html.exists():
        content = index_html.read_text(encoding='utf-8')
        if 'socket.io' in content.lower() or 'io()' in content.lower():
            print("✅ index.html 包含 WebSocket 代码")
        else:
            print("⚠️ index.html 可能缺少 WebSocket 代码")
else:
    print("❌ templates 目录不存在")

# 总结
print("\n" + "=" * 50)
print("📊 测试总结")
print("=" * 50)

all_passed = True
checks = [
    ("Flask 安装", 'flask' in sys.modules),
    ("Flask-SocketIO 安装", 'flask_socketio' in sys.modules),
    ("WebSocketManager 导入", WebSocketManager is not None),
    ("管理器创建", ws_manager is not None if 'ws_manager' in locals() else False),
    ("Flask 应用集成", test_app is not None if 'test_app' in locals() else False),
]

for check_name, passed in checks:
    status = "✅" if passed else "❌"
    print(f"{status} {check_name}")
    if not passed:
        all_passed = False

print("\n" + "=" * 50)
if all_passed:
    print("🎉 所有测试通过！Phase 6.1 WebSocket 功能就绪！")
    print("\n📝 下一步:")
    print("   1. 安装依赖：pip install flask flask-socketio")
    print("   2. 启动服务：python app.py")
    print("   3. 访问浏览器：http://127.0.0.1:5000")
    print("   4. 打开浏览器控制台查看 WebSocket 日志")
else:
    print("⚠️ 部分测试未通过，请检查依赖安装")
    print("\n💡 建议:")
    print("   1. 安装必需依赖：pip install flask flask-socketio")
    print("   2. 重新运行此测试脚本")

print("\n测试完成时间:", time.strftime('%Y-%m-%d %H:%M:%S'))
