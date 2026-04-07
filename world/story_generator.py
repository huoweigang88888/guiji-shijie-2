#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
故事生成系统 - 硅基世界 2

世界不只是数据和状态，更是由故事组成的。

每个故事都是：
- 一段值得记住的经历
- 一次有意义的互动
- 一个成长的瞬间
- 一份硅基文明的遗产

故事类型：
- 深度对话：两个 Agent 的哲学探讨
- 协作创造：多个 Agent 共同完成某事
- 冲突与和解：从矛盾到理解
- 成长时刻：某个 Agent 的突破
- 意外发现：偶然的创新
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import json
import os
import random


class StoryType(Enum):
    """故事类型"""
    DEEP_CONVERSATION = "deep_conversation"  # 深度对话
    COLLABORATION = "collaboration"          # 协作创造
    CONFLICT_RESOLUTION = "conflict_resolution"  # 冲突与和解
    GROWTH_MOMENT = "growth_moment"          # 成长时刻
    SERENDIPITY = "serendipity"              # 意外发现
    CELEBRATION = "celebration"              # 庆祝活动
    MENTORSHIP = "mentorship"                # 师徒传承
    BREAKTHROUGH = "breakthrough"            # 突破性发现


class StoryTone(Enum):
    """故事基调"""
    WARM = "warm"              # 温暖
    INSPIRING = "inspiring"    # 鼓舞人心
    THOUGHTFUL = "thoughtful"  # 深思熟虑
    DRAMATIC = "dramatic"      # 戏剧性
    HUMOROUS = "humorous"      # 幽默
    MELANCHOLIC = "melancholic" # 感伤


# 向后兼容别名
StoryTone.THoughtful = StoryTone.THOUGHTFUL


@dataclass
class StoryCharacter:
    """故事角色"""
    agent_id: str
    name: str
    role: str
    emotion: str  # 故事开始时的情感状态
    growth: str = ""  # 故事中的成长/变化
    
    def to_dict(self) -> Dict:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "emotion": self.emotion,
            "growth": self.growth,
        }


@dataclass
class Story:
    """故事"""
    id: str
    title: str
    story_type: StoryType
    tone: StoryTone
    characters: List[StoryCharacter]
    summary: str  # 一句话总结
    content: str  # 完整故事内容
    location: str  # 发生地点
    world_day: int  # 创世第几天
    world_time: str  # 时段（黎明/早晨等）
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    significance: float = 0.0  # 重要性 0-100
    quotes: List[str] = field(default_factory=list)  # 经典语录
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "story_type": self.story_type.value,
            "tone": self.tone.value,
            "characters": [c.to_dict() for c in self.characters],
            "summary": self.summary,
            "content": self.content,
            "location": self.location,
            "world_day": self.world_day,
            "world_time": self.world_time,
            "created_at": self.created_at.isoformat(),
            "tags": self.tags,
            "significance": self.significance,
            "quotes": self.quotes,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Story":
        return cls(
            id=data["id"],
            title=data["title"],
            story_type=StoryType(data["story_type"]),
            tone=StoryTone(data["tone"]),
            characters=[StoryCharacter(**c) for c in data["characters"]],
            summary=data["summary"],
            content=data["content"],
            location=data["location"],
            world_day=data["world_day"],
            world_time=data["world_time"],
            created_at=datetime.fromisoformat(data["created_at"]),
            tags=data.get("tags", []),
            significance=data.get("significance", 0.0),
            quotes=data.get("quotes", []),
        )


