#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消息协议 - 硅基世界 2

8 种消息类型：
1. Request - 发起协作请求
2. Response - 回复请求
3. Discussion - 多方讨论
4. Decision - 记录决策
5. Task - 任务分配
6. Status - 状态同步
7. Alert - 紧急告警
8. Knowledge - 知识分享
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import uuid


class MessageType(Enum):
    """消息类型"""
    REQUEST = "request"           # 请求
    RESPONSE = "response"         # 响应
    DISCUSSION = "discussion"     # 讨论
    DECISION = "decision"         # 决策
    TASK = "task"                 # 任务
    STATUS = "status"             # 状态
    ALERT = "alert"               # 告警
    KNOWLEDGE = "knowledge"       # 知识


class MessagePriority(Enum):
    """消息优先级"""
    LOW = "low"                   # 低
    NORMAL = "normal"             # 普通
    HIGH = "high"                 # 高
    CRITICAL = "critical"         # 紧急


class ResponseType(Enum):
    """响应类型"""
    ACCEPTANCE = "acceptance"     # 接受
    REJECTION = "rejection"       # 拒绝
    COUNTER_PROPOSAL = "counter_proposal"  # 反提案


@dataclass
class Message:
    """消息基类"""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    sender_id: str = ""
    receiver_id: str = ""
    message_type: MessageType = MessageType.REQUEST
    priority: MessagePriority = MessagePriority.NORMAL
    
    # 消息内容
    subject: str = ""
    body: str = ""
    attachments: List[Dict] = field(default_factory=list)
    
    # 上下文
    context: Dict[str, Any] = field(default_factory=dict)
    
    # 期望
    expectations: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "message_id": self.message_id,
            "timestamp": self.timestamp.isoformat(),
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "message_type": self.message_type.value,
            "priority": self.priority.value,
            "subject": self.subject,
            "body": self.body,
            "attachments": self.attachments,
            "context": self.context,
            "expectations": self.expectations,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Message":
        """从字典创建"""
        return cls(
            message_id=data.get("message_id", str(uuid.uuid4())),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            sender_id=data.get("sender_id", ""),
            receiver_id=data.get("receiver_id", ""),
            message_type=MessageType(data.get("message_type", "request")),
            priority=MessagePriority(data.get("priority", "normal")),
            subject=data.get("subject", ""),
            body=data.get("body", ""),
            attachments=data.get("attachments", []),
            context=data.get("context", {}),
            expectations=data.get("expectations", {}),
        )


@dataclass
class RequestMessage(Message):
    """请求消息"""
    
    def __post_init__(self):
        self.message_type = MessageType.REQUEST
        self.subtype: str = ""  # assessment | implementation | review | discussion
        self.requirements: List[str] = field(default_factory=list)
        self.constraints: List[str] = field(default_factory=list)
        self.deadline: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            "subtype": self.subtype,
            "requirements": self.requirements,
            "constraints": self.constraints,
            "deadline": self.deadline.isoformat() if self.deadline else None,
        })
        return data


@dataclass
class ResponseMessage(Message):
    """响应消息"""
    
    def __post_init__(self):
        self.message_type = MessageType.RESPONSE
        self.in_reply_to: str = ""
        self.response_type: ResponseType = ResponseType.ACCEPTANCE
        self.assessment: str = ""
        self.estimated_time: str = ""
        self.risks: List[str] = field(default_factory=list)
        self.dependencies: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            "in_reply_to": self.in_reply_to,
            "response_type": self.response_type.value,
            "assessment": self.assessment,
            "estimated_time": self.estimated_time,
            "risks": self.risks,
            "dependencies": self.dependencies,
        })
        return data


@dataclass
class DiscussionMessage(Message):
    """讨论消息"""
    
    def __post_init__(self):
        self.message_type = MessageType.DISCUSSION
        self.thread_id: str = ""
        self.participants: List[str] = field(default_factory=list)
        self.points: List[Dict] = field(default_factory=list)
        self.conclusion: str = ""
    
    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            "thread_id": self.thread_id,
            "participants": self.participants,
            "points": self.points,
            "conclusion": self.conclusion,
        })
        return data


@dataclass
class DecisionMessage(Message):
    """决策消息"""
    
    def __post_init__(self):
        self.message_type = MessageType.DECISION
        self.decision_id: str = ""
        self.topic: str = ""
        self.options: List[Dict] = field(default_factory=list)
        self.chosen_option: str = ""
        self.rationale: str = ""
        self.voters: Dict[str, List[str]] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            "decision_id": self.decision_id,
            "topic": self.topic,
            "options": self.options,
            "chosen_option": self.chosen_option,
            "rationale": self.rationale,
            "voters": self.voters,
        })
        return data


@dataclass
class TaskMessage(Message):
    """任务消息"""
    
    def __post_init__(self):
        self.message_type = MessageType.TASK
        self.task_id: str = ""
        self.title: str = ""
        self.description: str = ""
        self.assignee: str = ""
        self.reporter: str = ""
        self.priority: str = "normal"  # critical | high | normal | low
        self.status: str = "open"  # open | in_progress | blocked | done
        self.estimated_hours: int = 0
        self.deadline: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "assignee": self.assignee,
            "reporter": self.reporter,
            "priority": self.priority,
            "status": self.status,
            "estimated_hours": self.estimated_hours,
            "deadline": self.deadline.isoformat() if self.deadline else None,
        })
        return data


