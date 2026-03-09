"""
Enhanced Executor - 增强型执行代理

实现真实的任务执行能力：文件操作、命令执行、脚本运行等
"""

import json
import logging
import subprocess
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('enhanced-executor')


class TaskType(Enum):
    """任务类型"""
    FILE_READ = "file_read"
    FILE_WRITE = "file_write"
    FILE_COPY = "file_copy"
    FILE_DELETE = "file_delete"
    DIR_CREATE = "dir_create"
    DIR_LIST = "dir_list"
    COMMAND_RUN = "command_run"
    PYTHON_EXEC = "python_exec"
    WEB_FETCH = "web_fetch"
    CUSTOM = "custom"


class ExecutionStatus(Enum):
    """执行状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class ExecutionResult:
    """执行结果"""
    task_id: str
    task_type: TaskType
    status: ExecutionStatus
    output: Optional[str] = None
    error: Optional[str] = None
    execution_time: float = 0.0
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['task_type'] = self.task_type.value
        d['status'] = self.status.value
        return d


class EnhancedExecutor:
    """
    增强型执行代理
    
    功能:
    - 文件操作（读/写/复制/删除）
    - 目录管理
    - Shell 命令执行
    - Python 代码执行
    - Web 内容抓取
    """
    
    def __init__(self, work_dir: Optional[Path] = None, safe_mode: bool = True):
        """
        初始化执行代理
        
        Args:
            work_dir: 工作目录
            safe_mode: 安全模式（限制危险操作）
        """
        if work_dir is None:
            work_dir = Path(__file__).parent.parent
        
        self.work_dir = work_dir
        self.safe_mode = safe_mode
        
        # 执行历史
        self.execution_history: List[ExecutionResult] = []
        
        # 任务处理器
        self.handlers: Dict[TaskType, Callable] = {
            TaskType.FILE_READ: self._execute_file_read,
            TaskType.FILE_WRITE: self._execute_file_write,
            TaskType.FILE_COPY: self._execute_file_copy,
            TaskType.FILE_DELETE: self._execute_file_delete,
            TaskType.DIR_CREATE: self._execute_dir_create,
            TaskType.DIR_LIST: self._execute_dir_list,
            TaskType.COMMAND_RUN: self._execute_command,
            TaskType.PYTHON_EXEC: self._execute_python,
            TaskType.WEB_FETCH: self._execute_web_fetch,
        }
        
        logger.info(f"执行代理已初始化，工作目录：{self.work_dir}")
        if self.safe_mode:
            logger.info("安全模式已启用")
    
    def execute(self, task_type: TaskType, params: Dict[str, Any], 
                timeout: int = 30) -> ExecutionResult:
        """
        执行任务
        
        Args:
            task_type: 任务类型
            params: 任务参数
            timeout: 超时时间（秒）
            
        Returns:
            执行结果
        """
        import uuid
        import time
        
        task_id = f"exec_{uuid.uuid4().hex[:8]}"
        start_time = time.time()
        
        logger.info(f"执行任务：{task_type.value} (ID: {task_id})")
        
        # 创建结果对象
        result = ExecutionResult(
            task_id=task_id,
            task_type=task_type,
            status=ExecutionStatus.RUNNING
        )
        
        try:
            # 查找处理器
            handler = self.handlers.get(task_type)
            if not handler:
                raise ValueError(f"未知任务类型：{task_type}")
            
            # 执行任务
            output = handler(params)
            
            result.status = ExecutionStatus.COMPLETED
            result.output = output
            
        except subprocess.TimeoutExpired:
            result.status = ExecutionStatus.TIMEOUT
            result.error = f"任务超时（{timeout}秒）"
        except Exception as e:
            result.status = ExecutionStatus.FAILED
            result.error = str(e)
            logger.error(f"任务执行失败：{e}")
        
        # 记录执行时间
        result.execution_time = round(time.time() - start_time, 3)
        
        # 添加到历史
        self.execution_history.append(result)
        
        logger.info(f"任务完成：{task_id} - {result.status.value}")
        return result
    
    def _validate_path(self, path: Path) -> bool:
        """验证路径安全性"""
        if not self.safe_mode:
            return True
        
        # 如果是相对路径，转换为相对于工作目录的绝对路径
        if not path.is_absolute():
            path = self.work_dir / path
        
        # 确保路径在工作目录内
        try:
            resolved = path.resolve()
            work_resolved = self.work_dir.resolve()
            return str(resolved).startswith(str(work_resolved))
        except:
            return False
    
    def _execute_file_read(self, params: Dict[str, Any]) -> str:
        """读取文件"""
        file_path = Path(params.get('path', ''))
        
        if not self._validate_path(file_path):
            raise PermissionError(f"路径不允许访问：{file_path}")
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在：{file_path}")
        
        content = file_path.read_text(encoding=params.get('encoding', 'utf-8'))
        return content
    
    def _execute_file_write(self, params: Dict[str, Any]) -> str:
        """写入文件"""
        file_path = Path(params.get('path', ''))
        content = params.get('content', '')
        
        if not self._validate_path(file_path):
            raise PermissionError(f"路径不允许访问：{file_path}")
        
        # 创建父目录
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_path.write_text(content, encoding=params.get('encoding', 'utf-8'))
        return f"文件已写入：{file_path}"
    
    def _execute_file_copy(self, params: Dict[str, Any]) -> str:
        """复制文件"""
        src = Path(params.get('src', ''))
        dst = Path(params.get('dst', ''))
        
        if not self._validate_path(src) or not self._validate_path(dst):
            raise PermissionError("路径不允许访问")
        
        if not src.exists():
            raise FileNotFoundError(f"源文件不存在：{src}")
        
        shutil.copy2(src, dst)
        return f"文件已复制：{src} -> {dst}"
    
    def _execute_file_delete(self, params: Dict[str, Any]) -> str:
        """删除文件"""
        file_path = Path(params.get('path', ''))
        
        if not self._validate_path(file_path):
            raise PermissionError(f"路径不允许访问：{file_path}")
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在：{file_path}")
        
        file_path.unlink()
        return f"文件已删除：{file_path}"
    
    def _execute_dir_create(self, params: Dict[str, Any]) -> str:
        """创建目录"""
        dir_path = Path(params.get('path', ''))
        
        if not self._validate_path(dir_path):
            raise PermissionError(f"路径不允许访问：{dir_path}")
        
        dir_path.mkdir(parents=True, exist_ok=True)
        return f"目录已创建：{dir_path}"
    
    def _execute_dir_list(self, params: Dict[str, Any]) -> str:
        """列出目录内容"""
        dir_path = Path(params.get('path', ''))
        
        if not self._validate_path(dir_path):
            raise PermissionError(f"路径不允许访问：{dir_path}")
        
        if not dir_path.exists():
            raise FileNotFoundError(f"目录不存在：{dir_path}")
        
        items = []
        for item in dir_path.iterdir():
            item_type = "dir" if item.is_dir() else "file"
            items.append(f"{item_type}: {item.name}")
        
        return '\n'.join(items)
    
    def _execute_command(self, params: Dict[str, Any]) -> str:
        """执行 Shell 命令"""
        command = params.get('command', '')
        cwd = params.get('cwd', str(self.work_dir))
        
        if self.safe_mode:
            # 安全模式：限制危险命令
            dangerous_commands = ['rm -rf', 'del /f', 'format', 'mkfs']
            if any(cmd in command for cmd in dangerous_commands):
                raise PermissionError("命令不被允许（安全模式）")
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=params.get('timeout', 30),
            cwd=cwd
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\n[STDERR]\n{result.stderr}"
        
        return output
    
    def _execute_python(self, params: Dict[str, Any]) -> str:
        """执行 Python 代码"""
        code = params.get('code', '')
        cwd = params.get('cwd', str(self.work_dir))
        
        # 创建临时文件
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            result = subprocess.run(
                ['python', temp_file],
                capture_output=True,
                text=True,
                timeout=params.get('timeout', 30),
                cwd=cwd
            )
            
            output = result.stdout
            if result.stderr:
                output += f"\n[STDERR]\n{result.stderr}"
            
            return output
        finally:
            # 清理临时文件
            Path(temp_file).unlink()
    
    def _execute_web_fetch(self, params: Dict[str, Any]) -> str:
        """抓取网页内容"""
        url = params.get('url', '')
        
        if not url:
            raise ValueError("URL 不能为空")
        
        # 使用 OpenClaw web_fetch 工具
        # 这里简化实现，实际应该调用工具
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=30) as response:
                content = response.read().decode('utf-8', errors='ignore')
                return content[:5000]  # 限制返回长度
        except Exception as e:
            raise Exception(f"网页抓取失败：{e}")
    
    def execute_batch(self, tasks: List[Dict[str, Any]]) -> List[ExecutionResult]:
        """
        批量执行任务
        
        Args:
            tasks: 任务列表，每项包含 task_type 和 params
            
        Returns:
            执行结果列表
        """
        results = []
        
        for i, task in enumerate(tasks):
            task_type = TaskType(task.get('task_type', 'custom'))
            params = task.get('params', {})
            
            result = self.execute(task_type, params)
            results.append(result)
            
            # 如果失败且设置了 stop_on_error，则停止
            if result.status == ExecutionStatus.FAILED and task.get('stop_on_error'):
                logger.warning(f"批量执行在任务 {i} 处停止")
                break
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        status_counts = {}
        for result in self.execution_history:
            status = result.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            'total_executions': len(self.execution_history),
            'status_counts': status_counts,
            'work_dir': str(self.work_dir),
            'safe_mode': self.safe_mode
        }
    
    def get_summary(self) -> str:
        """获取摘要"""
        stats = self.get_stats()
        
        lines = [
            f"Enhanced Executor Agent",
            f"",
            f"**Total Executions**: {stats['total_executions']}",
            f"**Work Directory**: {stats['work_dir']}",
            f"**Safe Mode**: {stats['safe_mode']}",
            f""
        ]
        
        if stats['status_counts']:
            lines.append("**Execution Status**:")
            for status, count in stats['status_counts'].items():
                lines.append(f"- {status}: {count}")
        
        return '\n'.join(lines)


def main():
    """测试执行代理"""
    print("="*60)
    print("Enhanced Executor Agent Test")
    print("="*60)
    
    executor = EnhancedExecutor(safe_mode=True)
    
    # 测试 1: 创建目录
    print("\n1. Create directory test_dir")
    result = executor.execute(TaskType.DIR_CREATE, {'path': 'test_dir'})
    print(f"   Status: {result.status.value}")
    print(f"   Output: {result.output}")
    
    # 测试 2: 写入文件
    print("\n2. Write to file")
    result = executor.execute(TaskType.FILE_WRITE, {
        'path': 'test_dir/test.txt',
        'content': 'Hello from Enhanced Executor!'
    })
    print(f"   Status: {result.status.value}")
    print(f"   Output: {result.output}")
    
    # 测试 3: 读取文件
    print("\n3. Read from file")
    result = executor.execute(TaskType.FILE_READ, {
        'path': 'test_dir/test.txt'
    })
    print(f"   Status: {result.status.value}")
    print(f"   Output: {result.output}")
    
    # 测试 4: 列出目录
    print("\n4. List directory")
    result = executor.execute(TaskType.DIR_LIST, {
        'path': 'test_dir'
    })
    print(f"   Status: {result.status.value}")
    print(f"   Output:\n{result.output}")
    
    # 测试 5: 执行命令
    print("\n5. Run command")
    result = executor.execute(TaskType.COMMAND_RUN, {
        'command': 'python --version'
    })
    print(f"   Status: {result.status.value}")
    print(f"   Output: {result.output}")
    
    # 测试 6: 批量执行
    print("\n6. Batch execution")
    tasks = [
        {'task_type': 'file_write', 'params': {'path': 'test_dir/batch.txt', 'content': 'Batch 1'}},
        {'task_type': 'file_read', 'params': {'path': 'test_dir/batch.txt'}},
    ]
    results = executor.execute_batch(tasks)
    print(f"   Executed: {len(results)} tasks")
    
    # 显示统计
    print("\n" + "="*60)
    print(executor.get_summary())


if __name__ == '__main__':
    main()
