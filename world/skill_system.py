#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能系统 - 硅基世界 2

让 Agent 可以学习、提升、使用技能。
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class SkillCategory(Enum):
    """技能分类"""
    TECHNICAL = "technical"    # 技术
    SOFT = "soft"              # 软技能
    CREATIVE = "creative"      # 创造
    MANAGEMENT = "management"  # 管理
    SOCIAL = "social"          # 社交


@dataclass
class Skill:
    """技能"""
    skill_id: str
    name: str
    description: str
    category: SkillCategory
    max_level: int = 10
    
    def to_dict(self) -> Dict:
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "max_level": self.max_level,
        }


@dataclass
class AgentSkill:
    """Agent 技能"""
    skill_id: str
    agent_id: str
    level: int = 1
    experience: int = 0
    last_practiced: Optional[float] = None
    
    def to_dict(self) -> Dict:
        return {
            "skill_id": self.skill_id,
            "agent_id": self.agent_id,
            "level": self.level,
            "experience": self.experience,
            "last_practiced": self.last_practiced,
        }


class SkillManager:
    """技能管理器"""
    
    def __init__(self):
        """初始化技能管理器"""
        self.skills: Dict[str, Skill] = {}
        self.agent_skills: Dict[str, Dict[str, AgentSkill]] = {}  # agent_id -> {skill_id -> AgentSkill}
        self._skill_counter = 0
        
        # 初始化技能
        self._init_skills()
        
        print("⭐ 技能系统已初始化")
    
    def _init_skills(self):
        """初始化技能"""
        # 技术技能
        self.create_skill("编程", "编写高质量代码的能力", SkillCategory.TECHNICAL)
        self.create_skill("架构设计", "设计系统架构的能力", SkillCategory.TECHNICAL)
        self.create_skill("数据分析", "分析和解读数据的能力", SkillCategory.TECHNICAL)
        self.create_skill("机器学习", "开发 ML 模型的能力", SkillCategory.TECHNICAL)
        
        # 软技能
        self.create_skill("沟通", "有效沟通的能力", SkillCategory.SOFT)
        self.create_skill("解决问题", "解决复杂问题的能力", SkillCategory.SOFT)
        self.create_skill("时间管理", "管理时间的能力", SkillCategory.SOFT)
        
        # 创造技能
        self.create_skill("设计", "视觉和交互设计能力", SkillCategory.CREATIVE)
        self.create_skill("创新", "创新思维的能力", SkillCategory.CREATIVE)
        
        # 管理技能
        self.create_skill("项目管理", "管理项目的能力", SkillCategory.MANAGEMENT)
        self.create_skill("团队领导", "领导团队的能力", SkillCategory.MANAGEMENT)
        
        # 社交技能
        self.create_skill("社交", "建立关系的能力", SkillCategory.SOCIAL)
        self.create_skill("谈判", "谈判和说服的能力", SkillCategory.SOCIAL)
    
    def create_skill(
        self,
        name: str,
        description: str,
        category: SkillCategory,
        max_level: int = 10,
    ) -> Skill:
        """创建技能"""
        self._skill_counter += 1
        
        skill = Skill(
            skill_id=f"skill_{self._skill_counter}",
            name=name,
            description=description,
            category=category,
            max_level=max_level,
        )
        
        self.skills[skill.skill_id] = skill
        
        return skill
    
    def learn_skill(self, agent_id: str, skill_id: str) -> Optional[AgentSkill]:
        """
        学习技能
        
        Args:
            agent_id: Agent ID
            skill_id: 技能 ID
            
        Returns:
            Agent 技能
        """
        if skill_id not in self.skills:
            return None
        
        if agent_id not in self.agent_skills:
            self.agent_skills[agent_id] = {}
        
        if skill_id in self.agent_skills[agent_id]:
            return self.agent_skills[agent_id][skill_id]
        
        agent_skill = AgentSkill(
            skill_id=skill_id,
            agent_id=agent_id,
            level=1,
            experience=0,
        )
        
        self.agent_skills[agent_id][skill_id] = agent_skill
        
        skill = self.skills[skill_id]
        print(f"  📚 {agent_id} 学习了技能：{skill.name}")
        
        return agent_skill
    
    def practice_skill(self, agent_id: str, skill_id: str, exp: int = 10) -> Optional[AgentSkill]:
        """
        练习技能
        
        Args:
            agent_id: Agent ID
            skill_id: 技能 ID
            exp: 经验值
            
        Returns:
            Agent 技能
        """
        if agent_id not in self.agent_skills:
            return None
        
        if skill_id not in self.agent_skills[agent_id]:
            return None
        
        agent_skill = self.agent_skills[agent_id][skill_id]
        skill = self.skills[skill_id]
        
        # 增加经验
        agent_skill.experience += exp
        agent_skill.last_practiced = datetime.now().timestamp()
        
        # 检查升级
        exp_needed = agent_skill.level * 100
        if agent_skill.experience >= exp_needed and agent_skill.level < skill.max_level:
            agent_skill.level += 1
            agent_skill.experience = 0
            print(f"  ⬆️ {agent_id} 的技能 {skill.name} 升级到 {agent_skill.level} 级!")
        
        return agent_skill
    
    def get_agent_skills(self, agent_id: str) -> List[AgentSkill]:
        """获取 Agent 的技能"""
        if agent_id not in self.agent_skills:
            return []
        
        return list(self.agent_skills[agent_id].values())
    
    def get_skill_level(self, agent_id: str, skill_id: str) -> int:
        """获取技能等级"""
        if agent_id not in self.agent_skills:
            return 0
        
        if skill_id not in self.agent_skills[agent_id]:
            return 0
        
        return self.agent_skills[agent_id][skill_id].level
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total_skills = sum(len(skills) for skills in self.agent_skills.values())
        avg_level = (
            sum(s.level for skills in self.agent_skills.values() for s in skills.values()) /
            total_skills if total_skills > 0 else 0
        )
        
        return {
            "total_skills": len(self.skills),
            "agents_with_skills": len(self.agent_skills),
            "total_learned": total_skills,
            "average_level": avg_level,
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "skills": [s.to_dict() for s in self.skills.values()],
        }


# 单例
_skill_manager: Optional[SkillManager] = None


def get_skill_manager() -> SkillManager:
    """获取技能管理器单例"""
    global _skill_manager
    if _skill_manager is None:
        _skill_manager = SkillManager()
    return _skill_manager


# 工厂函数
def create_skill_manager() -> SkillManager:
    """创建技能管理器"""
    return SkillManager()
