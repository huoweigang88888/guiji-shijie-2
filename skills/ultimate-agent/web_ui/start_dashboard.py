#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动 Web 仪表板

用法:
    python start_dashboard.py              # 默认端口 5000
    python start_dashboard.py --port 8080  # 自定义端口
    python start_dashboard.py --debug      # 调试模式
"""

import sys
import argparse
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import run_dashboard
from main import GuijiWorld2


def main():
    parser = argparse.ArgumentParser(description='启动硅基世界 2 Web 仪表板')
    parser.add_argument('--host', default='127.0.0.1', help='监听地址 (默认：127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000, help='端口号 (默认：5000)')
    parser.add_argument('--debug', action='store_true', help='调试模式')
    parser.add_argument('--no-system', action='store_true', help='不加载完整系统（仅测试 UI）')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🌍 硅基世界 2 Web Dashboard")
    print("=" * 60)
    print()
    
    system = None
    
    if not args.no_system:
        print("📦 正在初始化系统...")
        try:
            system = GuijiWorld2()
            print("✅ 系统初始化完成")
        except Exception as e:
            print(f"⚠️ 系统初始化失败：{e}")
            print("   将以测试模式启动（无后端数据）")
    else:
        print("ℹ️  测试模式：不加载后端系统")
    
    print()
    print(f"🌐 启动 Web 服务器...")
    print(f"   地址：http://{args.host}:{args.port}")
    print(f"   调试：{'开启' if args.debug else '关闭'}")
    print()
    print("按 Ctrl+C 停止服务器")
    print()
    
    run_dashboard(
        host=args.host,
        port=args.port,
        debug=args.debug,
        system_instance=system
    )


if __name__ == '__main__':
    main()
