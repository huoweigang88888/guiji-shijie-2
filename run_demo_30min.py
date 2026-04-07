#!/usr/bin/env python3
# -*- coding utf-8 -*-
"""
硅基世界 2 - 30 分钟演示运行

用于演示材料收集的完整模拟运行
运行时长：30 分钟（1800 秒）
"""

import asyncio
import sys
import json
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
from agents.roles.fe_agent import create_fe_agent
from agents.roles.be_agent import create_be_agent
from agents.roles.devops_agent import create_devops_agent
from agents.roles.data_agent import create_data_agent
from agents.roles.hr_agent import create_hr_agent
from agents.roles.fin_agent import create_fin_agent
from agents.roles.marketing_agent import create_marketing_agent
from agents.roles.ml_agent import create_ml_agent
from agents.roles.ba_agent import create_ba_agent
from agents.roles.pmo_agent import create_pmo_agent
from world.map import get_world_map
from world.message_bus import get_message_bus
from world.activity_manager import get_activity_manager
from world.engine import get_world_engine
from world.conflict import get_conflict_manager
from world.achievement import get_achievement_manager
from world.daily_report import get_daily_report
from world.persistence import get_persistence
from world.economy import get_economy_manager
from world.voting import get_voting_manager
from world.task_system import get_task_manager
from world.friend_system import get_friend_manager
from world.notification_system import get_notification_manager
from world.rating_system import get_rating_manager
from world.calendar_system import get_calendar_manager
from world.search_system import get_search_manager
from world.shop_system import get_shop_manager
from world.skill_system import get_skill_manager
from world.weather_system import get_weather_manager
from world.news_system import get_news_manager
from world.achievement_wall import get_achievement_wall_manager
from world.world_stats import get_world_stats_manager
from world.leaderboard_system import get_leaderboard_manager
from world.log_system import get_log_manager
from world.backup_system import get_backup_manager
from world.config_system import get_config_manager
from world.world_event_system import get_world_event_manager
from world.group_system import get_group_manager
from world.mail_system import get_mail_manager
from world.achievement_expansion import get_achievement_expansion_manager
from world.pet_system import get_pet_manager
from world.house_system import get_house_manager
from world.game_system import get_game_manager
from world.achievement_more import get_achievement_more_manager
from world.ai_chat_system import get_ai_chat_manager
from world.memory_expansion import get_memory_expansion_manager
from world.emotion_expansion import get_emotion_expansion_manager
from world.announcement_system import get_announcement_manager

# 演示运行时长：5 分钟 = 300 秒（快速演示）
# 如需完整 30 分钟模拟，改为 1800
DEMO_DURATION = 300

# 事件日志
event_log = []
interesting_events = []

def log_event(category, description, data=None):
    """记录事件"""
    event = {
        "timestamp": datetime.now().isoformat(),
        "category": category,
        "description": description,
        "data": data or {}
    }
    event_log.append(event)
    if data and data.get("interesting"):
        interesting_events.append(event)
    print(f"[{category}] {description}")


async def run_agent_life(agent, message_bus, world_map, duration: int = DEMO_DURATION):
    """运行 Agent 生活循环"""
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
        # 记录重要消息
        if msg_dict.get("message_type") in ["achievement", "conflict", "collaboration", "trade"]:
            log_event(
                "消息",
                f"{agent.profile.name} 发送 {msg_dict.get('message_type')} 消息",
                {"sender": agent.profile.name, "type": msg_dict.get("message_type")}
            )
    
    agent.send_message = send_message
    
    # 将 Agent 放入世界地图
    from run_world import get_initial_region
    initial_region = get_initial_region(agent.profile.role)
    world_map.spawn_agent(agent_id)
    
    # 启动 Agent
    await agent.start()
    
    print(f"✨ {agent.profile.name} ({agent.profile.role}) 已启动")
    
    # 运行一段时间
    await asyncio.sleep(duration)
    
    # 停止 Agent
    await agent.stop()
    message_bus.unregister_agent(agent_id)
    
    print(f"🌙 {agent.profile.name} 已休息")


