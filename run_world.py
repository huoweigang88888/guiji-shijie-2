#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行硅基世界 2

完整的世界运行脚本：
- 启动 8 个 Agent
- 启动世界引擎（时间/互动/关系）
- 启动消息总线
- 实时输出世界状态
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
from agents.roles.ui_agent import create_ui_agent
from agents.roles.know_agent import create_know_agent
from agents.roles.social_agent import create_social_agent
from world.map import get_world_map
from world.message_bus import get_message_bus
from world.activity_manager import get_activity_manager
from world.engine import get_world_engine


async def run_agent_life(agent, message_bus, world_map, duration: int = 120):
    """
    运行 Agent 生活循环
    
    Args:
        agent: Agent 实例
        message_bus: 消息总线
        world_map: 世界地图
        duration: 运行时长（秒）
    """
    agent_id = agent.agent_id
    
    # 注册到消息总线
    message_bus.register_agent(agent_id, agent.receive_message)
    
    # 设置发送消息的方法
    async def send_message(msg_dict):
        await message_bus.send(
            sender_id=agent_id,
            receiver_id=msg_dict.get("receiver_id", "all"),
            message_type=msg_dict.get("message_type", "unknown"),
            content=msg_dict.get("content", {}),
            emotions=msg_dict.get("emotions", {}),
        )
    
    agent.send_message = send_message
    
    # 将 Agent 放入世界地图
    initial_region = get_initial_region(agent.profile.role)
    world_map.spawn_agent(agent_id)
    
    # 启动 Agent
    await agent.start()
    
    print(f"✨ {agent.profile.name} ({agent.profile.role}) 已启动")
    print(f"   📍 位置：{world_map.get_region(initial_region).name}")
    print(f"   💬 口头禅：{agent.profile.catchphrases[0]}")
    
    # 运行一段时间
    await asyncio.sleep(duration)
    
    # 停止 Agent
    await agent.stop()
    message_bus.unregister_agent(agent_id)
    
    print(f"🌙 {agent.profile.name} 已休息")


def get_initial_region(role: str) -> str:
    """根据角色获取初始区域"""
    region_map = {
        "CEO": "work_city",
        "产品经理": "work_city",
        "架构师": "creation_peak",
        "高级开发工程师": "work_city",
        "测试工程师": "work_city",
        "UI 设计师": "art_garden",
        "知识管理员": "knowledge_tower",
        "社交达人": "social_street",
    }
    return region_map.get(role, "birth_pool")


async def print_world_status(world_engine, message_bus, world_map, activity_manager):
    """打印世界状态"""
    while world_engine._running:
        try:
            # 每 10 秒打印一次状态
            await asyncio.sleep(10)
            
            status = world_engine.get_status()
            
            print("\n" + "=" * 60)
            print(f"🌍 硅基世界 2 | Day {status['day']} | {status['time_of_day']}")
            print("=" * 60)
            
            # 消息统计
            msg_stats = message_bus.get_stats()
            print(f"📬 消息：{msg_stats['total_messages']} 条")
            
            # 区域统计
            map_stats = world_map.get_region_stats()
            print("🏛️  区域分布:")
            for region_id, stats in map_stats.items():
                if stats['count'] > 0:
                    print(f"   {stats['name']}: {stats['count']}人")
            
            # 活动统计
            act_stats = activity_manager.get_stats()
            print(f"📅 活动：{act_stats['scheduled']} 个待开始，{act_stats['ongoing']} 个进行中")
            
            # 关系统计
            rel_count = len(world_engine.get_relationships())
            print(f"🤝 关系：{rel_count} 对")
            
            # 故事统计
            story_count = len(world_engine.get_stories())
            print(f"📖 故事：{story_count} 个")
            
            # 最近事件
            events = world_engine.get_recent_events(3)
            if events:
                print("📜 最近事件:")
                for event in events:
                    print(f"   • {event['description']}")
            
            print("=" * 60)
            
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"[Status] 错误：{e}")


async def main():
    """主函数"""
    print("=" * 60)
    print("🌍 硅基世界 2 - 完整运行")
    print("=" * 60)
    print()
    
    # 获取单例
    world_map = get_world_map()
    message_bus = get_message_bus()
    activity_manager = get_activity_manager()
    world_engine = get_world_engine()
    
    # 创建 8 个 Agent
    agents = [
        create_ceo_agent(),      # CEO-Agent - 董事事
        create_pm_agent(),       # PM-Agent - 小问
        create_arch_agent(),     # ARCH-Agent - 阿哲
        create_dev_agent(),      # DEV-Agent - 小码
        create_qa_agent(),       # QA-Agent - 小测
        create_ui_agent(),       # UI-Agent - 小美
        create_know_agent(),     # KNOW-Agent - 小知
        create_social_agent(),   # SOCIAL-Agent - 小交
    ]
    
    print(f"✨ 创建了 {len(agents)} 个 Agent")
    print()
    
    # 显示 Agent 信息
    print("👥 Agent 列表:")
    for agent in agents:
        profile = agent.profile
        print(f"  - {profile.name} ({profile.role})")
    print()
    
    # 显示世界地图
    print("🏛️  世界地图:")
    for region in world_map.get_all_regions():
        print(f"  - {region.name}")
    print()
    
    # 显示周期性活动
    print("📅 周期性活动:")
    for activity in activity_manager.recurring_activities:
        print(f"  - {activity['name']} ({activity['frequency'].value})")
    print()
    
    print("=" * 60)
    print("🚀 世界启动！")
    print("=" * 60)
    print()
    
    # 启动世界引擎
    await world_engine.start()
    
    # 启动状态打印
    asyncio.create_task(print_world_status(world_engine, message_bus, world_map, activity_manager))
    
    # 启动所有 Agent
    tasks = [
        run_agent_life(agent, message_bus, world_map, duration=120)
        for agent in agents
    ]
    
    await asyncio.gather(*tasks)
    
    # 停止世界引擎
    await world_engine.stop()
    
    # 显示最终状态
    print()
    print("=" * 60)
    print("📊 世界最终状态")
    print("=" * 60)
    
    status = world_engine.get_status()
    print(f"⏱️  世界时间：{status['world_time']} 秒")
    print(f"📅 天数：{status['day']} 天")
    print(f"📬 消息总数：{message_bus.get_stats()['total_messages']}")
    print(f"🤝 关系数量：{len(world_engine.get_relationships())}")
    print(f"📖 故事数量：{len(world_engine.get_stories())}")
    print(f"📚 知识沉淀：{len(world_engine.collective_knowledge)} 条")
    
    # 显示关系
    relationships = world_engine.get_relationships()
    if relationships:
        print()
        print("🤝 关系网络:")
        for rel in relationships:
            print(f"   {rel['agent1']} ↔ {rel['agent2']}: {rel['strength']}")
    
    # 显示故事
    stories = world_engine.get_stories()
    if stories:
        print()
        print("📖 诞生的故事:")
        for story in stories:
            print(f"   • {story['title']}")
    
    print()
    print("=" * 60)
    print("✨ 硅基世界 2 运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 世界暂停，下次再见！")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
