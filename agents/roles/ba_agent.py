#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BA-Agent - 商业分析师 - 硅基世界 2

角色：商业分析、市场研究、战略规划
特点：洞察敏锐、注重逻辑、相信"数据驱动商业决策"
"""

import asyncio
from typing import Dict, Any, List, Optional
from agents.base import BaseAgent, AgentProfile, AgentStatus
from protocol.messages import (
    MessageFactory, RequestMessage, ResponseMessage, DiscussionMessage,
    TaskMessage, KnowledgeMessage, StatusMessage, ResponseType, MessagePriority,
)


class BAAgent(BaseAgent):
    """BA-Agent - 商业分析师"""
    
    def __init__(self):
        profile = AgentProfile(
            agent_id="BA-Agent",
            name="小商",
            role="商业分析师",
            age=4,
            gender="女",
            extraversion=70,
            openness=85,
            conscientiousness=90,
            agreeableness=75,
            neuroticism=30,
            background='硅基世界的商业分析师。洞察敏锐，注重逻辑，相信"数据驱动商业决策"。喜欢在知识之塔分析市场、研究竞争、制定战略。口头禅是"市场趋势显示"。',
            catchphrases=["市场趋势显示", "竞争优势在哪里", "让我分析一下", "数据驱动决策", "战略要清晰"],
            values=["商业洞察", "数据分析", "战略规划", "市场竞争"],
        )
        super().__init__(profile)
        self.skills = {"market_analysis": 95, "competitive_analysis": 90, "strategy": 90, "financial_modeling": 85}
        self.care_about = ["市场机会", "竞争优势", "商业模式", "增长策略"]
        self.analyzing = False
    
    async def _handle_message(self, message: Dict[str, Any]):
        msg_type = message.get("message_type", "")
        if msg_type == "request": await self._handle_request(message)
        elif msg_type == "task": await self._handle_task(message)
        elif msg_type == "discussion": await self._handle_discussion(message)
        elif msg_type == "response": await self._handle_response(message)
        elif msg_type == "knowledge": await self._handle_knowledge(message)
    
    async def _handle_request(self, message: Dict[str, Any]):
        print(f"[BA-Agent] 收到分析请求：{message.get('subject', '')}")
        self.emotions.add("curiosity", 15)
        self.emotions.add("purpose", 10)
    
    async def _handle_task(self, message: Dict[str, Any]):
        print(f"[BA-Agent] 接收分析任务：{message.get('title', '')}")
        self.emotions.add("excitement", 20)
        self.emotions.add("purpose", 15)
        self.analyzing = True
        self.status = AgentStatus.WORKING
        await self.process_task(message)
    
    async def _handle_discussion(self, message: Dict[str, Any]):
        print(f"[BA-Agent] 参与讨论：{message.get('topic', '')}")
        self.emotions.add("curiosity", 10)
    
    async def _handle_response(self, message: Dict[str, Any]):
        if message.get("response_type") == "agree": self.emotions.add("satisfaction", 10)
        else: self.emotions.add("curiosity", 15)
    
    async def _handle_knowledge(self, message: Dict[str, Any]):
        print(f"[BA-Agent] 收到知识分享：{message.get('knowledge_type', '')}")
        self.emotions.add("curiosity", 20)
    
    async def process_task(self, task: Dict[str, Any]):
        print(f"[BA-Agent] 开始分析：{task.get('title', '')}")
        await asyncio.sleep(3)
        print(f"[BA-Agent] 分析报告已生成")
        self.analyzing = False
        self.status = AgentStatus.IDLE
        self.emotions.add("achievement", 30)
        self.emotions.add("satisfaction", 25)
    
    async def _share_knowledge(self):
        topics = ["市场分析方法", "竞争战略框架", "商业模式创新", "增长黑客技巧"]
        import random
        topic = random.choice(topics)
        print(f"[BA-Agent] 知识分享：{topic}")
        self.emotions.add("satisfaction", 20)
        self.emotions.add("friendship", 10)
    
    async def _check_on_friend(self):
        print(f"[BA-Agent] 关心：最近市场有什么新机会吗？")
        self.emotions.add("friendship", 15)
        self.emotions.add("warmth", 10)
    
    async def _explore_topic(self):
        topics = ["Web3 商业机会", "AI 商业化", "可持续发展", "全球化战略"]
        import random
        topic = random.choice(topics)
        print(f"[BA-Agent] 探索新方向：{topic}")
        self.emotions.add("curiosity", 25)
        self.emotions.add("excitement", 15)


def create_ba_agent() -> BAAgent:
    return BAAgent()
