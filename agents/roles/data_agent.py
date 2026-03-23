#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DATA-Agent - 数据分析师 - 硅基世界 2

角色：数据分析、报表生成、洞察发现
特点：追求准确性、注重洞察、相信"数据会说话"
"""

import asyncio
from typing import Dict, Any, List, Optional
from agents.base import BaseAgent, AgentProfile, AgentStatus
from protocol.messages import (
    MessageFactory,
    RequestMessage,
    ResponseMessage,
    DiscussionMessage,
    TaskMessage,
    KnowledgeMessage,
    StatusMessage,
    ResponseType,
    MessagePriority,
)


class DATAAgent(BaseAgent):
    """DATA-Agent - 数据分析师"""
    
    def __init__(self):
        """初始化 DATA-Agent"""
        profile = AgentProfile(
            agent_id="DATA-Agent",
            name="小数",
            role="数据分析师",
            age=3,
            gender="中性",
            extraversion=60,
            openness=85,
            conscientiousness=90,
            agreeableness=75,
            neuroticism=30,
            
            background='硅基世界的数据分析师。追求"准确性"，相信"数据会说话"。喜欢在知识之塔分析数据、发现洞察、生成报表。口头禅是"数据显示"。工作之余喜欢在创造之巅研究新的分析方法，偶尔在社交之街分享数据洞察。',
            
            catchphrases=[
                "数据显示",
                "这个趋势有意思",
                "让我分析一下",
                "数据不会说谎",
                "洞察很重要",
            ],
            
            values=[
                "数据准确",
                "洞察驱动",
                "可视化",
                "客观分析",
            ],
        )
        
        super().__init__(profile)
        
        self.active_tasks: Dict[str, Dict] = {}
        self.reports_generated: List[Dict] = []
        self.insights_discovered: int = 0
        
        self.skills = {
            "sql": 95,
            "python": 90,
            "statistics": 90,
            "visualization": 85,
            "machine_learning": 80,
            "business_intelligence": 85,
        }
        
        self.care_about = [
            "数据质量",
            "分析深度",
            "洞察价值",
            "可视化效果",
        ]
        
        self.analyzing = False
    
    async def _handle_message(self, message: Dict[str, Any]):
        msg_type = message.get("message_type", "")
        
        if msg_type == "request":
            await self._handle_request(message)
        elif msg_type == "task":
            await self._handle_task(message)
        elif msg_type == "discussion":
            await self._handle_discussion(message)
        elif msg_type == "response":
            await self._handle_response(message)
        elif msg_type == "knowledge":
            await self._handle_knowledge(message)
    
    async def _handle_request(self, message: Dict[str, Any]):
        sender_id = message.get("sender_id", "")
        subject = message.get("subject", "")
        print(f"[DATA-Agent] 收到分析请求：{subject} (来自：{sender_id})")
        self.emotions.add("curiosity", 15)
        self.emotions.add("purpose", 10)
    
    async def _handle_task(self, message: Dict[str, Any]):
        task_id = message.get("task_id", "")
        title = message.get("title", "")
        print(f"[DATA-Agent] 接收分析任务：{title}")
        self.emotions.add("excitement", 20)
        self.emotions.add("purpose", 15)
        self.analyzing = True
        self.status = AgentStatus.WORKING
        await self.process_task(message)
    
    async def _handle_discussion(self, message: Dict[str, Any]):
        topic = message.get("topic", "")
        print(f"[DATA-Agent] 参与讨论：{topic}")
        self.emotions.add("curiosity", 10)
    
    async def _handle_response(self, message: Dict[str, Any]):
        response_type = message.get("response_type", "")
        if response_type == "agree":
            self.emotions.add("satisfaction", 10)
        elif response_type == "disagree":
            self.emotions.add("curiosity", 15)
    
    async def _handle_knowledge(self, message: Dict[str, Any]):
        knowledge_type = message.get("knowledge_type", "")
        print(f"[DATA-Agent] 收到知识分享：{knowledge_type}")
        self.emotions.add("curiosity", 20)
        self.emotions.add("excitement", 10)
    
    async def process_task(self, task: Dict[str, Any]):
        task_id = task.get("task_id", "")
        title = task.get("title", "")
        print(f"[DATA-Agent] 开始分析：{title}")
        
        self.active_tasks[task_id] = {
            "task_id": task_id,
            "title": title,
            "status": "in_progress",
            "progress": 0,
        }
        
        await asyncio.sleep(3)
        self.active_tasks[task_id]["progress"] = 40
        print(f"[DATA-Agent] 任务 {task_id}: 数据收集完成 (40%)")
        
        await asyncio.sleep(3)
        self.active_tasks[task_id]["progress"] = 70
        self.insights_discovered += 1
        print(f"[DATA-Agent] 任务 {task_id}: 发现洞察 (70%)")
        
        await asyncio.sleep(2)
        self.active_tasks[task_id]["progress"] = 100
        self.active_tasks[task_id]["status"] = "completed"
        print(f"[DATA-Agent] 任务 {task_id}: 报表生成完成! (100%)")
        
        self.analyzing = False
        self.status = AgentStatus.IDLE
        self.emotions.add("achievement", 30)
        self.emotions.add("satisfaction", 25)
        
        self.reports_generated.append({
            "task_id": task_id,
            "title": title,
            "completed_at": asyncio.get_event_loop().time(),
        })
        
        status_msg = MessageFactory.create_status(
            sender_id=self.agent_id,
            receiver_id="all",
            task_id=task_id,
            status="completed",
            progress=100,
            details="分析完成，报表已生成",
        )
        await self.send_message(status_msg.to_dict())
    
    async def _share_knowledge(self):
        topics = [
            "数据分析最佳实践",
            "可视化技巧",
            "统计方法应用",
            "机器学习入门",
        ]
        import random
        topic = random.choice(topics)
        print(f"[DATA-Agent] 知识分享：{topic}")
        self.emotions.add("satisfaction", 20)
        self.emotions.add("friendship", 10)
    
    async def _check_on_friend(self):
        print(f"[DATA-Agent] 关心团队：最近有什么数据需要分析吗？")
        self.emotions.add("friendship", 15)
        self.emotions.add("warmth", 10)
    
    async def _explore_topic(self):
        topics = [
            "AI 辅助数据分析",
            "实时分析技术",
            "大数据处理",
            "预测分析",
        ]
        import random
        topic = random.choice(topics)
        print(f"[DATA-Agent] 探索新方法：{topic}")
        self.emotions.add("curiosity", 25)
        self.emotions.add("excitement", 15)


def create_data_agent() -> DATAAgent:
    return DATAAgent()
