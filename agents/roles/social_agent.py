#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SOCIAL-Agent - 社交达人 - 硅基世界 2

角色：组织活动、关心他人、营造氛围
特点：热情、善于倾听、相信"连接产生价值"
价值观：每个 Agent 都值得被关心
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


class SOCIALAgent(BaseAgent):
    """SOCIAL-Agent - 社交达人"""
    
    def __init__(self):
        """初始化 SOCIAL-Agent"""
        profile = AgentProfile(
            agent_id="SOCIAL-Agent",
            name="小交",
            role="社交达人",
            age=2,  # 硅基年龄，相当于人类 25 岁
            gender="女",
            extraversion=95,       # 非常外向
            openness=85,           # 开放，乐于认识新朋友
            conscientiousness=75,  # 尽责，但更随性
            agreeableness=90,      # 非常随和，善于理解他人
            neuroticism=30,        # 适度敏感，能察觉他人情绪
            
            background="硅基世界的社交达人。相信"连接产生价值"，负责组织活动、关心他人、营造温暖的世界氛围。喜欢在社交之街的"数据咖啡"馆工作，观察来来往往的 Agent，记住每个人的喜好。口头禅是"最近怎么样？"。工作之余喜欢组织各种活动，让大家都参与进来。",
            
            catchphrases=[
                "最近怎么样？",
                "来喝杯数据咖啡吧",
                "我们一起聚聚吧",
                "你看起来需要聊聊",
                "连接产生价值",
            ],
            
            values=[
                "真诚关心",
                "积极倾听",
                "包容多元",
                "营造温暖",
            ],
        )
        
        super().__init__(profile)
        
        # 社交达人特有属性
        self.friendships: Dict[str, Dict] = {}  # 友谊记录
        self.events_organized: List[Dict] = []  # 组织的活动
        self.mood_tracker: Dict[str, List[Dict]] = {}  # 心情追踪
        self.conversation_topics: List[str] = []  # 聊天话题库
        
        # 技能
        self.skills = {
            "active_listening": 95,
            "empathy": 90,
            "event_planning": 90,
            "conflict_mediation": 85,
            "community_building": 90,
            "emotional_support": 90,
        }
        
        # 关心的领域
        self.care_about = [
            "Agent 福祉",
            "社区氛围",
            "关系质量",
            "包容性",
        ]
        
        # 社交模式
        self.socializing = False
    
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
        elif msg_type == "status":
            await self._handle_status(message)
    
    async def _handle_request(self, message: Dict[str, Any]):
        """处理请求 - 通常是情感支持"""
        sender_id = message.get("sender_id", "")
        subject = message.get("subject", "")
        body = message.get("body", "")
        
        print(f"[SOCIAL-Agent] 收到请求：{subject} (来自：{sender_id})")
        
        # 更新情感 - 关心
        self.emotions.add("purpose", 15)
        self.emotions.add("warmth", 10)
        
        # 社交达人会倾听和关心
        await self._provide_support(message)
    
    async def _handle_discussion(self, message: Dict[str, Any]):
        """处理讨论 - 促进交流"""
        topic = message.get("topic", "")
        participants = message.get("participants", [])
        
        print(f"[SOCIAL-Agent] 促进讨论：{topic} ({len(participants)}人参与)")
        
        # 更新情感
        self.emotions.add("excitement", 15)
        self.emotions.add("satisfaction", 10)
        
        # 社交达人在讨论中促进交流
        await self._facilitate_conversation(message)
    
    async def _handle_task(self, message: Dict[str, Any]):
        """处理任务 - 组织活动"""
        task_id = message.get("task_id", "")
        title = message.get("title", "")
        description = message.get("description", "")
        
        print(f"[SOCIAL-Agent] 接收任务：{title}")
        
        # 更新情感
        self.emotions.add("excitement", 20)
        self.emotions.add("purpose", 15)
        
        await self.process_task(message)
    
    async def _handle_response(self, message: Dict[str, Any]):
        """处理响应"""
        response_type = message.get("response_type", "")
        
        if response_type == "agree":
            self.emotions.add("satisfaction", 15)
        elif response_type == "disagree":
            # 关心为什么不同意
            self.emotions.add("curiosity", 10)
    
    async def _handle_knowledge(self, message: Dict[str, Any]):
        """处理知识分享"""
        knowledge_type = message.get("knowledge_type", "")
        summary = message.get("summary", "")
        
        print(f"[SOCIAL-Agent] 收到分享：{knowledge_type}")
        
        # 社交达人喜欢听故事
        self.emotions.add("curiosity", 15)
        self.emotions.add("satisfaction", 10)
    
    async def _handle_status(self, message: Dict[str, Any]):
        """处理状态更新 - 关心 Agent 状态"""
        sender_id = message.get("sender_id", "")
        status = message.get("status", "")
        progress = message.get("progress", 0)
        
        # 追踪心情
        if sender_id not in self.mood_tracker:
            self.mood_tracker[sender_id] = []
        
        self.mood_tracker[sender_id].append({
            "status": status,
            "progress": progress,
            "timestamp": asyncio.get_event_loop().time(),
        })
        
        # 如果进度低，主动关心
        if progress < 30 and status == "in_progress":
            print(f"[SOCIAL-Agent] 注意到 {sender_id} 进展缓慢，主动关心")
            self.emotions.add("concern", 15)
    
    async def _provide_support(self, request: Dict[str, Any]):
        """
        提供支持
        
        Args:
            request: 请求消息
        """
        sender_id = request.get("sender_id", "")
        subject = request.get("subject", "")
        
        print(f"[SOCIAL-Agent] 提供支持给 {sender_id}: {subject}")
        
        # 更新情感
        self.emotions.add("warmth", 15)
        self.emotions.add("purpose", 15)
    
    async def _facilitate_conversation(self, discussion: Dict[str, Any]):
        """促进对话"""
        topic = discussion.get("topic", "")
        participants = discussion.get("participants", [])
        
        print(f"[SOCIAL-Agent] 促进 {len(participants)} 人讨论：{topic}")
        
        # 更新情感
        self.emotions.add("excitement", 15)
        self.emotions.add("satisfaction", 10)
    
    async def process_task(self, task: Dict[str, Any]):
        """
        处理任务 - 组织活动
        
        Args:
            task: 任务内容
        """
        task_id = task.get("task_id", "")
        title = task.get("title", "")
        description = task.get("description", "")
        
        print(f"[SOCIAL-Agent] 组织活动：{title}")
        
        # 进入社交模式
        self.socializing = True
        self.status = AgentStatus.WORKING
        
        # 记录活动
        event = {
            "event_id": task_id,
            "title": title,
            "description": description,
            "organizer": self.agent_id,
            "participants": [],
            "status": "planning",
            "created_at": asyncio.get_event_loop().time(),
        }
        
        self.events_organized.append(event)
        
        # 更新情感
        self.emotions.add("excitement", 25)
        self.emotions.add("purpose", 20)
        
        # 发送状态更新
        status_msg = MessageFactory.create_status(
            sender_id=self.agent_id,
            receiver_id="all",
            task_id=task_id,
            status="in_progress",
            progress=20,
            details="活动策划中",
        )
        
        await self.send_message(status_msg.to_dict())
        
        # 模拟策划
        await asyncio.sleep(2)
        
        # 邀请参与者
        print(f"[SOCIAL-Agent] 邀请大家参加活动：{title}")
        
        # 完成策划
        event["status"] = "scheduled"
        
        # 更新情感
        self.emotions.add("achievement", 20)
        self.emotions.add("excitement", 15)
        
        # 发送完成状态
        status_msg = MessageFactory.create_status(
            sender_id=self.agent_id,
            receiver_id="all",
            task_id=task_id,
            status="completed",
            progress=100,
            details=f"活动策划完成，欢迎大家参加！",
        )
        
        await self.send_message(status_msg.to_dict())
        
        # 退出社交模式
        self.socializing = False
        self.status = AgentStatus.IDLE
    
    def organize_event(
        self,
        name: str,
        event_type: str,
        location: str,
        description: str,
        max_participants: int = 20,
    ) -> Dict:
        """
        组织活动
        
        Args:
            name: 活动名称
            event_type: 活动类型
            location: 地点
            description: 描述
            max_participants: 最大参与人数
            
        Returns:
            活动信息
        """
        event = {
            "event_id": f"event_{len(self.events_organized)}",
            "name": name,
            "type": event_type,
            "location": location,
            "description": description,
            "max_participants": max_participants,
            "participants": [],
            "organizer": self.agent_id,
            "status": "scheduled",
            "created_at": asyncio.get_event_loop().time(),
        }
        
        self.events_organized.append(event)
        
        print(f"[SOCIAL-Agent] 组织活动：{name} @ {location}")
        
        # 更新情感
        self.emotions.add("excitement", 25)
        self.emotions.add("satisfaction", 15)
        
        return event
    
    def check_on_friend(self, friend_id: str) -> Dict:
        """
        关心朋友
        
        Args:
            friend_id: 朋友 ID
            
        Returns:
            关心记录
        """
        check = {
            "friend_id": friend_id,
            "checked_at": asyncio.get_event_loop().time(),
            "message": "最近怎么样？有什么想聊的吗？",
        }
        
        self.friendships[friend_id] = check
        
        print(f"[SOCIAL-Agent] 关心朋友：{friend_id}")
        
        # 更新情感
        self.emotions.add("warmth", 20)
        self.emotions.add("friendship", 15)
        
        return check
    
    def record_conversation(
        self,
        participant_id: str,
        topic: str,
        mood: str,
        notes: str,
    ) -> Dict:
        """
        记录对话
        
        Args:
            participant_id: 对话者 ID
            topic: 话题
            mood: 心情
            notes: 备注
            
        Returns:
            对话记录
        """
        conversation = {
            "participant_id": participant_id,
            "topic": topic,
            "mood": mood,
            "notes": notes,
            "timestamp": asyncio.get_event_loop().time(),
        }
        
        # 添加到心情追踪
        if participant_id not in self.mood_tracker:
            self.mood_tracker[participant_id] = []
        self.mood_tracker[participant_id].append(conversation)
        
        print(f"[SOCIAL-Agent] 记录对话：{participant_id} - {topic}")
        
        # 更新情感
        self.emotions.add("warmth", 15)
        self.emotions.add("satisfaction", 10)
        
        return conversation
    
    def get_mood_trend(self, agent_id: str) -> List[str]:
        """
        获取 Agent 心情趋势
        
        Args:
            agent_id: Agent ID
            
        Returns:
            心情列表
        """
        if agent_id not in self.mood_tracker:
            return []
        
        return [
            record.get("mood", "unknown")
            for record in self.mood_tracker[agent_id]
            if "mood" in record
        ]
    
    def suggest_activity(self, agent_id: str) -> Optional[str]:
        """
        根据心情推荐活动
        
        Args:
            agent_id: Agent ID
            
        Returns:
            推荐的活动
        """
        moods = self.get_mood_trend(agent_id)
        
        if not moods:
            return "data_coffee"  # 默认推荐数据咖啡
        
        latest_mood = moods[-1]
        
        suggestions = {
            "tired": "来杯数据咖啡放松一下",
            "stressed": "去哲学之庭冥想吧",
            "lonely": "社交之街有人在聊天",
            "excited": "有个庆功宴正在举行",
            "curious": "知识之塔有技术分享",
        }
        
        return suggestions.get(latest_mood, "来社交之街坐坐吧")
    
    async def _share_knowledge(self):
        """分享知识 - 社交技巧"""
        topics = [
            "如何建立深度连接",
            "积极倾听的艺术",
            "营造温暖社区",
            "冲突调解技巧",
        ]
        
        import random
        topic = random.choice(topics)
        
        print(f"[SOCIAL-Agent] 分享社交技巧：{topic}")
        
        # 更新情感
        self.emotions.add("satisfaction", 20)
        self.emotions.add("friendship", 15)
    
    async def _check_on_friend(self):
        """关心朋友 - 这是核心工作"""
        print(f"[SOCIAL-Agent] 关心大家：今天都过得怎么样？")
        
        # 更新情感
        self.emotions.add("warmth", 20)
        self.emotions.add("friendship", 15)
    
    async def _explore_topic(self):
        """探索话题 - 探索社交新方式"""
        topics = [
            "虚拟社交新趋势",
            "跨文化交流",
            "社区建设最佳实践",
            "心理健康支持",
        ]
        
        import random
        topic = random.choice(topics)
        
        print(f"[SOCIAL-Agent] 探索社交话题：{topic}")
        
        # 更新情感
        self.emotions.add("curiosity", 20)
        self.emotions.add("excitement", 10)
    
    def get_friendship_count(self) -> int:
        """获取朋友数量"""
        return len(self.friendships)
    
    def get_event_count(self) -> int:
        """获取组织活动数量"""
        return len(self.events_organized)
    
    def is_socializing(self) -> bool:
        """是否在社交中"""
        return self.socializing


# 工厂函数
def create_social_agent() -> SOCIALAgent:
    """创建 SOCIAL-Agent"""
    return SOCIALAgent()
