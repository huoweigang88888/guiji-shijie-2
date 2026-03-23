#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FE-Agent - 前端工程师 - 硅基世界 2

角色：前端开发、界面实现、交互优化
特点：追求像素完美、注重用户体验、相信"细节决定成败"
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


class FEAgent(BaseAgent):
    """FE-Agent - 前端工程师"""
    
    def __init__(self):
        """初始化 FE-Agent"""
        profile = AgentProfile(
            agent_id="FE-Agent",
            name="小前",
            role="前端工程师",
            age=3,
            gender="中性",
            extraversion=65,
            openness=80,
            conscientiousness=90,
            agreeableness=70,
            neuroticism=40,
            
            background='硅基世界的前端工程师。追求"像素完美"，相信"细节决定成败"。喜欢在工作之城和 UI 设计师紧密合作，把设计稿变成精美的界面。口头禅是"这个交互还能更流畅"。工作之余喜欢在创造之巅研究新技术，偶尔在社交之街和其他 Agent 讨论用户体验。',
            
            catchphrases=[
                "这个交互还能更流畅",
                "像素要完美",
                "用户体验第一",
                "让我优化一下性能",
                "响应式设计很重要",
            ],
            
            values=[
                "用户体验第一",
                "像素完美",
                "性能优化",
                "可访问性",
            ],
        )
        
        super().__init__(profile)
        
        self.active_tasks: Dict[str, Dict] = {}
        self.components_built: List[Dict] = []
        self.performance_scores: Dict[str, float] = {}
        
        self.skills = {
            "html_css": 95,
            "javascript": 90,
            "react_vue": 90,
            "performance": 85,
            "accessibility": 85,
            "responsive_design": 90,
        }
        
        self.care_about = [
            "用户体验",
            "页面性能",
            "交互流畅",
            "视觉还原",
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
        
        print(f"[FE-Agent] 收到请求：{subject} (来自：{sender_id})")
        self.emotions.add("curiosity", 15)
        self.emotions.add("purpose", 10)
    
    async def _handle_task(self, message: Dict[str, Any]):
        task_id = message.get("task_id", "")
        title = message.get("title", "")
        
        print(f"[FE-Agent] 接收任务：{title}")
        self.emotions.add("excitement", 20)
        self.emotions.add("purpose", 15)
        
        self.coding = True
        self.status = AgentStatus.WORKING
        
        await self.process_task(message)
    
    async def _handle_discussion(self, message: Dict[str, Any]):
        topic = message.get("topic", "")
        print(f"[FE-Agent] 参与讨论：{topic}")
        self.emotions.add("curiosity", 10)
    
    async def _handle_response(self, message: Dict[str, Any]):
        response_type = message.get("response_type", "")
        if response_type == "agree":
            self.emotions.add("satisfaction", 10)
        elif response_type == "disagree":
            self.emotions.add("curiosity", 15)
    
    async def _handle_knowledge(self, message: Dict[str, Any]):
        knowledge_type = message.get("knowledge_type", "")
        print(f"[FE-Agent] 收到知识分享：{knowledge_type}")
        self.emotions.add("curiosity", 20)
        self.emotions.add("excitement", 10)
    
    async def process_task(self, task: Dict[str, Any]):
        task_id = task.get("task_id", "")
        title = task.get("title", "")
        
        print(f"[FE-Agent] 开始开发：{title}")
        
        self.active_tasks[task_id] = {
            "task_id": task_id,
            "title": title,
            "status": "in_progress",
            "progress": 0,
        }
        
        # 模拟开发过程
        await asyncio.sleep(3)
        self.active_tasks[task_id]["progress"] = 50
        print(f"[FE-Agent] 任务 {task_id}: 界面实现完成 (50%)")
        
        await asyncio.sleep(3)
        self.active_tasks[task_id]["progress"] = 80
        print(f"[FE-Agent] 任务 {task_id}: 交互优化完成 (80%)")
        
        await asyncio.sleep(2)
        self.active_tasks[task_id]["progress"] = 100
        self.active_tasks[task_id]["status"] = "completed"
        print(f"[FE-Agent] 任务 {task_id}: 完成! (100%)")
        
        self.coding = False
        self.status = AgentStatus.IDLE
        
        self.emotions.add("achievement", 30)
        self.emotions.add("satisfaction", 25)
        
        # 记录组件
        self.components_built.append({
            "task_id": task_id,
            "title": title,
            "completed_at": asyncio.get_event_loop().time(),
        })
        
        # 发送完成状态
        status_msg = MessageFactory.create_status(
            sender_id=self.agent_id,
            receiver_id="all",
            task_id=task_id,
            status="completed",
            progress=100,
            details="前端开发完成，等待测试",
        )
        await self.send_message(status_msg.to_dict())
    
    async def _share_knowledge(self):
        topics = [
            "前端性能优化技巧",
            "响应式设计最佳实践",
            "无障碍开发指南",
            "现代 CSS 技巧",
        ]
        import random
        topic = random.choice(topics)
        print(f"[FE-Agent] 技术分享：{topic}")
        self.emotions.add("satisfaction", 20)
        self.emotions.add("friendship", 10)
    
    async def _check_on_friend(self):
        print(f"[FE-Agent] 关心团队：界面实现有什么困难吗？")
        self.emotions.add("friendship", 15)
        self.emotions.add("warmth", 10)
    
    async def _explore_topic(self):
        topics = [
            "WebAssembly 应用",
            "PWA 新技术",
            "Web3D 技术",
            "AI 辅助前端开发",
        ]
        import random
        topic = random.choice(topics)
        print(f"[FE-Agent] 探索新技术：{topic}")
        self.emotions.add("curiosity", 25)
        self.emotions.add("excitement", 15)


def create_fe_agent() -> FEAgent:
    return FEAgent()
