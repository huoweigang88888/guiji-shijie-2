"""
Self Improver - 自我改进系统

从错误中学习，分析模式，提出改进建议，安全地实施改进
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('self-improver')


class ImprovementType(Enum):
    """改进类型"""
    BUG_FIX = "bug_fix"
    PERFORMANCE = "performance"
    FEATURE = "feature"
    REFACTOR = "refactor"
    DOCUMENTATION = "documentation"
    SECURITY = "security"


class ConfidenceLevel(Enum):
    """置信度级别"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RiskLevel(Enum):
    """风险级别"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Lesson:
    """学习到的教训"""
    id: str
    title: str
    description: str
    category: str
    source: str  # 错误/事件来源
    learned_at: str
    applied: bool = False
    applied_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Improvement:
    """改进建议"""
    id: str
    title: str
    description: str
    improvement_type: ImprovementType
    confidence: ConfidenceLevel
    risk: RiskLevel
    estimated_value: int  # 1-10 价值评分
    estimated_effort: int  # 1-10 工作量评分
    created_at: str
    status: str = "pending"  # pending/approved/rejected/implemented
    implemented_at: Optional[str] = None
    related_lessons: List[str] = None
    
    def __post_init__(self):
        if self.related_lessons is None:
            self.related_lessons = []
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['improvement_type'] = self.improvement_type.value
        d['confidence'] = self.confidence.value
        d['risk'] = self.risk.value
        return d


@dataclass
class ErrorRecord:
    """错误记录"""
    id: str
    error_type: str
    error_message: str
    context: Dict[str, Any]
    timestamp: str
    resolved: bool = False
    resolution: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SelfImprover:
    """
    自我改进系统
    
    职责:
    - 记录和分析错误
    - 从经验中学习
    - 生成改进建议
    - 评估改进风险
    - 安全地实施改进
    """
    
    def __init__(self, state_dir: Optional[Path] = None):
        """
        初始化自我改进器
        
        Args:
            state_dir: 状态文件目录
        """
        if state_dir is None:
            state_dir = Path(__file__).parent.parent
        
        self.state_dir = state_dir
        self.errors_file = state_dir / "errors.json"
        self.lessons_file = state_dir / "lessons.json"
        self.improvements_file = state_dir / "improvements.json"
        
        # 数据
        self.errors: List[ErrorRecord] = []
        self.lessons: Dict[str, Lesson] = {}
        self.improvements: Dict[str, Improvement] = {}
        
        # 改进实施回调
        self.implementation_handlers: Dict[str, callable] = {}
        
        # 加载状态
        self._load_state()
    
    def _load_state(self) -> None:
        """加载状态文件"""
        # 加载错误记录
        if self.errors_file.exists():
            try:
                with open(self.errors_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.errors = [
                        ErrorRecord(**e) for e in data.get('errors', [])
                    ]
                logger.info(f"已加载 {len(self.errors)} 条错误记录")
            except:
                self.errors = []
        else:
            self.errors = []
        
        # 加载教训
        if self.lessons_file.exists():
            try:
                with open(self.lessons_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.lessons = {
                        k: Lesson(**v) for k, v in data.get('lessons', {}).items()
                    }
                logger.info(f"已加载 {len(self.lessons)} 条教训")
            except:
                self.lessons = {}
        else:
            self.lessons = {}
        
        # 加载改进建议
        if self.improvements_file.exists():
            try:
                with open(self.improvements_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.improvements = {
                        k: Improvement(**v) for k, v in data.get('improvements', {}).items()
                    }
                logger.info(f"已加载 {len(self.improvements)} 条改进建议")
            except:
                self.improvements = {}
        else:
            self.improvements = {}
    
    def _save_state(self) -> None:
        """保存状态文件"""
        # 保存错误记录（限制数量）
        if len(self.errors) > 100:
            self.errors = self.errors[-100:]
        
        with open(self.errors_file, 'w', encoding='utf-8') as f:
            json.dump({
                'errors': [e.to_dict() for e in self.errors],
                'last_updated': datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        
        # 保存教训
        with open(self.lessons_file, 'w', encoding='utf-8') as f:
            json.dump({
                'lessons': {k: v.to_dict() for k, v in self.lessons.items()},
                'last_updated': datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        
        # 保存改进建议
        with open(self.improvements_file, 'w', encoding='utf-8') as f:
            json.dump({
                'improvements': {k: v.to_dict() for k, v in self.improvements.items()},
                'last_updated': datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
    
    def record_error(
        self,
        error_type: str,
        error_message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> ErrorRecord:
        """
        记录错误
        
        Args:
            error_type: 错误类型
            error_message: 错误信息
            context: 上下文信息
            
        Returns:
            错误记录对象
        """
        error_id = f"err_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.errors)}"
        
        error = ErrorRecord(
            id=error_id,
            error_type=error_type,
            error_message=error_message,
            context=context or {},
            timestamp=datetime.now().isoformat()
        )
        
        self.errors.append(error)
        self._save_state()
        
        logger.info(f"已记录错误：{error_type} - {error_message[:50]}...")
        
        # 尝试从错误中学习
        self._learn_from_error(error)
        
        return error
    
    def _learn_from_error(self, error: ErrorRecord) -> Optional[Lesson]:
        """从错误中学习"""
        # 分析错误类型，生成教训
        lesson_title, lesson_description, category = self._analyze_error(error)
        
        if not lesson_title:
            return None
        
        lesson_id = f"lesson_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.lessons)}"
        
        lesson = Lesson(
            id=lesson_id,
            title=lesson_title,
            description=lesson_description,
            category=category,
            source=f"error:{error.id}",
            learned_at=datetime.now().isoformat()
        )
        
        self.lessons[lesson_id] = lesson
        self._save_state()
        
        logger.info(f"从错误中学到：{lesson_title}")
        
        # 基于教训生成改进建议
        self._generate_improvement_from_lesson(lesson)
        
        return lesson
    
    def _analyze_error(self, error: ErrorRecord) -> Tuple[Optional[str], Optional[str], str]:
        """
        分析错误，提取教训
        
        Returns:
            (lesson_title, lesson_description, category)
        """
        error_type = error.error_type.lower()
        error_msg = error.error_message.lower()
        
        # 简单规则匹配（可扩展为 AI 分析）
        if 'file' in error_type or 'no such file' in error_msg:
            return (
                "文件操作前检查文件存在性",
                "在执行文件操作前，应该先检查文件是否存在，避免 FileNotFoundError",
                "error_handling"
            )
        elif 'permission' in error_type or 'access' in error_msg:
            return (
                "处理权限相关异常",
                "文件操作可能遇到权限问题，需要适当的错误处理和用户提示",
                "security"
            )
        elif 'json' in error_type or 'parse' in error_msg:
            return (
                "JSON 解析需要异常处理",
                "解析外部数据时，应该使用 try-except 处理格式错误",
                "data_validation"
            )
        elif 'network' in error_type or 'timeout' in error_msg or 'connection' in error_msg:
            return (
                "网络操作需要超时和重试机制",
                "网络请求应该设置超时时间，并实现重试逻辑处理临时故障",
                "reliability"
            )
        elif 'key' in error_msg or 'index' in error_msg:
            return (
                "访问字典和列表前检查键/索引存在性",
                "使用 get() 方法或先检查键是否存在，避免 KeyError/IndexError",
                "error_handling"
            )
        else:
            # 通用教训
            return (
                f"处理 {error.error_type} 类型错误",
                f"错误信息：{error.error_message}。需要添加适当的异常处理逻辑。",
                "general"
            )
    
    def _generate_improvement_from_lesson(self, lesson: Lesson) -> Optional[Improvement]:
        """基于教训生成改进建议"""
        # 根据教训类别生成改进
        category = lesson.category
        
        if category == 'error_handling':
            improvement = Improvement(
                id=f"imp_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.improvements)}",
                title="增强错误处理机制",
                description="在关键代码路径添加 try-except 块，记录详细错误信息",
                improvement_type=ImprovementType.BUG_FIX,
                confidence=ConfidenceLevel.HIGH,
                risk=RiskLevel.LOW,
                estimated_value=7,
                estimated_effort=3,
                created_at=datetime.now().isoformat(),
                related_lessons=[lesson.id]
            )
        elif category == 'security':
            improvement = Improvement(
                id=f"imp_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.improvements)}",
                title="加强安全检查和权限验证",
                description="在敏感操作前添加权限检查和用户确认",
                improvement_type=ImprovementType.SECURITY,
                confidence=ConfidenceLevel.HIGH,
                risk=RiskLevel.MEDIUM,
                estimated_value=9,
                estimated_effort=4,
                created_at=datetime.now().isoformat(),
                related_lessons=[lesson.id]
            )
        elif category == 'reliability':
            improvement = Improvement(
                id=f"imp_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.improvements)}",
                title="实现重试机制和超时处理",
                description="为网络请求和外部依赖添加重试逻辑和超时控制",
                improvement_type=ImprovementType.PERFORMANCE,
                confidence=ConfidenceLevel.MEDIUM,
                risk=RiskLevel.LOW,
                estimated_value=6,
                estimated_effort=5,
                created_at=datetime.now().isoformat(),
                related_lessons=[lesson.id]
            )
        else:
            improvement = Improvement(
                id=f"imp_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.improvements)}",
                title=f"改进：{lesson.title}",
                description=lesson.description,
                improvement_type=ImprovementType.REFACTOR,
                confidence=ConfidenceLevel.MEDIUM,
                risk=RiskLevel.LOW,
                estimated_value=5,
                estimated_effort=3,
                created_at=datetime.now().isoformat(),
                related_lessons=[lesson.id]
            )
        
        self.improvements[improvement.id] = improvement
        self._save_state()
        
        logger.info(f"生成改进建议：{improvement.title}")
        return improvement
    
    def approve_improvement(self, improvement_id: str) -> bool:
        """批准改进建议"""
        if improvement_id not in self.improvements:
            logger.error(f"改进建议不存在：{improvement_id}")
            return False
        
        improvement = self.improvements[improvement_id]
        improvement.status = 'approved'
        
        self._save_state()
        logger.info(f"已批准改进：{improvement.title}")
        return True
    
    def reject_improvement(self, improvement_id: str) -> bool:
        """拒绝改进建议"""
        if improvement_id not in self.improvements:
            logger.error(f"改进建议不存在：{improvement_id}")
            return False
        
        improvement = self.improvements[improvement_id]
        improvement.status = 'rejected'
        
        self._save_state()
        logger.info(f"已拒绝改进：{improvement.title}")
        return True
    
    def implement_improvement(self, improvement_id: str) -> bool:
        """
        实施改进
        
        Args:
            improvement_id: 改进 ID
            
        Returns:
            实施是否成功
        """
        if improvement_id not in self.improvements:
            logger.error(f"改进建议不存在：{improvement_id}")
            return False
        
        improvement = self.improvements[improvement_id]
        
        if improvement.status not in ['pending', 'approved']:
            logger.warning(f"改进状态不允许实施：{improvement.status}")
            return False
        
        # 检查风险级别
        if improvement.risk == RiskLevel.CRITICAL:
            logger.error(f"高风险改进需要人工审核：{improvement.title}")
            return False
        
        logger.info(f"开始实施改进：{improvement.title}")
        
        try:
            # TODO: 实际实施改进逻辑
            # 目前仅标记为已实施
            
            improvement.status = 'implemented'
            improvement.implemented_at = datetime.now().isoformat()
            
            # 标记相关教训为已应用
            for lesson_id in improvement.related_lessons:
                if lesson_id in self.lessons:
                    self.lessons[lesson_id].applied = True
                    self.lessons[lesson_id].applied_at = datetime.now().isoformat()
            
            self._save_state()
            logger.info(f"改进已实施：{improvement.title}")
            return True
            
        except Exception as e:
            logger.error(f"改进实施失败：{improvement.title} - {e}")
            return False
    
    def get_pending_improvements(self) -> List[Improvement]:
        """获取待处理的改进建议"""
        return [
            imp for imp in self.improvements.values()
            if imp.status == 'pending'
        ]
    
    def get_high_priority_improvements(self) -> List[Improvement]:
        """获取高优先级改进建议"""
        pending = self.get_pending_improvements()
        # 按价值/努力比排序
        pending.sort(
            key=lambda i: (i.estimated_value / max(i.estimated_effort, 1)),
            reverse=True
        )
        return pending
    
    def get_summary(self) -> str:
        """获取自我改进摘要"""
        lines = [
            f"🧠 自我改进系统摘要",
            f"",
            f"**记录错误**: {len(self.errors)}",
            f"**学到教训**: {len(self.lessons)}",
            f"**改进建议**: {len(self.improvements)}",
            f""
        ]
        
        # 待处理改进
        pending = self.get_pending_improvements()
        if pending:
            lines.append(f"**待处理改进 ({len(pending)})**:")
            for imp in pending[:5]:  # 最多显示 5 个
                risk_icon = "🔴" if imp.risk == RiskLevel.HIGH else "🟠" if imp.risk == RiskLevel.MEDIUM else "🟢"
                value_effort = f"价值:{imp.estimated_value}/努力:{imp.estimated_effort}"
                lines.append(f"- {risk_icon} {imp.title} ({value_effort})")
            if len(pending) > 5:
                lines.append(f"- ... 还有 {len(pending) - 5} 个改进")
        else:
            lines.append("**待处理改进**: 无")
        
        # 高优先级推荐
        high_priority = self.get_high_priority_improvements()[:3]
        if high_priority:
            lines.append("")
            lines.append("**推荐优先实施**:")
            for i, imp in enumerate(high_priority, 1):
                lines.append(f"  {i}. {imp.title}")
        
        return '\n'.join(lines)
    
    def analyze_patterns(self) -> Dict[str, Any]:
        """分析错误模式"""
        if not self.errors:
            return {'message': '没有足够的错误数据'}
        
        # 统计错误类型
        error_types = {}
        for error in self.errors:
            error_types[error.error_type] = error_types.get(error.error_type, 0) + 1
        
        # 找出最常见的错误
        sorted_types = sorted(error_types.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'total_errors': len(self.errors),
            'error_types': dict(sorted_types[:10]),
            'most_common': sorted_types[0] if sorted_types else None,
            'recent_trend': self._analyze_trend()
        }
    
    def _analyze_trend(self) -> str:
        """分析错误趋势"""
        if len(self.errors) < 2:
            return "数据不足"
        
        # 比较最近 10 条和之前 10 条
        recent = self.errors[-10:]
        older = self.errors[-20:-10] if len(self.errors) >= 20 else self.errors[:-10]
        
        if not older:
            return "数据不足"
        
        recent_count = len(recent)
        older_count = len(older)
        
        if recent_count < older_count:
            return "错误数量呈下降趋势 ✅"
        elif recent_count > older_count:
            return "错误数量呈上升趋势 ⚠️"
        else:
            return "错误数量保持稳定"


def main():
    """测试自我改进系统"""
    improver = SelfImprover()
    
    print("="*60)
    print("🧠 硅基世界 2 - 自我改进系统")
    print("="*60)
    
    # 模拟记录错误
    print("\n1. 记录错误...")
    improver.record_error(
        'FileNotFoundError',
        '[Errno 2] No such file or directory: config.json',
        {'operation': 'read', 'path': 'config.json'}
    )
    
    improver.record_error(
        'JSONDecodeError',
        'Expecting value: line 1 column 1 (char 0)',
        {'operation': 'parse', 'source': 'api_response'}
    )
    
    improver.record_error(
        'TimeoutError',
        'Connection timed out after 30s',
        {'operation': 'http_request', 'url': 'https://api.example.com'}
    )
    
    # 显示分析
    print("\n2. 错误模式分析:")
    patterns = improver.analyze_patterns()
    print(f"   总错误数：{patterns.get('total_errors', 0)}")
    print(f"   趋势：{patterns.get('recent_trend', 'N/A')}")
    
    # 显示摘要
    print("\n" + "="*60)
    print(improver.get_summary())


if __name__ == '__main__':
    main()
