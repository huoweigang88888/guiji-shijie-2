#!/usr/bin/env python3
"""
API 响应缓存管理器 - Phase 7 性能优化
功能：缓存热点数据，减少重复计算和数据库查询
"""

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import asyncio
import time
import hashlib
import json
from typing import Any, Dict, Optional, List, Callable
from datetime import datetime, timedelta
from pathlib import Path
from functools import wraps


class CacheEntry:
    def __init__(self, key: str, value: Any, ttl: int):
        self.key = key
        self.value = value
        self.created_at = time.time()
        self.ttl = ttl
        self.hit_count = 0
        self.last_accessed = time.time()
    
    def is_expired(self) -> bool:
        return time.time() - self.created_at > self.ttl
    
    def access(self):
        self.hit_count += 1
        self.last_accessed = time.time()
    
    @property
    def age(self) -> float:
        return time.time() - self.created_at
    
    @property
    def remaining_ttl(self) -> float:
        return max(0, self.ttl - self.age)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'key': self.key,
            'value': str(self.value)[:100] + '...' if len(str(self.value)) > 100 else str(self.value),
            'age_s': round(self.age, 2),
            'remaining_ttl_s': round(self.remaining_ttl, 2),
            'hit_count': self.hit_count,
            'last_accessed': datetime.fromtimestamp(self.last_accessed).isoformat()
        }


class CacheManager:
    def __init__(self, max_size: int = 1000, default_ttl: int = 300):
        self.cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'deletes': 0,
            'evictions': 0
        }
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        key_data = f"{prefix}:{args}:{sorted(kwargs.items())}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        entry = self.cache.get(key)
        if entry is None:
            self.stats['misses'] += 1
            return None
        if entry.is_expired():
            del self.cache[key]
            self.stats['misses'] += 1
            return None
        entry.access()
        self.stats['hits'] += 1
        return entry.value
    
    def set(self, key: str, value: Any, ttl: int = None):
        if ttl is None:
            ttl = self.default_ttl
        if len(self.cache) >= self.max_size:
            self._evict()
        self.cache[key] = CacheEntry(key, value, ttl)
        self.stats['sets'] += 1
    
    def delete(self, key: str):
        if key in self.cache:
            del self.cache[key]
            self.stats['deletes'] += 1
    
    def _evict(self):
        if not self.cache:
            return
        lru_key = min(self.cache.keys(), key=lambda k: self.cache[k].last_accessed)
        del self.cache[lru_key]
        self.stats['evictions'] += 1
    
    def clear(self):
        self.cache.clear()
    
    def cleanup_expired(self):
        expired_keys = [k for k, v in self.cache.items() if v.is_expired()]
        for key in expired_keys:
            del self.cache[key]
        if expired_keys:
            print(f"[Cache] Cleaned up {len(expired_keys)} expired entries")
    
    def get_stats(self) -> Dict[str, Any]:
        total = self.stats['hits'] + self.stats['misses']
        hit_rate = (self.stats['hits'] / total * 100) if total > 0 else 0
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'hit_rate': round(hit_rate, 2),
            'sets': self.stats['sets'],
            'deletes': self.stats['deletes'],
            'evictions': self.stats['evictions'],
            'memory_entries': len(self.cache)
        }
    
    def get_all_entries(self) -> List[Dict[str, Any]]:
        return [entry.to_dict() for entry in self.cache.values()]
    
    def get_hot_keys(self, limit: int = 10) -> List[Dict[str, Any]]:
        sorted_entries = sorted(self.cache.values(), key=lambda e: e.hit_count, reverse=True)
        return [e.to_dict() for e in sorted_entries[:limit]]


class APICache:
    def __init__(self, cache_manager: CacheManager = None):
        self.cache = cache_manager or CacheManager()
    
    def cached(self, ttl: int = 300, prefix: str = "api"):
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                cache_key = self.cache._generate_key(f"{prefix}:{func.__name__}", *args, **kwargs)
                cached_result = self.cache.get(cache_key)
                if cached_result is not None:
                    return cached_result
                result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
                self.cache.set(cache_key, result, ttl)
                return result
            return wrapper
        return decorator
    
    def invalidate_pattern(self, pattern: str):
        keys_to_delete = [k for k in self.cache.cache.keys() if pattern in k]
        for key in keys_to_delete:
            self.cache.delete(key)
        if keys_to_delete:
            print(f"[APICache] Invalidated {len(keys_to_delete)} keys matching '{pattern}'")


api_cache = APICache()
cache_manager = CacheManager()


async def demo():
    print("=" * 60)
    print("API Response Cache Demo - Phase 7")
    print("=" * 60)
    cache = CacheManager(max_size=100, default_ttl=60)
    print(f"\nInitial stats:")
    print(f"  Cache size: {cache.get_stats()['size']}")
    print(f"  Hit rate: {cache.get_stats()['hit_rate']}%")
    print(f"\nSimulating API calls...")
    async def mock_api_call(user_id: int):
        await asyncio.sleep(0.01)
        return {"user_id": user_id, "data": f"User {user_id} data", "timestamp": time.time()}
    for i in range(20):
        user_id = i % 5
        key = cache._generate_key("api:user", user_id)
        result = cache.get(key)
        if result is None:
            result = await mock_api_call(user_id)
            cache.set(key, result, ttl=300)
    print(f"\nAfter 20 API calls (5 unique users):")
    stats = cache.get_stats()
    print(f"  Cache size: {stats['size']}")
    print(f"  Hits: {stats['hits']}")
    print(f"  Misses: {stats['misses']}")
    print(f"  Hit rate: {stats['hit_rate']}%")
    print(f"\nHot keys:")
    for entry in cache.get_hot_keys(5):
        print(f"  Key: {entry['key'][:16]}... Hits: {entry['hit_count']}")
    print(f"\nPerformance improvement:")
    print(f"  Without cache: 20 calls * 10ms = 200ms")
    print(f"  With cache: ~15 cache hits * 0.1ms + 5 misses * 10ms = 51.5ms")
    print(f"  Improvement: ~74% faster")
    return stats


if __name__ == "__main__":
    asyncio.run(demo())
