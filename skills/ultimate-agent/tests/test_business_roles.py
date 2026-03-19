"""
单元测试 - 业务角色代理

测试产品、UI、架构、开发四个业务角色代理
"""

import unittest
from pathlib import Path
import sys

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.business_roles.product_manager import ProductManagerAgent
from agents.business_roles.ui_designer import UIDesignerAgent
from agents.business_roles.architect import ArchitectAgent
from agents.business_roles.senior_dev import SeniorDevAgent


class TestProductManager(unittest.TestCase):
    """产品经理代理测试"""
    
    def setUp(self):
        self.agent = ProductManagerAgent()
    
    def test_init(self):
        """测试初始化"""
        self.assertIsNotNone(self.agent.workspace_dir)
        self.assertTrue(self.agent.prd_dir.exists())
    
    def test_analyze_requirement(self):
        """测试需求分析"""
        user_input = "开发一个待办事项应用"
        analysis = self.agent.analyze_requirement(user_input)
        
        self.assertIn('project_name', analysis)
        self.assertIn('goal', analysis)
        self.assertIn('user_roles', analysis)
    
    def test_generate_prd(self):
        """测试 PRD 生成"""
        analysis = {
            'project_name': '测试项目',
            'goal': '测试目标',
            'user_roles': ['用户'],
            'features': ['功能 1'],
            'priority': 'P0'
        }
        
        prd = self.agent.generate_prd(analysis)
        
        self.assertIn('产品需求文档', prd)
        self.assertIn('测试项目', prd)
        self.assertIn('功能列表', prd)
    
    def test_save_prd(self):
        """测试 PRD 保存"""
        prd_content = "# 测试 PRD"
        filepath = self.agent.save_prd(prd_content, 'TestProject')
        
        self.assertTrue(filepath.exists())
        self.assertIn('PRD_TestProject', filepath.name)
    
    def test_execute(self):
        """测试完整执行流程"""
        result = self.agent.execute('开发一个简单应用')
        
        self.assertTrue(result['success'])
        self.assertIn('prd_path', result)
        self.assertIn('message', result)
    
    def test_get_status(self):
        """测试状态查询"""
        status = self.agent.get_status()
        
        self.assertIn('workspace', status)
        self.assertIn('prd_count', status)
        self.assertEqual(status['status'], 'active')


class TestUIDesigner(unittest.TestCase):
    """UI 设计师代理测试"""
    
    def setUp(self):
        self.agent = UIDesignerAgent()
    
    def test_init(self):
        """测试初始化"""
        self.assertIsNotNone(self.agent.workspace_dir)
        self.assertTrue(self.agent.design_dir.exists())
        self.assertEqual(len(self.agent.color_palettes), 4)
    
    def test_color_palettes(self):
        """测试配色方案"""
        self.assertIn('blue', self.agent.color_palettes)
        self.assertIn('green', self.agent.color_palettes)
        self.assertIn('purple', self.agent.color_palettes)
        self.assertIn('orange', self.agent.color_palettes)
    
    def test_generate_design(self):
        """测试设计生成"""
        analysis = {
            'project_name': '测试项目',
            'user_roles': ['用户'],
            'features': ['功能 1'],
            'style_preference': 'blue'
        }
        
        design = self.agent.generate_design(analysis)
        
        self.assertIn('UI 设计文档', design)
        self.assertIn('#1E90FF', design)  # 蓝色主色
        self.assertIn('CSS', design)
    
    def test_save_design(self):
        """测试设计保存"""
        design_content = "# 测试设计"
        filepath = self.agent.save_design(design_content, 'TestProject')
        
        self.assertTrue(filepath.exists())
        self.assertIn('UIDesign_TestProject', filepath.name)
    
    def test_get_status(self):
        """测试状态查询"""
        status = self.agent.get_status()
        
        self.assertIn('workspace', status)
        self.assertIn('design_count', status)


class TestArchitect(unittest.TestCase):
    """架构师代理测试"""
    
    def setUp(self):
        self.agent = ArchitectAgent()
    
    def test_init(self):
        """测试初始化"""
        self.assertIsNotNone(self.agent.workspace_dir)
        self.assertTrue(self.agent.tech_design_dir.exists())
    
    def test_design_architecture(self):
        """测试架构设计"""
        requirements = {
            'project_name': '测试项目',
            'features': ['功能 1'],
            'scale': 'medium'
        }
        
        design = self.agent.design_architecture(requirements)
        
        self.assertIn('技术方案文档', design)
        self.assertIn('技术栈选择', design)
        self.assertIn('mermaid', design)
    
    def test_save_design(self):
        """测试设计保存"""
        content = "# 测试技术方案"
        filepath = self.agent.save_design(content, 'TestProject')
        
        self.assertTrue(filepath.exists())
        self.assertIn('TechDesign_TestProject', filepath.name)


class TestSeniorDev(unittest.TestCase):
    """开发工程师代理测试"""
    
    def setUp(self):
        self.agent = SeniorDevAgent()
    
    def test_init(self):
        """测试初始化"""
        self.assertIsNotNone(self.agent.workspace_dir)
        self.assertTrue(self.agent.src_dir.exists())
    
    def test_create_project_structure(self):
        """测试项目结构创建"""
        self.agent._create_project_structure()
        
        self.assertTrue((self.agent.src_dir / "app").exists())
        self.assertTrue((self.agent.src_dir / "tests").exists())
    
    def test_generate_sample_code(self):
        """测试示例代码生成"""
        code = self.agent._generate_sample_code()
        
        self.assertIn('FastAPI', code)
        self.assertIn('app = FastAPI', code)
    
    def test_generate_readme(self):
        """测试 README 生成"""
        readme = self.agent._generate_readme()
        
        self.assertIn('# 项目', readme)
        self.assertIn('快速开始', readme)
        self.assertIn('安装', readme)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流"""
        # 1. 产品经理生成 PRD
        pm = ProductManagerAgent()
        pm_result = pm.execute('开发一个待办事项应用')
        self.assertTrue(pm_result['success'])
        
        # 2. UI 设计师设计
        ui = UIDesignerAgent()
        ui_result = ui.execute(pm_result['prd_path'])
        self.assertTrue(ui_result['success'])
        
        # 3. 架构师设计
        arch = ArchitectAgent()
        arch_result = arch.execute(pm_result['prd_path'])
        self.assertTrue(arch_result['success'])
        
        # 4. 开发工程师实现
        dev = SeniorDevAgent()
        dev_result = dev.implement(arch_result['design_path'])
        self.assertTrue(dev_result['success'])


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestProductManager))
    suite.addTests(loader.loadTestsFromTestCase(TestUIDesigner))
    suite.addTests(loader.loadTestsFromTestCase(TestArchitect))
    suite.addTests(loader.loadTestsFromTestCase(TestSeniorDev))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回结果
    return {
        'tests_run': result.testsRun,
        'failures': len(result.failures),
        'errors': len(result.errors),
        'success': result.wasSuccessful()
    }


if __name__ == '__main__':
    print("="*60)
    print("业务角色代理单元测试")
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
