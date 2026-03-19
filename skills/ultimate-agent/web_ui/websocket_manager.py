#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebSocket 实时推送模块 - Phase 6.1

为 Web UI 提供实时双向通信能力，替代轮询机制
支持：
- 系统状态实时推送
- 任务状态变更通知
- 日志流式传输
- 代理状态更新
"""

import json
import asyncio
import logging
from datetime import datetime
from typing import Set, Dict, Any, Optional
from pathlib import Path

try:
    from flask import Flask
    from flask_socketio import SocketIO, emit, join_room, leave_room
    SOCKETIO_AVAILABLE = True
except ImportError:
    SOCKETIO_AVAILABLE = False
    print("[WARN] Flask-SocketIO 未安装，请运行：pip install flask-socketio")

logger = logging.getLogger('websocket')


class WebSocketManager:
    """
    WebSocket 连接管理器
    
    管理所有客户端连接，提供实时推送能力
    """
    
    def __init__(self, app: Optional[Flask] = None):
        """
        初始化 WebSocket 管理器
        
        Args:
            app: Flask 应用实例（可选）
        """
        self.app = app
        self.socketio = None
        self.clients: Set[str] = set()  # 客户端 ID 集合
        self.client_rooms: Dict[str, str] = {}  # 客户端房间映射
        self.system_instance = None
        
        if not SOCKETIO_AVAILABLE:
            logger.warning("Flask-SocketIO 不可用，WebSocket 功能将被禁用")
            return
        
        if app:
            self.socketio = SocketIO(
                app,
                cors_allowed_origins="*",
                async_mode='threading',
                logger=True,
                engineio_logger=True
            )
            self._register_handlers()
            logger.info("WebSocket 管理器已初始化")
    
    def set_system(self, system_instance):
        """设置系统实例"""
        self.system_instance = system_instance
    
    def _register_handlers(self):
        """注册 WebSocket 事件处理器"""
        if not self.socketio:
            return
        
        @self.socketio.on('connect')
        def handle_connect():
            """客户端连接"""
            from flask import request
            client_id = request.sid
            self.clients.add(client_id)
            logger.info(f"客户端连接：{client_id}")
            emit('connected', {'client_id': client_id, 'message': '已连接到硅基世界 2'})
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """客户端断开"""
            from flask import request
            client_id = request.sid
            self.clients.discard(client_id)
            if client_id in self.client_rooms:
                leave_room(self.client_rooms[client_id])
                del self.client_rooms[client_id]
            logger.info(f"客户端断开：{client_id}")
        
        @self.socketio.on('join')
        def handle_join(data):
            """加入房间"""
            from flask import request
            client_id = request.sid
            room = data.get('room', 'default')
            join_room(room)
            self.client_rooms[client_id] = room
            logger.info(f"客户端 {client_id} 加入房间 {room}")
            emit('joined', {'room': room})
        
        @self.socketio.on('leave')
        def handle_leave(data):
            """离开房间"""
            from flask import request
            client_id = request.sid
            room = data.get('room', 'default')
            leave_room(room)
            if client_id in self.client_rooms and self.client_rooms[client_id] == room:
                del self.client_rooms[client_id]
            logger.info(f"客户端 {client_id} 离开房间 {room}")
        
        @self.socketio.on('subscribe')
        def handle_subscribe(data):
            """订阅特定主题"""
            from flask import request
            client_id = request.sid
            topic = data.get('topic')
            if topic:
                join_room(topic)
                logger.info(f"客户端 {client_id} 订阅主题 {topic}")
                emit('subscribed', {'topic': topic})
        
        @self.socketio.on('unsubscribe')
        def handle_unsubscribe(data):
            """取消订阅"""
            from flask import request
            client_id = request.sid
            topic = data.get('topic')
            if topic:
                leave_room(topic)
                logger.info(f"客户端 {client_id} 取消订阅 {topic}")
        
        @self.socketio.on('ping')
        def handle_ping():
            """心跳检测"""
            emit('pong', {'timestamp': datetime.now().isoformat()})
        
        @self.socketio.on('request_status')
        def handle_request_status():
            """请求系统状态"""
            if self.system_instance:
                status = self.system_instance.get_status()
                emit('status_update', status)
            else:
                emit('status_update', {'status': 'no_system'})
        
        @self.socketio.on('request_tasks')
        def handle_request_tasks():
            """请求任务队列"""
            if self.system_instance and hasattr(self.system_instance, 'task_queue'):
                tasks = self.system_instance.task_queue.get_queue_status()
                emit('tasks_update', tasks)
    
    def broadcast(self, event: str, data: Dict[str, Any], room: Optional[str] = None):
        """
        广播消息
        
        Args:
            event: 事件名称
            data: 数据字典
            room: 房间名（可选，None 表示广播给所有客户端）
        """
        if not self.socketio:
            return
        
        if room:
            self.socketio.emit(event, data, room=room)
        else:
            self.socketio.emit(event, data)
        
        logger.debug(f"广播事件 {event} 到 {room or '所有客户端'}")
    
    def send_to_client(self, client_id: str, event: str, data: Dict[str, Any]):
        """
        发送消息到特定客户端
        
        Args:
            client_id: 客户端 ID
            event: 事件名称
            data: 数据字典
        """
        if not self.socketio:
            return
        
        self.socketio.emit(event, data, room=client_id)
        logger.debug(f"发送事件 {event} 到客户端 {client_id}")
    
    def push_system_status(self):
        """推送系统状态更新"""
        if not self.system_instance:
            return
        
        status = self.system_instance.get_status()
        status['timestamp'] = datetime.now().isoformat()
        self.broadcast('status_update', status)
    
    def push_task_update(self, task_data: Dict[str, Any]):
        """
        推送任务更新
        
        Args:
            task_data: 任务数据
        """
        task_data['timestamp'] = datetime.now().isoformat()
        self.broadcast('task_update', task_data, room='tasks')
    
    def push_agent_status(self, agent_id: str, status: Dict[str, Any]):
        """
        推送代理状态更新
        
        Args:
            agent_id: 代理 ID
            status: 状态数据
        """
        data = {
            'agent_id': agent_id,
            'status': status,
            'timestamp': datetime.now().isoformat()
        }
        self.broadcast('agent_update', data, room='agents')
    
    def push_log(self, log_entry: Dict[str, Any]):
        """
        推送日志条目
        
        Args:
            log_entry: 日志数据 {'level': str, 'message': str, 'timestamp': str}
        """
        log_entry['timestamp'] = log_entry.get('timestamp', datetime.now().isoformat())
        self.broadcast('log_entry', log_entry, room='logs')
    
    def push_notification(self, notification: Dict[str, Any]):
        """
        推送通知
        
        Args:
            notification: 通知数据
        """
        notification['timestamp'] = notification.get('timestamp', datetime.now().isoformat())
        self.broadcast('notification', notification, room='notifications')
    
    def get_connected_clients_count(self) -> int:
        """获取已连接的客户端数量"""
        return len(self.clients)
    
    def get_client_info(self) -> Dict[str, Any]:
        """获取客户端信息"""
        return {
            'total_clients': len(self.clients),
            'rooms': list(set(self.client_rooms.values())),
            'client_ids': list(self.clients)
        }


class LogStreamHandler(logging.Handler):
    """
    日志流式处理器
    
    将日志记录通过 WebSocket 实时推送
    """
    
    def __init__(self, ws_manager: WebSocketManager):
        """
        初始化
        
        Args:
            ws_manager: WebSocket 管理器
        """
        super().__init__()
        self.ws_manager = ws_manager
        self.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    
    def emit(self, record):
        """发送日志记录"""
        try:
            log_entry = {
                'level': record.levelname,
                'message': self.format(record),
                'logger': record.name,
                'timestamp': datetime.fromtimestamp(record.created).isoformat()
            }
            self.ws_manager.push_log(log_entry)
        except Exception:
            self.handleError(record)


def init_websocket(app: Flask, system_instance=None) -> WebSocketManager:
    """
    初始化 WebSocket
    
    Args:
        app: Flask 应用
        system_instance: 系统实例
    
    Returns:
        WebSocketManager 实例
    """
    ws_manager = WebSocketManager(app)
    ws_manager.set_system(system_instance)
    
    # 添加日志流处理器
    root_logger = logging.getLogger()
    log_handler = LogStreamHandler(ws_manager)
    log_handler.setLevel(logging.INFO)
    root_logger.addHandler(log_handler)
    
    return ws_manager


# 使用示例
if __name__ == '__main__':
    print("🧪 WebSocket 模块测试")
    print("=" * 40)
    
    if not SOCKETIO_AVAILABLE:
        print("❌ Flask-SocketIO 未安装")
        print("\n请安装依赖:")
        print("  pip install flask-socketio")
    else:
        print("✅ Flask-SocketIO 已安装")
        print("\nWebSocket 模块已就绪")
        print("\n在 app.py 中集成:")
        print("  from websocket_manager import init_websocket")
        print("  ws_manager = init_websocket(app, system_instance)")
