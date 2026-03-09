"""
硅基世界 2 - 主入口

整合所有代理功能，提供统一的命令行接口
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime

# 添加 agents 目录到路径
agents_dir = Path(__file__).parent / "agents"
sys.path.insert(0, str(agents_dir))

from coordinator import AgentCoordinator
from researcher import ResearchAssistant
from message_aggregator import MessageAggregator, MessagePlatform

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('guiji-world-2')


class GuijiWorld2:
    """
    硅基世界 2 - 主系统
    
    整合所有代理功能，提供统一的入口
    """
    
    def __init__(self):
        """初始化系统"""
        logger.info("初始化硅基世界 2 系统...")
        
        self.coordinator = AgentCoordinator(agents_dir)
        self.researcher = ResearchAssistant()
        self.messenger = MessageAggregator(agents_dir)
        
        logger.info("系统初始化完成")
    
    def run_task(self, task: str) -> dict:
        """
        执行任务
        
        Args:
            task: 任务描述
            
        Returns:
            任务执行结果
        """
        logger.info(f"执行任务：{task}")
        return self.coordinator.execute_task(task)
    
    def research(self, topic: str, count: int = 5) -> str:
        """
        研究主题
        
        Args:
            topic: 研究主题
            count: 结果数量
            
        Returns:
            研究报告
        """
        logger.info(f"研究主题：{topic}")
        return self.researcher.research(topic, count=count)
    
    def send_message(self, platform: str, recipient: str, content: str) -> bool:
        """
        发送消息
        
        Args:
            platform: 平台名称 (whatsapp/telegram/slack)
            recipient: 接收者
            content: 消息内容
            
        Returns:
            发送是否成功
        """
        try:
            platform_enum = MessagePlatform(platform.lower())
            return self.messenger.send_message(content, platform_enum, recipient)
        except ValueError:
            logger.error(f"不支持的平台：{platform}")
            return False
    
    def get_status(self) -> dict:
        """获取系统状态"""
        return {
            'system': '硅基世界 2',
            'version': '1.0.0',
            'timestamp': datetime.now().isoformat(),
            'components': {
                'coordinator': self.coordinator.get_status(),
                'researcher': self.researcher.get_status(),
                'messenger': self.messenger.get_status()
            }
        }
    
    def interactive_mode(self):
        """交互模式"""
        print("\n" + "="*60)
        print("🤖 硅基世界 2 - AI 代理系统")
        print("="*60)
        print("\n可用命令:")
        print("  task <描述>     - 执行任务")
        print("  research <主题> - 研究主题")
        print("  send <平台> <接收者> <内容> - 发送消息")
        print("  status          - 显示系统状态")
        print("  help            - 显示帮助")
        print("  quit            - 退出")
        print("="*60 + "\n")
        
        while True:
            try:
                user_input = input(">>> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("再见！👋")
                    break
                
                if user_input.lower() == 'help':
                    print("\n可用命令:")
                    print("  task <描述>     - 执行任务")
                    print("  research <主题> - 研究主题")
                    print("  send <平台> <接收者> <内容> - 发送消息")
                    print("  status          - 显示系统状态")
                    print("  help            - 显示帮助")
                    print("  quit            - 退出\n")
                    continue
                
                if user_input.lower() == 'status':
                    status = self.get_status()
                    print(json.dumps(status, indent=2, ensure_ascii=False))
                    continue
                
                if user_input.lower().startswith('task '):
                    task = user_input[5:].strip()
                    result = self.run_task(task)
                    print(f"\n结果：{result.get('summary', '无结果')}\n")
                    continue
                
                if user_input.lower().startswith('research '):
                    topic = user_input[9:].strip()
                    report = self.research(topic)
                    print(f"\n{report}\n")
                    continue
                
                if user_input.lower().startswith('send '):
                    parts = user_input[5:].strip().split(' ', 2)
                    if len(parts) >= 3:
                        platform, recipient, content = parts
                        success = self.send_message(platform, recipient, content)
                        print(f"发送{'成功' if success else '失败'}\n")
                    else:
                        print("用法：send <平台> <接收者> <内容>\n")
                    continue
                
                print(f"未知命令：{user_input}\n")
                
            except KeyboardInterrupt:
                print("\n再见！👋")
                break
            except Exception as e:
                logger.error(f"错误：{e}")
                print(f"错误：{e}\n")


def main():
    """主函数"""
    system = GuijiWorld2()
    
    if len(sys.argv) > 1:
        # 命令行模式
        command = sys.argv[1]
        
        if command == 'task' and len(sys.argv) > 2:
            task = ' '.join(sys.argv[2:])
            result = system.run_task(task)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == 'research' and len(sys.argv) > 2:
            topic = ' '.join(sys.argv[2:])
            report = system.research(topic)
            print(report)
        
        elif command == 'status':
            status = system.get_status()
            print(json.dumps(status, indent=2, ensure_ascii=False))
        
        elif command == 'interactive':
            system.interactive_mode()
        
        else:
            print("用法:")
            print("  python main.py task <任务描述>")
            print("  python main.py research <研究主题>")
            print("  python main.py status")
            print("  python main.py interactive")
    else:
        # 默认交互模式
        system.interactive_mode()


if __name__ == '__main__':
    main()
