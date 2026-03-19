#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent 注册表 - 管理所有可用代理

功能:
- 代理注册/注销
- 代理查询
- 代理状态管理
- 代理能力发现
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import importlib
import sys
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class AgentRegistry:
    """Agent 注册表 - 单例模式"""
    
    _instance = None
    _agents: Dict[str, Any] = {}
    _capabilities: Dict[str, List[str]] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._agents = {}
            self._capabilities = {}
            self._agent_status = {}
    
    def register(self, name: str, agent_instance: Any, capabilities: List[str] = None):
        """
        注册一个代理
        
        Args:
            name: 代理名称
            agent_instance: 代理实例
            capabilities: 能力列表
        """
        self._agents[name] = agent_instance
        self._capabilities[name] = capabilities or []
        self._agent_status[name] = {
            'status': 'active',
            'registered_at': datetime.now().isoformat(),
            'last_active': datetime.now().isoformat(),
            'tasks_completed': 0,
            'tasks_failed': 0
        }
        print(f"[Registry] ✅ 代理已注册：{name}")
        print(f"  能力：{', '.join(self._capabilities[name])}")
    
    def unregister(self, name: str):
        """注销一个代理"""
        if name in self._agents:
            del self._agents[name]
            del self._capabilities[name]
            del self._agent_status[name]
            print(f"[Registry] ❌ 代理已注销：{name}")
    
    def get(self, name: str) -> Optional[Any]:
        """获取代理实例"""
        agent = self._agents.get(name)
        if agent and name in self._agent_status:
            self._agent_status[name]['last_active'] = datetime.now().isoformat()
        return agent
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有代理"""
        return self._agents.copy()
    
    def get_status(self, name: str) -> Optional[Dict]:
        """获取代理状态"""
        return self._agent_status.get(name)
    
    def get_all_status(self) -> Dict[str, Dict]:
        """获取所有代理状态"""
        return self._agent_status.copy()
    
    def get_capabilities(self, name: str) -> List[str]:
        """获取代理能力"""
        return self._capabilities.get(name, [])
    
    def find_by_capability(self, capability: str) -> List[str]:
        """根据能力查找代理"""
        matching_agents = []
        for name, caps in self._capabilities.items():
            if capability in caps:
                matching_agents.append(name)
        return matching_agents
    
    def list_agents(self) -> List[Dict]:
        """列出所有代理信息"""
        result = []
        for name, agent in self._agents.items():
            result.append({
                'name': name,
                'capabilities': self._capabilities.get(name, []),
                'status': self._agent_status.get(name, {})
            })
        return result
    
    def update_stats(self, name: str, success: bool = True):
        """更新代理统计"""
        if name in self._agent_status:
            if success:
                self._agent_status[name]['tasks_completed'] += 1
            else:
                self._agent_status[name]['tasks_failed'] += 1
            self._agent_status[name]['last_active'] = datetime.now().isoformat()
    
    def get_statistics(self) -> Dict:
        """获取注册表统计"""
        total_agents = len(self._agents)
        active_agents = sum(1 for s in self._agent_status.values() if s['status'] == 'active')
        total_tasks = sum(s['tasks_completed'] + s['tasks_failed'] for s in self._agent_status.values())
        successful_tasks = sum(s['tasks_completed'] for s in self._agent_status.values())
        
        return {
            'total_agents': total_agents,
            'active_agents': active_agents,
            'total_tasks': total_tasks,
            'successful_tasks': successful_tasks,
            'failed_tasks': total_tasks - successful_tasks,
            'success_rate': (successful_tasks / total_tasks * 100) if total_tasks > 0 else 0
        }
    
    def __len__(self):
        return len(self._agents)
    
    def __contains__(self, name: str):
        return name in self._agents
    
    def __repr__(self):
        return f"AgentRegistry(agents={len(self._agents)}, capabilities={len(self._capabilities)})"


# 全局注册表实例
registry = AgentRegistry()


def auto_register_specialized_agents():
    """自动注册专用代理"""
    from agents.specialized import coordinator, researcher, analyst, notifier, reporter
    
    # 创建代理实例
    agents = {
        'coordinator': coordinator.CoordinatorAgent(),
        'researcher': researcher.ResearcherAgent(),
        'analyst': analyst.AnalystAgent(),
        'notifier': notifier.NotifierAgent(),
        'reporter': reporter.ReporterAgent()
    }
    
    # 注册每个代理
    for name, agent in agents.items():
        try:
            capabilities = agent.get_capabilities() if hasattr(agent, 'get_capabilities') else []
            registry.register(name, agent, capabilities)
        except Exception as e:
            print(f"[Registry] ❌ 注册代理失败 {name}: {e}")
    
    print(f"\n[Registry] 🎉 已注册 {len(registry)} 个专用代理")
    return registry


if __name__ == "__main__":
    # 测试注册表
    print("=" * 60)
    print("Agent 注册表测试")
    print("=" * 60)
    
    # 自动注册专用代理
    auto_register_specialized_agents()
    
    # 列出所有代理
    print("\n📋 已注册代理:")
    for agent_info in registry.list_agents():
        print(f"  - {agent_info['name']}: {', '.join(agent_info['capabilities'])}")
    
    # 获取统计
    print("\n📊 统计信息:")
    stats = registry.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
