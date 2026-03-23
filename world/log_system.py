#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志系统 - 硅基世界 2

记录世界的详细日志，用于调试和分析。
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
from enum import Enum


class LogLevel(Enum):
    """日志级别"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class LogManager:
    """日志管理器"""
    
    def __init__(self, log_dir: str = "logs"):
        """
        初始化日志管理器
        
        Args:
            log_dir: 日志目录
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self.logs: List[Dict] = []
        self.max_logs = 10000
        
        # 当前日志文件
        self.current_file = self.log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        
        print(f"📝 日志系统已初始化 (目录：{self.log_dir})")
    
    def log(
        self,
        level: LogLevel,
        message: str,
        source: str = "",
        data: Optional[Dict] = None,
    ):
        """
        记录日志
        
        Args:
            level: 日志级别
            message: 消息
            source: 来源
            data: 附加数据
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level.value,
            "message": message,
            "source": source,
            "data": data or {},
        }
        
        self.logs.append(log_entry)
        
        # 限制日志数量
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)
        
        # 写入文件
        self._write_to_file(log_entry)
        
        # 打印到控制台
        self._print_to_console(log_entry)
    
    def debug(self, message: str, source: str = "", data: Optional[Dict] = None):
        """记录 DEBUG 日志"""
        self.log(LogLevel.DEBUG, message, source, data)
    
    def info(self, message: str, source: str = "", data: Optional[Dict] = None):
        """记录 INFO 日志"""
        self.log(LogLevel.INFO, message, source, data)
    
    def warning(self, message: str, source: str = "", data: Optional[Dict] = None):
        """记录 WARNING 日志"""
        self.log(LogLevel.WARNING, message, source, data)
    
    def error(self, message: str, source: str = "", data: Optional[Dict] = None):
        """记录 ERROR 日志"""
        self.log(LogLevel.ERROR, message, source, data)
    
    def critical(self, message: str, source: str = "", data: Optional[Dict] = None):
        """记录 CRITICAL 日志"""
        self.log(LogLevel.CRITICAL, message, source, data)
    
    def _write_to_file(self, log_entry: Dict):
        """写入文件"""
        with open(self.current_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def _print_to_console(self, log_entry: Dict):
        """打印到控制台"""
        level_colors = {
            LogLevel.DEBUG: "\033[36m",
            LogLevel.INFO: "\033[32m",
            LogLevel.WARNING: "\033[33m",
            LogLevel.ERROR: "\033[31m",
            LogLevel.CRITICAL: "\033[35m",
        }
        
        reset = "\033[0m"
        color = level_colors.get(LogLevel(log_entry["level"]), "")
        
        print(f"{color}[{log_entry['level'].upper()}] {log_entry['timestamp'][:19]} - {log_entry['message']}{reset}")
    
    def get_logs(
        self,
        level: Optional[LogLevel] = None,
        source: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict]:
        """
        获取日志
        
        Args:
            level: 日志级别过滤
            source: 来源过滤
            limit: 返回数量
            
        Returns:
            日志列表
        """
        logs = self.logs
        
        if level:
            logs = [l for l in logs if l["level"] == level.value]
        
        if source:
            logs = [l for l in logs if l["source"] == source]
        
        return logs[-limit:]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total_logs": len(self.logs),
            "by_level": {
                level.value: len([l for l in self.logs if l["level"] == level.value])
                for level in LogLevel
            },
            "log_file": str(self.current_file),
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "recent": self.get_logs(limit=10),
        }


# 单例
_log_manager: Optional[LogManager] = None


def get_log_manager(log_dir: str = "logs") -> LogManager:
    """获取日志管理器单例"""
    global _log_manager
    if _log_manager is None:
        _log_manager = LogManager(log_dir)
    return _log_manager


# 工厂函数
def create_log_manager(log_dir: str = "logs") -> LogManager:
    """创建日志管理器"""
    return LogManager(log_dir)
