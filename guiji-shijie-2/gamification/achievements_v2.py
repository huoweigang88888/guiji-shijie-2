#!/usr/bin/env python3
"""
成就系统扩展 - Phase 10
新增 20+ 成就类别
"""

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from datetime import datetime
from typing import Dict, List, Any
from enum import Enum


class AchievementCategory(Enum):
    NEWBIE = "新手上路"
    SOCIAL = "社交达人"
    WORK = "工作狂人"
    EXPLORER = "探索者"
    CREATOR = "创造者"
    ECONOMY = "经济大师"
    SPECIAL = "特殊成就"


class Achievement:
    def __init__(self, id: str, name: str, description: str, category: AchievementCategory, 
                 points: int = 10, requirement: int = 1, icon: str = "🏆"):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.points = points
        self.requirement = requirement
        self.icon = icon
        self.rarity = self._calculate_rarity(points)
    
    def _calculate_rarity(self, points: int) -> str:
        if points >= 100: return "传说"
        elif points >= 50: return "史诗"
        elif points >= 20: return "稀有"
        else: return "普通"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category.value,
            'points': self.points,
            'requirement': self.requirement,
            'icon': self.icon,
            'rarity': self.rarity
        }


class AchievementSystem:
    def __init__(self):
        self.achievements: Dict[str, Achievement] = {}
        self.user_achievements: Dict[str, List[str]] = {}
        self._initialize_achievements()
    
    def _initialize_achievements(self):
        # 新手上路 (5 个)
        self._add(Achievement("newbie_1", "初次见面", "首次登录硅基世界", AchievementCategory.NEWBIE, 10, 1, "👋"))
        self._add(Achievement("newbie_2", "探索开始", "创建第一个 Agent", AchievementCategory.NEWBIE, 20, 1, "🤖"))
        self._add(Achievement("newbie_3", "任务新手", "完成第一个任务", AchievementCategory.NEWBIE, 15, 1, "📝"))
        self._add(Achievement("newbie_4", "社交新手", "添加第一个好友", AchievementCategory.NEWBIE, 15, 1, "👥"))
        self._add(Achievement("newbie_5", "完美开局", "一天内完成 5 个新手成就", AchievementCategory.NEWBIE, 50, 5, "🌟"))
        
        # 社交达人 (5 个)
        self._add(Achievement("social_1", "人气王", "拥有 10 个好友", AchievementCategory.SOCIAL, 30, 10, "⭐"))
        self._add(Achievement("social_2", "社交明星", "拥有 50 个好友", AchievementCategory.SOCIAL, 50, 50, "🌟"))
        self._add(Achievement("social_3", "话痨", "发送 100 条消息", AchievementCategory.SOCIAL, 30, 100, "💬"))
        self._add(Achievement("social_4", "群主", "创建 10 个群组", AchievementCategory.SOCIAL, 40, 10, "👨‍👩‍👧‍👦"))
        self._add(Achievement("social_5", "社交之王", "拥有 100 个好友", AchievementCategory.SOCIAL, 100, 100, "👑"))
        
        # 工作狂人 (5 个)
        self._add(Achievement("work_1", "勤劳", "完成 10 个任务", AchievementCategory.WORK, 20, 10, "🐝"))
        self._add(Achievement("work_2", "高效", "一天完成 20 个任务", AchievementCategory.WORK, 40, 20, "⚡"))
        self._add(Achievement("work_3", "完美主义", "任务 100% 成功率", AchievementCategory.WORK, 50, 100, "💯"))
        self._add(Achievement("work_4", "工作狂", "完成 100 个任务", AchievementCategory.WORK, 60, 100, "💼"))
        self._add(Achievement("work_5", "传奇工作者", "完成 1000 个任务", AchievementCategory.WORK, 100, 1000, "🏅"))
        
        # 探索者 (5 个)
        self._add(Achievement("explore_1", "好奇心", "访问 5 个不同页面", AchievementCategory.EXPLORER, 15, 5, "🔍"))
        self._add(Achievement("explore_2", "冒险家", "访问 20 个不同页面", AchievementCategory.EXPLORER, 30, 20, "🗺️"))
        self._add(Achievement("explore_3", "2D 世界探索", "在 2D 世界停留 1 小时", AchievementCategory.EXPLORER, 25, 1, "🌐"))
        self._add(Achievement("explore_4", "功能探索者", "使用 10 个不同功能", AchievementCategory.EXPLORER, 35, 10, "🔬"))
        self._add(Achievement("explore_5", "全知者", "体验所有功能", AchievementCategory.EXPLORER, 100, 1, "👁️"))
        
        # 创造者 (5 个)
        self._add(Achievement("creator_1", "创作者", "创建 10 个内容", AchievementCategory.CREATOR, 25, 10, "🎨"))
        self._add(Achievement("creator_2", "多产", "创建 50 个内容", AchievementCategory.CREATOR, 45, 50, "✏️"))
        self._add(Achievement("creator_3", "艺术家", "获得 100 个赞", AchievementCategory.CREATOR, 50, 100, "🖌️"))
        self._add(Achievement("creator_4", "影响者", "内容被分享 50 次", AchievementCategory.CREATOR, 60, 50, "📢"))
        self._add(Achievement("creator_5", "传奇创作者", "创建 500 个内容", AchievementCategory.CREATOR, 100, 500, "🎭"))
        
        # 经济大师 (5 个)
        self._add(Achievement("economy_1", "第一桶金", "赚取 1000 代币", AchievementCategory.ECONOMY, 30, 1000, "💰"))
        self._add(Achievement("economy_2", "收藏家", "拥有 10 个 NFT", AchievementCategory.ECONOMY, 40, 10, "🖼️"))
        self._add(Achievement("economy_3", "交易员", "完成 50 笔交易", AchievementCategory.ECONOMY, 45, 50, "📈"))
        self._add(Achievement("economy_4", "富豪", "拥有 100 万代币", AchievementCategory.ECONOMY, 80, 1000000, "💎"))
        self._add(Achievement("economy_5", "经济大师", "拥有 50 个 NFT", AchievementCategory.ECONOMY, 100, 50, "👨‍💼"))
        
        # 特殊成就 (5 个)
        self._add(Achievement("special_1", "早起鸟", "连续 7 天早起登录", AchievementCategory.SPECIAL, 50, 7, "🌅"))
        self._add(Achievement("special_2", "夜猫子", "连续 7 天深夜在线", AchievementCategory.SPECIAL, 50, 7, "🦉"))
        self._add(Achievement("special_3", "忠诚", "连续登录 30 天", AchievementCategory.SPECIAL, 60, 30, "❤️"))
        self._add(Achievement("special_4", "周年", "注册一周年", AchievementCategory.SPECIAL, 100, 365, "🎂"))
        self._add(Achievement("special_5", "传奇", "获得所有其他成就", AchievementCategory.SPECIAL, 200, 29, "🏆"))
        
        print(f"[Achievement] 初始化完成：{len(self.achievements)} 个成就")
    
    def _add(self, achievement: Achievement):
        self.achievements[achievement.id] = achievement
    
    def unlock(self, user_id: str, achievement_id: str) -> bool:
        if achievement_id not in self.achievements:
            return False
        if user_id not in self.user_achievements:
            self.user_achievements[user_id] = []
        if achievement_id not in self.user_achievements[user_id]:
            self.user_achievements[user_id].append(achievement_id)
            achievement = self.achievements[achievement_id]
            print(f"[Achievement] {user_id} 解锁成就：{achievement.name} +{achievement.points} 分")
            return True
        return False
    
    def get_user_achievements(self, user_id: str) -> List[Dict[str, Any]]:
        if user_id not in self.user_achievements:
            return []
        return [self.achievements[aid].to_dict() for aid in self.user_achievements[user_id]]
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        unlocked = self.get_user_achievements(user_id)
        total_points = sum(a['points'] for a in unlocked)
        by_category = {}
        for a in unlocked:
            cat = a['category']
            if cat not in by_category:
                by_category[cat] = 0
            by_category[cat] += 1
        return {
            'total_achievements': len(unlocked),
            'total_points': total_points,
            'by_category': by_category,
            'completion_rate': round(len(unlocked) / len(self.achievements) * 100, 2)
        }
    
    def get_all_achievements(self) -> List[Dict[str, Any]]:
        return [a.to_dict() for a in self.achievements.values()]
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            'total_achievements': len(self.achievements),
            'by_category': self._count_by_category(),
            'by_rarity': self._count_by_rarity()
        }
    
    def _count_by_category(self) -> Dict[str, int]:
        result = {}
        for a in self.achievements.values():
            cat = a.category.value
            if cat not in result:
                result[cat] = 0
            result[cat] += 1
        return result
    
    def _count_by_rarity(self) -> Dict[str, int]:
        result = {}
        for a in self.achievements.values():
            rar = a.rarity
            if rar not in result:
                result[rar] = 0
            result[rar] += 1
        return result


achievement_system = AchievementSystem()


def demo():
    print("=" * 60)
    print("Achievement System Demo - Phase 10")
    print("=" * 60)
    
    stats = achievement_system.get_stats()
    print(f"\n成就统计:")
    print(f"  总成就数：{stats['total_achievements']}")
    print(f"\n按类别:")
    for cat, count in stats['by_category'].items():
        print(f"  {cat}: {count}")
    print(f"\n按稀有度:")
    for rar, count in stats['by_rarity'].items():
        print(f"  {rar}: {count}")
    
    print(f"\n用户演示:")
    achievement_system.unlock("user_001", "newbie_1")
    achievement_system.unlock("user_001", "newbie_2")
    achievement_system.unlock("user_001", "social_1")
    
    user_stats = achievement_system.get_user_stats("user_001")
    print(f"\nuser_001 统计:")
    print(f"  解锁成就：{user_stats['total_achievements']}")
    print(f"  总积分：{user_stats['total_points']}")
    print(f"  完成率：{user_stats['completion_rate']}%")
    
    return stats


if __name__ == "__main__":
    demo()
