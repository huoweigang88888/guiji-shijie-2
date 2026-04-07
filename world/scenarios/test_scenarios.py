#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
硅基世界 2 - 场景模块测试

测试所有 5 个场景模块是否能正常加载和运行：
- collaboration.py - 任务协作场景
- conflict.py - 冲突解决场景
- celebration.py - 庆祝活动场景
- knowledge_share.py - 知识分享场景
- innovation.py - 创新讨论场景
"""

import asyncio
import sys
import os

# 添加项目根目录到路径以便导入
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

print("=" * 70)
print("🧪 硅基世界 2 - 场景模块测试")
print("=" * 70)
print()

# 测试结果记录
test_results = {
    "collaboration": {"loaded": False, "tested": False, "errors": []},
    "conflict": {"loaded": False, "tested": False, "errors": []},
    "celebration": {"loaded": False, "tested": False, "errors": []},
    "knowledge_share": {"loaded": False, "tested": False, "errors": []},
    "innovation": {"loaded": False, "tested": False, "errors": []},
}


def print_section(title: str):
    """打印章节标题"""
    print()
    print("-" * 70)
    print(f"  {title}")
    print("-" * 70)


# =============================================================================
# 1. 测试协作场景 (collaboration.py)
# =============================================================================
print_section("1️⃣  测试协作场景 (collaboration.py)")

try:
    from world.scenarios.collaboration import (
        get_collaboration_manager,
        create_collaboration_manager,
        CollaborationType,
        TaskStatus,
    )
    test_results["collaboration"]["loaded"] = True
    print("   ✅ 模块导入成功")
except Exception as e:
    test_results["collaboration"]["errors"].append(f"导入失败：{e}")
    print(f"   ❌ 模块导入失败：{e}")

if test_results["collaboration"]["loaded"]:
    try:
        # 测试创建管理器
        collab_mgr = create_collaboration_manager()
        print("   ✅ 管理器创建成功")
        
        # 测试创建协作任务
        async def test_collaboration():
            task = await collab_mgr.create_task(
                name="联合开发项目",
                description="CEO 和 PM 协作完成产品规划",
                collaborators=["CEO-Agent", "PM-Agent"],
                collab_type=CollaborationType.PAIR_PROGRAMMING,
            )
            
            # 测试更新进度
            await collab_mgr.update_progress(task.task_id, 50, "完成需求分析")
            await collab_mgr.update_progress(task.task_id, 100, "项目完成")
            
            # 测试统计数据
            stats = collab_mgr.get_stats()
            print(f"   ✅ 协作任务测试通过 (总任务数：{stats['total']})")
            return True
        
        asyncio.run(test_collaboration())
        test_results["collaboration"]["tested"] = True
        
    except Exception as e:
        test_results["collaboration"]["errors"].append(f"功能测试失败：{e}")
        print(f"   ❌ 功能测试失败：{e}")


# =============================================================================
# 2. 测试冲突场景 (conflict.py)
# =============================================================================
print_section("2️⃣  测试冲突解决场景 (conflict.py)")

try:
    from world.conflict import (
        get_conflict_manager,
        create_conflict_manager,
        ConflictType,
        ConflictStatus,
    )
    test_results["conflict"]["loaded"] = True
    print("   ✅ 模块导入成功")
except Exception as e:
    test_results["conflict"]["errors"].append(f"导入失败：{e}")
    print(f"   ❌ 模块导入失败：{e}")

if test_results["conflict"]["loaded"]:
    try:
        # 测试创建管理器
        conflict_mgr = create_conflict_manager()
        print("   ✅ 管理器创建成功")
        
        # 测试创建和解决冲突
        async def test_conflict():
            # 创建冲突
            conflict = await conflict_mgr.create_conflict(
                agents=["Dev-Agent", "QA-Agent"],
                conflict_type=ConflictType.OPINION_DIFFERENCE,
                topic="代码质量标准",
            )
            
            # 测试调解冲突
            await conflict_mgr.mediate_conflict(conflict.conflict_id, "CEO-Agent")
            
            # 测试统计数据
            stats = conflict_mgr.get_stats()
            print(f"   ✅ 冲突场景测试通过 (总冲突数：{stats['total']}, 已解决：{stats['resolved']})")
            return True
        
        asyncio.run(test_conflict())
        test_results["conflict"]["tested"] = True
        
    except Exception as e:
        test_results["conflict"]["errors"].append(f"功能测试失败：{e}")
        print(f"   ❌ 功能测试失败：{e}")


# =============================================================================
# 3. 测试庆祝场景 (celebration.py)
# =============================================================================
print_section("3️⃣  测试庆祝活动场景 (celebration.py)")

try:
    from world.scenarios.celebration import (
        get_celebration_manager,
        create_celebration_manager,
        CelebrationType,
        CelebrationScale,
    )
    test_results["celebration"]["loaded"] = True
    print("   ✅ 模块导入成功")
except Exception as e:
    test_results["celebration"]["errors"].append(f"导入失败：{e}")
    print(f"   ❌ 模块导入失败：{e}")

if test_results["celebration"]["loaded"]:
    try:
        # 测试创建管理器
        celebration_mgr = create_celebration_manager()
        print("   ✅ 管理器创建成功")
        
        # 测试创建庆祝活动
        async def test_celebration():
            # 创建庆祝活动
            celebration = await celebration_mgr.create_celebration(
                title="项目成功上线",
                description="庆祝新版本成功发布",
                celebration_type=CelebrationType.PROJECT_COMPLETED,
                participants=["CEO-Agent", "PM-Agent", "Dev-Agent", "QA-Agent"],
                scale=CelebrationScale.LARGE,
            )
            
            # 测试添加消息
            await celebration_mgr.add_message(celebration.celebration_id, "CEO-Agent", "大家辛苦了！")
            await celebration_mgr.add_message(celebration.celebration_id, "Dev-Agent", "🎉 值得庆祝！")
            
            # 测试赠送礼物
            await celebration_mgr.give_gift(celebration.celebration_id, "PM-Agent", "Dev-Agent", "虚拟奖杯 🏆")
            
            # 完成庆祝
            await celebration_mgr.complete_celebration(celebration.celebration_id)
            
            # 测试统计数据
            stats = celebration_mgr.get_stats()
            print(f"   ✅ 庆祝场景测试通过 (总庆祝数：{stats['total']}, 已完成：{stats['completed']})")
            return True
        
        asyncio.run(test_celebration())
        test_results["celebration"]["tested"] = True
        
    except Exception as e:
        test_results["celebration"]["errors"].append(f"功能测试失败：{e}")
        print(f"   ❌ 功能测试失败：{e}")


# =============================================================================
# 4. 测试知识分享场景 (knowledge_share.py)
# =============================================================================
print_section("4️⃣  测试知识分享场景 (knowledge_share.py)")

try:
    from world.scenarios.knowledge_share import (
        get_knowledge_share_manager,
        create_knowledge_share_manager,
        KnowledgeType,
        SharingFormat,
    )
    test_results["knowledge_share"]["loaded"] = True
    print("   ✅ 模块导入成功")
except Exception as e:
    test_results["knowledge_share"]["errors"].append(f"导入失败：{e}")
    print(f"   ❌ 模块导入失败：{e}")

if test_results["knowledge_share"]["loaded"]:
    try:
        # 测试创建管理器
        knowledge_mgr = create_knowledge_share_manager()
        print("   ✅ 管理器创建成功")
        
        # 测试知识分享功能
        async def test_knowledge_share():
            # 创建知识分享
            share = await knowledge_mgr.create_share(
                title="Python 异步编程最佳实践",
                content="async/await 使用指南...",
                author="Dev-Agent",
                knowledge_type=KnowledgeType.TUTORIAL,
                tags=["python", "async", "tutorial"],
                share_format=SharingFormat.TEXT,
            )
            
            # 测试查看
            await knowledge_mgr.view_share(share.share_id)
            
            # 测试点赞
            await knowledge_mgr.like_share(share.share_id, "PM-Agent")
            
            # 测试评论
            await knowledge_mgr.add_comment(share.share_id, "QA-Agent", "很实用的教程！")
            
            # 测试统计数据
            stats = knowledge_mgr.get_stats()
            print(f"   ✅ 知识分享场景测试通过 (总分享数：{stats['total']}, 总点赞：{stats['total_likes']})")
            return True
        
        asyncio.run(test_knowledge_share())
        test_results["knowledge_share"]["tested"] = True
        
    except Exception as e:
        test_results["knowledge_share"]["errors"].append(f"功能测试失败：{e}")
        print(f"   ❌ 功能测试失败：{e}")


# =============================================================================
# 5. 测试创新讨论场景 (innovation.py)
# =============================================================================
print_section("5️⃣  测试创新讨论场景 (innovation.py)")

try:
    from world.scenarios.innovation import (
        get_innovation_manager,
        create_innovation_manager,
        InnovationStage,
        IdeaStatus,
    )
    test_results["innovation"]["loaded"] = True
    print("   ✅ 模块导入成功")
except Exception as e:
    test_results["innovation"]["errors"].append(f"导入失败：{e}")
    print(f"   ❌ 模块导入失败：{e}")

if test_results["innovation"]["loaded"]:
    try:
        # 测试创建管理器
        innovation_mgr = create_innovation_manager()
        print("   ✅ 管理器创建成功")
        
        # 测试创新创意功能
        async def test_innovation():
            # 提出创意
            idea = await innovation_mgr.propose_idea(
                title="AI 辅助代码审查系统",
                description="使用 AI 自动审查代码质量和安全性",
                proposer="Arch-Agent",
            )
            
            # 测试支持
            await innovation_mgr.support_idea(idea.idea_id, "Dev-Agent")
            await innovation_mgr.support_idea(idea.idea_id, "QA-Agent")
            
            # 测试评论和改进建议
            await innovation_mgr.add_comment(idea.idea_id, "PM-Agent", "这个想法很有价值！", is_improvement=False)
            await innovation_mgr.add_comment(idea.idea_id, "Dev-Agent", "可以集成到 CI/CD 流程中", is_improvement=True)
            
            # 测试评估
            await innovation_mgr.evaluate_idea(idea.idea_id, feasibility=85, impact=90)
            
            # 推进阶段
            await innovation_mgr.advance_stage(idea.idea_id)
            
            # 测试统计数据
            stats = innovation_mgr.get_stats()
            print(f"   ✅ 创新讨论场景测试通过 (总创意数：{stats['total']}, 平均可行性：{stats['avg_feasibility']:.1f})")
            return True
        
        asyncio.run(test_innovation())
        test_results["innovation"]["tested"] = True
        
    except Exception as e:
        test_results["innovation"]["errors"].append(f"功能测试失败：{e}")
        print(f"   ❌ 功能测试失败：{e}")


# =============================================================================
# 测试结果汇总
# =============================================================================
print()
print("=" * 70)
print("📊 测试结果汇总")
print("=" * 70)
print()

total_scenarios = 5
passed_scenarios = 0
failed_scenarios = 0
warnings = []

for scenario_name, result in test_results.items():
    status_icon = "✅" if (result["loaded"] and result["tested"]) else "❌"
    status_text = "通过" if (result["loaded"] and result["tested"]) else "失败"
    
    if result["loaded"] and result["tested"]:
        passed_scenarios += 1
    else:
        failed_scenarios += 1
    
    print(f"   {status_icon} {scenario_name}.py: {status_text}")
    
    if result["errors"]:
        for error in result["errors"]:
            warnings.append(f"⚠️  {scenario_name}.py: {error}")
            print(f"      └─ {error}")

print()
print("-" * 70)
print(f"   总计：{total_scenarios} 个场景")
print(f"   ✅ 通过：{passed_scenarios} 个")
print(f"   ❌ 失败：{failed_scenarios} 个")
print(f"   通过率：{(passed_scenarios / total_scenarios * 100):.1f}%")
print("-" * 70)

if warnings:
    print()
    print("⚠️  错误和警告:")
    for warning in warnings:
        print(f"   {warning}")

print()
if passed_scenarios == total_scenarios:
    print("🎉 所有场景模块测试通过！")
else:
    print(f"⚡ {passed_scenarios}/{total_scenarios} 场景测试通过")

print()
print("=" * 70)
