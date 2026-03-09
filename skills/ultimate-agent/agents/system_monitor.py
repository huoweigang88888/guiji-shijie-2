"""
System Monitor - 系统监控模块

监控系统资源、性能指标、错误日志等
"""

import json
import logging
import subprocess
import platform
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import threading
import time

# 尝试导入 psutil
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    logging.warning("psutil not available, using simplified monitoring")

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('system-monitor')


@dataclass
class SystemMetrics:
    """系统指标"""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    memory_used_gb: float
    memory_total_gb: float
    disk_percent: float
    disk_used_gb: float
    disk_total_gb: float
    network_sent_mb: float
    network_recv_mb: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp,
            'cpu_percent': self.cpu_percent,
            'memory_percent': self.memory_percent,
            'memory_used_gb': self.memory_used_gb,
            'memory_total_gb': self.memory_total_gb,
            'disk_percent': self.disk_percent,
            'disk_used_gb': self.disk_used_gb,
            'disk_total_gb': self.disk_total_gb,
            'network_sent_mb': self.network_sent_mb,
            'network_recv_mb': self.network_recv_mb
        }


class SystemMonitor:
    """
    系统监控器
    
    功能:
    - CPU 使用率监控
    - 内存使用监控
    - 磁盘空间监控
    - 网络流量监控
    - 进程监控
    - 告警通知
    """
    
    def __init__(self, log_dir: Optional[Path] = None, 
                 alert_thresholds: Optional[Dict[str, float]] = None):
        """
        初始化监控器
        
        Args:
            log_dir: 日志目录
            alert_thresholds: 告警阈值
        """
        if log_dir is None:
            log_dir = Path(__file__).parent.parent / "monitor-logs"
        
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 告警阈值
        self.thresholds = alert_thresholds or {
            'cpu_critical': 90.0,
            'cpu_warning': 70.0,
            'memory_critical': 90.0,
            'memory_warning': 70.0,
            'disk_critical': 90.0,
            'disk_warning': 80.0
        }
        
        # 指标历史
        self.metrics_history: List[SystemMetrics] = []
        
        # 告警历史
        self.alerts: List[Dict[str, Any]] = []
        
        # 监控状态
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # 启动监控
        self.start_monitoring()
    
    def get_current_metrics(self) -> SystemMetrics:
        """获取当前系统指标"""
        timestamp = datetime.now().isoformat()
        
        if PSUTIL_AVAILABLE:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 内存
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_gb = memory.used / (1024 ** 3)
            memory_total_gb = memory.total / (1024 ** 3)
            
            # 磁盘
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_used_gb = disk.used / (1024 ** 3)
            disk_total_gb = disk.total / (1024 ** 3)
            
            # 网络
            net = psutil.net_io_counters()
            network_sent_mb = net.bytes_sent / (1024 ** 2)
            network_recv_mb = net.bytes_recv / (1024 ** 2)
        else:
            # 简化版：返回默认值
            cpu_percent = 0.0
            memory_percent = 0.0
            memory_used_gb = 0.0
            memory_total_gb = 0.0
            disk_percent = 0.0
            disk_used_gb = 0.0
            disk_total_gb = 0.0
            network_sent_mb = 0.0
            network_recv_mb = 0.0
        
        return SystemMetrics(
            timestamp=timestamp,
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            memory_used_gb=round(memory_used_gb, 2),
            memory_total_gb=round(memory_total_gb, 2),
            disk_percent=disk_percent,
            disk_used_gb=round(disk_used_gb, 2),
            disk_total_gb=round(disk_total_gb, 2),
            network_sent_mb=round(network_sent_mb, 2),
            network_recv_mb=round(network_recv_mb, 2)
        )
    
    def check_alerts(self, metrics: SystemMetrics) -> List[Dict[str, Any]]:
        """检查告警"""
        alerts = []
        
        # CPU 告警
        if metrics.cpu_percent >= self.thresholds['cpu_critical']:
            alerts.append({
                'level': 'critical',
                'type': 'cpu',
                'message': f'CPU 使用率过高：{metrics.cpu_percent}%',
                'timestamp': metrics.timestamp
            })
        elif metrics.cpu_percent >= self.thresholds['cpu_warning']:
            alerts.append({
                'level': 'warning',
                'type': 'cpu',
                'message': f'CPU 使用率警告：{metrics.cpu_percent}%',
                'timestamp': metrics.timestamp
            })
        
        # 内存告警
        if metrics.memory_percent >= self.thresholds['memory_critical']:
            alerts.append({
                'level': 'critical',
                'type': 'memory',
                'message': f'内存使用率过高：{metrics.memory_percent}%',
                'timestamp': metrics.timestamp
            })
        elif metrics.memory_percent >= self.thresholds['memory_warning']:
            alerts.append({
                'level': 'warning',
                'type': 'memory',
                'message': f'内存使用率警告：{metrics.memory_percent}%',
                'timestamp': metrics.timestamp
            })
        
        # 磁盘告警
        if metrics.disk_percent >= self.thresholds['disk_critical']:
            alerts.append({
                'level': 'critical',
                'type': 'disk',
                'message': f'磁盘空间不足：{metrics.disk_percent}%',
                'timestamp': metrics.timestamp
            })
        elif metrics.disk_percent >= self.thresholds['disk_warning']:
            alerts.append({
                'level': 'warning',
                'type': 'disk',
                'message': f'磁盘空间警告：{metrics.disk_percent}%',
                'timestamp': metrics.timestamp
            })
        
        # 记录告警
        self.alerts.extend(alerts)
        
        # 限制告警数量
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
        
        return alerts
    
    def _monitor_loop(self) -> None:
        """监控循环"""
        while self.monitoring:
            try:
                # 获取指标
                metrics = self.get_current_metrics()
                
                # 记录历史
                self.metrics_history.append(metrics)
                
                # 限制历史记录
                if len(self.metrics_history) > 1000:
                    self.metrics_history = self.metrics_history[-1000:]
                
                # 检查告警
                alerts = self.check_alerts(metrics)
                if alerts:
                    for alert in alerts:
                        logger.warning(f"[{alert['level'].upper()}] {alert['message']}")
                
                # 保存到日志文件（每小时）
                if len(self.metrics_history) % 60 == 0:
                    self._save_metrics_log()
                
                # 等待
                time.sleep(60)  # 每分钟采集一次
                
            except Exception as e:
                logger.error(f"监控循环错误：{e}")
                time.sleep(60)
    
    def _save_metrics_log(self) -> None:
        """保存指标日志"""
        timestamp = datetime.now().strftime('%Y%m%d')
        log_file = self.log_dir / f"metrics_{timestamp}.json"
        
        # 只保存最近的指标
        recent_metrics = self.metrics_history[-60:]  # 最近 1 小时
        
        data = {
            'last_updated': datetime.now().isoformat(),
            'metrics': [m.to_dict() for m in recent_metrics]
        }
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def start_monitoring(self, interval: int = 60) -> None:
        """
        启动监控
        
        Args:
            interval: 采集间隔（秒）
        """
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("系统监控已启动")
    
    def stop_monitoring(self) -> None:
        """停止监控"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("系统监控已停止")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        current = self.get_current_metrics()
        
        return {
            'current': current.to_dict(),
            'monitoring': self.monitoring,
            'history_size': len(self.metrics_history),
            'alerts_count': len(self.alerts)
        }
    
    def get_summary(self) -> str:
        """获取摘要"""
        stats = self.get_stats()
        current = stats['current']
        
        lines = [
            "System Monitor",
            "",
            "**Current Status**:",
            "",
            f"**CPU**: {current['cpu_percent']}%",
            f"**Memory**: {current['memory_percent']}% ({current['memory_used_gb']}/{current['memory_total_gb']} GB)",
            f"**Disk**: {current['disk_percent']}% ({current['disk_used_gb']}/{current['disk_total_gb']} GB)",
            f"**Network**: ↑{current['network_sent_mb']} MB ↓{current['network_recv_mb']} MB",
            "",
            f"**Monitoring**: {'Active' if stats['monitoring'] else 'Stopped'}",
            f"**Alerts**: {stats['alerts_count']}",
            ""
        ]
        
        # 最近告警
        if self.alerts:
            lines.append("**Recent Alerts**:")
            for alert in self.alerts[-5:]:
                lines.append(f"- [{alert['level']}] {alert['message']}")
        
        return '\n'.join(lines)


def main():
    """测试系统监控"""
    print("="*60)
    print("System Monitor Test")
    print("="*60)
    
    monitor = SystemMonitor()
    
    # 等待采集
    print("\n1. Collecting metrics...")
    time.sleep(3)
    
    # 当前状态
    print("\n2. Current metrics")
    stats = monitor.get_stats()
    current = stats['current']
    print(f"   CPU: {current['cpu_percent']}%")
    print(f"   Memory: {current['memory_percent']}%")
    print(f"   Disk: {current['disk_percent']}%")
    
    # 摘要
    print("\n" + "="*60)
    print(monitor.get_summary())
    
    print("\nMonitor is running in background...")


if __name__ == '__main__':
    main()
