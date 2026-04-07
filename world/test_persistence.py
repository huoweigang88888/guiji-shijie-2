#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界状态持久化系统测试

测试 save_state() 和 load_state() 功能
"""

import asyncio
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from world.engine import WorldEngine, SAVES_DIR


def test_save_and_load():
    """测试保存和加载功能"""
    print("=" * 60)
    print("🧪 世界状态持久化系统测试")
    print("=" * 60)
    
    # 创建世界引擎
    engine = WorldEngine()
    
    # 模拟一些世界状态
    print("\n📝 步骤 1: 初始化世界状态...")
    engine._world_time = 3600  # 1 小时
    engine._day = 5
    engine._current_time_of_day = engine._current_time_of_day.__class__.AFTERNOON
    
    # 添加一些事件
    for i in range(5):
        engine.events.append({
            "id": i,
            "type": "test_event",
            "description": f"测试事件 {i}",
            "timestamp": engine._world_time + i * 10,
            "day": engine._day,
        })
    
    # 添加一些关系
    engine.relationships["小问 - 阿哲"] = {
        "agent1": "小问",
        "agent2": "阿哲",
        "strength": 75,
        "interactions": 12,
    }
    engine.relationships["小码 - 小测"] = {
        "agent1": "小码",
        "agent2": "小测",
        "strength": 60,
        "interactions": 8,
    }
    
    # 添加一些知识
    engine.collective_knowledge.append({
        "type": "share",
        "author": "小问",
        "topic": "用户研究新发现",
        "timestamp": engine._world_time,
        "day": engine._day,
    })
    
    # 添加一些故事
    engine.stories.append({
        "id": 0,
        "title": "小问与阿哲的用户研究对话",
        "participants": ["小问", "阿哲"],
        "topic": "用户研究",
        "day": engine._day,
        "timestamp": engine._world_time,
        "summary": "一次富有成效的讨论",
    })
    
    # 更新统计数据
    engine.stats = {
        'total_interactions': 50,
        'total_knowledge_created': 15,
        'total_stories_created': 8,
        'total_votes_created': 3,
    }
    
    print(f"   - 世界时间：{engine._world_time}秒 (Day {engine._day})")
    print(f"   - 时段：{engine._current_time_of_day.value}")
    print(f"   - 事件数量：{len(engine.events)}")
    print(f"   - 关系数量：{len(engine.relationships)}")
    print(f"   - 知识数量：{len(engine.collective_knowledge)}")
    print(f"   - 故事数量：{len(engine.stories)}")
    print(f"   - 统计数据：{engine.stats}")
    
    # 保存状态
    print("\n💾 步骤 2: 保存世界状态...")
    save_success = engine.save_state("test_slot")
    
    if not save_success:
        print("❌ 保存失败！")
        return False
    
    # 验证文件已创建
    print("\n📁 步骤 3: 验证存档文件...")
    expected_files = [
        "test_slot_world_state.json",
        "test_slot_agents_state.json",
        "test_slot_relationships.json",
        "test_slot_metadata.json",
    ]
    
    all_files_exist = True
    for filename in expected_files:
        filepath = os.path.join(SAVES_DIR, filename)
        exists = os.path.exists(filepath)
        status = "✓" if exists else "✗"
        print(f"   {status} {filename}")
        if not exists:
            all_files_exist = False
    
    if not all_files_exist:
        print("❌ 部分文件未创建！")
        return False
    
    # 创建新引擎并加载状态
    print("\n📂 步骤 4: 创建新引擎并加载状态...")
    new_engine = WorldEngine()
    
    # 验证新引擎是空的
    print(f"   加载前 - 世界时间：{new_engine._world_time}, Day: {new_engine._day}")
    print(f"   加载前 - 事件数量：{len(new_engine.events)}")
    print(f"   加载前 - 关系数量：{len(new_engine.relationships)}")
    
    load_success = new_engine.load_state("test_slot")
    
    if not load_success:
        print("❌ 加载失败！")
        return False
    
    # 验证数据完整性
    print("\n✅ 步骤 5: 验证数据完整性...")
    
    checks = [
        ("世界时间", new_engine._world_time == 3600),
        ("天数", new_engine._day == 5),
        ("时段", new_engine._current_time_of_day.value == "afternoon"),
        ("事件数量", len(new_engine.events) == 5),
        ("关系数量", len(new_engine.relationships) == 2),
        ("知识数量", len(new_engine.collective_knowledge) == 1),
        ("故事数量", len(new_engine.stories) == 1),
        ("统计数据 - 总互动", new_engine.stats.get('total_interactions') == 50),
        ("统计数据 - 知识创建", new_engine.stats.get('total_knowledge_created') == 15),
    ]
    
    all_passed = True
    for check_name, passed in checks:
        status = "✓" if passed else "✗"
        print(f"   {status} {check_name}")
        if not passed:
            all_passed = False
    
    # 验证具体数据内容
    print("\n🔍 步骤 6: 验证具体数据内容...")
    
    # 验证关系
    if "小问 - 阿哲" in new_engine.relationships:
        rel = new_engine.relationships["小问 - 阿哲"]
        rel_ok = rel.get("strength") == 75 and rel.get("interactions") == 12
        status = "✓" if rel_ok else "✗"
        print(f"   {status} 关系数据：小问 - 阿哲 (强度：{rel.get('strength')}, 互动：{rel.get('interactions')})")
        if not rel_ok:
            all_passed = False
    
    # 验证知识
    if len(new_engine.collective_knowledge) > 0:
        knowledge = new_engine.collective_knowledge[0]
        knowledge_ok = knowledge.get("author") == "小问" and knowledge.get("topic") == "用户研究新发现"
        status = "✓" if knowledge_ok else "✗"
        print(f"   {status} 知识数据：{knowledge.get('author')} - {knowledge.get('topic')}")
        if not knowledge_ok:
            all_passed = False
    
    # 验证故事
    if len(new_engine.stories) > 0:
        story = new_engine.stories[0]
        story_ok = story.get("title") == "小问与阿哲的用户研究对话"
        status = "✓" if story_ok else "✗"
        print(f"   {status} 故事数据：{story.get('title')}")
        if not story_ok:
            all_passed = False
    
    # 测试列出存档
    print("\n📋 步骤 7: 测试列出存档...")
    saves = new_engine.list_saves()
    print(f"   找到 {len(saves)} 个存档:")
    for save in saves:
        print(f"   - 槽位：{save['slot']}, 时间：{save['saved_at']}, Day: {save['day']}")
    
    # 测试自动保存间隔设置
    print("\n⚙️  步骤 8: 测试自动保存间隔设置...")
    new_engine.set_auto_save_interval(30)
    print(f"   自动保存间隔已设置为：{new_engine._auto_save_interval}秒")
    
    # 测试手动保存
    print("\n💾 步骤 9: 测试手动保存...")
    manual_save_success = new_engine.manual_save("manual_test")
    status = "✓" if manual_save_success else "✗"
    print(f"   {status} 手动保存到槽位：manual_test")
    
    # 最终结果
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有测试通过！世界状态持久化系统工作正常。")
    else:
        print("❌ 部分测试失败！请检查输出。")
    print("=" * 60)
    
    return all_passed


async def test_auto_save():
    """测试自动保存功能"""
    print("\n" + "=" * 60)
    print("🕐 自动保存功能测试")
    print("=" * 60)
    
    engine = WorldEngine()
    engine._running = True
    engine._world_time = 100
    engine._day = 1
    
    # 设置较短的自动保存间隔用于测试
    engine._auto_save_interval = 5  # 5 秒
    
    print(f"\n📝 启动自动保存（间隔：{engine._auto_save_interval}秒）...")
    engine._start_auto_save()
    
    # 等待一段时间
    print("⏳ 等待 12 秒（应该触发 2 次自动保存）...")
    await asyncio.sleep(12)
    
    # 停止自动保存
    engine._stop_auto_save = True
    if engine._auto_save_thread and engine._auto_save_thread.is_alive():
        engine._auto_save_thread.join(timeout=2)
    
    # 检查自动保存的文件
    print("\n📁 检查自动保存的文件...")
    auto_save_exists = os.path.exists(os.path.join(SAVES_DIR, "auto_world_state.json"))
    status = "✓" if auto_save_exists else "✗"
    print(f"   {status} auto_world_state.json")
    
    # 列出所有存档
    saves = engine.list_saves()
    print(f"\n📋 当前存档列表 ({len(saves)} 个):")
    for save in saves:
        print(f"   - {save['slot']}: Day {save['day']}, 时间：{save['saved_at']}")
    
    print("\n✅ 自动保存功能测试完成")
    print("=" * 60)


if __name__ == "__main__":
    # 运行基本测试
    success = test_save_and_load()
    
    # 运行自动保存测试
    if success:
        asyncio.run(test_auto_save())
    
    # 退出码
    sys.exit(0 if success else 1)
