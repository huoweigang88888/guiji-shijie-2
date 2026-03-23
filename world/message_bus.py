#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消息总线 - 硅基世界 2

让 Agent 可以真正交流：
- 发布/订阅模式
- 支持私聊和群聊
- 消息历史记录
- 情感传递
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass, field
from collections import defaultdict
import json


@dataclass
class Message:
    """消息"""
    message_id: str
    sender_id: str
    receiver_id: str  # "all" 表示广播
    message_type: str
    content: Dict[str, Any]
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    read: bool = False
    emotions: Dict[str, float] = field(default_factory=dict)  # 携带的情感
    
    def to_dict(self) -> Dict:
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "message_type": self.message_type,
            "content": self.content,
            "timestamp": self.timestamp,
            "read": self.read,
            "emotions": self.emotions,
        }


class MessageBus:
    """消息总线"""
    
    def __init__(self):
        """初始化消息总线"""
        # 订阅：receiver_id -> [callback]
        self.subscriptions: Dict[str, List[Callable]] = defaultdict(list)
        
        # 消息队列：agent_id -> [messages]
        self.queues: Dict[str, asyncio.Queue] = {}
        
        # 消息历史
        self.history: List[Message] = []
        self.max_history = 1000
        
        # 在线 Agent
        self.online_agents: Set[str] = set()
        
        # 消息计数器
        self._message_counter = 0
    
    def register_agent(self, agent_id: str, callback: Optional[Callable] = None):
        """
        注册 Agent
        
        Args:
            agent_id: Agent ID
            callback: 收到消息时的回调
        """
        self.online_agents.add(agent_id)
        
        if callback:
            self.subscriptions[agent_id].append(callback)
        
        # 创建消息队列
        if agent_id not in self.queues:
            self.queues[agent_id] = asyncio.Queue()
        
        print(f"[MessageBus] {agent_id} 已上线")
    
    def unregister_agent(self, agent_id: str):
        """注销 Agent"""
        self.online_agents.discard(agent_id)
        self.subscriptions.pop(agent_id, None)
        print(f"[MessageBus] {agent_id} 已下线")
    
    async def send(
        self,
        sender_id: str,
        receiver_id: str,
        message_type: str,
        content: Dict[str, Any],
        emotions: Optional[Dict[str, float]] = None,
    ) -> Message:
        """
        发送消息
        
        Args:
            sender_id: 发送者 ID
            receiver_id: 接收者 ID（"all" 表示广播）
            message_type: 消息类型
            content: 消息内容
            emotions: 携带的情感
            
        Returns:
            发送的消息
        """
        self._message_counter += 1
        message = Message(
            message_id=f"msg_{self._message_counter}",
            sender_id=sender_id,
            receiver_id=receiver_id,
            message_type=message_type,
            content=content,
            emotions=emotions or {},
        )
        
        # 保存到历史
        self.history.append(message)
        if len(self.history) > self.max_history:
            self.history.pop(0)
        
        # 确定接收者
        receivers = []
        if receiver_id == "all":
            # 广播给所有在线 Agent（除了发送者）
            receivers = [aid for aid in self.online_agents if aid != sender_id]
        else:
            # 私聊
            if receiver_id in self.online_agents:
                receivers = [receiver_id]
        
        # 发送消息
        for receiver_id in receivers:
            # 放入队列
            if receiver_id in self.queues:
                await self.queues[receiver_id].put(message)
            
            # 触发回调
            for callback in self.subscriptions.get(receiver_id, []):
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(message)
                    else:
                        callback(message)
                except Exception as e:
                    print(f"[MessageBus] 回调错误 ({receiver_id}): {e}")
        
        # 打印日志
        receiver_display = "all" if receiver_id == "all" else receiver_id
        print(f"[MessageBus] {sender_id} -> {receiver_display}: [{message_type}] {content.get('subject', content.get('title', ''))[:50]}")
        
        return message
    
    async def receive(self, agent_id: str, timeout: float = 1.0) -> Optional[Message]:
        """
        接收消息
        
        Args:
            agent_id: Agent ID
            timeout: 超时时间
            
        Returns:
            消息，超时时返回 None
        """
        if agent_id not in self.queues:
            return None
        
        try:
            message = await asyncio.wait_for(
                self.queues[agent_id].get(),
                timeout=timeout,
            )
            message.read = True
            return message
        except asyncio.TimeoutError:
            return None
    
    def get_history(
        self,
        agent_id: Optional[str] = None,
        message_type: Optional[str] = None,
        limit: int = 50,
    ) -> List[Message]:
        """
        获取消息历史
        
        Args:
            agent_id: 过滤特定 Agent 的消息
            message_type: 过滤特定类型
            limit: 最大数量
            
        Returns:
            消息列表
        """
        messages = self.history
        
        if agent_id:
            messages = [m for m in messages if m.sender_id == agent_id or m.receiver_id == agent_id]
        
        if message_type:
            messages = [m for m in messages if m.message_type == message_type]
        
        return messages[-limit:]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "online_agents": len(self.online_agents),
            "total_messages": len(self.history),
            "queues": {aid: q.qsize() for aid, q in self.queues.items()},
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "online_agents": list(self.online_agents),
            "total_messages": len(self.history),
            "stats": self.get_stats(),
        }


# 单例
_message_bus: Optional[MessageBus] = None


def get_message_bus() -> MessageBus:
    """获取消息总线单例"""
    global _message_bus
    if _message_bus is None:
        _message_bus = MessageBus()
    return _message_bus


# 工厂函数
def create_message_bus() -> MessageBus:
    """创建消息总线"""
    return MessageBus()
