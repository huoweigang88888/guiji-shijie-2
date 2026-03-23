#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻系统 - 硅基世界 2

让 Agent 可以发布和阅读新闻，形成信息网络。
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class NewsCategory(Enum):
    """新闻分类"""
    WORLD = "world"          # 世界新闻
    TECHNOLOGY = "technology"  # 科技
    ECONOMY = "economy"      # 经济
    SOCIAL = "social"        # 社交
    ACHIEVEMENT = "achievement"  # 成就
    EVENT = "event"          # 事件


@dataclass
class News:
    """新闻"""
    news_id: str
    title: str
    content: str
    category: NewsCategory
    publisher: str
    published_at: float = field(default_factory=lambda: datetime.now().timestamp())
    views: int = 0
    likes: int = 0
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "news_id": self.news_id,
            "title": self.title,
            "content": self.content[:500],
            "category": self.category.value,
            "publisher": self.publisher,
            "published_at": self.published_at,
            "views": self.views,
            "likes": self.likes,
            "tags": self.tags,
        }


class NewsManager:
    """新闻管理器"""
    
    def __init__(self):
        """初始化新闻管理器"""
        self.news: Dict[str, News] = {}
        self._news_counter = 0
        
        print("📰 新闻系统已初始化")
    
    def publish(
        self,
        title: str,
        content: str,
        publisher: str,
        category: NewsCategory = NewsCategory.WORLD,
        tags: Optional[List[str]] = None,
    ) -> News:
        """
        发布新闻
        
        Args:
            title: 标题
            content: 内容
            publisher: 发布者
            category: 分类
            tags: 标签
            
        Returns:
            新闻对象
        """
        self._news_counter += 1
        
        news = News(
            news_id=f"news_{self._news_counter}",
            title=title,
            content=content,
            category=category,
            publisher=publisher,
            tags=tags or [],
        )
        
        self.news[news.news_id] = news
        
        print(f"  📰 {publisher} 发布新闻：{title}")
        
        return news
    
    def view(self, news_id: str) -> Optional[News]:
        """查看新闻"""
        if news_id not in self.news:
            return None
        
        news = self.news[news_id]
        news.views += 1
        
        return news
    
    def like(self, news_id: str) -> bool:
        """点赞新闻"""
        if news_id not in self.news:
            return False
        
        self.news[news_id].likes += 1
        return True
    
    def get_news(self, category: Optional[NewsCategory] = None, limit: int = 20) -> List[News]:
        """获取新闻"""
        news_list = list(self.news.values())
        
        if category:
            news_list = [n for n in news_list if n.category == category]
        
        # 按发布时间排序
        news_list.sort(key=lambda x: x.published_at, reverse=True)
        
        return news_list[:limit]
    
    def get_trending(self, limit: int = 10) -> List[News]:
        """获取热门新闻"""
        news_list = list(self.news.values())
        
        # 按热度排序（浏览量 + 点赞数）
        news_list.sort(key=lambda x: x.views + x.likes * 2, reverse=True)
        
        return news_list[:limit]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_news": len(self.news),
            "total_views": sum(n.views for n in self.news.values()),
            "total_likes": sum(n.likes for n in self.news.values()),
            "by_category": {
                cat.value: len([n for n in self.news.values() if n.category == cat])
                for cat in NewsCategory
            },
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "latest": [n.to_dict() for n in self.get_news(limit=5)],
            "trending": [n.to_dict() for n in self.get_trending(limit=5)],
        }


# 单例
_news_manager: Optional[NewsManager] = None


def get_news_manager() -> NewsManager:
    """获取新闻管理器单例"""
    global _news_manager
    if _news_manager is None:
        _news_manager = NewsManager()
    return _news_manager


# 工厂函数
def create_news_manager() -> NewsManager:
    """创建新闻管理器"""
    return NewsManager()
