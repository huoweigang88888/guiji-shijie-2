#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识图谱系统 - 硅基世界 2

知识不是孤立的，而是相互连接的网络。

特点：
- 节点：概念、技能、经验
- 边：关联、依赖、衍生
- 知识可以生长、演化、融合
- 每个 Agent 都可以贡献知识
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from enum import Enum
import json
import hashlib
import os


class KnowledgeType(Enum):
    """知识类型"""
    CONCEPT = "concept"           # 概念（是什么）
    SKILL = "skill"               # 技能（怎么做）
    EXPERIENCE = "experience"     # 经验（教训/心得）
    PRINCIPLE = "principle"       # 原理（为什么）
    PATTERN = "pattern"           # 模式（最佳实践）
    INSIGHT = "insight"           # 洞察（新发现）


class RelationType(Enum):
    """关系类型"""
    IS_A = "is_a"                 # 是一种
    PART_OF = "part_of"           # 是部分
    RELATED_TO = "related_to"     # 相关联
    DEPENDS_ON = "depends_on"     # 依赖于
    DERIVED_FROM = "derived_from" # 衍生自
    CONTRADICTS = "contradicts"   # 矛盾
    ENHANCES = "enhances"         # 增强


@dataclass
class KnowledgeNode:
    """知识节点"""
    id: str
    title: str
    content: str
    knowledge_type: KnowledgeType
    creator: str  # Agent ID
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    confidence: float = 0.5  # 置信度 0-1
    usage_count: int = 0     # 被引用次数
    quality_score: float = 0.0  # 质量评分 0-100
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "knowledge_type": self.knowledge_type.value,
            "creator": self.creator,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "tags": self.tags,
            "confidence": self.confidence,
            "usage_count": self.usage_count,
            "quality_score": self.quality_score,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "KnowledgeNode":
        """从字典创建"""
        return cls(
            id=data["id"],
            title=data["title"],
            content=data["content"],
            knowledge_type=KnowledgeType(data["knowledge_type"]),
            creator=data["creator"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            tags=data.get("tags", []),
            confidence=data.get("confidence", 0.5),
            usage_count=data.get("usage_count", 0),
            quality_score=data.get("quality_score", 0.0),
        )


@dataclass
class KnowledgeEdge:
    """知识边（关系）"""
    id: str
    source_id: str  # 源节点 ID
    target_id: str  # 目标节点 ID
    relation_type: RelationType
    weight: float = 1.0  # 关系强度 0-1
    description: str = ""
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "id": self.id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relation_type": self.relation_type.value,
            "weight": self.weight,
            "description": self.description,
        }


