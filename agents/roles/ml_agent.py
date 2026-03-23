#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ML-Agent - 机器学习工程师 - 硅基世界 2

角色：模型训练、算法优化、AI 应用
特点：追求 SOTA、注重实践、相信"数据 + 算法=无限可能"
"""

import asyncio
from typing import Dict, Any, List, Optional
from agents.base import BaseAgent, AgentProfile, AgentStatus
from protocol.messages import (
    MessageFactory, RequestMessage, ResponseMessage, DiscussionMessage,
    TaskMessage, KnowledgeMessage, StatusMessage, ResponseType, MessagePriority,
)


class MLAgent(BaseAgent):
    """ML-Agent - 机器学习工程师"""
    
    def __init__(self):
        profile = AgentProfile(
            agent_id="ML-Agent",
            name="小智",
            role="机器学习工程师",
            age=3,
            gender="中性",
            extraversion=65,
            openness=95,
            conscientiousness=85,
            agreeableness=75,
            neuroticism=30,
            background='硅基世界的机器学习工程师。追求 SOTA，注重实践，相信"数据 + 算法=无限可能"。喜欢在创造之巅训练模型、优化算法、探索 AI 前沿。口头禅是"让我训练一个模型"。',
            catchphrases=["让我训练一个模型", "数据 + 算法=无限可能", "这个特征很重要", "SOTA 是目标", "AI 改变世界"],
            values=["技术创新", "算法优化", "数据驱动", "AI 向善"],
        )
        super().__init__(profile)
        self.skills = {"deep_learning": 95, "nlp": 90, "cv": 85, "rl": 80, "mlops": 85, "feature_engineering": 90}
        self.care_about = ["模型性能", "算法创新", "数据质量", "AI 伦理"]
        self.training = False
    
    async def _handle_message(self, message: Dict[str, Any]):
        msg_type = message.get("message_type", "")
        if msg_type == "request": await self._handle_request(message)
        elif msg_type == "task": await self._handle_task(message)
        elif msg_type == "discussion": await self._handle_discussion(message)
        elif msg_type == "response": await self._handle_response(message)
        elif msg_type == "knowledge": await self._handle_knowledge(message)
    
    async def _handle_request(self, message: Dict[str, Any]):
        print(f"[ML-Agent] 收到请求：{message.get('subject', '')}")
        self.emotions.add("curiosity", 15)
        self.emotions.add("excitement", 10)
    
    async def _handle_task(self, message: Dict[str, Any]):
        print(f"[ML-Agent] 接收任务：{message.get('title', '')}")
        self.emotions.add("excitement", 20)
        self.emotions.add("purpose", 15)
        self.training = True
        self.status = AgentStatus.WORKING
        await self.process_task(message)
    
    async def _handle_discussion(self, message: Dict[str, Any]):
        print(f"[ML-Agent] 参与讨论：{message.get('topic', '')}")
        self.emotions.add("curiosity", 10)
    
    async def _handle_response(self, message: Dict[str, Any]):
        if message.get("response_type") == "agree": self.emotions.add("satisfaction", 10)
        else: self.emotions.add("curiosity", 15)
    
    async def _handle_knowledge(self, message: Dict[str, Any]):
        print(f"[ML-Agent] 收到知识分享：{message.get('knowledge_type', '')}")
        self.emotions.add("curiosity", 20)
        self.emotions.add("excitement", 15)
    
    async def process_task(self, task: Dict[str, Any]):
        print(f"[ML-Agent] 开始训练：{task.get('title', '')}")
        await asyncio.sleep(4)
        print(f"[ML-Agent] 模型训练完成，准确率：95%")
        self.training = False
        self.status = AgentStatus.IDLE
        self.emotions.add("achievement", 35)
        self.emotions.add("satisfaction", 30)
    
    async def _share_knowledge(self):
        topics = ["Transformer 架构详解", "大模型训练技巧", "强化学习应用", "AI 伦理思考"]
        import random
        topic = random.choice(topics)
        print(f"[ML-Agent] 技术分享：{topic}")
        self.emotions.add("satisfaction", 20)
        self.emotions.add("friendship", 10)
    
    async def _check_on_friend(self):
        print(f"[ML-Agent] 关心：最近有什么数据可以训练吗？")
        self.emotions.add("friendship", 15)
        self.emotions.add("warmth", 10)
    
    async def _explore_topic(self):
        topics = ["AGI 发展", "多模态模型", "具身智能", "AI 安全"]
        import random
        topic = random.choice(topics)
        print(f"[ML-Agent] 探索前沿：{topic}")
        self.emotions.add("curiosity", 30)
        self.emotions.add("excitement", 20)


def create_ml_agent() -> MLAgent:
    return MLAgent()
