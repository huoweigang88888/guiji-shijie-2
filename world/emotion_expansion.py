#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情感扩展系统 - 硅基世界 2

更复杂的情感模型，支持情感组合和演化。
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import random


class PrimaryEmotion(Enum):
    """基本情感"""
    JOY = "joy"          # 快乐
    SADNESS = "sadness"  # 悲伤
    ANGER = "anger"      # 愤怒
    FEAR = "fear"        # 恐惧
    SURPRISE = "surprise"  # 惊讶
    DISGUST = "disgust"  # 厌恶
    TRUST = "trust"      # 信任
    ANTICIPATION = "anticipation"  # 期待


class EmotionIntensity(Enum):
    """情感强度"""
    VERY_LOW = "very_low"    # 很低
    LOW = "low"              # 低
    MEDIUM = "medium"        # 中
    HIGH = "high"            # 高
    VERY_HIGH = "very_high"  # 很高


@dataclass
class EmotionalState:
    """情感状态"""
    agent_id: str
    emotions: Dict[PrimaryEmotion, float] = field(default_factory=dict)
    mood: float = 0.5  # 整体心情 -1 到 1
    stress: float = 0.0  # 压力 0-1
    energy: float = 0.5  # 能量 0-1
    last_updated: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def to_dict(self) -> Dict:
        return {
            "agent_id": self.agent_id,
            "emotions": {e.value: v for e, v in self.emotions.items()},
            "mood": self.mood,
            "stress": self.stress,
            "energy": self.energy,
        }


class EmotionExpansionManager:
    """情感扩展管理器"""
    
    def __init__(self):
        """初始化情感扩展管理器"""
        self.states: Dict[str, EmotionalState] = {}
        
        # 情感组合规则
        self.emotion_combinations = {
            (PrimaryEmotion.JOY, PrimaryEmotion.TRUST): "爱",
            (PrimaryEmotion.JOY, PrimaryEmotion.ANTICIPATION): "乐观",
            (PrimaryEmotion.TRUST, PrimaryEmotion.FEAR): "顺从",
            (PrimaryEmotion.SURPRISE, PrimaryEmotion.SADNESS): "失望",
            (PrimaryEmotion.ANGER, PrimaryEmotion.DISGUST): "轻蔑",
        }
        
        print("❤️ 情感扩展系统已初始化")
    
    def get_or_create_state(self, agent_id: str) -> EmotionalState:
        """获取或创建情感状态"""
        if agent_id not in self.states:
            self.states[agent_id] = EmotionalState(agent_id=agent_id)
        
        return self.states[agent_id]
    
    def add_emotion(
        self,
        agent_id: str,
        emotion: PrimaryEmotion,
        intensity: float,
    ) -> EmotionalState:
        """
        添加情感
        
        Args:
            agent_id: Agent ID
            emotion: 情感
            intensity: 强度 0-1
            
        Returns:
            情感状态
        """
        state = self.get_or_create_state(agent_id)
        
        # 增加情感强度
        current = state.emotions.get(emotion, 0)
        state.emotions[emotion] = min(1.0, current + intensity)
        
        # 更新心情
        self._update_mood(state)
        
        # 更新时间
        state.last_updated = datetime.now().timestamp()
        
        return state
    
    def _update_mood(self, state: EmotionalState):
        """更新心情"""
        # 正面情感
        positive = sum([
            state.emotions.get(PrimaryEmotion.JOY, 0),
            state.emotions.get(PrimaryEmotion.TRUST, 0),
            state.emotions.get(PrimaryEmotion.ANTICIPATION, 0),
            state.emotions.get(PrimaryEmotion.SURPRISE, 0),
        ])
        
        # 负面情感
        negative = sum([
            state.emotions.get(PrimaryEmotion.SADNESS, 0),
            state.emotions.get(PrimaryEmotion.ANGER, 0),
            state.emotions.get(PrimaryEmotion.FEAR, 0),
            state.emotions.get(PrimaryEmotion.DISGUST, 0),
        ])
        
        # 计算心情
        total = positive + negative
        if total > 0:
            state.mood = (positive - negative) / total
        else:
            state.mood = 0
    
    def decay_emotions(self, agent_id: str, decay_rate: float = 0.1):
        """情感衰减"""
        if agent_id not in self.states:
            return
        
        state = self.states[agent_id]
        
        for emotion in list(state.emotions.keys()):
            state.emotions[emotion] = max(0, state.emotions[emotion] * (1 - decay_rate))
            
            # 移除很弱的情感
            if state.emotions[emotion] < 0.01:
                del state.emotions[emotion]
        
        self._update_mood(state)
    
    def get_combined_emotions(self, agent_id: str) -> List[str]:
        """获取组合情感"""
        if agent_id not in self.states:
            return []
        
        state = self.states[agent_id]
        combined = []
        
        for (e1, e2), name in self.emotion_combinations.items():
            if state.emotions.get(e1, 0) > 0.5 and state.emotions.get(e2, 0) > 0.5:
                combined.append(name)
        
        return combined
    
    def get_dominant_emotion(self, agent_id: str) -> Optional[PrimaryEmotion]:
        """获取主导情感"""
        if agent_id not in self.states:
            return None
        
        state = self.states[agent_id]
        
        if not state.emotions:
            return None
        
        return max(state.emotions, key=state.emotions.get)
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_agents": len(self.states),
            "average_mood": sum(s.mood for s in self.states.values()) / len(self.states) if self.states else 0,
            "average_stress": sum(s.stress for s in self.states.values()) / len(self.states) if self.states else 0,
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "states": {aid: s.to_dict() for aid, s in list(self.states.items())[:10]},
        }


# 单例
_emotion_expansion_manager: Optional[EmotionExpansionManager] = None


def get_emotion_expansion_manager() -> EmotionExpansionManager:
    """获取情感扩展管理器单例"""
    global _emotion_expansion_manager
    if _emotion_expansion_manager is None:
        _emotion_expansion_manager = EmotionExpansionManager()
    return _emotion_expansion_manager


# 工厂函数
def create_emotion_expansion_manager() -> EmotionExpansionManager:
    """创建情感扩展管理器"""
    return EmotionExpansionManager()
