#!/usr/bin/env python3
"""
内存分析器 - Phase 7 性能优化
功能：内存使用监控、泄漏检测、优化建议
"""

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import gc
import tracemalloc
import linecache
import psutil
import os
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path


class MemoryProfiler:
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.snapshots = []
        self.baseline = None
    
    def get_memory_usage(self) -> Dict[str, Any]:
        mem_info = self.process.memory_info()
        return {
            'rss_mb': round(mem_info.rss / 1024 / 1024, 2),
            'vms_mb': round(mem_info.vms / 1024 / 1024, 2),
            'percent': round(self.process.memory_percent(), 2),
            'timestamp': datetime.now().isoformat()
        }
    
    def start_tracing(self):
        tracemalloc.start(25)
        self.baseline = tracemalloc.take_snapshot()
        print("[MemoryProfiler] Tracing started")
    
    def stop_tracing(self):
        tracemalloc.stop()
        print("[MemoryProfiler] Tracing stopped")
    
    def take_snapshot(self, label: str = ""):
        snapshot = tracemalloc.take_snapshot()
        self.snapshots.append({
            'label': label,
            'snapshot': snapshot,
            'time': datetime.now(),
            'memory': self.get_memory_usage()
        })
        print(f"[MemoryProfiler] Snapshot taken: {label or 'unnamed'}")
        return snapshot
    
    def get_top_allocations(self, limit: int = 10) -> List[Dict[str, Any]]:
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        results = []
        for stat in top_stats[:limit]:
            frame = stat.traceback[0]
            line = linecache.getline(frame.filename, frame.lineno).strip()
            results.append({
                'file': frame.filename,
                'line': frame.lineno,
                'code': line[:50],
                'size_kb': round(stat.size / 1024, 2),
                'count': stat.count
            })
        return results
    
    def compare_snapshots(self, idx1: int = 0, idx2: int = -1) -> Dict[str, Any]:
        if len(self.snapshots) < 2:
            return {'error': 'Need at least 2 snapshots'}
        snap1 = self.snapshots[idx1]
        snap2 = self.snapshots[idx2]
        mem1 = snap1['memory']['rss_mb']
        mem2 = snap2['memory']['rss_mb']
        diff = mem2 - mem1
        time_diff = (snap2['time'] - snap1['time']).total_seconds()
        return {
            'snapshot1': snap1['label'],
            'snapshot2': snap2['label'],
            'memory1_mb': mem1,
            'memory2_mb': mem2,
            'diff_mb': round(diff, 2),
            'time_diff_s': round(time_diff, 2),
            'leak_rate_mb_per_s': round(diff / time_diff, 4) if time_diff > 0 else 0
        }
    
    def detect_leaks(self, threshold_mb: float = 10.0) -> List[Dict[str, Any]]:
        leaks = []
        for i in range(len(self.snapshots) - 1):
            comp = self.compare_snapshots(i, i + 1)
            if comp.get('diff_mb', 0) > threshold_mb:
                leaks.append({
                    'from': comp['snapshot1'],
                    'to': comp['snapshot2'],
                    'leak_mb': comp['diff_mb'],
                    'rate_mb_per_s': comp['leak_rate_mb_per_s']
                })
        return leaks
    
    def get_gc_stats(self) -> Dict[str, Any]:
        gc.collect()
        return {
            'gc_enabled': gc.isenabled(),
            'objects_tracked': len(gc.get_objects()),
            'gc_counts': gc.get_count(),
            'gc_threshold': gc.get_threshold()
        }
    
    def find_circular_refs(self) -> List[str]:
        gc.collect()
        garbage = gc.garbage
        return [str(type(obj)) for obj in garbage[:10]]
    
    def get_memory_trend(self) -> List[Dict[str, Any]]:
        return [
            {
                'label': snap['label'],
                'memory_mb': snap['memory']['rss_mb'],
                'time': snap['time'].isoformat()
            }
            for snap in self.snapshots
        ]
    
    def get_optimization_suggestions(self) -> List[str]:
        suggestions = []
        mem_usage = self.get_memory_usage()
        if mem_usage['rss_mb'] > 500:
            suggestions.append("High memory usage (>500MB). Consider optimizing data structures.")
        if len(self.snapshots) > 1:
            leaks = self.detect_leaks()
            if leaks:
                suggestions.append(f"Memory leak detected: {len(leaks)} instances")
        gc_stats = self.get_gc_stats()
        if gc_stats['objects_tracked'] > 100000:
            suggestions.append("Many objects tracked. Check for circular references.")
        if not suggestions:
            suggestions.append("Memory usage looks healthy!")
        return suggestions


memory_profiler = MemoryProfiler()


async def demo():
    print("=" * 60)
    print("Memory Profiler Demo - Phase 7")
    print("=" * 60)
    profiler = MemoryProfiler()
    print(f"\nInitial memory usage:")
    mem = profiler.get_memory_usage()
    print(f"  RSS: {mem['rss_mb']} MB")
    print(f"  VMS: {mem['vms_mb']} MB")
    print(f"  Percent: {mem['percent']}%")
    print(f"\nGC stats:")
    gc_stats = profiler.get_gc_stats()
    print(f"  Objects tracked: {gc_stats['objects_tracked']}")
    print(f"  GC counts: {gc_stats['gc_counts']}")
    print(f"\nStart tracing...")
    profiler.start_tracing()
    print(f"\nTake snapshot 1...")
    profiler.take_snapshot("initial")
    data = []
    print(f"\nAllocating memory (10000 items)...")
    for i in range(10000):
        data.append({'id': i, 'data': 'x' * 100})
    print(f"\nTake snapshot 2...")
    profiler.take_snapshot("after_allocation")
    print(f"\nMemory trend:")
    for entry in profiler.get_memory_trend():
        print(f"  {entry['label']}: {entry['memory_mb']} MB")
    print(f"\nCompare snapshots:")
    comp = profiler.compare_snapshots()
    print(f"  Memory diff: {comp['diff_mb']} MB")
    print(f"  Time diff: {comp['time_diff_s']} s")
    print(f"\nTop allocations:")
    for alloc in profiler.get_top_allocations(5):
        print(f"  {alloc['file']}:{alloc['line']} - {alloc['size_kb']} KB ({alloc['count']} objects)")
    print(f"\nLeak detection:")
    leaks = profiler.detect_leaks(threshold_mb=1.0)
    if leaks:
        for leak in leaks:
            print(f"  {leak['from']} -> {leak['to']}: {leak['leak_mb']} MB")
    else:
        print("  No significant leaks detected")
    print(f"\nOptimization suggestions:")
    for suggestion in profiler.get_optimization_suggestions():
        print(f"  - {suggestion}")
    profiler.stop_tracing()
    return profiler.get_memory_usage()


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo())
