#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理中心 - Config Manager

功能：
- 统一配置管理
- 环境变量支持
- 配置热重载
- 配置验证

提供安全、灵活的配置管理方案。
"""

import json
import os
import logging
import threading
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger('config-manager')


class ConfigType(Enum):
    """配置类型"""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"


@dataclass
class ConfigSchema:
    """配置模式"""
    key: str
    type: ConfigType
    required: bool = False
    default: Any = None
    min_value: Any = None
    max_value: Any = None
    description: str = ""
    env_var: Optional[str] = None


@dataclass
class ConfigValue:
    """配置值"""
    key: str
    value: Any
    source: str = "default"  # default, file, env, runtime
    updated_at: str = None
    
    def __post_init__(self):
        if self.updated_at is None:
            self.updated_at = datetime.now().isoformat()


class ConfigValidator:
    """配置验证器"""
    
    def __init__(self, schemas: List[ConfigSchema]):
        self.schemas = {s.key: s for s in schemas}
    
    def validate(self, key: str, value: Any) -> bool:
        """验证配置值"""
        if key not in self.schemas:
            logger.warning(f"未知配置项：{key}")
            return True  # 允许未知配置项
        
        schema = self.schemas[key]
        
        # 类型检查
        type_map = {
            ConfigType.STRING: str,
            ConfigType.INTEGER: int,
            ConfigType.FLOAT: (int, float),
            ConfigType.BOOLEAN: bool,
            ConfigType.LIST: list,
            ConfigType.DICT: dict
        }
        
        expected_type = type_map.get(schema.type)
        if expected_type and not isinstance(value, expected_type):
            logger.error(f"配置项 {key} 类型错误：期望 {schema.type.value}, 得到 {type(value).__name__}")
            return False
        
        # 范围检查
        if schema.min_value is not None and value < schema.min_value:
            logger.error(f"配置项 {key} 值过小：{value} < {schema.min_value}")
            return False
        
        if schema.max_value is not None and value > schema.max_value:
            logger.error(f"配置项 {key} 值过大：{value} > {schema.max_value}")
            return False
        
        return True
    
    def get_default(self, key: str) -> Any:
        """获取默认值"""
        if key in self.schemas:
            return self.schemas[key].default
        return None


class ConfigManager:
    """
    配置管理中心
    
    支持：
    - 多源配置（文件、环境变量、运行时）
    - 配置验证
    - 热重载
    - 变更回调
    """
    
    def __init__(self, config_dir: Path = None, auto_load_env: bool = True):
        self.config_dir = config_dir or Path(__file__).parent.parent / "configs"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / "config.json"
        self.schemas: Dict[str, ConfigSchema] = {}
        self.values: Dict[str, ConfigValue] = {}
        self.callbacks: Dict[str, List[Callable]] = {}
        
        self.validator: Optional[ConfigValidator] = None
        self.auto_load_env = auto_load_env
        
        self._lock = threading.RLock()
        self._watch_thread: Optional[threading.Thread] = None
        self._watching = False
        self._last_modified: float = 0
        
        self._load()
    
    def register_schema(self, schema: ConfigSchema):
        """注册配置模式"""
        self.schemas[schema.key] = schema
        logger.debug(f"已注册配置模式：{schema.key}")
    
    def register_schemas(self, schemas: List[ConfigSchema]):
        """批量注册配置模式"""
        for schema in schemas:
            self.register_schema(schema)
        self.validator = ConfigValidator(schemas)
        logger.info(f"已注册 {len(schemas)} 个配置模式")
    
    def _load(self):
        """加载配置"""
        with self._lock:
            # 1. 加载默认值
            for key, schema in self.schemas.items():
                if schema.default is not None:
                    self.values[key] = ConfigValue(
                        key=key,
                        value=schema.default,
                        source="default"
                    )
            
            # 2. 加载文件配置
            if self.config_file.exists():
                try:
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        file_config = json.load(f)
                    
                    for key, value in file_config.items():
                        self._set_value(key, value, "file", persist=False)
                    
                    self._last_modified = self.config_file.stat().st_mtime
                    logger.info(f"已加载配置文件：{self.config_file}")
                except Exception as e:
                    logger.error(f"加载配置文件失败：{e}")
            
            # 3. 加载环境变量
            if self.auto_load_env:
                for key, schema in self.schemas.items():
                    if schema.env_var and schema.env_var in os.environ:
                        value = os.environ[schema.env_var]
                        
                        # 类型转换
                        if schema.type == ConfigType.INTEGER:
                            value = int(value)
                        elif schema.type == ConfigType.FLOAT:
                            value = float(value)
                        elif schema.type == ConfigType.BOOLEAN:
                            value = value.lower() in ['true', '1', 'yes']
                        elif schema.type in [ConfigType.LIST, ConfigType.DICT]:
                            value = json.loads(value)
                        
                        self._set_value(key, value, "env", persist=False)
            
            logger.info(f"配置加载完成，共 {len(self.values)} 项")
    
    def _set_value(self, key: str, value: Any, source: str, persist: bool = True):
        """设置配置值（内部方法）"""
        # 验证
        if self.validator and not self.validator.validate(key, value):
            logger.warning(f"配置验证失败：{key} = {value}")
            return False
        
        # 更新
        old_value = self.values.get(key)
        self.values[key] = ConfigValue(key=key, value=value, source=source)
        
        # 触发回调
        if key in self.callbacks:
            for callback in self.callbacks[key]:
                try:
                    callback(key, old_value.value if old_value else None, value)
                except Exception as e:
                    logger.error(f"配置回调失败：{e}")
        
        # 持久化
        if persist and source == "runtime":
            self._save()
        
        return True
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        with self._lock:
            if key in self.values:
                return self.values[key].value
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """设置配置值"""
        with self._lock:
            return self._set_value(key, value, "runtime", persist=True)
    
    def delete(self, key: str) -> bool:
        """删除配置值"""
        with self._lock:
            if key in self.values:
                del self.values[key]
                self._save()
                logger.info(f"已删除配置：{key}")
                return True
            return False
    
    def _save(self):
        """保存配置到文件"""
        with self._lock:
            # 只保存 runtime 和 file 来源的配置
            file_config = {
                k: v.value for k, v in self.values.items()
                if v.source in ["runtime", "file"]
            }
            
            try:
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(file_config, f, ensure_ascii=False, indent=2)
                
                self._last_modified = self.config_file.stat().st_mtime
                logger.debug("配置已保存")
            except Exception as e:
                logger.error(f"保存配置失败：{e}")
    
    def on_change(self, key: str, callback: Callable):
        """注册配置变更回调"""
        if key not in self.callbacks:
            self.callbacks[key] = []
        self.callbacks[key].append(callback)
        logger.debug(f"已注册配置回调：{key}")
    
    def reload(self):
        """重新加载配置"""
        with self._lock:
            logger.info("重新加载配置...")
            self._load()
    
    def start_watching(self, interval: float = 5.0):
        """启动配置监听（热重载）"""
        if self._watching:
            return
        
        self._watching = True
        
        def watch_loop():
            logger.info("配置监听启动")
            
            while self._watching:
                try:
                    if self.config_file.exists():
                        current_mtime = self.config_file.stat().st_mtime
                        
                        if current_mtime > self._last_modified:
                            logger.info("检测到配置变更，自动重载")
                            self._load()
                        
                        self._last_modified = current_mtime
                except Exception as e:
                    logger.error(f"配置监听出错：{e}")
                
                time.sleep(interval)
            
            logger.info("配置监听停止")
        
        self._watch_thread = threading.Thread(target=watch_loop, daemon=True)
        self._watch_thread.start()
    
    def stop_watching(self):
        """停止配置监听"""
        self._watching = False
        if self._watch_thread:
            self._watch_thread.join(timeout=5)
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有配置"""
        with self._lock:
            return {k: v.value for k, v in self.values.items()}
    
    def get_status(self) -> Dict[str, Any]:
        """获取配置状态"""
        with self._lock:
            return {
                "total_configs": len(self.values),
                "config_file": str(self.config_file),
                "file_exists": self.config_file.exists(),
                "watching": self._watching,
                "sources": {
                    "default": sum(1 for v in self.values.values() if v.source == "default"),
                    "file": sum(1 for v in self.values.values() if v.source == "file"),
                    "env": sum(1 for v in self.values.values() if v.source == "env"),
                    "runtime": sum(1 for v in self.values.values() if v.source == "runtime"),
                }
            }
    
    def export(self, output_file: Path) -> bool:
        """导出配置"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.get_all(), f, ensure_ascii=False, indent=2)
            logger.info(f"配置已导出：{output_file}")
            return True
        except Exception as e:
            logger.error(f"导出配置失败：{e}")
            return False
    
    def import_config(self, input_file: Path, merge: bool = True) -> bool:
        """导入配置"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                imported = json.load(f)
            
            with self._lock:
                if not merge:
                    self.values.clear()
                
                for key, value in imported.items():
                    self._set_value(key, value, "file", persist=False)
                
                self._save()
            
            logger.info(f"配置已导入：{input_file}")
            return True
        except Exception as e:
            logger.error(f"导入配置失败：{e}")
            return False


