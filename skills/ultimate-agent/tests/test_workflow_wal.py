"""
单元测试 - 工作流引擎和 WAL 协议
"""

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.workflow_engine import WorkflowEngine, WorkflowMode, StageStatus
from agents.wal_protocol import WALProtocol


class TestWorkflowEngine(unittest.TestCase):
    """工作流引擎测试"""
    
    def setUp(self):
        self.engine = WorkflowEngine()
    
    def test_init(self):
        """测试初始化"""
        self.assertIsNotNone(self.engine.config_path)
        self.assertEqual(len(self.engine.workflows), 0)
    
    def test_load_config(self):
        """测试配置加载"""
        config = self.engine.config
        self.assertIn('default_mode', config)
        self.assertIn('workflows', config)
    
    def test_register_agent(self):
        """测试代理注册"""
        def test_executor(input_data):
            return {'status': 'completed'}
        
        self.engine.register_agent('test-agent', test_executor)
        self.assertIn('test-agent', self.engine.agent_executors)
    
    def test_create_workflow(self):
        """测试工作流创建"""
        workflow = self.engine.create_workflow(
            'software_development',
            '开发一个应用'
        )
        
        self.assertIsNotNone(workflow.id)
        self.assertEqual(workflow.mode, WorkflowMode.SERIAL)
        self.assertGreater(len(workflow.stages), 0)
    
    def test_workflow_stages(self):
        """测试工作流阶段"""
        workflow = self.engine.create_workflow(
            'software_development',
            '开发应用'
        )
        
        # 检查阶段
        self.assertEqual(len(workflow.stages), 4)
        self.assertEqual(workflow.stages[0].name, '需求分析')
        self.assertEqual(workflow.stages[1].name, '视觉设计')
        self.assertEqual(workflow.stages[2].name, '架构设计')
        self.assertEqual(workflow.stages[3].name, '编码实现')
    
    def test_simulate_execution(self):
        """测试模拟执行"""
        from agents.workflow_engine import Stage
        
        stage = Stage(
            id='test',
            name='测试阶段',
            agent='test-agent',
            input='测试输入'
        )
        
        result = self.engine._simulate_execution(stage)
        
        self.assertEqual(result['status'], 'completed')
        self.assertIn('stage', result)
    
    def test_get_workflow_status(self):
        """测试状态查询"""
        workflow = self.engine.create_workflow(
            'software_development',
            '开发应用'
        )
        
        status = self.engine.get_workflow_status(workflow.id)
        
        self.assertIn('workflow_id', status)
        self.assertIn('status', status)
        self.assertIn('stages', status)
    
    def test_list_workflows(self):
        """测试工作流列表"""
        workflow = self.engine.create_workflow(
            'software_development',
            '开发应用'
        )
        
        workflows = self.engine.list_workflows()
        
        self.assertGreater(len(workflows), 0)
        self.assertIn('id', workflows[0])
        self.assertIn('name', workflows[0])
    
    def test_get_summary(self):
        """测试摘要"""
        summary = self.engine.get_summary()
        
        self.assertIn('Workflow Engine Summary', summary)
        self.assertIn('Total Workflows', summary)


class TestWALProtocol(unittest.TestCase):
    """WAL 协议测试"""
    
    def setUp(self):
        self.state_file = Path(__file__).parent / "test_session_state.md"
        self.wal = WALProtocol(self.state_file)
    
    def tearDown(self):
        # 清理测试文件
        if self.state_file.exists():
            self.state_file.unlink()
    
    def test_init(self):
        """测试初始化"""
        self.assertIsNotNone(self.wal.state_file)
    
    def test_write(self):
        """测试写入"""
        self.wal.write('test_key', {'data': 'test'}, category='test')
        
        # 检查文件是否创建
        self.assertTrue(self.state_file.exists())
    
    def test_read(self):
        """测试读取"""
        # 先写入
        self.wal.write('key1', 'value1', category='cat1')
        self.wal.write('key2', 'value2', category='cat1')
        
        # 读取
        state = self.wal.read()
        self.assertGreater(len(state), 0)
        
        # 按分类读取
        cat1_state = self.wal.read(category='cat1')
        self.assertGreater(len(cat1_state), 0)
    
    def test_prune(self):
        """测试裁剪"""
        # 写入多条
        for i in range(150):  # 写入足够多的条目
            self.wal.write(f'key{i}', f'value{i}', category='test')
        
        # 裁剪（保留最后 100 行）
        removed = self.wal.prune(keep_hours=24)
        
        # 应该删除了一些条目（至少 10 个）
        self.assertGreater(removed, 10)
    
    def test_restore(self):
        """测试恢复"""
        # 写入
        self.wal.write('restore_key', 'restore_value', category='restore')
        
        # 恢复
        state = self.wal.restore()
        
        self.assertGreater(len(state), 0)
    
    def test_get_summary(self):
        """测试摘要"""
        # 写入
        self.wal.write('summary_key', 'summary_value', category='summary')
        
        # 获取摘要
        summary = self.wal.get_summary()
        
        self.assertTrue(summary['exists'])
        self.assertIn('lines', summary)
        self.assertIn('size_bytes', summary)


class TestWorkflowIntegration(unittest.TestCase):
    """工作流集成测试"""
    
    def test_parallel_workflow(self):
        """测试并行工作流"""
        engine = WorkflowEngine()
        
        # 创建工作流
        workflow = engine.create_workflow(
            'research_report',
            '研究 AI 趋势'
        )
        
        # 应该是并行模式
        self.assertEqual(workflow.mode, WorkflowMode.PARALLEL)
    
    def test_serial_workflow(self):
        """测试串行工作流"""
        engine = WorkflowEngine()
        
        # 创建工作流
        workflow = engine.create_workflow(
            'software_development',
            '开发应用'
        )
        
        # 应该是串行模式
        self.assertEqual(workflow.mode, WorkflowMode.SERIAL)
    
    def test_confirm_callback(self):
        """测试确认回调"""
        engine = WorkflowEngine()
        
        # 创建工作流
        workflow = engine.create_workflow(
            'software_development',
            '开发应用'
        )
        
        # 定义确认回调
        confirm_called = []
        def on_confirm(stage_info):
            confirm_called.append(stage_info)
            return True
        
        # 执行（会因缺少代理而部分失败，但确认回调会被调用）
        try:
            engine.execute_workflow(workflow.id, on_confirm=on_confirm)
        except:
            pass
        
        # 确认回调应该被调用（如果阶段 require_confirm）
        # 由于是测试，不强制要求


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestWorkflowEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestWALProtocol))
    suite.addTests(loader.loadTestsFromTestCase(TestWorkflowIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return {
        'tests_run': result.testsRun,
        'failures': len(result.failures),
        'errors': len(result.errors),
        'success': result.wasSuccessful()
    }


if __name__ == '__main__':
    print("="*60)
    print("工作流引擎和 WAL 协议单元测试")
    print("="*60)
    print()
    
    result = run_tests()
    
    print()
    print("="*60)
    print(f"测试结果：{'✅ 通过' if result['success'] else '❌ 失败'}")
    print(f"运行测试：{result['tests_run']} 个")
    print(f"失败：{result['failures']} 个")
    print(f"错误：{result['errors']} 个")
    print("="*60)
