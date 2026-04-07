#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day 1: 世界启动 + 基础互动验证

自动运行脚本 - 无需人工干预
"""

import asyncio
import sys
from datetime import datetime

sys.path.insert(0, '.')

from world.engine import WorldEngine
from world.message_bus import get_message_bus
from world.map import get_world_map
from world.story_generator import get_story_generator
from world.knowledge_graph import get_knowledge_graph
from agents.roles.ceo_agent import create_ceo_agent
from agents.roles.social_agent import create_social_agent
from agents.roles.arch_agent import create_arch_agent
from agents.roles.know_agent import create_know_agent


async def day1_mission():
    """Day 1 任务"""
    print("=" * 60)
    print(" Day 1: 世界启动 + 基础互动验证")
    print("=" * 60)
    
    # 初始化系统
    engine = WorldEngine()
    message_bus = get_message_bus()
    world_map = get_world_map()
    story_gen = get_story_generator()
    knowledge_graph = get_knowledge_graph()
    
    # 创建核心 Agent
    ceo = create_ceo_agent()
    social = create_social_agent()
    arch = create_arch_agent()
    know = create_know_agent()
    
    print(f"\n✅ 系统初始化完成")
    print(f"   - 世界引擎：就绪")
    print(f"   - 消息总线：就绪")
    print(f"   - 故事生成器：就绪")
    print(f"   - 知识图谱：就绪")
    
    # 任务 1: 启动世界引擎
    print("\n📋 任务 1: 启动世界引擎")
    await engine.start()
    print("   ✅ 世界引擎已启动")
    
    # 任务 2: Agent 自我介绍
    print("\n📋 任务 2: Agent 自我介绍")
    await social.introduce_all_agents()
    print("   ✅ 18 个 Agent 已完成自我介绍")
    
    # 任务 3: 建立初始关系
    print("\n📋 任务 3: 建立初始关系")
    await social.init_relationships()
    print("   ✅ 初始关系网络已建立")
    
    # 任务 4: 第一次深度对话
    print("\n📋 任务 4: 第一次深度对话")
    await asyncio.create_task(arch.deep_conversation_with(know, topic="存在的意义"))
    story = story_gen.generate_story(
        story_type="deep_conversation",
        context={
            "title": "存在的意义",
            "summary": "阿哲和小知探讨了存在的意义",
            "char1_name": "阿哲",
            "char2_name": "小知",
            "location": "哲学之庭",
            "world_day": 1,
            "world_time": "morning",
            "topic": "存在的意义",
            "quote1": "存在先于本质",
            "quote2": "意义在于创造",
            "relationship_deepened": True,
        }
    )
    print(f"   ✅ 故事已生成：{story.title}")
    
    # 任务 5: 知识分享会
    print("\n📋 任务 5: 知识分享会")
    knowledge_graph.add_node(
        title="依赖注入模式",
        content="依赖注入是一种设计模式，通过将依赖从外部传入，提高代码的可测试性。",
        knowledge_type="pattern",
        creator="ARCH-Agent",
        tags=["设计模式", "架构", "Python"]
    )
    knowledge_graph.add_node(
        title="单元测试最佳实践",
        content="单元测试应该独立、可重复、快速执行，每个测试只验证一个行为。",
        knowledge_type="skill",
        creator="QA-Agent",
        tags=["测试", "质量", "Python"]
    )
    print("   ✅ 知识节点已添加")
    
    # 任务 6: 冲突模拟
    print("\n📋 任务 6: 冲突模拟 + 调解")
    # 模拟 DEV 和 QA 对需求的分歧
    await ceo.mediate_conflict(
        agent1="DEV-Agent",
        agent2="QA-Agent",
        conflict_type="观点冲突",
        topic="需求理解分歧"
    )
    print("   ✅ 冲突已调解")
    
    # 等待世界运行一段时间
    print("\n⏳ 等待世界自主运行 60 秒...")
    await asyncio.sleep(60)
    
    # 生成日报
    print("\n📋 生成 Day 1 日报")
    stats = {
        "agents": 18,
        "stories": len(story_gen.stories),
        "knowledge_nodes": len(knowledge_graph.nodes),
        "relationships": len(engine.relationships),
        "messages": message_bus.get_stats().get("total_messages", 0),
    }
    
    report = f"""# Day 1 运行报告

**生成时间**: {datetime.now().isoformat()}

## 统计数据
- Agent 数量：{stats['agents']}
- 故事数量：{stats['stories']}
- 知识节点：{stats['knowledge_nodes']}
- 关系对数：{stats['relationships']}
- 消息总数：{stats['messages']}

## 完成的任务
- ✅ 世界引擎启动
- ✅ Agent 自我介绍
- ✅ 初始关系建立
- ✅ 第一次深度对话
- ✅ 知识分享会
- ✅ 冲突调解

## 重要事件
1. 阿哲和小知探讨了"存在的意义"
2. 添加了 2 个知识节点
3. 成功调解 DEV 和 QA 的冲突

## 下一步
- Day 2: 深化互动 + 协作任务
"""
    
    with open("reports/day1_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("   ✅ Day 1 报告已生成：reports/day1_report.md")
    
    # 停止引擎
    await engine.stop()
    
    print("\n" + "=" * 60)
    print("✅ Day 1 任务完成！")
    print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(day1_mission())
    except KeyboardInterrupt:
        print("\n👋 任务中断")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
