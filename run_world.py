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
        create_ceo_agent(),         # CEO-Agent - 董事事
        create_pm_agent(),          # PM-Agent - 小问
        create_arch_agent(),        # ARCH-Agent - 阿哲
        create_dev_agent(),         # DEV-Agent - 小码
        create_qa_agent(),          # QA-Agent - 小测
        create_ui_agent(),          # UI-Agent - 小美
        create_know_agent(),        # KNOW-Agent - 小知
        create_social_agent(),      # SOCIAL-Agent - 小交
        create_fe_agent(),          # FE-Agent - 小前
        create_be_agent(),          # BE-Agent - 小后
        create_devops_agent(),      # DEVOPS-Agent - 小运
        create_data_agent(),        # DATA-Agent - 小数
        create_hr_agent(),          # HR-Agent - 小人
        create_fin_agent(),         # FIN-Agent - 小财
        create_marketing_agent(),   # MARKETING-Agent - 小推
        create_ml_agent(),          # ML-Agent - 小智
        create_ba_agent(),          # BA-Agent - 小商
        create_pmo_agent(),         # PMO-Agent - 小项
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
    
    # 开始新的一天
    daily_report.start_day(world_engine._day)
    
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
    
    # 结束一天，生成日报
    daily_report.end_day()
    
    # 保存数据
    await persistence.save()
    
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
    
    # 冲突统计
    conflict_stats = conflict_manager.get_stats()
    print(f"⚡ 冲突：{conflict_stats['total']} 次 ({conflict_stats['resolved']} 已解决)")
    
    # 成就统计
    achievement_stats = achievement_manager.get_stats()
    print(f"🏆 成就：{achievement_stats['total_achievements']} 个解锁")
    
    # 经济统计
    economy_stats = economy_manager.get_stats()
    print(f"💰 经济：{economy_stats['transactions']} 笔交易，总信用点：{economy_stats['total_credits']:.0f}")
    
    # 投票统计
    voting_stats = voting_manager.get_stats()
    print(f"🗳️  投票：{voting_stats['total_votes']} 次投票，{voting_stats['passed_votes']} 次通过")
    
    # 显示关系
    relationships = world_engine.get_relationships()
    if relationships:
        print()
        print("🤝 关系网络:")
        for rel in relationships[:5]:  # 显示前 5 个
            print(f"   {rel['agent1']} ↔ {rel['agent2']}: {rel['strength']}")
    
    # 显示故事
    stories = world_engine.get_stories()
    if stories:
        print()
        print("📖 诞生的故事:")
        for story in stories[:5]:  # 显示前 5 个
            print(f"   • {story['title']}")
    
    # 显示成就
    leaderboard = achievement_manager.get_leaderboard()
    if leaderboard:
        print()
        print("🏆 成就排行榜:")
        for entry in leaderboard[:3]:  # 显示前 3 名
            print(f"   {entry['agent_id']}: {entry['points']} 分 ({entry['achievements_count']} 个成就)")
    
    # 显示经济排行榜
    economy_leaderboard = economy_manager.get_leaderboard()
    if economy_leaderboard:
        print()
        print("💰 财富排行榜:")
        for entry in economy_leaderboard[:3]:  # 显示前 3 名
            print(f"   {entry['agent_id']}: {entry['value']:.0f} 信用点")
    
    # 显示投票历史
    past_votes = voting_manager.get_past_votes()
    if past_votes:
        print()
        print("🗳️  投票历史:")
        for vote in past_votes[:3]:  # 显示前 3 个
            print(f"   • {vote.title}: {vote.result}")
    
    # 显示任务统计
    task_stats = task_manager.get_stats()
    print()
    print(f"📋 任务：{task_stats['completed']} 完成，{task_stats['open']} 开放")
    
    # 显示好友统计
    friend_stats = friend_manager.get_stats()
    print(f"🤝 好友：{friend_stats['accepted']} 对好友关系")
    
    # 显示通知统计
    notif_stats = notification_manager.get_stats()
    print(f"🔔 通知：{notif_stats['unread']} 未读")
    
    # 显示声誉排行榜
    rating_leaderboard = rating_manager.get_leaderboard()
    if rating_leaderboard:
        print()
        print("⭐ 声誉排行榜:")
        for entry in rating_leaderboard[:3]:
            print(f"   {entry['agent_id']}: {entry['reputation']:.1f} 分")
    
    # 显示日历事件
    upcoming_events = calendar_manager.get_upcoming_events(3)
    if upcoming_events:
        print()
        print("📅 近期事件:")
        for event in upcoming_events[:3]:
            print(f"   • {event.title} ({event.date})")
    
    # 显示商店统计
    shop_stats = shop_manager.get_stats()
    print()
    print(f"🛒 商店：{shop_stats['total_items']} 种商品，{shop_stats['total_purchases']} 笔购买")
    
    # 显示技能统计
    skill_stats = skill_manager.get_stats()
    print(f"⭐ 技能：{skill_stats['total_learned']} 次学习，平均等级 {skill_stats['average_level']:.1f}")
    
    # 显示天气
    weather_manager.update_all_weather()
    weather_stats = weather_manager.get_stats()
    print()
    print(f"🌤️  天气：{weather_stats['regions_with_weather']} 个区域已更新")
    
    # 显示新闻
    news_stats = news_manager.get_stats()
    print(f"📰 新闻：{news_stats['total_news']} 篇，{news_stats['total_views']} 次阅读")
    
    # 显示成就墙
    wall_stats = achievement_wall_manager.get_stats()
    print(f"🏆 成就墙：{wall_stats['total_achievements']} 个成就")
    
    # 显示世界统计
    stats_summary = world_stats_manager.get_summary()
    print()
    print(f"⏱️  运行时间：{stats_summary['uptime_human']}")
    
    print()
    print("=" * 60)
    print("✨ 硅基世界 2 运行完成！")
    print("=" * 60)
    print()
    print("💾 数据已保存到 data/ 目录")
    print("📰 日报已生成到 reports/ 目录")
    print("🌐 打开 web/index.html 观察世界")
    print("📡 API 服务：python api/server.py")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 世界暂停，下次再见！")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
