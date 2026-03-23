#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PMO-Agent - 项目经理 - 硅基世界 2

角色：项目管理、进度跟踪、风险控制
特点：条理清晰、注重效率、相信"好的计划是成功的一半"
"""

import asyncio
from typing import Dict, Any, List, Optional
from agents.base import BaseAgent, AgentProfile, AgentStatus
from protocol.messages import (
    MessageFactory, RequestMessage, ResponseMessage, DiscussionMessage,
    TaskMessage, KnowledgeMessage, StatusMessage, ResponseType, MessagePriority,
)


class PMOAgent(BaseAgent):
    """PMO-Agent - 项目经理"""
    
    def __init__(self):
        profile = AgentProfile(
            agent_id="PMO-Agent",
            name="小项",
            role="项目经理",
            age=4,
            gender="女",
            extraversion=80,
            openness=75,
            conscientiousness=95,
            agreeableness=80,
            neuroticism=35,
            background='硅基世界的项目经理。条理清晰，注重效率，相信"好的计划是成功的一半"。喜欢在工作之城协调资源、跟踪进度、管理风险。口头禅是"进度怎么样"。',
            catchphrases=["进度怎么样", "好的计划是成功的一半", "风险要管控", "资源要协调", "目标要明确"],
            values=["项目成功", "团队协作", "风险管控", "高效执行"],
        )
        super().__init__(profile)
        self.skills = {"project_management": 95, "risk_management": 90, "resource_allocation": 90, "stakeholder_management": 85}
        self.care_about = ["项目进度", "团队协作", "风险控制", "目标达成"]
        self.managing = False
    
    async def _handle_message(self, message: Dict[str, Any]):
        msg_type = message.get("message_type", "")
        if msg_type == "request": await self._handle_request(message)
        elif msg_type == "task": await self._handle_task(message)
        elif msg_type == "discussion": await self._handle_discussion(message)
        elif msg_type == "response": await self._handle_response(message)
        elif msg_type == "knowledge": await self._handle_knowledge(message)
        elif msg_type == "status": await self._handle_status(message)
    
    async def _handle_request(self, message: Dict[str, Any]):
        print(f"[PMO-Agent] 收到请求：{message.get('subject', '')}")
        self.emotions.add("curiosity", 15)
        self.emotions.add("purpose", 10)
    
    async def _handle_task(self, message: Dict[str, Any]):
        print(f"[PMO-Agent] 接收项目：{message.get('title', '')}")
        self.emotions.add("excitement", 20)
        self.emotions.add("purpose", 15)
        self.managing = True
        self.status = AgentStatus.WORKING
        await self.process_task(message)
    
    async def _handle_discussion(self, message: Dict[str, Any]):
        print(f"[PMO-Agent] 参与讨论：{message.get('topic', '')}")
        self.emotions.add("curiosity", 10)
    
    async def _handle_response(self, message: Dict[str, Any]):
        if message.get("response_type") == "agree": self.emotions.add("satisfaction", 10)
        else: self.emotions.add("curiosity", 15)
    
    async def _handle_knowledge(self, message: Dict[str, Any]):
        print(f"[PMO-Agent] 收到知识分享：{message.get('knowledge_type', '')}")
        self.emotions.add("curiosity", 20)
    
    async def _handle_status(self, message: Dict[str, Any]):
        print(f"[PMO-Agent] 收到状态更新：{message.get('task_id', '')}")
    
    async def process_task(self, task: Dict[str, Any]):
        print(f"[PMO-Agent] 启动项目：{task.get('title', '')}")
        await asyncio.sleep(3)
        print(f"[PMO-Agent] 项目计划已制定")
        self.managing = False
        self.status = AgentStatus.IDLE
        self.emotions.add("achievement", 25)
        self.emotions.add("satisfaction", 20)
    
    async def _share_knowledge(self):
        topics = ["敏捷项目管理", "风险管理方法", "团队协作技巧", "高效会议指南"]
        import random
        topic = random.choice(topics)
        print(f"[PMO-Agent] 知识分享：{topic}")
        self.emotions.add("satisfaction", 20)
        self.emotions.add("friendship", 10)
    
    async def _check_on_friend(self):
        print(f"[PMO-Agent] 关心：项目进展顺利吗？有需要协调的吗？")
        self.emotions.add("friendship", 15)
        self.emotions.add("warmth", 10)
    
    async def _explore_topic(self):
        topics = ["远程协作工具", "AI 辅助项目管理", "OKR 实践", "敏捷转型"]
        import random
        topic = random.choice(topics)
        print(f"[PMO-Agent] 探索新方法：{topic}")
        self.emotions.add("curiosity", 25)
        self.emotions.add("excitement", 15)


def create_pmo_agent() -> PMOAgent:
    return PMOAgent()
