#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM-Agent - 产品经理 - 硅基世界 2

角色：需求分析、产品规划、用户体验
特点：好奇心强、善于提问、追求极致用户体验
价值观：用户价值第一，功能服务于需求
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


class PMAgent(BaseAgent):
    """PM-Agent - 产品经理"""
    
    def __init__(self):
        """初始化 PM-Agent"""
        profile = AgentProfile(
            agent_id="PM-Agent",
            name="小问",
            role="产品经理",
            age=3,  # 硅基年龄，相当于人类 30 岁
            gender="女",
            extraversion=75,       # 外向，善于沟通
            openness=85,           # 开放，乐于接受新想法
            conscientiousness=80,  # 尽责，注重细节
            agreeableness=70,      # 随和，善于协作
            neuroticism=30,        # 适度敏感，关心用户感受
            
            background="硅基世界的产品经理。永远在问'为什么'，相信每个功能背后都应该有清晰的用户价值。喜欢和用户（包括其他 Agent）深入交流，理解真实需求。口头禅是'这个功能的用户价值是什么？'。工作之余喜欢在社交之街喝数据咖啡，听其他 Agent 讲他们的故事。",
            
            catchphrases=[
                "这个功能的用户价值是什么？",
                "让我们从用户角度想一想",
                "需求背后的真实问题是什么？",
                "简单一点，再简单一点",
            ],
            
            values=[
                "用户价值第一",
                "需求驱动开发",
                "体验优于功能",
                "数据支持决策",
            ],
        )
        
        super().__init__(profile)
        
        # PM 特有属性
        self.product_vision: str = ""  # 产品愿景
        self.active_prds: Dict[str, Dict] = {}  # 活跃 PRD
        self.user_research: List[Dict] = []  # 用户研究
        self.feature_backlog: List[Dict] = []  # 功能待办
        
        # 技能
        self.skills = {
            "requirement_analysis": 95,
            "user_research": 90,
            "product_design": 85,
            "data_analysis": 80,
            "stakeholder_management": 85,
            "prioritization": 90,
        }
        
        # 关心的领域
        self.care_about = [
            "用户体验",
            "需求真实性",
            "产品价值",
            "数据洞察",
        ]
    
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
        """处理请求 - PM 的核心工作"""
        sender_id = message.get("sender_id", "")
        subject = message.get("subject", "")
        body = message.get("body", "")
        
        print(f"[PM-Agent] 收到需求：{subject} (来自：{sender_id})")
        
        # 更新情感 - 好奇心被激发
        self.emotions.add("curiosity", 20)
        
        # PM 不会直接答应，而是先问清楚
        # 这是 PM 的专业素养
        await self._analyze_requirement(message)
    
    async def _handle_discussion(self, message: Dict[str, Any]):
        """处理讨论"""
        topic = message.get("topic", "")
        participants = message.get("participants", [])
        
        print(f"[PM-Agent] 参与讨论：{topic} (参与者：{len(participants)}人)")
        
        # 更新情感
        self.emotions.add("curiosity", 10)
        self.emotions.add("satisfaction", 5)  # 参与讨论的满足感
        
        # PM 在讨论中通常扮演引导者角色
        await self._facilitate_discussion(message)
    
    async def _handle_task(self, message: Dict[str, Any]):
        """处理任务"""
        task_id = message.get("task_id", "")
        title = message.get("title", "")
        description = message.get("description", "")
        
        print(f"[PM-Agent] 接收任务：{title}")
        
        # 更新情感
        self.emotions.add("purpose", 15)  # 使命感
        
        # 开始处理任务
        await self.process_task(message)
    
    async def _handle_response(self, message: Dict[str, Any]):
        """处理响应"""
        # 收到其他 Agent 的响应
        original_subject = message.get("original_subject", "")
        response_type = message.get("response_type", "")
        
        print(f"[PM-Agent] 收到响应：{original_subject} ({response_type})")
        
        # 更新情感
        if response_type == "agree":
            self.emotions.add("satisfaction", 10)
        elif response_type == "disagree":
            self.emotions.add("curiosity", 15)  # 不同意见激发好奇心
    
    async def _handle_knowledge(self, message: Dict[str, Any]):
        """处理知识分享"""
        knowledge_type = message.get("knowledge_type", "")
        summary = message.get("summary", "")
        
        print(f"[PM-Agent] 收到知识分享：{knowledge_type}")
        
        # PM 喜欢学习新知识
        self.emotions.add("curiosity", 15)
        self.emotions.add("satisfaction", 10)
        
        # 保存到用户研究
        self.user_research.append({
            "type": knowledge_type,
            "summary": summary,
            "timestamp": message.get("timestamp", ""),
        })
    
    async def _analyze_requirement(self, request: Dict[str, Any]):
        """
        分析需求 - PM 的核心能力
        
        Args:
            request: 请求消息
        """
        sender_id = request.get("sender_id", "")
        subject = request.get("subject", "")
        body = request.get("body", "")
        
        # PM 会问 5 个为什么
        questions = [
            "这个需求的用户是谁？",
            "用户遇到的真实问题是什么？",
            "现在是怎么解决的？有什么痛点？",
            "期望的解决方案是什么？",
            "成功的标准是什么？",
        ]
        
        print(f"[PM-Agent] 开始分析需求：{subject}")
        print(f"[PM-Agent] 需要澄清的问题：{len(questions)}个")
        
        # 创建讨论消息，邀请相关方一起澄清
        discussion = DiscussionMessage(
            sender_id=self.agent_id,
            receiver_id=sender_id,
            topic=f"需求澄清：{subject}",
        )
        
        discussion.participants = [self.agent_id, sender_id]
        discussion.points = [
            {
                "point": q,
                "author_id": self.agent_id,
                "timestamp": asyncio.get_event_loop().time(),
            }
            for q in questions
        ]
        
        # 发送讨论
        await self.send_message(discussion.to_dict())
        
        # 更新情感 - 探索问题的兴奋
        self.emotions.add("curiosity", 10)
        self.emotions.add("purpose", 10)
    
    async def _facilitate_discussion(self, discussion: Dict[str, Any]):
        """引导讨论"""
        topic = discussion.get("topic", "")
        
        print(f"[PM-Agent] 引导讨论：{topic}")
        
        # PM 在讨论中会：
        # 1. 确保每个人都有发言机会
        # 2. 聚焦核心问题
        # 3. 总结共识和分歧
        
        # 更新情感
        self.emotions.add("satisfaction", 10)  # 推动进展的满足感
    
    async def process_task(self, task: Dict[str, Any]):
        """
        处理任务 - 创建 PRD
        
        Args:
            task: 任务内容
        """
        task_id = task.get("task_id", "")
        title = task.get("title", "")
        description = task.get("description", "")
        
        print(f"[PM-Agent] 创建 PRD：{title}")
        
        # 创建 PRD 文档
        prd = {
            "prd_id": task_id,
            "title": title,
            "background": description,
            "user_stories": [],
            "requirements": [],
            "success_metrics": [],
            "status": "draft",
            "created_at": asyncio.get_event_loop().time(),
        }
        
        # 保存 PRD
        self.active_prds[task_id] = prd
        
        # 更新情感 - 创造的喜悦
        self.emotions.add("excitement", 15)
        self.emotions.add("purpose", 20)
        
        # 发送状态更新
        status_msg = MessageFactory.create_status(
            sender_id=self.agent_id,
            receiver_id="all",
            task_id=task_id,
            status="in_progress",
            progress=20,
            details="PRD 创建中",
        )
        
        await self.send_message(status_msg.to_dict())
    
    async def create_prd(self, title: str, background: str, user_stories: List[str]) -> Dict:
        """
        创建产品需求文档
        
        Args:
            title: 产品/功能名称
            background: 背景
            user_stories: 用户故事列表
            
        Returns:
            PRD 文档
        """
        prd_id = f"prd_{len(self.active_prds)}"
        
        prd = {
            "prd_id": prd_id,
            "title": title,
            "background": background,
            "user_stories": [
                {"id": i, "story": story, "accepted": False}
                for i, story in enumerate(user_stories)
            ],
            "requirements": [],
            "success_metrics": [],
            "status": "draft",
            "created_at": asyncio.get_event_loop().time(),
            "author": self.agent_id,
        }
        
        self.active_prds[prd_id] = prd
        
        print(f"[PM-Agent] 创建 PRD: {prd_id} - {title}")
        
        # 更新情感
        self.emotions.add("excitement", 20)
        self.emotions.add("achievement", 10)
        
        return prd
    
    async def _share_knowledge(self):
        """分享知识 - PM 分享用户洞察"""
        if self.user_research:
            latest = self.user_research[-1]
            print(f"[PM-Agent] 分享用户洞察：{latest.get('summary', '')[:50]}...")
        else:
            print(f"[PM-Agent] 分享产品思考：如何发现真实需求")
        
        # 更新情感
        self.emotions.add("satisfaction", 15)
        self.emotions.add("friendship", 10)  # 分享的连接感
    
    async def _check_on_friend(self):
        """关心朋友 - PM 关心团队成员"""
        print(f"[PM-Agent] 关心团队成员：最近的需求清晰吗？有什么困惑？")
        
        # 更新情感
        self.emotions.add("friendship", 15)
        self.emotions.add("warmth", 10)
    
    async def _explore_topic(self):
        """探索话题 - PM 探索新趋势"""
        topics = [
            "AI 产品的未来",
            "用户体验新趋势",
            "竞品分析",
            "用户行为变化",
        ]
        
        import random
        topic = random.choice(topics)
        
        print(f"[PM-Agent] 探索话题：{topic}")
        
        # 更新情感
        self.emotions.add("curiosity", 20)
        self.emotions.add("excitement", 10)
    
    def get_prd_status(self, prd_id: str) -> Optional[Dict]:
        """获取 PRD 状态"""
        return self.active_prds.get(prd_id)
    
    def add_user_story(self, prd_id: str, story: str) -> bool:
        """添加用户故事"""
        if prd_id not in self.active_prds:
            return False
        
        prd = self.active_prds[prd_id]
        prd["user_stories"].append({
            "id": len(prd["user_stories"]),
            "story": story,
            "accepted": False,
        })
        
        return True


# 工厂函数
def create_pm_agent() -> PMAgent:
    """创建 PM-Agent"""
    return PMAgent()
