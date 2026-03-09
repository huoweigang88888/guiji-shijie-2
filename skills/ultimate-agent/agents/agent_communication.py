"""
Agent Communication - 多代理通信模块

实现代理间的消息传递、协议通信、协作机制
参考 FIPA ACL (Agent Communication Language) 标准
"""

import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import defaultdict

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('agent-communication')


class Performative(Enum):
    """言语行为类型 (FIPA ACL 风格)"""
    INFORM = "inform"  # 告知信息
    REQUEST = "request"  # 请求行动
    QUERY_IF = "query-if"  # 查询是否
    QUERY_REF = "query-ref"  # 查询引用
    PROPOSE = "propose"  # 提议
    ACCEPT_PROPOSAL = "accept-proposal"  # 接受提议
    REJECT_PROPOSAL = "reject-proposal"  # 拒绝提议
    CFP = "cfp"  # 征集提案
    AGREE = "agree"  # 同意
    REFUSE = "refuse"  # 拒绝
    FAILURE = "failure"  # 失败
    NOT_UNDERSTOOD = "not-understood"  # 不理解


class MessageStatus(Enum):
    """消息状态"""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    ACKNOWLEDGED = "acknowledged"
    FAILED = "failed"


@dataclass
class ACLMessage:
    """
    ACL 通信消息
    
    基于 FIPA ACL 标准
    """
    message_id: str
    sender: str
    receivers: List[str]
    performative: Performative
    content: Any
    conversation_id: str = ""
    reply_with: str = ""
    in_reply_to: str = ""
    ontology: str = ""
    language: str = "json"
    timestamp: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        if not self.conversation_id:
            self.conversation_id = self.message_id
        if isinstance(self.performative, str):
            self.performative = Performative(self.performative)
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['performative'] = self.performative.value
        return d
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ACLMessage':
        data['performative'] = Performative(data['performative'])
        return cls(**data)


@dataclass
class AgentCapability:
    """代理能力描述"""
    name: str
    description: str
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True


@dataclass
class AgentProfile:
    """代理档案"""
    agent_id: str
    agent_type: str
    capabilities: List[AgentCapability] = field(default_factory=list)
    status: str = "active"
    last_seen: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.last_seen:
            self.last_seen = datetime.now().isoformat()


class MessageQueue:
    """消息队列"""
    
    def __init__(self):
        self.queues: Dict[str, List[ACLMessage]] = defaultdict(list)
        self.processed_ids: Set[str] = set()
    
    def enqueue(self, message: ACLMessage) -> None:
        """添加消息到队列"""
        for receiver in message.receivers:
            if message.message_id not in self.processed_ids:
                self.queues[receiver].append(message)
    
    def dequeue(self, agent_id: str, limit: int = 10) -> List[ACLMessage]:
        """获取代理的消息"""
        messages = self.queues[agent_id][:limit]
        self.queues[agent_id] = self.queues[agent_id][limit:]
        for msg in messages:
            self.processed_ids.add(msg.message_id)
        return messages
    
    def pending_count(self, agent_id: str) -> int:
        """获取待处理消息数"""
        return len(self.queues[agent_id])


