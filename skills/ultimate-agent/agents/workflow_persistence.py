"""
Workflow Persistence - 工作流持久化模块

实现工作流、对话、任务的持久化存储和恢复
支持 SQLite 数据库和 JSON 文件两种存储方式
"""

import json
import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from contextlib import contextmanager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('workflow-persistence')


class WorkflowPersistence:
    """
    工作流持久化系统
    
    功能:
    - SQLite 数据库存储
    - JSON 文件备份
    - 自动保存和恢复
    - 数据清理和归档
    """
    
    def __init__(self, db_path: Optional[Path] = None, 
                 backup_dir: Optional[Path] = None):
        """
        初始化持久化系统
        
        Args:
            db_path: SQLite 数据库路径
            backup_dir: JSON 备份目录
        """
        if db_path is None:
            db_path = Path(__file__).parent.parent / "workflow.db"
        
        if backup_dir is None:
            backup_dir = Path(__file__).parent.parent / "backups"
        
        self.db_path = db_path
        self.backup_dir = backup_dir
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化数据库
        self._init_db()
        
        logger.info(f"持久化系统已初始化：{self.db_path}")
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接上下文管理器"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _init_db(self) -> None:
        """初始化数据库表"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 工作流表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS workflows (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    state TEXT NOT NULL,
                    context TEXT,
                    created_at TEXT NOT NULL,
                    started_at TEXT,
                    completed_at TEXT,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            # 任务表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    workflow_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    assigned_to TEXT,
                    status TEXT NOT NULL,
                    result TEXT,
                    error TEXT,
                    created_at TEXT NOT NULL,
                    started_at TEXT,
                    completed_at TEXT,
                    FOREIGN KEY (workflow_id) REFERENCES workflows(id)
                )
            ''')
            
            # 消息表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL,
                    sender TEXT NOT NULL,
                    receivers TEXT NOT NULL,
                    performative TEXT NOT NULL,
                    content TEXT,
                    timestamp TEXT NOT NULL
                )
            ''')
            
            # 创建索引
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_workflow ON tasks(workflow_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id)')
            
            logger.info("数据库表已初始化")
    
    def save_workflow(self, workflow: Dict[str, Any]) -> bool:
        """保存工作流"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO workflows 
                    (id, name, description, state, context, created_at, started_at, completed_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    workflow['id'],
                    workflow['name'],
                    workflow.get('description', ''),
                    workflow['state'],
                    json.dumps(workflow.get('context', {})),
                    workflow['created_at'],
                    workflow.get('started_at'),
                    workflow.get('completed_at'),
                    datetime.now().isoformat()
                ))
            
            logger.info(f"工作流已保存：{workflow['id']}")
            return True
        except Exception as e:
            logger.error(f"保存工作流失败：{e}")
            return False
    
    def load_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """加载工作流"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM workflows WHERE id = ?', (workflow_id,))
            row = cursor.fetchone()
            
            if row:
                workflow = dict(row)
                if workflow['context']:
                    workflow['context'] = json.loads(workflow['context'])
                return workflow
            return None
    
    def list_workflows(self, limit: int = 50) -> List[Dict[str, Any]]:
        """列出工作流"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM workflows ORDER BY updated_at DESC LIMIT ?', (limit,))
            workflows = []
            for row in cursor.fetchall():
                wf = dict(row)
                if wf['context']:
                    wf['context'] = json.loads(wf['context'])
                workflows.append(wf)
            return workflows
    
    def save_task(self, task: Dict[str, Any]) -> bool:
        """保存任务"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO tasks 
                    (id, workflow_id, title, description, assigned_to, status, result, error, 
                     created_at, started_at, completed_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    task['id'], task['workflow_id'], task['title'],
                    task.get('description', ''), task.get('assigned_to', ''),
                    task['status'], task.get('result'), task.get('error'),
                    task['created_at'], task.get('started_at'), task.get('completed_at')
                ))
            logger.info(f"任务已保存：{task['id']}")
            return True
        except Exception as e:
            logger.error(f"保存任务失败：{e}")
            return False
    
    def get_workflow_tasks(self, workflow_id: str) -> List[Dict[str, Any]]:
        """获取工作流任务"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE workflow_id = ? ORDER BY created_at', (workflow_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def save_message(self, message: Dict[str, Any]) -> bool:
        """保存消息"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO messages (id, conversation_id, sender, receivers, performative, content, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    message['id'], message['conversation_id'], message['sender'],
                    json.dumps(message['receivers']), message['performative'],
                    json.dumps(message.get('content', {})), message['timestamp']
                ))
            logger.info(f"消息已保存：{message['id']}")
            return True
        except Exception as e:
            logger.error(f"保存消息失败：{e}")
            return False
    
    def backup_all(self) -> str:
        """备份所有数据"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = self.backup_dir / f"full_backup_{timestamp}.json"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            data = {'backup_time': datetime.now().isoformat(), 'workflows': [], 'tasks': [], 'messages': []}
            
            cursor.execute('SELECT * FROM workflows')
            for row in cursor.fetchall():
                wf = dict(row)
                if wf['context']:
                    wf['context'] = json.loads(wf['context'])
                data['workflows'].append(wf)
            
            cursor.execute('SELECT * FROM tasks')
            data['tasks'] = [dict(row) for row in cursor.fetchall()]
            
            cursor.execute('SELECT * FROM messages')
            for row in cursor.fetchall():
                msg = dict(row)
                msg['receivers'] = json.loads(msg['receivers'])
                if msg['content']:
                    msg['content'] = json.loads(msg['content'])
                data['messages'].append(msg)
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"完整备份已保存：{backup_file}")
        return str(backup_file)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM workflows')
            workflow_count = cursor.fetchone()[0]
            cursor.execute('SELECT COUNT(*) FROM tasks')
            task_count = cursor.fetchone()[0]
            cursor.execute('SELECT COUNT(*) FROM messages')
            message_count = cursor.fetchone()[0]
            
            return {
                'workflows': workflow_count,
                'tasks': task_count,
                'messages': message_count,
                'database': str(self.db_path)
            }
    
    def get_summary(self) -> str:
        """获取摘要"""
        stats = self.get_stats()
        lines = [
            "Workflow Persistence System",
            "",
            f"**Workflows**: {stats['workflows']}",
            f"**Tasks**: {stats['tasks']}",
            f"**Messages**: {stats['messages']}",
            f"**Database**: {stats['database']}",
            ""
        ]
        return '\n'.join(lines)


