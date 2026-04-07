#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识分享场景 - 硅基世界 2

Agent 之间分享知识、经验和技能，促进共同成长。
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class KnowledgeType(Enum):
    """知识类型"""
    TUTORIAL = "tutorial"           # 教程
    BEST_PRACTICE = "best_practice" # 最佳实践
    TIP_TRICK = "tip_trick"         # 技巧提示
    CASE_STUDY = "case_study"       # 案例研究
    RESEARCH = "research"           # 研究成果
    DOCUMENTATION = "documentation" # 文档


class SharingFormat(Enum):
    """分享格式"""
    TEXT = "text"           # 文本
    CODE_SNIPPET = "code"   # 代码片段
    DIAGRAM = "diagram"     # 图表
    VIDEO = "video"         # 视频链接
    ARTICLE = "article"     # 文章链接


@dataclass
class KnowledgeShare:
    """知识分享"""
    share_id: str
    title: str
    content: str
    knowledge_type: KnowledgeType
    author: str
    tags: List[str] = field(default_factory=list)
    format: SharingFormat = SharingFormat.TEXT
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    views: int = 0
    likes: int = 0
    comments: List[Dict] = field(default_factory=list)
    related_shares: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "share_id": self.share_id,
            "title": self.title,
            "content": self.content,
            "knowledge_type": self.knowledge_type.value,
            "author": self.author,
            "tags": self.tags,
            "format": self.format.value,
            "created_at": self.created_at,
            "views": self.views,
            "likes": self.likes,
            "comments": self.comments,
            "related_shares": self.related_shares,
        }


class KnowledgeShareManager:
    """知识分享管理器"""
    
    def __init__(self):
        """初始化知识分享管理器"""
        self.shares: Dict[str, KnowledgeShare] = {}
        self._share_counter = 0
        
        # 知识分类
        self.knowledge_categories = {
            "technical": "技术知识",
            "process": "流程方法",
            "soft_skill": "软技能",
            "domain": "领域知识",
            "tool": "工具使用",
        }
    
    async def create_share(
        self,
        title: str,
        content: str,
        author: str,
        knowledge_type: KnowledgeType,
        tags: Optional[List[str]] = None,
        share_format: SharingFormat = SharingFormat.TEXT,
    ) -> KnowledgeShare:
        """
        创建知识分享
        
        Args:
            title: 标题
            content: 内容
            author: 作者
            knowledge_type: 知识类型
            tags: 标签列表
            share_format: 分享格式
            
        Returns:
            知识分享对象
        """
        self._share_counter += 1
        
        share = KnowledgeShare(
            share_id=f"knowledge_{self._share_counter}",
            title=title,
            content=content,
            knowledge_type=knowledge_type,
            author=author,
            tags=tags or [],
            format=share_format,
        )
        
        self.shares[share.share_id] = share
        
        print(f"📚 知识分享：{title}")
        print(f"   作者：{author}")
        print(f"   类型：{knowledge_type.value}")
        print(f"   标签：{', '.join(tags) if tags else '无'}")
        
        return share
    
    async def view_share(self, share_id: str) -> bool:
        """查看知识分享"""
        if share_id not in self.shares:
            return False
        
        share = self.shares[share_id]
        share.views += 1
        
        return True
    
    async def like_share(self, share_id: str, agent_id: str) -> bool:
        """点赞知识分享"""
        if share_id not in self.shares:
            return False
        
        share = self.shares[share_id]
        share.likes += 1
        
        print(f"👍 {agent_id} 点赞了：{share.title}")
        
        return True
    
    async def add_comment(self, share_id: str, agent_id: str, comment: str) -> bool:
        """添加评论"""
        if share_id not in self.shares:
            return False
        
        share = self.shares[share_id]
        share.comments.append({
            "agent_id": agent_id,
            "comment": comment,
            "timestamp": datetime.now().timestamp(),
        })
        
        print(f"💬 {agent_id}: {comment}")
        
        return True
    
    async def link_shares(self, share_id: str, related_share_id: str) -> bool:
        """关联相关知识分享"""
        if share_id not in self.shares or related_share_id not in self.shares:
            return False
        
        share = self.shares[share_id]
        if related_share_id not in share.related_shares:
            share.related_shares.append(related_share_id)
        
        return True
    
    def search_shares(self, query: str, tag: Optional[str] = None) -> List[KnowledgeShare]:
        """搜索知识分享"""
        results = []
        for share in self.shares.values():
            match = (
                query.lower() in share.title.lower() or
                query.lower() in share.content.lower()
            )
            if tag:
                match = match and tag in share.tags
            
            if match:
                results.append(share)
        
        return results
    
    def get_by_author(self, author: str) -> List[KnowledgeShare]:
        """获取作者的知识分享"""
        return [s for s in self.shares.values() if s.author == author]
    
    def get_popular_shares(self, limit: int = 10) -> List[KnowledgeShare]:
        """获取热门知识分享"""
        sorted_shares = sorted(self.shares.values(), key=lambda s: s.likes, reverse=True)
        return sorted_shares[:limit]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total_views = sum(s.views for s in self.shares.values())
        total_likes = sum(s.likes for s in self.shares.values())
        
        return {
            "total": len(self.shares),
            "total_views": total_views,
            "total_likes": total_likes,
            "by_type": {
                t.value: len([s for s in self.shares.values() if s.knowledge_type == t])
                for t in KnowledgeType
            },
        }


# 单例
_knowledge_share_manager: Optional[KnowledgeShareManager] = None


def get_knowledge_share_manager() -> KnowledgeShareManager:
    """获取知识分享管理器单例"""
    global _knowledge_share_manager
    if _knowledge_share_manager is None:
        _knowledge_share_manager = KnowledgeShareManager()
    return _knowledge_share_manager


def create_knowledge_share_manager() -> KnowledgeShareManager:
    """创建知识分享管理器"""
    return KnowledgeShareManager()
