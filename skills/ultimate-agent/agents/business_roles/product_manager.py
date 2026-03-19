"""
Product Manager Agent - 产品经理代理

负责将用户需求转化为产品需求文档（PRD）
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('product-manager')


class ProductManagerAgent:
    """
    产品经理代理
    
    职责:
    - 与用户沟通，理解业务目标
    - 产出标准化 PRD 文档
    - 保存 PRD 到指定目录
    """
    
    def __init__(self, workspace_dir: Optional[Path] = None):
        """
        初始化产品经理代理
        
        Args:
            workspace_dir: 工作空间目录，默认为 workspaces/product-manager/
        """
        if workspace_dir is None:
            workspace_dir = Path(__file__).parent.parent / "workspaces" / "product-manager"
        
        self.workspace_dir = workspace_dir
        self.prd_dir = workspace_dir / "prd"
        self.session_state_file = workspace_dir / "SESSION-STATE.md"
        
        # 确保目录存在
        self.prd_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"产品经理代理初始化完成，工作空间：{workspace_dir}")
    
    def analyze_requirement(self, user_input: str) -> Dict[str, Any]:
        """
        分析用户需求
        
        Args:
            user_input: 用户输入的需求描述
            
        Returns:
            需求分析结果
        """
        logger.info(f"分析需求：{user_input[:100]}...")
        
        # 提取关键信息
        analysis = {
            'project_name': self._extract_project_name(user_input),
            'goal': self._extract_goal(user_input),
            'user_roles': self._extract_user_roles(user_input),
            'features': self._extract_features(user_input),
            'priority': self._determine_priority(user_input)
        }
        
        # 写入 WAL（Write-Ahead Log）
        self._write_to_wal('requirement_analysis', analysis)
        
        return analysis
    
    def generate_prd(self, analysis: Dict[str, Any]) -> str:
        """
        生成 PRD 文档
        
        Args:
            analysis: 需求分析结果
            
        Returns:
            PRD 文档内容
        """
        logger.info("生成 PRD 文档...")
        
        prd_content = f"""# 产品需求文档 (PRD)

**项目名称**: {analysis['project_name']}
**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**版本**: 1.0

---

## 1. 项目背景与目标

### 背景
{analysis['goal']}

### 目标
- 核心目标：{analysis['goal']}
- 成功指标：用户满意度、功能完成率

---

## 2. 用户角色

"""
        
        # 添加用户角色
        for i, role in enumerate(analysis.get('user_roles', ['普通用户']), 1):
            prd_content += f"""
### 角色 {i}: {role}
- 描述：使用系统的普通用户
- 特点：需要简单易用的界面
- 核心需求：快速完成目标任务
"""
        
        prd_content += f"""

---

## 3. 功能列表

### P0 (必须 - 最高优先级)
"""
        
        # 添加功能列表
        features = analysis.get('features', ['核心功能'])
        for i, feature in enumerate(features[:3], 1):
            prd_content += f"- 功能 {i}: {feature}\n"
        
        prd_content += """
### P1 (重要 - 中等优先级)
- 用户认证与权限管理
- 数据导出功能

### P2 (可选 - 低优先级)
- 主题切换
- 高级搜索

---

## 4. 用户故事

"""
        
        # 添加用户故事
        for role in analysis.get('user_roles', ['普通用户'])[:2]:
            prd_content += f"- 作为 {role}，我想要 [功能]，以便 [价值]\n"
        
        prd_content += f"""

---

## 5. 验收标准

### 功能验收
- [ ] 核心功能可正常使用
- [ ] 用户体验流畅
- [ ] 无明显 Bug

### 性能验收
- [ ] 页面加载时间 < 2 秒
- [ ] 支持并发用户数 > 100

---

## 6. 非功能性需求

### 性能要求
- 响应时间：< 500ms
- 吞吐量：> 1000 请求/秒

### 安全要求
- 用户数据加密存储
- HTTPS 传输
- 定期安全审计

### 可用性要求
- 系统可用性：> 99.9%
- 支持主流浏览器

---

## 附录

### 术语表
- PRD: 产品需求文档
- P0/P1/P2: 优先级分级

### 参考资料
- [相关文档链接]

---