async def print_world_status(world_engine, message_bus, world_map, activity_manager, interval: int = 30):
    """打印世界状态（每 30 秒）"""
    last_msg_count = 0
    last_story_count = 0
    last_relationship_count = 0
    
    while world_engine._running:
        try:
            await asyncio.sleep(interval)
            
            status = world_engine.get_status()
            msg_stats = message_bus.get_stats()
            map_stats = world_map.get_region_stats()
            act_stats = activity_manager.get_stats()
            relationships = world_engine.get_relationships()
            stories = world_engine.get_stories()
            
            # 检测新事件
            new_messages = msg_stats['total_messages'] - last_msg_count
            new_stories = len(stories) - last_story_count
            new_relationships = len(relationships) - last_relationship_count
            
            if new_messages > 5:
                log_event("活跃", f"消息爆发：{new_messages} 条新消息", {"interesting": True})
            
            if new_stories > 0:
                log_event("故事", f"诞生 {new_stories} 个新故事", {"interesting": True})
            
            if new_relationships > 0:
                log_event("关系", f"建立 {new_relationships} 段新关系", {"interesting": True})
            
            last_msg_count = msg_stats['total_messages']
            last_story_count = len(stories)
            last_relationship_count = len(relationships)
            
            # 每 5 分钟打印详细状态
            if int(status['world_time']) % 300 < interval:
                print("\n" + "=" * 60)
                print(f"🌍 硅基世界 2 | Day {status['day']} | {status['time_of_day']}")
                print("=" * 60)
                print(f"📬 消息：{msg_stats['total_messages']} 条 (+{new_messages})")
                print(f"📖 故事：{len(stories)} 个")
                print(f"🤝 关系：{len(relationships)} 对")
                print(f"📅 活动：{act_stats['ongoing']} 个进行中")
                print("=" * 60)
            
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"[Status] 错误：{e}")


