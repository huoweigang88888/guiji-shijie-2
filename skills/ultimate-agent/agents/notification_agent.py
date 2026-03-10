"""
通知代理 - Notification Agent

支持多渠道通知推送，包括：
- 系统通知
- Webhook
- 邮件（SMTP）
- 控制台输出

功能：
- 多渠道通知
- 通知模板
- 优先级管理
- 历史记录
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, asdict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger('notification-agent')


class NotificationChannel(Enum):
    """通知渠道"""
    CONSOLE = "console"
    SYSTEM = "system"
    WEBHOOK = "webhook"
    EMAIL = "email"
    ALL = "all"


class NotificationPriority(Enum):
    """通知优先级"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class Notification:
    """通知对象"""
    title: str
    message: str
    channel: NotificationChannel
    priority: NotificationPriority = NotificationPriority.NORMAL
    created_at: str = ""
    sent_at: str = ""
    status: str = "pending"
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'title': self.title,
            'message': self.message,
            'channel': self.channel.value,
            'priority': self.priority.value,
            'created_at': self.created_at,
            'sent_at': self.sent_at,
            'status': self.status,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Notification':
        """从字典创建"""
        return cls(
            title=data['title'],
            message=data['message'],
            channel=NotificationChannel(data['channel']),
            priority=NotificationPriority(data.get('priority', 'normal')),
            created_at=data.get('created_at', ''),
            sent_at=data.get('sent_at', ''),
            status=data.get('status', 'pending'),
            metadata=data.get('metadata', {})
        )


@dataclass
class NotificationConfig:
    """通知配置"""
    # 系统通知
    enable_system: bool = True
    
    # Webhook
    webhook_url: str = ""
    webhook_headers: Dict[str, str] = None
    
    # 邮件
    smtp_server: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    email_from: str = ""
    email_to: List[str] = None
    
    def __post_init__(self):
        if self.webhook_headers is None:
            self.webhook_headers = {}
        if self.email_to is None:
            self.email_to = []
    
    def to_dict(self) -> dict:
        """转换为字典（不包含密码）"""
        return {
            'enable_system': self.enable_system,
            'webhook_url': self.webhook_url,
            'webhook_headers': self.webhook_headers,
            'smtp_server': self.smtp_server,
            'smtp_port': self.smtp_port,
            'smtp_user': self.smtp_user,
            'email_from': self.email_from,
            'email_to': self.email_to
        }


