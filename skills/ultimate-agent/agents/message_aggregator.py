"""
Message Aggregator - 消息聚合器

统一管理和分发来自多个平台的消息（WhatsApp/Telegram/Slack 等）
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from enum import Enum

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('message-aggregator')


class MessagePlatform(Enum):
    """支持的消息平台"""
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"
    SLACK = "slack"
    DISCORD = "discord"
    SIGNAL = "signal"
    WECHAT = "wechat"
    UNKNOWN = "unknown"


class MessagePriority(Enum):
    """消息优先级"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class Message:
    """消息对象"""
    
    def __init__(
        self,
        content: str,
        platform: MessagePlatform,
        sender: str,
        timestamp: datetime,
        chat_id: Optional[str] = None,
        message_id: Optional[str] = None,
        is_group: bool = False,
        attachments: Optional[List[str]] = None
    ):
        self.content = content
        self.platform = platform
        self.sender = sender
        self.timestamp = timestamp
        self.chat_id = chat_id
        self.message_id = message_id
        self.is_group = is_group
        self.attachments = attachments or []
        self.priority = MessagePriority.NORMAL
        self.processed = False
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'content': self.content,
            'platform': self.platform.value,
            'sender': self.sender,
            'timestamp': self.timestamp.isoformat(),
            'chat_id': self.chat_id,
            'message_id': self.message_id,
            'is_group': self.is_group,
            'attachments': self.attachments,
            'priority': self.priority.value,
            'processed': self.processed
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """从字典创建"""
        msg = cls(
            content=data['content'],
            platform=MessagePlatform(data.get('platform', 'unknown')),
            sender=data['sender'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            chat_id=data.get('chat_id'),
            message_id=data.get('message_id'),
            is_group=data.get('is_group', False),
            attachments=data.get('attachments', [])
        )
        msg.priority = MessagePriority(data.get('priority', 'normal'))
        msg.processed = data.get('processed', False)
        return msg
    
    def __repr__(self) -> str:
        return f"Message({self.platform.value}, {self.sender}, {self.content[:30]}...)"


class MessageAggregator:
    """
    消息聚合器
    
    职责:
    - 接收来自多个平台的消息
    - 统一消息格式和接口
    - 消息过滤和优先级排序
    - 消息路由和分发
    - 发送消息到指定平台
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        初始化消息聚合器
        
        Args:
            config_dir: 配置文件目录
        """
        if config_dir is None:
            config_dir = Path(__file__).parent
            
        self.config_dir = config_dir
        self.config_file = config_dir / "message-aggregator.json"
        
        # 消息队列
        self.inbox: List[Message] = []
        self.sent_history: List[Message] = []
        
        # 平台连接状态
        self.platform_connections: Dict[MessagePlatform, bool] = {
            platform: False for platform in MessagePlatform
        }
        
        # 消息处理器（回调函数）
        self.message_handlers: List[Callable[[Message], None]] = []
        
        # 加载配置
        self._load_config()
    
    def _load_config(self) -> None:
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    logger.info(f"已加载消息聚合器配置：{self.config_file}")
                    
                    # 恢复平台连接状态
                    connected_platforms = config.get('connected_platforms', [])
                    for platform_name in connected_platforms:
                        try:
                            platform = MessagePlatform(platform_name)
                            self.platform_connections[platform] = True
                        except ValueError:
                            pass
            except Exception as e:
                logger.error(f"加载配置失败：{e}")
        else:
            logger.info("配置文件不存在，使用默认配置")
            self._save_config()
    
    def _save_config(self) -> None:
        """保存配置文件"""
        config = {
            'connected_platforms': [
                p.value for p, connected in self.platform_connections.items() 
                if connected
            ],
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        logger.info(f"配置已保存：{self.config_file}")
    
    def connect_platform(self, platform: MessagePlatform, credentials: Dict[str, Any]) -> bool:
        """
        连接消息平台
        
        Args:
            platform: 平台类型
            credentials: 平台认证信息
            
        Returns:
            连接是否成功
        """
        logger.info(f"尝试连接平台：{platform.value}")
        
        # TODO: 实现实际的平台连接逻辑
        # 目前模拟连接成功
        
        # 验证凭证（简化版）
        if not credentials:
            logger.error(f"缺少 {platform.value} 的认证信息")
            return False
        
        # 模拟连接
        self.platform_connections[platform] = True
        self._save_config()
        
        logger.info(f"成功连接平台：{platform.value}")
        return True
    
    def disconnect_platform(self, platform: MessagePlatform) -> bool:
        """断开平台连接"""
        self.platform_connections[platform] = False
        self._save_config()
        logger.info(f"已断开平台：{platform.value}")
        return True
    
    def receive_message(self, message: Message) -> None:
        """
        接收消息
        
        Args:
            message: 消息对象
        """
        # 检查平台是否已连接
        if not self.platform_connections.get(message.platform, False):
            logger.warning(f"平台 {message.platform.value} 未连接，消息已忽略")
            return
        
        # 分析消息优先级
        self._analyze_priority(message)
        
        # 添加到收件箱
        self.inbox.append(message)
        
        # 通知处理器
        for handler in self.message_handlers:
            try:
                handler(message)
            except Exception as e:
                logger.error(f"消息处理器错误：{e}")
        
        logger.info(f"收到消息：{message.platform.value} - {message.sender}")
    
    def _analyze_priority(self, message: Message) -> None:
        """分析消息优先级"""
        content_lower = message.content.lower()
        
        # 紧急关键词
        urgent_keywords = ['紧急', 'urgent', '急', 'asap', '立即', 'immediately']
        if any(kw in content_lower for kw in urgent_keywords):
            message.priority = MessagePriority.URGENT
            return
        
        # 高优先级关键词
        high_keywords = ['重要', 'important', '优先', 'priority', '请尽快']
        if any(kw in content_lower for kw in high_keywords):
            message.priority = MessagePriority.HIGH
            return
        
        # @提及
        if '@' in message.content:
            message.priority = MessagePriority.HIGH
            return
        
        # 默认为普通优先级
        message.priority = MessagePriority.NORMAL
    
    def send_message(
        self,
        content: str,
        platform: MessagePlatform,
        recipient: str,
        chat_id: Optional[str] = None
    ) -> bool:
        """
        发送消息
        
        Args:
            content: 消息内容
            platform: 目标平台
            recipient: 接收者
            chat_id: 聊天 ID（可选）
            
        Returns:
            发送是否成功
        """
        logger.info(f"发送消息到 {platform.value}: {recipient}")
        
        # 检查平台是否已连接
        if not self.platform_connections.get(platform, False):
            logger.error(f"平台 {platform.value} 未连接")
            return False
        
        # 创建消息对象
        message = Message(
            content=content,
            platform=platform,
            sender='me',  # 自己发送的
            timestamp=datetime.now(),
            chat_id=chat_id
        )
        
        # TODO: 实现实际的消息发送逻辑
        # 目前模拟发送成功
        
        # 添加到发送历史
        message.processed = True
        self.sent_history.append(message)
        
        logger.info(f"消息已发送：{platform.value} - {recipient}")
        return True
    
    def get_unread_messages(
        self,
        platform: Optional[MessagePlatform] = None,
        priority: Optional[MessagePriority] = None
    ) -> List[Message]:
        """
        获取未读消息
        
        Args:
            platform: 过滤平台（可选）
            priority: 过滤优先级（可选）
            
        Returns:
            未读消息列表
        """
        unread = [m for m in self.inbox if not m.processed]
        
        if platform:
            unread = [m for m in unread if m.platform == platform]
        
        if priority:
            unread = [m for m in unread if m.priority == priority]
        
        # 按优先级和时间排序
        priority_order = {
            MessagePriority.URGENT: 0,
            MessagePriority.HIGH: 1,
            MessagePriority.NORMAL: 2,
            MessagePriority.LOW: 3
        }
        unread.sort(key=lambda m: (priority_order[m.priority], m.timestamp))
        
        return unread
    
    def mark_as_read(self, message: Message) -> None:
        """标记消息为已读"""
        message.processed = True
        logger.info(f"消息已标记为已读：{message}")
    
    def mark_all_as_read(self, platform: Optional[MessagePlatform] = None) -> int:
        """
        标记所有消息为已读
        
        Args:
            platform: 过滤平台（可选）
            
        Returns:
            标记的消息数量
        """
        count = 0
        for message in self.inbox:
            if not message.processed:
                if platform is None or message.platform == platform:
                    message.processed = True
                    count += 1
        
        logger.info(f"已标记 {count} 条消息为已读")
        return count
    
    def register_handler(self, handler: Callable[[Message], None]) -> None:
        """注册消息处理器"""
        self.message_handlers.append(handler)
        logger.info("消息处理器已注册")
    
    def get_status(self) -> Dict[str, Any]:
        """获取聚合器状态"""
        unread_count = len([m for m in self.inbox if not m.processed])
        sent_count = len(self.sent_history)
        
        return {
            'connected_platforms': [
                p.value for p, connected in self.platform_connections.items() 
                if connected
            ],
            'unread_messages': unread_count,
            'sent_messages': sent_count,
            'handlers_registered': len(self.message_handlers),
            'status': 'active'
        }
    
    def get_summary(self) -> str:
        """获取消息摘要"""
        unread = self.get_unread_messages()
        
        if not unread:
            return "没有未读消息"
        
        # 按优先级分组
        urgent = [m for m in unread if m.priority == MessagePriority.URGENT]
        high = [m for m in unread if m.priority == MessagePriority.HIGH]
        normal = [m for m in unread if m.priority == MessagePriority.NORMAL]
        
        lines = ["📬 消息摘要", ""]
        
        if urgent:
            lines.append(f"🔴 紧急：{len(urgent)} 条")
            for msg in urgent[:3]:
                lines.append(f"  - {msg.platform.value}: {msg.sender} - {msg.content[:30]}...")
        
        if high:
            lines.append(f"🟠 重要：{len(high)} 条")
            for msg in high[:3]:
                lines.append(f"  - {msg.platform.value}: {msg.sender} - {msg.content[:30]}...")
        
        if normal:
            lines.append(f"⚪ 普通：{len(normal)} 条")
        
        return '\n'.join(lines)


def main():
    """测试消息聚合器功能"""
    aggregator = MessageAggregator()
    
    # 模拟连接平台
    aggregator.connect_platform(MessagePlatform.WHATSAPP, {'token': 'test'})
    aggregator.connect_platform(MessagePlatform.TELEGRAM, {'bot_token': 'test'})
    
    # 模拟接收消息
    test_messages = [
        Message("紧急：项目截止日期提前了！", MessagePlatform.WHATSAPP, "张三", datetime.now()),
        Message("请尽快回复这个重要问题", MessagePlatform.TELEGRAM, "李四", datetime.now()),
        Message("早上好！今天天气不错", MessagePlatform.WHATSAPP, "王五", datetime.now()),
    ]
    
    for msg in test_messages:
        aggregator.receive_message(msg)
    
    # 获取未读消息
    print("\n未读消息:")
    print('='*60)
    unread = aggregator.get_unread_messages()
    for msg in unread:
        print(f"[{msg.priority.value}] {msg.platform.value} - {msg.sender}: {msg.content}")
    
    # 消息摘要
    print("\n" + '='*60)
    print(aggregator.get_summary())
    
    # 发送消息
    print("\n" + '='*60)
    aggregator.send_message("收到，谢谢！", MessagePlatform.WHATSAPP, "张三")
    
    # 状态
    print("\n" + '='*60)
    print("聚合器状态:")
    print('='*60)
    status = aggregator.get_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
