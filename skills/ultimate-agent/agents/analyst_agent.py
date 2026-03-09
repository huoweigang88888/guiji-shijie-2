"""
Analyst Agent - 数据分析代理

实现数据统计、趋势分析、报告生成等功能
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import re

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('analyst-agent')


@dataclass
class DataPoint:
    """数据点"""
    timestamp: str
    value: float
    label: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class AnalystAgent:
    """
    数据分析代理
    
    功能:
    - 统计数据（平均值、中位数、标准差等）
    - 趋势分析
    - 异常检测
    - 报告生成
    - 数据可视化（文本图表）
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        初始化分析代理
        
        Args:
            output_dir: 报告输出目录
        """
        if output_dir is None:
            output_dir = Path(__file__).parent.parent / "analysis-output"
        
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 数据集存储
        self.datasets: Dict[str, List[DataPoint]] = {}
        
        # 分析历史
        self.analysis_history: List[Dict[str, Any]] = []
    
    def load_dataset(self, name: str, data: List[Dict[str, Any]]) -> int:
        """
        加载数据集
        
        Args:
            name: 数据集名称
            data: 数据列表
            
        Returns:
            数据点数量
        """
        points = []
        for item in data:
            point = DataPoint(
                timestamp=item.get('timestamp', datetime.now().isoformat()),
                value=float(item.get('value', 0)),
                label=item.get('label'),
                metadata=item.get('metadata', {})
            )
            points.append(point)
        
        self.datasets[name] = points
        logger.info(f"已加载数据集 {name}: {len(points)} 个数据点")
        return len(points)
    
    def calculate_statistics(self, dataset_name: str) -> Dict[str, float]:
        """
        计算统计指标
        
        Args:
            dataset_name: 数据集名称
            
        Returns:
            统计指标
        """
        if dataset_name not in self.datasets:
            raise ValueError(f"数据集不存在：{dataset_name}")
        
        values = [p.value for p in self.datasets[dataset_name]]
        
        if not values:
            return {}
        
        # 基础统计
        n = len(values)
        mean = sum(values) / n
        sorted_values = sorted(values)
        median = sorted_values[n // 2] if n % 2 == 1 else (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
        min_val = min(values)
        max_val = max(values)
        
        # 标准差
        variance = sum((x - mean) ** 2 for x in values) / n
        std_dev = variance ** 0.5
        
        # 百分位数
        p25_idx = int(n * 0.25)
        p75_idx = int(n * 0.75)
        p25 = sorted_values[p25_idx]
        p75 = sorted_values[p75_idx]
        
        return {
            'count': n,
            'mean': round(mean, 4),
            'median': round(median, 4),
            'min': round(min_val, 4),
            'max': round(max_val, 4),
            'std_dev': round(std_dev, 4),
            'variance': round(variance, 4),
            'p25': round(p25, 4),
            'p75': round(p75, 4),
            'range': round(max_val - min_val, 4)
        }
    
    def detect_trend(self, dataset_name: str) -> Dict[str, Any]:
        """
        检测趋势
        
        Args:
            dataset_name: 数据集名称
            
        Returns:
            趋势分析结果
        """
        if dataset_name not in self.datasets:
            raise ValueError(f"数据集不存在：{dataset_name}")
        
        points = self.datasets[dataset_name]
        values = [p.value for p in points]
        
        if len(values) < 2:
            return {'trend': 'insufficient_data'}
        
        # 简单线性回归
        n = len(values)
        x_mean = (n - 1) / 2
        y_mean = sum(values) / n
        
        numerator = sum((i - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        
        # 判断趋势
        if slope > 0.01:
            trend = 'increasing'
        elif slope < -0.01:
            trend = 'decreasing'
        else:
            trend = 'stable'
        
        # 计算变化率
        if values[0] != 0:
            change_rate = ((values[-1] - values[0]) / abs(values[0])) * 100
        else:
            change_rate = 0
        
        return {
            'trend': trend,
            'slope': round(slope, 6),
            'change_rate': round(change_rate, 2),
            'start_value': values[0],
            'end_value': values[-1]
        }
    
    def detect_anomalies(self, dataset_name: str, threshold: float = 2.0) -> List[Dict[str, Any]]:
        """
        检测异常值
        
        Args:
            dataset_name: 数据集名称
            threshold: 标准差阈值
            
        Returns:
            异常值列表
        """
        if dataset_name not in self.datasets:
            raise ValueError(f"数据集不存在：{dataset_name}")
        
        stats = self.calculate_statistics(dataset_name)
        points = self.datasets[dataset_name]
        
        mean = stats['mean']
        std_dev = stats['std_dev']
        
        anomalies = []
        for i, point in enumerate(points):
            z_score = abs(point.value - mean) / std_dev if std_dev > 0 else 0
            if z_score > threshold:
                anomalies.append({
                    'index': i,
                    'value': point.value,
                    'timestamp': point.timestamp,
                    'z_score': round(z_score, 2),
                    'label': point.label
                })
        
        return anomalies
    
    def compare_datasets(self, names: List[str]) -> Dict[str, Any]:
        """
        比较多个数据集
        
        Args:
            names: 数据集名称列表
            
        Returns:
            比较结果
        """
        results = {}
        
        for name in names:
            if name in self.datasets:
                stats = self.calculate_statistics(name)
                trend = self.detect_trend(name)
                results[name] = {
                    'statistics': stats,
                    'trend': trend
                }
        
        return results
    
    def generate_text_chart(self, dataset_name: str, width: int = 50, height: int = 10) -> str:
        """
        生成文本图表
        
        Args:
            dataset_name: 数据集名称
            width: 图表宽度
            height: 图表高度
            
        Returns:
            文本图表
        """
        if dataset_name not in self.datasets:
            raise ValueError(f"数据集不存在：{dataset_name}")
        
        values = [p.value for p in self.datasets[dataset_name]]
        
        if not values:
            return "No data"
        
        min_val = min(values)
        max_val = max(values)
        range_val = max_val - min_val if max_val != min_val else 1
        
        # 创建图表
        chart_lines = []
        for row in range(height, 0, -1):
            threshold = min_val + (range_val * row / height)
            line = ""
            for value in values[:width]:
                normalized = (value - min_val) / range_val
                if normalized >= (row / height):
                    line += "█"
                else:
                    line += " "
            chart_lines.append(line)
        
        # 添加基线
        chart_lines.append("─" * min(len(values), width))
        
        # 添加标签
        chart_lines.append(f"Min: {min_val:.2f} | Max: {max_val:.2f} | Count: {len(values)}")
        
        return "\n".join(chart_lines)
    
    def generate_report(self, dataset_name: str, output_file: Optional[str] = None) -> str:
        """
        生成分析报告
        
        Args:
            dataset_name: 数据集名称
            output_file: 输出文件名（可选）
            
        Returns:
            报告内容
        """
        stats = self.calculate_statistics(dataset_name)
        trend = self.detect_trend(dataset_name)
        anomalies = self.detect_anomalies(dataset_name)
        chart = self.generate_text_chart(dataset_name)
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"""
# 数据分析报告

