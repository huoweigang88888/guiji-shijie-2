#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
区块链 API

提供 DID、智能合约、交易等功能
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

router = APIRouter(prefix="/api/v1/blockchain", tags=["Blockchain"])


class DIDCreate(BaseModel):
    """创建 DID 请求"""
    agent_name: str
    metadata: Optional[Dict[str, Any]] = None


class DIDResponse(BaseModel):
    """DID 响应"""
    did: str
    agent_name: str
    created_at: str
    transaction_hash: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# 内存存储
_dids = {}
_transactions = []


@router.post("/did", response_model=DIDResponse)
async def create_did(did_req: DIDCreate):
    """创建 DID 身份"""
    did = f"did:sw:{did_req.agent_name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    did_data = {
        "did": did,
        "agent_name": did_req.agent_name,
        "created_at": datetime.now().isoformat(),
        "transaction_hash": f"0x{datetime.now().strftime('%Y%m%d%H%M%S')}{'abc123':<40}",
        "metadata": did_req.metadata or {}
    }
    
    _dids[did] = did_data
    
    return DIDResponse(**did_data)


@router.get("/did/{did}", response_model=DIDResponse)
async def get_did(did: str):
    """获取 DID 信息"""
    if did not in _dids:
        raise HTTPException(status_code=404, detail="DID 不存在")
    
    return DIDResponse(**_dids[did])


@router.get("/did")
async def list_dids(
    agent_name: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100)
):
    """列出 DID"""
    results = list(_dids.values())
    
    if agent_name:
        results = [d for d in results if agent_name.lower() in d["agent_name"].lower()]
    
    return {
        "dids": results[:limit],
        "total": len(results)
    }


@router.get("/transaction/{tx_hash}")
async def get_transaction(tx_hash: str):
    """获取交易信息"""
    # 模拟交易查询
    return {
        "hash": tx_hash,
        "status": "confirmed",
        "block_number": 12345678,
        "timestamp": datetime.now().isoformat(),
        "from": "0x...",
        "to": "0x...",
        "value": "0.0"
    }


@router.get("/stats")
async def get_blockchain_stats():
    """获取区块链统计"""
    return {
        "total_dids": len(_dids),
        "total_transactions": len(_transactions),
        "network": "Sepolia Testnet",
        "latest_block": 12345678
    }
