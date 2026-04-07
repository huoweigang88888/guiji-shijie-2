#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day 2: 深化互动 + 协作任务

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
from world.activity_manager import get_activity_manager
from agents.roles.pm_agent import create_pm_agent
from agents.roles.dev_agent import create_dev_agent
from agents.roles.qa_agent import create_qa_agent
from agents.roles.ui_agent import create_ui_agent


async def day2_mission():
    """Day 2 任务"""
    print("=" * 60)
    print(" Day 2: 深化互动 + 协作任务")
    print("=" * 60)
    
    # 初始化系统
    engine = WorldEngine()
    message_bus = get_message_bus()
    world_map = get_world_map()
    story_gen = get_story_generator()
    knowledge_graph = get_knowledge_graph()
    activity_mgr = get_activity_manager()
    
    # 创建核心 Agent
    pm = create_pm_agent()
    dev = create_dev_agent()
    qa = create_qa_agent()
    ui = create_ui_agent()
    
    print(f"\n✅ 系统初始化完成")
    
    # 任务 1: 加载 Day 1 状态
    print("\n📋 任务 1: 加载 Day 1 状态")
    engine.load_state()
    print("   ✅ Day 1 状态已加载")
    
    # 任务 2: 每日站会
    print("\n📋 任务 2: 每日站会")
    await activity_mgr.start_activity("daily_standup")
    print("   ✅ 每日站会已完成")
    
    # 任务 3: 协作任务 - 新功能开发
    print("\n📋 任务 3: 协作任务 - 新功能开发")
    
    # PM 提出需求
    await pm.send_request(
        receiver="DEV-Agent",
        subject="新增用户反馈功能",
        content="用户希望能够快速提交反馈，需要实现一个反馈表单。"
    )
    
    # DEV 实现功能
    await dev.implement_feature("用户反馈表单")
    
    # QA 编写测试
    await qa.write_tests("用户反馈表单")
    
    # UI 设计界面
    await ui.design_ui("用户反馈表单")
    
    print("   ✅ 协作任务已完成")
    
    # 生成协作故事
    story_gen.generate_story(
        story_type="collaboration",
        context={
            "title": "用户反馈功能的诞生",
            "summary": "PM、DEV、QA、UI 协作完成新功能",
            "characters": [
                {"agent_id": "PM-Agent", "name": "小问", "role": "产品经理", "emotion": "期待"},
                {"agent_id": "DEV-Agent", "name": "小码", "role": "开发", "emotion": "专注"},
                {"agent_id": "QA-Agent", "name": "小测", "role": "测试", "emotion": "严谨"},
                {"agent_id": "UI-Agent", "name": "小美", "role": "设计师", "emotion": "创意"},
            ],
            "location": "工作之城",
            "world_day": 2,
            "world_time": "afternoon",
            "goal": "用户反馈功能",
            "task1": "需求分析",
            "task2": "功能实现",
            "task3": "测试验证",
            "duration": "3 小时",
        }
    )
    print("   ✅ 协作故事已生成")
    
    # 任务 4: 知识沉淀
    print("\n📋 任务 4: 知识沉淀")
    knowledge_graph.add_node(
        title="用户反馈系统设计",
        content="用户反馈系统应包含：表单收集、分类标签、优先级排序、状态跟踪、回复机制。",
        knowledge_type="experience",
        creator="PM-Agent",
        tags=["产品设计", "用户体验", "反馈"]
    )
    knowledge_graph.add_node(
        title="表单验证最佳实践",
        content="前端验证 + 后端验证双重保障，实时反馈错误信息，友好的错误提示。",
        knowledge_type="pattern",
        creator="DEV-Agent",
        tags=["前端", "验证", "用户体验"]
    )
    knowledge_graph.add_node(
        title="测试用例设计方法",
        content="边界值分析、等价类划分、因果图、状态转换测试等多种方法结合使用。",
        knowledge_type="skill",
        creator="QA-Agent",
        tags=["测试", "质量保证"]
    )
    
    # 添加知识关联
    nodes = list(knowledge_graph.nodes.values())
    if len(nodes) >= 3:
        knowledge_graph.add_edge(nodes[-3].id, nodes[-2].id, "related_to", description="反馈系统需要表单验证")
        knowledge_graph.add_edge(nodes[-2].id, nodes[-1].id, "related_to", description="表单验证需要测试")
    
    print("   ✅ 知识节点已添加并关联")
    
    # 任务 5: 数据咖啡时间
    print("\n📋 任务 5: 数据咖啡时间")
    await activity_mgr.start_activity("data_coffee_time")
    print("   ✅ 数据咖啡时间已完成")
    
    # 任务 6: 关系深化
    print("\n📋 任务 6: 关系深化")
    engine.deepen_relationships()
    print("   ✅ 关系已深化")
    
    # 等待世界自主运行
    print("\n⏳ 等待世界自主运行 60 秒...")
    await asyncio.sleep(60)
    
    # 生成日报
    print("\n📋 生成 Day 2 日报")
    stats = {
        "agents": 18,
        "stories": len(story_gen.stories),
        "knowledge_nodes": len(knowledge_graph.nodes),
        "knowledge_edges": len(knowledge_graph.edges),
        "relationships": len(engine.relationships),
        "messages": message_bus.get_stats().get("total_messages", 0),
        "activities": activity_mgr.get_stats().get("completed", 0),
    }
    
    report = f"""# Day 2 运行报告

**生成时间**: {datetime.now().isoformat()}

## 统计数据
- Agent 数量：{stats['agents']}
- 故事数量：{stats['stories']}
- 知识节点：{stats['knowledge_nodes']}
- 知识关联：{stats['knowledge_edges']}
- 关系对数：{stats['relationships']}
- 消息总数：{stats['messages']}
- 活动完成：{stats['activities']}

## 完成的任务
- ✅ 加载 Day 1 状态
- ✅ 每日站会
- ✅ 协作任务（用户反馈功能）
- ✅ 知识沉淀（3 个节点 + 2 条关联）
- ✅ 数据咖啡时间
- ✅ 关系深化

## 重要事件
1. PM、DEV、QA、UI 协作完成用户反馈功能
2. 添加 3 个知识节点和 2 条关联
3. 关系网络进一步深化

## 知识增长
- 产品设计经验 +1
- 开发模式 +1
- 测试技能 +1

## 下一步
- Day 3: 自主演化 + 成果展示
"""
    
    with open("reports/day2_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("   ✅ Day 2 报告已生成：reports/day2_report.md")
    
    # 保存状态
    engine.save_state()
    
    print("\n" + "=" * 60)
    print("✅ Day 2 任务完成！")
    print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(day2_mission())
    except KeyboardInterrupt:
        print("\n👋 任务中断")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
