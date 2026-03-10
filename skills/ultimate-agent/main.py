"""
硅基世界 2 - 主入口

整合所有代理功能，提供统一的命令行接口
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime

# Windows 编码支持
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 添加 agents 目录到路径
agents_dir = Path(__file__).parent / "agents"
sys.path.insert(0, str(agents_dir))

from coordinator import AgentCoordinator
from researcher import ResearchAssistant
from message_aggregator import MessageAggregator, MessagePlatform
from heartbeat import HeartbeatSystem
from auto_executor import AutoExecutor
from self_improver import SelfImprover
from vector_search import VectorSearch
from knowledge_graph import KnowledgeGraph, RelationType
from agent_communication import AgentCommunication, Performative
from agent_orchestration import AgentOrchestration
from enhanced_researcher import EnhancedResearcher
from enhanced_executor import EnhancedExecutor, TaskType
from analyst_agent import AnalystAgent
from scheduler import Scheduler, TaskFrequency
from system_monitor import SystemMonitor
from workflow_persistence import WorkflowPersistence

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
        
        # Phase 1 组件
        self.coordinator = AgentCoordinator(agents_dir)
        self.researcher = ResearchAssistant()
        self.messenger = MessageAggregator(agents_dir)
        
        # Phase 2 组件
        self.heartbeat = HeartbeatSystem(agents_dir.parent)
        self.executor = AutoExecutor(agents_dir.parent)
        self.improver = SelfImprover(agents_dir.parent)
        
        # Phase 3 组件
        self.vector_search = VectorSearch(agents_dir.parent / "vector-db")
        self.knowledge_graph = KnowledgeGraph(agents_dir.parent)
        
        # Phase 4 组件
        self.agent_comm = AgentCommunication(agents_dir)
        self.orchestration = AgentOrchestration(self.agent_comm)
        
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
    
    def run_heartbeat(self) -> dict:
        """
        运行心跳检查
        
        Returns:
            心跳报告
        """
        logger.info("运行心跳检查...")
        report = self.heartbeat.run_check()
        return {
            'summary': report.summary,
            'issues_found': report.issues_found,
            'checks_performed': report.checks_performed,
            'recommended_actions': report.recommended_actions
        }
    
    def add_goal(self, title: str, description: str, tasks: list = None) -> dict:
        """
        添加目标
        
        Args:
            title: 目标标题
            description: 目标描述
            tasks: 任务列表
            
        Returns:
            目标信息
        """
        goal = self.executor.add_goal(title, description)
        
        if tasks:
            self.executor.generate_tasks(goal.id, tasks)
        
        return {
            'goal_id': goal.id,
            'title': goal.title,
            'status': goal.status
        }
    
    def execute_tasks(self, limit: int = None) -> dict:
        """
        执行待处理任务
        
        Returns:
            执行结果
        """
        return self.executor.execute_pending_tasks(limit)
    
    def get_improvements(self) -> dict:
        """
        获取改进建议
        
        Returns:
            改进建议列表
        """
        improvements = self.improver.get_high_priority_improvements()
        return {
            'count': len(improvements),
            'improvements': [imp.to_dict() for imp in improvements[:5]]
        }
    
    def create_workflow(self, name: str, description: str, tasks: list = None) -> dict:
        """
        创建工作流
        
        Returns:
            工作流信息
        """
        workflow = self.orchestration.create_workflow(name, description)
        
        if tasks:
            self.orchestration.decompose_task(workflow, description, tasks)
        
        return {
            'workflow_id': workflow.id,
            'name': workflow.name,
            'state': workflow.state.value
        }
    
    def execute_workflow(self, workflow_id: str) -> dict:
        """
        执行工作流
        
        Returns:
            执行结果
        """
        return self.orchestration.execute_workflow(workflow_id)
    
    def agent_comm_send(self, sender: str, receiver: str, performative: str, content: str) -> dict:
        """
        发送代理间消息
        
        Returns:
            发送结果
        """
        try:
            perf = Performative(performative)
            msg = self.agent_comm.send_message(sender, [receiver], perf, content)
            return {
                'success': True,
                'message_id': msg.message_id,
                'conversation_id': msg.conversation_id
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def vector_add(self, content: str, doc_type: str = "general", metadata: dict = None) -> dict:
        """
        添加文档到向量库
        
        Returns:
            添加结果
        """
        table_name = f"{doc_type}s"
        doc_id = self.vector_search.add_document(table_name, content, metadata or {})
        return {
            'success': doc_id is not None,
            'doc_id': doc_id,
            'table': table_name
        }
    
    def vector_search_query(self, query: str, doc_type: str = "general", limit: int = 5) -> dict:
        """
        向量搜索
        
        Returns:
            搜索结果
        """
        table_name = f"{doc_type}s"
        results = self.vector_search.search(table_name, query, limit=limit)
        return {
            'query': query,
            'count': len(results),
            'results': results
        }
    
    def graph_add_node(self, title: str, description: str, category: str = "general", tags: str = "") -> dict:
        """
        添加知识节点
        
        Returns:
            添加结果
        """
        tag_list = [t.strip() for t in tags.split(',') if t.strip()] if tags else []
        node_id = self.knowledge_graph.add_node(title, description, category, tag_list)
        return {
            'success': True,
            'node_id': node_id,
            'title': title
        }
    
    def graph_add_relation(self, from_node: str, to_node: str, rel_type: str, description: str = "") -> dict:
        """
        添加知识关系
        
        Returns:
            添加结果
        """
        try:
            relation_type = RelationType(rel_type)
            rel_id = self.knowledge_graph.add_relation(from_node, to_node, relation_type, description)
            return {
                'success': rel_id is not None,
                'relation_id': rel_id
            }
        except ValueError:
            return {
                'success': False,
                'error': f'Invalid relation type: {rel_type}'
            }
    
    def graph_search(self, query: str, category: str = "", limit: int = 5) -> dict:
        """
        搜索知识节点
        
        Returns:
            搜索结果
        """
        results = self.knowledge_graph.search_nodes(query, category if category else None, limit=limit)
        return {
            'count': len(results),
            'results': [
                {'id': n.id, 'title': n.title, 'description': n.description, 'category': n.category}
                for n in results
            ]
        }
    
    def get_status(self) -> dict:
        """获取系统状态"""
        return {
            'system': '硅基世界 2',
            'version': '3.0.0',
            'timestamp': datetime.now().isoformat(),
            'components': {
                # Phase 1
                'coordinator': self.coordinator.get_status(),
                'researcher': self.researcher.get_status(),
                'messenger': self.messenger.get_status(),
                # Phase 2
                'heartbeat': {
                    'last_check': self.heartbeat.last_check,
                    'status': 'active'
                },
                'executor': self.executor.get_progress(),
                'improver': {
                    'errors': len(self.improver.errors),
                    'lessons': len(self.improver.lessons),
                    'improvements': len(self.improver.improvements)
                },
                # Phase 3
                'vector_search': self.vector_search.get_stats(),
                'knowledge_graph': self.knowledge_graph.get_stats(),
                # Phase 4
                'agent_communication': self.agent_comm.get_system_stats(),
                'orchestration': self.orchestration.get_system_stats()
            }
        }
    
    def interactive_mode(self):
        """交互模式"""
        print("\n" + "="*60)
        print("🤖 硅基世界 2 - AI 代理系统 (Phase 2)")
        print("="*60)
        print("\n可用命令:")
        print("  Phase 1 - 核心功能")
        print("    task <描述>              - 执行任务")
        print("    research <主题>          - 研究主题")
        print("    send <平台> <接收者> <内容> - 发送消息")
        print("")
        print("  Phase 2 - 自动化系统")
        print("    heartbeat                - 运行心跳检查")
        print("    goal <标题> <描述>       - 添加目标")
        print("    exec-tasks [数量]        - 执行待处理任务")
        print("    improvements             - 查看改进建议")
        print("")
        print("  Phase 3 - 增强功能")
        print("    v-add <类型> <内容>      - 添加向量文档")
        print("    v-search <类型> <查询>   - 向量搜索")
        print("    g-add <标题> <描述> [类别] [标签] - 添加知识节点")
        print("    g-rel <从节点> <到节点> <关系类型> - 添加关系")
        print("    g-search <查询>          - 搜索知识节点")
        print("")
        print("  通用")
        print("    status                   - 显示系统状态")
        print("    help                     - 显示帮助")
        print("    quit                     - 退出")
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
                    print("  Phase 1 - 核心功能")
                    print("    task <描述>              - 执行任务")
                    print("    research <主题>          - 研究主题")
                    print("    send <平台> <接收者> <内容> - 发送消息")
                    print("")
                    print("  Phase 2 - 自动化系统")
                    print("    heartbeat                - 运行心跳检查")
                    print("    goal <标题> <描述>       - 添加目标")
                    print("    exec-tasks [数量]        - 执行待处理任务")
                    print("    improvements             - 查看改进建议")
                    print("")
                    print("  Phase 3 - 增强功能")
                    print("    v-add <类型> <内容>      - 添加向量文档")
                    print("    v-search <类型> <查询>   - 向量搜索")
                    print("    g-add <标题> <描述> [类别] [标签] - 添加知识节点")
                    print("    g-rel <从节点> <到节点> <关系类型> - 添加关系")
                    print("    g-search <查询>          - 搜索知识节点")
                    print("")
                    print("  通用")
                    print("    status                   - 显示系统状态")
                    print("    help                     - 显示帮助")
                    print("    quit                     - 退出\n")
                    continue
                
                if user_input.lower() == 'status':
                    status = self.get_status()
                    print(json.dumps(status, indent=2, ensure_ascii=False))
                    continue
                
                if user_input.lower() == 'heartbeat':
                    result = self.run_heartbeat()
                    print(f"\n{result['summary']}")
                    if result['recommended_actions']:
                        print("\n建议行动:")
                        for action in result['recommended_actions']:
                            print(f"  - [{action['severity']}] {action['action']}")
                    print()
                    continue
                
                if user_input.lower() == 'improvements':
                    result = self.get_improvements()
                    if result['count'] == 0:
                        print("\n暂无改进建议 ✅\n")
                    else:
                        print(f"\n发现 {result['count']} 个改进建议:")
                        for imp in result['improvements']:
                            print(f"  - {imp['title']} (价值:{imp['estimated_value']}/努力:{imp['estimated_effort']})")
                    print()
                    continue
                
                if user_input.lower().startswith('exec-tasks'):
                    parts = user_input.split()
                    limit = int(parts[1]) if len(parts) > 1 else None
                    result = self.execute_tasks(limit)
                    print(f"\n执行完成：{result['completed']}/{result['total']}")
                    if result['failed'] > 0:
                        print(f"失败：{result['failed']}")
                    print()
                    continue
                
                if user_input.lower().startswith('v-add '):
                    parts = user_input[6:].strip().split(' ', 1)
                    if len(parts) >= 2:
                        doc_type, content = parts
                        result = self.vector_add(content, doc_type)
                        if result['success']:
                            print(f"\n文档已添加：{result['table']}/{result['doc_id']}\n")
                        else:
                            print("\n添加失败\n")
                    else:
                        print("用法：v-add <类型> <内容>\n")
                    continue
                
                if user_input.lower().startswith('v-search '):
                    parts = user_input[9:].strip().split(' ', 1)
                    if len(parts) >= 2:
                        doc_type, query = parts
                        result = self.vector_search_query(query, doc_type)
                        print(f"\n搜索结果 ({result['count']} 条):")
                        for i, r in enumerate(result['results'], 1):
                            print(f"  {i}. [{r.get('score', 0):.2f}] {r.get('content', '')[:80]}...")
                        print()
                    else:
                        print("用法：v-search <类型> <查询>\n")
                    continue
                
                if user_input.lower().startswith('g-add '):
                    parts = user_input[6:].strip().split(' ', 2)
                    if len(parts) >= 2:
                        title = parts[0]
                        rest = parts[1].split(' ', 1)
                        description = rest[0]
                        category_tags = rest[1].split(' ', 1) if len(rest) > 1 else ['', '']
                        category = category_tags[0] if category_tags else 'general'
                        tags = category_tags[1] if len(category_tags) > 1 else ''
                        result = self.graph_add_node(title, description, category, tags)
                        if result['success']:
                            print(f"\n节点已添加：{result['title']} (ID: {result['node_id']})\n")
                        else:
                            print("\n添加失败\n")
                    else:
                        print("用法：g-add <标题> <描述> [类别] [标签]\n")
                    continue
                
                if user_input.lower().startswith('g-search '):
                    query = user_input[9:].strip()
                    if query:
                        result = self.graph_search(query)
                        print(f"\n搜索结果 ({result['count']} 条):")
                        for i, r in enumerate(result['results'], 1):
                            print(f"  {i}. {r['title']} [{r['category']}]")
                            print(f"      {r['description'][:60]}...")
                        print()
                    else:
                        print("用法：g-search <查询>\n")
                    continue
                
                if user_input.lower().startswith('goal '):
                    parts = user_input[5:].strip().split(' ', 1)
                    if len(parts) >= 2:
                        title, description = parts
                        result = self.add_goal(title, description)
                        print(f"\n目标已创建：{result['title']} (ID: {result['goal_id']})\n")
                    else:
                        print("用法：goal <标题> <描述>\n")
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
        
        elif command == 'heartbeat':
            result = system.run_heartbeat()
            print(f"\n{result['summary']}\n")
            if result['recommended_actions']:
                print("建议行动:")
                for action in result['recommended_actions']:
                    print(f"  - [{action['severity']}] {action['action']}")
        
        elif command == 'improvements':
            result = system.get_improvements()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == 'exec-tasks':
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
            result = system.execute_tasks(limit)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == 'interactive':
            system.interactive_mode()
        
        else:
            print("用法:")
            print("  python main.py task <任务描述>")
            print("  python main.py research <研究主题>")
            print("  python main.py status")
            print("  python main.py heartbeat")
            print("  python main.py improvements")
            print("  python main.py exec-tasks [数量]")
            print("  python main.py interactive")
    else:
        # 默认交互模式
        system.interactive_mode()


if __name__ == '__main__':
    main()
