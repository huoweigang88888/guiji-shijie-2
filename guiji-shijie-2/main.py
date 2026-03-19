#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
硅基世界 2 (Guiji World 2) - 主入口
多 AI 代理协作应用平台
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# 项目根目录
PROJECT_ROOT = Path(__file__).parent
CONFIGS_DIR = PROJECT_ROOT / "configs"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
LOGS_DIR = PROJECT_ROOT / "logs"
MEMORY_DIR = PROJECT_ROOT / "memory"
TASKS_DIR = PROJECT_ROOT / "tasks"

def load_config():
    """加载配置文件"""
    config_path = CONFIGS_DIR / "agent_config.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_config(config):
    """保存配置文件"""
    CONFIGS_DIR.mkdir(parents=True, exist_ok=True)
    config_path = CONFIGS_DIR / "agent_config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def print_banner():
    """打印欢迎横幅"""
    print("=" * 60)
    print("[Guiji World 2] 硅基世界 2")
    print("   多 AI 代理协作应用平台")
    print("=" * 60)
    print()

def cmd_status():
    """显示系统状态"""
    print("[STATUS] 系统状态")
    print("-" * 40)
    
    # 检查目录
    dirs = {
        "agents": AGENTS_DIR.exists(),
        "configs": CONFIGS_DIR.exists(),
        "outputs": OUTPUTS_DIR.exists(),
        "logs": LOGS_DIR.exists(),
        "memory": MEMORY_DIR.exists(),
        "tasks": TASKS_DIR.exists(),
    }
    
    for name, exists in dirs.items():
        status = "[OK]" if exists else "[--]"
        print(f"  {status} {name}")
    
    # 加载配置
    config = load_config()
    if config:
        print(f"\n[CONFIG] 已加载配置项：{len(config)}")
    else:
        print("\n[WARN] 暂无配置文件")
    
    # 检查代理文件
    if AGENTS_DIR.exists():
        agent_files = list(AGENTS_DIR.glob("*.py"))
        print(f"\n[AGENTS] 可用代理模块：{len(agent_files)}")
        for f in agent_files:
            if f.name != "__init__.py":
                print(f"   - {f.stem}")
    
    print()

def cmd_run(task=None):
    """运行任务"""
    print("[RUN] 执行任务")
    print("-" * 40)
    
    if not task:
        print("[WARN] 请提供任务描述")
        print("用法：python main.py run <任务描述>")
        return
    
    print(f"任务：{task}")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 这里可以集成 ultimate-agent 的协调器
    # 目前作为示例，输出任务信息
    print("[OK] 任务已接收，正在协调代理执行...")
    print("   (需要配置 ultimate-agent 集成)")
    
    # 保存任务记录
    task_record = {
        "task": task,
        "timestamp": datetime.now().isoformat(),
        "status": "pending"
    }
    
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    task_file = TASKS_DIR / f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(task_file, 'w', encoding='utf-8') as f:
        json.dump(task_record, f, ensure_ascii=False, indent=2)
    
    print(f"\n[SAVE] 任务已保存到：{task_file}")
    print()

def cmd_interactive():
    """交互式模式"""
    print("[INTERACTIVE] 进入交互模式")
    print("-" * 40)
    print("输入任务描述，或输入 'quit' 退出")
    print()
    
    while True:
        try:
            task = input("[TASK] > ").strip()
            if task.lower() in ['quit', 'exit', 'q']:
                print("[BYE] 再见！")
                break
            if task:
                cmd_run(task)
        except (EOFError, KeyboardInterrupt):
            print("\n[BYE] 再见！")
            break

def cmd_create_agent(name):
    """创建新代理"""
    print(f"[CREATE] 创建代理：{name}")
    print("-" * 40)
    
    if not name:
        print("[WARN] 请提供代理名称")
        print("用法：python main.py create-agent <代理名称>")
        return
    
    # 创建代理文件模板
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    agent_file = AGENTS_DIR / f"{name}.py"
    
    if agent_file.exists():
        print(f"[WARN] 代理已存在：{name}")
        return
    
    template = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{name.replace("-", " ").title()} Agent
自动生成的代理模块
"""

from pathlib import Path

class {name.replace("-", "_").title().replace("_", "")}Agent:
    """{name.replace("-", " ").title()} 代理"""
    
    def __init__(self, config=None):
        self.config = config or {{}}
        self.name = "{name}"
    
    def execute(self, task, **kwargs):
        """执行任务"""
        print(f"[{{self.name}}] 执行任务：{{task}}")
        # TODO: 实现具体逻辑
        return {{"status": "success", "result": None}}
    
    def get_capabilities(self):
        """获取代理能力列表"""
        return [
            "能力 1",
            "能力 2",
        ]

if __name__ == "__main__":
    agent = {name.replace("-", "_").title().replace("_", "")}Agent()
    print(f"代理：{{agent.name}}")
    print(f"能力：{{agent.get_capabilities()}}")
'''
    
    with open(agent_file, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"[OK] 代理已创建：{agent_file}")
    print()

def cmd_help():
    """显示帮助信息"""
    print("📖 使用帮助")
    print("-" * 40)
    print()
    print("用法：python main.py <命令> [参数]")
    print()
    print("可用命令:")
    print("  status              显示系统状态")
    print("  run <任务>          执行任务")
    print("  interactive         交互模式")
    print("  create-agent <名称> 创建新代理")
    print("  help                显示此帮助")
    print()

def main():
    """主函数"""
    global AGENTS_DIR
    AGENTS_DIR = PROJECT_ROOT / "agents"
    
    print_banner()
    
    if len(sys.argv) < 2:
        cmd_help()
        return
    
    cmd = sys.argv[1]
    
    if cmd == "status":
        cmd_status()
    elif cmd == "run":
        task = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
        cmd_run(task)
    elif cmd == "interactive":
        cmd_interactive()
    elif cmd == "create-agent":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_create_agent(name)
    elif cmd == "help":
        cmd_help()
    else:
        print(f"❌ 未知命令：{cmd}")
        print("使用 'python main.py help' 查看帮助")

if __name__ == "__main__":
    main()