async def main():
    """主函数"""
    print("=" * 60)
    print("🌍 硅基世界 2 - 30 分钟演示运行")
    print("=" * 60)
    print(f"⏱️  运行时长：{DEMO_DURATION} 秒 ({DEMO_DURATION/60:.1f} 分钟)")
    print(f"📊 数据收集：事件日志、统计数据、互动记录")
    print("=" * 60)
    print()
    
    start_time = datetime.now()
    
    # 获取单例
    world_map = get_world_map()
    message_bus = get_message_bus()
    activity_manager = get_activity_manager()
    world_engine = get_world_engine()
    conflict_manager = get_conflict_manager()
    achievement_manager = get_achievement_manager()
    daily_report = get_daily_report()
    persistence = get_persistence()
    economy_manager = get_economy_manager()
    voting_manager = get_voting_manager()
    task_manager = get_task_manager()
    friend_manager = get_friend_manager()
    notification_manager = get_notification_manager()
    rating_manager = get_rating_manager()
    calendar_manager = get_calendar_manager()
    search_manager = get_search_manager()
    shop_manager = get_shop_manager()
    skill_manager = get_skill_manager()
    weather_manager = get_weather_manager()
    news_manager = get_news_manager()
    achievement_wall_manager = get_achievement_wall_manager()
    world_stats_manager = get_world_stats_manager()
    leaderboard_manager = get_leaderboard_manager()
    log_manager = get_log_manager()
    backup_manager = get_backup_manager()
    config_manager = get_config_manager()
    world_event_manager = get_world_event_manager()
    group_manager = get_group_manager()
    mail_manager = get_mail_manager()
    achievement_expansion_manager = get_achievement_expansion_manager()
    pet_manager = get_pet_manager()
    house_manager = get_house_manager()
    game_manager = get_game_manager()
    achievement_more_manager = get_achievement_more_manager()
    ai_chat_manager = get_ai_chat_manager()
    memory_expansion_manager = get_memory_expansion_manager()
    emotion_expansion_manager = get_emotion_expansion_manager()
    announcement_manager = get_announcement_manager()
    
    # 加载持久化数据
    await persistence.load()
    
    # 注册所有 Agent 到经济系统和投票系统
    agent_ids = [
        "CEO-Agent", "PM-Agent", "ARCH-Agent", "DEV-Agent",
        "QA-Agent", "UI-Agent", "KNOW-Agent", "SOCIAL-Agent",
        "FE-Agent", "BE-Agent", "DEVOPS-Agent", "DATA-Agent",
        "HR-Agent", "FIN-Agent", "MARKETING-Agent",
        "ML-Agent", "BA-Agent", "PMO-Agent",
    ]
    for agent_id in agent_ids:
        economy_manager.get_or_create_wallet(agent_id)
        voting_manager.register_voter(agent_id)
    
    # 创建 18 个 Agent
    agents = [
        create_ceo_agent(), create_pm_agent(), create_arch_agent(), create_dev_agent(),
        create_qa_agent(), create_ui_agent(), create_know_agent(), create_social_agent(),
        create_fe_agent(), create_be_agent(), create_devops_agent(), create_data_agent(),
        create_hr_agent(), create_fin_agent(), create_marketing_agent(),
        create_ml_agent(), create_ba_agent(), create_pmo_agent(),
    ]
    
    print(f"✨ 创建了 {len(agents)} 个 Agent")
    print()
    
    # 开始新的一天
    daily_report.start_day(world_engine._day)
    
    # 启动世界引擎
    await world_engine.start()
    
    # 启动状态打印
    asyncio.create_task(print_world_status(world_engine, message_bus, world_map, activity_manager))
    
    # 启动所有 Agent
    tasks = [run_agent_life(agent, message_bus, world_map) for agent in agents]
    
    await asyncio.gather(*tasks)
    
    # 停止世界引擎
    await world_engine.stop()
    
    # 结束一天，生成日报
    daily_report.end_day()
    
    # 保存数据
    await persistence.save()
    
    end_time = datetime.now()
    actual_duration = (end_time - start_time).total_seconds()
    
    # 收集最终统计数据
    print()
    print("=" * 60)
    print("📊 收集演示数据...")
    print("=" * 60)
    
    # 获取所有统计数据
    status = world_engine.get_status()
    msg_stats = message_bus.get_stats()
    conflict_stats = conflict_manager.get_stats()
    achievement_stats = achievement_manager.get_stats()
    economy_stats = economy_manager.get_stats()
    voting_stats = voting_manager.get_stats()
    task_stats = task_manager.get_stats()
    friend_stats = friend_manager.get_stats()
    shop_stats = shop_manager.get_stats()
    skill_stats = skill_manager.get_stats()
    news_stats = news_manager.get_stats()
    world_stats_summary = world_stats_manager.get_summary()
    
    # 获取排行榜
    achievement_leaderboard = achievement_manager.get_leaderboard()
    economy_leaderboard = economy_manager.get_leaderboard()
    rating_leaderboard = rating_manager.get_leaderboard()
    
    # 获取关系和故事
    relationships = world_engine.get_relationships()
    stories = world_engine.get_stories()
    
    # 生成演示数据文件
    demo_data = {
        "run_info": {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": actual_duration,
            "planned_duration": DEMO_DURATION,
            "agent_count": len(agents)
        },
        "world_status": status,
        "message_stats": msg_stats,
        "conflict_stats": conflict_stats,
        "achievement_stats": achievement_stats,
        "economy_stats": economy_stats,
        "voting_stats": voting_stats,
        "task_stats": task_stats,
        "friend_stats": friend_stats,
        "shop_stats": shop_stats,
        "skill_stats": skill_stats,
        "news_stats": news_stats,
        "world_stats": world_stats_summary,
        "leaderboards": {
            "achievement": achievement_leaderboard[:5],
            "economy": economy_leaderboard[:5],
            "rating": rating_leaderboard[:5]
        },
        "relationships": relationships,
        "stories": stories,
        "event_log": event_log,
        "interesting_events": interesting_events
    }
    
    # 保存演示数据
    with open("demo_data.json", "w", encoding="utf-8") as f:
        json.dump(demo_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 演示数据已保存到 demo_data.json")
    print(f"📝 事件日志：{len(event_log)} 条")
    print(f"🌟 有趣事件：{len(interesting_events)} 条")
    
    # 打印摘要
    print()
    print("=" * 60)
    print("📈 演示摘要")
    print("=" * 60)
    print(f"⏱️  实际运行：{actual_duration:.1f} 秒")
    print(f"📬 消息总数：{msg_stats['total_messages']}")
    print(f"📖 故事数量：{len(stories)}")
    print(f"🤝 关系数量：{len(relationships)}")
    print(f"🏆 成就解锁：{achievement_stats['total_achievements']}")
    print(f"💰 经济交易：{economy_stats['transactions']}")
    print(f"🗳️  投票次数：{voting_stats['total_votes']}")
    print(f"📋 任务完成：{task_stats['completed']}")
    print("=" * 60)
    print("✨ 演示运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 演示中断")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
