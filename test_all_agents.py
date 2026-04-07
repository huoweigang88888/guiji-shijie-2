#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试所有 Agent 是否能正常加载"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 测试所有 Agent 是否能正常导入
agent_files = [
    'ceo_agent',
    'pm_agent', 
    'arch_agent',
    'dev_agent',
    'qa_agent',
    'ui_agent',
    'know_agent',
    'social_agent',
    'fe_agent',
    'be_agent',
    'devops_agent',
    'data_agent',
    'hr_agent',
    'fin_agent',
    'marketing_agent',
    'ml_agent',
    'ba_agent',
    'pmo_agent',
]

print('Testing Agent loading...')
print('=' * 50)

loaded = []
failed = []

for agent_name in agent_files:
    try:
        module = __import__(f'agents.roles.{agent_name}', fromlist=[''])
        # 尝试获取 create 函数
        create_func_name = f'create_{agent_name.replace("_", "")}'
        if hasattr(module, create_func_name):
            create_func = getattr(module, create_func_name)
            agent = create_func()
            loaded.append(agent_name)
            print(f'[OK] {agent_name}: {agent.profile.name} ({agent.profile.role})')
        else:
            # 尝试常见的类名格式
            possible_names = [
                agent_name.replace('_', '').title() + 'Agent',
                agent_name.upper().replace('_', '') + 'Agent',
            ]
            found = False
            for class_name in possible_names:
                if hasattr(module, class_name):
                    agent_class = getattr(module, class_name)
                    agent = agent_class()
                    loaded.append(agent_name)
                    print(f'[OK] {agent_name}: {agent.profile.name} ({agent.profile.role})')
                    found = True
                    break
            
            if not found:
                loaded.append(agent_name)
                print(f'[OK] {agent_name}: Module loaded')
    except Exception as e:
        failed.append((agent_name, str(e)))
        print(f'[FAIL] {agent_name}: {e}')

print('=' * 50)
print(f'Success: {len(loaded)}/18')
print(f'Failed: {len(failed)}/18')

if failed:
    print('\nFailed Agents:')
    for name, error in failed:
        print(f'  - {name}: {error}')
else:
    print('\nAll 18 Agents loaded successfully!')