**数据集**: {dataset_name}  
**生成时间**: {timestamp}

## 统计指标

| 指标 | 值 |
|------|-----|
| 数据点数 | {stats.get('count', 0)} |
| 平均值 | {stats.get('mean', 0)} |
| 中位数 | {stats.get('median', 0)} |
| 标准差 | {stats.get('std_dev', 0)} |
| 最小值 | {stats.get('min', 0)} |
| 最大值 | {stats.get('max', 0)} |
| 25 百分位 | {stats.get('p25', 0)} |
| 75 百分位 | {stats.get('p75', 0)} |

## 趋势分析

- **趋势方向**: {trend.get('trend', 'unknown')}
- **斜率**: {trend.get('slope', 0)}
- **变化率**: {trend.get('change_rate', 0)}%
- **起始值**: {trend.get('start_value', 0)}
- **结束值**: {trend.get('end_value', 0)}

## 异常检测

发现 {len(anomalies)} 个异常值:

"""
        
        for anomaly in anomalies[:10]:
            report += f"- 值：{anomaly['value']}, Z-Score: {anomaly['z_score']}, 时间：{anomaly['timestamp']}\n"
        
        if not anomalies:
            report += "未发现异常值 ✓\n"
        
        report += f"""
## 数据可视化

```
{chart}
```

---
*报告由 硅基世界 2 - Analyst Agent 自动生成*
"""
        
        # 保存报告
        if output_file:
            output_path = self.output_dir / output_file
        else:
            timestamp_file = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = self.output_dir / f"analysis_{dataset_name}_{timestamp_file}.md"
        
        output_path.write_text(report, encoding='utf-8')
        logger.info(f"报告已保存：{output_path}")
        
        # 记录分析历史
        self.analysis_history.append({
            'dataset': dataset_name,
            'timestamp': timestamp,
            'stats': stats,
            'trend': trend,
            'anomalies_count': len(anomalies)
        })
        
        return report
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'datasets': len(self.datasets),
            'total_data_points': sum(len(d) for d in self.datasets.values()),
            'analysis_count': len(self.analysis_history),
            'output_directory': str(self.output_dir)
        }
    
    def get_summary(self) -> str:
        """获取摘要"""
        stats = self.get_stats()
        lines = [
            "Analyst Agent",
            "",
            f"**Datasets**: {stats['datasets']}",
            f"**Total Data Points**: {stats['total_data_points']}",
            f"**Analysis Reports**: {stats['analysis_count']}",
            ""
        ]
        
        if self.datasets:
            lines.append("**Available Datasets**:")
            for name, data in self.datasets.items():
                lines.append(f"- {name}: {len(data)} points")
        
        return '\n'.join(lines)


def main():
    """测试分析代理"""
    print("="*60)
    print("Analyst Agent Test")
    print("="*60)
    
    analyst = AnalystAgent()
    
    # 生成测试数据
    import random
    random.seed(42)
    
    print("\n1. Generate test data")
    test_data = [
        {'timestamp': f'2026-03-{i:02d}', 'value': 100 + i * 2 + random.gauss(0, 5)}
        for i in range(1, 31)
    ]
    analyst.load_dataset('monthly_sales', test_data)
    print(f"   Loaded {len(test_data)} data points")
    
    # 统计
    print("\n2. Calculate statistics")
    stats = analyst.calculate_statistics('monthly_sales')
    print(f"   Mean: {stats['mean']}, Median: {stats['median']}, StdDev: {stats['std_dev']}")
    
    # 趋势
    print("\n3. Detect trend")
    trend = analyst.detect_trend('monthly_sales')
    print(f"   Trend: {trend['trend']}, Change rate: {trend['change_rate']}%")
    
    # 异常
    print("\n4. Detect anomalies")
    anomalies = analyst.detect_anomalies('monthly_sales')
    print(f"   Found {len(anomalies)} anomalies")
    
    # 图表
    print("\n5. Generate chart")
    chart = analyst.generate_text_chart('monthly_sales', width=40, height=8)
    print(chart)
    
    # 报告
    print("\n6. Generate report")
    report = analyst.generate_report('monthly_sales')
    print(f"   Report generated ({len(report)} bytes)")
    
    # 摘要
    print("\n" + "="*60)
    print(analyst.get_summary())


if __name__ == '__main__':
    main()
