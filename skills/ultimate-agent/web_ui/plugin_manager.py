#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
插件管理器 - Plugin Manager

功能：
- 插件加载/卸载
- 插件生命周期管理
- 插件事件系统
- 插件配置管理

Phase 7 - 插件系统基础版
"""

import importlib
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
import traceback

logger = logging.getLogger('plugin-manager')


@dataclass
class PluginInfo:
    """插件信息"""
    name: str
    version: str
    description: str
    author: str = "Unknown"
    enabled: bool = True
    loaded_at: str = None
    path: str = ""
    
    def __post_init__(self):
        if self.loaded_at is None:
            self.loaded_at = datetime.now().isoformat()


class Plugin:
    """插件基类"""
    
    name = "base_plugin"
    version = "1.0.0"
    description = "Base plugin"
    author = "Unknown"
    
    def __init__(self, manager: 'PluginManager'):
        self.manager = manager
        self.enabled = True
        self.config: Dict[str, Any] = {}
    
    def on_load(self):
        """插件加载时调用"""
        pass
    
    def on_unload(self):
        """插件卸载时调用"""
        pass
    
    def on_enable(self):
        """插件启用时调用"""
        pass
    
    def on_disable(self):
        """插件禁用时调用"""
        pass
    
    def on_event(self, event_type: str, data: Dict):
        """事件触发时调用"""
        pass
    
    def get_info(self) -> Dict:
        """获取插件信息"""
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'author': self.author,
            'enabled': self.enabled
        }


class PluginManager:
    """插件管理器"""
    
    def __init__(self, plugins_dir: Optional[Path] = None):
        self.plugins_dir = plugins_dir or Path(__file__).parent.parent / 'plugins'
        self.plugins_dir.mkdir(parents=True, exist_ok=True)
        
        self.plugins: Dict[str, Plugin] = {}
        self.plugin_info: Dict[str, PluginInfo] = {}
        self.event_handlers: Dict[str, List[Callable]] = {}
        
        self.config_file = self.plugins_dir / 'plugins_config.json'
        self.config: Dict[str, dict] = {}
        self.load_config()
    
    def load_config(self):
        """加载插件配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                logger.info(f"✅ 已加载 {len(self.config)} 个插件配置")
            except Exception as e:
                logger.error(f"❌ 加载插件配置失败：{e}")
                self.config = {}
    
    def save_config(self):
        """保存插件配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def discover_plugins(self) -> List[str]:
        """发现可用插件"""
        plugin_names = []
        
        if not self.plugins_dir.exists():
            return []
        
        for item in self.plugins_dir.iterdir():
            if item.is_dir() and not item.name.startswith('_') and item.name != '__pycache__':
                plugin_file = item / 'plugin.py'
                if plugin_file.exists():
                    plugin_names.append(item.name)
        
        logger.info(f"🔍 发现 {len(plugin_names)} 个插件")
        return plugin_names
    
    def load_plugin(self, name: str) -> bool:
        """加载插件"""
        if name in self.plugins:
            logger.warning(f"插件已加载：{name}")
            return False
        
        plugin_path = self.plugins_dir / name / 'plugin.py'
        
        if not plugin_path.exists():
            logger.error(f"插件文件不存在：{name}")
            return False
        
        try:
            # 动态导入插件
            spec = importlib.util.spec_from_file_location(f"plugins.{name}", plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # 获取插件类
            if hasattr(module, 'Plugin'):
                plugin_class = module.Plugin
                plugin = plugin_class(self)
                
                # 初始化插件
                plugin.name = getattr(module, 'name', name)
                plugin.version = getattr(module, 'version', '1.0.0')
                plugin.description = getattr(module, 'description', '')
                plugin.author = getattr(module, 'author', 'Unknown')
                
                # 加载配置
                plugin.config = self.config.get(name, {})
                
                # 调用 on_load
                plugin.on_load()
                
                # 注册插件
                self.plugins[name] = plugin
                self.plugin_info[name] = PluginInfo(
                    name=plugin.name,
                    version=plugin.version,
                    description=plugin.description,
                    author=plugin.author,
                    enabled=plugin.enabled,
                    path=str(plugin_path)
                )
                
                logger.info(f"✅ 插件已加载：{name} v{plugin.version}")
                return True
            else:
                logger.error(f"插件 {name} 缺少 Plugin 类")
                return False
                
        except Exception as e:
            logger.error(f"❌ 加载插件失败 {name}: {e}")
            logger.error(traceback.format_exc())
            return False
    
    def unload_plugin(self, name: str) -> bool:
        """卸载插件"""
        if name not in self.plugins:
            logger.warning(f"插件未加载：{name}")
            return False
        
        plugin = self.plugins[name]
        
        try:
            # 调用 on_unload
            plugin.on_unload()
            
            # 取消注册
            del self.plugins[name]
            del self.plugin_info[name]
            
            logger.info(f"🗑️ 插件已卸载：{name}")
            return True
        except Exception as e:
            logger.error(f"❌ 卸载插件失败 {name}: {e}")
            return False
    
    def enable_plugin(self, name: str) -> bool:
        """启用插件"""
        if name not in self.plugins:
            logger.warning(f"插件未加载：{name}")
            return False
        
        plugin = self.plugins[name]
        
        if plugin.enabled:
            return True
        
        try:
            plugin.on_enable()
            plugin.enabled = True
            self.plugin_info[name].enabled = True
            
            # 保存配置
            self.config[name]['enabled'] = True
            self.save_config()
            
            logger.info(f"✅ 插件已启用：{name}")
            return True
        except Exception as e:
            logger.error(f"❌ 启用插件失败 {name}: {e}")
            return False
    
    def disable_plugin(self, name: str) -> bool:
        """禁用插件"""
        if name not in self.plugins:
            logger.warning(f"插件未加载：{name}")
            return False
        
        plugin = self.plugins[name]
        
        if not plugin.enabled:
            return True
        
        try:
            plugin.on_disable()
            plugin.enabled = False
            self.plugin_info[name].enabled = False
            
            # 保存配置
            self.config[name]['enabled'] = False
            self.save_config()
            
            logger.info(f"⏸️ 插件已禁用：{name}")
            return True
        except Exception as e:
            logger.error(f"❌ 禁用插件失败 {name}: {e}")
            return False
    
    def load_all_plugins(self):
        """加载所有插件"""
        discovered = self.discover_plugins()
        loaded = 0
        
        for name in discovered:
            # 检查配置
            if name not in self.config:
                self.config[name] = {'enabled': True}
            
            if self.config[name].get('enabled', True):
                if self.load_plugin(name):
                    loaded += 1
        
        logger.info(f"📦 已加载 {loaded}/{len(discovered)} 个插件")
    
    def unload_all_plugins(self):
        """卸载所有插件"""
        for name in list(self.plugins.keys()):
            self.unload_plugin(name)
        logger.info("🗑️ 所有插件已卸载")
    
    def get_plugin(self, name: str) -> Optional[Plugin]:
        """获取插件实例"""
        return self.plugins.get(name)
    
    def get_plugin_info(self, name: str) -> Optional[Dict]:
        """获取插件信息"""
        if name in self.plugin_info:
            return asdict(self.plugin_info[name])
        return None
    
    def list_plugins(self) -> List[Dict]:
        """列出所有插件"""
        return [asdict(info) for info in self.plugin_info.values()]
    
    def register_event(self, event_type: str, handler: Callable):
        """注册事件处理器"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def unregister_event(self, event_type: str, handler: Callable):
        """注销事件处理器"""
        if event_type in self.event_handlers:
            try:
                self.event_handlers[event_type].remove(handler)
            except ValueError:
                pass
    
    def emit_event(self, event_type: str, data: Dict):
        """触发事件"""
        # 通知所有插件
        for plugin in self.plugins.values():
            if plugin.enabled:
                try:
                    plugin.on_event(event_type, data)
                except Exception as e:
                    logger.error(f"插件事件处理失败 {plugin.name}: {e}")
        
        # 通知注册的事件处理器
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    handler(event_type, data)
                except Exception as e:
                    logger.error(f"事件处理器失败 {event_type}: {e}")
        
        logger.debug(f"📢 事件触发：{event_type}")


