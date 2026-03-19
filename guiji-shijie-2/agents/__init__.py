# 硅基世界 2 - Agent 系统
# Author: 三二 🐱
# Date: 2026-03-19

"""
Agent 系统 - 硅基世界 2 的核心

包含:
- 核心代理 (agents/core/): Agent 基类、决策、执行、记忆等
- 专用代理 (agents/specialized/): 协调器、研究员、分析师等
- 注册表 (registry.py): 代理注册和管理
- 协作引擎 (collaboration.py): 多代理协作机制
- OpenClaw 集成 (openclaw_integration.py): 与 OpenClaw 深度整合
"""

__version__ = "2.0.0-alpha"
__author__ = "三二 🐱"

# 导入核心组件
from agents.registry import registry, AgentRegistry, auto_register_specialized_agents
from agents.collaboration import collaboration, CollaborationEngine, Task
from agents.openclaw_integration import openclaw, OpenClawIntegration, OpenClawAgent

# 导出公共 API
__all__ = [
    # 注册表
    'registry',
    'AgentRegistry',
    'auto_register_specialized_agents',
    
    # 协作引擎
    'collaboration',
    'CollaborationEngine',
    'Task',
    
    # OpenClaw 集成
    'openclaw',
    'OpenClawIntegration',
    'OpenClawAgent',
    
    # 版本信息
    '__version__',
    '__author__'
]


def init_agent_system():
    """初始化 Agent 系统"""
    print("=" * 60)
    print("硅基世界 2 - Agent 系统初始化")
    print("=" * 60)
    
    # 自动注册专用代理
    auto_register_specialized_agents()
    
    # 显示统计
    stats = registry.get_statistics()
    print(f"\n📊 系统统计:")
    print(f"  注册代理：{stats['total_agents']}")
    print(f"  活跃代理：{stats['active_agents']}")
    
    print("\n✅ Agent 系统初始化完成")
    print("=" * 60)
    
    return {
        'registry': registry,
        'collaboration': collaboration,
        'openclaw': openclaw
    }


def get_agent_system_status() -> dict:
    """获取 Agent 系统状态"""
    return {
        'version': __version__,
        'author': __author__,
        'registry': {
            'total_agents': len(registry),
            'agents': registry.list_agents()
        },
        'collaboration': collaboration.get_statistics(),
        'openclaw': {
            'available': openclaw.openclaw_available,
            'tools': openclaw.get_available_tools()
        }
    }


if __name__ == "__main__":
    # 初始化系统
    init_agent_system()
    
    # 显示状态
    print("\n📋 系统状态:")
    status = get_agent_system_status()
    print(f"  版本：{status['version']}")
    print(f"  作者：{status['author']}")
    print(f"  代理数：{status['registry']['total_agents']}")
    print(f"  可用工具：{len(status['openclaw']['tools'])}")
