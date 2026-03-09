#!/usr/bin/env python3
"""
Multi-Agent Collaboration Demo - 多代理协作演示
展示 agent-coordinator、message-aggregator、research-assistant 如何协作
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# 导入协调器和研究助手
sys.path.insert(0, str(Path(__file__).parent))
from coordinator import AgentCoordinator
from researcher import ResearchAssistant

class CollaborationDemo:
    """多代理协作演示"""
    
    def __init__(self):
        self.coordinator = AgentCoordinator()
        self.researcher = ResearchAssistant()
    
    def execute_complex_task(self, task: str) -> dict:
        """执行复杂任务"""
        print("\n" + "="*60)
        print(f"📋 复杂任务：{task}")
        print("="*60)
        
        # 步骤 1: 协调器分析任务
        print("\n[1/4] 协调器分析任务...")
        analysis = self.coordinator.analyze_task(task)
        print(f"   分解为 {len(analysis['subtasks'])} 个子任务")
        
        for i, subtask in enumerate(analysis['subtasks'], 1):
            print(f"   {i}. {subtask['description']} → {subtask['agent']}")
        
        # 步骤 2: 分派并执行子任务
        print("\n[2/4] 分派并执行子任务...")
        results = {}
        
        for subtask in analysis['subtasks']:
            agent_name = subtask['agent']
            print(f"\n   📤 分派给 {agent_name}...")
            
            if agent_name == "research-assistant":
                # 执行研究任务
                report = self.researcher.research(subtask['description'], depth="quick")
                results[agent_name] = {
                    "status": "completed",
                    "result": report
                }
                print(f"   ✅ 研究完成，找到 {len(report.get('search_results', []))} 条结果")
            
            elif agent_name == "message-aggregator":
                # 消息代理需要配置
                results[agent_name] = {
                    "status": "pending_config",
                    "message": "消息聚合代理需要配置消息平台连接"
                }
                print(f"   ⏳ 等待配置（消息平台未连接）")
        
        # 步骤 3: 整合结果
        print("\n[3/4] 整合结果...")
        summary = {
            "task": task,
            "completed": sum(1 for r in results.values() if r["status"] == "completed"),
            "pending": sum(1 for r in results.values() if r["status"] == "pending_config"),
            "errors": sum(1 for r in results.values() if r["status"] == "error"),
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"   完成：{summary['completed']} | 待配置：{summary['pending']} | 错误：{summary['errors']}")
        
        # 步骤 4: 生成最终报告
        print("\n[4/4] 生成最终报告...")
        
        final_report = {
            "original_task": task,
            "analysis": analysis,
            "agent_results": results,
            "summary": summary,
            "final_output": self._generate_final_output(task, results)
        }
        
        return final_report
    
    def _generate_final_output(self, task: str, results: dict) -> str:
        """生成最终输出"""
        output_lines = [f"\n📝 任务完成报告：{task}\n"]
        
        for agent_name, result in results.items():
            if result["status"] == "completed":
                if "result" in result and "summary" in result["result"]:
                    summary = result["result"]["summary"]
                    output_lines.append(f"\n✅ {agent_name} 的贡献:")
                    for point in summary.get("key_points", [])[:3]:
                        output_lines.append(f"   • {point}")
            elif result["status"] == "pending_config":
                output_lines.append(f"\n⏳ {agent_name}: {result.get('message', '待配置')}")
        
        output_lines.append("\n" + "="*60)
        return "\n".join(output_lines)


def main():
    """主函数"""
    demo = CollaborationDemo()
    
    print("\n" + "="*60)
    print("🤖 MULTI-AGENT COLLABORATION DEMO")
    print("   多代理协作系统演示")
    print("="*60)
    
    # 演示复杂任务
    complex_task = "帮我研究 AI 代理的最新进展，并整理成报告"
    
    final_report = demo.execute_complex_task(complex_task)
    
    # 打印最终报告
    print(final_report["final_output"])
    
    # 保存报告
    report_file = Path(__file__).parent.parent / "memory" / "collaboration-report.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        # 简化报告，移除大对象
        simplified = {
            "task": final_report["original_task"],
            "summary": final_report["summary"],
            "timestamp": final_report["summary"]["timestamp"]
        }
        json.dump(simplified, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 报告已保存：{report_file}")


if __name__ == "__main__":
    main()
