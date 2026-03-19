"""
Architect Agent - 架构师代理

负责技术方案设计和架构规划
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('architect')


class ArchitectAgent:
    """
    架构师代理
    
    职责:
    - 基于 PRD 进行技术选型
    - 设计系统架构
    - 输出技术方案文档
    """
    
    def __init__(self, workspace_dir: Optional[Path] = None):
        if workspace_dir is None:
            workspace_dir = Path(__file__).parent.parent / "workspaces" / "architect"
        
        self.workspace_dir = workspace_dir
        self.tech_design_dir = workspace_dir / "tech-design"
        self.session_state_file = workspace_dir / "SESSION-STATE.md"
        
        self.tech_design_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"架构师代理初始化完成：{workspace_dir}")
    
    def analyze_requirements(self, prd_path: str) -> Dict[str, Any]:
        """分析 PRD 需求"""
        logger.info(f"分析 PRD: {prd_path}")
        
        prd_file = Path(prd_path)
        content = ""
        if prd_file.exists():
            content = prd_file.read_text(encoding='utf-8')
        
        analysis = {
            'project_name': self._extract_field(content, '项目名称'),
            'features': self._extract_features(content),
            'scale': self._estimate_scale(content)
        }
        
        self._write_to_wal('requirements_analyzed', analysis)
        return analysis
    
    def design_architecture(self, requirements: Dict[str, Any]) -> str:
        """设计系统架构"""
        logger.info("设计系统架构...")
        
        scale = requirements.get('scale', 'medium')
        
        tech_content = f"""# 技术方案文档

**项目名称**: {requirements['project_name']}
**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**版本**: 1.0

---

## 1. 技术栈选择

### 1.1 后端技术

#### 编程语言
- **Python 3.11+**
- 理由：生态丰富、开发效率高、AI 支持好

#### Web 框架
- **FastAPI**
- 理由：高性能、异步支持、自动 API 文档

#### 数据库
- **PostgreSQL 15+**
- 理由：可靠性强、功能丰富、支持 JSON

### 1.2 前端技术

#### 框架
- **React 18+**
- 理由：生态成熟、组件丰富

#### UI 库
- **Ant Design / Tailwind CSS**
- 理由：组件齐全、样式美观

### 1.3 基础设施

#### 缓存
- **Redis**
- 理由：高性能、支持多种数据结构

#### 消息队列
- **RabbitMQ / Celery**
- 理由：异步任务处理

---

## 2. 系统架构图

```mermaid
graph TB
    Client[客户端] --> CDN[CDN]
    CDN --> LB[负载均衡]
    LB --> API[API 网关]
    
    API --> Auth[认证服务]
    API --> Business[业务服务]
    
    Business --> Cache[(Redis)]
    Business --> DB[(PostgreSQL)]
    Business --> MQ[消息队列]
    
    MQ --> Worker[后台任务]
    Worker --> DB
```

---

## 3. 核心数据模型

### 3.1 用户表 (users)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### 3.2 核心业务表

```sql
CREATE TABLE items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 4. API 设计

### 4.1 RESTful 规范

```
GET    /api/v1/items      # 获取列表
POST   /api/v1/items      # 创建项目
GET    /api/v1/items/:id  # 获取详情
PUT    /api/v1/items/:id  # 更新项目
DELETE /api/v1/items/:id  # 删除项目
```

### 4.2 响应格式

```json
{{
  "success": true,
  "data": {{}},
  "message": "操作成功"
}}
```

---

## 5. 部署架构

### 5.1 开发环境
- Docker Compose 本地运行
- 热重载开发模式

### 5.2 生产环境
- Docker 容器化部署
- Kubernetes 编排
- CI/CD 自动化

---

*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        self._write_to_wal('architecture_designed', {
            'timestamp': datetime.now().isoformat(),
            'project_name': requirements['project_name']
        })
        
        return tech_content
    
    def save_design(self, content: str, project_name: str) -> Path:
        """保存技术方案"""
        date_str = datetime.now().strftime('%Y%m%d')
        filename = f"TechDesign_{project_name}_{date_str}.md"
        filepath = self.tech_design_dir / filename
        
        filepath.write_text(content, encoding='utf-8')
        logger.info(f"技术方案已保存：{filepath}")
        
        self._write_to_wal('design_saved', {'filepath': str(filepath)})
        return filepath
    
    def execute(self, prd_path: str) -> Dict[str, Any]:
        """执行完整流程"""
        logger.info(f"开始执行架构设计任务")
        
        requirements = self.analyze_requirements(prd_path)
        design_content = self.design_architecture(requirements)
        filepath = self.save_design(design_content, requirements['project_name'])
        
        result = {
            'success': True,
            'project_name': requirements['project_name'],
            'design_path': str(filepath),
            'message': f"技术方案已就绪，路径为 {filepath}"
        }
        
        self._write_to_wal('task_completed', result)
        return result
    
    def _write_to_wal(self, key: str, value: Any) -> None:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.session_state_file, 'a', encoding='utf-8') as f:
            f.write(f"\n## {timestamp} - {key}\n{json.dumps(value, ensure_ascii=False, indent=2)}\n")
    
    def _extract_field(self, content: str, field: str) -> str:
        for line in content.split('\n'):
            if field in line:
                return line.split(':', 1)[-1].strip()
        return "未命名项目"
    
    def _extract_features(self, content: str) -> List[str]:
        features = []
        for line in content.split('\n'):
            if line.strip().startswith('- 功能'):
                features.append(line.strip())
        return features if features else ['核心功能']
    
    def _estimate_scale(self, content: str) -> str:
        if '企业' in content or '大型' in content:
            return 'large'
        elif '简单' in content or '小型' in content:
            return 'small'
        return 'medium'
    
    def get_status(self) -> Dict[str, Any]:
        files = list(self.tech_design_dir.glob("TechDesign_*.md"))
        return {
            'workspace': str(self.workspace_dir),
            'design_count': len(files),
            'latest_design': files[-1].name if files else None,
            'status': 'active'
        }


def main():
    print("="*60)
    print("架构师代理测试")
    print("="*60)
    
    agent = ArchitectAgent()
    status = agent.get_status()
    print(f"技术方案数量：{status['design_count']}")


if __name__ == '__main__':
    main()
