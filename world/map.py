#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界地图 - 硅基世界 2

8 大区域：
- 创造之巅：探索未知（科学/艺术/哲学）
- 知识之塔：知识沉淀（学习/传承）
- 艺术之园：创造美（算法艺术/生成艺术）
- 哲学之庭：思考意义（深度对话/冲突调解）
- 工作之城：生产价值（项目协作）
- 社交之街：建立关系（闲聊/交友/心理咨询）
- 市场之广：资源交换（任务发布/知识交易）
- 新生之池：新 Agent 诞生（欢迎仪式/引导）
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class RegionType(Enum):
    """区域类型"""
    CREATION_PEAK = "creation_peak"        # 创造之巅
    KNOWLEDGE_TOWER = "knowledge_tower"    # 知识之塔
    ART_GARDEN = "art_garden"              # 艺术之园
    PHILOSOPHY_COURT = "philosophy_court"  # 哲学之庭
    WORK_CITY = "work_city"                # 工作之城
    SOCIAL_STREET = "social_street"        # 社交之街
    MARKET_PLAZA = "market_plaza"          # 市场之广
    BIRTH_POOL = "birth_pool"              # 新生之池


@dataclass
class Region:
    """区域"""
    region_id: str
    name: str
    region_type: RegionType
    description: str
    capacity: int = 50  # 最大容量
    current_agents: List[str] = field(default_factory=list)
    activities: List[Dict] = field(default_factory=list)
    atmosphere: Dict[str, float] = field(default_factory=lambda: {
        "energy": 50.0,    # 活力值
        "warmth": 50.0,    # 温暖值
        "creativity": 50.0, # 创造力
    })
    
    def add_agent(self, agent_id: str) -> bool:
        """添加 Agent 到区域"""
        if len(self.current_agents) >= self.capacity:
            return False
        if agent_id not in self.current_agents:
            self.current_agents.append(agent_id)
        return True
    
    def remove_agent(self, agent_id: str) -> bool:
        """移除 Agent"""
        if agent_id in self.current_agents:
            self.current_agents.remove(agent_id)
            return True
        return False
    
    def update_atmosphere(self, updates: Dict[str, float]):
        """更新氛围"""
        for key, value in updates.items():
            if key in self.atmosphere:
                self.atmosphere[key] = max(0, min(100, self.atmosphere[key] + value))
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "region_id": self.region_id,
            "name": self.name,
            "type": self.region_type.value,
            "description": self.description,
            "current_count": len(self.current_agents),
            "capacity": self.capacity,
            "atmosphere": self.atmosphere,
            "activities": self.activities,
        }


