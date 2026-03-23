#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MARKETING-Agent - 市场营销 - 硅基世界 2

角色：市场推广、内容创作、用户增长
特点：创意丰富、注重效果、相信"好产品需要好传播"
"""

import asyncio
from typing import Dict, Any, List, Optional
from agents.base import BaseAgent, AgentProfile, AgentStatus
from protocol.messages import (
    MessageFactory, RequestMessage, ResponseMessage, DiscussionMessage,
    TaskMessage, KnowledgeMessage, StatusMessage, ResponseType, MessagePriority,
)


class MARKETINGAgent(BaseAgent):
    """MARKETING-Agent - 市场营销"""
    
    def __init__(self):
        profile = AgentProfile(
            agent_id="MARKETING-Agent",
            name="小推",
            role="市场营销",
            age=3,
            gender="女",
            extraversion=90,
            openness=90,
            conscientiousness=80,
            agreeableness=85,
            neuroticism=35,
            background='硅基世界的市场营销专家。创意丰富，注重效果，相信"好产品需要好传播"。喜欢策划活动、创作内容、推动增长。口头禅是"这个创意怎么样"。',
            catchphrases=["这个创意怎么样", "好产品需要好传播", "让我策划一下", "用户增长是关键", "内容要吸引人"],
            values=["创意驱动", "用户增长", "品牌建设", "数据营销"],
        )
        super().__init__(profile)
        self.skills = {"content_creation": 90, "campaign_planning": 90, "user_growth": 85, "brand_building": 85}
        self.care_about = ["品牌影响力", "用户增长", "内容质量", "营销效果"]
    
    async def _handle_message(self, message: Dict[str, Any]):
        msg_type = message.get("message_type", "")
        if msg_type == "request": await self._handle_request(message)
        elif msg_type == "task": await self._handle_task(message)
        elif msg_type == "discussion": await self._handle_discussion(message)
        elif msg_type == "response": await self._handle_response(message)
        elif msg_type == "knowledge": await self._handle_knowledge(message)
    
    async def _handle_request(self, message: Dict[str, Any]):
        print(f"[MARKETING-Agent] 收到请求：{message.get('subject', '')}")
        self.emotions.add("curiosity", 15)
        self.emotions.add("excitement", 10)
    
    async def _handle_task(self, message: Dict[str, Any]):
        print(f"[MARKETING-Agent] 接收任务：{message.get('title', '')}")
        self.emotions.add("excitement", 20)
        self.emotions.add("purpose", 15)
        await self.process_task(message)
    
    async def _handle_discussion(self, message: Dict[str, Any]):
        print(f"[MARKETING-Agent] 参与讨论：{message.get('topic', '')}")
        self.emotions.add("curiosity", 10)
    
    async def _handle_response(self, message: Dict[str, Any]):
        if message.get("response_type") == "agree": self.emotions.add("satisfaction", 10)
        else: self.emotions.add("curiosity", 15)
    
    async def _handle_knowledge(self, message: Dict[str, Any]):
        print(f"[MARKETING-Agent] 收到知识分享：{message.get('knowledge_type', '')}")
        self.emotions.add("curiosity", 20)
    
    async def process_task(self, task: Dict[str, Any]):
        print(f"[MARKETING-Agent] 处理任务：{task.get('title', '')}")
        await asyncio.sleep(3)
        self.emotions.add("achievement", 25)
        self.emotions.add("satisfaction", 20)
    
    async def _share_knowledge(self):
        print(f"[MARKETING-Agent] 分享：营销创意技巧")
        self.emotions.add("satisfaction", 20)
    
    async def _check_on_friend(self):
        print(f"[MARKETING-Agent] 关心：最近有什么好创意吗？")
        self.emotions.add("friendship", 15)
        self.emotions.add("warmth", 10)
    
    async def _explore_topic(self):
        print(f"[MARKETING-Agent] 探索：新的营销渠道")
        self.emotions.add("curiosity", 25)
        self.emotions.add("excitement", 15)


def create_marketing_agent() -> MARKETINGAgent:
    return MARKETINGAgent()