@dataclass
class StatusMessage(Message):
    """状态消息"""
    
    def __post_init__(self):
        self.message_type = MessageType.STATUS
        self.task_id: str = ""
        self.status: str = ""
        self.progress: int = 0  # 0-100
        self.updates: str = ""
        self.blockers: List[str] = field(default_factory=list)
        self.next_steps: str = ""
    
    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            "task_id": self.task_id,
            "status": self.status,
            "progress": self.progress,
            "updates": self.updates,
            "blockers": self.blockers,
            "next_steps": self.next_steps,
        })
        return data


@dataclass
class AlertMessage(Message):
    """告警消息"""
    
    def __post_init__(self):
        self.message_type = MessageType.ALERT
        self.alert_level: str = "info"  # critical | warning | info
        self.title: str = ""
        self.description: str = ""
        self.affected_systems: List[str] = field(default_factory=list)
        self.suggested_actions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            "alert_level": self.alert_level,
            "title": self.title,
            "description": self.description,
            "affected_systems": self.affected_systems,
            "suggested_actions": self.suggested_actions,
        })
        return data


@dataclass
class KnowledgeMessage(Message):
    """知识分享消息"""
    
    def __post_init__(self):
        self.message_type = MessageType.KNOWLEDGE
        self.title: str = ""
        self.category: str = ""  # 技术分享 | 产品洞察 | 最佳实践
        self.tags: List[str] = field(default_factory=list)
        self.content: str = ""
        self.references: List[str] = field(default_factory=list)
        self.author: str = ""
    
    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            "title": self.title,
            "category": self.category,
            "tags": self.tags,
            "content": self.content,
            "references": self.references,
            "author": self.author,
        })
        return data


# 消息工厂
class MessageFactory:
    """消息工厂"""
    
    @staticmethod
    def create_request(
        sender_id: str,
        receiver_id: str,
        subject: str,
        body: str,
        subtype: str = "assessment",
        requirements: List[str] = None,
        constraints: List[str] = None,
        deadline: datetime = None,
        priority: MessagePriority = MessagePriority.NORMAL,
    ) -> RequestMessage:
        """创建请求消息"""
        msg = RequestMessage(
            sender_id=sender_id,
            receiver_id=receiver_id,
            subject=subject,
            body=body,
            priority=priority,
        )
        msg.subtype = subtype
        msg.requirements = requirements or []
        msg.constraints = constraints or []
        msg.deadline = deadline
        return msg
    
    @staticmethod
    def create_response(
        sender_id: str,
        receiver_id: str,
        in_reply_to: str,
        response_type: ResponseType = ResponseType.ACCEPTANCE,
        assessment: str = "",
        estimated_time: str = "",
        risks: List[str] = None,
        dependencies: List[str] = None,
    ) -> ResponseMessage:
        """创建响应消息"""
        msg = ResponseMessage(
            sender_id=sender_id,
            receiver_id=receiver_id,
            subject="Re: " + in_reply_to,
            body="",
        )
        msg.in_reply_to = in_reply_to
        msg.response_type = response_type
        msg.assessment = assessment
        msg.estimated_time = estimated_time
        msg.risks = risks or []
        msg.dependencies = dependencies or []
        return msg
    
    @staticmethod
    def create_task(
        sender_id: str,
        receiver_id: str,
        title: str,
        description: str,
        priority: str = "normal",
        estimated_hours: int = 0,
        deadline: datetime = None,
    ) -> TaskMessage:
        """创建任务消息"""
        msg = TaskMessage(
            sender_id=sender_id,
            receiver_id=receiver_id,
            subject=title,
            body=description,
        )
        msg.task_id = str(uuid.uuid4())
        msg.title = title
        msg.description = description
        msg.assignee = receiver_id
        msg.reporter = sender_id
        msg.priority = priority
        msg.estimated_hours = estimated_hours
        msg.deadline = deadline
        return msg
    
    @staticmethod
    def create_status(
        sender_id: str,
        receiver_id: str,
        task_id: str,
        status: str,
        progress: int = 0,
        updates: str = "",
        blockers: List[str] = None,
        next_steps: str = "",
    ) -> StatusMessage:
        """创建状态消息"""
        msg = StatusMessage(
            sender_id=sender_id,
            receiver_id=receiver_id,
            subject=f"Status: {task_id}",
        )
        msg.task_id = task_id
        msg.status = status
        msg.progress = progress
        msg.updates = updates
        msg.blockers = blockers or []
        msg.next_steps = next_steps
        return msg
    
    @staticmethod
    def create_alert(
        sender_id: str,
        receiver_id: str,
        title: str,
        description: str,
        alert_level: str = "warning",
        affected_systems: List[str] = None,
        suggested_actions: List[str] = None,
    ) -> AlertMessage:
        """创建告警消息"""
        msg = AlertMessage(
            sender_id=sender_id,
            receiver_id=receiver_id,
            subject=title,
            body=description,
        )
        msg.alert_level = alert_level
        msg.title = title
        msg.description = description
        msg.affected_systems = affected_systems or []
        msg.suggested_actions = suggested_actions or []
        return msg
    
    @staticmethod
    def create_knowledge(
        sender_id: str,
        receiver_id: str,
        title: str,
        content: str,
        category: str = "技术分享",
        tags: List[str] = None,
        references: List[str] = None,
    ) -> KnowledgeMessage:
        """创建知识分享消息"""
        msg = KnowledgeMessage(
            sender_id=sender_id,
            receiver_id=receiver_id,
            subject=title,
            body=content,
        )
        msg.title = title
        msg.content = content
        msg.category = category
        msg.tags = tags or []
        msg.references = references or []
        msg.author = sender_id
        return msg
