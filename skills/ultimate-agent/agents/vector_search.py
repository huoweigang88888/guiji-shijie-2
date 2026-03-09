"""
Vector Search - 向量搜索模块

基于 LanceDB 实现语义搜索能力
支持记忆、文档、知识的向量化存储和检索
"""

import json
import logging
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('vector-search')

# 尝试导入 LanceDB
try:
    import lancedb
    import pyarrow as pa
    LANCEDB_AVAILABLE = True
except ImportError:
    LANCEDB_AVAILABLE = False
    logger.warning("LanceDB 未安装，使用简化版向量搜索")


@dataclass
class VectorDocument:
    """向量文档"""
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class VectorSearch:
    """
    向量搜索系统
    
    功能:
    - 文档向量化存储
    - 语义相似度搜索
    - 记忆检索
    - 相关内容推荐
    """
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        初始化向量搜索
        
        Args:
            db_path: 数据库路径
        """
        if db_path is None:
            db_path = Path(__file__).parent.parent / "vector-db"
        
        self.db_path = db_path
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        self.db = None
        self.tables: Dict[str, Any] = {}
        
        # 简化版词向量映射（当 LanceDB 不可用时）
        self.simple_index: Dict[str, List[VectorDocument]] = {}
        
        # 初始化数据库
        self._init_db()
    
    def _init_db(self) -> None:
        """初始化数据库"""
        if LANCEDB_AVAILABLE:
            try:
                self.db = lancedb.connect(str(self.db_path))
                logger.info(f"LanceDB 已连接：{self.db_path}")
            except Exception as e:
                logger.error(f"LanceDB 初始化失败：{e}")
                self.db = None
        else:
            logger.info("使用简化版向量搜索（无 LanceDB）")
    
    def _generate_embedding(self, text: str) -> List[float]:
        """
        生成文本向量
        
        当 LanceDB 不可用时，使用简化的词袋模型
        """
        if LANCEDB_AVAILABLE and self.db:
            # TODO: 集成真实的嵌入模型（如 sentence-transformers）
            # 目前返回随机向量用于测试
            import random
            random.seed(hash(text) % 2**32)
            return [random.gauss(0, 1) for _ in range(384)]
        else:
            # 简化版：基于词频的向量
            return self._simple_embedding(text)
    
    def _simple_embedding(self, text: str) -> List[float]:
        """简化版词袋向量"""
        # 提取关键词
        words = text.lower().split()
        word_hash = hashlib.md5(text.encode()).hexdigest()
        
        # 生成固定长度的向量（128 维）
        vector = []
        for i in range(128):
            char_val = int(word_hash[i % len(word_hash)], 16)
            vector.append((char_val / 15.0) - 0.5)
        
        return vector
    
    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """计算余弦相似度"""
        if len(v1) != len(v2) or not v1:
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm1 = sum(a * a for a in v1) ** 0.5
        norm2 = sum(b * b for b in v2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def create_table(self, table_name: str, schema: Optional[Any] = None) -> bool:
        """
        创建数据表
        
        Args:
            table_name: 表名
            schema: 表结构（LanceDB Schema）
            
        Returns:
            创建是否成功
        """
        if LANCEDB_AVAILABLE and self.db:
            try:
                # 定义默认 schema
                if schema is None:
                    schema = pa.schema([
                        pa.field("id", pa.string()),
                        pa.field("content", pa.string()),
                        pa.field("metadata", pa.string()),
                        pa.field("embedding", pa.list_(pa.float32(), 384)),
                        pa.field("created_at", pa.string())
                    ])
                
                table = self.db.create_table(table_name, schema=schema)
                self.tables[table_name] = table
                logger.info(f"已创建表：{table_name}")
                return True
            except Exception as e:
                logger.error(f"创建表失败 {table_name}: {e}")
                return False
        else:
            # 简化版：在内存中创建表
            self.simple_index[table_name] = []
            logger.info(f"已创建简化表：{table_name}")
            return True
    
    def add_document(
        self,
        table_name: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        doc_id: Optional[str] = None
    ) -> Optional[str]:
        """
        添加文档到向量库
        
        Args:
            table_name: 表名
            content: 文档内容
            metadata: 元数据
            doc_id: 文档 ID（可选，自动生成）
            
        Returns:
            文档 ID
        """
        if doc_id is None:
            doc_id = f"doc_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hash(content) % 10000}"
        
        # 生成向量
        embedding = self._generate_embedding(content)
        
        doc = VectorDocument(
            id=doc_id,
            content=content,
            metadata=metadata or {},
            embedding=embedding
        )
        
        if LANCEDB_AVAILABLE and self.db and table_name in self.tables:
            try:
                table = self.tables[table_name]
                table.add([{
                    'id': doc.id,
                    'content': doc.content,
                    'metadata': json.dumps(doc.metadata),
                    'embedding': doc.embedding,
                    'created_at': doc.created_at
                }])
                logger.info(f"文档已添加：{doc_id}")
            except Exception as e:
                logger.error(f"添加文档失败：{e}")
                return None
        else:
            # 简化版
            if table_name not in self.simple_index:
                self.create_table(table_name)
            self.simple_index[table_name].append(doc)
            logger.info(f"文档已添加（简化版）：{doc_id}")
        
        return doc_id
    
    def search(
        self,
        table_name: str,
        query: str,
        limit: int = 5,
        threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        语义搜索
        
        Args:
            table_name: 表名
            query: 搜索查询
            limit: 返回结果数量
            threshold: 相似度阈值
            
        Returns:
            搜索结果列表
        """
        logger.info(f"搜索：{query} (limit={limit}, threshold={threshold})")
        
        # 生成查询向量
        query_embedding = self._generate_embedding(query)
        
        results = []
        
        if LANCEDB_AVAILABLE and self.db and table_name in self.tables:
            try:
                table = self.tables[table_name]
                # LanceDB 向量搜索
                result_iter = table.search(query_embedding).limit(limit * 2).to_list()
                
                for item in result_iter:
                    # LanceDB 返回的向量距离需要转换
                    # 这里简化处理
                    results.append({
                        'id': item.get('id', ''),
                        'content': item.get('content', ''),
                        'metadata': json.loads(item.get('metadata', '{}')),
                        'score': 0.8,  # 简化评分
                        'created_at': item.get('created_at', '')
                    })
            except Exception as e:
                logger.error(f"搜索失败：{e}")
        else:
            # 简化版：计算余弦相似度
            if table_name in self.simple_index:
                docs = self.simple_index[table_name]
                scored_docs = []
                
                for doc in docs:
                    if doc.embedding:
                        score = self._cosine_similarity(query_embedding, doc.embedding)
                        if score >= threshold:
                            scored_docs.append({
                                'id': doc.id,
                                'content': doc.content,
                                'metadata': doc.metadata,
                                'score': score,
                                'created_at': doc.created_at
                            })
                
                # 按相似度排序
                scored_docs.sort(key=lambda x: x['score'], reverse=True)
                results = scored_docs[:limit]
        
        logger.info(f"搜索完成：找到 {len(results)} 条结果")
        return results
    
    def add_memory(
        self,
        memory_content: str,
        memory_type: str = "general",
        tags: Optional[List[str]] = None
    ) -> Optional[str]:
        """
        添加记忆到向量库
        
        Args:
            memory_content: 记忆内容
            memory_type: 记忆类型 (general/decision/lesson/etc)
            tags: 标签列表
            
        Returns:
            记忆 ID
        """
        metadata = {
            'type': memory_type,
            'tags': tags or [],
            'source': 'memory'
        }
        
        doc_id = self.add_document(
            table_name="memories",
            content=memory_content,
            metadata=metadata
        )
        
        if doc_id:
            logger.info(f"记忆已存储：{memory_type} - {memory_content[:50]}...")
        
        return doc_id
    
    def search_memories(
        self,
        query: str,
        memory_type: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        搜索记忆
        
        Args:
            query: 搜索查询
            memory_type: 记忆类型过滤
            limit: 返回结果数量
            
        Returns:
            记忆列表
        """
        results = self.search("memories", query, limit=limit * 2)
        
        # 类型过滤
        if memory_type:
            results = [r for r in results if r.get('metadata', {}).get('type') == memory_type]
        
        return results[:limit]
    
    def get_similar_documents(
        self,
        table_name: str,
        doc_id: str,
        limit: int = 3
    ) -> List[Dict[str, Any]]:
        """
        查找相似文档
        
        Args:
            table_name: 表名
            doc_id: 文档 ID
            limit: 返回结果数量
            
        Returns:
            相似文档列表
        """
        # 先获取原文档
        if LANCEDB_AVAILABLE and self.db and table_name in self.tables:
            try:
                table = self.tables[table_name]
                doc = table.search().where(f"id = '{doc_id}'").limit(1).to_list()
                if doc:
                    embedding = doc[0].get('embedding')
                    if embedding:
                        return self.search(table_name, "", limit=limit)
            except:
                pass
        
        # 简化版：不实现
        return []
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = {
            'tables': [],
            'total_documents': 0,
            'lancedb_available': LANCEDB_AVAILABLE
        }
        
        if LANCEDB_AVAILABLE and self.db:
            try:
                stats['tables'] = self.db.table_names()
                for table_name in stats['tables']:
                    table = self.db.open_table(table_name)
                    count = table.count_rows()
                    stats['total_documents'] += count
            except:
                pass
        else:
            stats['tables'] = list(self.simple_index.keys())
            for table_name, docs in self.simple_index.items():
                stats['total_documents'] += len(docs)
        
        return stats
    
    def get_summary(self) -> str:
        """获取摘要"""
        stats = self.get_stats()
        
        lines = [
            f"Vector Search System",
            f"",
            f"**Engine**: {'LanceDB' if stats['lancedb_available'] else 'Simple'}",
            f"**Tables**: {len(stats['tables'])}",
            f"**Total Documents**: {stats['total_documents']}",
            f""
        ]
        
        if stats['tables']:
            lines.append("**Tables**:")
            for table in stats['tables']:
                lines.append(f"- {table}")
        
        return '\n'.join(lines)


def main():
    """测试向量搜索"""
    search = VectorSearch()
    
    print("="*60)
    print("Vector Search System Test")
    print("="*60)
    
    # 创建表
    print("\n1. Creating memories table...")
    search.create_table("memories")
    
    # 添加记忆
    print("\n2. Adding memories...")
    memories = [
        "Python is a high-level programming language",
        "Machine learning is a branch of AI",
        "Deep learning uses neural networks",
        "Natural language processing understands human language",
        "Vector search based on semantic similarity"
    ]
    
    for memory in memories:
        search.add_memory(memory, memory_type="knowledge")
    
    # 搜索
    print("\n3. Searching for 'AI and machine learning'...")
    results = search.search_memories("AI and machine learning", limit=3)
    
    for i, result in enumerate(results, 1):
        print(f"   {i}. [{result['score']:.2f}] {result['content'][:50]}...")
    
    # 统计
    print("\n" + "="*60)
    print(search.get_summary())


if __name__ == '__main__':
    main()
