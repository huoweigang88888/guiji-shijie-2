"""
Heartbeat System - 心跳检查系统

定期检查系统状态、执行维护任务、发现并解决问题
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('heartbeat-system')


class CheckType(Enum):
    """检查类型"""
    SYSTEM = "system"
    MEMORY = "memory"
    TASKS = "tasks"
    MESSAGES = "messages"
    SECURITY = "security"
    PERFORMANCE = "performance"


class SeverityLevel(Enum):
    """严重程度"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class CheckResult:
    """检查结果"""
    check_type: CheckType
    status: str  # ok/warning/error
    message: str
    severity: SeverityLevel
    timestamp: str
    details: Optional[Dict[str, Any]] = None
    recommended_action: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（JSON 可序列化）"""
        return {
            'check_type': self.check_type.value,
            'status': self.status,
            'message': self.message,
            'severity': self.severity.value,
            'timestamp': self.timestamp,
            'details': self.details,
            'recommended_action': self.recommended_action
        }


@dataclass
class HeartbeatReport:
    """心跳报告"""
    timestamp: str
    checks_performed: int
    issues_found: int
    results: List[CheckResult]
    recommended_actions: List[Dict[str, str]]
    summary: str


class HeartbeatSystem:
    """
    心跳检查系统
    
    职责:
    - 定期执行系统健康检查
    - 发现并报告问题
    - 提供修复建议
    - 记录检查历史
    """
    
    def __init__(self, state_dir: Optional[Path] = None):
        """
        初始化心跳系统
        
        Args:
            state_dir: 状态文件目录
        """
        if state_dir is None:
            state_dir = Path(__file__).parent.parent
            
        self.state_dir = state_dir
        self.state_file = state_dir / "heartbeat-state.json"
        self.history_file = state_dir / "heartbeat-history.json"
        
        # 检查处理器
        self.check_handlers: Dict[CheckType, Callable[[], CheckResult]] = {
            CheckType.SYSTEM: self._check_system,
            CheckType.MEMORY: self._check_memory,
            CheckType.TASKS: self._check_tasks,
            CheckType.MESSAGES: self._check_messages,
            CheckType.SECURITY: self._check_security,
            CheckType.PERFORMANCE: self._check_performance,
        }
        
        # 检查历史
        self.history: List[HeartbeatReport] = []
        
        # 加载状态
        self._load_state()
    
    def _load_state(self) -> None:
        """加载状态文件"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    logger.info(f"已加载心跳状态：{self.state_file}")
                    self.last_check = state.get('last_check')
                    self.check_interval = state.get('check_interval', 3600)  # 默认 1 小时
            except Exception as e:
                logger.error(f"加载状态失败：{e}")
                self.last_check = None
                self.check_interval = 3600
        else:
            self.last_check = None
            self.check_interval = 3600
            self._save_state()
    
    def _save_state(self) -> None:
        """保存状态文件"""
        state = {
            'last_check': self.last_check,
            'check_interval': self.check_interval,
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    
    def _check_system(self) -> CheckResult:
        """系统健康检查"""
        try:
            # 检查磁盘空间（简化版）
            workspace = Path(__file__).parent.parent.parent
            if workspace.exists():
                # 模拟检查
                disk_ok = True
                message = "系统运行正常"
                status = "ok"
                severity = SeverityLevel.INFO
            else:
                disk_ok = False
                message = "工作区目录不存在"
                status = "error"
                severity = SeverityLevel.ERROR
            
            return CheckResult(
                check_type=CheckType.SYSTEM,
                status=status,
                message=message,
                severity=severity,
                timestamp=datetime.now().isoformat(),
                details={'workspace': str(workspace), 'disk_ok': disk_ok},
                recommended_action=None if disk_ok else "检查工作区配置"
            )
        except Exception as e:
            return CheckResult(
                check_type=CheckType.SYSTEM,
                status="error",
                message=f"系统检查失败：{e}",
                severity=SeverityLevel.ERROR,
                timestamp=datetime.now().isoformat(),
                recommended_action="查看日志获取详细信息"
            )
    
    def _check_memory(self) -> CheckResult:
        """记忆系统检查"""
        try:
            memory_dir = Path(__file__).parent.parent.parent / "memory"
            memory_file = Path(__file__).parent.parent.parent / "MEMORY.md"
            
            memory_exists = memory_file.exists()
            daily_logs_count = len(list(memory_dir.glob("*.md"))) if memory_dir.exists() else 0
            
            if memory_exists:
                status = "ok"
                severity = SeverityLevel.INFO
                message = f"记忆系统正常 ({daily_logs_count} 篇日志)"
            else:
                status = "warning"
                severity = SeverityLevel.WARNING
                message = "MEMORY.md 不存在"
            
            return CheckResult(
                check_type=CheckType.MEMORY,
                status=status,
                message=message,
                severity=severity,
                timestamp=datetime.now().isoformat(),
                details={
                    'memory_file': str(memory_file),
                    'exists': memory_exists,
                    'daily_logs': daily_logs_count
                },
                recommended_action=None if memory_exists else "创建 MEMORY.md 文件"
            )
        except Exception as e:
            return CheckResult(
                check_type=CheckType.MEMORY,
                status="error",
                message=f"记忆系统检查失败：{e}",
                severity=SeverityLevel.ERROR,
                timestamp=datetime.now().isoformat(),
                recommended_action="检查记忆系统配置"
            )
    
    def _check_tasks(self) -> CheckResult:
        """任务状态检查"""
        try:
            tasks_file = Path(__file__).parent.parent.parent / "todos.json"
            
            if tasks_file.exists():
                with open(tasks_file, 'r', encoding='utf-8') as f:
                    tasks = json.load(f)
                
                pending = len([t for t in tasks.get('todos', []) if not t.get('done')])
                
                if pending == 0:
                    status = "ok"
                    severity = SeverityLevel.INFO
                    message = "所有任务已完成"
                elif pending <= 5:
                    status = "ok"
                    severity = SeverityLevel.INFO
                    message = f"有 {pending} 个待办任务"
                else:
                    status = "warning"
                    severity = SeverityLevel.WARNING
                    message = f"有 {pending} 个待办任务（较多）"
            else:
                status = "info"
                severity = SeverityLevel.INFO
                message = "未发现任务文件"
                pending = 0
            
            return CheckResult(
                check_type=CheckType.TASKS,
                status=status,
                message=message,
                severity=severity,
                timestamp=datetime.now().isoformat(),
                details={'pending_tasks': pending},
                recommended_action="优先处理高优先级任务" if pending > 5 else None
            )
        except Exception as e:
            return CheckResult(
                check_type=CheckType.TASKS,
                status="error",
                message=f"任务检查失败：{e}",
                severity=SeverityLevel.ERROR,
                timestamp=datetime.now().isoformat(),
                recommended_action="检查任务文件配置"
            )
    
    def _check_messages(self) -> CheckResult:
        """消息系统检查"""
        try:
            # 检查消息平台配置
            config_file = Path(__file__).parent / "agents" / "message-aggregator.json"
            
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                connected = config.get('connected_platforms', [])
                
                if len(connected) >= 2:
                    status = "ok"
                    severity = SeverityLevel.INFO
                    message = f"已连接 {len(connected)} 个消息平台"
                elif len(connected) == 1:
                    status = "warning"
                    severity = SeverityLevel.WARNING
                    message = f"仅连接 1 个消息平台：{connected[0]}"
                else:
                    status = "warning"
                    severity = SeverityLevel.WARNING
                    message = "未连接任何消息平台"
            else:
                status = "info"
                severity = SeverityLevel.INFO
                message = "消息聚合器未配置"
            
            return CheckResult(
                check_type=CheckType.MESSAGES,
                status=status,
                message=message,
                severity=severity,
                timestamp=datetime.now().isoformat(),
                details={'config_file': str(config_file)},
                recommended_action="配置消息平台连接" if status == "warning" else None
            )
        except Exception as e:
            return CheckResult(
                check_type=CheckType.MESSAGES,
                status="error",
                message=f"消息系统检查失败：{e}",
                severity=SeverityLevel.ERROR,
                timestamp=datetime.now().isoformat(),
                recommended_action="检查消息系统配置"
            )
    
    def _check_security(self) -> CheckResult:
        """安全检查"""
        try:
            # 检查敏感文件
            sensitive_files = []
            workspace = Path(__file__).parent.parent.parent
            
            for pattern in ['*.key', '*.pem', '*password*', '*secret*', '*token*']:
                for f in workspace.glob(f"**/{pattern}"):
                    if '.git' not in str(f):
                        sensitive_files.append(str(f))
            
            if len(sensitive_files) > 0:
                status = "warning"
                severity = SeverityLevel.WARNING
                message = f"发现 {len(sensitive_files)} 个敏感文件"
                recommended_action = "确保敏感文件已添加到 .gitignore"
            else:
                status = "ok"
                severity = SeverityLevel.INFO
                message = "未发现明显的安全风险"
                recommended_action = None
            
            return CheckResult(
                check_type=CheckType.SECURITY,
                status=status,
                message=message,
                severity=severity,
                timestamp=datetime.now().isoformat(),
                details={'sensitive_files': sensitive_files[:10]},  # 限制数量
                recommended_action=recommended_action
            )
        except Exception as e:
            return CheckResult(
                check_type=CheckType.SECURITY,
                status="error",
                message=f"安全检查失败：{e}",
                severity=SeverityLevel.ERROR,
                timestamp=datetime.now().isoformat(),
                recommended_action="手动检查安全配置"
            )
    
    def _check_performance(self) -> CheckResult:
        """性能检查"""
        try:
            # 检查日志文件大小
            log_files = []
            workspace = Path(__file__).parent.parent.parent
            
            for f in workspace.glob("**/*.log"):
                size_mb = f.stat().st_size / (1024 * 1024)
                if size_mb > 10:
                    log_files.append({'file': str(f), 'size_mb': round(size_mb, 2)})
            
            if len(log_files) > 0:
                status = "warning"
                severity = SeverityLevel.WARNING
                message = f"发现 {len(log_files)} 个大型日志文件"
                recommended_action = "清理或归档大型日志文件"
            else:
                status = "ok"
                severity = SeverityLevel.INFO
                message = "系统性能正常"
                recommended_action = None
            
            return CheckResult(
                check_type=CheckType.PERFORMANCE,
                status=status,
                message=message,
                severity=severity,
                timestamp=datetime.now().isoformat(),
                details={'large_logs': log_files},
                recommended_action=recommended_action
            )
        except Exception as e:
            return CheckResult(
                check_type=CheckType.PERFORMANCE,
                status="error",
                message=f"性能检查失败：{e}",
                severity=SeverityLevel.ERROR,
                timestamp=datetime.now().isoformat(),
                recommended_action="检查系统资源使用情况"
            )
    
    def run_check(self, check_types: Optional[List[CheckType]] = None) -> HeartbeatReport:
        """
        执行心跳检查
        
        Args:
            check_types: 要执行的检查类型列表，None 表示执行所有检查
            
        Returns:
            心跳报告
        """
        logger.info(f"开始心跳检查：{check_types or 'all'}")
        
        if check_types is None:
            check_types = list(self.check_handlers.keys())
        
        results: List[CheckResult] = []
        
        for check_type in check_types:
            if check_type in self.check_handlers:
                try:
                    result = self.check_handlers[check_type]()
                    results.append(result)
                except Exception as e:
                    logger.error(f"检查 {check_type.value} 失败：{e}")
                    results.append(CheckResult(
                        check_type=check_type,
                        status="error",
                        message=f"检查失败：{e}",
                        severity=SeverityLevel.ERROR,
                        timestamp=datetime.now().isoformat()
                    ))
        
        # 生成推荐行动
        recommended_actions = []
        for result in results:
            if result.recommended_action:
                recommended_actions.append({
                    'type': result.check_type.value,
                    'action': result.recommended_action,
                    'severity': result.severity.value
                })
        
        # 生成摘要
        issues_count = len([r for r in results if r.status in ['warning', 'error']])
        if issues_count == 0:
            summary = "✅ 所有检查通过，系统运行正常"
        elif issues_count <= 2:
            summary = f"⚠️ 发现 {issues_count} 个需要注意的问题"
        else:
            summary = f"🚨 发现 {issues_count} 个问题，建议立即处理"
        
        # 创建报告
        report = HeartbeatReport(
            timestamp=datetime.now().isoformat(),
            checks_performed=len(results),
            issues_found=issues_count,
            results=results,
            recommended_actions=recommended_actions,
            summary=summary
        )
        
        # 更新状态
        self.last_check = datetime.now().isoformat()
        self._save_state()
        
        # 保存历史
        self._save_history(report)
        
        logger.info(f"心跳检查完成：{summary}")
        return report
    
    def _save_history(self, report: HeartbeatReport) -> None:
        """保存检查历史"""
        # 加载现有历史
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
                    self.history = [HeartbeatReport(**h) for h in history_data.get('reports', [])]
            except:
                self.history = []
        
        # 添加新报告
        self.history.append(report)
        
        # 限制历史记录数量（保留最近 50 条）
        if len(self.history) > 50:
            self.history = self.history[-50:]
        
        # 保存（手动序列化以避免枚举问题）
        reports_data = []
        for r in self.history:
            reports_data.append({
                'timestamp': r.timestamp,
                'checks_performed': r.checks_performed,
                'issues_found': r.issues_found,
                'results': [result.to_dict() for result in r.results],
                'recommended_actions': r.recommended_actions,
                'summary': r.summary
            })
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump({
                'reports': reports_data,
                'last_updated': datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
    
    def get_summary(self) -> str:
        """获取检查摘要"""
        if not self.last_check:
            return "尚未执行心跳检查"
        
        # 获取最后一次检查
        if self.history:
            last_report = self.history[-1]
            lines = [
                f"💓 心跳检查摘要",
                f"",
                f"**最后检查**: {last_report.timestamp}",
                f"**检查项目**: {last_report.checks_performed}",
                f"**发现问题**: {last_report.issues_found}",
                f"",
                f"{last_report.summary}",
                f""
            ]
            
            if last_report.recommended_actions:
                lines.append("**建议行动**:")
                for action in last_report.recommended_actions:
                    lines.append(f"- [{action['severity'].upper()}] {action['action']}")
            
            return '\n'.join(lines)
        else:
            return f"最后检查：{self.last_check}"
    
    def set_interval(self, seconds: int) -> None:
        """设置检查间隔（秒）"""
        self.check_interval = seconds
        self._save_state()
        logger.info(f"心跳检查间隔已设置为 {seconds} 秒")


def main():
    """测试心跳系统"""
    system = HeartbeatSystem()
    
    print("="*60)
    print("💓 硅基世界 2 - 心跳检查系统")
    print("="*60)
    
    # 执行完整检查
    report = system.run_check()
    
    print(f"\n{report.summary}\n")
    
    print("详细结果:")
    print("-"*60)
    for result in report.results:
        icon = "✅" if result.status == "ok" else "⚠️" if result.status == "warning" else "❌"
        print(f"{icon} [{result.check_type.value}] {result.message}")
        if result.recommended_action:
            print(f"   建议：{result.recommended_action}")
    
    if report.recommended_actions:
        print("\n" + "-"*60)
        print("推荐行动:")
        for action in report.recommended_actions:
            print(f"- [{action['severity']}] {action['action']}")
    
    # 显示历史摘要
    print("\n" + "="*60)
    print(system.get_summary())


if __name__ == '__main__':
    main()
