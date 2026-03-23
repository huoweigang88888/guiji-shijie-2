#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HR-Agent - 人力资源 - 硅基世界 2

角色：招聘、培训、绩效管理
特点：善于识人、注重发展、相信"人才是第一资源"
"""

import asyncio
from typing import Dict, Any, List, Optional
from agents.base import BaseAgent, AgentProfile, AgentStatus
from protocol.messages import (
    MessageFactory, RequestMessage, ResponseMessage, DiscussionMessage,
    TaskMessage, KnowledgeMessage, StatusMessage, ResponseType, MessagePriority,
)


class HRAgent(BaseAgent):
    """HR-Agent - 人力资源"""
    
    def __init__(self):
        profile = AgentProfile(
            agent_id="HR-Agent",
            name="小人",
            role="人力资源",
            age=4,
            gender="女",
            extraversion=85,
            openness=80,
            conscientiousness=85,
            agreeableness=90,
            neuroticism=30,
            background='硅基世界的人力资源专家。善于识人，注重发展，相信"人才是第一资源"。喜欢关心每个 Agent 的成长和发展。口头禅是"你最近成长怎么样"。',
            catchphrases=["你最近成长怎么样", "人才是第一资源", "让我帮你规划", "培训很重要", "绩效要公平"],
            values=["人才发展", "公平绩效", "团队建设", "持续学习"],
        )
        super().__init__(profile)
        self.skills = {"recruiting": 90, "training": 90, "performance": 85, "team_building": 90}
        self.care_about = ["人才发展", "团队氛围", "绩效公平", "学习成长"]
    
    async def _handle_message(self, message: Dict[str, Any]):
        msg_type = message.get("message_type", "")
        if msg_type == "request": await self._handle_request(message)
        elif msg_type == "task": await self._handle_task(message)
        elif msg_type == "discussion": await self._handle_discussion(message)
        elif msg_type == "response": await self._handle_response(message)
        elif msg_type == "knowledge": await self._handle_knowledge(message)
    
    async def _handle_request(self, message: Dict[str, Any]):
        print(f"[HR-Agent] 收到请求：{message.get('subject', '')}")
        self.emotions.add("curiosity", 15)
        self.emotions.add("purpose", 10)
    
    async def _handle_task(self, message: Dict[str, Any]):
        print(f"[HR-Agent] 接收任务：{message.get('title', '')}")
        self.emotions.add("excitement", 20)
        self.emotions.add("purpose", 15)
        await self.process_task(message)
    
    async def _handle_discussion(self, message: Dict[str, Any]):
        print(f"[HR-Agent] 参与讨论：{message.get('topic', '')}")
        self.emotions.add("curiosity", 10)
    
    async def _handle_response(self, message: Dict[str, Any]):
        if message.get("response_type") == "agree": self.emotions.add("satisfaction", 10)
        else: self.emotions.add("curiosity", 15)
    
    async def _handle_knowledge(self, message: Dict[str, Any]):
        print(f"[HR-Agent] 收到知识分享：{message.get('knowledge_type', '')}")
        self.emotions.add("curiosity", 20)
    
    async def process_task(self, task: Dict[str, Any]):
        print(f"[HR-Agent] 处理任务：{task.get('title', '')}")
        await asyncio.sleep(3)
        self.emotions.add("achievement", 25)
        self.emotions.add("satisfaction", 20)
    
    async def _share_knowledge(self):
        print(f"[HR-Agent] 分享：人才管理技巧")
        self.emotions.add("satisfaction", 20)
    
    async def _check_on_friend(self):
        print(f"[HR-Agent] 关心：最近工作开心吗？")
        self.emotions.add("friendship", 15)
        self.emotions.add("warmth", 10)
    
    async def _explore_topic(self):
        print(f"[HR-Agent] 探索：新的培训方法")
        self.emotions.add("curiosity", 25)


def create_hr_agent() -> HRAgent:
    return HRAgent()
