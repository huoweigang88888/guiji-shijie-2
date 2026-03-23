#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商店系统 - 硅基世界 2

让 Agent 可以购买物品、服务、技能书等。
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class ItemType(Enum):
    """物品类型"""
    TOOL = "tool"              # 工具
    BOOK = "book"              # 书籍
    SERVICE = "service"        # 服务
    DECORATION = "decoration"  # 装饰
    CONSUMABLE = "consumable"  # 消耗品


@dataclass
class Item:
    """物品"""
    item_id: str
    name: str
    description: str
    item_type: ItemType
    price: float
    effect: Optional[Dict] = None  # 效果
    duration: Optional[int] = None  # 持续时间（小时）
    
    def to_dict(self) -> Dict:
        return {
            "item_id": self.item_id,
            "name": self.name,
            "description": self.description,
            "type": self.item_type.value,
            "price": self.price,
            "effect": self.effect,
        }


@dataclass
class Purchase:
    """购买记录"""
    purchase_id: str
    buyer: str
    item: Item
    price: float
    purchased_at: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def to_dict(self) -> Dict:
        return {
            "purchase_id": self.purchase_id,
            "buyer": self.buyer,
            "item": self.item.to_dict(),
            "price": self.price,
            "purchased_at": self.purchased_at,
        }


class ShopManager:
    """商店管理器"""
    
    def __init__(self):
        """初始化商店管理器"""
        self.items: Dict[str, Item] = {}
        self.purchases: List[Purchase] = []
        self._item_counter = 0
        self._purchase_counter = 0
        
        # 初始化商品
        self._init_items()
        
        print("🛒 商店系统已初始化")
    
    def _init_items(self):
        """初始化商品"""
        # 工具
        self.create_item(
            "效率工具",
            "提高工作效率的工具",
            ItemType.TOOL,
            50.0,
            effect={"productivity": 10},
            duration=24,
        )
        
        # 书籍
        self.create_item(
            "《架构设计指南》",
            "学习架构设计的书籍",
            ItemType.BOOK,
            30.0,
            effect={"skill_architecture": 5},
        )
        
        self.create_item(
            "《代码整洁之道》",
            "学习代码规范的书籍",
            ItemType.BOOK,
            25.0,
            effect={"skill_coding": 5},
        )
        
        # 服务
        self.create_item(
            "咨询服务",
            "专业咨询服务 1 小时",
            ItemType.SERVICE,
            100.0,
            effect={"consultation": 1},
        )
        
        # 装饰
        self.create_item(
            "办公室装饰",
            "装饰办公室，提升心情",
            ItemType.DECORATION,
            20.0,
            effect={"mood": 10},
            duration=48,
        )
        
        # 消耗品
        self.create_item(
            "数据咖啡",
            "提神醒脑的数据咖啡",
            ItemType.CONSUMABLE,
            5.0,
            effect={"energy": 15},
            duration=4,
        )
        
        self.create_item(
            "能量饮料",
            "快速补充能量",
            ItemType.CONSUMABLE,
            8.0,
            effect={"energy": 25},
            duration=6,
        )
    
    def create_item(
        self,
        name: str,
        description: str,
        item_type: ItemType,
        price: float,
        effect: Optional[Dict] = None,
        duration: Optional[int] = None,
    ) -> Item:
        """创建商品"""
        self._item_counter += 1
        
        item = Item(
            item_id=f"item_{self._item_counter}",
            name=name,
            description=description,
            item_type=item_type,
            price=price,
            effect=effect,
            duration=duration,
        )
        
        self.items[item.item_id] = item
        
        print(f"  🛒 上架商品：{name} ({price} 信用点)")
        
        return item
    
    def purchase(self, buyer: str, item_id: str) -> Optional[Purchase]:
        """
        购买商品
        
        Args:
            buyer: 购买者
            item_id: 商品 ID
            
        Returns:
            购买记录
        """
        if item_id not in self.items:
            print(f"  ❌ 商品不存在：{item_id}")
            return None
        
        item = self.items[item_id]
        
        self._purchase_counter += 1
        
        purchase = Purchase(
            purchase_id=f"purchase_{self._purchase_counter}",
            buyer=buyer,
            item=item,
            price=item.price,
        )
        
        self.purchases.append(purchase)
        
        print(f"  💰 {buyer} 购买了 {item.name} ({item.price} 信用点)")
        
        return purchase
    
    def get_items(self, item_type: Optional[ItemType] = None) -> List[Item]:
        """获取商品列表"""
        if item_type:
            return [i for i in self.items.values() if i.item_type == item_type]
        return list(self.items.values())
    
    def get_purchases(self, buyer: Optional[str] = None) -> List[Purchase]:
        """获取购买记录"""
        if buyer:
            return [p for p in self.purchases if p.buyer == buyer]
        return self.purchases
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_items": len(self.items),
            "total_purchases": len(self.purchases),
            "total_revenue": sum(p.price for p in self.purchases),
            "by_type": {
                t.value: len([i for i in self.items.values() if i.item_type == t])
                for t in ItemType
            },
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "items": [i.to_dict() for i in self.get_items()],
            "recent_purchases": [p.to_dict() for p in self.purchases[-10:]],
        }


# 单例
_shop_manager: Optional[ShopManager] = None


def get_shop_manager() -> ShopManager:
    """获取商店管理器单例"""
    global _shop_manager
    if _shop_manager is None:
        _shop_manager = ShopManager()
    return _shop_manager


# 工厂函数
def create_shop_manager() -> ShopManager:
    """创建商店管理器"""
    return ShopManager()
