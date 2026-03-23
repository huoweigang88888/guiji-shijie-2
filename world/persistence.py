#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据持久化 - 硅基世界 2

保存世界的状态、历史、故事，让世界不会"失忆"。
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class WorldPersistence:
    """世界持久化"""
    
    def __init__(self, data_dir: str = "data"):
        """
        初始化持久化
        
        Args:
            data_dir: 数据目录
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # 数据文件路径
        self.world_state_file = self.data_dir / "world_state.json"
        self.events_file = self.data_dir / "events.jsonl"
        self.stories_file = self.data_dir / "stories.jsonl"
        self.relationships_file = self.data_dir / "relationships.json"
        self.knowledge_file = self.data_dir / "knowledge.jsonl"
        
        # 内存缓存
        self.world_state: Dict = {}
        self.events: List[Dict] = []
        self.stories: List[Dict] = []
        self.relationships: Dict = {}
        self.knowledge: List[Dict] = []
        
        print(f"💾 数据持久化已初始化：{self.data_dir.absolute()}")
    
    async def load(self):
        """加载数据"""
        print("💾 加载世界数据...")
        
        # 加载世界状态
        if self.world_state_file.exists():
            with open(self.world_state_file, 'r', encoding='utf-8') as f:
                self.world_state = json.load(f)
            print(f"  ✓ 世界状态已加载")
        
        # 加载事件
        if self.events_file.exists():
            with open(self.events_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        self.events.append(json.loads(line))
            print(f"  ✓ 事件历史已加载 ({len(self.events)} 条)")
        
        # 加载故事
        if self.stories_file.exists():
            with open(self.stories_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        self.stories.append(json.loads(line))
            print(f"  ✓ 故事已加载 ({len(self.stories)} 个)")
        
        # 加载关系
        if self.relationships_file.exists():
            with open(self.relationships_file, 'r', encoding='utf-8') as f:
                self.relationships = json.load(f)
            print(f"  ✓ 关系已加载 ({len(self.relationships)} 对)")
        
        # 加载知识
        if self.knowledge_file.exists():
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        self.knowledge.append(json.loads(line))
            print(f"  ✓ 知识已加载 ({len(self.knowledge)} 条)")
    
    async def save(self):
        """保存数据"""
        print("💾 保存世界数据...")
        
        # 保存世界状态
        with open(self.world_state_file, 'w', encoding='utf-8') as f:
            json.dump(self.world_state, f, ensure_ascii=False, indent=2)
        print(f"  ✓ 世界状态已保存")
        
        # 保存关系（JSON）
        with open(self.relationships_file, 'w', encoding='utf-8') as f:
            json.dump(self.relationships, f, ensure_ascii=False, indent=2)
        print(f"  ✓ 关系已保存")
    
    async def append_event(self, event: Dict):
        """
        追加事件
        
        Args:
            event: 事件数据
        """
        self.events.append(event)
        
        # 追加到文件
        with open(self.events_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event, ensure_ascii=False) + '\n')
    
    async def append_story(self, story: Dict):
        """
        追加故事
        
        Args:
            story: 故事数据
        """
        self.stories.append(story)
        
        # 追加到文件
        with open(self.stories_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(story, ensure_ascii=False) + '\n')
        
        print(f"📖 新故事已保存：{story.get('title', 'Untitled')}")
    
    async def append_knowledge(self, knowledge: Dict):
        """
        追加知识
        
        Args:
            knowledge: 知识数据
        """
        self.knowledge.append(knowledge)
        
        # 追加到文件
        with open(self.knowledge_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(knowledge, ensure_ascii=False) + '\n')
    
    def update_relationships(self, relationships: Dict):
        """
        更新关系
        
        Args:
            relationships: 关系数据
        """
        self.relationships = relationships
    
    def update_world_state(self, state: Dict):
        """
        更新世界状态
        
        Args:
            state: 世界状态
        """
        self.world_state = state
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "events": len(self.events),
            "stories": len(self.stories),
            "relationships": len(self.relationships),
            "knowledge": len(self.knowledge),
        }
    
    def get_recent_events(self, limit: int = 20) -> List[Dict]:
        """获取最近事件"""
        return self.events[-limit:]
    
    def get_all_stories(self) -> List[Dict]:
        """获取所有故事"""
        return self.stories
    
    def get_relationships(self) -> Dict:
        """获取关系"""
        return self.relationships
    
    def get_knowledge(self, limit: int = 50) -> List[Dict]:
        """获取知识"""
        return self.knowledge[-limit:]
    
    def export_world_archive(self, output_path: str) -> str:
        """
        导出世界档案
        
        Args:
            output_path: 输出路径
            
        Returns:
            输出文件路径
        """
        archive = {
            "exported_at": datetime.now().isoformat(),
            "world_state": self.world_state,
            "events": self.events,
            "stories": self.stories,
            "relationships": self.relationships,
            "knowledge": self.knowledge,
        }
        
        output = Path(output_path)
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(archive, f, ensure_ascii=False, indent=2)
        
        print(f"📦 世界档案已导出：{output}")
        
        return str(output)


# 单例
_persistence: Optional[WorldPersistence] = None


def get_persistence(data_dir: str = "data") -> WorldPersistence:
    """获取持久化单例"""
    global _persistence
    if _persistence is None:
        _persistence = WorldPersistence(data_dir)
    return _persistence


# 工厂函数
def create_persistence(data_dir: str = "data") -> WorldPersistence:
    """创建持久化"""
    return WorldPersistence(data_dir)
