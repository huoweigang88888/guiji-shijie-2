"""
业务代理使用演示

演示如何使用 4 个业务代理完成完整的软件开发流程
"""

from agents.business_roles.product_manager import ProductManagerAgent
from agents.business_roles.ui_designer import UIDesignerAgent
from agents.business_roles.architect import ArchitectAgent
from agents.business_roles.senior_dev import SeniorDevAgent


def main():
    print("="*70)
    print("OpenClaw Ultimate Agent - 业务代理使用演示")
    print("="*70)
    print()
    
    # 用户需求
    user_requirement = "开发一个智能待办事项应用，支持任务管理、提醒功能、数据统计"
    print(f"用户需求：{user_requirement}")
    print()
    
    # 步骤 1: 产品经理生成 PRD
    print("="*70)
    print("步骤 1: 产品经理 - 需求分析 & PRD 生成")
    print("="*70)
    
    pm = ProductManagerAgent()
    pm_result = pm.execute(user_requirement)
    
    print(f"[OK] PRD 已生成")
    print(f"   项目名称：{pm_result['project_name']}")
    print(f"   PRD 路径：{pm_result['prd_path']}")
    print(f"   消息：{pm_result['message']}")
    print()
    
    # 步骤 2: UI 设计师创建设计
    print("="*70)
    print("步骤 2: UI 设计师 - 视觉设计")
    print("="*70)
    
    ui = UIDesignerAgent()
    ui_result = ui.execute(pm_result['prd_path'])
    
    print(f"[OK] 设计已完成")
    print(f"   项目名称：{ui_result['project_name']}")
    print(f"   设计路径：{ui_result['design_path']}")
    print(f"   配色方案：{ui_result['color_scheme']}")
    print(f"   消息：{ui_result['message']}")
    print()
    
    # 步骤 3: 架构师设计技术方案
    print("="*70)
    print("步骤 3: 架构师 - 技术选型 & 架构设计")
    print("="*70)
    
    arch = ArchitectAgent()
    arch_result = arch.execute(pm_result['prd_path'])
    
    print(f"[OK] 技术方案已完成")
    print(f"   项目名称：{arch_result['project_name']}")
    print(f"   方案路径：{arch_result['design_path']}")
    print(f"   消息：{arch_result['message']}")
    print()
    
    # 步骤 4: 开发工程师实现代码
    print("="*70)
    print("步骤 4: 开发工程师 - 代码实现")
    print("="*70)
    
    dev = SeniorDevAgent()
    dev_result = dev.implement(
        tech_design_path=arch_result['design_path'],
        ui_design_path=ui_result['design_path']
    )
    
    print(f"[OK] 代码已实现")
    print(f"   代码路径：{dev_result['code_path']}")
    print(f"   消息：{dev_result['message']}")
    print()
    
    # 总结
    print("="*70)
    print("项目完成总结")
    print("="*70)
    print()
    print("已生成文件:")
    print(f"  1. PRD 文档：{pm_result['prd_path']}")
    print(f"  2. 设计文档：{ui_result['design_path']}")
    print(f"  3. 技术方案：{arch_result['design_path']}")
    print(f"  4. 源代码：{dev_result['code_path']}")
    print()
    print("="*70)
    print("演示完成！")
    print("="*70)


if __name__ == '__main__':
    main()
