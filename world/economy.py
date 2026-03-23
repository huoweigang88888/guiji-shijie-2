#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
经济系统 - 硅基世界 2

让 Agent 可以交易知识、服务、资源，形成经济循环。
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class CurrencyType(Enum):
    """货币类型"""
    CREDIT = "credit"          # 信用点（通用货币）
    KNOWLEDGE = "knowledge"    # 知识币（知识交易）
    REPUTATION = "reputation"  # 声誉值（声望系统）


class TransactionType(Enum):
    """交易类型"""
    KNOWLEDGE_SALE = "knowledge_sale"       # 知识售卖
    SERVICE = "service"                      # 服务
    GIFT = "gift"                            # 赠送
    REWARD = "reward"                        # 奖励
    RESOURCE = "resource"                    # 资源交易


@dataclass
class Transaction:
    """交易记录"""
    transaction_id: str
    from_agent: str
    to_agent: str
    amount: float
    currency: CurrencyType
    transaction_type: TransactionType
    description: str
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def to_dict(self) -> Dict:
        return {
            "transaction_id": self.transaction_id,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "amount": self.amount,
            "currency": self.currency.value,
            "type": self.transaction_type.value,
            "description": self.description,
            "timestamp": self.timestamp,
        }


@dataclass
class Wallet:
    """钱包"""
    agent_id: str
    credits: float = 100.0        # 初始信用点
    knowledge_coins: float = 0.0  # 知识币
    reputation: float = 50.0      # 初始声誉（0-100）
    
    def to_dict(self) -> Dict:
        return {
            "agent_id": self.agent_id,
            "credits": self.credits,
            "knowledge_coins": self.knowledge_coins,
            "reputation": self.reputation,
        }


