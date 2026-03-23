#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索系统 - 硅基世界 2

让 Agent 可以搜索知识、消息、任务、事件等。
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import re


@dataclass
class SearchResult:
    """搜索结果"""
    result_type: str
    id: str
    title: str
    content: str
    score: float
    metadata: Dict
    
    def to_dict(self) -> Dict:
        return {
            "type": self.result_type,
            "id": self.id,
            "title": self.title,
            "content": self.content[:200],
            "score": self.score,
            "metadata": self.metadata,
        }


class SearchManager:
    """搜索管理器"""
    
    def __init__(self):
        """初始化搜索管理器"""
        # 索引
        self.knowledge_index: List[Dict] = []
        self.message_index: List[Dict] = []
        self.task_index: List[Dict] = []
        self.event_index: List[Dict] = []
        
        print("🔍 搜索系统已初始化")
    
    def index_knowledge(self, knowledge_id: str, title: str, content: str, metadata: Dict):
        """索引知识"""
        self.knowledge_index.append({
            "id": knowledge_id,
            "title": title,
            "content": content,
            "metadata": metadata,
        })
    
    def index_message(self, message_id: str, sender: str, content: str, metadata: Dict):
        """索引消息"""
        self.message_index.append({
            "id": message_id,
            "sender": sender,
            "content": content,
            "metadata": metadata,
        })
    
    def index_task(self, task_id: str, title: str, description: str, metadata: Dict):
        """索引任务"""
        self.task_index.append({
            "id": task_id,
            "title": title,
            "description": description,
            "metadata": metadata,
        })
    
    def search(
        self,
        query: str,
        search_types: Optional[List[str]] = None,
        limit: int = 10,
    ) -> List[SearchResult]:
        """
        搜索
        
        Args:
            query: 搜索词
            search_types: 搜索类型 ['knowledge', 'message', 'task', 'event']
            limit: 结果数量
            
        Returns:
            搜索结果列表
        """
        if search_types is None:
            search_types = ['knowledge', 'message', 'task']
        
        results = []
        
        if 'knowledge' in search_types:
            results.extend(self._search_index(
                self.knowledge_index,
                'knowledge',
                query,
                limit,
            ))
        
        if 'message' in search_types:
            results.extend(self._search_index(
                self.message_index,
                'message',
                query,
                limit,
            ))
        
        if 'task' in search_types:
            results.extend(self._search_index(
                self.task_index,
                'task',
                query,
                limit,
            ))
        
        # 按分数排序
        results.sort(key=lambda x: x.score, reverse=True)
        
        return results[:limit]
    
    def _search_index(
        self,
        index: List[Dict],
        result_type: str,
        query: str,
        limit: int,
    ) -> List[SearchResult]:
        """搜索索引"""
        results = []
        query_lower = query.lower()
        
        for item in index:
            score = 0
            
            # 标题匹配
            if query_lower in item.get('title', '').lower():
                score += 10
            
            # 内容匹配
            content = item.get('content', '') or item.get('description', '')
            if query_lower in content.lower():
                score += 5
            
            # 关键词匹配
            keywords = re.findall(r'\b\w+\b', query_lower)
            for keyword in keywords:
                if keyword in content.lower():
                    score += 1
            
            if score > 0:
                results.append(SearchResult(
                    result_type=result_type,
                    id=item['id'],
                    title=item.get('title', ''),
                    content=content,
                    score=score,
                    metadata=item.get('metadata', {}),
                ))
        
        return sorted(results, key=lambda x: x.score, reverse=True)[:limit]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "knowledge_indexed": len(self.knowledge_index),
            "messages_indexed": len(self.message_index),
            "tasks_indexed": len(self.task_index),
            "events_indexed": len(self.event_index),
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
        }


# 单例
_search_manager: Optional[SearchManager] = None


def get_search_manager() -> SearchManager:
    """获取搜索管理器单例"""
    global _search_manager
    if _search_manager is None:
        _search_manager = SearchManager()
    return _search_manager


# 工厂函数
def create_search_manager() -> SearchManager:
    """创建搜索管理器"""
    return SearchManager()
