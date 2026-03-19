#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
硅基世界 2 - 代理测试脚本
测试所有代理模块是否正常工作
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_coordinator():
    """测试协调器代理"""
    print("=" * 60)
    print("测试：Coordinator Agent")
    print("=" * 60)
    
    from agents.coordinator import CoordinatorAgent
    
    coordinator = CoordinatorAgent()
    
    # 测试注册代理
    coordinator.register_agent("researcher", ["网络搜索", "信息整理"])
    coordinator.register_agent("analyst", ["数据分析", "统计"])
    
    # 测试执行任务
    result = coordinator.execute("研究 2026 年 AI 发展趋势")
    
    print(f"✅ 协调器测试通过\n")
    return True

def test_researcher():
    """测试研究员代理"""
    print("=" * 60)
    print("测试：Researcher Agent")
    print("=" * 60)
    
    from agents.researcher import ResearcherAgent
    
    researcher = ResearcherAgent()
    result = researcher.execute("2026 年 AI 发展趋势", count=5)
    
    print(f"✅ 研究员测试通过\n")
    return True

def test_analyst():
    """测试分析师代理"""
    print("=" * 60)
    print("测试：Analyst Agent")
    print("=" * 60)
    
    from agents.analyst import AnalystAgent
    
    analyst = AnalystAgent()
    
    # 加载示例数据
    sample_data = [
        {"date": "2026-03-01", "value": 100},
        {"date": "2026-03-02", "value": 120},
        {"date": "2026-03-03", "value": 115},
    ]
    analyst.load_data("sales", sample_data)
    
    # 执行分析
    result = analyst.execute("分析销售数据趋势")
    
    print(f"✅ 分析师测试通过\n")
    return True

def test_notifier():
    """测试通知代理"""
    print("=" * 60)
    print("测试：Notifier Agent")
    print("=" * 60)
    
    from agents.notifier import NotifierAgent
    
    notifier = NotifierAgent()
    
    # 发送测试通知
    notifier.send("测试通知", "这是一条测试消息", channel="console", priority="normal")
    notifier.send("系统警告", "CPU 使用率过高", channel="system", priority="high")
    
    print(f"✅ 通知器测试通过\n")
    return True

def test_all():
    """运行所有测试"""
    print("\n")
    print("🧪 硅基世界 2 - 代理测试套件")
    print("=" * 60)
    print()
    
    tests = [
        ("协调器", test_coordinator),
        ("研究员", test_researcher),
        ("分析师", test_analyst),
        ("通知器", test_notifier),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {name} 测试失败：{e}\n")
            failed += 1
    
    print("=" * 60)
    print(f"测试结果：{passed} 通过，{failed} 失败")
    print("=" * 60)
    
    return failed == 0

if __name__ == "__main__":
    success = test_all()
    sys.exit(0 if success else 1)
