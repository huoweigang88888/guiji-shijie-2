#!/usr/bin/env python3
"""
数据库连接池优化模块 - Phase 7 性能优化
"""

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import asyncio
import time
from typing import Optional, Dict, Any, List
from datetime import datetime
from contextlib import asynccontextmanager
from pathlib import Path


class DatabaseConnection:
    def __init__(self, connection_id: int):
        self.id = connection_id
        self.created_at = datetime.now()
        self.last_used = datetime.now()
        self.in_use = False
        self.query_count = 0
        self.total_query_time = 0.0
        self.is_alive = True
    
    def use(self):
        self.in_use = True
        self.last_used = datetime.now()
    
    def release(self):
        self.in_use = False
        self.last_used = datetime.now()
    
    def record_query(self, duration: float):
        self.query_count += 1
        self.total_query_time += duration
    
    @property
    def avg_query_time(self) -> float:
        return self.total_query_time / self.query_count if self.query_count > 0 else 0.0
    
    @property
    def idle_time(self) -> float:
        return (datetime.now() - self.last_used).total_seconds()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'last_used': self.last_used.isoformat(),
            'in_use': self.in_use,
            'query_count': self.query_count,
            'avg_query_time_ms': self.avg_query_time * 1000,
            'idle_time_s': self.idle_time,
            'is_alive': self.is_alive
        }


class DatabasePool:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self.pool: List[DatabaseConnection] = []
            self.max_connections = 20
            self.min_connections = 5
            self.connection_timeout = 30
            self.idle_timeout = 300
            self.current_connection_id = 0
            self.stats = {
                'total_queries': 0,
                'total_query_time': 0.0,
                'pool_hits': 0,
                'pool_misses': 0,
                'connection_creates': 0,
                'connection_closes': 0
            }
            self._initialize_min_connections()
    
    def _initialize_min_connections(self):
        for _ in range(self.min_connections):
            conn = self._create_connection()
            self.pool.append(conn)
    
    def _create_connection(self) -> DatabaseConnection:
        self.current_connection_id += 1
        self.stats['connection_creates'] += 1
        conn = DatabaseConnection(self.current_connection_id)
        print(f"[DBPool] Create connection #{conn.id}")
        return conn
    
    def _close_connection(self, conn: DatabaseConnection):
        self.stats['connection_closes'] += 1
        print(f"[DBPool] Close connection #{conn.id}")
    
    async def acquire(self, timeout: float = None) -> DatabaseConnection:
        if timeout is None:
            timeout = self.connection_timeout
        start_time = time.time()
        while True:
            for conn in self.pool:
                if not conn.in_use and conn.is_alive:
                    conn.use()
                    self.stats['pool_hits'] += 1
                    self.stats['total_queries'] += 1
                    return conn
            active_connections = sum(1 for c in self.pool if c.in_use)
            if len(self.pool) < self.max_connections:
                conn = self._create_connection()
                conn.use()
                self.pool.append(conn)
                self.stats['pool_misses'] += 1
                self.stats['total_queries'] += 1
                return conn
            elapsed = time.time() - start_time
            if elapsed >= timeout:
                raise TimeoutError(f"Get connection timeout ({timeout}s)")
            await asyncio.sleep(0.1)
    
    def release(self, conn: DatabaseConnection):
        conn.release()
    
    @asynccontextmanager
    async def get_connection(self):
        conn = await self.acquire()
        try:
            yield conn
        finally:
            self.release(conn)
    
    async def execute(self, query: str, params: tuple = None):
        async with self.get_connection() as conn:
            start_time = time.time()
            await asyncio.sleep(0.001)
            duration = time.time() - start_time
            conn.record_query(duration)
            self.stats['total_query_time'] += duration
            return {'status': 'success', 'duration': duration}
    
    def cleanup_idle_connections(self):
        connections_to_remove = []
        for conn in self.pool:
            if not conn.in_use and conn.idle_time > self.idle_timeout:
                if len(self.pool) - len(connections_to_remove) > self.min_connections:
                    connections_to_remove.append(conn)
        for conn in connections_to_remove:
            self._close_connection(conn)
            self.pool.remove(conn)
        if connections_to_remove:
            print(f"[DBPool] Cleanup {len(connections_to_remove)} idle connections")
    
    def get_stats(self) -> Dict[str, Any]:
        active = sum(1 for c in self.pool if c.in_use)
        idle = len(self.pool) - active
        avg_query_time = 0.0
        if self.stats['total_queries'] > 0:
            avg_query_time = self.stats['total_query_time'] / self.stats['total_queries']
        pool_hit_rate = 0.0
        total_ops = self.stats['pool_hits'] + self.stats['pool_misses']
        if total_ops > 0:
            pool_hit_rate = self.stats['pool_hits'] / total_ops * 100
        return {
            'pool_size': len(self.pool),
            'active_connections': active,
            'idle_connections': idle,
            'max_connections': self.max_connections,
            'min_connections': self.min_connections,
            'total_queries': self.stats['total_queries'],
            'avg_query_time_ms': avg_query_time * 1000,
            'pool_hit_rate': pool_hit_rate,
            'connection_creates': self.stats['connection_creates'],
            'connection_closes': self.stats['connection_closes']
        }
    
    def get_connection_details(self) -> List[Dict[str, Any]]:
        return [conn.to_dict() for conn in self.pool]
    
    async def health_check(self):
        for conn in self.pool:
            if conn.in_use and conn.idle_time > self.connection_timeout * 2:
                print(f"[DBPool] Warning: Connection #{conn.id} may leak")
        self.cleanup_idle_connections()


db_pool = DatabasePool()


async def demo():
    print("=" * 60)
    print("Database Connection Pool Demo - Phase 7")
    print("=" * 60)
    pool = DatabasePool()
    stats = pool.get_stats()
    print(f"\nInitial state:")
    print(f"  Pool size: {stats['pool_size']}")
    print(f"  Idle connections: {stats['idle_connections']}")
    print(f"\nExecute 10 concurrent queries...")
    async def run_query(query_id):
        async with pool.get_connection() as conn:
            result = await pool.execute(f"SELECT * FROM table WHERE id = {query_id}")
            return result
    tasks = [run_query(i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    print(f"  Completed {len(results)} queries")
    print(f"\nFinal stats:")
    stats = pool.get_stats()
    print(f"  Pool size: {stats['pool_size']}")
    print(f"  Active connections: {stats['active_connections']}")
    print(f"  Total queries: {stats['total_queries']}")
    print(f"  Avg query time: {stats['avg_query_time_ms']:.2f}ms")
    print(f"  Pool hit rate: {stats['pool_hit_rate']:.1f}%")
    return stats


if __name__ == "__main__":
    asyncio.run(demo())
