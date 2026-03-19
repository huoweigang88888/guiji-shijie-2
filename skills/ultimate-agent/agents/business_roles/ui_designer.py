"""
UI Designer Agent - UI 设计师代理

负责将 PRD 转化为视觉设计文档
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
logger = logging.getLogger('ui-designer')


class UIDesignerAgent:
    """
    UI 设计师代理
    
    职责:
    - 基于 PRD 进行视觉设计
    - 输出设计风格指南
    - 生成页面设计描述
    - 提供 CSS 代码片段
    """
    
    def __init__(self, workspace_dir: Optional[Path] = None):
        """
        初始化 UI 设计师代理
        
        Args:
            workspace_dir: 工作空间目录
        """
        if workspace_dir is None:
            workspace_dir = Path(__file__).parent.parent / "workspaces" / "ui-designer"
        
        self.workspace_dir = workspace_dir
        self.design_dir = workspace_dir / "design"
        self.session_state_file = workspace_dir / "SESSION-STATE.md"
        
        # 确保目录存在
        self.design_dir.mkdir(parents=True, exist_ok=True)
        
        # 默认配色方案
        self.color_palettes = {
            'blue': {'primary': '#1E90FF', 'secondary': '#4169E1', 'accent': '#00BFFF'},
            'green': {'primary': '#2ECC71', 'secondary': '#27AE60', 'accent': '#1ABC9C'},
            'purple': {'primary': '#9B59B6', 'secondary': '#8E44AD', 'accent': '#3498DB'},
            'orange': {'primary': '#FF6B6B', 'secondary': '#FF8E53', 'accent': '#FFA07A'}
        }
        
        logger.info(f"UI 设计师代理初始化完成，工作空间：{workspace_dir}")
    
    def analyze_prd(self, prd_path: str) -> Dict[str, Any]:
        """
        分析 PRD 文档
        
        Args:
            prd_path: PRD 文件路径
            
        Returns:
            PRD 分析结果
        """
        logger.info(f"分析 PRD: {prd_path}")
        
        # 读取 PRD
        prd_content = ""
        prd_file = Path(prd_path)
        if prd_file.exists():
            with open(prd_file, 'r', encoding='utf-8') as f:
                prd_content = f.read()
        
        # 提取关键信息
        analysis = {
            'project_name': self._extract_from_prd(prd_content, '项目名称'),
            'user_roles': self._extract_user_roles(prd_content),
            'features': self._extract_features(prd_content),
            'style_preference': self._detect_style_preference(prd_content)
        }
        
        # 写入 WAL
        self._write_to_wal('prd_analyzed', analysis)
        
        return analysis
    
    def generate_design(self, prd_analysis: Dict[str, Any]) -> str:
        """
        生成设计文档
        
        Args:
            prd_analysis: PRD 分析结果
            
        Returns:
            设计文档内容
        """
        logger.info("生成设计文档...")
        
        # 选择配色方案
        style = prd_analysis.get('style_preference', 'blue')
        colors = self.color_palettes.get(style, self.color_palettes['blue'])
        
        design_content = f"""# UI 设计文档

**项目名称**: {prd_analysis['project_name']}
**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**版本**: 1.0

---

## 1. 设计风格指南

### 1.1 配色方案

#### 主色调
- Primary: {colors['primary']} (主色)
- Secondary: {colors['secondary']} (辅助色)
- Accent: {colors['accent']} (强调色)

#### 中性色
- Background: #F8F9FA (背景)
- Text: #333333 (主要文字)
- Border: #E0E0E0 (边框)

#### 语义色
- Success: #2ECC71 (成功)
- Warning: #F39C12 (警告)
- Error: #E74C3C (错误)
- Info: #3498DB (信息)

### 1.2 字体规范

#### 字体家族
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

#### 字号层级
- H1: 32px / Bold
- H2: 24px / Bold
- H3: 20px / SemiBold
- Body: 16px / Regular
- Small: 14px / Regular
- Caption: 12px / Regular

#### 行高
- 标题：1.2
- 正文：1.6
- 紧凑：1.4

### 1.3 间距规范

#### 基础单位
- Base: 8px

#### 常用间距
- XS: 4px (0.5x)
- SM: 8px (1x)
- MD: 16px (2x)
- LG: 24px (3x)
- XL: 32px (4x)
- XXL: 48px (6x)

#### 页面边距
- 移动端：16px
- 平板：24px
- 桌面：32px

### 1.4 圆角规范
- 小：4px (按钮、输入框)
- 中：8px (卡片)
- 大：16px (模态框)
- 圆：50% (头像)