class NotificationAgent:
    """
    通知代理
    
    支持多渠道通知推送
    """
    
    def __init__(self, data_dir: Path):
        """
        初始化通知代理
        
        Args:
            data_dir: 数据目录
        """
        self.data_dir = Path(data_dir)
        self.config_file = self.data_dir / "notification-config.json"
        self.history_file = self.data_dir / "notification-history.json"
        
        # 确保目录存在
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载配置和历史
        self.config = self._load_config()
        self.history: List[Notification] = self._load_history()
        
        logger.info(f"通知代理已初始化：{self.data_dir}")
    
    def _load_config(self) -> NotificationConfig:
        """加载配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return NotificationConfig(
                        enable_system=data.get('enable_system', True),
                        webhook_url=data.get('webhook_url', ''),
                        webhook_headers=data.get('webhook_headers', {}),
                        smtp_server=data.get('smtp_server', ''),
                        smtp_port=data.get('smtp_port', 587),
                        smtp_user=data.get('smtp_user', ''),
                        email_from=data.get('email_from', ''),
                        email_to=data.get('email_to', [])
                    )
            except Exception as e:
                logger.error(f"加载配置失败：{e}")
        
        # 返回默认配置
        return NotificationConfig()
    
    def _save_config(self) -> None:
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config.to_dict(), f, indent=2, ensure_ascii=False)
        logger.info("配置已保存")
    
    def _load_history(self) -> List[Notification]:
        """加载历史记录"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [Notification.from_dict(n) for n in data.get('notifications', [])]
            except Exception as e:
                logger.error(f"加载历史失败：{e}")
        return []
    
    def _save_history(self) -> None:
        """保存历史记录"""
        # 限制历史记录数量（保留最近 100 条）
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump({
                'notifications': [n.to_dict() for n in self.history],
                'last_updated': datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
    
    def configure(self, **kwargs) -> bool:
        """
        配置通知渠道
        
        Args:
            **kwargs: 配置参数
            
        Returns:
            是否成功
        """
        try:
            if 'enable_system' in kwargs:
                self.config.enable_system = kwargs['enable_system']
            if 'webhook_url' in kwargs:
                self.config.webhook_url = kwargs['webhook_url']
            if 'webhook_headers' in kwargs:
                self.config.webhook_headers = kwargs['webhook_headers']
            if 'smtp_server' in kwargs:
                self.config.smtp_server = kwargs['smtp_server']
            if 'smtp_port' in kwargs:
                self.config.smtp_port = kwargs['smtp_port']
            if 'smtp_user' in kwargs:
                self.config.smtp_user = kwargs['smtp_user']
            if 'smtp_password' in kwargs:
                self.config.smtp_password = kwargs['smtp_password']
            if 'email_from' in kwargs:
                self.config.email_from = kwargs['email_from']
            if 'email_to' in kwargs:
                self.config.email_to = kwargs['email_to']
            
            self._save_config()
            logger.info("配置已更新")
            return True
        except Exception as e:
            logger.error(f"配置失败：{e}")
            return False
    
    def send(
        self,
        title: str,
        message: str,
        channel: NotificationChannel = NotificationChannel.CONSOLE,
        priority: NotificationPriority = NotificationPriority.NORMAL,
        metadata: Dict[str, Any] = None
    ) -> bool:
        """
        发送通知
        
        Args:
            title: 标题
            message: 消息内容
            channel: 通知渠道
            priority: 优先级
            metadata: 元数据
            
        Returns:
            是否成功
        """
        notification = Notification(
            title=title,
            message=message,
            channel=channel,
            priority=priority,
            metadata=metadata or {}
        )
        
        logger.info(f"发送通知 [{channel.value}]: {title}")
        
        success = False
        
        if channel == NotificationChannel.CONSOLE:
            success = self._send_console(notification)
        elif channel == NotificationChannel.SYSTEM:
            success = self._send_system(notification)
        elif channel == NotificationChannel.WEBHOOK:
            success = self._send_webhook(notification)
        elif channel == NotificationChannel.EMAIL:
            success = self._send_email(notification)
        elif channel == NotificationChannel.ALL:
            # 发送到所有启用的渠道
            success = True
            if self.config.enable_system:
                success &= self._send_system(notification)
            if self.config.webhook_url:
                success &= self._send_webhook(notification)
            if self.config.smtp_server and self.config.email_to:
                success &= self._send_email(notification)
            # 控制台总是输出
            self._send_console(notification)
        
        # 更新状态并保存历史
        notification.status = "sent" if success else "failed"
        notification.sent_at = datetime.now().isoformat()
        self.history.append(notification)
        self._save_history()
        
        return success
    
    def _send_console(self, notification: Notification) -> bool:
        """发送到控制台"""
        priority_icons = {
            NotificationPriority.LOW: "📝",
            NotificationPriority.NORMAL: "📢",
            NotificationPriority.HIGH: "⚠️",
            NotificationPriority.URGENT: "🚨"
        }
        
        icon = priority_icons.get(notification.priority, "📢")
        print(f"\n{icon} [{notification.priority.value.upper()}] {notification.title}")
        print(f"   {notification.message}\n")
        
        return True
    
    def _send_system(self, notification: Notification) -> bool:
        """发送系统通知"""
        if not self.config.enable_system:
            return False
        
        try:
            # Windows 系统通知
            import subprocess
            script = f"""
            [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")
            [System.Windows.Forms.MessageBox]::Show("{notification.message}", "{notification.title}")
            """
            subprocess.run(['powershell', '-Command', script], timeout=5)
            logger.info("系统通知已发送")
            return True
        except Exception as e:
            logger.error(f"系统通知失败：{e}")
            # 降级到控制台
            return self._send_console(notification)
    
    def _send_webhook(self, notification: Notification) -> bool:
        """发送 Webhook 通知"""
        if not self.config.webhook_url:
            logger.warning("Webhook URL 未配置")
            return False
        
        try:
            import urllib.request
            import json
            
            payload = {
                'title': notification.title,
                'message': notification.message,
                'priority': notification.priority.value,
                'timestamp': notification.created_at,
                **notification.metadata
            }
            
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                self.config.webhook_url,
                data=data,
                headers={
                    'Content-Type': 'application/json',
                    **self.config.webhook_headers
                }
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                logger.info(f"Webhook 通知已发送，状态码：{response.status}")
                return True
        except Exception as e:
            logger.error(f"Webhook 通知失败：{e}")
            return False
    
    def _send_email(self, notification: Notification) -> bool:
        """发送邮件通知"""
        if not self.config.smtp_server or not self.config.email_to:
            logger.warning("邮件配置不完整")
            return False
        
        try:
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = self.config.email_from
            msg['To'] = ', '.join(self.config.email_to)
            msg['Subject'] = f"[{notification.priority.value.upper()}] {notification.title}"
            
            # 邮件正文
            body = f"""
<html>
<body>
    <h2>{notification.title}</h2>
    <p>{notification.message}</p>
    <hr>
    <p><small>发送时间：{notification.created_at}</small></p>
</body>
</html>
            """
            msg.attach(MIMEText(body, 'html', 'utf-8'))
            
            # 发送邮件
            server = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port)
            server.starttls()
            server.login(self.config.smtp_user, self.config.smtp_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"邮件通知已发送到 {len(self.config.email_to)} 个收件人")
            return True
        except Exception as e:
            logger.error(f"邮件通知失败：{e}")
            return False
    
    def get_history(self, limit: int = 10) -> List[Notification]:
        """获取历史记录"""
        return self.history[-limit:]
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        total = len(self.history)
        by_channel = {}
        by_priority = {}
        by_status = {}
        
        for n in self.history:
            # 按渠道统计
            ch = n.channel.value
            by_channel[ch] = by_channel.get(ch, 0) + 1
            
            # 按优先级统计
            p = n.priority.value
            by_priority[p] = by_priority.get(p, 0) + 1
            
            # 按状态统计
            s = n.status
            by_status[s] = by_status.get(s, 0) + 1
        
        return {
            'total_notifications': total,
            'by_channel': by_channel,
            'by_priority': by_priority,
            'by_status': by_status,
            'config': self.config.to_dict()
        }
    
    def clear_history(self) -> int:
        """清空历史记录"""
        count = len(self.history)
        self.history = []
        self._save_history()
        logger.info(f"已清空 {count} 条历史记录")
        return count


# 测试代码
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    # 创建测试实例
    agent = NotificationAgent(Path('./test-notifications'))
    
    # 测试发送通知
    print("\n=== 测试通知代理 ===\n")
    
    # 控制台通知
    agent.send(
        title="测试通知",
        message="这是一条测试消息",
        channel=NotificationChannel.CONSOLE,
        priority=NotificationPriority.NORMAL
    )
    
    # 高优先级通知
    agent.send(
        title="⚠️ 警告",
        message="系统资源使用率超过 80%",
        channel=NotificationChannel.CONSOLE,
        priority=NotificationPriority.HIGH
    )
    
    # 查看统计
    print("\n=== 统计信息 ===")
    print(json.dumps(agent.get_stats(), indent=2, ensure_ascii=False))
