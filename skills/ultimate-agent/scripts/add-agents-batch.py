#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量添加 4 个新代理"""

import json
from pathlib import Path
import sys

# Windows 编码支持
if sys.platform == 'win32':
    sys.stdout = open(sys.stdout.fileno(), 'w', encoding='utf-8', buffering=1)

config_path = Path(__file__).parent.parent / "configs" / "company-agents.json"
workspaces_root = Path(__file__).parent.parent / "workspaces"

# 新代理列表
new_agents = [
    {
        "id": "agent-legal",
        "name": "法务顾问代理",
        "role": "Legal Advisor",
        "description": "合同审查、法律咨询、风险评估、合规检查",
        "capabilities": ["合同审查", "法律咨询", "风险评估", "合规检查", "知识产权保护"],
        "model": "bailian/qwen3.5-plus",
        "workspace": "workspaces/legal",
        "triggers": ["合同审查", "法律咨询", "合规问题", "法律纠纷"]
    },
    {
        "id": "agent-customer-service",
        "name": "客服专员代理",
        "role": "Customer Service",
        "description": "客户咨询、投诉处理、售后支持、满意度调查",
        "capabilities": ["客户咨询", "投诉处理", "售后支持", "满意度调查", "客户关系管理"],
        "model": "bailian/qwen3.5-plus",
        "workspace": "workspaces/customer-service",
        "triggers": ["客户咨询", "投诉", "售后", "退换货"]
    },
    {
        "id": "agent-procurement",
        "name": "采购专员代理",
        "role": "Procurement Specialist",
        "description": "供应商管理、采购谈判、订单跟踪、成本控制",
        "capabilities": ["供应商筛选", "价格谈判", "订单管理", "库存监控", "成本控制"],
        "model": "bailian/qwen3.5-plus",
        "workspace": "workspaces/procurement",
        "triggers": ["采购", "供应商", "订单", "进货"]
    },
    {
        "id": "agent-social-media",
        "name": "社交媒体经理代理",
        "role": "Social Media Manager",
        "description": "社交媒体运营、内容创作、粉丝互动、品牌推广",
        "capabilities": ["内容策划", "社交媒体运营", "粉丝互动", "数据分析", "危机公关"],
        "model": "bailian/qwen3.5-plus",
        "workspace": "workspaces/social-media",
        "triggers": ["社交媒体", "微博", "微信", "抖音", "小红书"]
    }
]

print("=" * 60)
print("🚀 批量添加新代理")
print("=" * 60)
print()

# 读取配置
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

print(f"📦 添加前代理数：{len(config['agents'])}")

# 添加新代理
existing_ids = [a['id'] for a in config['agents']]
added_count = 0

for agent in new_agents:
    if agent['id'] in existing_ids:
        print(f"  ⚠️  跳过已存在：{agent['id']}")
    else:
        config['agents'].append(agent)
        print(f"  ✅ 添加：{agent['name']} ({agent['id']})")
        added_count += 1

# 保存配置
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print()
print(f"📦 添加后代理数：{len(config['agents'])}")
print(f"✅ 新增代理：{added_count} 个")
print()

# 创建工作空间
print("📁 创建工作空间...")
for agent in new_agents:
    ws_name = agent['workspace'].replace('workspaces/', '')
    ws_path = workspaces_root / ws_name
    
    if not ws_path.exists():
        ws_path.mkdir(parents=True, exist_ok=True)
        
        # 创建 SESSION-STATE.md
        state_content = f"""# {agent['name']} - Session State

**Agent ID**: {agent['id']}  
**Role**: {agent['role']}  
**Status**: 🟢 Active  
**Initialized**: 2026-03-18

---

## Current Tasks
- [ ] 等待任务分配

## WAL Log (Write-Ahead Log)
*所有操作先写入 WAL，防止上下文丢失*

---

## Memory
*待记录*
"""
        state_file = ws_path / "SESSION-STATE.md"
        with open(state_file, 'w', encoding='utf-8') as f:
            f.write(state_content)
        
        print(f"  ✅ 创建：{ws_name}")
    else:
        print(f"  ℹ️  已存在：{ws_name}")

print()
print("=" * 60)
print("                    ✅ 批量添加完成！")
print("=" * 60)
print()
print("下一步:")
print("  1. 重启 Web UI 以查看新代理")
print("  2. 访问 http://127.0.0.1:18789/agents.html")
print()
