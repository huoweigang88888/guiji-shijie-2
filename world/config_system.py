#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置系统 - 硅基世界 2

管理世界的配置，支持动态修改。
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = "config.json"):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = Path(config_file)
        self.config: Dict[str, Any] = {}
        self.defaults: Dict[str, Any] = {}
        
        # 默认配置
        self._init_defaults()
        
        # 加载配置
        self._load_config()
        
        print(f"⚙️  配置系统已初始化 (文件：{self.config_file})")
    
    def _init_defaults(self):
        """初始化默认配置"""
        self.defaults = {
            # 世界设置
            "world": {
                "name": "硅基世界 2",
                "day_duration_seconds": 86.4,
                "auto_save": True,
                "auto_backup": True,
            },
            
            # Agent 设置
            "agents": {
                "max_agents": 100,
                "auto_start": True,
                "spontaneous_action_chance": 0.1,
            },
            
            # 经济设置
            "economy": {
                "initial_credits": 100.0,
                "knowledge_share_reward": 10.0,
                "celebration_reward": 5.0,
            },
            
            # 社交设置
            "social": {
                "max_friends": 50,
                "relationship_decay": False,
            },
            
            # 日志设置
            "logging": {
                "level": "info",
                "save_to_file": True,
                "console_output": True,
            },
            
            # 性能设置
            "performance": {
                "max_events_per_second": 100,
                "auto_cleanup": True,
            },
        }
    
    def _load_config(self):
        """加载配置"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            print(f"  ✓ 配置已加载")
        else:
            self.config = {}
            self._save_config()
            print(f"  ✓ 创建默认配置")
    
    def _save_config(self):
        """保存配置"""
        self.config_file.parent.mkdir(exist_ok=True)
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键（支持点分隔，如 "world.name"）
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                # 尝试从默认配置获取
                default_value = self.defaults
                for dk in keys:
                    if isinstance(default_value, dict) and dk in default_value:
                        default_value = default_value[dk]
                    else:
                        return default
                return default_value
        
        return value
    
    def set(self, key: str, value: Any, save: bool = True):
        """
        设置配置值
        
        Args:
            key: 配置键
            value: 配置值
            save: 是否保存
        """
        keys = key.split(".")
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        
        if save:
            self._save_config()
        
        print(f"  ⚙️  配置更新：{key} = {value}")
    
    def reset(self, key: str):
        """
        重置配置为默认值
        
        Args:
            key: 配置键
        """
        keys = key.split(".")
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                return
            config = config[k]
        
        if keys[-1] in config:
            del config[keys[-1]]
        
        self._save_config()
        print(f"  ♻️  配置重置：{key}")
    
    def get_all(self) -> Dict:
        """获取所有配置"""
        # 合并默认配置和自定义配置
        result = self.defaults.copy()
        
        def merge(base: Dict, override: Dict):
            for key, value in override.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    merge(base[key], value)
                else:
                    base[key] = value
        
        merge(result, self.config)
        
        return result
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "config_file": str(self.config_file),
            "custom_settings": len(self._count_keys(self.config)),
            "total_settings": len(self._count_keys(self.get_all())),
        }
    
    def _count_keys(self, d: Dict, prefix: str = "") -> Dict:
        """计算配置键数量"""
        keys = {}
        for key, value in d.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                keys.update(self._count_keys(value, full_key))
            else:
                keys[full_key] = value
        return keys
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "config": self.get_all(),
        }


# 单例
_config_manager: Optional[ConfigManager] = None


def get_config_manager(config_file: str = "config.json") -> ConfigManager:
    """获取配置管理器单例"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(config_file)
    return _config_manager


# 工厂函数
def create_config_manager(config_file: str = "config.json") -> ConfigManager:
    """创建配置管理器"""
    return ConfigManager(config_file)
