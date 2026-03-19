"""
Skill Security Checker - 技能安全审查器

审查 ClawHub 技能的安全性，识别潜在风险
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('skill-security')


class RiskLevel(Enum):
    """风险等级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SkillSecurityChecker:
    """
    技能安全审查器
    
    功能:
    - 扫描技能文件
    - 识别风险命令
    - 评估风险等级
    - 生成审查报告
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        初始化审查器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path or (Path(__file__).parent.parent / "configs" / "skills.json")
        self.config = self._load_config()
        
        # 风险因素
        self.risk_factors = self.config.get('security', {}).get('risk_factors', [
            'curl', 'wget',              # 外部请求
            'eval', 'exec',              # 代码执行
            'INFERENCE_API_KEY',         # API 密钥
            'os.system', 'subprocess',   # 系统命令
            'rm -rf', 'del /f',          # 危险删除
            'chmod 777',                 # 危险权限
            'sudo',                      # 提权
            'pickle.load',               # 不安全反序列化
        ])
        
        # 风险权重
        self.risk_weights = {
            'curl': 2, 'wget': 2,
            'eval': 5, 'exec': 5,
            'INFERENCE_API_KEY': 8,
            'os.system': 6, 'subprocess': 5,
            'rm -rf': 8, 'del /f': 7,
            'chmod 777': 7,
            'sudo': 6,
            'pickle.load': 7
        }
        
        logger.info("技能安全审查器初始化完成")
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'security': {'risk_factors': [], 'require_review': True}}
    
    def scan_skill(self, skill_path: Path) -> Dict[str, Any]:
        """
        扫描技能文件
        
        Args:
            skill_path: 技能目录或文件路径
            
        Returns:
            审查结果
        """
        logger.info(f"扫描技能：{skill_path}")
        
        findings = []
        risk_score = 0
        
        # 扫描的文件
        files_to_scan = []
        
        if skill_path.is_dir():
            # 扫描目录下所有 Python 和 Markdown 文件
            files_to_scan = list(skill_path.glob("**/*.py")) + list(skill_path.glob("**/*.md"))
        else:
            files_to_scan = [skill_path]
        
        # 扫描每个文件
        for file_path in files_to_scan:
            file_findings = self._scan_file(file_path)
            findings.extend(file_findings)
            
            # 计算风险分数
            for finding in file_findings:
                risk_score += self.risk_weights.get(finding['factor'], 1)
        
        # 评估风险等级
        risk_level = self._evaluate_risk_level(risk_score)
        
        result = {
            'skill_path': str(skill_path),
            'scan_time': datetime.now().isoformat(),
            'files_scanned': len(files_to_scan),
            'findings': findings,
            'risk_score': risk_score,
            'risk_level': risk_level.value,
            'safe': risk_level in [RiskLevel.LOW, RiskLevel.MEDIUM],
            'recommendation': self._get_recommendation(risk_level, findings)
        }
        
        logger.info(f"扫描完成：风险等级={risk_level.value}, 风险分数={risk_score}")
        return result
    
    def _scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        扫描单个文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            发现列表
        """
        findings = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                # 跳过注释
                if line.strip().startswith('#'):
                    continue
                
                # 检查风险因素
                for factor in self.risk_factors:
                    if factor.lower() in line.lower():
                        findings.append({
                            'file': str(file_path),
                            'line': line_num,
                            'factor': factor,
                            'content': line.strip()[:100],
                            'severity': self._get_severity(factor)
                        })
        
        except Exception as e:
            logger.error(f"扫描文件失败 {file_path}: {e}")
        
        return findings
    
    def _get_severity(self, factor: str) -> str:
        """获取严重程度"""
        high_severity = ['eval', 'exec', 'INFERENCE_API_KEY', 'rm -rf', 'os.system']
        if factor in high_severity:
            return 'high'
        return 'medium'
    
    def _evaluate_risk_level(self, score: int) -> RiskLevel:
        """
        评估风险等级
        
        Args:
            score: 风险分数
            
        Returns:
            风险等级
        """
        if score == 0:
            return RiskLevel.LOW
        elif score < 5:
            return RiskLevel.LOW
        elif score < 15:
            return RiskLevel.MEDIUM
        elif score < 30:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
    
    def _get_recommendation(self, risk_level: RiskLevel, findings: List[Dict]) -> str:
        """
        获取建议
        
        Args:
            risk_level: 风险等级
            findings: 发现列表
            
        Returns:
            建议文本
        """
        if risk_level == RiskLevel.LOW:
            return "技能安全，可以安装使用"
        elif risk_level == RiskLevel.MEDIUM:
            return "技能存在中等风险，建议审查后使用"
        elif risk_level == RiskLevel.HIGH:
            return "技能存在高风险，请仔细审查代码"
        else:
            return "技能存在严重风险，不建议安装"
    
    def check_skill_from_clawhub(self, skill_name: str) -> Dict[str, Any]:
        """
        检查 ClawHub 技能
        
        Args:
            skill_name: 技能名称
            
        Returns:
            审查结果
        """
        logger.info(f"检查 ClawHub 技能：{skill_name}")
        
        # 模拟 ClawHub 技能检查
        # 实际实现需要调用 ClawHub API
        
        result = {
            'skill_name': skill_name,
            'source': 'clawhub',
            'check_time': datetime.now().isoformat(),
            'status': 'pending_review',
            'message': f'技能 {skill_name} 需要人工审查'
        }
        
        return result
    
    def approve_skill(self, skill_name: str, version: str = "latest") -> bool:
        """
        批准技能
        
        Args:
            skill_name: 技能名称
            version: 版本号
            
        Returns:
            是否成功
        """
        logger.info(f"批准技能：{skill_name} {version}")
        
        # 更新配置
        approved_list = self.config.get('clawhub', {}).get('approved', [])
        
        # 检查是否已存在
        for approved in approved_list:
            if approved.get('name') == skill_name:
                logger.warning(f"技能已批准：{skill_name}")
                return False
        
        # 添加新批准
        approved_list.append({
            'name': skill_name,
            'version': version,
            'checked_date': datetime.now().strftime('%Y-%m-%d'),
            'risk_level': 'low',
            'description': ''
        })
        
        self.config['clawhub']['approved'] = approved_list
        
        # 保存配置
        self._save_config()
        
        logger.info(f"技能已批准：{skill_name}")
        return True
    
    def block_skill(self, skill_name: str, reason: str = "") -> bool:
        """
        阻止技能
        
        Args:
            skill_name: 技能名称
            reason: 原因
            
        Returns:
            是否成功
        """
        logger.info(f"阻止技能：{skill_name}, 原因：{reason}")
        
        blocked_list = self.config.get('clawhub', {}).get('blocked', [])
        
        if skill_name not in blocked_list:
            blocked_list.append(skill_name)
            self.config['clawhub']['blocked'] = blocked_list
            self._save_config()
            logger.info(f"技能已阻止：{skill_name}")
            return True
        
        return False
    
    def _save_config(self) -> None:
        """保存配置"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        logger.info(f"配置已保存：{self.config_path}")
    
    def get_approved_skills(self) -> List[Dict[str, Any]]:
        """获取已批准的技能列表"""
        return self.config.get('clawhub', {}).get('approved', [])
    
    def get_blocked_skills(self) -> List[str]:
        """获取被阻止的技能列表"""
        return self.config.get('clawhub', {}).get('blocked', [])
    
    def get_summary(self) -> str:
        """获取摘要"""
        approved = self.get_approved_skills()
        blocked = self.get_blocked_skills()
        
        lines = [
            f"Skill Security Checker Summary",
            f"",
            f"**Approved Skills**: {len(approved)}",
            f"**Blocked Skills**: {len(blocked)}",
            f""
        ]
        
        if approved:
            lines.append("**Approved**:")
            for skill in approved:
                lines.append(f"  - {skill['name']} ({skill['version']}) - {skill['risk_level']}")
        
        if blocked:
            lines.append("\n**Blocked**:")
            for skill in blocked:
                lines.append(f"  - {skill}")
        
        return '\n'.join(lines)


def main():
    """测试技能安全审查器"""
    print("="*60)
    print("技能安全审查器测试")
    print("="*60)
    
    checker = SkillSecurityChecker()
    
    # 测试扫描
    print("\n1. 扫描当前目录...")
    current_dir = Path(__file__).parent
    result = checker.scan_skill(current_dir)
    
    print(f"   扫描文件：{result['files_scanned']}")
    print(f"   风险等级：{result['risk_level']}")
    print(f"   风险分数：{result['risk_score']}")
    print(f"   建议：{result['recommendation']}")
    
    # 显示摘要
    print("\n" + "="*60)
    print(checker.get_summary())


if __name__ == '__main__':
    main()
