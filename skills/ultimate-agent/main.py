"""
硅基世界 2 - 主入口

整合所有代理功能，提供统一的命令行接口
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

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
from notification_agent import NotificationAgent, NotificationChannel, NotificationPriority
from report_generator import ReportGenerator, ReportFormat
from api_integration import ApiIntegration, setup_default_apis
from task_queue import TaskQueue, TaskPriority, create_task
from config_manager import ConfigManager, SYSTEM_SCHEMAS
from subagent_manager import SubagentManager
from workflow_engine import WorkflowEngine
from business_roles.product_manager import ProductManagerAgent
from business_roles.ui_designer import UIDesignerAgent
from business_roles.architect import ArchitectAgent
from business_roles.senior_dev import SeniorDevAgent

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
        
        # Phase 5 组件 (新增)
        self.notifier = NotificationAgent(agents_dir.parent / "notifications")
        self.reporter = ReportGenerator(agents_dir.parent / "reports")
        self.api_integration = ApiIntegration(agents_dir.parent / "api-configs")
        self.task_queue = TaskQueue(max_concurrent=5, persist_dir=agents_dir.parent / "task-queue")
        self.config_manager = ConfigManager(agents_dir.parent / "configs")
        
        # Phase 7: 子代理管理
        self.subagent_manager = SubagentManager(agents_dir.parent / "configs" / "config.json")
        
        # Phase 8: 业务代理
        self.workflow_engine = WorkflowEngine(agents_dir.parent / "configs" / "workflows.json")
        self.product_manager = ProductManagerAgent()
        self.ui_designer = UIDesignerAgent()
        self.architect = ArchitectAgent()
        self.senior_dev = SeniorDevAgent()
        
        # 设置默认 API
        setup_default_apis(self.api_integration)
        
        # 注册系统配置模式
        self.config_manager.register_schemas(SYSTEM_SCHEMAS)
        
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
    
    # ========== Phase 5: 通知和报告 ==========
    
    def send_notification(
        self,
        title: str,
        message: str,
        channel: str = "console",
        priority: str = "normal"
    ) -> dict:
        """
        发送通知
        
        Args:
            title: 标题
            message: 消息内容
            channel: 渠道 (console/system/webhook/email/all)
            priority: 优先级 (low/normal/high/urgent)
            
        Returns:
            发送结果
        """
        try:
            ch = NotificationChannel(channel)
            prio = NotificationPriority(priority)
            success = self.notifier.send(title, message, ch, prio)
            return {
                'success': success,
                'title': title,
                'channel': channel,
                'priority': priority
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_notification_stats(self) -> dict:
        """获取通知统计"""
        return self.notifier.get_stats()
    
    def generate_report(
        self,
        title: str,
        sections: list,
        format: str = "markdown",
        filename: str = None
    ) -> dict:
        """
        生成报告
        
        Args:
            title: 报告标题
            sections: 章节列表 [{'title': ..., 'content': ..., 'level': 2}]
            format: 格式 (markdown/html/pdf/json/text)
            filename: 文件名
            
        Returns:
            生成结果
        """
        try:
            from report_generator import Report, ReportSection
            
            report = Report(
                title=title,
                sections=[
                    ReportSection(
                        title=s.get('title', 'Untitled'),
                        content=s.get('content', ''),
                        level=s.get('level', 2)
                    )
                    for s in sections
                ]
            )
            
            fmt = ReportFormat(format)
            filepath = self.reporter.generate(report, fmt, filename)
            
            return {
                'success': True,
                'filepath': str(filepath),
                'format': format
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_research_report(
        self,
        topic: str,
        summary: str = "",
        format: str = "markdown"
    ) -> dict:
        """
        生成研究报告
        
        Args:
            topic: 研究主题
            summary: 摘要
            format: 格式
            
        Returns:
            生成结果
        """
        try:
            # 使用研究员获取研究发现
            research_result = self.researcher.research(topic, count=5)
            
            # 创建报告
            report = self.reporter.create_research_report(
                topic=topic,
                findings=[],  # 简化处理
                summary=summary or f"关于 {topic} 的研究报告"
            )
            
            fmt = ReportFormat(format)
            filepath = self.reporter.generate(report, fmt)
            
            return {
                'success': True,
                'filepath': str(filepath),
                'topic': topic
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_reports(self) -> dict:
        """列出所有报告"""
        reports = self.reporter.list_reports()
        return {
            'count': len(reports),
            'reports': [
                {
                    'filename': p.name,
                    'size': p.stat().st_size,
                    'modified': datetime.fromtimestamp(p.stat().st_mtime).isoformat()
                }
                for p in reports[:20]  # 限制返回 20 个
            ]
        }
    
    # ========== 子代理管理 ==========
    
    def spawn_subagent(
        self,
        task: str,
        runtime: str = "subagent",
        agent_id: Optional[str] = None,
        mode: str = "session",
        thread: bool = False,
        timeout_seconds: Optional[int] = None,
        label: Optional[str] = None
    ) -> dict:
        """
        生成子代理
        
        Args:
            task: 任务描述
            runtime: 运行时类型 (subagent/acp)
            agent_id: 代理 ID（可选，自动选择）
            mode: 模式 (run/session)
            thread: 是否绑定线程（仅 ACP + Discord）
            timeout_seconds: 超时时间（秒）
            label: 会话标签
            
        Returns:
            子代理配置信息
        """
        try:
            config = self.subagent_manager.create_subagent(
                task=task,
                runtime=runtime,
                agent_id=agent_id,
                mode=mode,
                thread=thread,
                timeout_seconds=timeout_seconds,
                label=label
            )
            
            return {
                'success': True,
                'subagent_id': config.id,
                'name': config.name,
                'agent_id': config.agent_id,
                'runtime': config.runtime.value,
                'mode': config.mode.value,
                'task': config.task,
                'created_at': config.created_at
            }
        except ValueError as e:
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'创建失败：{str(e)}'
            }
    
    def execute_subagent(self, subagent_id: str) -> dict:
        """
        执行子代理
        
        Args:
            subagent_id: 子代理 ID
            
        Returns:
            执行结果
        """
        result = self.subagent_manager.execute_subagent(subagent_id)
        return result
    
    def list_subagents(self, active_only: bool = False) -> dict:
        """
        列出子代理
        
        Args:
            active_only: 是否只列出活跃的
            
        Returns:
            子代理列表
        """
        subagents = self.subagent_manager.list_subagents(active_only)
        return {
            'count': len(subagents),
            'active_only': active_only,
            'subagents': subagents
        }
    
    def cleanup_subagents(self, older_than_hours: int = 24) -> dict:
        """清理已完成的子代理"""
        cleaned = self.subagent_manager.cleanup_completed(older_than_hours)
        return {
            'cleaned': cleaned,
            'older_than_hours': older_than_hours
        }
    
    # ========== Phase 8: 业务代理 ==========
    
    def generate_prd(self, requirement: str) -> dict:
        """使用产品经理生成 PRD"""
        result = self.product_manager.execute(requirement)
        return {
            'success': True,
            'project_name': result['project_name'],
            'prd_path': result['prd_path'],
            'message': result['message']
        }
    
    def generate_design(self, prd_path: str) -> dict:
        """使用 UI 设计师生成设计"""
        result = self.ui_designer.execute(prd_path)
        return {
            'success': True,
            'project_name': result['project_name'],
            'design_path': result['design_path'],
            'color_scheme': result['color_scheme'],
            'message': result['message']
        }
    
    def generate_architecture(self, prd_path: str) -> dict:
        """使用架构师生成技术方案"""
        result = self.architect.execute(prd_path)
        return {
            'success': True,
            'project_name': result['project_name'],
            'design_path': result['design_path'],
            'message': result['message']
        }
    
    def implement_code(self, tech_design_path: str, ui_design_path: str = None) -> dict:
        """使用开发工程师实现代码"""
        result = self.senior_dev.implement(tech_design_path, ui_design_path)
        return {
            'success': True,
            'code_path': result['code_path'],
            'message': result['message']
        }
    
    def full_workflow(self, requirement: str) -> dict:
        """完整软件开发流程"""
        # 1. PRD
        pm_result = self.generate_prd(requirement)
        
        # 2. 设计
        ui_result = self.generate_design(pm_result['prd_path'])
        
        # 3. 架构
        arch_result = self.generate_architecture(pm_result['prd_path'])
        
        # 4. 代码
        dev_result = self.implement_code(arch_result['design_path'], ui_result['design_path'])
        
        return {
            'success': True,
            'requirement': requirement,
            'prd_path': pm_result['prd_path'],
            'design_path': ui_result['design_path'],
            'architecture_path': arch_result['design_path'],
            'code_path': dev_result['code_path']
        }
    
    # ========== 系统状态 ==========
    
    def get_status(self) -> dict:
        """获取系统状态"""
        return {
            'system': '硅基世界 2',
            'version': '3.1.0',  # 升级到 3.1.0
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
                'orchestration': self.orchestration.get_system_stats(),
                # Phase 5
                'notification': self.notifier.get_stats(),
                'reporter': {
                    'output_dir': str(self.reporter.output_dir),
                    'reports_count': len(self.reporter.list_reports())
                },
                # Phase 7: Subagent
                'subagent': self.subagent_manager.get_statistics()
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
        
        # Phase 5: 通知和报告
        elif command == 'notify' and len(sys.argv) > 2:
            # 用法：notify <标题> <消息> [渠道] [优先级]
            title = sys.argv[2]
            message = sys.argv[3] if len(sys.argv) > 3 else "通知消息"
            channel = sys.argv[4] if len(sys.argv) > 4 else "console"
            priority = sys.argv[5] if len(sys.argv) > 5 else "normal"
            
            result = system.send_notification(title, message, channel, priority)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == 'notify-stats':
            result = system.get_notification_stats()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == 'report' and len(sys.argv) > 2:
            # 用法：report <标题> <格式> [文件名]
            title = sys.argv[2]
            format = sys.argv[3] if len(sys.argv) > 3 else "markdown"
            filename = sys.argv[4] if len(sys.argv) > 4 else None
            
            # 创建简单报告
            sections = [
                {'title': '简介', 'content': f'这是关于 {title} 的报告。', 'level': 2},
                {'title': '内容', 'content': '详细内容待补充。', 'level': 2},
                {'title': '总结', 'content': '报告完成。', 'level': 2}
            ]
            
            result = system.generate_report(title, sections, format, filename)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == 'research-report' and len(sys.argv) > 2:
            # 用法：research-report <主题> [格式]
            topic = sys.argv[2]
            format = sys.argv[3] if len(sys.argv) > 3 else "markdown"
            
            result = system.generate_research_report(topic, format=format)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == 'reports':
            result = system.list_reports()
            print(f"\n报告列表 ({result['count']} 个):\n")
            for r in result['reports']:
                print(f"  📄 {r['filename']} ({r['size']} bytes) - {r['modified'][:10]}")
            print()
        
        elif command == 'interactive':
            system.interactive_mode()
        
        elif command == 'webui':
            # 启动 Web UI
            host = sys.argv[2] if len(sys.argv) > 2 else '127.0.0.1'
            port = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
            debug = '--debug' in sys.argv
            
            print(f"\n🌐 启动 Web UI...")
            print(f"   地址：http://{host}:{port}")
            print(f"   调试：{'开启' if debug else '关闭'}")
            print(f"\n按 Ctrl+C 停止服务\n")
            
            from web_ui.app import run_dashboard
            run_dashboard(host=host, port=port, debug=debug, system_instance=system)
        
        # Phase 7: 子代理管理
        elif command == 'spawn':
            # 用法：spawn <任务描述> [--runtime subagent|acp] [--agent-id <id>] [--mode run|session] [--thread] [--timeout <秒>] [--label <标签>]
            import shlex
            
            task = None
            runtime = 'subagent'
            agent_id = None
            mode = 'session'
            thread = False
            timeout = None
            label = None
            
            # 解析命令行参数
            args = sys.argv[2:] if len(sys.argv) > 2 else []
            
            # 首先获取第一个参数作为任务描述
            if args and not args[0].startswith('--'):
                task = args[0]
                args = args[1:]
            
            # 解析选项参数
            i = 0
            while i < len(args):
                if args[i] == '--runtime' and i + 1 < len(args):
                    runtime = args[i + 1]
                    i += 2
                elif args[i] == '--agent-id' and i + 1 < len(args):
                    agent_id = args[i + 1]
                    i += 2
                elif args[i] == '--mode' and i + 1 < len(args):
                    mode = args[i + 1]
                    i += 2
                elif args[i] == '--thread':
                    thread = True
                    i += 1
                elif args[i] == '--timeout' and i + 1 < len(args):
                    timeout = int(args[i + 1])
                    i += 2
                elif args[i] == '--label' and i + 1 < len(args):
                    label = args[i + 1]
                    i += 2
                else:
                    i += 1
            
            if not task:
                print("用法：python main.py spawn <任务描述> [选项]")
                print("选项:")
                print("  --runtime subagent|acp  (默认：subagent)")
                print("  --agent-id <代理 ID>     (可选，自动选择)")
                print("  --mode run|session      (默认：session)")
                print("  --thread                (仅 ACP + Discord)")
                print("  --timeout <秒>          (超时时间)")
                print("  --label <标签>          (会话标签)")
            else:
                result = system.spawn_subagent(
                    task=task,
                    runtime=runtime,
                    agent_id=agent_id,
                    mode=mode,
                    thread=thread,
                    timeout_seconds=timeout,
                    label=label
                )
                print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == 'subagents':
            # 列出子代理
            active_only = '--active' in sys.argv
            json_output = '--json' in sys.argv
            
            result = system.list_subagents(active_only)
            
            if json_output:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"\n子代理列表 ({result['count']} 个):\n")
                if result['subagents']:
                    print(f"{'ID':<30} {'名称':<20} {'状态':<12} {'代理':<15} {'运行时':<10}")
                    print("-" * 90)
                    for sa in result['subagents'][:20]:  # 限制显示 20 个
                        print(f"{sa['id']:<30} {sa['name']:<20} {sa['status']:<12} {sa['agent_id']:<15} {sa['runtime']:<10}")
                else:
                    print("  没有子代理")
                print()
        
        elif command == 'execute-subagent' and len(sys.argv) > 2:
            # 执行子代理
            subagent_id = sys.argv[2]
            result = system.execute_subagent(subagent_id)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == 'cleanup-subagents':
            hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
            result = system.cleanup_subagents(older_than_hours=hours)
            print(f"已清理 {result['cleaned']} 个超过 {result['older_than_hours']} 小时的已完成子代理")
        
        # Phase 8: 业务代理
        elif command == 'prd' and len(sys.argv) > 2:
            # 生成 PRD
            requirement = ' '.join(sys.argv[2:])
            result = system.generate_prd(requirement)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == 'design' and len(sys.argv) > 2:
            # 生成设计
            prd_path = sys.argv[2]
            result = system.generate_design(prd_path)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == 'architecture' and len(sys.argv) > 2:
            # 生成架构
            prd_path = sys.argv[2]
            result = system.generate_architecture(prd_path)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == 'code' and len(sys.argv) > 2:
            # 生成代码
            tech_path = sys.argv[2]
            ui_path = sys.argv[3] if len(sys.argv) > 3 else None
            result = system.implement_code(tech_path, ui_path)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == 'full-dev' and len(sys.argv) > 2:
            # 完整开发流程
            requirement = ' '.join(sys.argv[2:])
            result = system.full_workflow(requirement)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        else:
            print("用法:")
            print("  python main.py task <任务描述>")
            print("  python main.py research <研究主题>")
            print("  python main.py status")
            print("  python main.py heartbeat")
            print("  python main.py improvements")
            print("  python main.py exec-tasks [数量]")
            print("  python main.py notify <标题> <消息> [渠道] [优先级]")
            print("  python main.py notify-stats")
            print("  python main.py report <标题> <格式> [文件名]")
            print("  python main.py research-report <主题> [格式]")
            print("  python main.py reports")
            print("  python main.py interactive")
            print("  python main.py webui [主机] [端口] [--debug]  # 启动 Web UI")
            print("")
            print("子代理管理 (Phase 7):")
            print("  python main.py spawn <任务描述> [--runtime subagent|acp] [--agent-id <id>] [--mode run|session] [--thread] [--timeout <秒>] [--label <标签>]")
            print("  python main.py subagents [--active] [--json]")
            print("  python main.py execute-subagent <子代理 ID>")
            print("  python main.py cleanup-subagents [小时数]")
            print("")
            print("业务代理 (Phase 8):")
            print("  python main.py prd <需求描述>              # 生成 PRD")
            print("  python main.py design <PRD 路径>            # 生成 UI 设计")
            print("  python main.py architecture <PRD 路径>      # 生成技术方案")
            print("  python main.py code <技术路径> [UI 路径]     # 生成代码")
            print("  python main.py full-dev <需求描述>          # 完整开发流程")
    else:
        # 默认交互模式
        system.interactive_mode()


if __name__ == '__main__':
    main()
