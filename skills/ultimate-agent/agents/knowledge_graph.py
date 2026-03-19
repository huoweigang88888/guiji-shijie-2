"""
Knowledge Graph - 知识图谱模块

基于 Git-Notes 实现概念关联和知识网络
支持知识节点管理、关系建立、路径查询
"""

import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('knowledge-graph')


class RelationType(Enum):
    """关系类型"""
    IS_A = "is_a"  # 是一种
    HAS_PART = "has_part"  # 有部分
    RELATED_TO = "related_to"  # 相关
    CAUSES = "causes"  # 导致
    USED_FOR = "used_for"  # 用于
    EXAMPLE_OF = "example_of"  # 示例
    OPPOSITE_OF = "opposite_of"  # 相反
    SIMILAR_TO = "similar_to"  # 相似


@dataclass
class KnowledgeNode:
    """知识节点"""
    id: str
    title: str
    description: str
    category: str
    tags: List[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        now = datetime.now().isoformat()
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = now
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KnowledgeNode':
        return cls(**data)


@dataclass
class KnowledgeRelation:
    """知识关系"""
    id: str
    from_node: str
    to_node: str
    relation_type: RelationType
    description: str = ""
    created_at: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['relation_type'] = self.relation_type.value
        return d
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KnowledgeRelation':
        data['relation_type'] = RelationType(data['relation_type'])
        return cls(**data)


class KnowledgeGraph:
    """
    知识图谱系统
    
    功能:
    - 知识节点管理
    - 关系建立和查询
    - 路径发现
    - 知识推荐
    """
    
    def __init__(self, repo_path: Optional[Path] = None):
        """
        初始化知识图谱
        
        Args:
            repo_path: Git 仓库路径
        """
        if repo_path is None:
            repo_path = Path(__file__).parent.parent
        
        self.repo_path = repo_path
        self.graph_file = repo_path / "knowledge-graph.json"
        
        # 图谱数据
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.relations: Dict[str, KnowledgeRelation] = {}
        
        # Git notes 可用性
        self.git_notes_available = self._check_git_notes()
        
        # 加载图谱
        self._load_graph()
    
    def _check_git_notes(self) -> bool:
        """检查 Git Notes 是否可用"""
        try:
            # 使用 'git notes list' 而不是 '--help'（--help 会打开 HTML 文档）
            result = subprocess.run(
                ['git', 'notes', 'list'],
                capture_output=True,
                timeout=5,
                cwd=str(self.repo_path)
            )
            # returncode == 0 表示 Git Notes 可用
            return result.returncode == 0
        except:
            logger.warning("Git Notes 不可用，使用本地存储")
            return False
    
    def _load_graph(self) -> None:
        """加载图谱数据"""
        if self.graph_file.exists():
            try:
                with open(self.graph_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.nodes = {
                    k: KnowledgeNode.from_dict(v)
                    for k, v in data.get('nodes', {}).items()
                }
                self.relations = {
                    k: KnowledgeRelation.from_dict(v)
                    for k, v in data.get('relations', {}).items()
                }
                
                logger.info(f"已加载知识图谱：{len(self.nodes)} 节点，{len(self.relations)} 关系")
            except Exception as e:
                logger.error(f"加载图谱失败：{e}")
                self.nodes = {}
                self.relations = {}
        else:
            logger.info("创建新知识图谱")
    
    def _save_graph(self) -> None:
        """保存图谱数据"""
        data = {
            'nodes': {k: v.to_dict() for k, v in self.nodes.items()},
            'relations': {k: v.to_dict() for k, v in self.relations.items()},
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.graph_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # 如果 Git Notes 可用，同步到 Git
        if self.git_notes_available:
            self._sync_to_git_notes()
    
    def _sync_to_git_notes(self) -> None:
        """同步到 Git Notes"""
        try:
            # 将图谱数据添加到 Git notes
            data = json.dumps({
                'nodes': len(self.nodes),
                'relations': len(self.relations),
                'updated': datetime.now().isoformat()
            }, ensure_ascii=False)
            
            subprocess.run(
                ['git', 'notes', 'add', '-f', '-m', data],
                cwd=str(self.repo_path),
                capture_output=True,
                timeout=10
            )
            logger.info("已同步到 Git Notes")
        except Exception as e:
            logger.error(f"Git Notes 同步失败：{e}")
    
    def add_node(
        self,
        title: str,
        description: str,
        category: str = "general",
        tags: Optional[List[str]] = None,
        node_id: Optional[str] = None
    ) -> str:
        """
        添加知识节点
        
        Args:
            title: 节点标题
            description: 节点描述
            category: 类别
            tags: 标签列表
            node_id: 节点 ID（可选，自动生成）
            
        Returns:
            节点 ID
        """
        if node_id is None:
            node_id = f"node_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hash(title) % 10000}"
        
        node = KnowledgeNode(
            id=node_id,
            title=title,
            description=description,
            category=category,
            tags=tags or []
        )
        
        self.nodes[node_id] = node
        self._save_graph()
        
        logger.info(f"已添加节点：{title} ({node_id})")
        return node_id
    
    def add_relation(
        self,
        from_node_id: str,
        to_node_id: str,
        relation_type: RelationType,
        description: str = "",
        relation_id: Optional[str] = None
    ) -> Optional[str]:
        """
        添加知识关系
        
        Args:
            from_node_id: 起始节点 ID
            to_node_id: 目标节点 ID
            relation_type: 关系类型
            description: 关系描述
            relation_id: 关系 ID（可选）
            
        Returns:
            关系 ID
        """
        if from_node_id not in self.nodes or to_node_id not in self.nodes:
            logger.error("节点不存在")
            return None
        
        if relation_id is None:
            relation_id = f"rel_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hash(from_node_id + to_node_id) % 10000}"
        
        relation = KnowledgeRelation(
            id=relation_id,
            from_node=from_node_id,
            to_node=to_node_id,
            relation_type=relation_type,
            description=description
        )
        
        self.relations[relation_id] = relation
        self._save_graph()
        
        logger.info(f"已添加关系：{from_node_id} -[{relation_type.value}]-> {to_node_id}")
        return relation_id
    
    def get_node(self, node_id: str) -> Optional[KnowledgeNode]:
        """获取节点"""
        return self.nodes.get(node_id)
    
    def get_related_nodes(
        self,
        node_id: str,
        relation_type: Optional[RelationType] = None,
        direction: str = "both"
    ) -> List[Tuple[KnowledgeNode, KnowledgeRelation]]:
        """
        获取相关节点
        
        Args:
            node_id: 节点 ID
            relation_type: 关系类型过滤
            direction: 方向 (out/in/both)
            
        Returns:
            (相关节点，关系) 列表
        """
        results = []
        
        for rel in self.relations.values():
            if relation_type and rel.relation_type != relation_type:
                continue
            
            related_node_id = None
            
            if direction in ["out", "both"] and rel.from_node == node_id:
                related_node_id = rel.to_node
            elif direction in ["in", "both"] and rel.to_node == node_id:
                related_node_id = rel.from_node
            
            if related_node_id and related_node_id in self.nodes:
                results.append((self.nodes[related_node_id], rel))
        
        return results
    
    def find_path(
        self,
        from_node_id: str,
        to_node_id: str,
        max_depth: int = 5
    ) -> Optional[List[Tuple[KnowledgeNode, KnowledgeRelation]]]:
        """
        查找两个节点之间的路径
        
        Args:
            from_node_id: 起始节点
            to_node_id: 目标节点
            max_depth: 最大深度
            
        Returns:
            路径（节点，关系）列表，无路径返回 None
        """
        if from_node_id not in self.nodes or to_node_id not in self.nodes:
            return None
        
        # BFS 搜索
        visited: Set[str] = {from_node_id}
        queue = [(from_node_id, [])]
        
        while queue:
            current_id, path = queue.pop(0)
            
            if current_id == to_node_id:
                return path
            
            if len(path) >= max_depth:
                continue
            
            # 获取相邻节点
            related = self.get_related_nodes(current_id, direction="out")
            
            for node, rel in related:
                if node.id not in visited:
                    visited.add(node.id)
                    new_path = path + [(node, rel)]
                    queue.append((node.id, new_path))
        
        return None
    
    def search_nodes(
        self,
        query: str,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[KnowledgeNode]:
        """
        搜索节点
        
        Args:
            query: 搜索词
            category: 类别过滤
            tags: 标签过滤
            limit: 结果数量
            
        Returns:
            节点列表
        """
        results = []
        query_lower = query.lower()
        
        for node in self.nodes.values():
            # 类别过滤
            if category and node.category != category:
                continue
            
            # 标签过滤
            if tags and not any(t in node.tags for t in tags):
                continue
            
            # 文本搜索
            score = 0
            if query_lower in node.title.lower():
                score += 3
            if query_lower in node.description.lower():
                score += 1
            if any(query_lower in tag.lower() for tag in node.tags):
                score += 2
            
            if score > 0:
                results.append((score, node))
        
        # 按相关性排序
        results.sort(key=lambda x: x[0], reverse=True)
        
        return [node for _, node in results[:limit]]
    
    def get_recommendations(
        self,
        node_id: str,
        limit: int = 5
    ) -> List[KnowledgeNode]:
        """
        获取推荐节点
        
        基于：
        - 直接相关的节点
        - 相同类别的节点
        - 有相同标签的节点
        
        Args:
            node_id: 节点 ID
            limit: 推荐数量
            
        Returns:
            推荐节点列表
        """
        if node_id not in self.nodes:
            return []
        
        node = self.nodes[node_id]
        recommendations: Dict[str, int] = {}
        
        # 1. 直接相关的节点（权重 3）
        for related_node, _ in self.get_related_nodes(node_id):
            recommendations[related_node.id] = recommendations.get(related_node.id, 0) + 3
        
        # 2. 相同类别的节点（权重 1）
        for other_id, other_node in self.nodes.items():
            if other_id != node_id and other_node.category == node.category:
                recommendations[other_id] = recommendations.get(other_id, 0) + 1
        
        # 3. 有相同标签的节点（权重 2）
        for other_id, other_node in self.nodes.items():
            if other_id != node_id:
                common_tags = set(node.tags) & set(other_node.tags)
                if common_tags:
                    recommendations[other_id] = recommendations.get(other_id, 0) + 2 * len(common_tags)
        
        # 排序
        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        
        return [
            self.nodes[node_id]
            for node_id, _ in sorted_recs[:limit]
            if node_id in self.nodes
        ]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        # 按类别统计
        categories: Dict[str, int] = {}
        for node in self.nodes.values():
            categories[node.category] = categories.get(node.category, 0) + 1
        
        # 按关系类型统计
        relation_types: Dict[str, int] = {}
        for rel in self.relations.values():
            rt = rel.relation_type.value
            relation_types[rt] = relation_types.get(rt, 0) + 1
        
        return {
            'total_nodes': len(self.nodes),
            'total_relations': len(self.relations),
            'categories': categories,
            'relation_types': relation_types,
            'git_notes_available': self.git_notes_available
        }
    
    def get_summary(self) -> str:
        """获取摘要"""
        stats = self.get_stats()
        
        lines = [
            f"Knowledge Graph System",
            f"",
            f"**Total Nodes**: {stats['total_nodes']}",
            f"**Total Relations**: {stats['total_relations']}",
            f"**Git Notes**: {'Available' if stats['git_notes_available'] else 'Not Available'}",
            f""
        ]
        
        if stats['categories']:
            lines.append("**Categories**:")
            for cat, count in stats['categories'].items():
                lines.append(f"- {cat}: {count}")
        
        if stats['relation_types']:
            lines.append("")
            lines.append("**Relation Types**:")
            for rt, count in stats['relation_types'].items():
                lines.append(f"- {rt}: {count}")
        
        return '\n'.join(lines)
    
    def export_graph(self, output_path: Path) -> bool:
        """导出图谱为 JSON"""
        try:
            data = {
                'nodes': {k: v.to_dict() for k, v in self.nodes.items()},
                'relations': {k: v.to_dict() for k, v in self.relations.items()},
                'exported_at': datetime.now().isoformat()
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"图谱已导出：{output_path}")
            return True
        except Exception as e:
            logger.error(f"导出失败：{e}")
            return False


def main():
    """测试知识图谱"""
    graph = KnowledgeGraph()
    
    print("="*60)
    print("Knowledge Graph System Test")
    print("="*60)
    
    # 添加节点
    print("\n1. Adding knowledge nodes...")
    nodes = [
        ("Python", "A high-level programming language", "language", ["programming", "scripting"]),
        ("Machine Learning", "AI branch for learning from data", "ai", ["ai", "data"]),
        ("Deep Learning", "ML using neural networks", "ai", ["ai", "neural"]),
        ("Neural Network", "Computing system inspired by brain", "ai", ["ai", "biology"]),
        ("Data Science", "Extract insights from data", "science", ["data", "analysis"]),
    ]
    
    node_ids = []
    for title, desc, cat, tags in nodes:
        node_id = graph.add_node(title, desc, cat, tags)
        node_ids.append(node_id)
        print(f"   Added: {title}")
    
    # 添加关系
    print("\n2. Adding relations...")
    graph.add_relation(node_ids[0], node_ids[1], RelationType.USED_FOR, "Python used in ML")
    graph.add_relation(node_ids[1], node_ids[2], RelationType.IS_A, "DL is a type of ML")
    graph.add_relation(node_ids[2], node_ids[3], RelationType.USED_FOR, "DL uses neural networks")
    graph.add_relation(node_ids[1], node_ids[4], RelationType.RELATED_TO, "ML related to data science")
    print("   Added 4 relations")
    
    # 搜索
    print("\n3. Searching for 'AI'...")
    results = graph.search_nodes("AI", limit=3)
    for node in results:
        print(f"   - {node.title}: {node.description[:40]}...")
    
    # 获取相关节点
    print("\n4. Related to 'Machine Learning':")
    related = graph.get_related_nodes(node_ids[1])
    for node, rel in related:
        print(f"   - {node.title} [{rel.relation_type.value}]")
    
    # 推荐
    print("\n5. Recommendations for 'Machine Learning':")
    recs = graph.get_recommendations(node_ids[1], limit=3)
    for node in recs:
        print(f"   - {node.title}")
    
    # 统计
    print("\n" + "="*60)
    print(graph.get_summary())


if __name__ == '__main__':
    main()
