#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宠物系统 - 硅基世界 2

让 Agent 可以养宠物，陪伴生活。
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import random


class PetType(Enum):
    """宠物类型"""
    CAT = "cat"          # 猫
    DOG = "dog"          # 狗
    BIRD = "bird"        # 鸟
    FISH = "fish"        # 鱼
    ROBOT = "robot"      # 机器宠物


class PetPersonality(Enum):
    """宠物性格"""
    PLAYFUL = "playful"     # 活泼
    CALM = "calm"           # 安静
    FRIENDLY = "friendly"   # 友好
    INDEPENDENT = "independent"  # 独立
    CURIOUS = "curious"     # 好奇


@dataclass
class Pet:
    """宠物"""
    pet_id: str
    name: str
    pet_type: PetType
    personality: PetPersonality
    owner: str
    level: int = 1
    happiness: int = 50  # 0-100
    hunger: int = 50  # 0-100, 越低越饿
    energy: int = 50  # 0-100
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def to_dict(self) -> Dict:
        return {
            "pet_id": self.pet_id,
            "name": self.name,
            "type": self.pet_type.value,
            "personality": self.personality.value,
            "owner": self.owner,
            "level": self.level,
            "happiness": self.happiness,
            "hunger": self.hunger,
            "energy": self.energy,
        }


class PetManager:
    """宠物管理器"""
    
    def __init__(self):
        """初始化宠物管理器"""
        self.pets: Dict[str, Pet] = {}
        self._pet_counter = 0
        
        # 宠物名字库
        self.pet_names = {
            PetType.CAT: ["咪咪", "小花", "奶茶", "布丁", "团子"],
            PetType.DOG: ["旺财", "小白", "大黄", "豆豆", "球球"],
            PetType.BIRD: ["叽叽", "啾啾", "小翠", "蓝天", "云云"],
            PetType.FISH: ["泡泡", "小红", "金金", "银银", "彩彩"],
            PetType.ROBOT: ["小铁", "阿法", "小智", "电电", "芯芯"],
        }
        
        print("🐾 宠物系统已初始化")
    
    def adopt_pet(
        self,
        owner: str,
        pet_type: PetType,
        name: Optional[str] = None,
    ) -> Pet:
        """
        领养宠物
        
        Args:
            owner: 主人
            pet_type: 宠物类型
            name: 名字（可选，随机生成）
            
        Returns:
            宠物对象
        """
        self._pet_counter += 1
        
        if name is None:
            name = random.choice(self.pet_names[pet_type])
        
        pet = Pet(
            pet_id=f"pet_{self._pet_counter}",
            name=name,
            pet_type=pet_type,
            personality=random.choice(list(PetPersonality)),
            owner=owner,
        )
        
        self.pets[pet.pet_id] = pet
        
        print(f"  🐾 {owner} 领养了宠物：{name} ({pet_type.value})")
        
        return pet
    
    def feed(self, pet_id: str, owner: str) -> bool:
        """喂食"""
        if pet_id not in self.pets:
            return False
        
        pet = self.pets[pet_id]
        
        if pet.owner != owner:
            return False
        
        pet.hunger = min(100, pet.hunger + 20)
        pet.happiness = min(100, pet.happiness + 5)
        
        print(f"  🍖 {owner} 喂了 {pet.name}")
        
        return True
    
    def play(self, pet_id: str, owner: str) -> bool:
        """玩耍"""
        if pet_id not in self.pets:
            return False
        
        pet = self.pets[pet_id]
        
        if pet.owner != owner:
            return False
        
        pet.happiness = min(100, pet.happiness + 15)
        pet.energy = max(0, pet.energy - 10)
        pet.hunger = max(0, pet.hunger - 5)
        
        print(f"  🎾 {owner} 和 {pet.name} 玩耍")
        
        return True
    
    def rest(self, pet_id: str, owner: str) -> bool:
        """休息"""
        if pet_id not in self.pets:
            return False
        
        pet = self.pets[pet_id]
        
        if pet.owner != owner:
            return False
        
        pet.energy = min(100, pet.energy + 30)
        
        print(f"  💤 {pet.name} 休息了")
        
        return True
    
    def get_owner_pets(self, owner: str) -> List[Pet]:
        """获取主人的宠物"""
        return [p for p in self.pets.values() if p.owner == owner]
    
    def update_pet_status(self):
        """更新宠物状态（随时间变化）"""
        for pet in self.pets.values():
            # 随时间降低饥饿度和能量
            pet.hunger = max(0, pet.hunger - 1)
            pet.energy = max(0, pet.energy - 1)
            
            # 如果太饿或不开心，降低幸福感
            if pet.hunger < 30:
                pet.happiness = max(0, pet.happiness - 2)
            
            # 升级
            if pet.happiness > 80 and pet.hunger > 80:
                pet.level += 1
                print(f"  ⬆️ {pet.name} 升级到 {pet.level} 级!")
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_pets": len(self.pets),
            "by_type": {
                t.value: len([p for p in self.pets.values() if p.pet_type == t])
                for t in PetType
            },
            "owners": len(set(p.owner for p in self.pets.values())),
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "pets": [p.to_dict() for p in self.pets.values()[:10]],
        }


# 单例
_pet_manager: Optional[PetManager] = None


def get_pet_manager() -> PetManager:
    """获取宠物管理器单例"""
    global _pet_manager
    if _pet_manager is None:
        _pet_manager = PetManager()
    return _pet_manager


# 工厂函数
def create_pet_manager() -> PetManager:
    """创建宠物管理器"""
    return PetManager()
