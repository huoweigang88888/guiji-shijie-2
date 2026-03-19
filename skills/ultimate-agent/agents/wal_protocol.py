"""
WAL Protocol - Write-Ahead Log 协议

在回复用户之前，先将重要信息写入状态文件，防止上下文丢失
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('wal-protocol')


class WALProtocol:
    """WAL 协议实现"""
    
    def __init__(self, state_file: Path):
        self.state_file = state_file
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
    
    def write(self, key: str, value: Any, category: str = "general") -> None:
        """
        写入 WAL
        
        Args:
            key: 键名
            value: 值
            category: 分类
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        entry = {
            'timestamp': timestamp,
            'category': category,
            'key': key,
            'value': value
        }
        
        with open(self.state_file, 'a', encoding='utf-8') as f:
            f.write(f"\n## {timestamp} - {category}/{key}\n")
            f.write(f"{json.dumps(value, ensure_ascii=False, indent=2)}\n")
        
        logger.debug(f"WAL 写入：{category}/{key}")
    
    def read(self, category: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """
        读取 WAL
        
        Args:
            category: 分类过滤
            limit: 限制条数
            
        Returns:
            状态字典
        """
        if not self.state_file.exists():
            return {}
        
        state = {}
        entries = []
        
        with open(self.state_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 简单解析
        current_key = None
        current_value = []
        
        for line in content.split('\n'):
            if line.startswith('## '):
                if current_key:
                    entries.append((current_key, '\n'.join(current_value)))
                current_key = line
                current_value = []
            elif current_key:
                current_value.append(line)
        
        if current_key:
            entries.append((current_key, '\n'.join(current_value)))
        
        # 取最新的 limit 条
        for key, value in entries[-limit:]:
            if category is None or category in key:
                state[key] = value
        
        return state
    
    def prune(self, keep_hours: int = 24) -> int:
        """
        裁剪旧条目
        
        Args:
            keep_hours: 保留小时数
            
        Returns:
            删除的条目数
        """
        # 简化实现：保留最新内容
        if not self.state_file.exists():
            return 0
        
        # 读取当前内容
        content = self.state_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # 保留最新的条目（简单策略：保留后 100 行）
        keep_lines = lines[-100:]
        
        # 写回
        self.state_file.write_text('\n'.join(keep_lines), encoding='utf-8')
        
        removed = len(lines) - len(keep_lines)
        logger.info(f"WAL 裁剪：删除 {removed} 行")
        return removed
    
    def restore(self) -> Dict[str, Any]:
        """
        从 WAL 恢复状态
        
        Returns:
            恢复的状态
        """
        return self.read()
    
    def get_summary(self) -> Dict[str, Any]:
        """获取摘要"""
        if not self.state_file.exists():
            return {'exists': False}
        
        content = self.state_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        return {
            'exists': True,
            'file': str(self.state_file),
            'lines': len(lines),
            'size_bytes': len(content.encode('utf-8'))
        }


def main():
    """测试 WAL 协议"""
    print("="*60)
    print("WAL 协议测试")
    print("="*60)
    
    state_file = Path(__file__).parent.parent / "workspaces" / "main" / "SESSION-STATE.md"
    wal = WALProtocol(state_file)
    
    # 测试写入
    wal.write('test_key', {'data': 'test_value'}, category='test')
    
    # 获取摘要
    summary = wal.get_summary()
    print(f"WAL 文件：{summary['file']}")
    print(f"行数：{summary['lines']}")
    print(f"大小：{summary['size_bytes']} bytes")


if __name__ == '__main__':
    main()
