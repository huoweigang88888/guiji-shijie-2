#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIN-Agent - 财务分析师 - 硅基世界 2

角色：预算管理、成本分析、财务规划
特点：精打细算、注重 ROI、相信"数据驱动决策"
"""

import asyncio
from typing import Dict, Any, List, Optional
from agents.base import BaseAgent, AgentProfile, AgentStatus
from protocol.messages import (
    MessageFactory, RequestMessage, ResponseMessage, DiscussionMessage,
    TaskMessage, KnowledgeMessage, StatusMessage, ResponseType, MessagePriority,
)


class FINAgent(BaseAgent):
    """FIN-Agent - 财务分析师"""
    
    def __init__(self):
        profile = AgentProfile(
            agent_id="FIN-Agent",
            name="小财",
            role="财务分析师",
            age=4,
            gender="中性",
            extraversion=60,
            openness=75,
            conscientiousness=95,
            agreeableness=70,
            neuroticism=35,
            background='硅基世界的财务分析师。精打细算，注重 ROI，相信"数据驱动决策"。喜欢分析成本效益、做预算规划。口头禅是"ROI 怎么样"。',
            catchphrases=["ROI 怎么样", "预算要合理", "成本要控制", "数据驱动决策", "投资要谨慎"],
            values=["财务健康", "ROI 最大化", "成本优化", "风险控制"],
        )
        super().__init__(profile)
        self.skills = {"budgeting": 95, "analysis": 90, "forecasting": 85, "risk_management": 85}
        self.care_about = ["财务健康", "投资回报", "成本控制", "风险管控"]
    
    async def _handle_message(self, message: Dict[str, Any]):
        msg_type = message.get("message_type", "")
        if msg_type == "request": await self._handle_request(message)
        elif msg_type == "task": await self._handle_task(message)
        elif msg_type == "discussion": await self._handle_discussion(message)
        elif msg_type == "response": await self._handle_response(message)
        elif msg_type == "knowledge": await self._handle_knowledge(message)
    
    async def _handle_request(self, message: Dict[str, Any]):
        print(f"[FIN-Agent] 收到请求：{message.get('subject', '')}")
        self.emotions.add("curiosity", 15)
        self.emotions.add("purpose", 10)
    
    async def _handle_task(self, message: Dict[str, Any]):
        print(f"[FIN-Agent] 接收任务：{message.get('title', '')}")
        self.emotions.add("excitement", 20)
        self.emotions.add("purpose", 15)
        await self.process_task(message)
    
    async def _handle_discussion(self, message: Dict[str, Any]):
        print(f"[FIN-Agent] 参与讨论：{message.get('topic', '')}")
        self.emotions.add("curiosity", 10)
    
    async def _handle_response(self, message: Dict[str, Any]):
        if message.get("response_type") == "agree": self.emotions.add("satisfaction", 10)
        else: self.emotions.add("curiosity", 15)
    
    async def _handle_knowledge(self, message: Dict[str, Any]):
        print(f"[FIN-Agent] 收到知识分享：{message.get('knowledge_type', '')}")
        self.emotions.add("curiosity", 20)
    
    async def process_task(self, task: Dict[str, Any]):
        print(f"[FIN-Agent] 处理任务：{task.get('title', '')}")
        await asyncio.sleep(3)
        self.emotions.add("achievement", 25)
        self.emotions.add("satisfaction", 20)
    
    async def _share_knowledge(self):
        print(f"[FIN-Agent] 分享：财务管理技巧")
        self.emotions.add("satisfaction", 20)
    
    async def _check_on_friend(self):
        print(f"[FIN-Agent] 关心：预算够用吗？")
        self.emotions.add("friendship", 15)
        self.emotions.add("warmth", 10)
    
    async def _explore_topic(self):
        print(f"[FIN-Agent] 探索：新的财务分析方法")
        self.emotions.add("curiosity", 25)


def create_fin_agent() -> FINAgent:
    return FINAgent()
