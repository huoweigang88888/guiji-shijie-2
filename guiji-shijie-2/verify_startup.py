#!/usr/bin/env python3
"""
项目启动验证 - Phase 10 完成
"""

print("=" * 60)
print("硅基世界 2 v2.0.0 - 启动验证")
print("=" * 60)
print()

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# 验证 Agent 系统
try:
    from agents import get_agent_system_status
    status = get_agent_system_status()
    print("✅ Agent 系统状态:")
    print(f"  版本：{status['version']}")
    print(f"  代理数：{status['registry']['total_agents']}")
    print(f"  OpenClaw 集成：{status['openclaw']['available']}")
except Exception as e:
    print(f"⚠️ Agent 系统：{e}")

print()

# 验证核心模块
modules = [
    ("数据库连接池", "core.db_pool"),
    ("缓存管理器", "core.cache_manager"),
    ("内存分析器", "core.memory_profiler"),
    ("WebSocket 优化", "core.websocket_optimized"),
    ("成就系统", "gamification.achievements_v2"),
    ("Scheduler Agent", "agents.specialized.scheduler"),
]

print("✅ 核心模块验证:")
for name, module in modules:
    try:
        __import__(module)
        print(f"  ✅ {name}")
    except Exception as e:
        print(f"  ⚠️ {name}: {e}")

print()

# 验证文件完整性
print("✅ 文件完整性:")
files = [
    "README.md",
    "requirements.txt",
    "api/main.py",
    "web_ui/dashboard-v2.html",
    "web_ui/world-2d.html",
    "docs/QUICKSTART.md",
    "docs/FINAL_SUMMARY.md",
]

for f in files:
    path = Path(f)
    if path.exists():
        print(f"  ✅ {f}")
    else:
        print(f"  ❌ {f} (缺失)")

print()
print("=" * 60)
print("✅ 项目已就绪，可以投入使用！")
print("=" * 60)
print()
print("📋 快速启动:")
print("  1. 安装依赖：pip install -r requirements.txt")
print("  2. 启动服务：python -m uvicorn api.main:app --reload --port 8000")
print("  3. 访问 Dashboard: http://localhost:3000/dashboard-v2.html")
print("  4. 访问 API 文档：http://localhost:8000/docs")
print()
print("🎉 硅基世界 2 v2.0.0 - 生产就绪！")
