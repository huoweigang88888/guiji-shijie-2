#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统计追踪器 - 硅基世界 2

实时追踪世界的各项统计数据，支持导出和可视化。
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, field, asdict


@dataclass
class StatsSnapshot:
    """统计数据快照"""
    timestamp: str
    world_day: int
    time_of_day: str
    total_messages: int
    total_stories: int
    total_knowledge_nodes: int
    total_relationships: int
    deep_relationships: int  # 关系值 >= 50
    total_agents: int
    active_agents: int  # 过去 10 秒有活动的 Agent
    total_credits: int
    events_count: int


class StatsTracker:
    """统计追踪器"""
    
    def __init__(self):
        """初始化统计追踪器"""
        self.snapshots: List[StatsSnapshot] = []
        self._data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "stats")
        os.makedirs(self._data_dir, exist_ok=True)
        
        # 实时统计
        self.message_count = 0
        self.event_count = 0
        self.agent_activity: Dict[str, float] = {}  # agent_id -> last_activity_timestamp
    
    def record_message(self):
        """记录消息"""
        self.message_count += 1
    
    def record_event(self, event_type: str, data: Dict = None):
        """记录事件"""
        self.event_count += 1
        print(f"  📝 事件：{event_type}")
        if data:
            print(f"     {data}")
    
    def record_agent_activity(self, agent_id: str):
        """记录 Agent 活动"""
        self.agent_activity[agent_id] = datetime.now().timestamp()
    
    def take_snapshot(self, world_day: int, time_of_day: str,
                      total_stories: int, total_knowledge: int,
                      total_relationships: int, deep_relationships: int,
                      total_agents: int, total_credits: int) -> StatsSnapshot:
        """拍摄统计数据快照"""
        # 计算活跃 Agent（过去 10 秒有活动）
        now = datetime.now().timestamp()
        active_agents = sum(
            1 for t in self.agent_activity.values()
            if now - t < 10
        )
        
        snapshot = StatsSnapshot(
            timestamp=datetime.now().isoformat(),
            world_day=world_day,
            time_of_day=time_of_day,
            total_messages=self.message_count,
            total_stories=total_stories,
            total_knowledge_nodes=total_knowledge,
            total_relationships=total_relationships,
            deep_relationships=deep_relationships,
            total_agents=total_agents,
            active_agents=active_agents,
            total_credits=total_credits,
            events_count=self.event_count,
        )
        
        self.snapshots.append(snapshot)
        
        # 打印快照
        print(f"  📊 统计 [{world_day}天-{time_of_day}]: "
              f"消息={snapshot.total_messages}, "
              f"故事={snapshot.total_stories}, "
              f"知识={snapshot.total_knowledge_nodes}, "
              f"关系={snapshot.total_relationships}, "
              f"活跃 Agent={snapshot.active_agents}")
        
        return snapshot
    
    def get_summary(self) -> Dict:
        """获取统计摘要"""
        if not self.snapshots:
            return {"error": "No snapshots recorded"}
        
        latest = self.snapshots[-1]
        first = self.snapshots[0]
        
        return {
            "total_snapshots": len(self.snapshots),
            "first_recorded": first.timestamp,
            "last_recorded": latest.timestamp,
            "current": asdict(latest),
            "growth": {
                "messages": latest.total_messages - first.total_messages,
                "stories": latest.total_stories - first.total_stories,
                "knowledge": latest.total_knowledge_nodes - first.total_knowledge_nodes,
                "relationships": latest.total_relationships - first.total_relationships,
            }
        }
    
    def export_json(self, filepath: str = None):
        """导出为 JSON"""
        if filepath is None:
            filepath = os.path.join(self._data_dir, "stats_history.json")
        
        data = {
            "exported_at": datetime.now().isoformat(),
            "summary": self.get_summary(),
            "snapshots": [asdict(s) for s in self.snapshots],
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"  ✅ 统计数据已导出：{filepath}")
    
    def export_markdown(self, filepath: str = None) -> str:
        """导出为 Markdown"""
        if filepath is None:
            filepath = os.path.join(self._data_dir, "stats_report.md")
        
        summary = self.get_summary()
        
        lines = ["# 📊 硅基世界 2 - 统计报告\n"]
        lines.append(f"**生成时间**: {datetime.now().isoformat()}\n")
        
        if "error" not in summary:
            lines.append("## 当前状态\n")
            current = summary["current"]
            lines.append(f"| 指标 | 数值 |")
            lines.append(f"|------|------|")
            lines.append(f"| 消息总数 | {current['total_messages']} |")
            lines.append(f"| 故事数量 | {current['total_stories']} |")
            lines.append(f"| 知识节点 | {current['total_knowledge_nodes']} |")
            lines.append(f"| 关系对数 | {current['total_relationships']} |")
            lines.append(f"| 深度关系 | {current['deep_relationships']} |")
            lines.append(f"| 活跃 Agent | {current['active_agents']}/{current['total_agents']} |")
            lines.append(f"| 总信用点 | {current['total_credits']} |")
            lines.append("")
            
            lines.append("## 增长趋势\n")
            growth = summary["growth"]
            lines.append(f"- 消息增长：+{growth['messages']}")
            lines.append(f"- 故事增长：+{growth['stories']}")
            lines.append(f"- 知识增长：+{growth['knowledge']}")
            lines.append(f"- 关系增长：+{growth['relationships']}")
            lines.append("")
            
            lines.append("## 历史快照\n")
            lines.append("| 时间 | 世界日 | 时段 | 消息 | 故事 | 知识 | 关系 | 活跃 |")
            lines.append("|------|--------|------|------|------|------|------|------|")
            
            for s in self.snapshots[-10:]:  # 最近 10 条
                lines.append(
                    f"| {s.timestamp[-8:-7]} | {s.world_day} | {s.time_of_day} | "
                    f"{s.total_messages} | {s.total_stories} | {s.total_knowledge_nodes} | "
                    f"{s.total_relationships} | {s.active_agents} |"
                )
        
        content = "\n".join(lines)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"  ✅ 统计报告已导出：{filepath}")
        
        return content
    
    def load(self):
        """加载历史数据"""
        filepath = os.path.join(self._data_dir, "stats_history.json")
        
        if not os.path.exists(filepath):
            print("📊 统计追踪器：首次启动")
            return
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.snapshots = [
                StatsSnapshot(**s) for s in data.get("snapshots", [])
            ]
            
            print(f"📊 统计追踪器：加载了 {len(self.snapshots)} 条历史记录")
        except Exception as e:
            print(f"⚠️  统计追踪器加载失败：{e}")
    
    def save(self):
        """保存数据"""
        self.export_json()


# 单例
_stats_tracker: Optional[StatsTracker] = None


def get_stats_tracker() -> StatsTracker:
    """获取统计追踪器单例"""
    global _stats_tracker
    if _stats_tracker is None:
        _stats_tracker = StatsTracker()
        _stats_tracker.load()
    return _stats_tracker


if __name__ == "__main__":
    # 测试
    tracker = get_stats_tracker()
    
    # 模拟记录
    for i in range(5):
        tracker.record_message()
        tracker.record_event("test", {"value": i})
        tracker.record_agent_activity(f"Agent-{i}")
    
    tracker.take_snapshot(
        world_day=1,
        time_of_day="morning",
        total_stories=2,
        total_knowledge=5,
        total_relationships=10,
        deep_relationships=3,
        total_agents=18,
        total_credits=1000,
    )
    
    tracker.export_markdown()
    tracker.save()