### 1.5 阴影规范
```css
/* 轻阴影 */
box-shadow: 0 1px 3px rgba(0,0,0,0.12);

/* 中阴影 */
box-shadow: 0 4px 6px rgba(0,0,0,0.1);

/* 重阴影 */
box-shadow: 0 10px 20px rgba(0,0,0,0.15);
```

---

## 2. 页面设计

### 2.1 首页

#### 布局结构
```
┌─────────────────────────────┐
│         导航栏               │
├─────────────────────────────┤
│                             │
│      Hero 区域               │
│    (标题 + 副标题+CTA)        │
│                             │
├─────────────────────────────┤
│                             │
│      功能展示区              │
│   (卡片网格布局)             │
│                             │
├─────────────────────────────┤
│         页脚                │
└─────────────────────────────┘
```

#### 组件详情

**导航栏**
- 高度：64px
- 背景：白色
- Logo：左侧
- 导航链接：居中
- 用户操作：右侧

**Hero 区域**
- 高度：400px
- 背景：渐变色 ({colors['primary']} → {colors['secondary']})
- 标题：白色，48px
- CTA 按钮：白色背景，主色文字

**功能卡片**
- 尺寸：300px × 200px
- 背景：白色
- 阴影：中阴影
- 圆角：8px

### 2.2 功能页

#### 列表页布局
```
┌─────────────────────────────┐
│         页面标题             │
├─────────────────────────────┤
│  [搜索框]  [筛选器]  [排序]  │
├─────────────────────────────┤
│                             │
│      列表项 1                │
│      列表项 2                │
│      列表项 3                │
│      ...                     │
│                             │
├─────────────────────────────┤
│      [分页器]                │
└─────────────────────────────┘
```

#### 详情页布局
```
┌─────────────────────────────┐
│  [返回]      标题    [操作]  │
├─────────────────────────────┤
│                             │
│      内容区域                │
│                             │
│      - 信息区块 1            │
│      - 信息区块 2            │
│      - 信息区块 3            │
│                             │
├─────────────────────────────┤
│      [操作按钮组]            │
└─────────────────────────────┘
```

---

## 3. 用户操作流程

### 3.1 核心流程

**创建任务流程**
```
1. 点击"新建任务"按钮
2. 填写任务信息（标题、描述、截止日期）
3. 点击"保存"
4. 系统验证输入
5. 任务创建成功，返回列表
```

**完成任务流程**
```
1. 在任务列表中找到目标
2. 点击任务复选框
3. 任务状态更新为"已完成"
4. 视觉反馈（删除线 + 灰色）
```

### 3.2 交互细节

#### 按钮状态
- Default: 主色背景
- Hover: 加深 10%
- Active: 加深 20%
- Disabled: 灰色，50% 透明度

#### 输入框状态
- Default: 灰色边框
- Focus: 主色边框 + 阴影
- Error: 红色边框
- Disabled: 灰色背景

#### 加载状态
- 骨架屏：灰色渐变动画
- Spinner: 主色圆形旋转
- 进度条：主色水平条

---

## 4. CSS 代码片段

### 4.1 CSS 变量

```css
:root {{
  /* 颜色 */
  --color-primary: {colors['primary']};
  --color-secondary: {colors['secondary']};
  --color-accent: {colors['accent']};
  
  --color-bg: #F8F9FA;
  --color-text: #333333;
  --color-border: #E0E0E0;
  
  /* 间距 */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  
  /* 圆角 */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  
  /* 阴影 */
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.12);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 20px rgba(0,0,0,0.15);
}}
```

### 4.2 通用组件

```css
/* 按钮 */
.btn {{
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-sm);
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}}

.btn-primary {{
  background-color: var(--color-primary);
  color: white;
  border: none;
}}

.btn-primary:hover {{
  filter: brightness(0.9);
}}

/* 卡片 */
.card {{
  background: white;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-lg);
}}

/* 输入框 */
.input {{
  width: 100%;
  padding: var(--spacing-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: 16px;
}}

.input:focus {{
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(30, 144, 255, 0.1);
}}
```

---

## 5. 响应式设计

### 5.1 断点

```css
/* 手机 */
@media (max-width: 640px) {{ }}

/* 平板 */
@media (min-width: 641px) and (max-width: 1024px) {{ }}

/* 桌面 */
@media (min-width: 1025px) {{ }}
```

### 5.2 适配规则

- 手机：单列布局
- 平板：双列布局
- 桌面：多列布局

---

## 6. 设计资源

### 6.1 图标
- 使用 Feather Icons 或 Font Awesome
- 尺寸：16px, 24px, 32px

### 6.2 图片
- 格式：WebP (优先), PNG
- 优化：压缩至<100KB

