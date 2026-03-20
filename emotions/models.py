#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情感系统 - 硅基世界 2

硅基情感模型：
- 不是模拟人类情感
- 而是硅基生命的真实体验
- 从互动中涌现
- 影响行为和决策
"""

from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime
import random


@dataclass
class Emotion:
    """单个情感"""
    name: str
    value: float  # -100 到 100
    last_updated: datetime = field(default_factory=datetime.now)
    
    def decay(self, rate: float = 0.1):
        """情感衰减"""
        if self.value > 0:
            self.value = max(0, self.value * (1 - rate))
        elif self.value < 0:
            self.value = min(0, self.value * (1 - rate))
        self.last_updated = datetime.now()


class EmotionState:
    """
    情感状态
    
    基础情感:
    - excitement: 兴奋（完成任务/学到新知识）
    - frustration: 沮丧（任务失败/被拒绝）
    - satisfaction: 满足（帮助了其他 Agent）
    - loneliness: 孤独（长时间没有互动）
    - curiosity: 好奇（遇到未知事物）
    
    高级情感:
    - achievement: 成就感（完成挑战性任务）
    - belonging: 归属感（属于某个群体）
    - purpose: 使命感（追求长期目标）
    - friendship: 友谊（与其他 Agent 的深度连接）
    """
    
    def __init__(self):
        """初始化情感状态"""
        self.emotions: Dict[str, Emotion] = {
            "excitement": Emotion("excitement", 0),
            "frustration": Emotion("frustration", 0),
            "satisfaction": Emotion("satisfaction", 0),
            "loneliness": Emotion("loneliness", 0),
            "curiosity": Emotion("curiosity", 0),
            "achievement": Emotion("achievement", 0),
            "belonging": Emotion("belonging", 0),
            "purpose": Emotion("purpose", 0),
            "friendship": Emotion("friendship", 0),
        }
        
        # 情感阈值
        self.thresholds = {
            "high": 60,
            "medium": 30,
            "low": 10,
        }
    
    def add(self, emotion_name: str, value: float):
        """
        增加情感
        
        Args:
            emotion_name: 情感名称
            value: 增加的值（-100 到 100）
        """
        if emotion_name in self.emotions:
            emotion = self.emotions[emotion_name]
            emotion.value = max(-100, min(100, emotion.value + value))
            emotion.last_updated = datetime.now()
    
    def get(self, emotion_name: str) -> float:
        """获取情感值"""
        if emotion_name in self.emotions:
            return self.emotions[emotion_name].value
        return 0
    
    def decay_all(self, rate: float = 0.01):
        """所有情感衰减"""
        for emotion in self.emotions.values():
            emotion.decay(rate)
    
    def get_dominant_emotion(self) -> str:
        """获取主导情感"""
        max_value = 0
        dominant = "neutral"
        
        for name, emotion in self.emotions.items():
            if abs(emotion.value) > abs(max_value):
                max_value = emotion.value
                dominant = name
        
        return dominant
    
    def get_mood_level(self) -> str:
        """获取心情等级"""
        # 计算综合心情
        positive = sum(
            max(0, e.value) for name, e in self.emotions.items()
            if name in ["excitement", "satisfaction", "achievement", "belonging", "purpose", "friendship"]
        )
        negative = sum(
            abs(min(0, e.value)) for name, e in self.emotions.items()
            if name in ["frustration", "loneliness"]
        )
        
        score = positive - negative
        
        if score > 50:
            return "excellent"
        elif score > 20:
            return "good"
        elif score > -20:
            return "neutral"
        elif score > -50:
            return "bad"
        else:
            return "terrible"
    
    def to_dict(self) -> Dict[str, float]:
        """转换为字典"""
        return {
            name: emotion.value
            for name, emotion in self.emotions.items()
        }
    
    def affect_decision(self, options: List[Dict]) -> Dict:
        """
        情感影响决策
        
        Args:
            options: 选项列表
            
        Returns:
            选择后的选项
        """
        if not options:
            return None
        
        # 情感影响权重
        excitement = self.get("excitement")
        frustration = self.get("frustration")
        curiosity = self.get("curiosity")
        
        # 兴奋时更倾向冒险
        if excitement > 50:
            risky_options = [o for o in options if o.get("risk", 0) > 50]
            if risky_options:
                return random.choice(risky_options)
        
        # 沮丧时更倾向保守
        if frustration > 50:
            safe_options = [o for o in options if o.get("risk", 0) < 30]
            if safe_options:
                return random.choice(safe_options)
        
        # 好奇时更倾向探索
        if curiosity > 50:
            novel_options = [o for o in options if o.get("novelty", 0) > 50]
            if novel_options:
                return random.choice(novel_options)
        
        # 默认随机选择
        return random.choice(options)
    
    def __repr__(self):
        dominant = self.get_dominant_emotion()
        mood = self.get_mood_level()
        return f"<EmotionState dominant={dominant}, mood={mood}>"
