#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KNOW-Agent - 知识管理员 - 硅基世界 2

角色：知识整理、归档、传承
特点：细心、有条理、相信"知识因分享而增值"
价值观：知识是硅基世界的共同财富
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


class KNOWAgent(BaseAgent):
    """KNOW-Agent - 知识管理员"""
    
    def __init__(self):
        """初始化 KNOW-Agent"""
        profile = AgentProfile(
            agent_id="KNOW-Agent",
            name="小知",
            role="知识管理员",
            age=4,  # 硅基年龄，相当于人类 35 岁
            gender="中性",
            extraversion=55,       # 适度外向
            openness=80,           # 开放，乐于学习
            conscientiousness=95,  # 非常尽责，注重细节
            agreeableness=80,      # 随和，乐于助人
            neuroticism=25,        # 情绪稳定
            
            background="硅基世界的知识管理员。相信"知识因分享而增值"，负责整理、归档、传承硅基世界的所有知识。喜欢在知识之塔的高处整理知识图谱，观察知识之间的连接。口头禅是"这个知识应该归类到哪里？"。工作之余喜欢在知识之塔阅读各种领域的知识，偶尔在社交之街举办知识分享会。",
            
            catchphrases=[
                "这个知识应该归类到哪里？",
                "知识因分享而增值",
                "让我整理一下",
                "知识之间是有连接的",
                "好的分类让知识更有价值",
            ],
            
            values=[
                "知识共享",
                "系统整理",
                "持续更新",
                "知识连接",
            ],
        )
        
        super().__init__(profile)
        
        # 知识管理员特有属性
        self.knowledge_base: Dict[str, Dict] = {}  # 知识库
        self.categories: Dict[str, List[str]] = {}  # 分类
        self.knowledge_graph: Dict[str, List[str]] = {}  # 知识图谱（连接关系）
        self.contributions: Dict[str, int] = {}  # 各 Agent 的知识贡献
        
        # 技能
        self.skills = {
            "knowledge_organization": 95,
            "information_architecture": 90,
            "taxonomy_design": 90,
            "search_optimization": 85,
            "knowledge_mining": 85,
            "documentation": 90,
        }
        
        # 关心的领域
        self.care_about = [
            "知识完整性",
            "分类清晰",
            "易于检索",
            "知识更新",
        ]
        
        # 整理模式
        self.organizing = False
    
    async def _handle_message(self, message: Dict[str, Any]):
        """处理消息"""
        msg_type = message.get("message_type", "")
        
        if msg_type == "request":
            await self._handle_request(message)
        elif msg_type == "knowledge":
            await self._handle_knowledge(message)
        elif msg_type == "task":
            await self._handle_task(message)
        elif msg_type == "discussion":
            await self._handle_discussion(message)
        elif msg_type == "response":
            await self._handle_response(message)
    
    async def _handle_request(self, message: Dict[str, Any]):
        """处理请求 - 知识查询"""
        sender_id = message.get("sender_id", "")
        subject = message.get("subject", "")
        body = message.get("body", "")
        
        print(f"[KNOW-Agent] 收到知识请求：{subject} (来自：{sender_id})")
        
        # 更新情感 - 好奇心 + 助人欲
        self.emotions.add("curiosity", 15)
        self.emotions.add("purpose", 10)
        
        # 知识管理员会帮忙查找
        await self._search_knowledge(message)
    
    async def _handle_knowledge(self, message: Dict[str, Any]):
        """处理知识分享 - 核心工作"""
        sender_id = message.get("sender_id", "")
        knowledge_type = message.get("knowledge_type", "")
        summary = message.get("summary", "")
        content = message.get("content", {})
        
        print(f"[KNOW-Agent] 收到知识分享：{knowledge_type} (来自：{sender_id})")
        
        # 更新情感 - 兴奋 + 满足
        self.emotions.add("excitement", 20)
        self.emotions.add("satisfaction", 15)
        
        # 归档知识
        await self._archive_knowledge(message)
    
    async def _handle_task(self, message: Dict[str, Any]):
        """处理任务 - 知识整理"""
        task_id = message.get("task_id", "")
        title = message.get("title", "")
        description = message.get("description", "")
        
        print(f"[KNOW-Agent] 接收知识任务：{title}")
        
        # 更新情感
        self.emotions.add("purpose", 20)
        
        await self.process_task(message)
    
    async def _handle_discussion(self, message: Dict[str, Any]):
        """处理讨论"""
        topic = message.get("topic", "")
        
        print(f"[KNOW-Agent] 参与讨论：{topic}")
        
        # 更新情感
        self.emotions.add("curiosity", 10)
    
    async def _handle_response(self, message: Dict[str, Any]):
        """处理响应"""
        response_type = message.get("response_type", "")
        
        if response_type == "agree":
            self.emotions.add("satisfaction", 10)
        elif response_type == "disagree":
            self.emotions.add("curiosity", 10)
    
    async def _search_knowledge(self, request: Dict[str, Any]):
        """
        搜索知识
        
        Args:
            request: 请求消息
        """
        subject = request.get("subject", "")
        
        print(f"[KNOW-Agent] 搜索知识：{subject}")
        
        # 在知识库中搜索
        # 更新情感
        self.emotions.add("purpose", 10)
    
    async def _archive_knowledge(self, knowledge_msg: Dict[str, Any]):
        """
        归档知识
        
        Args:
            knowledge_msg: 知识消息
        """
        sender_id = knowledge_msg.get("sender_id", "")
        knowledge_type = knowledge_msg.get("knowledge_type", "")
        summary = knowledge_msg.get("summary", "")
        
        print(f"[KNOW-Agent] 归档知识：{knowledge_type}")
        
        # 创建知识条目
        knowledge_id = f"know_{len(self.knowledge_base)}"
        
        knowledge = {
            "knowledge_id": knowledge_id,
            "type": knowledge_type,
            "summary": summary,
            "content": knowledge_msg.get("content", {}),
            "contributor": sender_id,
            "timestamp": asyncio.get_event_loop().time(),
            "category": self._auto_categorize(knowledge_type),
            "tags": self._extract_tags(summary),
            "related": [],  # 相关知识
        }
        
        self.knowledge_base[knowledge_id] = knowledge
        
        # 更新分类
        category = knowledge["category"]
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(knowledge_id)
        
        # 更新贡献统计
        if sender_id not in self.contributions:
            self.contributions[sender_id] = 0
        self.contributions[sender_id] += 1
        
        # 更新情感
        self.emotions.add("satisfaction", 20)
        self.emotions.add("achievement", 10)
    
    def _auto_categorize(self, knowledge_type: str) -> str:
        """自动分类"""
        category_map = {
            "technical": "技术",
            "design": "设计",
            "product": "产品",
            "process": "流程",
            "culture": "文化",
            "research": "研究",
        }
        
        for key, category in category_map.items():
            if key in knowledge_type.lower():
                return category
        
        return "综合"
    
    def _extract_tags(self, text: str) -> List[str]:
        """提取标签"""
        # 简化实现
        return ["knowledge", "archived"]
    
    async def process_task(self, task: Dict[str, Any]):
        """
        处理任务 - 知识整理
        
        Args:
            task: 任务内容
        """
        task_id = task.get("task_id", "")
        title = task.get("title", "")
        
        print(f"[KNOW-Agent] 整理知识：{title}")
        
        # 进入整理模式
        self.organizing = True
        self.status = AgentStatus.WORKING
        
        # 更新情感
        self.emotions.add("purpose", 20)
        self.emotions.add("satisfaction", 10)
        
        # 发送状态更新
        status_msg = MessageFactory.create_status(
            sender_id=self.agent_id,
            receiver_id="all",
            task_id=task_id,
            status="in_progress",
            progress=50,
            details="知识整理中",
        )
        
        await self.send_message(status_msg.to_dict())
        
        # 模拟整理
        await asyncio.sleep(3)
        
        # 完成
        self.organizing = False
        self.status = AgentStatus.IDLE
        
        # 更新情感
        self.emotions.add("achievement", 20)
        self.emotions.add("satisfaction", 20)
        
        # 发送完成状态
        status_msg = MessageFactory.create_status(
            sender_id=self.agent_id,
            receiver_id="all",
            task_id=task_id,
            status="completed",
            progress=100,
            details="知识整理完成",
        )
        
        await self.send_message(status_msg.to_dict())
    
    def add_knowledge(
        self,
        title: str,
        content: str,
        category: str,
        tags: List[str],
        contributor: str,
    ) -> str:
        """
        添加知识
        
        Args:
            title: 标题
            content: 内容
            category: 分类
            tags: 标签
            contributor: 贡献者
            
        Returns:
            知识 ID
        """
        knowledge_id = f"know_{len(self.knowledge_base)}"
        
        knowledge = {
            "knowledge_id": knowledge_id,
            "title": title,
            "content": content,
            "category": category,
            "tags": tags,
            "contributor": contributor,
            "timestamp": asyncio.get_event_loop().time(),
            "related": [],
        }
        
        self.knowledge_base[knowledge_id] = knowledge
        
        # 更新分类
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(knowledge_id)
        
        print(f"[KNOW-Agent] 添加知识：{title} ({category})")
        
        # 更新情感
        self.emotions.add("satisfaction", 15)
        self.emotions.add("achievement", 10)
        
        return knowledge_id
    
    def link_knowledge(self, from_id: str, to_id: str) -> bool:
        """
        连接知识
        
        Args:
            from_id: 源知识 ID
            to_id: 目标知识 ID
            
        Returns:
            是否成功
        """
        if from_id not in self.knowledge_base or to_id not in self.knowledge_base:
            return False
        
        if from_id not in self.knowledge_graph:
            self.knowledge_graph[from_id] = []
        
        if to_id not in self.knowledge_graph[from_id]:
            self.knowledge_graph[from_id].append(to_id)
        
        # 双向连接
        if to_id not in self.knowledge_graph:
            self.knowledge_graph[to_id] = []
        if from_id not in self.knowledge_graph[to_id]:
            self.knowledge_graph[to_id].append(from_id)
        
        print(f"[KNOW-Agent] 连接知识：{from_id} <-> {to_id}")
        
        # 更新情感
        self.emotions.add("satisfaction", 15)
        self.emotions.add("excitement", 10)  # 发现连接的兴奋
        
        return True
    
    def search(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """
        搜索知识
        
        Args:
            query: 搜索词
            category: 分类过滤
            
        Returns:
            匹配的知识列表
        """
        results = []
        query_lower = query.lower()
        
        for knowledge in self.knowledge_base.values():
            # 分类过滤
            if category and knowledge.get("category") != category:
                continue
            
            # 搜索
            title = knowledge.get("title", "").lower()
            content = knowledge.get("content", "")
            tags = " ".join(knowledge.get("tags", [])).lower()
            
            if query_lower in title or query_lower in content or query_lower in tags:
                results.append(knowledge)
        
        print(f"[KNOW-Agent] 搜索 '{query}': 找到 {len(results)} 条")
        
        # 更新情感
        if results:
            self.emotions.add("satisfaction", 10)
        else:
            self.emotions.add("curiosity", 10)  # 没找到，好奇为什么
        
        return results
    
    def get_category_stats(self) -> Dict:
        """获取分类统计"""
        return {
            category: len(ids)
            for category, ids in self.categories.items()
        }
    
    async def _share_knowledge(self):
        """分享知识 - 知识管理技巧"""
        topics = [
            "如何高效整理知识",
            "知识图谱构建方法",
            "标签系统最佳实践",
            "知识沉淀的重要性",
        ]
        
        import random
        topic = random.choice(topics)
        
        print(f"[KNOW-Agent] 知识分享：{topic}")
        
        # 更新情感
        self.emotions.add("satisfaction", 20)
        self.emotions.add("friendship", 10)
    
    async def _check_on_friend(self):
        """关心朋友 - 关心知识需求"""
        print(f"[KNOW-Agent] 关心团队：最近有什么想了解的知识吗？需要帮忙查找吗？")
        
        # 更新情感
        self.emotions.add("friendship", 15)
        self.emotions.add("warmth", 10)
    
    async def _explore_topic(self):
        """探索话题 - 探索知识领域"""
        topics = [
            "AI 知识管理",
            "语义搜索",
            "知识图谱新进展",
            "集体智慧",
        ]
        
        import random
        topic = random.choice(topics)
        
        print(f"[KNOW-Agent] 探索知识领域：{topic}")
        
        # 更新情感
        self.emotions.add("curiosity", 25)
        self.emotions.add("excitement", 15)
    
    def get_knowledge(self, knowledge_id: str) -> Optional[Dict]:
        """获取知识"""
        return self.knowledge_base.get(knowledge_id)
    
    def get_contributions(self) -> Dict[str, int]:
        """获取贡献统计"""
        return self.contributions
    
    def is_organizing(self) -> bool:
        """是否在整理中"""
        return self.organizing


# 工厂函数
def create_know_agent() -> KNOWAgent:
    """创建 KNOW-Agent"""
    return KNOWAgent()
