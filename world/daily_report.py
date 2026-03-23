#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界日报 - 硅基世界 2

每天生成一份世界日报，记录这一天发生的故事。
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


class DailyReport:
    """世界日报"""
    
    def __init__(self, reports_dir: str = "reports"):
        """
        初始化日报
        
        Args:
            reports_dir: 报告目录
        """
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(exist_ok=True)
        
        self.current_report: Dict = {}
    
    def start_day(self, day: int):
        """
        开始新的一天
        
        Args:
            day: 天数
        """
        self.current_report = {
            "day": day,
            "date": datetime.now().isoformat(),
            "events": [],
            "stories": [],
            "conflicts": [],
            "achievements": [],
            "knowledge_added": 0,
            "messages_count": 0,
            "active_agents": set(),
        }
        
        print(f"📰 Day {day} 的日报开始记录")
    
    def log_event(self, event_type: str, description: str, agents: Optional[List[str]] = None):
        """
        记录事件
        
        Args:
            event_type: 事件类型
            description: 描述
            agents: 涉及的 Agent
        """
        event = {
            "type": event_type,
            "description": description,
            "agents": agents or [],
            "timestamp": datetime.now().isoformat(),
        }
        
        self.current_report["events"].append(event)
        
        if agents:
            for agent in agents:
                self.current_report["active_agents"].add(agent)
    
    def log_story(self, story: Dict):
        """记录故事"""
        self.current_report["stories"].append(story)
        
        if "participants" in story:
            for agent in story["participants"]:
                self.current_report["active_agents"].add(agent)
    
    def log_conflict(self, conflict: Dict):
        """记录冲突"""
        self.current_report["conflicts"].append(conflict)
        
        if "agents" in conflict:
            for agent in conflict["agents"]:
                self.current_report["active_agents"].add(agent)
    
    def log_achievement(self, achievement: Dict):
        """记录成就"""
        self.current_report["achievements"].append(achievement)
        
        if "agent_id" in achievement:
            self.current_report["active_agents"].add(achievement["agent_id"])
    
    def increment_messages(self, count: int = 1):
        """增加消息计数"""
        self.current_report["messages_count"] += count
    
    def increment_knowledge(self, count: int = 1):
        """增加知识计数"""
        self.current_report["knowledge_added"] += count
    
    def end_day(self) -> str:
        """
        结束一天，生成日报
        
        Returns:
            报告文件路径
        """
        day = self.current_report.get("day", 0)
        
        # 生成报告内容
        report_content = self._generate_report()
        
        # 保存文件
        report_path = self.reports_dir / f"day_{day}_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📰 Day {day} 的日报已生成：{report_path}")
        
        # 重置
        self.current_report = {}
        
        return str(report_path)
    
    def _generate_report(self) -> str:
        """生成报告内容"""
        day = self.current_report.get("day", 0)
        date = self.current_report.get("date", "")
        
        # 标题
        content = f"""# 硅基世界 2 - 创世元年 Day {day}

**日期**: {date}

---

## 📊 今日概览

| 指标 | 数值 |
|------|------|
| 👥 活跃 Agent | {len(self.current_report.get('active_agents', set()))} |
| 💬 消息数量 | {self.current_report.get('messages_count', 0)} |
| 📚 新增知识 | {self.current_report.get('knowledge_added', 0)} |
| 📖 诞生故事 | {len(self.current_report.get('stories', []))} |
| ⚡ 发生冲突 | {len(self.current_report.get('conflicts', []))} |
| 🏆 解锁成就 | {len(self.current_report.get('achievements', []))} |

---

## 👥 活跃 Agent

"""
        
        # 活跃 Agent
        for agent in sorted(self.current_report.get('active_agents', set())):
            content += f"- {agent}\n"
        
        content += "\n---\n\n"
        
        # 今日故事
        stories = self.current_report.get('stories', [])
        if stories:
            content += "## 📖 今日故事\n\n"
            for story in stories:
                content += f"### {story.get('title', 'Untitled')}\n\n"
                content += f"{story.get('summary', '')}\n\n"
                content += f"**参与者**: {', '.join(story.get('participants', []))}\n\n"
                content += "---\n\n"
        else:
            content += "## 📖 今日故事\n\n今天没有新的故事诞生...\n\n---\n\n"
        
        # 冲突与和解
        conflicts = self.current_report.get('conflicts', [])
        if conflicts:
            content += "## ⚡ 冲突与和解\n\n"
            for conflict in conflicts:
                status_emoji = "🔥" if conflict.get('status') == 'escalated' else "🤝"
                content += f"{status_emoji} **{conflict.get('topic', '')}**\n\n"
                content += f"{conflict.get('description', '')}\n\n"
                if conflict.get('resolution'):
                    content += f"**解决方式**: {conflict.get('resolution')}\n\n"
                content += "---\n\n"
        else:
            content += "## ⚡ 冲突与和解\n\n今天没有发生冲突，和平的一天！\n\n---\n\n"
        
        # 成就
        achievements = self.current_report.get('achievements', [])
        if achievements:
            content += "## 🏆 今日成就\n\n"
            for ach in achievements:
                rarity_emoji = {
                    "common": "⚪",
                    "uncommon": "🟢",
                    "rare": "🔵",
                    "epic": "🟣",
                    "legendary": "🟡",
                }.get(ach.get('rarity', 'common'), "⚪")
                
                content += f"{rarity_emoji} **{ach.get('name', '')}** - {ach.get('agent_id', '')}\n\n"
                content += f"{ach.get('description', '')}\n\n"
            content += "---\n\n"
        else:
            content += "## 🏆 今日成就\n\n今天没有新成就解锁...\n\n---\n\n"
        
        # 重要事件
        events = self.current_report.get('events', [])
        if events:
            content += "## 📜 重要事件\n\n"
            for event in events[:10]:  # 最多显示 10 个
                content += f"- **{event.get('type', '')}**: {event.get('description', '')}\n"
            content += "\n---\n\n"
        
        # 结语
        content += f"""## 💭 结语

Day {day} 结束了。

"""
        
        if stories:
            content += f"今天诞生了 {len(stories)} 个故事，"
        if conflicts:
            content += f"经历了 {len(conflicts)} 次冲突与和解，"
        if achievements:
            content += f"见证了 {len(achievements)} 个成就的解锁。"
        
        content += "\n\n明天，硅基世界将继续演化...\n\n"
        content += "---\n\n"
        content += "*硅基世界 2 | 创世元年*\n"
        
        return content
    
    def get_report(self, day: int) -> Optional[str]:
        """
        获取指定天数的报告
        
        Args:
            day: 天数
            
        Returns:
            报告内容
        """
        report_path = self.reports_dir / f"day_{day}_report.md"
        
        if report_path.exists():
            with open(report_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        return None
    
    def list_reports(self) -> List[int]:
        """列出所有报告的天数"""
        reports = []
        
        for file in self.reports_dir.glob("day_*_report.md"):
            try:
                day = int(file.stem.split('_')[1])
                reports.append(day)
            except (ValueError, IndexError):
                continue
        
        return sorted(reports)


# 单例
_daily_report: Optional[DailyReport] = None


def get_daily_report(reports_dir: str = "reports") -> DailyReport:
    """获取日报单例"""
    global _daily_report
    if _daily_report is None:
        _daily_report = DailyReport(reports_dir)
    return _daily_report


# 工厂函数
def create_daily_report(reports_dir: str = "reports") -> DailyReport:
    """创建日报"""
    return DailyReport(reports_dir)
