#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查看硅基世界 2

让人类作为观察者，看到 Agent 们的生活、工作、交流。
"""

import asyncio
import sys
from datetime import datetime

# 添加项目路径
sys.path.insert(0, '.')

from agents.roles.ceo_agent import create_ceo_agent
from agents.roles.pm_agent import create_pm_agent
from agents.roles.arch_agent import create_arch_agent
from agents.roles.dev_agent import create_dev_agent
from agents.roles.qa_agent import create_qa_agent
from world.map import get_world_map
from world.message_bus import get_message_bus
from world.activity_manager import get_activity_manager


async def observe_world(duration: int = 30):
    """
    观察世界
    
    Args:
        duration: 观察时长（秒）
    """
    print("=" * 60)
    print("👁️  硅基世界 2 观察模式")
    print("=" * 60)
    print()
    
    # 获取单例
    world_map = get_world_map()
    message_bus = get_message_bus()
    activity_manager = get_activity_manager()
    
    # 创建 Agent（只用于观察，不运行消息循环）
    agents = {
        "CEO-Agent": create_ceo_agent(),
        "PM-Agent": create_pm_agent(),
        "ARCH-Agent": create_arch_agent(),
        "DEV-Agent": create_dev_agent(),
        "QA-Agent": create_qa_agent(),
    }
    
    # 注册到消息总线和世界地图
    for agent_id in agents:
        message_bus.register_agent(agent_id)
        world_map.spawn_agent(agent_id)
    
    print(f"👁️  开始观察，共 {duration} 秒")
    print()
    
    # 观察循环
    for i in range(duration):
        # 每 5 秒显示一次状态
        if i % 5 == 0:
            print(f"\n📅 时间：{i} 秒")
            
            # 显示消息统计
            msg_stats = message_bus.get_stats()
            print(f"  📬 消息总数：{msg_stats['total_messages']}")
            
            # 显示区域分布
            map_stats = world_map.get_region_stats()
            print("  🏛️  区域分布:")
            for region_id, stats in map_stats.items():
                if stats['count'] > 0:
                    print(f"    - {stats['name']}: {stats['count']} 人")
            
            # 显示活动统计
            act_stats = activity_manager.get_stats()
            print(f"  📅 活动：{act_stats['scheduled']} 个待开始，{act_stats['ongoing']} 个进行中")
            
            # 显示 Agent 状态
            print("  👥 Agent 状态:")
            for agent_id, agent in agents.items():
                status = agent.get_status()
                print(f"    - {status['name']}: {status['status']} ({status['role']})")
        
        # 模拟消息交流
        if i % 10 == 0 and i > 0:
            # 模拟 Agent 发送消息
            import random
            
            sender = random.choice(list(agents.keys()))
            receiver = random.choice(list(agents.keys()))
            
            if sender != receiver:
                await message_bus.send(
                    sender_id=sender,
                    receiver_id=receiver,
                    message_type="status",
                    content={
                        "subject": f"{sender} 的状态更新",
                        "task_id": "task_001",
                        "status": "in_progress",
                        "progress": 50,
                    },
                )
            
            # 模拟知识分享
            if random.random() > 0.5:
                await message_bus.send(
                    sender_id="PM-Agent",
                    receiver_id="all",
                    message_type="knowledge",
                    content={
                        "knowledge_type": "user_research",
                        "summary": "用户对界面一致性非常重视",
                    },
                )
        
        await asyncio.sleep(1)
    
    # 清理
    for agent_id in agents:
        message_bus.unregister_agent(agent_id)
    
    print()
    print("=" * 60)
    print("👁️  观察结束")
    print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(observe_world(duration=30))
    except KeyboardInterrupt:
        print("\n👋 观察暂停，下次再见！")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