class AgentCommunication:
    """
    代理通信系统
    
    功能:
    - 消息路由和传递
    - 对话管理
    - 协议处理
    - 服务发现
    """
    
    def __init__(self, agents_dir: Optional[Path] = None):
        """
        初始化代理通信
        
        Args:
            agents_dir: 代理配置目录
        """
        if agents_dir is None:
            agents_dir = Path(__file__).parent
        
        self.agents_dir = agents_dir
        self.config_file = agents_dir / "agent-communication.json"
        
        # 消息队列
        self.message_queue = MessageQueue()
        
        # 代理注册表
        self.agents: Dict[str, AgentProfile] = {}
        
        # 对话历史
        self.conversations: Dict[str, List[ACLMessage]] = defaultdict(list)
        
        # 消息处理器
        self.handlers: Dict[Performative, Callable[[ACLMessage], Any]] = {}
        
        # 订阅关系
        self.subscriptions: Dict[str, Set[str]] = defaultdict(set)
        
        # 加载配置
        self._load_config()
    
    def _load_config(self) -> None:
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.info(f"已加载代理通信配置：{self.config_file}")
            except Exception as e:
                logger.error(f"加载配置失败：{e}")
    
    def _save_config(self) -> None:
        """保存配置文件"""
        def serialize_agent(profile: AgentProfile) -> Dict[str, Any]:
            d = {
                'agent_id': profile.agent_id,
                'agent_type': profile.agent_type,
                'status': profile.status,
                'last_seen': profile.last_seen,
                'metadata': profile.metadata,
                'capabilities': [
                    {
                        'name': c.name,
                        'description': c.description,
                        'input_schema': c.input_schema,
                        'output_schema': c.output_schema,
                        'enabled': c.enabled
                    }
                    for c in profile.capabilities
                ]
            }
            return d
        
        data = {
            'agents': {k: serialize_agent(v) for k, v in self.agents.items()},
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def register_agent(
        self,
        agent_id: str,
        agent_type: str,
        capabilities: Optional[List[Dict[str, Any]]] = None
    ) -> AgentProfile:
        """
        注册代理
        
        Args:
            agent_id: 代理 ID
            agent_type: 代理类型
            capabilities: 能力列表
            
        Returns:
            代理档案
        """
        caps = []
        if capabilities:
            for cap in capabilities:
                caps.append(AgentCapability(**cap))
        
        profile = AgentProfile(
            agent_id=agent_id,
            agent_type=agent_type,
            capabilities=caps
        )
        
        self.agents[agent_id] = profile
        self._save_config()
        
        logger.info(f"代理已注册：{agent_id} ({agent_type})")
        return profile
    
    def unregister_agent(self, agent_id: str) -> bool:
        """注销代理"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            self._save_config()
            logger.info(f"代理已注销：{agent_id}")
            return True
        return False
    
    def send_message(
        self,
        sender: str,
        receivers: List[str],
        performative: Performative,
        content: Any,
        conversation_id: Optional[str] = None,
        reply_with: Optional[str] = None,
        in_reply_to: Optional[str] = None
    ) -> ACLMessage:
        """
        发送消息
        
        Args:
            sender: 发送者 ID
            receivers: 接收者 ID 列表
            performative: 言语行为类型
            content: 消息内容
            conversation_id: 对话 ID
            reply_with: 回复标识
            in_reply_to: 回复的消息 ID
            
        Returns:
            发送的消息
        """
        message = ACLMessage(
            message_id=str(uuid.uuid4()),
            sender=sender,
            receivers=receivers,
            performative=performative,
            content=content,
            conversation_id=conversation_id or str(uuid.uuid4()),
            reply_with=reply_with or "",
            in_reply_to=in_reply_to or ""
        )
        
        # 添加到队列
        self.message_queue.enqueue(message)
        
        # 记录对话
        self.conversations[message.conversation_id].append(message)
        
        logger.info(f"消息已发送：{sender} -> {receivers} [{performative.value}]")
        return message
    
    def receive_messages(self, agent_id: str, limit: int = 10) -> List[ACLMessage]:
        """
        接收消息
        
        Args:
            agent_id: 代理 ID
            limit: 最大消息数
            
        Returns:
            消息列表
        """
        if agent_id not in self.agents:
            logger.warning(f"未知代理：{agent_id}")
            return []
        
        messages = self.message_queue.dequeue(agent_id, limit)
        
        # 更新代理最后活动时间
        if agent_id in self.agents:
            self.agents[agent_id].last_seen = datetime.now().isoformat()
        
        return messages
    
    def register_handler(
        self,
        performative: Performative,
        handler: Callable[[ACLMessage], Any]
    ) -> None:
        """
        注册消息处理器
        
        Args:
            performative: 言语行为类型
            handler: 处理函数
        """
        self.handlers[performative] = handler
        logger.info(f"已注册处理器：{performative.value}")
    
    def process_messages(self, agent_id: str) -> List[Any]:
        """
        处理代理消息
        
        Args:
            agent_id: 代理 ID
            
        Returns:
            处理结果列表
        """
        messages = self.receive_messages(agent_id)
        results = []
        
        for msg in messages:
            handler = self.handlers.get(msg.performative)
            if handler:
                try:
                    result = handler(msg)
                    results.append(result)
                except Exception as e:
                    logger.error(f"处理消息失败：{e}")
                    # 发送失败通知
                    self.send_message(
                        sender="system",
                        receivers=[msg.sender],
                        performative=Performative.FAILURE,
                        content={"error": str(e), "original_message_id": msg.message_id}
                    )
            else:
                logger.warning(f"未找到处理器：{msg.performative.value}")
        
        return results
    
    def subscribe(self, agent_id: str, topic: str) -> None:
        """
        订阅主题
        
        Args:
            agent_id: 代理 ID
            topic: 主题名称
        """
        self.subscriptions[topic].add(agent_id)
        logger.info(f"代理 {agent_id} 已订阅主题 {topic}")
    
    def unsubscribe(self, agent_id: str, topic: str) -> None:
        """取消订阅"""
        if topic in self.subscriptions and agent_id in self.subscriptions[topic]:
            self.subscriptions[topic].remove(agent_id)
            logger.info(f"代理 {agent_id} 已取消订阅主题 {topic}")
    
    def broadcast(
        self,
        sender: str,
        topic: str,
        content: Any,
        performative: Performative = Performative.INFORM
    ) -> int:
        """
        广播消息到主题订阅者
        
        Args:
            sender: 发送者 ID
            topic: 主题名称
            content: 消息内容
            performative: 言语行为类型
            
        Returns:
            发送数量
        """
        subscribers = self.subscriptions.get(topic, set())
        if not subscribers:
            logger.warning(f"主题 {topic} 没有订阅者")
            return 0
        
        message = self.send_message(
            sender=sender,
            receivers=list(subscribers),
            performative=performative,
            content=content
        )
        
        logger.info(f"广播消息到 {topic}: {len(subscribers)} 个订阅者")
        return len(subscribers)
    
    def request_response(
        self,
        requester: str,
        responder: str,
        request_content: Any,
        timeout: int = 30
    ) -> Optional[Any]:
        """
        请求 - 响应模式
        
        Args:
            requester: 请求者
            responder: 响应者
            request_content: 请求内容
            timeout: 超时时间（秒）
            
        Returns:
            响应内容或 None
        """
        conversation_id = str(uuid.uuid4())
        
        # 发送请求
        self.send_message(
            sender=requester,
            receivers=[responder],
            performative=Performative.REQUEST,
            content=request_content,
            conversation_id=conversation_id
        )
        
        # 等待响应（简化版，实际应该异步等待）
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            messages = self.receive_messages(requester)
            for msg in messages:
                if (msg.conversation_id == conversation_id and 
                    msg.in_reply_to and 
                    msg.performative in [Performative.INFORM, Performative.AGREE]):
                    return msg.content
            time.sleep(0.1)
        
        logger.warning(f"请求超时：{conversation_id}")
        return None
    
    def get_agent_stats(self, agent_id: str) -> Dict[str, Any]:
        """获取代理统计"""
        if agent_id not in self.agents:
            return {'error': 'Agent not found'}
        
        profile = self.agents[agent_id]
        pending = self.message_queue.pending_count(agent_id)
        conversations = len([c for c in self.conversations.values() 
                            if any(m.sender == agent_id or agent_id in m.receivers 
                                  for m in c)])
        
        return {
            'agent_id': agent_id,
            'type': profile.agent_type,
            'status': profile.status,
            'capabilities': len(profile.capabilities),
            'pending_messages': pending,
            'conversations': conversations,
            'last_seen': profile.last_seen
        }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """获取系统统计"""
        return {
            'total_agents': len(self.agents),
            'active_agents': len([a for a in self.agents.values() if a.status == 'active']),
            'total_conversations': len(self.conversations),
            'total_topics': len(self.subscriptions),
            'pending_messages': sum(
                self.message_queue.pending_count(aid) 
                for aid in self.agents.keys()
            )
        }
    
    def get_summary(self) -> str:
        """获取摘要"""
        stats = self.get_system_stats()
        
        lines = [
            f"Agent Communication System",
            f"",
            f"**Total Agents**: {stats['total_agents']}",
            f"**Active Agents**: {stats['active_agents']}",
            f"**Conversations**: {stats['total_conversations']}",
            f"**Topics**: {stats['total_topics']}",
            f"**Pending Messages**: {stats['pending_messages']}",
            f""
        ]
        
        if self.agents:
            lines.append("**Registered Agents**:")
            for agent_id, profile in self.agents.items():
                lines.append(f"- {agent_id} ({profile.agent_type})")
        
        return '\n'.join(lines)


def main():
    """测试代理通信"""
    comm = AgentCommunication()
    
    print("="*60)
    print("Agent Communication System Test")
    print("="*60)
    
    # 注册代理
    print("\n1. Registering agents...")
    comm.register_agent("coordinator", "orchestrator", [
        {"name": "delegate_task", "description": "Delegate tasks to agents"}
    ])
    comm.register_agent("researcher", "researcher", [
        {"name": "search", "description": "Search information"}
    ])
    comm.register_agent("messenger", "messenger", [
        {"name": "send_message", "description": "Send messages"}
    ])
    print(f"   Registered {len(comm.agents)} agents")
    
    # 订阅主题
    print("\n2. Subscribing to topics...")
    comm.subscribe("researcher", "research-tasks")
    comm.subscribe("messenger", "message-tasks")
    comm.subscribe("coordinator", "all-tasks")
    
    # 发送消息
    print("\n3. Sending messages...")
    comm.send_message(
        sender="coordinator",
        receivers=["researcher"],
        performative=Performative.REQUEST,
        content={"task": "Research AI trends", "priority": "high"}
    )
    
    comm.broadcast(
        sender="system",
        topic="all-tasks",
        content={"announcement": "New task available"},
        performative=Performative.INFORM
    )
    
    # 处理消息
    print("\n4. Processing messages...")
    messages = comm.receive_messages("researcher")
    print(f"   Researcher received {len(messages)} messages")
    
    # 请求 - 响应
    print("\n5. Request-Response pattern...")
    response = comm.request_response(
        requester="coordinator",
        responder="researcher",
        request_content={"query": "What is your status?"}
    )
    
    # 统计
    print("\n" + "="*60)
    print(comm.get_summary())
    
    # 代理统计
    print("\nAgent Stats:")
    for agent_id in comm.agents:
        stats = comm.get_agent_stats(agent_id)
        print(f"  {agent_id}: {stats['pending_messages']} pending, {stats['conversations']} conversations")


if __name__ == '__main__':
    main()
