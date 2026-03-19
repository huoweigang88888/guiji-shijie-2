# 硅基世界 2 - 代理配置文件
# Author: 三二 🐱
# Date: 2026-03-19

"""
代理系统配置

此文件定义了系统中所有代理的配置信息。
"""

# ========== 代理配置 ==========
AGENTS = {
    # 核心代理 (agents/core/)
    "core": {
        "path": "agents.core",
        "modules": [
            "core",
            "decision",
            "executor",
            "memory",
            "llm",
            "personality"
        ]
    },
    
    # 专用代理 (agents/specialized/)
    "specialized": {
        "path": "agents.specialized",
        "modules": [
            "coordinator",
            "researcher",
            "analyst",
            "notifier",
            "reporter",
            # 可选: scheduler (待实现)
        ]
    }
}

# ========== 代理实例配置 ==========
INSTANCES = {
    "coordinator": {
        "enabled": True,
        "priority": 1,
        "config": {}
    },
    "researcher": {
        "enabled": True,
        "priority": 2,
        "config": {}
    },
    "analyst": {
        "enabled": True,
        "priority": 3,
        "config": {}
    },
    "notifier": {
        "enabled": True,
        "priority": 4,
        "config": {}
    },
    "reporter": {
        "enabled": True,
        "priority": 5,
        "config": {}
    }
}

# ========== 代理协作规则 ==========
COLLABORATION = {
    # 任务分发规则
    "task_routing": {
        "policy": "priority",
        "default_routing": "coordinator"
    },
    
    # 代理间通信
    "communication": {
        "protocol": "internal",  # internal | a2a
        "timeout": 30,
        "retry_times": 3
    }
}

# ========== 全局代理设置 ==========
GLOBAL = {
    "default_model": "bailian/qwen3.5-plus",
    "max_concurrent_tasks": 5,
    "task_timeout": 300,
    "default_output_format": "markdown"
}