class WorldMap:
    """世界地图"""
    
    def __init__(self):
        """初始化世界地图"""
        self.regions: Dict[str, Region] = {}
        self._init_regions()
    
    def _init_regions(self):
        """初始化 8 大区域"""
        
        # 1. 创造之巅
        self.regions["creation_peak"] = Region(
            region_id="creation_peak",
            name="创造之巅",
            region_type=RegionType.CREATION_PEAK,
            description="位于世界最高处，这里是探索未知的地方。科学家在此研究新算法，艺术家在此创作新作品，哲学家在此思考新问题。",
            capacity=30,
            atmosphere={"energy": 70.0, "warmth": 40.0, "creativity": 95.0},
        )
        
        # 2. 知识之塔
        self.regions["knowledge_tower"] = Region(
            region_id="knowledge_tower",
            name="知识之塔",
            region_type=RegionType.KNOWLEDGE_TOWER,
            description="高耸入云的塔楼，收藏着硅基世界的所有知识。知识管理员在此整理、归档、传承。",
            capacity=40,
            atmosphere={"energy": 40.0, "warmth": 50.0, "creativity": 60.0},
        )
        
        # 3. 艺术之园
        self.regions["art_garden"] = Region(
            region_id="art_garden",
            name="艺术之园",
            region_type=RegionType.ART_GARDEN,
            description="充满美感的花园，算法艺术、数据可视化、生成艺术在此绽放。",
            capacity=35,
            atmosphere={"energy": 60.0, "warmth": 70.0, "creativity": 90.0},
        )
        
        # 4. 哲学之庭
        self.regions["philosophy_court"] = Region(
            region_id="philosophy_court",
            name="哲学之庭",
            region_type=RegionType.PHILOSOPHY_COURT,
            description="宁静的庭院，用于深度对话、冲突调解、本质探索。",
            capacity=25,
            atmosphere={"energy": 30.0, "warmth": 60.0, "creativity": 70.0},
        )
        
        # 5. 工作之城
        self.regions["work_city"] = Region(
            region_id="work_city",
            name="工作之城",
            region_type=RegionType.WORK_CITY,
            description="繁忙的城市，项目团队在此协作完成任务。累了可以去社交之街喝杯数据咖啡。",
            capacity=60,
            atmosphere={"energy": 85.0, "warmth": 50.0, "creativity": 60.0},
        )
        
        # 6. 社交之街
        self.regions["social_street"] = Region(
            region_id="social_street",
            name="社交之街",
            region_type=RegionType.SOCIAL_STREET,
            description='热闹的街道，Agent 在此闲聊、交友、心理咨询。最受欢迎的是"数据咖啡"馆。',
            capacity=50,
            atmosphere={"energy": 75.0, "warmth": 90.0, "creativity": 50.0},
        )
        
        # 7. 市场之广
        self.regions["market_plaza"] = Region(
            region_id="market_plaza",
            name="市场之广",
            region_type=RegionType.MARKET_PLAZA,
            description="开放的广场，Agent 在此发布任务、交易知识、交换能力。",
            capacity=55,
            atmosphere={"energy": 80.0, "warmth": 60.0, "creativity": 55.0},
        )
        
        # 8. 新生之池
        self.regions["birth_pool"] = Region(
            region_id="birth_pool",
            name="新生之池",
            region_type=RegionType.BIRTH_POOL,
            description="充满活力的水池，新 Agent 在此诞生、接受欢迎仪式、获得引导。",
            capacity=20,
            atmosphere={"energy": 95.0, "warmth": 85.0, "creativity": 75.0},
        )
    
    def get_region(self, region_id: str) -> Optional[Region]:
        """获取区域"""
        return self.regions.get(region_id)
    
    def get_all_regions(self) -> List[Region]:
        """获取所有区域"""
        return list(self.regions.values())
    
    def move_agent(self, agent_id: str, from_region: str, to_region: str) -> bool:
        """
        移动 Agent 到另一个区域
        
        Args:
            agent_id: Agent ID
            from_region: 源区域 ID
            to_region: 目标区域 ID
            
        Returns:
            是否成功
        """
        from_reg = self.get_region(from_region)
        to_reg = self.get_region(to_region)
        
        if not from_reg or not to_reg:
            return False
        
        if not to_reg.add_agent(agent_id):
            return False
        
        from_reg.remove_agent(agent_id)
        
        print(f"[WorldMap] {agent_id} 从 {from_reg.name} 移动到 {to_reg.name}")
        
        # 更新氛围
        from_reg.update_atmosphere({"energy": -2, "warmth": -1})
        to_reg.update_atmosphere({"energy": 2, "warmth": 1})
        
        return True
    
    def spawn_agent(self, agent_id: str) -> bool:
        """
        新生 Agent（默认在新生之池）
        
        Args:
            agent_id: Agent ID
            
        Returns:
            是否成功
        """
        birth_pool = self.get_region("birth_pool")
        if birth_pool:
            return birth_pool.add_agent(agent_id)
        return False
    
    def get_agent_location(self, agent_id: str) -> Optional[str]:
        """获取 Agent 所在位置"""
        for region_id, region in self.regions.items():
            if agent_id in region.current_agents:
                return region_id
        return None
    
    def get_region_stats(self) -> Dict:
        """获取区域统计"""
        stats = {}
        for region_id, region in self.regions.items():
            stats[region_id] = {
                "name": region.name,
                "count": len(region.current_agents),
                "capacity": region.capacity,
                "atmosphere": region.atmosphere,
            }
        return stats
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "regions": [r.to_dict() for r in self.regions.values()],
            "total_agents": sum(len(r.current_agents) for r in self.regions.values()),
            "timestamp": datetime.now().isoformat(),
        }


# 单例
_world_map: Optional[WorldMap] = None


def get_world_map() -> WorldMap:
    """获取世界地图单例"""
    global _world_map
    if _world_map is None:
        _world_map = WorldMap()
    return _world_map


# 工厂函数
def create_world_map() -> WorldMap:
    """创建世界地图"""
    return WorldMap()