def main():
    """测试持久化系统"""
    print("="*60)
    print("Workflow Persistence Test")
    print("="*60)
    
    persistence = WorkflowPersistence()
    
    # 测试 1: 保存工作流
    print("\n1. Save workflow")
    workflow = {
        'id': 'wf_test_001',
        'name': 'Test Workflow',
        'description': 'A test workflow',
        'state': 'running',
        'context': {'key': 'value'},
        'created_at': datetime.now().isoformat(),
        'started_at': datetime.now().isoformat(),
        'completed_at': None,
        'updated_at': datetime.now().isoformat()
    }
    persistence.save_workflow(workflow)
    
    # 测试 2: 加载工作流
    print("\n2. Load workflow")
    loaded = persistence.load_workflow('wf_test_001')
    print(f"   Loaded: {loaded['name']} ({loaded['state']})")
    
    # 测试 3: 保存任务
    print("\n3. Save task")
    task = {
        'id': 'task_001',
        'workflow_id': 'wf_test_001',
        'title': 'Test Task',
        'description': 'A test task',
        'assigned_to': 'executor',
        'status': 'completed',
        'result': 'Success',
        'error': None,
        'created_at': datetime.now().isoformat(),
        'started_at': datetime.now().isoformat(),
        'completed_at': datetime.now().isoformat()
    }
    persistence.save_task(task)
    
    # 测试 4: 获取任务
    print("\n4. Get workflow tasks")
    tasks = persistence.get_workflow_tasks('wf_test_001')
    print(f"   Found {len(tasks)} tasks")
    
    # 测试 5: 备份
    print("\n5. Backup all data")
    backup_file = persistence.backup_all()
    print(f"   Backup: {backup_file}")
    
    # 显示统计
    print("\n" + "="*60)
    print(persistence.get_summary())


if __name__ == '__main__':
    main()
