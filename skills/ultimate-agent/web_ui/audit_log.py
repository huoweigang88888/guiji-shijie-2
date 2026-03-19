#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
审计日志模块 - Audit Log

功能：
- 记录用户操作
- 记录系统事件
- 日志查询和筛选
- 日志导出

Phase 6.3 - 安全增强版
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import csv

logger = logging.getLogger('audit')


@dataclass
class AuditEntry:
    """审计日志条目"""
    id: int
    timestamp: str
    event_type: str  # login, logout, config_change, task_create, etc.
    username: str
    action: str
    resource: str
    details: Dict[str, Any]
    ip_address: str = ""
    user_agent: str = ""
    status: str = "success"  # success, failure


class AuditLogger:
    """审计日志记录器"""
    
    def __init__(self, data_dir: Optional[Path] = None, max_entries: int = 10000):
        self.data_dir = data_dir or Path(__file__).parent.parent / 'audit_logs'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.data_dir / 'audit.jsonl'
        self.max_entries = max_entries
        self.entry_counter = 0
        self._load_counter()
    
    def _load_counter(self):
        """加载计数器"""
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if lines:
                    try:
                        last_entry = json.loads(lines[-1])
                        self.entry_counter = last_entry.get('id', 0)
                    except:
                        self.entry_counter = 0
    
    def log(self, event_type: str, action: str, username: str = "system",
            resource: str = "", details: Optional[Dict] = None,
            ip_address: str = "", user_agent: str = "", status: str = "success"):
        """记录审计日志"""
        self.entry_counter += 1
        
        entry = AuditEntry(
            id=self.entry_counter,
            timestamp=datetime.now().isoformat(),
            event_type=event_type,
            username=username,
            action=action,
            resource=resource,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
            status=status
        )
        
        # 写入文件（JSONL 格式）
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(entry), ensure_ascii=False) + '\n')
        
        # 清理旧日志
        self._cleanup_old_entries()
        
        logger.info(f"📝 AUDIT: {event_type}.{action} by {username} - {status}")
        
        return entry
    
    def _cleanup_old_entries(self):
        """清理旧日志，保留最近的 max_entries 条"""
        if not self.log_file.exists():
            return
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) > self.max_entries:
            # 保留最近的 max_entries 条
            lines = lines[-self.max_entries:]
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            logger.info(f"🗑️ 已清理旧审计日志，保留 {len(lines)} 条")
    
    def get_entries(self, limit: int = 100, offset: int = 0,
                    event_type: Optional[str] = None,
                    username: Optional[str] = None,
                    start_date: Optional[str] = None,
                    end_date: Optional[str] = None) -> List[Dict]:
        """获取审计日志"""
        entries = []
        
        if not self.log_file.exists():
            return []
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    
                    # 筛选
                    if event_type and entry.get('event_type') != event_type:
                        continue
                    if username and entry.get('username') != username:
                        continue
                    if start_date and entry.get('timestamp', '') < start_date:
                        continue
                    if end_date and entry.get('timestamp', '') > end_date:
                        continue
                    
                    entries.append(entry)
                except:
                    continue
        
        # 排序（最新的在前）
        entries.sort(key=lambda x: x.get('id', 0), reverse=True)
        
        # 分页
        return entries[offset:offset + limit]
    
    def get_statistics(self, days: int = 7) -> Dict:
        """获取统计数据"""
        entries = self.get_entries(limit=10000)
        
        now = datetime.now()
        cutoff = (now - timedelta(days=days)).isoformat()
        
        recent_entries = [e for e in entries if e.get('timestamp', '') > cutoff]
        
        stats = {
            'total_entries': len(recent_entries),
            'by_event_type': {},
            'by_user': {},
            'by_status': {'success': 0, 'failure': 0},
            'top_actions': []
        }
        
        for entry in recent_entries:
            # 按事件类型统计
            event_type = entry.get('event_type', 'unknown')
            stats['by_event_type'][event_type] = stats['by_event_type'].get(event_type, 0) + 1
            
            # 按用户统计
            username = entry.get('username', 'unknown')
            stats['by_user'][username] = stats['by_user'].get(username, 0) + 1
            
            # 按状态统计
            status = entry.get('status', 'unknown')
            if status in stats['by_status']:
                stats['by_status'][status] += 1
        
        # 最常执行的操作
        action_counts = {}
        for entry in recent_entries:
            action = entry.get('action', 'unknown')
            action_counts[action] = action_counts.get(action, 0) + 1
        
        stats['top_actions'] = sorted(
            [{'action': k, 'count': v} for k, v in action_counts.items()],
            key=lambda x: x['count'],
            reverse=True
        )[:10]
        
        return stats
    
    def export_csv(self, output_file: Path, limit: int = 1000) -> int:
        """导出为 CSV"""
        entries = self.get_entries(limit=limit)
        
        if not entries:
            return 0
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            if entries:
                writer = csv.DictWriter(f, fieldnames=entries[0].keys())
                writer.writeheader()
                writer.writerows(entries)
        
        return len(entries)
    
    def search(self, query: str, limit: int = 100) -> List[Dict]:
        """搜索审计日志"""
        entries = self.get_entries(limit=1000)
        results = []
        
        query_lower = query.lower()
        
        for entry in entries:
            # 搜索各个字段
            searchable = ' '.join([
                str(entry.get('event_type', '')),
                str(entry.get('username', '')),
                str(entry.get('action', '')),
                str(entry.get('resource', '')),
                json.dumps(entry.get('details', {}))
            ]).lower()
            
            if query_lower in searchable:
                results.append(entry)
                
                if len(results) >= limit:
                    break
        
        return results


# 事件类型常量
EVENT_LOGIN = 'login'
EVENT_LOGOUT = 'logout'
EVENT_CONFIG_CHANGE = 'config_change'
EVENT_TASK_CREATE = 'task_create'
EVENT_TASK_DELETE = 'task_delete'
EVENT_USER_CREATE = 'user_create'
EVENT_USER_DELETE = 'user_delete'
EVENT_REPORT_GENERATE = 'report_generate'
EVENT_NOTIFICATION_SEND = 'notification_send'
EVENT_SYSTEM_START = 'system_start'
EVENT_SYSTEM_STOP = 'system_stop'


# 全局实例
_audit_logger: Optional[AuditLogger] = None


def get_audit_logger() -> AuditLogger:
    """获取审计日志记录器实例"""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger


# Flask 集成
def init_audit_logging(app):
    """初始化 Flask 应用审计日志"""
    from flask import request, g
    
    audit_logger = get_audit_logger()
    
    @app.before_request
    def log_request():
        """记录请求"""
        g.start_time = datetime.now()
    
    @app.after_request
    def log_response(response):
        """记录响应"""
        if request.path.startswith('/api/'):
            username = getattr(g, 'current_user', None)
            username = username.username if username else 'anonymous'
            
            audit_logger.log(
                event_type='api_request',
                action=f"{request.method} {request.path}",
                username=username,
                resource=request.path,
                ip_address=request.remote_addr or "",
                user_agent=request.headers.get('User-Agent', ''),
                status='success' if response.status_code < 400 else 'failure'
            )
        
        return response
    
    return audit_logger
