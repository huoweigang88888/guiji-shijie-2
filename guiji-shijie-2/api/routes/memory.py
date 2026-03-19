#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆管理 API

提供记忆存储、查询、搜索等功能
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

router = APIRouter(prefix="/api/v1/memory", tags=["Memory"])


class MemoryCreate(BaseModel):
    """创建记忆请求"""
    content: str
    agent_id: str
    memory_type: str = "long_term"  # short_term, long_term, semantic
    metadata: Optional[Dict[str, Any]] = None


class MemoryResponse(BaseModel):
    """记忆响应"""
    id: str
    content: str
    agent_id: str
    memory_type: str
    created_at: str
    metadata: Optional[Dict[str, Any]] = None


# 内存存储（实际应该用数据库）
_memories = {}


@router.post("/", response_model=MemoryResponse)
async def create_memory(memory: MemoryCreate):
    """创建记忆"""
    memory_id = f"mem_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(_memories)}"
    
    memory_data = {
        "id": memory_id,
        "content": memory.content,
        "agent_id": memory.agent_id,
        "memory_type": memory.memory_type,
        "created_at": datetime.now().isoformat(),
        "metadata": memory.metadata or {}
    }
    
    _memories[memory_id] = memory_data
    
    return MemoryResponse(**memory_data)


@router.get("/{memory_id}", response_model=MemoryResponse)
async def get_memory(memory_id: str):
    """获取记忆"""
    if memory_id not in _memories:
        raise HTTPException(status_code=404, detail="记忆不存在")
    
    return MemoryResponse(**_memories[memory_id])


@router.get("/", response_model=List[MemoryResponse])
async def list_memories(
    agent_id: Optional[str] = Query(None, description="代理 ID"),
    memory_type: Optional[str] = Query(None, description="记忆类型"),
    limit: int = Query(50, ge=1, le=100)
):
    """列出记忆"""
    results = list(_memories.values())
    
    if agent_id:
        results = [m for m in results if m["agent_id"] == agent_id]
    
    if memory_type:
        results = [m for m in results if m["memory_type"] == memory_type]
    
    return [MemoryResponse(**m) for m in results[-limit:]]


@router.delete("/{memory_id}")
async def delete_memory(memory_id: str):
    """删除记忆"""
    if memory_id not in _memories:
        raise HTTPException(status_code=404, detail="记忆不存在")
    
    del _memories[memory_id]
    return {"status": "success", "message": "记忆已删除"}


@router.post("/search")
async def search_memories(
    query: str,
    agent_id: Optional[str] = None,
    limit: int = 10
):
    """搜索记忆"""
    results = []
    
    for memory in _memories.values():
        if query.lower() in memory["content"].lower():
            if agent_id is None or memory["agent_id"] == agent_id:
                results.append(memory)
    
    return {
        "query": query,
        "results": results[:limit],
        "total": len(results)
    }
