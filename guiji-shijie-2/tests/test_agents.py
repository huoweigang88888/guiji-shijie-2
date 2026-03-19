#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
"""
Agent 系统测试

测试内容:
1. Agent 注册表
2. 多代理协作
3. OpenClaw 集成
4. 专用代理功能
"""

import sys
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def test_registry():
    """测试 Agent 注册表"""
    print("\n" + "=" * 60)
    print("测试 1: Agent 注册表")
    print("=" * 60)
    
    from agents.registry import AgentRegistry, auto_register_specialized_agents
    
    # 创建注册表
    registry = AgentRegistry()
    print(f"✅ 注册表创建成功：{registry}")
    
    # 自动注册专用代理
    auto_register_specialized_agents()
    print(f"✅ 自动注册完成")
    
    # 列出所有代理
    agents = registry.list_agents()
    print(f"\n📋 已注册代理 ({len(agents)} 个):")
    for agent in agents:
        print(f"  - {agent['name']}: {len(agent['capabilities'])} 个能力")
    
    # 测试查询
    coordinator = registry.get('coordinator')
    assert coordinator is not None, "coordinator 代理应该存在"
    print(f"\n✅ 查询代理成功：coordinator")
    
    # 测试能力查找
    matching = registry.find_by_capability('协调')
    print(f"✅ 能力查找：'协调' -> {matching}")
    
    # 测试统计
    stats = registry.get_statistics()
    print(f"\n📊 统计信息:")
    print(f"  总代理数：{stats['total_agents']}")
    print(f"  活跃代理：{stats['active_agents']}")
    
    print("\n✅ 测试 1 通过：Agent 注册表")
    return True


def test_collaboration():
    """测试多代理协作"""
    print("\n" + "=" * 60)
    print("测试 2: 多代理协作")
    print("=" * 60)
    
    import asyncio
    from agents.collaboration import CollaborationEngine
    
    # 创建协作引擎
    engine = CollaborationEngine()
    print(f"✅ 协作引擎创建成功")
    
    # 创建任务
    task = engine.create_task(
        description="测试任务：研究 AI 发展趋势",
        assigned_to="researcher",
        priority=8,
        timeout=60
    )
    print(f"✅ 任务创建成功：{task.id}")
    
    # 测试任务分配
    engine.assign_task(task.id, "researcher")
    print(f"✅ 任务分配成功")
    
    # 测试工作流
    workflow = [
        {
            'title': '研究任务',
            'description': '研究 AI 技术',
            'assigned_to': 'researcher',
            'priority': 8
        },
        {
            'title': '分析任务',
            'description': '分析研究数据',
            'assigned_to': 'analyst',
            'priority': 7
        }
    ]
    
    async def run_workflow():
        results = await engine.execute_workflow(workflow)
        return results
    
    results = asyncio.run(run_workflow())
    print(f"✅ 工作流执行完成：{len(results)} 个任务")
    
    # 显示统计
    stats = engine.get_statistics()
    print(f"\n📊 协作统计:")
    print(f"  总任务数：{stats['total_tasks']}")
    print(f"  完成：{stats['completed_tasks']}")
    print(f"  成功率：{stats['success_rate']:.1f}%")
    
    print("\n✅ 测试 2 通过：多代理协作")
    return True


def test_openclaw_integration():
    """测试 OpenClaw 集成"""
    print("\n" + "=" * 60)
    print("测试 3: OpenClaw 集成")
    print("=" * 60)
    
    from agents.openclaw_integration import OpenClawIntegration, OpenClawAgent
    
    # 创建集成实例
    oc = OpenClawIntegration()
    print(f"✅ OpenClaw 集成创建成功")
    print(f"  OpenClaw 可用：{oc.openclaw_available}")
    
    # 测试工具列表
    tools = oc.get_available_tools()
    print(f"  可用工具：{len(tools)} 个")
    for tool in tools[:5]:
        print(f"    - {tool}")
    
    # 测试 web_search
    results = oc.web_search("AI 技术 2026", count=3)
    print(f"\n✅ 网页搜索：返回 {len(results)} 个结果")
    
    # 测试 OpenClawAgent
    agent = OpenClawAgent()
    capabilities = agent.get_capabilities()
    print(f"\n✅ OpenClawAgent 能力：{len(capabilities)} 个")
    for cap in capabilities:
        print(f"    - {cap}")
    
    # 测试执行
    result = agent.execute("搜索 AI 最新进展")
    print(f"\n✅ 任务执行：{result['status']}")
    print(f"  使用工具：{', '.join(result['tools_used']) if result['tools_used'] else '无'}")
    
    print("\n✅ 测试 3 通过：OpenClaw 集成")
    return True


def test_specialized_agents():
    """测试专用代理"""
    print("\n" + "=" * 60)
    print("测试 4: 专用代理功能")
    print("=" * 60)
    
    from agents.specialized import coordinator, researcher, analyst, notifier, reporter
    
    agents = {
        'coordinator': coordinator.CoordinatorAgent(),
        'researcher': researcher.ResearcherAgent(),
        'analyst': analyst.AnalystAgent(),
        'notifier': notifier.NotifierAgent(),
        'reporter': reporter.ReporterAgent()
    }
    
    print(f"✅ 创建 5 个专用代理实例")
    
    # 测试每个代理
    for name, agent in agents.items():
        print(f"\n  测试 {name}:")
        
        # 获取能力
        if hasattr(agent, 'get_capabilities'):
            caps = agent.get_capabilities()
            print(f"    能力：{len(caps)} 个")
        
        # 执行简单任务
        if hasattr(agent, 'execute'):
            result = agent.execute(f"测试 {name} 功能")
            if isinstance(result, dict):
                print(f"    执行：{result.get('status', 'unknown')}")
            else:
                print(f"    执行：completed")
    
    print("\n✅ 测试 4 通过：专用代理功能")
    return True


def test_agent_system():
    """测试整个 Agent 系统"""
    print("\n" + "=" * 60)
    print("测试 5: Agent 系统集成测试")
    print("=" * 60)
    
    import agents
    
    # 初始化系统
    components = agents.init_agent_system()
    
    # 获取系统状态
    status = agents.get_agent_system_status()
    
    print(f"\n📊 系统状态:")
    print(f"  版本：{status['version']}")
    print(f"  作者：{status['author']}")
    print(f"  代理数：{status['registry']['total_agents']}")
    print(f"  OpenClaw 可用：{status['openclaw']['available']}")
    
    # 验证组件
    assert 'registry' in components, "应该包含注册表"
    assert 'collaboration' in components, "应该包含协作引擎"
    assert 'openclaw' in components, "应该包含 OpenClaw 集成"
    
    print("\n✅ 测试 5 通过：Agent 系统集成")
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("🧪 硅基世界 2 - Agent 系统测试套件")
    print("=" * 60)
    
    tests = [
        ("Agent 注册表", test_registry),
        ("多代理协作", test_collaboration),
        ("OpenClaw 集成", test_openclaw_integration),
        ("专用代理", test_specialized_agents),
        ("系统集成", test_agent_system)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result, None))
        except Exception as e:
            results.append((name, False, str(e)))
            print(f"\n❌ {name} 测试失败：{e}")
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result, _ in results if result)
    total = len(results)
    
    for name, result, error in results:
        icon = "✅" if result else "❌"
        print(f"  {icon} {name}")
        if error:
            print(f"      错误：{error}")
    
    print(f"\n📈 总计：{passed}/{total} 通过 ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        return True
    else:
        print(f"\n⚠️ {total - passed} 个测试失败")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
