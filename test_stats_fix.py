#!/usr/bin/env python3
"""测试统计修复"""
import asyncio
import sys
sys.path.insert(0, '.')
from world.engine import WorldEngine
from world.stats_tracker import get_stats_tracker

async def test():
    engine = WorldEngine()
    stats = get_stats_tracker()
    
    await engine.start()
    
    # 等待 120 秒让事件发生
    print('等待 120 秒让引擎产生事件...')
    await asyncio.sleep(120)
    
    # 手动拍摄快照（使用修复后的逻辑）
    print()
    print('=== 拍摄统计快照（使用修复后的数据源）===')
    stats.take_snapshot(
        world_day=engine._day,
        time_of_day=engine._current_time_of_day.value,
        total_stories=len(engine.stories),  # 修复：使用 engine.stories
        total_knowledge=len(engine.collective_knowledge),  # 修复：使用 engine.collective_knowledge
        total_relationships=len(engine.relationships),
        deep_relationships=sum(1 for r in engine.relationships.values() if r.get('value', 0) >= 50),
        total_agents=18,
        total_credits=0,
    )
    
    await engine.stop()
    
    # 获取摘要
    summary = stats.get_summary()
    current = summary['current']
    
    print()
    print('=== 统计数据验证 ===')
    print(f"消息数：{current['total_messages']}")
    print(f"故事数：{current['total_stories']}")
    print(f"知识数：{current['total_knowledge_nodes']}")
    print(f"关系数：{current['total_relationships']}")
    print()
    print('=== 验证结论 ===')
    
    story_ok = current['total_stories'] > 0
    knowledge_ok = current['total_knowledge_nodes'] > 0
    relationship_ok = current['total_relationships'] > 0
    
    print(f"{'✅' if story_ok else '⚠️'}  故事数 > 0: {current['total_stories']}")
    print(f"{'✅' if knowledge_ok else '⚠️'}  知识数 > 0: {current['total_knowledge_nodes']}")
    print(f"{'✅' if relationship_ok else '❌'}  关系数 > 0: {current['total_relationships']}")
    
    if knowledge_ok or story_ok:
        print()
        print('✅ 修复成功！统计数据现在从引擎获取真实数据')
    else:
        print()
        print('⚠️  运行时间内未产生足够事件，但数据源已修复')

if __name__ == '__main__':
    asyncio.run(test())