# 预定义的系统配置模式
SYSTEM_SCHEMAS = [
    ConfigSchema("system.name", ConfigType.STRING, default="硅基世界 2", description="系统名称"),
    ConfigSchema("system.version", ConfigType.STRING, default="1.0.0", description="系统版本"),
    ConfigSchema("system.debug", ConfigType.BOOLEAN, default=False, description="调试模式", env_var="GUIJI_DEBUG"),
    
    ConfigSchema("workspace.path", ConfigType.STRING, default="", description="工作空间路径", env_var="GUIJI_WORKSPACE"),
    ConfigSchema("workspace.auto_save", ConfigType.BOOLEAN, default=True, description="自动保存"),
    
    ConfigSchema("agent.max_concurrent", ConfigType.INTEGER, default=5, min_value=1, max_value=20, description="最大并发代理数"),
    ConfigSchema("agent.timeout", ConfigType.INTEGER, default=300, min_value=10, description="代理超时时间（秒）"),
    
    ConfigSchema("logging.level", ConfigType.STRING, default="INFO", description="日志级别"),
    ConfigSchema("logging.file", ConfigType.STRING, default="", description="日志文件路径"),
    
    ConfigSchema("api.retry_count", ConfigType.INTEGER, default=3, min_value=0, max_value=10, description="API 重试次数"),
    ConfigSchema("api.timeout", ConfigType.INTEGER, default=30, min_value=5, description="API 超时时间（秒）"),
]


def create_default_config_manager() -> ConfigManager:
    """创建默认配置管理器"""
    manager = ConfigManager()
    manager.register_schemas(SYSTEM_SCHEMAS)
    return manager


if __name__ == "__main__":
    # 测试
    logging.basicConfig(level=logging.INFO)
    
    manager = create_default_config_manager()
    
    print("配置管理器测试")
    print("=" * 40)
    print(f"系统名称：{manager.get('system.name')}")
    print(f"调试模式：{manager.get('system.debug')}")
    print(f"最大并发：{manager.get('agent.max_concurrent')}")
    
    print("\n配置状态:")
    print(json.dumps(manager.get_status(), indent=2, ensure_ascii=False))
    
    # 测试设置
    manager.set("system.debug", True)
    print(f"\n调试模式已设置为：{manager.get('system.debug')}")
    
    # 测试回调
    def on_debug_change(key, old_value, new_value):
        print(f"配置变更：{key} = {old_value} -> {new_value}")
    
    manager.on_change("system.debug", on_debug_change)
    manager.set("system.debug", False)
