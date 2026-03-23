#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件系统 - 硅基世界 2

让 Agent 可以发送和接收邮件。
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class MailType(Enum):
    """邮件类型"""
    PERSONAL = "personal"    # 个人邮件
    SYSTEM = "system"        # 系统邮件
    NOTIFICATION = "notification"  # 通知
    INVITATION = "invitation"  # 邀请


class MailStatus(Enum):
    """邮件状态"""
    UNREAD = "unread"      # 未读
    READ = "read"          # 已读
    ARCHIVED = "archived"  # 已归档
    DELETED = "deleted"    # 已删除


@dataclass
class Mail:
    """邮件"""
    mail_id: str
    sender: str
    receiver: str
    subject: str
    content: str
    mail_type: MailType = MailType.PERSONAL
    status: MailStatus = MailStatus.UNREAD
    sent_at: float = field(default_factory=lambda: datetime.now().timestamp())
    read_at: Optional[float] = None
    attachments: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "mail_id": self.mail_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "subject": self.subject,
            "content": self.content[:500],
            "type": self.mail_type.value,
            "status": self.status.value,
            "sent_at": self.sent_at,
            "read_at": self.read_at,
        }


class MailManager:
    """邮件管理器"""
    
    def __init__(self):
        """初始化邮件管理器"""
        self.mails: Dict[str, List[Mail]] = {}  # receiver -> [mails]
        self._mail_counter = 0
        
        print("📧 邮件系统已初始化")
    
    def send(
        self,
        sender: str,
        receiver: str,
        subject: str,
        content: str,
        mail_type: MailType = MailType.PERSONAL,
        attachments: Optional[List[Dict]] = None,
    ) -> Mail:
        """
        发送邮件
        
        Args:
            sender: 发送者
            receiver: 接收者
            subject: 主题
            content: 内容
            mail_type: 邮件类型
            attachments: 附件
            
        Returns:
            邮件对象
        """
        self._mail_counter += 1
        
        mail = Mail(
            mail_id=f"mail_{self._mail_counter}",
            sender=sender,
            receiver=receiver,
            subject=subject,
            content=content,
            mail_type=mail_type,
            attachments=attachments or [],
        )
        
        if receiver not in self.mails:
            self.mails[receiver] = []
        
        self.mails[receiver].append(mail)
        
        print(f"  📧 {sender} 发送邮件给 {receiver}: {subject}")
        
        return mail
    
    def read(self, receiver: str, mail_id: str) -> Optional[Mail]:
        """
        阅读邮件
        
        Args:
            receiver: 接收者
            mail_id: 邮件 ID
            
        Returns:
            邮件对象
        """
        if receiver not in self.mails:
            return None
        
        for mail in self.mails[receiver]:
            if mail.mail_id == mail_id:
                mail.status = MailStatus.READ
                mail.read_at = datetime.now().timestamp()
                return mail
        
        return None
    
    def archive(self, receiver: str, mail_id: str) -> bool:
        """归档邮件"""
        mail = self._get_mail(receiver, mail_id)
        if mail:
            mail.status = MailStatus.ARCHIVED
            return True
        return False
    
    def delete(self, receiver: str, mail_id: str) -> bool:
        """删除邮件"""
        if receiver not in self.mails:
            return False
        
        for i, mail in enumerate(self.mails[receiver]):
            if mail.mail_id == mail_id:
                mail.status = MailStatus.DELETED
                return True
        
        return False
    
    def _get_mail(self, receiver: str, mail_id: str) -> Optional[Mail]:
        """获取邮件"""
        if receiver not in self.mails:
            return None
        
        for mail in self.mails[receiver]:
            if mail.mail_id == mail_id:
                return mail
        
        return None
    
    def get_inbox(self, receiver: str, status: Optional[MailStatus] = None, limit: int = 50) -> List[Mail]:
        """
        获取收件箱
        
        Args:
            receiver: 接收者
            status: 状态过滤
            limit: 返回数量
            
        Returns:
            邮件列表
        """
        if receiver not in self.mails:
            return []
        
        mails = self.mails[receiver]
        
        # 排除已删除
        mails = [m for m in mails if m.status != MailStatus.DELETED]
        
        if status:
            mails = [m for m in mails if m.status == status]
        
        # 按时间排序
        mails.sort(key=lambda x: x.sent_at, reverse=True)
        
        return mails[:limit]
    
    def get_unread_count(self, receiver: str) -> int:
        """获取未读邮件数"""
        if receiver not in self.mails:
            return 0
        
        return len([
            m for m in self.mails[receiver]
            if m.status == MailStatus.UNREAD and m.status != MailStatus.DELETED
        ])
    
    def get_sent(self, sender: str, limit: int = 50) -> List[Mail]:
        """获取已发送"""
        sent = []
        
        for mails in self.mails.values():
            for mail in mails:
                if mail.sender == sender:
                    sent.append(mail)
        
        sent.sort(key=lambda x: x.sent_at, reverse=True)
        
        return sent[:limit]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total = sum(len(mails) for mails in self.mails.values())
        unread = sum(
            len([m for m in mails if m.status == MailStatus.UNREAD])
            for mails in self.mails.values()
        )
        
        return {
            "total_mails": total,
            "unread": unread,
            "receivers": len(self.mails),
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
        }


# 单例
_mail_manager: Optional[MailManager] = None


def get_mail_manager() -> MailManager:
    """获取邮件管理器单例"""
    global _mail_manager
    if _mail_manager is None:
        _mail_manager = MailManager()
    return _mail_manager


# 工厂函数
def create_mail_manager() -> MailManager:
    """创建邮件管理器"""
    return MailManager()