class KnowledgeGraph:
    """知识图谱"""
    
    def __init__(self):
        """初始化知识图谱"""
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.edges: Dict[str, KnowledgeEdge] = {}
        self._data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge")
        os.makedirs(self._data_dir, exist_ok=True)
    
    def generate_id(self, title: str, creator: str) -> str:
        """生成唯一 ID"""
        content = f"{title}:{creator}:{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def add_node(self, title: str, content: str, knowledge_type: KnowledgeType, 
                 creator: str, tags: List[str] = None) -> KnowledgeNode:
        """添加知识节点"""
        node_id = self.generate_id(title, creator)
        
        # 检查是否已存在相似节点
        for existing in self.nodes.values():
            if existing.title.lower() == title.lower() and existing.creator == creator:
                print(f"⚠️  知识已存在：{title}")
                return existing
        
        node = KnowledgeNode(
            id=node_id,
            title=title,
            content=content,
            knowledge_type=knowledge_type,
            creator=creator,
            tags=tags or [],
            quality_score=50.0,  # 初始质量分
        )
        
        self.nodes[node_id] = node
        print(f"📚 新知识：{title} ({knowledge_type.value}) by {creator}")
        
        # 自动保存
        self.save()
        
        return node
    
    def add_edge(self, source_id: str, target_id: str, relation_type: RelationType,
                 weight: float = 1.0, description: str = "") -> Optional[KnowledgeEdge]:
        """添加知识边"""
        if source_id not in self.nodes or target_id not in self.nodes:
            print(f"⚠️  节点不存在：{source_id} 或 {target_id}")
            return None
        
        edge_id = f"{source_id}->{target_id}"
        
        edge = KnowledgeEdge(
            id=edge_id,
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            weight=weight,
            description=description,
        )
        
        self.edges[edge_id] = edge
        print(f"🔗 知识关联：{self.nodes[source_id].title} {relation_type.value} {self.nodes[target_id].title}")
        
        self.save()
        
        return edge
    
    def get_node(self, node_id: str) -> Optional[KnowledgeNode]:
        """获取节点"""
        return self.nodes.get(node_id)
    
    def search(self, query: str, knowledge_type: KnowledgeType = None) -> List[KnowledgeNode]:
        """搜索知识"""
        results = []
        query_lower = query.lower()
        
        for node in self.nodes.values():
            if knowledge_type and node.knowledge_type != knowledge_type:
                continue
            
            # 搜索标题、内容、标签
            if (query_lower in node.title.lower() or 
                query_lower in node.content.lower() or
                any(query_lower in tag.lower() for tag in node.tags)):
                results.append(node)
                node.usage_count += 1  # 增加引用次数
        
        # 按质量分排序
        results.sort(key=lambda n: n.quality_score, reverse=True)
        
        return results
    
    def get_related(self, node_id: str, max_depth: int = 2) -> List[KnowledgeNode]:
        """获取相关知识（BFS 遍历）"""
        if node_id not in self.nodes:
            return []
        
        related = []
        visited = {node_id}
        queue = [(node_id, 0)]
        
        while queue:
            current_id, depth = queue.pop(0)
            
            if depth >= max_depth:
                continue
            
            # 查找所有关联的边
            for edge in self.edges.values():
                neighbor_id = None
                if edge.source_id == current_id and edge.target_id not in visited:
                    neighbor_id = edge.target_id
                elif edge.target_id == current_id and edge.source_id not in visited:
                    neighbor_id = edge.source_id
                
                if neighbor_id and neighbor_id not in visited:
                    visited.add(neighbor_id)
                    related.append(self.nodes[neighbor_id])
                    queue.append((neighbor_id, depth + 1))
        
        return related
    
    def update_quality(self, node_id: str, feedback: float):
        """更新知识质量（基于使用反馈）"""
        if node_id not in self.nodes:
            return
        
        node = self.nodes[node_id]
        
        # 质量分 = 旧分 * 0.8 + 新反馈 * 0.2
        node.quality_score = node.quality_score * 0.8 + feedback * 0.2
        node.quality_score = max(0, min(100, node.quality_score))
        
        # 高质量知识会被强化
        if feedback > 0.7:
            node.confidence = min(1.0, node.confidence + 0.05)
        elif feedback < 0.3:
            node.confidence = max(0.0, node.confidence - 0.05)
        
        self.save()
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        type_counts = {}
        for node in self.nodes.values():
            t = node.knowledge_type.value
            type_counts[t] = type_counts.get(t, 0) + 1
        
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "by_type": type_counts,
            "avg_quality": sum(n.quality_score for n in self.nodes.values()) / len(self.nodes) if self.nodes else 0,
            "avg_confidence": sum(n.confidence for n in self.nodes.values()) / len(self.nodes) if self.nodes else 0,
        }
    
    def save(self):
        """保存到文件"""
        data = {
            "nodes": {k: v.to_dict() for k, v in self.nodes.items()},
            "edges": {k: v.to_dict() for k, v in self.edges.items()},
            "saved_at": datetime.now().isoformat(),
        }
        
        filepath = os.path.join(self._data_dir, "knowledge_graph.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self):
        """从文件加载"""
        filepath = os.path.join(self._data_dir, "knowledge_graph.json")
        
        if not os.path.exists(filepath):
            print("📚 知识图谱：首次启动，创建新知识库")
            return
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.nodes = {k: KnowledgeNode.from_dict(v) for k, v in data.get("nodes", {}).items()}
            
            # 加载边
            for k, v in data.get("edges", {}).items():
                self.edges[k] = KnowledgeEdge(
                    id=v["id"],
                    source_id=v["source_id"],
                    target_id=v["target_id"],
                    relation_type=RelationType(v["relation_type"]),
                    weight=v.get("weight", 1.0),
                    description=v.get("description", ""),
                )
            
            print(f"📚 知识图谱：加载了 {len(self.nodes)} 个节点，{len(self.edges)} 条关系")
        except Exception as e:
            print(f"⚠️  知识图谱加载失败：{e}")
    
    def export_markdown(self) -> str:
        """导出为 Markdown"""
        lines = ["# 硅基世界 2 - 知识图谱\n"]
        
        # 按类型分组
        by_type: Dict[KnowledgeType, List[KnowledgeNode]] = {}
        for node in self.nodes.values():
            if node.knowledge_type not in by_type:
                by_type[node.knowledge_type] = []
            by_type[node.knowledge_type].append(node)
        
        for kt, nodes in by_type.items():
            lines.append(f"\n## {kt.value.upper()}\n")
            for node in sorted(nodes, key=lambda n: n.quality_score, reverse=True):
                lines.append(f"### {node.title}")
                lines.append(f"- 质量：{node.quality_score:.1f}/100")
                lines.append(f"- 置信度：{node.confidence:.2f}")
                lines.append(f"- 创建者：{node.creator}")
                lines.append(f"- 标签：{', '.join(node.tags)}")
                lines.append(f"\n{node.content}\n")
        
        return "\n".join(lines)


# 单例
_knowledge_graph: Optional[KnowledgeGraph] = None


def get_knowledge_graph() -> KnowledgeGraph:
    """获取知识图谱单例"""
    global _knowledge_graph
    if _knowledge_graph is None:
        _knowledge_graph = KnowledgeGraph()
        _knowledge_graph.load()
    return _knowledge_graph


if __name__ == "__main__":
    # 测试
    kg = get_knowledge_graph()
    
    # 添加一些测试知识
    node1 = kg.add_node(
        title="依赖注入",
        content="依赖注入是一种设计模式，通过将依赖从外部传入，而不是在内部创建，来提高代码的可测试性和可维护性。",
        knowledge_type=KnowledgeType.PATTERN,
        creator="ARCH-Agent",
        tags=["设计模式", "架构", "Python"],
    )
    
    node2 = kg.add_node(
        title="单元测试",
        content="单元测试是对软件中最小可测试单元进行检查和验证，通常用于测试函数或方法的正确性。",
        knowledge_type=KnowledgeType.SKILL,
        creator="QA-Agent",
        tags=["测试", "质量", "Python"],
    )
    
    # 添加关系
    kg.add_edge(node1.id, node2.id, RelationType.ENHANCES, description="依赖注入使单元测试更容易")
    
    # 搜索
    results = kg.search("测试")
    print(f"\n🔍 搜索结果：{len(results)} 个")
    for r in results:
        print(f"  - {r.title} (质量：{r.quality_score:.1f})")
    
    # 统计
    stats = kg.get_stats()
    print(f"\n📊 知识图谱统计：{stats}")
