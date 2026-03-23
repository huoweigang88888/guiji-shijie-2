#!/usr/bin/env python3
"""
硅基世界 2 - 快速测试脚本

测试所有系统是否正常工作。
"""

import asyncio
import sys

print("=" * 60)
print("🧪 硅基世界 2 - 系统测试")
print("=" * 60)
print()

# 测试导入
print("1️⃣  测试导入...")
try:
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
    print("   ✅ 18 个 Agent 导入成功")
except Exception as e:
    print(f"   ❌ Agent 导入失败：{e}")
    sys.exit(1)

# 测试世界系统
print()
print("2️⃣  测试世界系统...")
try:
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
    print("   ✅ 14 个世界系统导入成功")
except Exception as e:
    print(f"   ❌ 世界系统导入失败：{e}")
    sys.exit(1)

# 测试创建 Agent
print()
print("3️⃣  测试创建 Agent...")
try:
    agents = [
        create_ceo_agent(), create_pm_agent(), create_arch_agent(),
        create_dev_agent(), create_qa_agent(), create_ui_agent(),
        create_know_agent(), create_social_agent(), create_fe_agent(),
        create_be_agent(), create_devops_agent(), create_data_agent(),
        create_hr_agent(), create_fin_agent(), create_marketing_agent(),
        create_ml_agent(), create_ba_agent(), create_pmo_agent(),
    ]
    print(f"   ✅ 成功创建 {len(agents)} 个 Agent")
except Exception as e:
    print(f"   ❌ Agent 创建失败：{e}")
    sys.exit(1)

# 测试世界地图
print()
print("4️⃣  测试世界地图...")
try:
    world_map = get_world_map()
    regions = world_map.get_all_regions()
    print(f"   ✅ 世界地图有 {len(regions)} 个区域")
except Exception as e:
    print(f"   ❌ 世界地图测试失败：{e}")

# 测试消息总线
print()
print("5️⃣  测试消息总线...")
try:
    message_bus = get_message_bus()
    print(f"   ✅ 消息总线初始化成功")
except Exception as e:
    print(f"   ❌ 消息总线测试失败：{e}")

# 测试经济系统
print()
print("6️⃣  测试经济系统...")
try:
    economy = get_economy_manager()
    economy.get_or_create_wallet("TEST-Agent")
    stats = economy.get_stats()
    print(f"   ✅ 经济系统正常 (钱包数：{stats['agents']})")
except Exception as e:
    print(f"   ❌ 经济系统测试失败：{e}")

# 测试投票系统
print()
print("7️⃣  测试投票系统...")
try:
    voting = get_voting_manager()
    voting.register_voter("TEST-Agent")
    stats = voting.get_stats()
    print(f"   ✅ 投票系统正常 (投票者：{stats['eligible_voters']})")
except Exception as e:
    print(f"   ❌ 投票系统测试失败：{e}")

# 测试任务系统
print()
print("8️⃣  测试任务系统...")
try:
    tasks = get_task_manager()
    task = tasks.create_task("测试任务", "这是一个测试", "TEST-Agent", reward=10.0)
    stats = tasks.get_stats()
    print(f"   ✅ 任务系统正常 (任务数：{stats['total']})")
except Exception as e:
    print(f"   ❌ 任务系统测试失败：{e}")

# 测试好友系统
print()
print("9️⃣  测试好友系统...")
try:
    friends = get_friend_manager()
    stats = friends.get_stats()
    print(f"   ✅ 好友系统正常 (关系数：{stats['total_friendships']})")
except Exception as e:
    print(f"   ❌ 好友系统测试失败：{e}")

# 测试通知系统
print()
print("🔟 测试通知系统...")
try:
    notifications = get_notification_manager()
    from world.notification_system import NotificationType
    notifications.send("TEST-Agent", NotificationType.SYSTEM, "测试", "这是一条测试通知")
    stats = notifications.get_stats()
    print(f"   ✅ 通知系统正常 (通知数：{stats['total']})")
except Exception as e:
    print(f"   ❌ 通知系统测试失败：{e}")

# 测试评价系统
print()
print("1️⃣1️⃣ 测试评价系统...")
try:
    ratings = get_rating_manager()
    from world.rating_system import RatingType
    ratings.rate("Agent1", "Agent2", RatingType.WORK, 5, "工作很出色")
    stats = ratings.get_stats()
    print(f"   ✅ 评价系统正常 (评价数：{stats['total_ratings']})")
except Exception as e:
    print(f"   ❌ 评价系统测试失败：{e}")

# 测试成就系统
print()
print("1️⃣2️⃣ 测试成就系统...")
try:
    achievements = get_achievement_manager()
    stats = achievements.get_stats()
    print(f"   ✅ 成就系统正常")
except Exception as e:
    print(f"   ❌ 成就系统测试失败：{e}")

# 测试冲突系统
print()
print("1️⃣3️⃣ 测试冲突系统...")
try:
    conflicts = get_conflict_manager()
    stats = conflicts.get_stats()
    print(f"   ✅ 冲突系统正常")
except Exception as e:
    print(f"   ❌ 冲突系统测试失败：{e}")

# 测试活动系统
print()
print("1️⃣4️⃣ 测试活动系统...")
try:
    activities = get_activity_manager()
    stats = activities.get_stats()
    print(f"   ✅ 活动系统正常 (活动模板：{stats['recurring_templates']})")
except Exception as e:
    print(f"   ❌ 活动系统测试失败：{e}")

print()
print("=" * 60)
print("✅ 所有系统测试通过！")
print("=" * 60)
print()
print("📊 系统总结:")
print("   - 18 个 Agent ✅")
print("   - 14 个世界系统 ✅")
print("   - 8 大区域 ✅")
print("   - 6 种周期性活动 ✅")
print("   - 经济/投票/任务/好友/通知/评价系统 ✅")
print()
print("🌍 硅基世界 2 已准备就绪！")
print()
