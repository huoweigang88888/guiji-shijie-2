"""
Senior Developer Agent - 高级开发工程师代理

负责代码实现和单元测试
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('senior-dev')


class SeniorDevAgent:
    """
    开发工程师代理
    
    职责:
    - 根据技术方案和视觉设计进行编码
    - 编写单元测试
    - 生成 README 文档
    """
    
    def __init__(self, workspace_dir: Optional[Path] = None):
        if workspace_dir is None:
            workspace_dir = Path(__file__).parent.parent / "workspaces" / "senior-dev"
        
        self.workspace_dir = workspace_dir
        self.src_dir = workspace_dir / "src"
        self.session_state_file = workspace_dir / "SESSION-STATE.md"
        
        self.src_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"开发工程师代理初始化：{workspace_dir}")
    
    def implement(self, tech_design_path: str, ui_design_path: Optional[str] = None) -> Dict[str, Any]:
        """实现代码"""
        logger.info("开始代码实现...")
        
        # 创建项目结构
        self._create_project_structure()
        
        # 生成示例代码
        code_content = self._generate_sample_code()
        
        # 保存代码
        main_file = self.src_dir / "app" / "main.py"
        main_file.parent.mkdir(parents=True, exist_ok=True)
        main_file.write_text(code_content, encoding='utf-8')
        
        # 生成 README
        readme = self._generate_readme()
        (self.src_dir / "README.md").write_text(readme, encoding='utf-8')
        
        result = {
            'success': True,
            'code_path': str(self.src_dir),
            'message': f"代码已就绪，位于 {self.src_dir}"
        }
        
        self._write_to_wal('code_implemented', result)
        return result
    
    def _create_project_structure(self):
        """创建项目结构"""
        dirs = [
            self.src_dir / "app" / "models",
            self.src_dir / "app" / "routes",
            self.src_dir / "app" / "services",
            self.src_dir / "tests",
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
            (d / "__init__.py").touch()
    
    def _generate_sample_code(self) -> str:
        """生成示例代码"""
        return '''"""
主应用入口
"""
from fastapi import FastAPI

app = FastAPI(title="My Project", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/v1/items")
async def get_items():
    return {"items": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    def _generate_readme(self) -> str:
        """生成 README"""
        return f'''# 项目

**创建时间**: {datetime.now().strftime('%Y-%m-%d')}

## 快速开始

### 环境要求
- Python 3.11+
- PostgreSQL 15+

### 安装
```bash
pip install -r requirements.txt
```

### 运行
```bash
python app/main.py
```

### 测试
```bash
pytest tests/
```

## 项目结构
```
src/
├── app/
│   ├── main.py
│   ├── models/
│   ├── routes/
│   └── services/
└── tests/
```
'''
    
    def _write_to_wal(self, key: str, value: Any) -> None:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.session_state_file, 'a', encoding='utf-8') as f:
            f.write(f"\n## {timestamp} - {key}\n{json.dumps(value, ensure_ascii=False, indent=2)}\n")
    
    def get_status(self) -> Dict[str, Any]:
        files = list(self.src_dir.glob("**/*.py"))
        return {
            'workspace': str(self.workspace_dir),
            'python_files': len(files),
            'status': 'active'
        }


def main():
    print("="*60)
    print("开发工程师代理测试")
    print("="*60)
    
    agent = SeniorDevAgent()
    status = agent.get_status()
    print(f"Python 文件数：{status['python_files']}")


if __name__ == '__main__':
    main()
