#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📝 命令行待办事项管理器
简单、轻量、本地存储的 Todo 工具

用法:
    python demo-todo.py add "买牛奶"
    python demo-todo.py list
    python demo-todo.py done 1
    python demo-todo.py delete 1
    python demo-todo.py clear
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 数据文件路径
DATA_FILE = Path.home() / ".openclaw" / "workspace" / "todos.json"


def load_todos():
    """加载待办事项"""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_todos(todos):
    """保存待办事项"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def add_todo(text: str):
    """添加待办事项"""
    todos = load_todos()
    todo = {
        "id": len(todos) + 1,
        "text": text,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "done": False
    }
    todos.append(todo)
    save_todos(todos)
    print(f"[OK] 已添加：{text}")


def list_todos(show_done: bool = False):
    """列出待办事项"""
    todos = load_todos()
    if not todos:
        print("[INFO] 暂无待办事项")
        return
    
    print("\n" + "=" * 50)
    print("待办事项列表")
    print("=" * 50)
    
    pending = [t for t in todos if not t["done"]]
    done = [t for t in todos if t["done"]]
    
    if pending:
        print("\n[待完成]:")
        for t in pending:
            print(f"   [{t['id']}] {t['text']}")
            print(f"       {t['created_at']}")
    
    if show_done and done:
        print("\n[已完成]:")
        for t in done:
            print(f"   [{t['id']}] [x] {t['text']}")
    
    if not pending and not done:
        print("\n[INFO] 全部完成！")
    
    print("=" * 50 + "\n")


def mark_done(todo_id: int):
    """标记为完成"""
    todos = load_todos()
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = True
            save_todos(todos)
            print(f"[OK] 已完成：{todo['text']}")
            return
    print(f"[ERROR] 未找到 ID 为 {todo_id} 的待办事项")


def delete_todo(todo_id: int):
    """删除待办事项"""
    todos = load_todos()
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            deleted = todos.pop(i)
            save_todos(todos)
            print(f"[DEL] 已删除：{deleted['text']}")
            return
    print(f"[ERROR] 未找到 ID 为 {todo_id} 的待办事项")


def clear_done():
    """清除已完成的事项"""
    todos = load_todos()
    pending = [t for t in todos if not t["done"]]
    removed = len(todos) - len(pending)
    save_todos(pending)
    print(f"[CLR] 已清除 {removed} 个已完成的事项")


def print_help():
    """打印帮助信息"""
    help_text = """
=== 命令行待办事项管理器 ===

用法:
    python demo-todo.py add <内容>       添加待办事项
    python demo-todo.py list            列出所有事项
    python demo-todo.py done <ID>       标记为完成
    python demo-todo.py delete <ID>     删除事项
    python demo-todo.py clear           清除已完成
    python demo-todo.py help            显示帮助

示例:
    python demo-todo.py add "买牛奶"
    python demo-todo.py list
    python demo-todo.py done 1
"""
    print(help_text.encode('utf-8').decode('utf-8'))


def main():
    import sys
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "add":
        if len(sys.argv) < 3:
            print("[ERROR] 请提供待办内容")
            return
        text = " ".join(sys.argv[2:])
        add_todo(text)
    
    elif command == "list":
        show_done = "--done" in sys.argv
        list_todos(show_done)
    
    elif command == "done":
        if len(sys.argv) < 3:
            print("[ERROR] 请提供事项 ID")
            return
        try:
            mark_done(int(sys.argv[2]))
        except ValueError:
            print("[ERROR] ID 必须是数字")
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("[ERROR] 请提供事项 ID")
            return
        try:
            delete_todo(int(sys.argv[2]))
        except ValueError:
            print("[ERROR] ID 必须是数字")
    
    elif command == "clear":
        clear_done()
    
    elif command == "help":
        print_help()
    
    else:
        print(f"[ERROR] 未知命令：{command}")
        print_help()


if __name__ == "__main__":
    main()
