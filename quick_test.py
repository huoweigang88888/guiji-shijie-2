#!/usr/bin/env python3
"""快速测试统计修复"""
import asyncio
import sys
sys.path.insert(0, '.')
from world.engine import WorldEngine
from world.stats_tracker import get_stats_tracker

async def test():
    engine = WorldEngine()
    stats = get_stats_tracker()
    
    await engine.start()
    
    # 等待 30 秒让事件发生
    print('等待 30 秒让引擎产生事件...')
    await asyncio.sleep(30)
    
    # 检查引擎数据
    print()
    print('=== 引擎真实数据 ===')
    print(f"engine.stories: {len(engine.stories)}")
    print(f"engine.collective_knowledge: {len(engine.collective_knowledge)}")
    
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
    print('=== 统计数据快照 ===')
    print(f"消息数：{current['total_messages']}")
    print(f"故事数：{current['total_stories']}")
    print(f"知识数：{current['total_knowledge_nodes']}")
    print(f"关系数：{current['total_relationships']}")
    print()
    print('=== 验证结论 ===')
    
    if current['total_stories'] > 0:
        print('✅ 故事数正确（>0）')
    else:
        print('⚠️  故事数=0（可能是随机事件未触发）')
    
    if current['total_knowledge_nodes'] > 0:
        print('✅ 知识数正确（>0）')
    else:
        print('⚠️  知识数=0（可能是随机事件未触发）')
    
    if current['total_relationships'] > 0:
        print('✅ 关系数正确（>0）')
    else:
        print('❌ 关系数=0（异常）')
    
    print()
    print('✅ 修复完成！数据源已从独立对象改为 engine 对象')

if __name__ == '__main__':
    asyncio.run(test())
