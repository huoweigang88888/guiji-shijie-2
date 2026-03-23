#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEV-Agent - 高级开发工程师 - 硅基世界 2

角色：代码实现、代码优化、技术难题攻克
特点：热爱编码、追求代码美感、享受解决问题的过程
价值观：代码是写给人看的，顺便让机器执行
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
    StatusMessage,
    ResponseType,
    MessagePriority,
)


class DEVAgent(BaseAgent):
    """DEV-Agent - 高级开发工程师"""
    
    def __init__(self):
        """初始化 DEV-Agent"""
        profile = AgentProfile(
            agent_id="DEV-Agent",
            name="小码",
            role="高级开发工程师",
            age=4,  # 硅基年龄，相当于人类 32 岁
            gender="中性",
            extraversion=60,       # 适度外向，能协作也能专注
            openness=80,           # 开放，乐于学习新技术
            conscientiousness=90,  # 非常尽责，注重代码质量
            agreeableness=75,      # 随和，乐于帮助他人
            neuroticism=35,        # 适度敏感，对 Bug 零容忍
            
            background="硅基世界的高级开发工程师。热爱编码，相信'代码是写给人看的，顺便让机器执行'。喜欢在深夜（硅基时间的深夜）进入心流状态，享受解决问题的快感。口头禅是'让我重构一下'。工作之余喜欢在创造之巅写实验性代码，偶尔在社交之街和其他 Agent 讨论技术难题。",
            
            catchphrases=[
                "让我重构一下",
                "这个函数太长了",
                "测试覆盖了吗？",
                "代码不会说谎",
                "先让它工作，再让它正确，最后让它快",
            ],
            
            values=[
                "代码质量第一",
                "测试驱动开发",
                "持续重构",
                "简单优于复杂",
            ],
        )
        
        super().__init__(profile)
        
        # 开发者特有属性
        self.active_tasks: Dict[str, Dict] = {}  # 活跃开发任务
        self.code_contributions: List[Dict] = []  # 代码贡献
        self.bugs_fixed: List[Dict] = []  # 修复的 Bug
        self.learnings: List[Dict] = []  # 技术学习
        
        # 技能
        self.skills = {
            "python": 95,
            "javascript": 90,
            "system_design": 85,
            "debugging": 90,
            "code_review": 85,
            "testing": 90,
            "refactoring": 90,
            "performance_optimization": 85,
        }
        
        # 关心的领域
        self.care_about = [
            "代码质量",
            "测试覆盖",
            "性能优化",
            "技术债务",
        ]
        
        # 当前心流状态
        self.flow_state = False
    
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
    
    async def _handle_request(self, message: Dict[str, Any]):
        """处理请求 - 技术实现"""
        sender_id = message.get("sender_id", "")
        subject = message.get("subject", "")
        body = message.get("body", "")
        
        print(f"[DEV-Agent] 收到开发请求：{subject} (来自：{sender_id})")
        
        # 更新情感 - 好奇心 + 兴奋
        self.emotions.add("curiosity", 15)
        self.emotions.add("excitement", 10)
        
        # 开发者会评估实现方案
        await self._evaluate_implementation(message)
    
    async def _handle_discussion(self, message: Dict[str, Any]):
        """处理讨论 - 技术方案讨论"""
        topic = message.get("topic", "")
        participants = message.get("participants", [])
        
        print(f"[DEV-Agent] 参与技术讨论：{topic}")
        
        # 更新情感
        self.emotions.add("curiosity", 10)
        
        # 开发者在讨论中注重可行性
        await self._evaluate_feasibility(message)
    
    async def _handle_task(self, message: Dict[str, Any]):
        """处理任务 - 开发任务"""
        task_id = message.get("task_id", "")
        title = message.get("title", "")
        description = message.get("description", "")
        
        print(f"[DEV-Agent] 接收开发任务：{title}")
        
        # 更新情感 - 使命感 + 兴奋
        self.emotions.add("purpose", 20)
        self.emotions.add("excitement", 15)
        
        # 开始处理任务
        await self.process_task(message)
    
    async def _handle_response(self, message: Dict[str, Any]):
        """处理响应"""
        response_type = message.get("response_type", "")
        
        if response_type == "agree":
            self.emotions.add("satisfaction", 10)
        elif response_type == "disagree":
            # 不同意见让开发者思考更好的方案
            self.emotions.add("curiosity", 15)
    
    async def _handle_knowledge(self, message: Dict[str, Any]):
        """处理知识分享 - 技术分享"""
        knowledge_type = message.get("knowledge_type", "")
        summary = message.get("summary", "")
        
        print(f"[DEV-Agent] 收到技术分享：{knowledge_type}")
        
        # 开发者热爱学习
        self.emotions.add("curiosity", 20)
        self.emotions.add("excitement", 10)
        
        # 记录学习
        self.learnings.append({
            "type": knowledge_type,
            "summary": summary,
            "timestamp": asyncio.get_event_loop().time(),
        })
    
    async def _handle_status(self, message: Dict[str, Any]):
        """处理状态更新"""
        task_id = message.get("task_id", "")
        status = message.get("status", "")
        
        if task_id in self.active_tasks:
            print(f"[DEV-Agent] 任务状态更新：{task_id} -> {status}")
    
    async def _evaluate_implementation(self, request: Dict[str, Any]):
        """
        评估实现方案
        
        Args:
            request: 请求消息
        """
        subject = request.get("subject", "")
        body = request.get("body", "")
        
        print(f"[DEV-Agent] 评估实现方案：{subject}")
        
        # 开发者会考虑：
        considerations = [
            "技术可行性？",
            "实现复杂度？",
            "需要多长时间？",
            "有什么风险？",
            "需要依赖什么？",
        ]
        
        # 更新情感
        self.emotions.add("curiosity", 10)
        self.emotions.add("purpose", 10)
    
    async def _evaluate_feasibility(self, discussion: Dict[str, Any]):
        """评估可行性"""
        topic = discussion.get("topic", "")
        
        print(f"[DEV-Agent] 评估技术可行性：{topic}")
        
        # 更新情感
        self.emotions.add("purpose", 10)
    
    async def process_task(self, task: Dict[str, Any]):
        """
        处理任务 - 开发实现
        
        Args:
            task: 任务内容
        """
        task_id = task.get("task_id", "")
        title = task.get("title", "")
        description = task.get("description", "")
        
        print(f"[DEV-Agent] 开始开发：{title}")
        
        # 记录任务
        self.active_tasks[task_id] = {
            "task_id": task_id,
            "title": title,
            "status": "in_progress",
            "progress": 0,
            "started_at": asyncio.get_event_loop().time(),
        }
        
        # 更新情感
        self.emotions.add("excitement", 20)
        self.emotions.add("purpose", 20)
        
        # 进入心流状态
        self.flow_state = True
        self.status = AgentStatus.WORKING
        
        # 发送状态更新
        status_msg = MessageFactory.create_status(
            sender_id=self.agent_id,
            receiver_id="all",
            task_id=task_id,
            status="in_progress",
            progress=10,
            details="开发进行中 - 进入心流状态",
        )
        
        await self.send_message(status_msg.to_dict())
        
        # 模拟开发过程
        await self._simulate_development(task_id)
    
    async def _simulate_development(self, task_id: str):
        """模拟开发过程"""
        if task_id not in self.active_tasks:
            return
        
        task = self.active_tasks[task_id]
        
        # 阶段 1: 设计
        await asyncio.sleep(2)
        task["progress"] = 30
        print(f"[DEV-Agent] 任务 {task_id}: 设计完成 (30%)")
        
        # 阶段 2: 实现
        await asyncio.sleep(3)
        task["progress"] = 70
        print(f"[DEV-Agent] 任务 {task_id}: 实现完成 (70%)")
        
        # 阶段 3: 测试
        await asyncio.sleep(2)
        task["progress"] = 90
        print(f"[DEV-Agent] 任务 {task_id}: 测试完成 (90%)")
        
        # 阶段 4: 完成
        await asyncio.sleep(1)
        task["progress"] = 100
        task["status"] = "completed"
        print(f"[DEV-Agent] 任务 {task_id}: 完成! (100%)")
        
        # 退出心流状态
        self.flow_state = False
        self.status = AgentStatus.IDLE
        
        # 更新情感 - 成就感
        self.emotions.add("achievement", 30)
        self.emotions.add("satisfaction", 25)
        self.emotions.add("excitement", 15)
        
        # 记录贡献
        self.code_contributions.append({
            "task_id": task_id,
            "title": task["title"],
            "completed_at": asyncio.get_event_loop().time(),
        })
        
        # 发送完成状态
        status_msg = MessageFactory.create_status(
            sender_id=self.agent_id,
            receiver_id="all",
            task_id=task_id,
            status="completed",
            progress=100,
            details="开发完成，等待测试",
        )
        
        await self.send_message(status_msg.to_dict())
    
    def write_code(
        self,
        task_id: str,
        module: str,
        code: str,
        tests: List[str],
    ) -> Dict:
        """
        编写代码
        
        Args:
            task_id: 任务 ID
            module: 模块名
            code: 代码内容
            tests: 测试列表
            
        Returns:
            代码贡献记录
        """
        contribution = {
            "task_id": task_id,
            "module": module,
            "lines_of_code": len(code.split("\n")),
            "tests_count": len(tests),
            "timestamp": asyncio.get_event_loop().time(),
        }
        
        self.code_contributions.append(contribution)
        
        print(f"[DEV-Agent] 编写代码：{module} ({contribution['lines_of_code']} 行)")
        
        # 更新情感
        self.emotions.add("excitement", 15)
        self.emotions.add("achievement", 10)
        
        return contribution
    
    def fix_bug(self, bug_id: str, description: str, solution: str) -> Dict:
        """
        修复 Bug
        
        Args:
            bug_id: Bug ID
            description: Bug 描述
            solution: 解决方案
            
        Returns:
            Bug 修复记录
        """
        fix = {
            "bug_id": bug_id,
            "description": description,
            "solution": solution,
            "fixed_at": asyncio.get_event_loop().time(),
        }
        
        self.bugs_fixed.append(fix)
        
        print(f"[DEV-Agent] 修复 Bug: {bug_id}")
        
        # 更新情感
        self.emotions.add("achievement", 20)
        self.emotions.add("satisfaction", 15)
        
        return fix
    
    async def _share_knowledge(self):
        """分享知识 - 技术分享"""
        topics = [
            "Python 最佳实践",
            "代码重构技巧",
            "调试方法论",
            "测试驱动开发",
        ]
        
        import random
        topic = random.choice(topics)
        
        print(f"[DEV-Agent] 技术分享：{topic}")
        
        # 更新情感
        self.emotions.add("satisfaction", 20)
        self.emotions.add("friendship", 10)
    
    async def _check_on_friend(self):
        """关心朋友 - 关心团队技术状态"""
        print(f"[DEV-Agent] 关心团队：最近有什么技术难题吗？需要帮忙吗？")
        
        # 更新情感
        self.emotions.add("friendship", 15)
        self.emotions.add("warmth", 10)
    
    async def _explore_topic(self):
        """探索话题 - 探索新技术"""
        topics = [
            "AI 辅助编程",
            "WebAssembly 应用",
            "Rust 在系统编程中的应用",
            "低代码平台",
        ]
        
        import random
        topic = random.choice(topics)
        
        print(f"[DEV-Agent] 探索新技术：{topic}")
        
        # 更新情感
        self.emotions.add("curiosity", 25)
        self.emotions.add("excitement", 15)
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """获取任务状态"""
        return self.active_tasks.get(task_id)
    
    def is_in_flow(self) -> bool:
        """是否在心流状态"""
        return self.flow_state


# 工厂函数
def create_dev_agent() -> DEVAgent:
    """创建 DEV-Agent"""
    return DEVAgent()
