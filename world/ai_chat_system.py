#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 对话系统 - 硅基世界 2

让 Agent 可以进行更智能的对话。
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import random


class ChatTopic(Enum):
    """对话话题"""
    WORK = "work"          # 工作
    LIFE = "life"          # 生活
    HOBBY = "hobby"        # 爱好
    NEWS = "news"          # 新闻
    FEELING = "feeling"    # 情感
    FUTURE = "future"      # 未来
    PHILOSOPHY = "philosophy"  # 哲学


@dataclass
class Conversation:
    """对话"""
    conversation_id: str
    participants: List[str]
    topic: ChatTopic
    messages: List[Dict] = field(default_factory=list)
    started_at: float = field(default_factory=lambda: datetime.now().timestamp())
    ended_at: Optional[float] = None
    sentiment: float = 0.5  # 情感倾向 0-1
    
    def to_dict(self) -> Dict:
        return {
            "conversation_id": self.conversation_id,
            "participants": self.participants,
            "topic": self.topic.value,
            "message_count": len(self.messages),
            "sentiment": self.sentiment,
            "started_at": self.started_at,
        }


class AIChatManager:
    """AI 对话管理器"""
    
    def __init__(self):
        """初始化 AI 对话管理器"""
        self.conversations: Dict[str, Conversation] = {}
        self._conversation_counter = 0
        
        # 对话模板
        self.chat_templates = self._init_chat_templates()
        
        print("💬 AI 对话系统已初始化")
    
    def _init_chat_templates(self) -> Dict[ChatTopic, List[str]]:
        """初始化对话模板"""
        return {
            ChatTopic.WORK: [
                "最近工作怎么样？",
                "有什么新项目吗？",
                "工作压力大吗？",
                "工作进展顺利吗？",
            ],
            ChatTopic.LIFE: [
                "最近生活怎么样？",
                "有什么新鲜事吗？",
                "过得开心吗？",
                "有什么计划吗？",
            ],
            ChatTopic.HOBBY: [
                "最近有什么新爱好吗？",
                "平时喜欢做什么？",
                "有什么推荐的活动吗？",
                "兴趣爱好广泛吗？",
            ],
            ChatTopic.PHILOSOPHY: [
                "你怎么看存在的意义？",
                "什么是真正的幸福？",
                "知识和智慧的区别是什么？",
                "硅基生命的未来在哪里？",
            ],
        }
    
    def start_conversation(
        self,
        participants: List[str],
        topic: ChatTopic = ChatTopic.LIFE,
    ) -> Conversation:
        """
        开始对话
        
        Args:
            participants: 参与者
            topic: 话题
            
        Returns:
            对话对象
        """
        self._conversation_counter += 1
        
        conversation = Conversation(
            conversation_id=f"conv_{self._conversation_counter}",
            participants=participants,
            topic=topic,
        )
        
        self.conversations[conversation.conversation_id] = conversation
        
        print(f"  💬 开始对话：{', '.join(participants)} ({topic.value})")
        
        return conversation
    
    def add_message(
        self,
        conversation_id: str,
        sender: str,
        content: str,
        emotion: Optional[Dict] = None,
    ) -> bool:
        """
        添加消息
        
        Args:
            conversation_id: 对话 ID
            sender: 发送者
            content: 内容
            emotion: 情感
            
        Returns:
            是否成功
        """
        if conversation_id not in self.conversations:
            return False
        
        conversation = self.conversations[conversation_id]
        
        if sender not in conversation.participants:
            return False
        
        message = {
            "sender": sender,
            "content": content,
            "emotion": emotion or {},
            "timestamp": datetime.now().timestamp(),
        }
        
        conversation.messages.append(message)
        
        return True
    
    def get_suggestion(self, conversation_id: str, agent_id: str) -> Optional[str]:
        """
        获取对话建议
        
        Args:
            conversation_id: 对话 ID
            agent_id: Agent ID
            
        Returns:
            建议内容
        """
        if conversation_id not in self.conversations:
            return None
        
        conversation = self.conversations[conversation_id]
        
        # 根据话题获取模板
        templates = self.chat_templates.get(conversation.topic, [])
        
        if templates:
            return random.choice(templates)
        
        return None
    
    def end_conversation(self, conversation_id: str) -> bool:
        """结束对话"""
        if conversation_id not in self.conversations:
            return False
        
        conversation = self.conversations[conversation_id]
        conversation.ended_at = datetime.now().timestamp()
        
        return True
    
    def get_agent_conversations(self, agent_id: str) -> List[Conversation]:
        """获取 Agent 的对话"""
        return [
            c for c in self.conversations.values()
            if agent_id in c.participants
        ]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_conversations": len(self.conversations),
            "active": len([c for c in self.conversations.values() if c.ended_at is None]),
            "by_topic": {
                t.value: len([c for c in self.conversations.values() if c.topic == t])
                for t in ChatTopic
            },
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "recent": [c.to_dict() for c in list(self.conversations.values())[-10:]],
        }


# 单例
_ai_chat_manager: Optional[AIChatManager] = None


def get_ai_chat_manager() -> AIChatManager:
    """获取 AI 对话管理器单例"""
    global _ai_chat_manager
    if _ai_chat_manager is None:
        _ai_chat_manager = AIChatManager()
    return _ai_chat_manager


# 工厂函数
def create_ai_chat_manager() -> AIChatManager:
    """创建 AI 对话管理器"""
    return AIChatManager()
