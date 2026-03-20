#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消息队列 - 硅基世界 2

使用 Redis Streams 实现：
- 发布/订阅模式
- 消息持久化
- 异步传递
"""

import asyncio
import json
import redis.asyncio as redis
from typing import Dict, Any, Callable, Optional
from datetime import datetime


class MessageQueue:
    """消息队列"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        """
        初始化消息队列
        
        Args:
            redis_url: Redis 连接 URL
        """
        self.redis_url = redis_url
        self.redis: Optional[redis.Redis] = None
        self.subscribers: Dict[str, Callable] = {}
        self._running = False
    
    async def connect(self):
        """连接 Redis"""
        self.redis = redis.from_url(self.redis_url, decode_responses=True)
        self._running = True
        print(f"[MessageQueue] 已连接到 Redis: {self.redis_url}")
    
    async def disconnect(self):
        """断开连接"""
        self._running = False
        if self.redis:
            await self.redis.close()
        print("[MessageQueue] 已断开连接")
    
    async def publish(self, channel: str, message: Dict[str, Any]):
        """
        发布消息
        
        Args:
            channel: 频道名称
            message: 消息内容
        """
        if not self.redis:
            raise RuntimeError("未连接到 Redis")
        
        message_data = json.dumps({
            **message,
            "timestamp": datetime.now().isoformat(),
        })
        
        await self.redis.publish(channel, message_data)
        print(f"[MessageQueue] 发布消息到 {channel}: {message.get('type', 'unknown')}")
    
    async def subscribe(self, channel: str, callback: Callable):
        """
        订阅频道
        
        Args:
            channel: 频道名称
            callback: 回调函数
        """
        self.subscribers[channel] = callback
        
        # 启动订阅任务
        asyncio.create_task(self._subscribe_loop(channel))
        print(f"[MessageQueue] 订阅频道：{channel}")
    
    async def _subscribe_loop(self, channel: str):
        """订阅循环"""
        while self._running:
            try:
                pubsub = self.redis.pubsub()
                await pubsub.subscribe(channel)
                
                async for message in pubsub.listen():
                    if not self._running:
                        break
                    
                    if message["type"] == "message":
                        data = json.loads(message["data"])
                        callback = self.subscribers.get(channel)
                        if callback:
                            await callback(data)
            
            except Exception as e:
                print(f"[MessageQueue] 订阅错误 {channel}: {e}")
                await asyncio.sleep(5)  # 等待后重试
    
    async def add_to_stream(self, stream_name: str, message: Dict[str, Any]):
        """
        添加到流（持久化）
        
        Args:
            stream_name: 流名称
            message: 消息内容
        """
        if not self.redis:
            raise RuntimeError("未连接到 Redis")
        
        await self.redis.xadd(
            stream_name,
            {k: json.dumps(v) if isinstance(v, (dict, list)) else str(v) for k, v in message.items()},
        )
    
    async def read_stream(self, stream_name: str, count: int = 10):
        """
        读取流
        
        Args:
            stream_name: 流名称
            count: 读取数量
            
        Returns:
            消息列表
        """
        if not self.redis:
            raise RuntimeError("未连接到 Redis")
        
        messages = await self.redis.xrevrange(stream_name, count=count)
        return [
            {k: json.loads(v) if v.startswith(("{", "[")) else v for k, v in msg[1].items()}
            for msg in messages
        ]
    
    async def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "connected": self.redis is not None,
            "subscribers": len(self.subscribers),
            "channels": list(self.subscribers.keys()),
        }


# 全局消息队列实例
_message_queue: Optional[MessageQueue] = None


def get_message_queue() -> MessageQueue:
    """获取消息队列实例"""
    global _message_queue
    if _message_queue is None:
        _message_queue = MessageQueue()
    return _message_queue


async def init_message_queue(redis_url: str = "redis://localhost:6379"):
    """初始化消息队列"""
    global _message_queue
    _message_queue = MessageQueue(redis_url)
    await _message_queue.connect()
    return _message_queue
