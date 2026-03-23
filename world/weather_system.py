#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天气系统 - 硅基世界 2

让世界更有真实感，不同区域有不同天气，影响 Agent 心情和活动。
"""

import random
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class WeatherType(Enum):
    """天气类型"""
    SUNNY = "sunny"          # 晴朗
    CLOUDY = "cloudy"        # 多云
    RAINY = "rainy"          # 下雨
    STORMY = "stormy"        # 暴风雨
    SNOWY = "snowy"          # 下雪
    FOGGY = "foggy"          # 有雾
    WINDY = "windy"          # 有风


@dataclass
class Weather:
    """天气"""
    region_id: str
    weather_type: WeatherType
    temperature: float  # 摄氏度
    humidity: float  # 湿度%
    wind_speed: float  # 风速
    description: str
    mood_effect: float = 0.0  # 对心情的影响 (-10 到 +10)
    updated_at: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def to_dict(self) -> Dict:
        return {
            "region_id": self.region_id,
            "weather": self.weather_type.value,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "wind_speed": self.wind_speed,
            "description": self.description,
            "mood_effect": self.mood_effect,
        }


class WeatherManager:
    """天气管理器"""
    
    def __init__(self):
        """初始化天气管理器"""
        self.weather_data: Dict[str, Weather] = {}
        self.weather_history: List[Dict] = []
        
        # 天气描述
        self.weather_descriptions = {
            WeatherType.SUNNY: "阳光明媚，万里无云",
            WeatherType.CLOUDY: "云层较厚，光线柔和",
            WeatherType.RAINY: "细雨绵绵，空气清新",
            WeatherType.STORMY: "电闪雷鸣，风雨交加",
            WeatherType.SNOWY: "雪花飘飘，银装素裹",
            WeatherType.FOGGY: "雾气弥漫，能见度低",
            WeatherType.WINDY: "微风习习，清爽宜人",
        }
        
        # 天气对心情的影响
        self.mood_effects = {
            WeatherType.SUNNY: 5.0,
            WeatherType.CLOUDY: 0.0,
            WeatherType.RAINY: -3.0,
            WeatherType.STORMY: -5.0,
            WeatherType.SNOWY: 3.0,
            WeatherType.FOGGY: -2.0,
            WeatherType.WINDY: 2.0,
        }
        
        print("🌤️  天气系统已初始化")
    
    def generate_weather(self, region_id: str) -> Weather:
        """
        生成天气
        
        Args:
            region_id: 区域 ID
            
        Returns:
            天气对象
        """
        # 随机生成天气
        weather_type = random.choice(list(WeatherType))
        
        # 根据天气类型生成温度
        base_temp = {
            WeatherType.SUNNY: 25,
            WeatherType.CLOUDY: 20,
            WeatherType.RAINY: 18,
            WeatherType.STORMY: 22,
            WeatherType.SNOWY: -5,
            WeatherType.FOGGY: 15,
            WeatherType.WINDY: 20,
        }
        
        temperature = base_temp[weather_type] + random.randint(-3, 3)
        humidity = random.randint(30, 90)
        wind_speed = random.randint(0, 30)
        
        weather = Weather(
            region_id=region_id,
            weather_type=weather_type,
            temperature=temperature,
            humidity=humidity,
            wind_speed=wind_speed,
            description=self.weather_descriptions[weather_type],
            mood_effect=self.mood_effects[weather_type],
        )
        
        self.weather_data[region_id] = weather
        
        # 记录历史
        self.weather_history.append({
            "region_id": region_id,
            "weather": weather_type.value,
            "timestamp": datetime.now().timestamp(),
        })
        
        return weather
    
    def get_weather(self, region_id: str) -> Optional[Weather]:
        """获取区域天气"""
        return self.weather_data.get(region_id)
    
    def update_all_weather(self) -> Dict[str, Weather]:
        """更新所有区域天气"""
        regions = [
            "creation_peak", "knowledge_tower", "art_garden",
            "philosophy_court", "work_city", "social_street",
            "market_plaza", "birth_pool",
        ]
        
        for region_id in regions:
            self.generate_weather(region_id)
        
        print("  🌤️  天气已更新")
        
        return self.weather_data
    
    def get_weather_by_type(self, weather_type: WeatherType) -> List[str]:
        """获取特定天气的区域"""
        return [
            region_id for region_id, weather in self.weather_data.items()
            if weather.weather_type == weather_type
        ]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        weather_counts = {}
        for weather in self.weather_data.values():
            wtype = weather.weather_type.value
            weather_counts[wtype] = weather_counts.get(wtype, 0) + 1
        
        return {
            "regions_with_weather": len(self.weather_data),
            "weather_distribution": weather_counts,
            "history_records": len(self.weather_history),
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "current_weather": {
                region_id: w.to_dict() for region_id, w in self.weather_data.items()
            },
        }


# 单例
_weather_manager: Optional[WeatherManager] = None


def get_weather_manager() -> WeatherManager:
    """获取天气管理器单例"""
    global _weather_manager
    if _weather_manager is None:
        _weather_manager = WeatherManager()
    return _weather_manager


# 工厂函数
def create_weather_manager() -> WeatherManager:
    """创建天气管理器"""
    return WeatherManager()
