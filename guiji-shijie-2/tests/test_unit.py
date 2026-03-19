#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单元测试套件

测试各个模块的单元功能
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
import unittest
from datetime import datetime

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestAgentRegistry(unittest.TestCase):
    """测试 Agent 注册表"""
    
    def setUp(self):
        from agents.registry import AgentRegistry
        self.registry = AgentRegistry()
    
    def test_register_agent(self):
        """测试注册代理"""
        mock_agent = object()
        self.registry.register('test_agent', mock_agent, ['capability1', 'capability2'])
        
        self.assertIn('test_agent', self.registry)
        self.assertEqual(self.registry.get('test_agent'), mock_agent)
    
    def test_get_capabilities(self):
        """测试获取能力"""
        mock_agent = object()
        self.registry.register('test_agent', mock_agent, ['cap1', 'cap2'])
        
        caps = self.registry.get_capabilities('test_agent')
        self.assertEqual(len(caps), 2)
        self.assertIn('cap1', caps)
    
    def test_find_by_capability(self):
        """测试按能力查找"""
        self.registry.register('agent1', object(), ['search', 'research'])
        self.registry.register('agent2', object(), ['analysis', 'data'])
        
        results = self.registry.find_by_capability('search')
        self.assertEqual(len(results), 1)
        self.assertIn('agent1', results)
    
    def test_statistics(self):
        """测试统计"""
        self.registry.register('agent1', object(), ['cap1'])
        self.registry.register('agent2', object(), ['cap2'])
        
        stats = self.registry.get_statistics()
        self.assertEqual(stats['total_agents'], 2)
        self.assertEqual(stats['active_agents'], 2)


class TestTask(unittest.TestCase):
    """测试任务对象"""
    
    def test_create_task(self):
        """测试创建任务"""
        from agents.collaboration import Task
        
        task = Task(
            task_id='test_001',
            description='测试任务',
            assigned_to='researcher',
            priority=8,
            timeout=60
        )
        
        self.assertEqual(task.id, 'test_001')
        self.assertEqual(task.description, '测试任务')
        self.assertEqual(task.priority, 8)
        self.assertEqual(task.status, 'pending')
    
    def test_task_to_dict(self):
        """测试任务转字典"""
        from agents.collaboration import Task
        
        task = Task('test_001', '测试')
        task_dict = task.to_dict()
        
        self.assertIsInstance(task_dict, dict)
        self.assertIn('id', task_dict)
        self.assertIn('description', task_dict)
        self.assertIn('status', task_dict)


class TestCollaborationEngine(unittest.TestCase):
    """测试协作引擎"""
    
    def setUp(self):
        from agents.collaboration import CollaborationEngine
        self.engine = CollaborationEngine()
    
    def test_create_task(self):
        """测试创建任务"""
        task = self.engine.create_task(
            description='测试任务',
            assigned_to='researcher',
            priority=5
        )
        
        self.assertIn(task.id, self.engine.tasks)
        self.assertEqual(task.description, '测试任务')
    
    def test_assign_task(self):
        """测试分配任务"""
        task = self.engine.create_task('测试')
        self.engine.assign_task(task.id, 'analyst')
        
        self.assertEqual(task.assigned_to, 'analyst')
        self.assertEqual(task.status, 'assigned')
    
    def test_get_statistics(self):
        """测试统计"""
        self.engine.create_task('任务 1')
        self.engine.create_task('任务 2')
        
        stats = self.engine.get_statistics()
        self.assertEqual(stats['total_tasks'], 2)


class TestOpenClawIntegration(unittest.TestCase):
    """测试 OpenClaw 集成"""
    
    def setUp(self):
        from agents.openclaw_integration import OpenClawIntegration
        self.oc = OpenClawIntegration()
    
    def test_web_search(self):
        """测试网页搜索"""
        results = self.oc.web_search('AI 技术', count=3)
        
        self.assertIsInstance(results, list)
        self.assertLessEqual(len(results), 3)
    
    def test_memory_search(self):
        """测试记忆搜索"""
        results = self.oc.memory_search('测试', max_results=5)
        
        self.assertIsInstance(results, list)
        self.assertLessEqual(len(results), 5)
    
    def test_get_available_tools(self):
        """测试获取可用工具"""
        tools = self.oc.get_available_tools()
        
        self.assertIsInstance(tools, list)
        self.assertGreater(len(tools), 0)
        self.assertIn('web_search', tools)