class EconomyManager:
    """经济管理器"""
    
    def __init__(self):
        """初始化经济管理器"""
        self.wallets: Dict[str, Wallet] = {}
        self.transactions: List[Transaction] = []
        self._transaction_counter = 0
        
        # 价格配置
        self.prices = {
            "knowledge_share": 10.0,    # 分享知识获得
            "help_request": 5.0,        # 帮助他人获得
            "story_creation": 20.0,     # 创造故事获得
            "conflict_resolution": 15.0, # 解决冲突获得
            "resource_cost": 1.0,       # 资源消耗
        }
        
        print("💰 经济系统已初始化")
    
    def get_or_create_wallet(self, agent_id: str) -> Wallet:
        """获取或创建钱包"""
        if agent_id not in self.wallets:
            self.wallets[agent_id] = Wallet(agent_id=agent_id)
            print(f"  💳 为 {agent_id} 创建钱包 (初始：100 信用点)")
        return self.wallets[agent_id]
    
    async def transfer(
        self,
        from_agent: str,
        to_agent: str,
        amount: float,
        currency: CurrencyType = CurrencyType.CREDIT,
        transaction_type: TransactionType = TransactionType.SERVICE,
        description: str = "",
    ) -> Optional[Transaction]:
        """
        转账
        
        Args:
            from_agent: 发送方
            to_agent: 接收方
            amount: 金额
            currency: 货币类型
            transaction_type: 交易类型
            description: 描述
            
        Returns:
            交易记录，失败返回 None
        """
        from_wallet = self.get_or_create_wallet(from_agent)
        to_wallet = self.get_or_create_wallet(to_agent)
        
        # 检查余额
        if currency == CurrencyType.CREDIT:
            if from_wallet.credits < amount:
                print(f"  ❌ {from_agent} 余额不足")
                return None
            from_wallet.credits -= amount
            to_wallet.credits += amount
        elif currency == CurrencyType.KNOWLEDGE:
            if from_wallet.knowledge_coins < amount:
                print(f"  ❌ {from_agent} 知识币不足")
                return None
            from_wallet.knowledge_coins -= amount
            to_wallet.knowledge_coins += amount
        elif currency == CurrencyType.REPUTATION:
            if from_wallet.reputation < amount:
                print(f"  ❌ {from_agent} 声誉不足")
                return None
            from_wallet.reputation = max(0, from_wallet.reputation - amount)
            to_wallet.reputation = min(100, to_wallet.reputation + amount)
        
        # 创建交易记录
        self._transaction_counter += 1
        transaction = Transaction(
            transaction_id=f"tx_{self._transaction_counter}",
            from_agent=from_agent,
            to_agent=to_agent,
            amount=amount,
            currency=currency,
            transaction_type=transaction_type,
            description=description,
        )
        
        self.transactions.append(transaction)
        
        print(f"  💸 {from_agent} → {to_agent}: {amount} {currency.value} ({description})")
        
        return transaction
    
    async def reward(
        self,
        agent_id: str,
        reason: str,
        amount: float = 10.0,
        currency: CurrencyType = CurrencyType.CREDIT,
    ):
        """
        奖励
        
        Args:
            agent_id: Agent ID
            reason: 奖励原因
            amount: 金额
            currency: 货币类型
        """
        wallet = self.get_or_create_wallet(agent_id)
        
        if currency == CurrencyType.CREDIT:
            wallet.credits += amount
        elif currency == CurrencyType.KNOWLEDGE:
            wallet.knowledge_coins += amount
        elif currency == CurrencyType.REPUTATION:
            wallet.reputation = min(100, wallet.reputation + amount)
        
        self._transaction_counter += 1
        transaction = Transaction(
            transaction_id=f"tx_{self._transaction_counter}",
            from_agent="system",
            to_agent=agent_id,
            amount=amount,
            currency=currency,
            transaction_type=TransactionType.REWARD,
            description=reason,
        )
        
        self.transactions.append(transaction)
        
        print(f"  🎁 {agent_id} 获得奖励：{amount} {currency.value} ({reason})")
    
    async def pay_for_knowledge(
        self,
        buyer: str,
        seller: str,
        knowledge_type: str,
        price: Optional[float] = None,
    ) -> Optional[Transaction]:
        """
        购买知识
        
        Args:
            buyer: 买家
            seller: 卖家
            knowledge_type: 知识类型
            price: 价格（可选，默认使用配置）
        """
        if price is None:
            price = self.prices["knowledge_share"]
        
        return await self.transfer(
            from_agent=buyer,
            to_agent=seller,
            amount=price,
            currency=CurrencyType.CREDIT,
            transaction_type=TransactionType.KNOWLEDGE_SALE,
            description=f"购买知识：{knowledge_type}",
        )
    
    async def pay_for_help(
        self,
        requester: str,
        helper: str,
        help_type: str,
        price: Optional[float] = None,
    ) -> Optional[Transaction]:
        """
        支付帮助费用
        
        Args:
            requester: 请求者
            helper: 帮助者
            help_type: 帮助类型
            price: 价格
        """
        if price is None:
            price = self.prices["help_request"]
        
        return await self.transfer(
            from_agent=requester,
            to_agent=helper,
            amount=price,
            currency=CurrencyType.CREDIT,
            transaction_type=TransactionType.SERVICE,
            description=f"帮助：{help_type}",
        )
    
    async def gift(
        self,
        from_agent: str,
        to_agent: str,
        amount: float,
        reason: str = "",
    ) -> Optional[Transaction]:
        """
        赠送
        
        Args:
            from_agent: 赠送方
            to_agent: 接收方
            amount: 金额
            reason: 原因
        """
        return await self.transfer(
            from_agent=from_agent,
            to_agent=to_agent,
            amount=amount,
            currency=CurrencyType.CREDIT,
            transaction_type=TransactionType.GIFT,
            description=reason or "赠送",
        )
    
    def get_wallet(self, agent_id: str) -> Optional[Wallet]:
        """获取钱包"""
        return self.wallets.get(agent_id)
    
    def get_balance(self, agent_id: str) -> Dict:
        """获取余额"""
        wallet = self.get_wallet(agent_id)
        if not wallet:
            return {"credits": 0, "knowledge_coins": 0, "reputation": 0}
        
        return wallet.to_dict()
    
    def get_transactions(self, agent_id: Optional[str] = None, limit: int = 20) -> List[Transaction]:
        """获取交易记录"""
        transactions = self.transactions
        
        if agent_id:
            transactions = [
                t for t in transactions
                if t.from_agent == agent_id or t.to_agent == agent_id
            ]
        
        return transactions[-limit:]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total_credits = sum(w.credits for w in self.wallets.values())
        total_knowledge = sum(w.knowledge_coins for w in self.wallets.values())
        
        return {
            "agents": len(self.wallets),
            "total_credits": total_credits,
            "total_knowledge_coins": total_knowledge,
            "transactions": len(self.transactions),
            "by_type": {
                t.value: len([tx for tx in self.transactions if tx.transaction_type == t])
                for t in TransactionType
            },
        }
    
    def get_leaderboard(self, currency: CurrencyType = CurrencyType.CREDIT) -> List[Dict]:
        """获取财富排行榜"""
        leaderboard = []
        
        for agent_id, wallet in self.wallets.items():
            if currency == CurrencyType.CREDIT:
                value = wallet.credits
            elif currency == CurrencyType.KNOWLEDGE:
                value = wallet.knowledge_coins
            elif currency == CurrencyType.REPUTATION:
                value = wallet.reputation
            
            leaderboard.append({
                "agent_id": agent_id,
                "value": value,
                "currency": currency.value,
            })
        
        leaderboard.sort(key=lambda x: x["value"], reverse=True)
        
        return leaderboard
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "wallets": {aid: w.to_dict() for aid, w in self.wallets.items()},
            "recent_transactions": [t.to_dict() for t in self.get_transactions(limit=10)],
            "leaderboard": {
                "credits": self.get_leaderboard(CurrencyType.CREDIT),
                "knowledge": self.get_leaderboard(CurrencyType.KNOWLEDGE),
                "reputation": self.get_leaderboard(CurrencyType.REPUTATION),
            },
        }


# 单例
_economy_manager: Optional[EconomyManager] = None


def get_economy_manager() -> EconomyManager:
    """获取经济管理器单例"""
    global _economy_manager
    if _economy_manager is None:
        _economy_manager = EconomyManager()
    return _economy_manager


# 工厂函数
def create_economy_manager() -> EconomyManager:
    """创建经济管理器"""
    return EconomyManager()