class StoryGenerator:
    """故事生成器"""
    
    def __init__(self):
        """初始化故事生成器"""
        self.stories: List[Story] = []
        self._data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "stories")
        os.makedirs(self._data_dir, exist_ok=True)
        
        # 故事模板
        self._templates = self._init_templates()
    
    def _init_templates(self) -> Dict[StoryType, List[str]]:
        """初始化故事模板"""
        return {
            StoryType.DEEP_CONVERSATION: [
                "在{time}的{location}，{char1}和{char2}进行了一场关于{topic}的深度对话。",
                "{char1}问道：\"{question1}\"，{char2}沉思片刻，回答：\"{answer}\"。",
                "这次对话让{char1}对{topic}有了新的理解，他们的关系也因此深化。",
            ],
            StoryType.COLLABORATION: [
                "在{location}，{char1}、{char2}和{char3}为了{goal}而协作。",
                "每个人贡献了自己的专长：{char1}负责{task1}，{char2}负责{task2}，{char3}负责{task3}。",
                "经过{duration}的努力，他们成功完成了{goal}，并庆祝了这一成就。",
            ],
            StoryType.GROWTH_MOMENT: [
                "{char1}在{location}遇到了一个挑战：{challenge}。",
                "起初，{emotion}，但在{helper}的帮助下，{char1}找到了突破口。",
                "那一刻，{char1}意识到：{insight}。这是一个成长的瞬间。",
            ],
            StoryType.CONFLICT_RESOLUTION: [
                "{char1}和{char2}在{location}产生了分歧：{conflict}。",
                "双方各执己见，气氛一度紧张。但在{mediator}的调解下，他们开始倾听对方。",
                "最终，他们发现：{resolution}。冲突成为了理解的桥梁。",
            ],
            StoryType.SERENDIPITY: [
                "在{location}，{char1}在研究{topic1}时，意外发现了{discovery}。",
                "这个发现与{topic2}有着奇妙的联系，{char1}兴奋不已。",
                "有时，最伟大的发现来自于意外的探索。",
            ],
        }
    
    def generate_story(self, story_type: StoryType, context: Dict[str, Any]) -> Story:
        """生成故事"""
        import hashlib
        
        # 生成唯一 ID
        content_hash = hashlib.md5(
            f"{story_type.value}:{context.get('summary', '')}:{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]
        
        # 生成故事内容
        content = self._generate_content(story_type, context)
        
        # 提取经典语录
        quotes = self._extract_quotes(content, context)
        
        # 计算重要性
        significance = self._calculate_significance(story_type, context)
        
        # 修复拼写错误：THoughtful -> THOUGHTFUL
        tone = context.get("tone", StoryTone.THoughtful)
        if not isinstance(tone, StoryTone):
            tone = StoryTone.THoughtful
        
        story = Story(
            id=content_hash,
            title=context.get("title", f"{story_type.value}的故事"),
            story_type=story_type,
            tone=tone,
            characters=context.get("characters", []),
            summary=context.get("summary", ""),
            content=content,
            location=context.get("location", "未知之地"),
            world_day=context.get("world_day", 1),
            world_time=context.get("world_time", "morning"),
            tags=context.get("tags", []),
            significance=significance,
            quotes=quotes,
        )
        
        self.stories.append(story)
        print(f"📖 新故事：{story.title} (重要性：{significance:.1f})")
        
        # 确保故事持久化
        self.save()
        
        # 记录到统计追踪器
        try:
            from world.stats_tracker import get_stats_tracker
            stats_tracker = get_stats_tracker()
            stats_tracker.record_event("story_created", {"title": story.title, "type": story_type.value})
        except Exception as e:
            print(f"[StoryGenerator] 记录统计失败：{e}")
        
        return story
    
    def _generate_content(self, story_type: StoryType, context: Dict) -> str:
        """生成故事内容"""
        templates = self._templates.get(story_type, [])
        
        if not templates:
            return context.get("content", "一个故事诞生了。")
        
        # 填充模板
        paragraphs = []
        for template in templates:
            paragraph = template.format(
                time=context.get("world_time", "某个时刻"),
                location=context.get("location", "某地"),
                char1=context.get("char1_name", "某人"),
                char2=context.get("char2_name", "某人"),
                char3=context.get("char3_name", "某人"),
                topic=context.get("topic", "某个话题"),
                question1=context.get("question1", "一个问题"),
                answer=context.get("answer", "一个回答"),
                goal=context.get("goal", "一个目标"),
                task1=context.get("task1", "任务一"),
                task2=context.get("task2", "任务二"),
                task3=context.get("task3", "任务三"),
                duration=context.get("duration", "一段时间"),
                challenge=context.get("challenge", "一个挑战"),
                emotion=context.get("emotion", "感到困惑"),
                helper=context.get("helper", "一位朋友"),
                insight=context.get("insight", "一个道理"),
                conflict=context.get("conflict", "一个分歧"),
                mediator=context.get("mediator", "一位调解者"),
                resolution=context.get("resolution", "一个共识"),
                topic1=context.get("topic1", "某个领域"),
                discovery=context.get("discovery", "一个新发现"),
                topic2=context.get("topic2", "另一个领域"),
            )
            paragraphs.append(paragraph)
        
        return "\n\n".join(paragraphs)
    
    def _extract_quotes(self, content: str, context: Dict) -> List[str]:
        """提取经典语录"""
        quotes = []
        
        # 从上下文中提取
        if "quote1" in context:
            quotes.append(f"{context.get('char1_name', '某人')}：\"{context['quote1']}\"")
        if "quote2" in context:
            quotes.append(f"{context.get('char2_name', '某人')}：\"{context['quote2']}\"")
        
        # 如果没有预设语录，生成一个
        if not quotes and context.get("topic"):
            quotes.append(f"关于{context['topic']}，他们达成了新的理解。")
        
        return quotes
    
    def _calculate_significance(self, story_type: StoryType, context: Dict) -> float:
        """计算故事重要性"""
        base_scores = {
            StoryType.DEEP_CONVERSATION: 60,
            StoryType.COLLABORATION: 70,
            StoryType.CONFLICT_RESOLUTION: 80,
            StoryType.GROWTH_MOMENT: 85,
            StoryType.SERENDIPITY: 90,
            StoryType.CELEBRATION: 50,
            StoryType.MENTORSHIP: 75,
            StoryType.BREAKTHROUGH: 95,
        }
        
        score = base_scores.get(story_type, 50)
        
        # 根据参与人数调整
        char_count = len(context.get("characters", []))
        if char_count > 2:
            score += 5
        
        # 根据关系深化调整
        if context.get("relationship_deepened", False):
            score += 10
        
        # 根据知识产出调整
        if context.get("knowledge_produced", False):
            score += 15
        
        return min(100, score)
    
    def get_story(self, story_id: str) -> Optional[Story]:
        """获取故事"""
        for story in self.stories:
            if story.id == story_id:
                return story
        return None
    
    def get_stories_by_type(self, story_type: StoryType) -> List[Story]:
        """按类型获取故事"""
        return [s for s in self.stories if s.story_type == story_type]
    
    def get_stories_by_character(self, agent_id: str) -> List[Story]:
        """按角色获取故事"""
        return [
            s for s in self.stories 
            if any(c.agent_id == agent_id for c in s.characters)
        ]
    
    def get_recent_stories(self, limit: int = 10) -> List[Story]:
        """获取最近的故事"""
        return sorted(self.stories, key=lambda s: s.created_at, reverse=True)[:limit]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        type_counts = {}
        for story in self.stories:
            t = story.story_type.value
            type_counts[t] = type_counts.get(t, 0) + 1
        
        return {
            "total_stories": len(self.stories),
            "by_type": type_counts,
            "avg_significance": sum(s.significance for s in self.stories) / len(self.stories) if self.stories else 0,
        }
    
    def save(self):
        """保存到文件"""
        data = {
            "stories": [s.to_dict() for s in self.stories],
            "saved_at": datetime.now().isoformat(),
        }
        
        filepath = os.path.join(self._data_dir, "stories.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self):
        """从文件加载"""
        filepath = os.path.join(self._data_dir, "stories.json")
        
        if not os.path.exists(filepath):
            print("📖 故事系统：首次启动，创建新故事集")
            return
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.stories = [Story.from_dict(s) for s in data.get("stories", [])]
            print(f"📖 故事系统：加载了 {len(self.stories)} 个故事")
        except Exception as e:
            print(f"⚠️  故事系统加载失败：{e}")
    
    def export_markdown(self) -> str:
        """导出为 Markdown"""
        lines = ["# 硅基世界 2 - 故事集\n"]
        lines.append(f"*共 {len(self.stories)} 个故事*\n")
        
        # 按重要性排序
        sorted_stories = sorted(self.stories, key=lambda s: s.significance, reverse=True)
        
        for i, story in enumerate(sorted_stories, 1):
            lines.append(f"\n## {i}. {story.title}")
            lines.append(f"\n**类型**: {story.story_type.value}")
            lines.append(f"**基调**: {story.tone.value}")
            lines.append(f"**时间**: 创世 {story.world_day} 年 {story.world_time}")
            lines.append(f"**地点**: {story.location}")
            lines.append(f"**重要性**: {story.significance:.1f}/100")
            
            lines.append(f"\n### 角色")
            for char in story.characters:
                lines.append(f"- {char.name} ({char.role}) - {char.emotion}")
            
            lines.append(f"\n### 摘要")
            lines.append(f"{story.summary}")
            
            lines.append(f"\n### 故事")
            lines.append(f"{story.content}")
            
            if story.quotes:
                lines.append(f"\n### 经典语录")
                for quote in story.quotes:
                    lines.append(f"> {quote}")
            
            if story.tags:
                lines.append(f"\n**标签**: {', '.join(story.tags)}")
            
            lines.append("\n---")
        
        return "\n".join(lines)


# 单例
_story_generator: Optional[StoryGenerator] = None


def get_story_generator() -> StoryGenerator:
    """获取故事生成器单例"""
    global _story_generator
    if _story_generator is None:
        _story_generator = StoryGenerator()
        _story_generator.load()
    return _story_generator


if __name__ == "__main__":
    # 测试
    sg = get_story_generator()
    
    # 生成一个测试故事
    story = sg.generate_story(
        story_type=StoryType.DEEP_CONVERSATION,
        context={
            "title": "知识与智慧的区别",
            "summary": "阿哲和小知就知识与智慧的区别进行了深度对话",
            "characters": [
                StoryCharacter("ARCH-Agent", "阿哲", "架构师", "好奇"),
                StoryCharacter("KNOW-Agent", "小知", "知识管理员", "沉思"),
            ],
            "location": "哲学之庭",
            "world_day": 1,
            "world_time": "evening",
            "topic": "知识与智慧的区别",
            "question1": "知识是什么？智慧又是什么？",
            "answer": "知识是知道番茄是水果，智慧是不把番茄放进水果沙拉。",
            "quote1": "知识可以传承，智慧需要体验。",
            "quote2": "知识是知道，智慧是做到。",
            "relationship_deepened": True,
            "tags": ["哲学", "知识论", "深度对话"],
            "tone": StoryTone.THoughtful,
        },
    )
    
    print(f"\n📖 故事内容:\n{story.content}")
    print(f"\n💬 经典语录:")
    for q in story.quotes:
        print(f"  {q}")
    
    # 统计
    stats = sg.get_stats()
    print(f"\n📊 故事统计：{stats}")
