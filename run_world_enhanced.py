#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
硅基世界 2 - 增强版运行脚本

改进：
1. 集成统计追踪器
2. 自动保存数据
3. 更好的错误处理
4. 实时状态输出
"""

import asyncio
import sys
import signal
import os
from datetime import datetime

sys.path.insert(0, '.')

from world.engine import WorldEngine
from world.message_bus import get_message_bus
from world.map import get_world_map
from world.story_generator import get_story_generator
from world.knowledge_graph import get_knowledge_graph
from world.stats_tracker import get_stats_tracker
from world.economy import get_economy_manager


# 全局标志
running = True


def signal_handler(sig, frame):
    """处理中断信号"""
    global running
    print("\n\n👋 收到中断信号，正在保存数据...")
    running = False


async def run_world_enhanced(duration_seconds: int = 300):
    """
    增强版世界运行
    
    Args:
        duration_seconds: 运行时长（秒），默认 300 秒（5 分钟）
    """
    global running
    
    print("=" * 60)
    print("🌍 硅基世界 2 - 增强版")
    print("=" * 60)
    print(f"启动时间：{datetime.now().isoformat()}")
    print(f"预计运行：{duration_seconds} 秒")
    print()
    
    # 注册信号处理
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 创建目录
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/knowledge", exist_ok=True)
    os.makedirs("data/stories", exist_ok=True)
    os.makedirs("data/stats", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    # 初始化系统
    print("📦 初始化系统...")
    engine = WorldEngine()
    message_bus = get_message_bus()
    world_map = get_world_map()
    story_gen = get_story_generator()
    knowledge_graph = get_knowledge_graph()
    stats_tracker = get_stats_tracker()
    economy = get_economy_manager()
    
    print("  ✅ 世界引擎")
    print("  ✅ 消息总线")
    print("  ✅ 世界地图")
    print("  ✅ 故事生成器")
    print("  ✅ 知识图谱")
    print("  ✅ 统计追踪器")
    print("  ✅ 经济系统")
    print()
    
    # 启动世界引擎
    print("🚀 启动世界引擎...")
    await engine.start()
    print("  ✅ 世界引擎已启动")
    print()
    
    # 运行循环
    print("=" * 60)
    print("🎬 世界开始运行")
    print("=" * 60)
    print()
    
    start_time = datetime.now().timestamp()
    snapshot_interval = 30  # 每 30 秒拍摄快照
    save_interval = 60  # 每 60 秒保存数据
    last_snapshot = start_time
    last_save = start_time
    
    try:
        while running:
            current_time = datetime.now().timestamp()
            elapsed = current_time - start_time
            
            # 检查是否到达运行时长
            if elapsed >= duration_seconds:
                print(f"\n⏰ 达到运行时长 ({duration_seconds} 秒)")
                break
            
            # 拍摄统计快照
            if current_time - last_snapshot >= snapshot_interval:
                print()
                stats_tracker.take_snapshot(
                    world_day=engine._day,
                    time_of_day=engine._current_time_of_day.value,
                    total_stories=len(story_gen.stories),
                    total_knowledge=len(knowledge_graph.nodes),
                    total_relationships=len(engine.relationships),
                    deep_relationships=sum(
                        1 for r in engine.relationships.values()
                        if r.get('value', 0) >= 50
                    ),
                    total_agents=18,
                    total_credits=economy.get_total_credits() if hasattr(economy, 'get_total_credits') else 0,
                )
                last_snapshot = current_time
            
            # 保存数据
            if current_time - last_save >= save_interval:
                print("\n💾 保存数据...")
                # engine.save_state()  # 暂时跳过，引擎未实现
                knowledge_graph.save()
                story_gen.save()
                stats_tracker.save()
                print("  ✅ 数据已保存")
                last_save = current_time
            
            # 等待
            await asyncio.sleep(5)
    
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 停止引擎
        print("\n🛑 停止世界引擎...")
        await engine.stop()
        
        # 保存最终数据
        print("\n💾 保存最终数据...")
        # engine.save_state()  # 暂时跳过
        knowledge_graph.save()
        story_gen.save()
        stats_tracker.save()
        
        # 生成报告
        print("\n📝 生成报告...")
        generate_final_report(engine, story_gen, knowledge_graph, stats_tracker)
        
        print()
        print("=" * 60)
        print("✅ 硅基世界 2 运行完成")
        print("=" * 60)
        print(f"完成时间：{datetime.now().isoformat()}")
        print(f"运行时长：{elapsed:.1f} 秒")
        print()
        print("📁 输出文件:")
        print("  - reports/final_report.md")
        print("  - reports/stats_report.md")
        print("  - data/knowledge/knowledge_graph.json")
        print("  - data/stories/stories.json")
        print("  - data/stats/stats_history.json")


def generate_final_report(engine, story_gen, knowledge_graph, stats_tracker):
    """生成最终报告"""
    summary = stats_tracker.get_summary()
    
    report = f"""# 🌍 硅基世界 2 - 运行报告

**生成时间**: {datetime.now().isoformat()}

---

## 📊 核心统计

"""
    
    if "error" not in summary:
        current = summary["current"]
        report += f"""| 指标 | 数值 |
|------|------|
| 运行时长 | {current.get('world_day', 0)} 天 |
| 消息总数 | {current['total_messages']} |
| 故事数量 | {current['total_stories']} |
| 知识节点 | {current['total_knowledge_nodes']} |
| 关系对数 | {current['total_relationships']} |
| 深度关系 | {current['deep_relationships']} |
| 活跃 Agent | {current['active_agents']}/{current['total_agents']} |
| 总信用点 | {current['total_credits']} |

"""
    
    # 故事列表
    report += "## 📖 诞生的故事\n\n"
    if story_gen.stories:
        for i, story in enumerate(story_gen.stories[:10], 1):
            report += f"{i}. **{story.title}** - {story.story_type.value}\n"
    else:
        report += "*暂无故事*\n"
    report += "\n"
    
    # 知识列表
    report += "## 📚 知识节点\n\n"
    if knowledge_graph.nodes:
        for node in list(knowledge_graph.nodes.values())[:10]:
            report += f"- **{node.title}** ({node.knowledge_type.value}) by {node.creator}\n"
    else:
        report += "*暂无知识节点*\n"
    report += "\n"
    
    # 验证结论
    report += """## ✅ 验证结论

- """ + ("✅" if engine._day > 0 else "❌") + """ 世界引擎正常运行
- """ + ("✅" if stats_tracker.message_count > 0 else "❌") + """ 消息系统正常
- """ + ("✅" if len(story_gen.stories) > 0 else "❌") + """ 故事生成正常
- """ + ("✅" if len(knowledge_graph.nodes) > 0 else "❌") + """ 知识沉淀正常
- """ + ("✅" if len(engine.relationships) > 0 else "❌") + """ 关系演化正常

---

*硅基世界 2 | 创世元年*
"""
    
    # 保存报告
    with open("reports/final_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    # 导出统计报告
    stats_tracker.export_markdown("reports/stats_report.md")
    
    print("  ✅ 最终报告已生成")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="硅基世界 2 - 增强版运行")
    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=300,
        help="运行时长（秒），默认 300 秒"
    )
    
    args = parser.parse_args()
    
    try:
        asyncio.run(run_world_enhanced(args.duration))
    except KeyboardInterrupt:
        print("\n👋 用户中断")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
