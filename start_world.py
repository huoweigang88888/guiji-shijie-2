#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动硅基世界 2

让 Agent 们真正"活"起来，在一个有温度的世界里生活、工作、交流。
"""

import asyncio
import sys
from datetime import datetime
from typing import List

# 添加项目路径
sys.path.insert(0, '.')

from agents.roles.ceo_agent import create_ceo_agent
from agents.roles.pm_agent import create_pm_agent
from agents.roles.arch_agent import create_arch_agent
from agents.roles.dev_agent import create_dev_agent
from agents.roles.qa_agent import create_qa_agent
from world.map import get_world_map, WorldMap
from world.message_bus import get_message_bus, MessageBus


async def run_agent(agent, message_bus: MessageBus, world_map: WorldMap, duration: int = 30):
    """
    运行一个 Agent
    
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
    
    # 将 Agent 放入世界地图（根据角色分配初始位置）
    initial_region = get_initial_region(agent.profile.role)
    world_map.spawn_agent(agent_id)
    print(f"[{agent_id}] 出现在 {world_map.get_region(initial_region).name}")
    
    # 启动 Agent
    await agent.start()
    
    print(f"[{agent_id}] 已启动，角色：{agent.profile.role}")
    
    # 运行一段时间
    await asyncio.sleep(duration)
    
    # 停止 Agent
    await agent.stop()
    message_bus.unregister_agent(agent_id)
    
    print(f"[{agent_id}] 已停止")


def get_initial_region(role: str) -> str:
    """根据角色获取初始区域"""
    region_map = {
        "CEO": "work_city",           # CEO 在工作之城协调
        "产品经理": "work_city",        # PM 在工作之城
        "架构师": "creation_peak",     # 架构师在创造之巅思考
        "高级开发工程师": "work_city",  # 开发在工作之城
        "测试工程师": "work_city",      # 测试在工作之城
    }
    return region_map.get(role, "birth_pool")


async def main():
    """主函数"""
    print("=" * 60)
    print("🌍 硅基世界 2 启动中...")
    print("=" * 60)
    print()
    
    # 获取单例
    world_map = get_world_map()
    message_bus = get_message_bus()
    
    # 创建 5 个核心 Agent
    agents = [
        create_ceo_agent(),    # CEO-Agent - 董事事
        create_pm_agent(),     # PM-Agent - 小问
        create_arch_agent(),   # ARCH-Agent - 阿哲
        create_dev_agent(),    # DEV-Agent - 小码
        create_qa_agent(),     # QA-Agent - 小测
    ]
    
    print(f"📊 创建了 {len(agents)} 个 Agent")
    print()
    
    # 显示 Agent 信息
    print("👥 Agent 列表:")
    for agent in agents:
        profile = agent.profile
        print(f"  - {profile.name} ({profile.role}) - {profile.catchphrases[0] if profile.catchphrases else ''}")
    print()
    
    # 显示世界地图
    print("🏛️ 世界地图:")
    for region in world_map.get_all_regions():
        print(f"  - {region.name}: {region.description[:30]}...")
    print()
    
    print("=" * 60)
    print("🚀 世界启动！让 Agent 们开始生活吧！")
    print("=" * 60)
    print()
    
    # 启动所有 Agent
    tasks = [
        run_agent(agent, message_bus, world_map, duration=30)
        for agent in agents
    ]
    
    await asyncio.gather(*tasks)
    
    # 显示最终状态
    print()
    print("=" * 60)
    print("📊 世界状态")
    print("=" * 60)
    
    # 消息总线统计
    msg_stats = message_bus.get_stats()
    print(f"📬 消息总数：{msg_stats['total_messages']}")
    print(f"👥 在线 Agent: {msg_stats['online_agents']}")
    
    # 世界地图统计
    map_stats = world_map.get_region_stats()
    print()
    print("🏛️ 区域分布:")
    for region_id, stats in map_stats.items():
        if stats['count'] > 0:
            print(f"  - {stats['name']}: {stats['count']} 人")
    
    # 消息历史
    print()
    print("📜 最近消息:")
    history = message_bus.get_history(limit=10)
    for msg in history:
        content = msg.content.get('subject', msg.content.get('title', '...'))
        print(f"  [{msg.message_type}] {msg.sender_id} -> {msg.receiver_id}: {content[:40]}")
    
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