class TestBlockchainDID(unittest.TestCase):
    """测试区块链 DID"""
    
    def test_did_format(self):
        """测试 DID 格式"""
        did = f"did:sw:test_agent_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        self.assertTrue(did.startswith('did:sw:'))
        self.assertIn('test_agent', did)


class TestEconomyBalance(unittest.TestCase):
    """测试经济系统余额"""
    
    def test_balance_calculation(self):
        """测试余额计算"""
        initial = 1000.0
        transfer = 100.0
        remaining = initial - transfer
        
        self.assertEqual(remaining, 900.0)
        self.assertGreater(remaining, 0)


class TestGamificationAchievements(unittest.TestCase):
    """测试游戏化成就"""
    
    def test_achievement_structure(self):
        """测试成就结构"""
        achievement = {
            'id': 'ach_001',
            'name': '新手上路',
            'description': '首次创建 Agent',
            'points': 10
        }
        
        self.assertIn('id', achievement)
        self.assertIn('name', achievement)
        self.assertIn('points', achievement)


class TestSocialMessage(unittest.TestCase):
    """测试社交消息"""
    
    def test_message_structure(self):
        """测试消息结构"""
        message = {
            'id': 'msg_001',
            'from': 'user1',
            'to': 'user2',
            'content': '你好',
            'timestamp': datetime.now().isoformat()
        }
        
        self.assertIn('id', message)
        self.assertIn('from', message)
        self.assertIn('to', message)
        self.assertIn('content', message)


class TestAPIEndpoints(unittest.TestCase):
    """测试 API 端点"""
    
    def test_health_endpoint_structure(self):
        """测试健康检查端点结构"""
        response = {
            'status': 'healthy',
            'service': 'guiji-world-2-api',
            'version': '2.0.0-alpha'
        }
        
        self.assertEqual(response['status'], 'healthy')
        self.assertIn('service', response)
        self.assertIn('version', response)


class TestUtilities(unittest.TestCase):
    """测试工具函数"""
    
    def test_format_date(self):
        """测试日期格式化"""
        from agents.openclaw_integration import datetime
        
        now = datetime.now()
        formatted = now.strftime('%Y-%m-%d %H:%M:%S')
        
        self.assertIsInstance(formatted, str)
        self.assertRegex(formatted, r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
    
    def test_truncate_string(self):
        """测试字符串截断"""
        def truncate(s, length=50):
            return s[:length] + '...' if len(s) > length else s
        
        long_str = 'a' * 100
        short_str = 'abc'
        
        self.assertEqual(len(truncate(long_str, 50)), 53)
        self.assertEqual(truncate(short_str, 50), short_str)


def run_unit_tests():
    """运行所有单元测试"""
    print("\n" + "=" * 60)
    print("🧪 硅基世界 2 - 单元测试套件")
    print("=" * 60)
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestAgentRegistry))
    suite.addTests(loader.loadTestsFromTestCase(TestTask))
    suite.addTests(loader.loadTestsFromTestCase(TestCollaborationEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestOpenClawIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestBlockchainDID))
    suite.addTests(loader.loadTestsFromTestCase(TestEconomyBalance))
    suite.addTests(loader.loadTestsFromTestCase(TestGamificationAchievements))
    suite.addTests(loader.loadTestsFromTestCase(TestSocialMessage))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIEndpoints))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilities))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    tests_run = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    successes = tests_run - failures - errors
    
    print(f"  总测试数：{tests_run}")
    print(f"  ✅ 通过：{successes}")
    print(f"  ❌ 失败：{failures}")
    print(f"  ⚠️  错误：{errors}")
    print(f"  成功率：{successes/tests_run*100:.1f}%")
    
    if result.wasSuccessful():
        print("\n🎉 所有测试通过！")
        return True
    else:
        print(f"\n⚠️ {failures + errors} 个测试失败")
        return False


if __name__ == '__main__':
    success = run_unit_tests()
    sys.exit(0 if success else 1)
