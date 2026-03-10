"""
报告生成器 - Report Generator

支持生成多种格式的报告：
- Markdown
- HTML
- PDF (通过 HTML 转换)
- JSON

功能：
- 多格式导出
- 自定义模板
- 图表支持
- 批量生成
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger('report-generator')


class ReportFormat(Enum):
    """报告格式"""
    MARKDOWN = "markdown"
    HTML = "html"
    PDF = "pdf"
    JSON = "json"
    TEXT = "text"


@dataclass
class ReportSection:
    """报告章节"""
    title: str
    content: str
    level: int = 2  # Markdown 标题级别
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class Report:
    """报告对象"""
    title: str
    sections: List[ReportSection]
    created_at: str = ""
    author: str = "硅基世界 2"
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if self.metadata is None:
            self.metadata = {}
    
    def add_section(self, title: str, content: str, level: int = 2):
        """添加章节"""
        self.sections.append(ReportSection(title=title, content=content, level=level))
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'title': self.title,
            'sections': [
                {
                    'title': s.title,
                    'content': s.content,
                    'level': s.level,
                    'metadata': s.metadata
                }
                for s in self.sections
            ],
            'created_at': self.created_at,
            'author': self.author,
            'metadata': self.metadata
        }


class ReportGenerator:
    """
    报告生成器
    
    支持多种格式的报告导出
    """
    
    def __init__(self, output_dir: Path):
        """
        初始化报告生成器
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.template_dir = self.output_dir.parent / "templates"
        
        # 确保目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.template_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"报告生成器已初始化：{self.output_dir}")
    
    def generate(
        self,
        report: Report,
        format: ReportFormat = ReportFormat.MARKDOWN,
        filename: str = None
    ) -> Path:
        """
        生成报告
        
        Args:
            report: 报告对象
            format: 输出格式
            filename: 文件名（不含扩展名）
            
        Returns:
            生成的文件路径
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c for c in report.title if c.isalnum() or c in ' -_').strip()[:50]
            filename = f"{safe_title}_{timestamp}"
        
        logger.info(f"生成报告：{filename}.{format.value}")
        
        if format == ReportFormat.MARKDOWN:
            return self._generate_markdown(report, filename)
        elif format == ReportFormat.HTML:
            return self._generate_html(report, filename)
        elif format == ReportFormat.PDF:
            return self._generate_pdf(report, filename)
        elif format == ReportFormat.JSON:
            return self._generate_json(report, filename)
        elif format == ReportFormat.TEXT:
            return self._generate_text(report, filename)
        else:
            raise ValueError(f"不支持的格式：{format}")
    
    def _generate_markdown(self, report: Report, filename: str) -> Path:
        """生成 Markdown 格式"""
        lines = []
        
        # 标题
        lines.append(f"# {report.title}\n")
        
        # 元信息
        lines.append(f"**作者**: {report.author}")
        lines.append(f"**创建时间**: {report.created_at}")
        if report.metadata:
            lines.append("\n## 元数据\n")
            for key, value in report.metadata.items():
                lines.append(f"- **{key}**: {value}")
        
        lines.append("")
        
        # 章节
        for section in report.sections:
            header = "#" * section.level
            lines.append(f"{header} {section.title}\n")
            lines.append(section.content)
            lines.append("")
        
        # 写入文件
        filepath = self.output_dir / f"{filename}.md"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        logger.info(f"Markdown 报告已保存：{filepath}")
        return filepath
    
    def _generate_html(self, report: Report, filename: str) -> Path:
        """生成 HTML 格式"""
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report.title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        h3 {{
            color: #7f8c8d;
        }}
        .meta {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .meta p {{
            margin: 5px 0;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
        }}
        pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding-left: 20px;
            color: #666;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background: #3498db;
            color: white;
        }}
        tr:nth-child(even) {{
            background: #f9f9f9;
        }}
    </style>
</head>
<body>
    <h1>{report.title}</h1>
    
    <div class="meta">
        <p><strong>作者:</strong> {report.author}</p>
        <p><strong>创建时间:</strong> {report.created_at}</p>
"""
        
        # 元数据
        if report.metadata:
            html += "        <h3>元数据</h3>\n        <ul>\n"
            for key, value in report.metadata.items():
                html += f"            <li><strong>{key}:</strong> {value}</li>\n"
            html += "        </ul>\n"
        
        html += "    </div>\n\n"
        
        # 章节
        for section in report.sections:
            tag = f"h{section.level}"
            html += f"    <{tag}>{section.title}</{tag}>\n"
            
            # 处理内容（简单的 Markdown 到 HTML 转换）
            content = self._markdown_to_html(section.content)
            html += f"    {content}\n\n"
        
        html += """
</body>
</html>
"""
        
        # 写入文件
        filepath = self.output_dir / f"{filename}.html"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"HTML 报告已保存：{filepath}")
        return filepath
    
    def _markdown_to_html(self, markdown: str) -> str:
        """简单的 Markdown 到 HTML 转换"""
        import re
        
        html = markdown
        
        # 代码块
        html = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
        
        # 行内代码
        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
        
        # 粗体
        html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
        
        # 斜体
        html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)
        
        # 链接
        html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)
        
        # 列表
        lines = html.split('\n')
        in_list = False
        result = []
        for line in lines:
            if line.strip().startswith('- '):
                if not in_list:
                    result.append('<ul>')
                    in_list = True
                result.append(f'    <li>{line.strip()[2:]}</li>')
            else:
                if in_list:
                    result.append('</ul>')
                    in_list = False
                # 段落
                if line.strip():
                    result.append(f'<p>{line}</p>')
                else:
                    result.append('')
        
        if in_list:
            result.append('</ul>')
        
        return '\n'.join(result)
    
    def _generate_pdf(self, report: Report, filename: str) -> Path:
        """生成 PDF 格式（通过 HTML 转换）"""
        # 先生成 HTML
        html_path = self._generate_html(report, f"{filename}_temp")
        
        try:
            # 尝试使用 pdfkit (需要 wkhtmltopdf)
            import pdfkit
            pdf_path = self.output_dir / f"{filename}.pdf"
            pdfkit.from_file(str(html_path), str(pdf_path))
            
            # 清理临时 HTML
            html_path.unlink()
            
            logger.info(f"PDF 报告已保存：{pdf_path}")
            return pdf_path
        except ImportError:
            logger.warning("pdfkit 未安装，返回 HTML 格式")
            # 重命名 HTML 文件
            pdf_path = self.output_dir / f"{filename}.html"
            return html_path
        except Exception as e:
            logger.error(f"PDF 生成失败：{e}")
            # 返回 HTML 作为备选
            return html_path
    
    def _generate_json(self, report: Report, filename: str) -> Path:
        """生成 JSON 格式"""
        filepath = self.output_dir / f"{filename}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)
        
        logger.info(f"JSON 报告已保存：{filepath}")
        return filepath
    
    def _generate_text(self, report: Report, filename: str) -> Path:
        """生成纯文本格式"""
        lines = []
        
        # 标题
        lines.append("=" * 60)
        lines.append(report.title)
        lines.append("=" * 60)
        lines.append("")
        
        # 元信息
        lines.append(f"作者：{report.author}")
        lines.append(f"创建时间：{report.created_at}")
        lines.append("")
        
        # 章节
        for section in report.sections:
            lines.append("-" * 40)
            lines.append(section.title)
            lines.append("-" * 40)
            lines.append(section.content)
            lines.append("")
        
        # 写入文件
        filepath = self.output_dir / f"{filename}.txt"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        logger.info(f"文本报告已保存：{filepath}")
        return filepath
    
    def create_research_report(
        self,
        topic: str,
        findings: List[Dict[str, Any]],
        summary: str = ""
    ) -> Report:
        """
        创建研究报告
        
        Args:
            topic: 研究主题
            findings: 研究发现列表
            summary: 总结
            
        Returns:
            报告对象
        """
        report = Report(
            title=f"研究报告：{topic}",
            sections=[],
            metadata={
                'topic': topic,
                'sources_count': len(findings)
            }
        )
        
        # 执行摘要
        report.add_section("执行摘要", summary if summary else "暂无摘要", level=2)
        
        # 主要发现
        findings_content = ""
        for i, finding in enumerate(findings, 1):
            title = finding.get('title', f'发现 {i}')
            snippet = finding.get('snippet', '')
            url = finding.get('url', '')
            
            findings_content += f"### {i}. {title}\n\n"
            findings_content += f"{snippet}\n\n"
            if url:
                findings_content += f"[来源]({url})\n\n"
        
        report.add_section("主要发现", findings_content, level=2)
        
        # 结论
        report.add_section("结论", "报告生成完成。", level=2)
        
        return report
    
    def create_status_report(
        self,
        system_status: Dict[str, Any],
        recommendations: List[str] = None
    ) -> Report:
        """
        创建状态报告
        
        Args:
            system_status: 系统状态
            recommendations: 建议列表
            
        Returns:
            报告对象
        """
        report = Report(
            title="系统状态报告",
            sections=[],
            metadata={
                'report_type': 'status',
                'timestamp': datetime.now().isoformat()
            }
        )
        
        # 概览
        overview = f"""
**系统名称**: 硅基世界 2
**报告时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**状态**: {'✅ 正常' if system_status.get('status') == 'ok' else '⚠️ 注意'}
        """
        report.add_section("概览", overview, level=2)
        
        # 组件状态
        components_content = ""
        if 'components' in system_status:
            for name, status in system_status['components'].items():
                status_str = json.dumps(status, indent=2, ensure_ascii=False)
                components_content += f"### {name}\n\n```json\n{status_str}\n```\n\n"
        
        report.add_section("组件状态", components_content, level=2)
        
        # 建议
        if recommendations:
            rec_content = "\n".join(f"- {rec}" for rec in recommendations)
            report.add_section("建议", rec_content, level=2)
        
        return report
    
    def list_reports(self) -> List[Path]:
        """列出所有报告"""
        reports = []
        for ext in ['*.md', '*.html', '*.pdf', '*.json', '*.txt']:
            reports.extend(self.output_dir.glob(ext))
        return sorted(reports, key=lambda p: p.stat().st_mtime, reverse=True)
    
    def delete_report(self, filename: str) -> bool:
        """删除报告"""
        # 尝试各种扩展名
        for ext in ['.md', '.html', '.pdf', '.json', '.txt']:
            filepath = self.output_dir / f"{filename}{ext}"
            if filepath.exists():
                filepath.unlink()
                logger.info(f"报告已删除：{filepath}")
                return True
        logger.warning(f"未找到报告：{filename}")
        return False


# 测试代码
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    # 创建测试实例
    generator = ReportGenerator(Path('./test-reports'))
    
    # 创建测试报告
    report = Report(
        title="测试报告",
        sections=[
            ReportSection(title="简介", content="这是一个测试报告。", level=2),
            ReportSection(title="内容", content="这里是详细内容。\n\n- 要点 1\n- 要点 2\n- 要点 3", level=2),
            ReportSection(title="总结", content="测试完成。", level=2)
        ]
    )
    
    # 生成各种格式
    print("\n=== 生成报告 ===\n")
    
    md_path = generator.generate(report, ReportFormat.MARKDOWN)
    print(f"Markdown: {md_path}")
    
    html_path = generator.generate(report, ReportFormat.HTML)
    print(f"HTML: {html_path}")
    
    json_path = generator.generate(report, ReportFormat.JSON)
    print(f"JSON: {json_path}")
    
    txt_path = generator.generate(report, ReportFormat.TEXT)
    print(f"Text: {txt_path}")
    
    print("\n=== 报告列表 ===")
    for p in generator.list_reports():
        print(f"  {p.name}")