*文档生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # 写入 WAL
        self._write_to_wal('prd_generated', {
            'timestamp': datetime.now().isoformat(),
            'project_name': analysis['project_name']
        })
        
        return prd_content
    
    def save_prd(self, prd_content: str, project_name: Optional[str] = None) -> Path:
        """
        保存 PRD 文档
        
        Args:
            prd_content: PRD 文档内容
            project_name: 项目名称（可选，用于生成文件名）
            
        Returns:
            保存的文件路径
        """
        if project_name is None:
            project_name = "PRD"
        
        # 生成文件名
        date_str = datetime.now().strftime('%Y%m%d')
        filename = f"PRD_{project_name}_{date_str}.md"
        filepath = self.prd_dir / filename
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(prd_content)
        
        logger.info(f"PRD 已保存：{filepath}")
        
        # 更新 WAL
        self._write_to_wal('prd_saved', {
            'filepath': str(filepath),
            'filename': filename
        })
        
        return filepath
    
    def execute(self, user_input: str) -> Dict[str, Any]:
        """
        执行完整流程：分析→生成→保存
        
        Args:
            user_input: 用户需求描述
            
        Returns:
            执行结果
        """
        logger.info(f"开始执行产品经理任务：{user_input[:100]}...")
        
        # 1. 分析需求
        analysis = self.analyze_requirement(user_input)
        
        # 2. 生成 PRD
        prd_content = self.generate_prd(analysis)
        
        # 3. 保存 PRD
        filepath = self.save_prd(prd_content, analysis['project_name'])
        
        # 4. 返回结果
        result = {
            'success': True,
            'project_name': analysis['project_name'],
            'prd_path': str(filepath),
            'analysis': analysis,
            'message': f"PRD 已就绪，路径为 {filepath}"
        }
        
        # 更新 WAL
        self._write_to_wal('task_completed', result)
        
        return result
    
    def _write_to_wal(self, key: str, value: Any) -> None:
        """
        写入 WAL（Write-Ahead Log）
        
        Args:
            key: 键名
            value: 值
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(self.session_state_file, 'a', encoding='utf-8') as f:
            f.write(f"\n## {timestamp} - {key}\n")
            f.write(f"{json.dumps(value, ensure_ascii=False, indent=2)}\n")
    
    def _extract_project_name(self, text: str) -> str:
        """提取项目名称"""
        # 简单实现，可根据关键词提取
        keywords = ['应用', '系统', '平台', '网站', '工具']
        for kw in keywords:
            if kw in text:
                return text.split(kw)[0].strip()[-10:] + kw
        return "未命名项目"
    
    def _extract_goal(self, text: str) -> str:
        """提取项目目标"""
        return text.strip()
    
    def _extract_user_roles(self, text: str) -> List[str]:
        """提取用户角色"""
        # 简单实现
        return ['普通用户', '管理员']
    
    def _extract_features(self, text: str) -> List[str]:
        """提取功能列表"""
        # 简单实现
        return ['核心功能', '用户管理', '数据管理']
    
    def _determine_priority(self, text: str) -> str:
        """确定优先级"""
        return 'P0'
    
    def get_status(self) -> Dict[str, Any]:
        """获取代理状态"""
        prd_files = list(self.prd_dir.glob("PRD_*.md"))
        
        return {
            'workspace': str(self.workspace_dir),
            'prd_count': len(prd_files),
            'latest_prd': prd_files[-1].name if prd_files else None,
            'status': 'active'
        }


def main():
    """测试产品经理代理"""
    print("="*60)
    print("产品经理代理测试")
    print("="*60)
    
    agent = ProductManagerAgent()
    
    # 测试用例
    test_input = "开发一个待办事项应用，用户可以创建任务、标记完成、删除任务"
    
    print(f"\n用户需求：{test_input}\n")
    
    result = agent.execute(test_input)
    
    print(f"项目名称：{result['project_name']}")
    print(f"PRD 路径：{result['prd_path']}")
    print(f"状态：{result['message']}")
    
    # 显示状态
    print("\n代理状态:")
    status = agent.get_status()
    print(f"  PRD 数量：{status['prd_count']}")
    print(f"  最新 PRD: {status['latest_prd']}")


if __name__ == '__main__':
    main()
