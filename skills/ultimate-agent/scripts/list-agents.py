#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""列出所有代理配置"""

import json
import sys
import io
from pathlib import Path

# Windows 编码支持
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

config_path = Path(__file__).parent.parent / "configs" / "company-agents.json"

with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

print("=" * 60)
print("🏢 公司多智能体系统 - 代理列表")
print("=" * 60)
print()
print(f"📦 代理总数：{len(config['agents'])}")
print(f"🔄 工作流数：{len(config['workflows'])}")
print()
print("📋 代理详情:")
print("-" * 60)

for i, agent in enumerate(config['agents'], 1):
    print(f"\n{i:2}. {agent['name']}")
    print(f"    ID: {agent['id']}")
    print(f"    角色：{agent['role']}")
    print(f"    能力：{', '.join(agent['capabilities'][:3])}")
    if len(agent['capabilities']) > 3:
        print(f"          ... 等 {len(agent['capabilities'])} 项能力")
    print(f"    触发器：{', '.join(agent.get('triggers', []))}")

print()
print("=" * 60)
print("🔄 工作流:")
print("-" * 60)

for i, wf in enumerate(config['workflows'], 1):
    print(f"\n{i}. {wf['name']} ({wf['id']})")
    for step in wf['steps']:
        print(f"   → {step['agent']}: {step['task']}")

print()
print("=" * 60)
