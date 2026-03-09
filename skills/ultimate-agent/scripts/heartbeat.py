#!/usr/bin/env python3
"""
Ultimate System Heartbeat - 简化版
定期运行检查系统状态和代理需求
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

def run_heartbeat() -> Dict[str, Any]:
    """运行心跳检查"""
    workspace = Path(os.environ.get("OPENCLAW_WORKSPACE", "."))
    skill_dir = Path(__file__).parent.parent
    state_file = skill_dir / "memory" / "ultimate-state.json"
    agents_dir = skill_dir / "agents"
    
    # 加载状态
    if state_file.exists():
        with open(state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
    else:
        state = {"active_projects": [], "created_agents": []}
    
    # 检查代理状态
    agents_status = []
    if agents_dir.exists():
        for config_file in agents_dir.glob("*.json"):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                agents_status.append({
                    "name": config["name"],
                    "display_name": config["displayName"],
                    "status": config.get("status", "unknown"),
                    "description": config.get("description", "")
                })
    
    # 生成报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "active_projects": len(state.get("active_projects", [])),
        "created_agents": len(state.get("created_agents", [])),
        "agents": agents_status,
        "issues": []
    }
    
    # 检查问题
    for agent in agents_status:
        if agent["status"] == "needs_user_config":
            report["issues"].append({
                "type": "agent_pending",
                "agent": agent["name"],
                "message": f"{agent['display_name']} 需要用户配置"
            })
    
    # 保存心跳记录
    state["last_heartbeat"] = report
    state["last_updated"] = datetime.now().timestamp()
    
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    
    return report


def print_report(report: Dict[str, Any]):
    """打印心跳报告"""
    print("\n" + "="*60)
    print("💓 ULTIMATE SYSTEM HEARTBEAT")
    print("="*60)
    
    print(f"\n⏰ 时间：{report['timestamp']}")
    print(f"📁 活跃项目：{report['active_projects']}")
    print(f"🤖 已创建代理：{report['created_agents']}")
    
    print(f"\n📊 代理状态:")
    for agent in report['agents']:
        icon = "✅" if agent["status"] == "active" else "⏳" if agent["status"] == "pending_setup" else "⚠️" if agent["status"] == "needs_user_config" else "❓"
        print(f"   {icon} {agent['display_name']} ({agent['status']})")
    
    if report['issues']:
        print(f"\n⚠️ 注意事项 ({len(report['issues'])}个):")
        for issue in report['issues']:
            print(f"   • {issue['message']}")
    else:
        print(f"\n✅ 一切正常")
    
    print("\n" + "="*60)


def main():
    """主函数"""
    report = run_heartbeat()
    print_report(report)


if __name__ == "__main__":
    main()