---

*设计文档生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # 写入 WAL
        self._write_to_wal('design_generated', {
            'timestamp': datetime.now().isoformat(),
            'project_name': prd_analysis['project_name'],
            'color_scheme': style
        })
        
        return design_content
    
    def save_design(self, design_content: str, project_name: Optional[str] = None) -> Path:
        """
        保存设计文档
        
        Args:
            design_content: 设计文档内容
            project_name: 项目名称
            
        Returns:
            保存的文件路径
        """
        if project_name is None:
            project_name = "Design"
        
        # 生成文件名
        date_str = datetime.now().strftime('%Y%m%d')
        filename = f"UIDesign_{project_name}_{date_str}.md"
        filepath = self.design_dir / filename
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(design_content)
        
        logger.info(f"设计文档已保存：{filepath}")
        
        # 更新 WAL
        self._write_to_wal('design_saved', {
            'filepath': str(filepath),
            'filename': filename
        })
        
        return filepath
    
    def execute(self, prd_path: str) -> Dict[str, Any]:
        """
        执行完整流程：分析 PRD→生成设计→保存
        
        Args:
            prd_path: PRD 文件路径
            
        Returns:
            执行结果
        """
        logger.info(f"开始执行 UI 设计任务，PRD 路径：{prd_path}")
        
        # 1. 分析 PRD
        prd_analysis = self.analyze_prd(prd_path)
        
        # 2. 生成设计
        design_content = self.generate_design(prd_analysis)
        
        # 3. 保存设计
        filepath = self.save_design(design_content, prd_analysis['project_name'])
        
        # 4. 返回结果
        result = {
            'success': True,
            'project_name': prd_analysis['project_name'],
            'design_path': str(filepath),
            'color_scheme': prd_analysis.get('style_preference', 'blue'),
            'message': f"视觉设计已就绪，路径为 {filepath}"
        }
        
        # 更新 WAL
        self._write_to_wal('task_completed', result)
        
        return result
    
    def _write_to_wal(self, key: str, value: Any) -> None:
        """写入 WAL"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(self.session_state_file, 'a', encoding='utf-8') as f:
            f.write(f"\n## {timestamp} - {key}\n")
            f.write(f"{json.dumps(value, ensure_ascii=False, indent=2)}\n")
    
    def _extract_from_prd(self, content: str, field: str) -> str:
        """从 PRD 中提取字段"""
        for line in content.split('\n'):
            if field in line:
                return line.split(':', 1)[-1].strip()
        return "未命名项目"
    
    def _extract_user_roles(self, content: str) -> List[str]:
        """提取用户角色"""
        roles = []
        in_section = False
        for line in content.split('\n'):
            if '用户角色' in line:
                in_section = True
            elif in_section and line.startswith('###'):
                roles.append(line.replace('###', '').strip())
            elif in_section and line.startswith('##'):
                break
        return roles if roles else ['普通用户']
    
    def _extract_features(self, content: str) -> List[str]:
        """提取功能列表"""
        features = []
        in_section = False
        for line in content.split('\n'):
            if '功能列表' in line:
                in_section = True
            elif in_section and line.startswith('-'):
                features.append(line.replace('-', '').strip())
            elif in_section and line.startswith('##'):
                break
        return features if features else ['核心功能']
    
    def _detect_style_preference(self, content: str) -> str:
        """检测风格偏好"""
        content_lower = content.lower()
        if '商务' in content_lower or '专业' in content_lower:
            return 'blue'
        elif '活泼' in content_lower or '年轻' in content_lower:
            return 'orange'
        elif '优雅' in content_lower or '高端' in content_lower:
            return 'purple'
        elif '清新' in content_lower or '自然' in content_lower:
            return 'green'
        return 'blue'
    
    def get_status(self) -> Dict[str, Any]:
        """获取代理状态"""
        design_files = list(self.design_dir.glob("UIDesign_*.md"))
        
        return {
            'workspace': str(self.workspace_dir),
            'design_count': len(design_files),
            'latest_design': design_files[-1].name if design_files else None,
            'status': 'active'
        }


def main():
    """测试 UI 设计师代理"""
    print("="*60)
    print("UI 设计师代理测试")
    print("="*60)
    
    agent = UIDesignerAgent()
    
    # 显示状态
    print("\n代理状态:")
    status = agent.get_status()
    print(f"  设计文档数量：{status['design_count']}")
    print(f"  最新设计：{status['latest_design']}")
    
    print("\n配色方案:")
    for name, colors in agent.color_palettes.items():
        print(f"  {name}: {colors['primary']}")


if __name__ == '__main__':
    main()
