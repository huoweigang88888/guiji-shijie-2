#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三天工作任务 - 总控脚本

一键启动，自动完成三天任务
"""

import asyncio
import sys
import os
from datetime import datetime

sys.path.insert(0, '.')


async def run_all_days():
    """运行全部三天任务"""
    print("=" * 60)
    print("🌍 硅基世界 2 - 三天工作任务")
    print("=" * 60)
    print(f"启动时间：{datetime.now().isoformat()}")
    print()
    
    # 创建 reports 目录
    os.makedirs("reports", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/knowledge", exist_ok=True)
    os.makedirs("data/stories", exist_ok=True)
    
    # Day 1
    print("\n" + "📅" * 30)
    print("📅 Day 1: 世界启动 + 基础互动验证")
    print("📅" * 30 + "\n")
    
    from tasks.day1_auto_run import day1_mission
    await day1_mission()
    
    await asyncio.sleep(5)  # 休息 5 秒
    
    # Day 2
    print("\n" + "📅" * 30)
    print("📅 Day 2: 深化互动 + 协作任务")
    print("📅" * 30 + "\n")
    
    from tasks.day2_auto_run import day2_mission
    await day2_mission()
    
    await asyncio.sleep(5)  # 休息 5 秒
    
    # Day 3
    print("\n" + "📅" * 30)
    print("📅 Day 3: 自主演化 + 成果展示")
    print("📅" * 30 + "\n")
    
    from tasks.day3_auto_run import day3_mission
    await day3_mission()
    
    print("\n" + "=" * 60)
    print("✅ 三天工作任务全部完成！")
    print("=" * 60)
    print(f"完成时间：{datetime.now().isoformat()}")


if __name__ == "__main__":
    try:
        asyncio.run(run_all_days())
    except KeyboardInterrupt:
        print("\n👋 任务中断")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
