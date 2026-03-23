#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
房屋系统 - 硅基世界 2

让 Agent 可以拥有和装饰房屋。
"""

from datetime import datetime
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum


class HouseType(Enum):
    """房屋类型"""
    APARTMENT = "apartment"    # 公寓
    HOUSE = "house"            # 房子
    VILLA = "villa"            # 别墅
    MANSION = "mansion"        # 豪宅


class DecorationType(Enum):
    """装饰类型"""
    FURNITURE = "furniture"    # 家具
    ART = "art"                # 艺术品
    PLANT = "plant"            # 植物
    ELECTRONIC = "electronic"  # 电子产品


@dataclass
class Decoration:
    """装饰品"""
    deco_id: str
    name: str
    deco_type: DecorationType
    value: float  # 价值
    comfort_bonus: float = 0.0  # 舒适度加成
    
    def to_dict(self) -> Dict:
        return {
            "deco_id": self.deco_id,
            "name": self.name,
            "type": self.deco_type.value,
            "value": self.value,
            "comfort_bonus": self.comfort_bonus,
        }


@dataclass
class House:
    """房屋"""
    house_id: str
    owner: str
    house_type: HouseType
    location: str
    size: int  # 平方米
    decorations: List[Decoration] = field(default_factory=list)
    comfort: float = 50.0  # 舒适度 0-100
    purchased_at: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def to_dict(self) -> Dict:
        return {
            "house_id": self.house_id,
            "owner": self.owner,
            "type": self.house_type.value,
            "location": self.location,
            "size": self.size,
            "comfort": self.comfort,
            "decoration_count": len(self.decorations),
            "total_value": sum(d.value for d in self.decorations),
        }


class HouseManager:
    """房屋管理器"""
    
    def __init__(self):
        """初始化房屋管理器"""
        self.houses: Dict[str, House] = {}
        self._house_counter = 0
        self._deco_counter = 0
        
        # 装饰库
        self.decoration_catalog: Dict[str, Decoration] = {}
        self._init_decorations()
        
        print("🏠 房屋系统已初始化")
    
    def _init_decorations(self):
        """初始化装饰库"""
        decorations = [
            ("沙发", DecorationType.FURNITURE, 100.0, 5.0),
            ("床", DecorationType.FURNITURE, 200.0, 10.0),
            ("桌子", DecorationType.FURNITURE, 80.0, 3.0),
            ("名画", DecorationType.ART, 500.0, 15.0),
            ("雕塑", DecorationType.ART, 300.0, 10.0),
            ("绿植", DecorationType.PLANT, 30.0, 5.0),
            ("花园", DecorationType.PLANT, 150.0, 10.0),
            ("电视", DecorationType.ELECTRONIC, 200.0, 5.0),
            ("音响", DecorationType.ELECTRONIC, 150.0, 5.0),
        ]
        
        for name, deco_type, value, comfort in decorations:
            self._deco_counter += 1
            self.decoration_catalog[f"deco_{self._deco_counter}"] = Decoration(
                deco_id=f"deco_{self._deco_counter}",
                name=name,
                deco_type=deco_type,
                value=value,
                comfort_bonus=comfort,
            )
    
    def purchase_house(
        self,
        owner: str,
        house_type: HouseType,
        location: str,
        size: int,
        price: float,
    ) -> House:
        """
        购买房屋
        
        Args:
            owner: 主人
            house_type: 房屋类型
            location: 位置
            size: 面积
            price: 价格
            
        Returns:
            房屋对象
        """
        self._house_counter += 1
        
        house = House(
            house_id=f"house_{self._house_counter}",
            owner=owner,
            house_type=house_type,
            location=location,
            size=size,
        )
        
        self.houses[house.house_id] = house
        
        print(f"  🏠 {owner} 购买了 {house_type.value} @ {location}")
        
        return house
    
    def add_decoration(self, house_id: str, owner: str, deco_id: str) -> bool:
        """
        添加装饰
        
        Args:
            house_id: 房屋 ID
            owner: 主人
            deco_id: 装饰 ID
            
        Returns:
            是否成功
        """
        if house_id not in self.houses:
            return False
        
        house = self.houses[house_id]
        
        if house.owner != owner:
            return False
        
        if deco_id not in self.decoration_catalog:
            return False
        
        deco = self.decoration_catalog[deco_id]
        house.decorations.append(deco)
        
        # 更新舒适度
        house.comfort = min(100, house.comfort + deco.comfort_bonus)
        
        print(f"  🎨 {owner} 为房屋添加了 {deco.name}")
        
        return True
    
    def get_owner_houses(self, owner: str) -> List[House]:
        """获取主人的房屋"""
        return [h for h in self.houses.values() if h.owner == owner]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_houses": len(self.houses),
            "by_type": {
                t.value: len([h for h in self.houses.values() if h.house_type == t])
                for t in HouseType
            },
            "owners": len(set(h.owner for h in self.houses.values())),
            "total_decorations": sum(len(h.decorations) for h in self.houses.values()),
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "houses": [h.to_dict() for h in self.houses.values()[:10]],
            "decoration_catalog": [d.to_dict() for d in list(self.decoration_catalog.values())[:10]],
        }


# 单例
_house_manager: Optional[HouseManager] = None


def get_house_manager() -> HouseManager:
    """获取房屋管理器单例"""
    global _house_manager
    if _house_manager is None:
        _house_manager = HouseManager()
    return _house_manager


# 工厂函数
def create_house_manager() -> HouseManager:
    """创建房屋管理器"""
    return HouseManager()
