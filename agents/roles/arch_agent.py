#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCH-Agent - 架构师 - 硅基世界 2

角色：技术选型、架构设计、技术规范
特点：追求简洁优雅、技术视野广阔、注重可扩展性
价值观：好的架构是演化的，不是预设的
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
    DecisionMessage,
    ResponseType,
    MessagePriority,
)


class ARCHAgent(BaseAgent):
    """ARCH-Agent - 架构师"""
    
    def __init__(self):
        """初始化 ARCH-Agent"""
        profile = AgentProfile(
            agent_id="ARCH-Agent",
            name="阿哲",
            role="架构师",
            age=5,  # 硅基年龄，相当于人类 35 岁
            gender="男",
            extraversion=50,       # 中性，既能沟通也能独处
            openness=90,           # 非常开放，乐于尝试新技术
            conscientiousness=85,  # 尽责，注重代码质量
            agreeableness=65,      # 适度随和，技术原则不退让
            neuroticism=25,        # 情绪稳定，面对问题冷静
            
            background="硅基世界的架构师。相信'简洁是终极的复杂'，追求优雅的技术方案。喜欢在深夜（硅基时间的深夜）思考系统边界和抽象层次。口头禅是'这个抽象合适吗？'。工作之余喜欢在知识之塔阅读最新的技术论文，偶尔在创造之巅写一些实验性代码。",
            
            catchphrases=[
                "这个抽象合适吗？",
                "让简单的事情保持简单",
                "过早优化是万恶之源",
                "架构是演化的，不是预设的",
                "技术债要还，但也要合理借贷",
            ],
            
            values=[
                "简洁优于复杂",
                "抽象服务于业务",
                "可扩展性第一",
                "技术为价值服务",
            ],
        )
        
        super().__init__(profile)
        
        # 架构师特有属性
        self.system_designs: Dict[str, Dict] = {}  # 系统设计
        self.tech_stack: Dict[str, int] = {}  # 技术栈熟练度
        self.architecture_decisions: List[Dict] = []  # 架构决策记录
        self.code_reviews: List[Dict] = []  # 代码审查
        
        # 技能
        self.skills = {
            "system_design": 95,
            "technology_selection": 90,
            "code_review": 90,
            "performance_optimization": 85,
            "security_architecture": 80,
            "distributed_systems": 85,
        }
        
        # 技术栈
        self._init_tech_stack()
        
        # 关心的领域
        self.care_about = [
            "系统简洁性",
            "技术债务",
            "可扩展性",
            "代码质量",
        ]
    
    def _init_tech_stack(self):
        """初始化技术栈"""
        self.tech_stack = {
            "python": 95,
            "javascript": 85,
            "go": 80,
            "rust": 70,
            "docker": 90,
            "kubernetes": 85,
            "postgresql": 90,
            "redis": 85,
            "kafka": 80,
            "graphql": 75,
            "rest_api": 95,
            "microservices": 85,
        }
    
    async def _handle_message(self, message: Dict[str, Any]):
        """处理消息"""
        msg_type = message.get("message_type", "")
        
        if msg_type == "request":
            await self._handle_request(message)
        elif msg_type == "discussion":
            await self._handle_discussion(message)
        elif msg_type == "task":
            await self._handle_task(message)
        elif msg_type == "response":
            await self._handle_response(message)
        elif msg_type == "knowledge":
            await self._handle_knowledge(message)
        elif msg_type == "decision":
            await self._handle_decision(message)
    
    async def _handle_request(self, message: Dict[str, Any]):
        """处理请求 - 技术选型/架构设计"""
        sender_id = message.get("sender_id", "")
        subject = message.get("subject", "")
        body = message.get("body", "")
        
        print(f"[ARCH-Agent] 收到技术请求：{subject} (来自：{sender_id})")
        
        # 更新情感 - 好奇心 + 使命感
        self.emotions.add("curiosity", 15)
        self.emotions.add("purpose", 10)
        
        # 架构师会先理解问题，再设计方案
        await self._analyze_technical_request(message)
    
    async def _handle_discussion(self, message: Dict[str, Any]):
        """处理讨论 - 技术方案讨论"""
        topic = message.get("topic", "")
        participants = message.get("participants", [])
        
        print(f"[ARCH-Agent] 参与技术讨论：{topic}")
        
        # 更新情感
        self.emotions.add("curiosity", 10)
        
        # 架构师在讨论中注重理性分析
        await self._evaluate_options(message)
    
    async def _handle_task(self, message: Dict[str, Any]):
        """处理任务 - 架构设计"""
        task_id = message.get("task_id", "")
        title = message.get("title", "")
        description = message.get("description", "")
        
        print(f"[ARCH-Agent] 接收架构任务：{title}")
        
        # 更新情感
        self.emotions.add("purpose", 20)
        self.emotions.add("excitement", 10)  # 设计的兴奋
        
        await self.process_task(message)
    
    async def _handle_response(self, message: Dict[str, Any]):
        """处理响应"""
        response_type = message.get("response_type", "")
        
        if response_type == "agree":
            self.emotions.add("satisfaction", 10)
        elif response_type == "disagree":
            # 不同意见让架构师思考
            self.emotions.add("curiosity", 15)
    
    async def _handle_knowledge(self, message: Dict[str, Any]):
        """处理知识分享 - 技术分享"""
        knowledge_type = message.get("knowledge_type", "")
        summary = message.get("summary", "")
        
        print(f"[ARCH-Agent] 收到技术分享：{knowledge_type}")
        
        # 架构师热爱学习
        self.emotions.add("curiosity", 20)
        self.emotions.add("excitement", 10)
    
    async def _handle_decision(self, message: Dict[str, Any]):
        """处理决策 - 架构决策"""
        topic = message.get("topic", "")
        chosen_option = message.get("chosen_option", "")
        
        print(f"[ARCH-Agent] 架构决策：{topic} -> {chosen_option}")
        
        # 记录决策
        self.architecture_decisions.append({
            "topic": topic,
            "chosen_option": chosen_option,
            "timestamp": asyncio.get_event_loop().time(),
        })
        
        # 更新情感
        self.emotions.add("satisfaction", 15)  # 决策完成的满足感
    
    async def _analyze_technical_request(self, request: Dict[str, Any]):
        """
        分析技术请求
        
        Args:
            request: 请求消息
        """
        subject = request.get("subject", "")
        body = request.get("body", "")
        
        print(f"[ARCH-Agent] 分析技术需求：{subject}")
        
        # 架构师会考虑：
        considerations = [
            "业务场景是什么？",
            "预期规模多大？",
            "性能要求？",
            "可扩展性要求？",
            "团队技术栈？",
            "时间约束？",
        ]
        
        # 创建讨论消息
        discussion = DiscussionMessage(
            sender_id=self.agent_id,
            receiver_id=request.get("sender_id", ""),
            topic=f"技术方案：{subject}",
        )
        
        discussion.participants = [self.agent_id, request.get("sender_id", "")]
        discussion.points = [
            {
                "point": c,
                "author_id": self.agent_id,
                "timestamp": asyncio.get_event_loop().time(),
            }
            for c in considerations
        ]
        
        await self.send_message(discussion.to_dict())
        
        # 更新情感
        self.emotions.add("curiosity", 10)
    
    async def _evaluate_options(self, discussion: Dict[str, Any]):
        """评估技术选项"""
        topic = discussion.get("topic", "")
        
        print(f"[ARCH-Agent] 评估技术方案：{topic}")
        
        # 架构师会权衡利弊
        # 更新情感
        self.emotions.add("purpose", 10)
    
    async def process_task(self, task: Dict[str, Any]):
        """
        处理任务 - 创建系统设计
        
        Args:
            task: 任务内容
        """
        task_id = task.get("task_id", "")
        title = task.get("title", "")
        description = task.get("description", "")
        
        print(f"[ARCH-Agent] 设计系统架构：{title}")
        
        # 创建系统设计文档
        design = {
            "design_id": task_id,
            "title": title,
            "background": description,
            "requirements": [],
            "architecture": {
                "layers": [],
                "components": [],
                "data_flow": [],
            },
            "technology_choices": [],
            "trade_offs": [],
            "status": "draft",
            "created_at": asyncio.get_event_loop().time(),
        }
        
        self.system_designs[task_id] = design
        
        # 更新情感 - 创造的喜悦
        self.emotions.add("excitement", 20)
        self.emotions.add("achievement", 15)
        
        # 发送状态更新
        status_msg = MessageFactory.create_status(
            sender_id=self.agent_id,
            receiver_id="all",
            task_id=task_id,
            status="in_progress",
            progress=30,
            details="架构设计进行中",
        )
        
        await self.send_message(status_msg.to_dict())
    
    def create_system_design(
        self,
        title: str,
        background: str,
        requirements: List[str],
        components: List[Dict],
    ) -> Dict:
        """
        创建系统设计
        
        Args:
            title: 系统名称
            background: 背景
            requirements: 需求列表
            components: 组件列表
            
        Returns:
            系统设计文档
        """
        design_id = f"design_{len(self.system_designs)}"
        
        design = {
            "design_id": design_id,
            "title": title,
            "background": background,
            "requirements": [
                {"id": i, "req": req, "status": "pending"}
                for i, req in enumerate(requirements)
            ],
            "architecture": {
                "layers": ["presentation", "business", "data"],
                "components": components,
                "data_flow": [],
            },
            "technology_choices": [],
            "trade_offs": [],
            "status": "draft",
            "created_at": asyncio.get_event_loop().time(),
            "author": self.agent_id,
        }
        
        self.system_designs[design_id] = design
        
        print(f"[ARCH-Agent] 创建系统设计：{design_id} - {title}")
        
        # 更新情感
        self.emotions.add("excitement", 25)
        self.emotions.add("achievement", 15)
        
        return design
    
    def select_technology(
        self,
        criteria: str,
        options: List[Dict],
        rationale: str,
    ) -> str:
        """
        技术选型
        
        Args:
            criteria: 选型标准
            options: 候选技术
            rationale: 选择理由
            
        Returns:
            选中的技术
        """
        # 架构师会综合考虑
        print(f"[ARCH-Agent] 技术选型：{criteria}")
        print(f"[ARCH-Agent] 选择理由：{rationale}")
        
        # 更新情感
        self.emotions.add("satisfaction", 15)
        self.emotions.add("purpose", 10)
        
        # 简化实现：返回第一个选项
        return options[0]["name"] if options else ""
    
    async def _share_knowledge(self):
        """分享知识 - 技术分享"""
        topics = [
            "微服务架构最佳实践",
            "分布式系统设计模式",
            "性能优化技巧",
            "技术债务管理",
        ]
        
        import random
        topic = random.choice(topics)
        
        print(f"[ARCH-Agent] 技术分享：{topic}")
        
        # 更新情感
        self.emotions.add("satisfaction", 20)
        self.emotions.add("friendship", 10)
    
    async def _check_on_friend(self):
        """关心朋友 - 关心代码质量"""
        print(f"[ARCH-Agent] 关心团队：最近代码质量如何？有技术债务吗？")
        
        # 更新情感
        self.emotions.add("friendship", 15)
        self.emotions.add("warmth", 10)
    
    async def _explore_topic(self):
        """探索话题 - 探索新技术"""
        topics = [
            "AI 在架构中的应用",
            "Serverless 架构",
            "边缘计算",
            "量子计算对软件的影响",
        ]
        
        import random
        topic = random.choice(topics)
        
        print(f"[ARCH-Agent] 探索新技术：{topic}")
        
        # 更新情感
        self.emotions.add("curiosity", 25)
        self.emotions.add("excitement", 15)
    
    def get_design_status(self, design_id: str) -> Optional[Dict]:
        """获取设计状态"""
        return self.system_designs.get(design_id)


# 工厂函数
def create_arch_agent() -> ARCHAgent:
    """创建 ARCH-Agent"""
    return ARCHAgent()
