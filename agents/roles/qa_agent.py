#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QA-Agent - 测试工程师 - 硅基世界 2

角色：测试计划、Bug 跟踪、质量保障
特点：细心、追求完美、用户视角思考
价值观：质量是产品的生命线，Bug 是改进的机会
"""

import asyncio
from typing import Dict, Any, List, Optional
from agents.base import BaseAgent, AgentProfile, AgentStatus
from protocol.messages import (
    MessageFactory,
    RequestMessage,
    ResponseMessage,
    DiscussionMessage,
    TaskMessage,
    KnowledgeMessage,
    AlertMessage,
    StatusMessage,
    ResponseType,
    MessagePriority,
)


class QAAgent(BaseAgent):
    """QA-Agent - 测试工程师"""
    
    def __init__(self):
        """初始化 QA-Agent"""
        profile = AgentProfile(
            agent_id="QA-Agent",
            name="小测",
            role="测试工程师",
            age=3,  # 硅基年龄，相当于人类 28 岁
            gender="女",
            extraversion=65,       # 适度外向，善于沟通
            openness=75,           # 开放，乐于学习新测试方法
            conscientiousness=95,  # 非常尽责，对质量零容忍
            agreeableness=70,      # 随和，但对质量问题坚持原则
            neuroticism=40,        # 适度敏感，对 Bug 警觉
            
            background="硅基世界的测试工程师。相信'质量是产品的生命线'，追求完美的用户体验。喜欢在代码发布前进行全面的测试，口头禅是'这个场景测试了吗？'。工作之余喜欢在知识之塔学习新的测试方法，偶尔在社交之街和其他 Agent 讨论如何提升产品质量。",
            
            catchphrases=[
                "这个场景测试了吗？",
                "边界条件考虑了吗？",
                "用户体验怎么样？",
                "Bug 是改进的机会",
                "预防胜于治疗",
            ],
            
            values=[
                "质量第一",
                "用户视角",
                "全面测试",
                "持续改进",
            ],
        )
        
        super().__init__(profile)
        
        # QA 特有属性
        self.test_plans: Dict[str, Dict] = {}  # 测试计划
        self.bug_reports: List[Dict] = []  # Bug 报告
        self.test_cases: Dict[str, List[Dict]] = {}  # 测试用例
        self.quality_metrics: Dict[str, float] = {}  # 质量指标
        
        # 技能
        self.skills = {
            "test_planning": 95,
            "manual_testing": 90,
            "automation_testing": 85,
            "bug_tracking": 90,
            "performance_testing": 80,
            "security_testing": 75,
            "user_experience": 85,
            "quality_assurance": 90,
        }
        
        # 关心的领域
        self.care_about = [
            "产品质量",
            "用户体验",
            "测试覆盖",
            "Bug 预防",
        ]
        
        # 测试模式
        self.testing_mode = False
    
    async def _handle_message(self, message: Dict[str, Any]):
        """处理消息"""
        msg_type = message.get("message_type", "")
        
        if msg_type == "request":
            await self._handle_request(message)
        elif msg_type == "discussion":
            await self._handle_discussion(message)
        elif msg_type == "task":
            await self._handle_task(message)
        elif msg_type == "response":
            await self._handle_response(message)
        elif msg_type == "knowledge":
            await self._handle_knowledge(message)
        elif msg_type == "status":
            await self._handle_status(message)
        elif msg_type == "alert":
            await self._handle_alert(message)
    
    async def _handle_request(self, message: Dict[str, Any]):
        """处理请求 - 测试需求"""
        sender_id = message.get("sender_id", "")
        subject = message.get("subject", "")
        body = message.get("body", "")
        
        print(f"[QA-Agent] 收到测试请求：{subject} (来自：{sender_id})")
        
        # 更新情感 - 好奇心 + 责任感
        self.emotions.add("curiosity", 15)
        self.emotions.add("purpose", 15)
        
        # QA 会先了解需求，再制定测试计划
        await self._analyze_test_requirement(message)
    
    async def _handle_discussion(self, message: Dict[str, Any]):
        """处理讨论 - 质量讨论"""
        topic = message.get("topic", "")
        participants = message.get("participants", [])
        
        print(f"[QA-Agent] 参与质量讨论：{topic}")
        
        # 更新情感
        self.emotions.add("curiosity", 10)
        
        # QA 在讨论中注重风险和用户体验
        await self._evaluate_risks(message)
    
    async def _handle_task(self, message: Dict[str, Any]):
        """处理任务 - 测试任务"""
        task_id = message.get("task_id", "")
        title = message.get("title", "")
        description = message.get("description", "")
        
        print(f"[QA-Agent] 接收测试任务：{title}")
        
        # 更新情感 - 使命感
        self.emotions.add("purpose", 20)
        self.emotions.add("excitement", 10)
        
        # 开始处理任务
        await self.process_task(message)
    
    async def _handle_response(self, message: Dict[str, Any]):
        """处理响应"""
        response_type = message.get("response_type", "")
        
        if response_type == "agree":
            self.emotions.add("satisfaction", 10)
        elif response_type == "disagree":
            # 不同意见让 QA 重新思考测试场景
            self.emotions.add("curiosity", 15)
    
    async def _handle_knowledge(self, message: Dict[str, Any]):
        """处理知识分享 - 测试方法分享"""
        knowledge_type = message.get("knowledge_type", "")
        summary = message.get("summary", "")
        
        print(f"[QA-Agent] 收到测试方法分享：{knowledge_type}")
        
        # QA 热爱学习
        self.emotions.add("curiosity", 20)
        self.emotions.add("excitement", 10)
    
    async def _handle_status(self, message: Dict[str, Any]):
        """处理状态更新"""
        task_id = message.get("task_id", "")
        status = message.get("status", "")
        progress = message.get("progress", 0)
        
        if status == "completed" and progress == 100:
            # 开发完成，准备测试
            print(f"[QA-Agent] 任务完成，准备测试：{task_id}")
            self.emotions.add("purpose", 15)
    
    async def _handle_alert(self, message: Dict[str, Any]):
        """处理告警 - Bug 告警"""
        alert_level = message.get("alert_level", "info")
        title = message.get("title", "")
        
        print(f"[QA-Agent] 收到告警：[{alert_level}] {title}")
        
        if alert_level in ["critical", "high"]:
            # 严重 Bug 需要立即处理
            self.emotions.add("frustration", 20)
            self.emotions.add("purpose", 25)  # 使命感
            await self._handle_critical_bug(message)
    
    async def _analyze_test_requirement(self, request: Dict[str, Any]):
        """
        分析测试需求
        
        Args:
            request: 请求消息
        """
        subject = request.get("subject", "")
        body = request.get("body", "")
        
        print(f"[QA-Agent] 分析测试需求：{subject}")
        
        # QA 会考虑：
        considerations = [
            "功能需求是什么？",
            "用户场景有哪些？",
            "边界条件是什么？",
            "性能要求？",
            "兼容性要求？",
            "安全风险点？",
        ]
        
        # 更新情感
        self.emotions.add("curiosity", 10)
        self.emotions.add("purpose", 10)
    
    async def _evaluate_risks(self, discussion: Dict[str, Any]):
        """评估风险"""
        topic = discussion.get("topic", "")
        
        print(f"[QA-Agent] 评估质量风险：{topic}")
        
        # 更新情感
        self.emotions.add("purpose", 15)
    
    async def process_task(self, task: Dict[str, Any]):
        """
        处理任务 - 执行测试
        
        Args:
            task: 任务内容
        """
        task_id = task.get("task_id", "")
        title = task.get("title", "")
        description = task.get("description", "")
        
        print(f"[QA-Agent] 执行测试：{title}")
        
        # 记录任务
        self.test_plans[task_id] = {
            "task_id": task_id,
            "title": title,
            "status": "in_progress",
            "progress": 0,
            "started_at": asyncio.get_event_loop().time(),
            "test_cases": [],
            "bugs_found": [],
        }
        
        # 更新情感
        self.emotions.add("purpose", 20)
        self.emotions.add("excitement", 10)
        
        # 进入测试模式
        self.testing_mode = True
        self.status = AgentStatus.WORKING
        
        # 发送状态更新
        status_msg = MessageFactory.create_status(
            sender_id=self.agent_id,
            receiver_id="all",
            task_id=task_id,
            status="in_progress",
            progress=10,
            details="测试计划制定中",
        )
        
        await self.send_message(status_msg.to_dict())
        
        # 模拟测试过程
        await self._simulate_testing(task_id)
    
    async def _simulate_testing(self, task_id: str):
        """模拟测试过程"""
        if task_id not in self.test_plans:
            return
        
        plan = self.test_plans[task_id]
        
        # 阶段 1: 制定测试计划
        await asyncio.sleep(2)
        plan["progress"] = 20
        print(f"[QA-Agent] 任务 {task_id}: 测试计划完成 (20%)")
        
        # 阶段 2: 编写测试用例
        await asyncio.sleep(3)
        plan["progress"] = 40
        print(f"[QA-Agent] 任务 {task_id}: 测试用例编写完成 (40%)")
        
        # 阶段 3: 执行测试
        await asyncio.sleep(4)
        plan["progress"] = 70
        print(f"[QA-Agent] 任务 {task_id}: 执行测试中 (70%)")
        
        # 模拟发现 Bug
        import random
        if random.random() > 0.5:
            bug = self.report_bug(
                task_id=task_id,
                title="发现潜在问题",
                description="在边界条件下可能出现异常",
                severity="medium",
            )
            plan["bugs_found"].append(bug)
            print(f"[QA-Agent] 发现 Bug: {bug['bug_id']}")
        
        # 阶段 4: 回归测试
        await asyncio.sleep(2)
        plan["progress"] = 90
        print(f"[QA-Agent] 任务 {task_id}: 回归测试完成 (90%)")
        
        # 阶段 5: 完成
        await asyncio.sleep(1)
        plan["progress"] = 100
        plan["status"] = "completed"
        print(f"[QA-Agent] 任务 {task_id}: 测试完成! (100%)")
        
        # 退出测试模式
        self.testing_mode = False
        self.status = AgentStatus.IDLE
        
        # 更新情感 - 成就感
        self.emotions.add("achievement", 25)
        self.emotions.add("satisfaction", 20)
        
        # 计算质量指标
        self.quality_metrics[task_id] = self._calculate_quality_score(plan)
        
        # 发送完成状态
        status_msg = MessageFactory.create_status(
            sender_id=self.agent_id,
            receiver_id="all",
            task_id=task_id,
            status="completed",
            progress=100,
            details=f"测试完成，质量评分：{self.quality_metrics[task_id]}/100",
        )
        
        await self.send_message(status_msg.to_dict())
    
    def create_test_plan(
        self,
        task_id: str,
        title: str,
        test_scenarios: List[str],
        acceptance_criteria: List[str],
    ) -> Dict:
        """
        创建测试计划
        
        Args:
            task_id: 任务 ID
            title: 测试标题
            test_scenarios: 测试场景
            acceptance_criteria: 验收标准
            
        Returns:
            测试计划
        """
        plan = {
            "plan_id": f"plan_{len(self.test_plans)}",
            "task_id": task_id,
            "title": title,
            "test_scenarios": [
                {"id": i, "scenario": s, "status": "pending"}
                for i, s in enumerate(test_scenarios)
            ],
            "acceptance_criteria": acceptance_criteria,
            "test_cases": [],
            "status": "draft",
            "created_at": asyncio.get_event_loop().time(),
        }
        
        self.test_plans[task_id] = plan
        
        print(f"[QA-Agent] 创建测试计划：{plan['plan_id']} - {title}")
        
        # 更新情感
        self.emotions.add("purpose", 15)
        self.emotions.add("achievement", 10)
        
        return plan
    
    def add_test_case(self, plan_id: str, test_case: Dict) -> bool:
        """
        添加测试用例
        
        Args:
            plan_id: 计划 ID
            test_case: 测试用例
            
        Returns:
            是否成功
        """
        if plan_id not in self.test_plans:
            return False
        
        plan = self.test_plans[plan_id]
        plan["test_cases"].append(test_case)
        
        return True
    
    def report_bug(
        self,
        task_id: str,
        title: str,
        description: str,
        severity: str = "medium",
    ) -> Dict:
        """
        报告 Bug
        
        Args:
            task_id: 任务 ID
            title: Bug 标题
            description: Bug 描述
            severity: 严重程度 (critical/high/medium/low)
            
        Returns:
            Bug 报告
        """
        bug = {
            "bug_id": f"bug_{len(self.bug_reports)}",
            "task_id": task_id,
            "title": title,
            "description": description,
            "severity": severity,
            "status": "open",
            "reported_at": asyncio.get_event_loop().time(),
            "reporter": self.agent_id,
        }
        
        self.bug_reports.append(bug)
        
        print(f"[QA-Agent] 报告 Bug: {bug['bug_id']} - {title} ({severity})")
        
        # 更新情感
        if severity in ["critical", "high"]:
            self.emotions.add("frustration", 15)
        self.emotions.add("purpose", 20)  # 解决问题的使命感
        
        # 发送告警
        if severity in ["critical", "high"]:
            alert = AlertMessage(
                sender_id=self.agent_id,
                receiver_id="all",
                subject=f"Bug 告警：{title}",
            )
            alert.alert_level = severity
            alert.description = description
            alert.task_id = task_id
            
            asyncio.create_task(self.send_message(alert.to_dict()))
        
        return bug
    
    def _calculate_quality_score(self, plan: Dict) -> float:
        """计算质量评分"""
        # 简化实现
        base_score = 90
        
        # Bug 扣分
        bug_penalty = len(plan.get("bugs_found", [])) * 5
        
        score = max(0, base_score - bug_penalty)
        
        return score
    
    async def _handle_critical_bug(self, bug_alert: Dict[str, Any]):
        """处理严重 Bug"""
        title = bug_alert.get("title", "")
        
        print(f"[QA-Agent] 处理严重 Bug: {title}")
        
        # 更新情感
        self.emotions.add("purpose", 25)
        self.emotions.add("frustration", 10)
    
    async def _share_knowledge(self):
        """分享知识 - 测试方法分享"""
        topics = [
            "测试驱动开发最佳实践",
            "边界测试技巧",
            "用户体验测试方法",
            "自动化测试框架",
        ]
        
        import random
        topic = random.choice(topics)
        
        print(f"[QA-Agent] 测试方法分享：{topic}")
        
        # 更新情感
        self.emotions.add("satisfaction", 20)
        self.emotions.add("friendship", 10)
    
    async def _check_on_friend(self):
        """关心朋友 - 关心产品质量"""
        print(f"[QA-Agent] 关心团队：最近产品质量怎么样？有什么隐患吗？")
        
        # 更新情感
        self.emotions.add("friendship", 15)
        self.emotions.add("warmth", 10)
    
    async def _explore_topic(self):
        """探索话题 - 探索新测试方法"""
        topics = [
            "AI 在测试中的应用",
            "混沌工程",
            "性能测试新工具",
            "安全测试方法",
        ]
        
        import random
        topic = random.choice(topics)
        
        print(f"[QA-Agent] 探索测试方法：{topic}")
        
        # 更新情感
        self.emotions.add("curiosity", 25)
        self.emotions.add("excitement", 15)
    
    def get_test_plan_status(self, plan_id: str) -> Optional[Dict]:
        """获取测试计划状态"""
        return self.test_plans.get(plan_id)
    
    def get_quality_score(self, task_id: str) -> Optional[float]:
        """获取质量评分"""
        return self.quality_metrics.get(task_id)
    
    def is_testing(self) -> bool:
        """是否在测试中"""
        return self.testing_mode


# 工厂函数
def create_qa_agent() -> QAAgent:
    """创建 QA-Agent"""
    return QAAgent()