# 全局实例
_plugin_manager: Optional[PluginManager] = None


def get_plugin_manager() -> PluginManager:
    """获取插件管理器实例"""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager


# Flask 集成
def init_plugins(app):
    """初始化 Flask 应用插件系统"""
    from flask import request, jsonify, g
    
    plugin_manager = get_plugin_manager()
    
    # 加载所有插件
    plugin_manager.load_all_plugins()
    
    @app.route('/api/plugins', methods=['GET'])
    def api_list_plugins():
        """获取插件列表"""
        return jsonify(plugin_manager.list_plugins())
    
    @app.route('/api/plugins/<name>', methods=['GET'])
    def api_get_plugin(name):
        """获取插件信息"""
        info = plugin_manager.get_plugin_info(name)
        if info:
            return jsonify(info)
        return jsonify({'error': '插件不存在'}), 404
    
    @app.route('/api/plugins/<name>/enable', methods=['POST'])
    def api_enable_plugin(name):
        """启用插件"""
        if plugin_manager.enable_plugin(name):
            return jsonify({'status': 'success', 'message': f'插件 {name} 已启用'})
        return jsonify({'status': 'error', 'message': '启用失败'}), 400
    
    @app.route('/api/plugins/<name>/disable', methods=['POST'])
    def api_disable_plugin(name):
        """禁用插件"""
        if plugin_manager.disable_plugin(name):
            return jsonify({'status': 'success', 'message': f'插件 {name} 已禁用'})
        return jsonify({'status': 'error', 'message': '禁用失败'}), 400
    
    @app.route('/api/plugins/<name>/reload', methods=['POST'])
    def api_reload_plugin(name):
        """重新加载插件"""
        plugin_manager.unload_plugin(name)
        if plugin_manager.load_plugin(name):
            return jsonify({'status': 'success', 'message': f'插件 {name} 已重新加载'})
        return jsonify({'status': 'error', 'message': '重新加载失败'}), 400
    
    return plugin_manager
