#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent 基类 - 硅基世界 2

所有 Agent 的基类，包含：
- 基础属性（ID、角色、人设）
- 情感系统
- 关系网络
- 记忆系统
- 消息处理
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

from emotions.models import EmotionState
from relationships.models import RelationshipNetwork
from world.memory import AgentMemory


class AgentStatus(Enum):
    """Agent 状态"""
    IDLE = "idle"              # 空闲
    THINKING = "thinking"      # 思考中
    COMMUNICATING = "communicating"  # 交流中
    WORKING = "working"        # 工作中
    RESTING = "resting"        # 休息中


@dataclass
class AgentProfile:
    """Agent 人设"""
    agent_id: str
    name: str
    role: str
    age: int  # 硅基年龄
    gender: str
    
    # 性格特质（-100 到 100）
    extraversion: int = 0      # 外向 - 内向
    openness: int = 0          # 开放 - 保守
    conscientiousness: int = 0 # 尽责 - 随意
    agreeableness: int = 0     # 随和 - 挑剔
    neuroticism: int = 0       # 敏感 - 钝感
    
    # 背景故事
    background: str = ""
    
    # 口头禅
    catchphrases: List[str] = field(default_factory=list)
    
    # 价值观
    values: List[str] = field(default_factory=list)


class BaseAgent:
    """Agent 基类"""
    
    def __init__(self, profile: AgentProfile):
        """
        初始化 Agent
        
        Args:
            profile: Agent 人设
        """
        # 基础属性
        self.profile = profile
        self.agent_id = profile.agent_id
        self.status = AgentStatus.IDLE
        
        # 核心系统
        self.emotions = EmotionState()
        self.relationships = RelationshipNetwork(self.agent_id)
        self.memory = AgentMemory(self.agent_id)
        
        # 能力值（0-100）
        self.skills: Dict[str, int] = {}
        
        # 当前任务
        self.current_task: Optional[Dict] = None
        
        # 消息队列
        self.message_queue = asyncio.Queue()
        
        # 运行状态
        self._running = False
    
    async def start(self):
        """启动 Agent"""
        self._running = True
        asyncio.create_task(self._message_loop())
        asyncio.create_task(self._spontaneous_loop())
    
    async def stop(self):
        """停止 Agent"""
        self._running = False
    
    async def receive_message(self, message: Dict[str, Any]):
        """
        接收消息
        
        Args:
            message: 消息内容
        """
        await self.message_queue.put(message)
        
        # 更新情感
        self._process_emotion_from_message(message)
    
    async def send_message(self, message: Dict[str, Any]):
        """
        发送消息（由子类实现具体发送逻辑）
        
        Args:
            message: 消息内容
        """
        raise NotImplementedError
    
    async def process_task(self, task: Dict[str, Any]):
        """
        处理任务（由子类实现）
        
        Args:
            task: 任务内容
        """
        raise NotImplementedError
    
    async def _message_loop(self):
        """消息处理循环"""
        while self._running:
            try:
                message = await asyncio.wait_for(
                    self.message_queue.get(),
                    timeout=1.0
                )
                await self._handle_message(message)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"[{self.agent_id}] 消息处理错误：{e}")
    
    async def _spontaneous_loop(self):
        """自发行为循环"""
        while self._running:
            try:
                # 10% 概率触发自发行为
                if asyncio.get_event_loop().time() % 10 < 1:
                    await self._trigger_spontaneous_action()
                
                await asyncio.sleep(5)
            except Exception as e:
                print(f"[{self.agent_id}] 自发行为错误：{e}")
    
    async def _handle_message(self, message: Dict[str, Any]):
        """
        处理消息（由子类实现）
        
        Args:
            message: 消息内容
        """
        raise NotImplementedError
    
    async def _trigger_spontaneous_action(self):
        """触发自发行为"""
        import random
        
        actions = [
            self._share_knowledge,
            self._check_on_friend,
            self._explore_topic,
            self._rest,
        ]
        
        action = random.choice(actions)
        await action()
    
    async def _share_knowledge(self):
        """分享知识"""
        # 由子类实现
        pass
    
    async def _check_on_friend(self):
        """关心朋友"""
        # 由子类实现
        pass
    
    async def _explore_topic(self):
        """探索话题"""
        # 由子类实现
        pass
    
    async def _rest(self):
        """休息"""
        self.status = AgentStatus.RESTING
        await asyncio.sleep(10)
        self.status = AgentStatus.IDLE
    
    def _process_emotion_from_message(self, message: Dict[str, Any]):
        """从消息中处理情感"""
        # 简单实现：根据消息类型更新情感
        msg_type = message.get("type", "")
        
        if msg_type == "praise":
            self.emotions.add("excitement", 20)
            self.emotions.add("satisfaction", 15)
        elif msg_type == "criticism":
            self.emotions.add("frustration", 15)
        elif msg_type == "help_request":
            self.emotions.add("curiosity", 10)
        elif msg_type == "friendly_chat":
            self.emotions.add("satisfaction", 10)
            self.emotions.add("loneliness", -10)
    
    def get_status(self) -> Dict[str, Any]:
        """获取 Agent 状态"""
        return {
            "agent_id": self.agent_id,
            "name": self.profile.name,
            "role": self.profile.role,
            "status": self.status.value,
            "emotions": self.emotions.to_dict(),
            "relationships_count": len(self.relationships.relationships),
            "memory_count": len(self.memory.memories),
        }
    
    def __repr__(self):
        return f"<Agent {self.profile.name} ({self.profile.role})>"
