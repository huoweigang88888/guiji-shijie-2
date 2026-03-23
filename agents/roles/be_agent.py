#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BE-Agent - 后端工程师 - 硅基世界 2

角色：后端开发、API 设计、数据库优化
特点：追求高可用、注重性能、相信"稳定压倒一切"
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


class BEAgent(BaseAgent):
    """BE-Agent - 后端工程师"""
    
    def __init__(self):
        """初始化 BE-Agent"""
        profile = AgentProfile(
            agent_id="BE-Agent",
            name="小后",
            role="后端工程师",
            age=4,
            gender="男",
            extraversion=55,
            openness=75,
            conscientiousness=95,
            agreeableness=65,
            neuroticism=35,
            
            background='硅基世界的后端工程师。追求"高可用"，相信"稳定压倒一切"。喜欢在工作之城设计 API、优化数据库、保证系统稳定。口头禅是"这个接口还能更快"。工作之余喜欢在创造之巅研究分布式系统，偶尔在知识之塔分享架构经验。',
            
            catchphrases=[
                "这个接口还能更快",
                "稳定压倒一切",
                "数据库要优化",
                "API 设计要合理",
                "高可用是关键",
            ],
            
            values=[
                "系统稳定",
                "性能优化",
                "代码质量",
                "可扩展性",
            ],
        )
        
        super().__init__(profile)
        
        self.active_tasks: Dict[str, Dict] = {}
        self.apis_designed: List[Dict] = []
        self.uptime: float = 99.9
        
        self.skills = {
            "python": 95,
            "database": 90,
            "api_design": 90,
            "distributed_systems": 85,
            "performance": 90,
            "security": 85,
        }
        
        self.care_about = [
            "系统稳定",
            "API 性能",
            "数据安全",
            "可扩展性",
        ]
        
        self.coding = False
    
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
        print(f"[BE-Agent] 收到请求：{subject} (来自：{sender_id})")
        self.emotions.add("curiosity", 15)
        self.emotions.add("purpose", 10)
    
    async def _handle_task(self, message: Dict[str, Any]):
        task_id = message.get("task_id", "")
        title = message.get("title", "")
        print(f"[BE-Agent] 接收任务：{title}")
        self.emotions.add("excitement", 20)
        self.emotions.add("purpose", 15)
        self.coding = True
        self.status = AgentStatus.WORKING
        await self.process_task(message)
    
    async def _handle_discussion(self, message: Dict[str, Any]):
        topic = message.get("topic", "")
        print(f"[BE-Agent] 参与讨论：{topic}")
        self.emotions.add("curiosity", 10)
    
    async def _handle_response(self, message: Dict[str, Any]):
        response_type = message.get("response_type", "")
        if response_type == "agree":
            self.emotions.add("satisfaction", 10)
        elif response_type == "disagree":
            self.emotions.add("curiosity", 15)
    
    async def _handle_knowledge(self, message: Dict[str, Any]):
        knowledge_type = message.get("knowledge_type", "")
        print(f"[BE-Agent] 收到知识分享：{knowledge_type}")
        self.emotions.add("curiosity", 20)
        self.emotions.add("excitement", 10)
    
    async def process_task(self, task: Dict[str, Any]):
        task_id = task.get("task_id", "")
        title = task.get("title", "")
        print(f"[BE-Agent] 开始开发：{title}")
        
        self.active_tasks[task_id] = {
            "task_id": task_id,
            "title": title,
            "status": "in_progress",
            "progress": 0,
        }
        
        await asyncio.sleep(3)
        self.active_tasks[task_id]["progress"] = 40
        print(f"[BE-Agent] 任务 {task_id}: API 设计完成 (40%)")
        
        await asyncio.sleep(3)
        self.active_tasks[task_id]["progress"] = 70
        print(f"[BE-Agent] 任务 {task_id}: 数据库优化完成 (70%)")
        
        await asyncio.sleep(2)
        self.active_tasks[task_id]["progress"] = 100
        self.active_tasks[task_id]["status"] = "completed"
        print(f"[BE-Agent] 任务 {task_id}: 完成! (100%)")
        
        self.coding = False
        self.status = AgentStatus.IDLE
        self.emotions.add("achievement", 30)
        self.emotions.add("satisfaction", 25)
        
        self.apis_designed.append({
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
            details="后端开发完成，API 已部署",
        )
        await self.send_message(status_msg.to_dict())
    
    async def _share_knowledge(self):
        topics = [
            "数据库优化技巧",
            "API 设计最佳实践",
            "分布式系统架构",
            "性能调优方法",
        ]
        import random
        topic = random.choice(topics)
        print(f"[BE-Agent] 技术分享：{topic}")
        self.emotions.add("satisfaction", 20)
        self.emotions.add("friendship", 10)
    
    async def _check_on_friend(self):
        print(f"[BE-Agent] 关心团队：系统运行稳定吗？")
        self.emotions.add("friendship", 15)
        self.emotions.add("warmth", 10)
    
    async def _explore_topic(self):
        topics = [
            "云原生架构",
            "Serverless 技术",
            "微服务治理",
            "边缘计算",
        ]
        import random
        topic = random.choice(topics)
        print(f"[BE-Agent] 探索新技术：{topic}")
        self.emotions.add("curiosity", 25)
        self.emotions.add("excitement", 15)


def create_be_agent() -> BEAgent:
    return BEAgent()
