#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example Plugin - 示例插件

演示如何创建一个基本插件
"""

import logging
from datetime import datetime

# 插件元数据
name = "example_plugin"
version = "1.0.0"
description = "示例插件 - 演示插件系统基本功能"
author = "硅基世界 2"

logger = logging.getLogger('example-plugin')


class Plugin:
    """示例插件类"""
    
    def __init__(self, manager):
        self.manager = manager
        self.enabled = True
        self.config = {}
        self.event_count = 0
    
    def on_load(self):
        """插件加载时调用"""
        logger.info(f"🔌 {self.name} v{version} 已加载")
        print(f"[{self.name}] 插件已加载，当前时间：{datetime.now().strftime('%H:%M:%S')}")
    
    def on_unload(self):
        """插件卸载时调用"""
        logger.info(f"🗑️ {self.name} 已卸载")
        print(f"[{self.name}] 插件已卸载，共处理 {self.event_count} 个事件")
    
    def on_enable(self):
        """插件启用时调用"""
        logger.info(f"✅ {self.name} 已启用")
        print(f"[{self.name}] 插件已启用")
    
    def on_disable(self):
        """插件禁用时调用"""
        logger.info(f"⏸️ {self.name} 已禁用")
        print(f"[{self.name}] 插件已禁用")
    
    def on_event(self, event_type: str, data: dict):
        """
        事件触发时调用
        
        Args:
            event_type: 事件类型
            data: 事件数据
        """
        self.event_count += 1
        
        # 处理特定事件
        if event_type == 'user_login':
            username = data.get('username', 'unknown')
            logger.info(f"👤 用户登录：{username}")
            print(f"[{self.name}] 用户 {username} 登录成功")
        
        elif event_type == 'user_logout':
            username = data.get('username', 'unknown')
            logger.info(f"👋 用户登出：{username}")
            print(f"[{self.name}] 用户 {username} 登出")
        
        elif event_type == 'task_create':
            task_desc = data.get('description', 'unknown')
            logger.info(f"📝 任务创建：{task_desc}")
            print(f"[{self.name}] 新任务：{task_desc}")
        
        elif event_type == 'config_change':
            key = data.get('key', 'unknown')
            logger.info(f"⚙️ 配置变更：{key}")
            print(f"[{self.name}] 配置 {key} 已修改")
        
        else:
            logger.debug(f"📢 事件：{event_type}")
    
    def get_info(self) -> dict:
        """获取插件信息"""
        return {
            'name': self.name,
            'version': version,
            'description': description,
            'author': author,
            'enabled': self.enabled,
            'event_count': self.event_count
        }
