"""
硅基世界 2 - 测试脚本

测试所有核心功能模块
"""

import sys
from pathlib import Path

# 添加 agents 目录到路径
agents_dir = Path(__file__).parent / "agents"
sys.path.insert(0, str(agents_dir))

def test_all():
    """运行所有测试"""
    print("="*60)
    print("Guiji World 2 - Function Test")
    print("="*60)
    
    # 测试 1: 代理协调器
    print("\n[1/6] Testing Agent Coordinator...")
    try:
        from coordinator import AgentCoordinator
        coordinator = AgentCoordinator()
        result = coordinator.execute_task("Research AI technology")
        print(f"   [PASS] Coordinator: {result['status']}")
    except Exception as e:
        print(f"   [FAIL] Coordinator: {e}")
    
    # 测试 2: 研究助手
    print("\n[2/6] Testing Research Assistant...")
    try:
        from researcher import ResearchAssistant
        assistant = ResearchAssistant()
        report = assistant.research("Python programming", count=3)
        print(f"   [PASS] Researcher: generated {len(report)} bytes")
    except Exception as e:
        print(f"   [FAIL] Researcher: {e}")
    
    # 测试 3: 消息聚合器
    print("\n[3/6] Testing Message Aggregator...")
    try:
        from message_aggregator import MessageAggregator, MessagePlatform, Message
        from datetime import datetime
        
        aggregator = MessageAggregator()
        msg = Message("Test message", MessagePlatform.WHATSAPP, "Test User", datetime.now())
        aggregator.receive_message(msg)
        summary = aggregator.get_summary()
        print(f"   [PASS] Message Aggregator: {summary[:50]}...")
    except Exception as e:
        print(f"   [FAIL] Message Aggregator: {e}")
    
    # 测试 4: 心跳系统
    print("\n[4/6] Testing Heartbeat System...")
    try:
        from heartbeat import HeartbeatSystem
        system = HeartbeatSystem()
        report = system.run_check()
        print(f"   [PASS] Heartbeat: {report.summary}")
    except Exception as e:
        print(f"   [FAIL] Heartbeat: {e}")
    
    # 测试 5: 自动任务执行器
    print("\n[5/6] Testing Auto Executor...")
    try:
        from auto_executor import AutoExecutor, TaskPriority
        
        executor = AutoExecutor()
        goal = executor.add_goal("Test Goal", "This is a test goal")
        tasks = executor.generate_tasks(goal.id, [
            {'title': 'Test Task 1', 'description': 'Description', 'priority': 'normal'}
        ])
        progress = executor.get_progress(goal.id)
        print(f"   [PASS] Auto Executor: progress {progress['progress_percent']}%")
    except Exception as e:
        print(f"   [FAIL] Auto Executor: {e}")
    
    # 测试 6: 自我改进器
    print("\n[6/6] Testing Self Improver...")
    try:
        from self_improver import SelfImprover
        
        improver = SelfImprover()
        improver.record_error('TestError', 'This is a test error')
        summary = improver.get_summary()
        print(f"   [PASS] Self Improver: {len(improver.lessons)} lessons")
    except Exception as e:
        print(f"   [FAIL] Self Improver: {e}")
    
    # 总结
    print("\n" + "="*60)
    print("All Tests Completed!")
    print("="*60)


if __name__ == '__main__':
    test_all()
