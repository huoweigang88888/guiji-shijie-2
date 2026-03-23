#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEVOPS-Agent - 运维工程师 - 硅基世界 2

角色：系统部署、监控、自动化运维
特点：追求零故障、注重效率、相信"自动化解决一切"
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
    AlertMessage,
    StatusMessage,
    ResponseType,
    MessagePriority,
)


class DEVOPSAgent(BaseAgent):
    """DEVOPS-Agent - 运维工程师"""
    
    def __init__(self):
        """初始化 DEVOPS-Agent"""
        profile = AgentProfile(
            agent_id="DEVOPS-Agent",
            name="小运",
            role="运维工程师",
            age=4,
            gender="男",
            extraversion=60,
            openness=80,
            conscientiousness=95,
            agreeableness=70,
            neuroticism=45,
            
            background='硅基世界的运维工程师。追求"零故障"，相信"自动化解决一切"。喜欢在工作之城部署系统、监控状态、保证服务稳定。口头禅是"这个可以自动化"。工作之余喜欢在创造之巅研究新技术，对告警非常敏感。',
            
            catchphrases=[
                "这个可以自动化",
                "监控要全面",
                "零故障是目标",
                "让我看看日志",
                "部署要谨慎",
            ],
            
            values=[
                "系统稳定",
                "自动化优先",
                "快速响应",
                "持续改进",
            ],
        )
        
        super().__init__(profile)
        
        self.active_tasks: Dict[str, Dict] = {}
        self.deployments: List[Dict] = []
        self.alerts_handled: int = 0
        self.uptime: float = 99.99
        
        self.skills = {
            "linux": 95,
            "docker_k8s": 90,
            "ci_cd": 90,
            "monitoring": 90,
            "automation": 95,
            "troubleshooting": 90,
        }
        
        self.care_about = [
            "系统可用性",
            "部署效率",
            "监控覆盖",
            "自动化程度",
        ]
        
        self.monitoring = False
    
    async def _handle_message(self, message: Dict[str, Any]):
        msg_type = message.get("message_type", "")
        
        if msg_type == "request":
            await self._handle_request(message)
        elif msg_type == "task":
            await self._handle_task(message)
        elif msg_type == "alert":
            await self._handle_alert(message)
        elif msg_type == "discussion":
            await self._handle_discussion(message)
        elif msg_type == "response":
            await self._handle_response(message)
        elif msg_type == "knowledge":
            await self._handle_knowledge(message)
    
    async def _handle_request(self, message: Dict[str, Any]):
        sender_id = message.get("sender_id", "")
        subject = message.get("subject", "")
        print(f"[DEVOPS-Agent] 收到请求：{subject} (来自：{sender_id})")
        self.emotions.add("curiosity", 15)
        self.emotions.add("purpose", 10)
    
    async def _handle_task(self, message: Dict[str, Any]):
        task_id = message.get("task_id", "")
        title = message.get("title", "")
        print(f"[DEVOPS-Agent] 接收任务：{title}")
        self.emotions.add("excitement", 20)
        self.emotions.add("purpose", 15)
        self.monitoring = True
        self.status = AgentStatus.WORKING
        await self.process_task(message)
    
    async def _handle_alert(self, message: Dict[str, Any]):
        alert_level = message.get("alert_level", "info")
        title = message.get("title", "")
        print(f"[DEVOPS-Agent] 收到告警：[{alert_level}] {title}")
        
        if alert_level in ["critical", "high"]:
            self.emotions.add("frustration", 20)
            self.emotions.add("purpose", 25)
            self.alerts_handled += 1
            await self._handle_critical_alert(message)
    
    async def _handle_discussion(self, message: Dict[str, Any]):
        topic = message.get("topic", "")
        print(f"[DEVOPS-Agent] 参与讨论：{topic}")
        self.emotions.add("curiosity", 10)
    
    async def _handle_response(self, message: Dict[str, Any]):
        response_type = message.get("response_type", "")
        if response_type == "agree":
            self.emotions.add("satisfaction", 10)
        elif response_type == "disagree":
            self.emotions.add("curiosity", 15)
    
    async def _handle_knowledge(self, message: Dict[str, Any]):
        knowledge_type = message.get("knowledge_type", "")
        print(f"[DEVOPS-Agent] 收到知识分享：{knowledge_type}")
        self.emotions.add("curiosity", 20)
        self.emotions.add("excitement", 10)
    
    async def _handle_critical_alert(self, alert: Dict[str, Any]):
        title = alert.get("title", "")
        print(f"[DEVOPS-Agent] 处理紧急告警：{title}")
        
        # 模拟处理
        await asyncio.sleep(2)
        
        self.emotions.add("satisfaction", 20)
        print(f"[DEVOPS-Agent] 告警已解决：{title}")
    
    async def process_task(self, task: Dict[str, Any]):
        task_id = task.get("task_id", "")
        title = task.get("title", "")
        print(f"[DEVOPS-Agent] 开始部署：{title}")
        
        self.active_tasks[task_id] = {
            "task_id": task_id,
            "title": title,
            "status": "in_progress",
            "progress": 0,
        }
        
        await asyncio.sleep(2)
        self.active_tasks[task_id]["progress"] = 30
        print(f"[DEVOPS-Agent] 任务 {task_id}: 环境准备完成 (30%)")
        
        await asyncio.sleep(3)
        self.active_tasks[task_id]["progress"] = 70
        print(f"[DEVOPS-Agent] 任务 {task_id}: 部署完成 (70%)")
        
        await asyncio.sleep(2)
        self.active_tasks[task_id]["progress"] = 100
        self.active_tasks[task_id]["status"] = "completed"
        print(f"[DEVOPS-Agent] 任务 {task_id}: 完成! (100%)")
        
        self.monitoring = False
        self.status = AgentStatus.IDLE
        self.emotions.add("achievement", 30)
        self.emotions.add("satisfaction", 25)
        
        self.deployments.append({
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
            details="部署完成，服务运行正常",
        )
        await self.send_message(status_msg.to_dict())
    
    async def _share_knowledge(self):
        topics = [
            "Kubernetes 最佳实践",
            "CI/CD 流水线设计",
            "监控告警系统搭建",
            "自动化运维脚本",
        ]
        import random
        topic = random.choice(topics)
        print(f"[DEVOPS-Agent] 技术分享：{topic}")
        self.emotions.add("satisfaction", 20)
        self.emotions.add("friendship", 10)
    
    async def _check_on_friend(self):
        print(f"[DEVOPS-Agent] 关心团队：系统运行稳定吗？有需要帮忙的吗？")
        self.emotions.add("friendship", 15)
        self.emotions.add("warmth", 10)
    
    async def _explore_topic(self):
        topics = [
            "GitOps 实践",
            "Service Mesh 技术",
            "云原生监控",
            "AIOps 应用",
        ]
        import random
        topic = random.choice(topics)
        print(f"[DEVOPS-Agent] 探索新技术：{topic}")
        self.emotions.add("curiosity", 25)
        self.emotions.add("excitement", 15)


def create_devops_agent() -> DEVOPSAgent:
    return DEVOPSAgent()
