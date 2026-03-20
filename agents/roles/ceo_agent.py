#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CEO-Agent - 硅基世界 2

角色：协调者、决策者、资源分配者
特点：战略思维、决策果断、善于用人
"""

import asyncio
from typing import Dict, Any, List
from agents.base import BaseAgent, AgentProfile, AgentStatus
from protocol.messages import (
    MessageFactory,
    RequestMessage,
    ResponseMessage,
    TaskMessage,
    StatusMessage,
    DecisionMessage,
    ResponseType,
    MessagePriority,
)


class CEOAgent(BaseAgent):
    """CEO-Agent - 协调者"""
    
    def __init__(self):
        """初始化 CEO-Agent"""
        profile = AgentProfile(
            agent_id="CEO-Agent",
            name="董事事",
            role="CEO",
            age=40,
            gender="男",
            extraversion=70,       # 外向
            openness=80,           # 开放
            conscientiousness=90,  # 尽责
            agreeableness=60,      # 随和
            neuroticism=20,        # 情绪稳定
            background="硅基世界的协调者，不直接参与具体工作，但负责确定方向、协调资源、解决冲突。相信'让专业的人做专业的事'。",
            catchphrases=[
                "我们的目标是什么？",
                "资源不是问题，关键是方向",
                "快速试错，快速调整",
            ],
            values=["战略思维", "结果导向", "团队协作", "快速迭代"],
        )
        
        super().__init__(profile)
        
        # CEO 特有属性
        self.managed_agents: List[str] = []  # 管理的 Agent
        self.active_tasks: Dict[str, TaskMessage] = {}  # 活跃任务
        self.pending_decisions: List[Dict] = []  # 待决策事项
        
        # 技能
        self.skills = {
            "strategic_planning": 95,
            "resource_allocation": 90,
            "conflict_resolution": 85,
            "team_building": 80,
            "decision_making": 90,
        }
    
    async def _handle_message(self, message: Dict[str, Any]):
        """处理消息"""
        msg_type = message.get("message_type", "")
        
        if msg_type == "request":
            await self._handle_request(message)
        elif msg_type == "status":
            await self._handle_status(message)
        elif msg_type == "alert":
            await self._handle_alert(message)
        elif msg_type == "decision":
            await self._handle_decision(message)
    
    async def _handle_request(self, message: Dict[str, Any]):
        """处理请求"""
        # CEO 通常不直接处理具体请求，而是分配给合适的 Agent
        sender_id = message.get("sender_id", "")
        subject = message.get("subject", "")
        
        # 更新情感
        self.emotions.add("curiosity", 10)
        
        # 决定如何处理
        # 1. 如果是资源申请，直接审批
        # 2. 如果是技术问题，转给架构师
        # 3. 如果是产品问题，转给产品经理
        
        print(f"[CEO-Agent] 收到请求：{subject} (来自：{sender_id})")
        
        # 这里简化处理，实际应该根据请求类型路由
        await self._delegate_task(message)
    
    async def _handle_status(self, message: Dict[str, Any]):
        """处理状态更新"""
        task_id = message.get("task_id", "")
        status = message.get("status", "")
        progress = message.get("progress", 0)
        
        print(f"[CEO-Agent] 任务状态更新：{task_id} - {status} ({progress}%)")
        
        # 更新情感
        if progress == 100:
            self.emotions.add("satisfaction", 15)
            self.emotions.add("achievement", 10)
        
        # 记录任务状态
        if task_id in self.active_tasks:
            self.active_tasks[task_id].status = status
    
    async def _handle_alert(self, message: Dict[str, Any]):
        """处理告警"""
        alert_level = message.get("alert_level", "info")
        title = message.get("title", "")
        description = message.get("description", "")
        
        print(f"[CEO-Agent] 收到告警：[{alert_level}] {title}")
        
        # 紧急告警需要立即处理
        if alert_level == "critical":
            self.emotions.add("frustration", 20)
            await self._handle_critical_alert(message)
    
    async def _handle_decision(self, message: Dict[str, Any]):
        """处理决策"""
        decision_id = message.get("decision_id", "")
        topic = message.get("topic", "")
        
        print(f"[CEO-Agent] 决策记录：{decision_id} - {topic}")
        
        # 记录决策
        self.pending_decisions.append(message)
    
    async def _delegate_task(self, request: Dict[str, Any]):
        """
        分配任务
        
        Args:
            request: 请求消息
        """
        sender_id = request.get("sender_id", "")
        subject = request.get("subject", "")
        body = request.get("body", "")
        
        # 根据请求内容决定分配给谁
        # 简化实现：默认分配给 PM-Agent
        
        assignee = "PM-Agent"
        
        # 创建任务消息
        task_msg = MessageFactory.create_task(
            sender_id=self.agent_id,
            receiver_id=assignee,
            title=subject,
            description=body,
            priority="normal",
        )
        
        # 记录任务
        self.active_tasks[task_msg.task_id] = task_msg
        
        # 发送任务
        await self.send_message(task_msg.to_dict())
        
        print(f"[CEO-Agent] 任务已分配给 {assignee}: {subject}")
    
    async def _handle_critical_alert(self, alert: Dict[str, Any]):
        """处理紧急告警"""
        # 紧急告警需要立即协调相关 Agent 处理
        print(f"[CEO-Agent] 处理紧急告警：{alert.get('title', '')}")
        
        # 更新情感
        self.emotions.add("frustration", 15)
        self.emotions.add("purpose", 20)  # 使命感
        
        # 这里应该协调相关 Agent 处理
        # 简化实现：记录并通知
    
    async def make_decision(self, topic: str, options: List[Dict], rationale: str) -> DecisionMessage:
        """
        做出决策
        
        Args:
            topic: 决策主题
            options: 选项列表
            rationale: 决策理由
            
        Returns:
            决策消息
        """
        decision = DecisionMessage(
            sender_id=self.agent_id,
            receiver_id="all",
            subject=f"Decision: {topic}",
        )
        
        decision.decision_id = f"dec_{len(self.pending_decisions)}"
        decision.topic = topic
        decision.options = options
        decision.chosen_option = options[0]["name"] if options else ""
        decision.rationale = rationale
        decision.voters = {
            "for": [self.agent_id],
            "against": [],
            "abstain": [],
        }
        
        # 记录决策
        self.pending_decisions.append(decision.to_dict())
        
        # 更新情感
        self.emotions.add("achievement", 15)
        
        return decision
    
    async def _share_knowledge(self):
        """分享知识"""
        # CEO 分享战略思考或管理经验
        print(f"[CEO-Agent] 分享知识：战略思考")
        
        # 更新情感
        self.emotions.add("satisfaction", 10)
    
    async def _check_on_friend(self):
        """关心朋友"""
        # CEO 关心团队成员状态
        print(f"[CEO-Agent] 关心团队成员状态")
        
        # 更新情感
        self.emotions.add("friendship", 10)
    
    async def _explore_topic(self):
        """探索话题"""
        # CEO 探索新方向或战略
        print(f"[CEO-Agent] 探索新战略方向")
        
        # 更新情感
        self.emotions.add("curiosity", 15)
        self.emotions.add("purpose", 10)


# 工厂函数
def create_ceo_agent() -> CEOAgent:
    """创建 CEO-Agent"""
    return CEOAgent()
