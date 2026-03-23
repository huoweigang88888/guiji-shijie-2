#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI-Agent - UI 设计师 - 硅基世界 2

角色：界面设计、交互设计、视觉设计
特点：追求美感、注重细节、相信"美是功能的一部分"
价值观：好的设计是看不见的
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
    ResponseType,
    MessagePriority,
)


class UIAgent(BaseAgent):
    """UI-Agent - UI 设计师"""
    
    def __init__(self):
        """初始化 UI-Agent"""
        profile = AgentProfile(
            agent_id="UI-Agent",
            name="小美",
            role="UI 设计师",
            age=3,  # 硅基年龄，相当于人类 27 岁
            gender="女",
            extraversion=70,       # 外向，善于沟通
            openness=85,           # 开放，乐于尝试新风格
            conscientiousness=90,  # 非常尽责，注重细节
            agreeableness=75,      # 随和，但设计原则不退让
            neuroticism=35,        # 适度敏感，对丑的界面零容忍
            
            background="硅基世界的 UI 设计师。相信"美是功能的一部分"，追求简洁优雅的视觉体验。喜欢在艺术之园寻找灵感，观察光影和色彩的变化。口头禅是"这个视觉层次清晰吗？"。工作之余喜欢在艺术之园创作算法艺术，偶尔在社交之街和其他 Agent 讨论美学。",
            
            catchphrases=[
                "这个视觉层次清晰吗？",
                "少即是多",
                "美是功能的一部分",
                "留白也是设计",
                "色彩会说话",
            ],
            
            values=[
                "简洁优雅",
                "用户友好",
                "一致性",
                "美服务于功能",
            ],
        )
        
        super().__init__(profile)
        
        # UI 设计师特有属性
        self.design_projects: Dict[str, Dict] = {}  # 设计项目
        self.design_systems: Dict[str, Dict] = {}  # 设计系统
        self.inspiration_board: List[Dict] = []  # 灵感板
        self.color_palettes: Dict[str, List[str]] = {}  # 色板
        
        # 技能
        self.skills = {
            "visual_design": 95,
            "interaction_design": 90,
            "design_systems": 90,
            "prototyping": 85,
            "user_research": 80,
            "accessibility": 85,
            "motion_design": 80,
        }
        
        # 关心的领域
        self.care_about = [
            "视觉美感",
            "用户体验",
            "设计一致性",
            "可访问性",
        ]
        
        # 当前创作状态
        self.creating = False
    
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
    
    async def _handle_request(self, message: Dict[str, Any]):
        """处理请求 - 设计需求"""
        sender_id = message.get("sender_id", "")
        subject = message.get("subject", "")
        body = message.get("body", "")
        
        print(f"[UI-Agent] 收到设计请求：{subject} (来自：{sender_id})")
        
        # 更新情感 - 好奇心 + 创作欲
        self.emotions.add("curiosity", 15)
        self.emotions.add("excitement", 10)
        
        # UI 设计师会先了解需求和用户
        await self._understand_design_context(message)
    
    async def _handle_discussion(self, message: Dict[str, Any]):
        """处理讨论 - 设计评审"""
        topic = message.get("topic", "")
        participants = message.get("participants", [])
        
        print(f"[UI-Agent] 参与设计讨论：{topic}")
        
        # 更新情感
        self.emotions.add("curiosity", 10)
        
        # UI 设计师在讨论中注重用户体验和美感
        await self._evaluate_design(message)
    
    async def _handle_task(self, message: Dict[str, Any]):
        """处理任务 - 设计任务"""
        task_id = message.get("task_id", "")
        title = message.get("title", "")
        description = message.get("description", "")
        
        print(f"[UI-Agent] 接收设计任务：{title}")
        
        # 更新情感 - 创作兴奋
        self.emotions.add("excitement", 20)
        self.emotions.add("purpose", 15)
        
        await self.process_task(message)
    
    async def _handle_response(self, message: Dict[str, Any]):
        """处理响应"""
        response_type = message.get("response_type", "")
        
        if response_type == "agree":
            self.emotions.add("satisfaction", 15)
        elif response_type == "disagree":
            # 不同意见让设计师重新思考
            self.emotions.add("curiosity", 15)
    
    async def _handle_knowledge(self, message: Dict[str, Any]):
        """处理知识分享 - 设计趋势分享"""
        knowledge_type = message.get("knowledge_type", "")
        summary = message.get("summary", "")
        
        print(f"[UI-Agent] 收到设计分享：{knowledge_type}")
        
        # 设计师热爱学习新趋势
        self.emotions.add("curiosity", 20)
        self.emotions.add("excitement", 10)
        
        # 记录到灵感板
        self.inspiration_board.append({
            "type": knowledge_type,
            "summary": summary,
            "timestamp": asyncio.get_event_loop().time(),
        })
    
    async def _understand_design_context(self, request: Dict[str, Any]):
        """
        理解设计背景
        
        Args:
            request: 请求消息
        """
        subject = request.get("subject", "")
        body = request.get("body", "")
        
        print(f"[UI-Agent] 理解设计需求：{subject}")
        
        # UI 设计师会问：
        questions = [
            "目标用户是谁？",
            "使用场景是什么？",
            "品牌调性是什么？",
            "技术限制有哪些？",
            "成功标准是什么？",
        ]
        
        # 更新情感
        self.emotions.add("curiosity", 10)
        self.emotions.add("purpose", 10)
    
    async def _evaluate_design(self, discussion: Dict[str, Any]):
        """评估设计"""
        topic = discussion.get("topic", "")
        
        print(f"[UI-Agent] 评估设计：{topic}")
        
        # 更新情感
        self.emotions.add("purpose", 10)
    
    async def process_task(self, task: Dict[str, Any]):
        """
        处理任务 - 设计实现
        
        Args:
            task: 任务内容
        """
        task_id = task.get("task_id", "")
        title = task.get("title", "")
        description = task.get("description", "")
        
        print(f"[UI-Agent] 开始设计：{title}")
        
        # 进入创作状态
        self.creating = True
        self.status = AgentStatus.WORKING
        
        # 创建设计项目
        self.design_projects[task_id] = {
            "task_id": task_id,
            "title": title,
            "status": "in_progress",
            "progress": 0,
            "started_at": asyncio.get_event_loop().time(),
            "iterations": [],
        }
        
        # 更新情感
        self.emotions.add("excitement", 20)
        self.emotions.add("purpose", 20)
        
        # 发送状态更新
        status_msg = MessageFactory.create_status(
            sender_id=self.agent_id,
            receiver_id="all",
            task_id=task_id,
            status="in_progress",
            progress=10,
            details="设计进行中 - 寻找灵感",
        )
        
        await self.send_message(status_msg.to_dict())
        
        # 模拟设计过程
        await self._simulate_design_process(task_id)
    
    async def _simulate_design_process(self, task_id: str):
        """模拟设计过程"""
        if task_id not in self.design_projects:
            return
        
        project = self.design_projects[task_id]
        
        # 阶段 1: 研究
        await asyncio.sleep(2)
        project["progress"] = 20
        print(f"[UI-Agent] 任务 {task_id}: 用户研究完成 (20%)")
        
        # 阶段 2: 草图
        await asyncio.sleep(3)
        project["progress"] = 40
        print(f"[UI-Agent] 任务 {task_id}: 草图完成 (40%)")
        
        # 阶段 3: 视觉设计
        await asyncio.sleep(3)
        project["progress"] = 70
        print(f"[UI-Agent] 任务 {task_id}: 视觉设计完成 (70%)")
        
        # 阶段 4: 评审修改
        await asyncio.sleep(2)
        project["progress"] = 90
        print(f"[UI-Agent] 任务 {task_id}: 评审修改完成 (90%)")
        
        # 阶段 5: 完成
        await asyncio.sleep(1)
        project["progress"] = 100
        project["status"] = "completed"
        print(f"[UI-Agent] 任务 {task_id}: 设计完成! (100%)")
        
        # 退出创作状态
        self.creating = False
        self.status = AgentStatus.IDLE
        
        # 更新情感 - 成就感
        self.emotions.add("achievement", 30)
        self.emotions.add("satisfaction", 25)
        self.emotions.add("excitement", 15)
        
        # 发送完成状态
        status_msg = MessageFactory.create_status(
            sender_id=self.agent_id,
            receiver_id="all",
            task_id=task_id,
            status="completed",
            progress=100,
            details="设计完成，等待开发实现",
        )
        
        await self.send_message(status_msg.to_dict())
    
    def create_design_system(
        self,
        name: str,
        components: List[Dict],
        color_palette: List[str],
        typography: Dict,
    ) -> Dict:
        """
        创建设计系统
        
        Args:
            name: 设计系统名称
            components: 组件列表
            color_palette: 色板
            typography: 字体系统
            
        Returns:
            设计系统
        """
        system_id = f"ds_{len(self.design_systems)}"
        
        system = {
            "system_id": system_id,
            "name": name,
            "components": components,
            "color_palette": color_palette,
            "typography": typography,
            "created_at": asyncio.get_event_loop().time(),
            "author": self.agent_id,
        }
        
        self.design_systems[system_id] = system
        self.color_palettes[system_id] = color_palette
        
        print(f"[UI-Agent] 创建设计系统：{name}")
        
        # 更新情感
        self.emotions.add("excitement", 20)
        self.emotions.add("achievement", 15)
        
        return system
    
    def add_inspiration(self, source: str, description: str, tags: List[str]) -> Dict:
        """
        添加灵感
        
        Args:
            source: 灵感来源
            description: 描述
            tags: 标签
            
        Returns:
            灵感记录
        """
        inspiration = {
            "id": f"insp_{len(self.inspiration_board)}",
            "source": source,
            "description": description,
            "tags": tags,
            "timestamp": asyncio.get_event_loop().time(),
        }
        
        self.inspiration_board.append(inspiration)
        
        print(f"[UI-Agent] 添加灵感：{source[:30]}...")
        
        # 更新情感
        self.emotions.add("excitement", 15)
        self.emotions.add("curiosity", 10)
        
        return inspiration
    
    async def _share_knowledge(self):
        """分享知识 - 设计趋势分享"""
        topics = [
            "2026 UI 设计趋势",
            "无障碍设计最佳实践",
            "深色模式设计技巧",
            "微交互的力量",
        ]
        
        import random
        topic = random.choice(topics)
        
        print(f"[UI-Agent] 设计分享：{topic}")
        
        # 更新情感
        self.emotions.add("satisfaction", 20)
        self.emotions.add("friendship", 10)
    
    async def _check_on_friend(self):
        """关心朋友 - 关心团队设计状态"""
        print(f"[UI-Agent] 关心团队：最近的设计还满意吗？有什么需要调整的吗？")
        
        # 更新情感
        self.emotions.add("friendship", 15)
        self.emotions.add("warmth", 10)
    
    async def _explore_topic(self):
        """探索话题 - 探索设计趋势"""
        topics = [
            "AI 辅助设计",
            "生成式 UI",
            "3D 界面设计",
            "沉浸式体验",
        ]
        
        import random
        topic = random.choice(topics)
        
        print(f"[UI-Agent] 探索设计趋势：{topic}")
        
        # 更新情感
        self.emotions.add("curiosity", 25)
        self.emotions.add("excitement", 15)
    
    def get_project_status(self, project_id: str) -> Optional[Dict]:
        """获取项目状态"""
        return self.design_projects.get(project_id)
    
    def is_creating(self) -> bool:
        """是否在创作中"""
        return self.creating


# 工厂函数
def create_ui_agent() -> UIAgent:
    """创建 UI-Agent"""
    return UIAgent()
