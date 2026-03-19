#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
经济系统 API

提供代币、余额、市场、交易等功能
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

router = APIRouter(prefix="/api/v1/economy", tags=["Economy"])


class BalanceResponse(BaseModel):
    """余额响应"""
    user_id: str
    balance: float
    currency: str = "SWT"  # Silicon World Token
    last_updated: str


class TransferRequest(BaseModel):
    """转账请求"""
    from_user: str
    to_user: str
    amount: float
    currency: str = "SWT"


# 内存存储
_balances = {}
_transactions = []


@router.get("/balance/{user_id}", response_model=BalanceResponse)
async def get_balance(user_id: str):
    """获取余额"""
    if user_id not in _balances:
        _balances[user_id] = {
            "user_id": user_id,
            "balance": 1000.0,  # 初始余额
            "currency": "SWT",
            "last_updated": datetime.now().isoformat()
        }
    
    return BalanceResponse(**_balances[user_id])


@router.post("/transfer")
async def transfer(transfer_req: TransferRequest):
    """转账"""
    # 检查发送方余额
    if transfer_req.from_user not in _balances:
        _balances[transfer_req.from_user] = {
            "user_id": transfer_req.from_user,
            "balance": 1000.0,
            "currency": "SWT",
            "last_updated": datetime.now().isoformat()
        }
    
    if _balances[transfer_req.from_user]["balance"] < transfer_req.amount:
        raise HTTPException(status_code=400, detail="余额不足")
    
    # 执行转账
    _balances[transfer_req.from_user]["balance"] -= transfer_req.amount
    _balances[transfer_req.from_user]["last_updated"] = datetime.now().isoformat()
    
    if transfer_req.to_user not in _balances:
        _balances[transfer_req.to_user] = {
            "user_id": transfer_req.to_user,
            "balance": 0.0,
            "currency": "SWT",
            "last_updated": datetime.now().isoformat()
        }
    
    _balances[transfer_req.to_user]["balance"] += transfer_req.amount
    _balances[transfer_req.to_user]["last_updated"] = datetime.now().isoformat()
    
    # 记录交易
    transaction = {
        "id": f"tx_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(_transactions)}",
        "from": transfer_req.from_user,
        "to": transfer_req.to_user,
        "amount": transfer_req.amount,
        "currency": transfer_req.currency,
        "timestamp": datetime.now().isoformat()
    }
    _transactions.append(transaction)
    
    return {
        "status": "success",
        "transaction": transaction
    }


@router.get("/transactions")
async def get_transactions(
    user_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100)
):
    """获取交易记录"""
    results = _transactions
    
    if user_id:
        results = [t for t in results if t["from"] == user_id or t["to"] == user_id]
    
    return {
        "transactions": results[-limit:],
        "total": len(results)
    }


@router.get("/market/stats")
async def get_market_stats():
    """获取市场统计"""
    return {
        "total_users": len(_balances),
        "total_transactions": len(_transactions),
        "total_volume": sum(t["amount"] for t in _transactions),
        "currency": "SWT"
    }
