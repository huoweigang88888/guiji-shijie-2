#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
备份系统 - 硅基世界 2

自动备份世界数据，防止数据丢失。
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class BackupManager:
    """备份管理器"""
    
    def __init__(self, backup_dir: str = "backups", max_backups: int = 10):
        """
        初始化备份管理器
        
        Args:
            backup_dir: 备份目录
            max_backups: 最大备份数量
        """
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        
        self.max_backups = max_backups
        self.backups: List[Dict] = []
        
        print(f"💾 备份系统已初始化 (目录：{self.backup_dir})")
    
    def create_backup(
        self,
        data: Dict,
        name: str = "",
        description: str = "",
    ) -> str:
        """
        创建备份
        
        Args:
            data: 备份数据
            name: 备份名称
            description: 描述
            
        Returns:
            备份文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = name if name else f"backup_{timestamp}"
        
        backup_file = self.backup_dir / f"{backup_name}.json"
        
        backup_data = {
            "timestamp": datetime.now().isoformat(),
            "name": backup_name,
            "description": description,
            "data": data,
        }
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)
        
        # 记录备份
        self.backups.append({
            "file": str(backup_file),
            "name": backup_name,
            "timestamp": backup_data["timestamp"],
            "size": backup_file.stat().st_size,
        })
        
        # 清理旧备份
        self._cleanup_old_backups()
        
        print(f"  💾 创建备份：{backup_name} ({backup_file.stat().st_size} 字节)")
        
        return str(backup_file)
    
    def restore_backup(self, backup_name: str) -> Optional[Dict]:
        """
        恢复备份
        
        Args:
            backup_name: 备份名称
            
        Returns:
            备份数据
        """
        backup_file = self.backup_dir / f"{backup_name}.json"
        
        if not backup_file.exists():
            print(f"  ❌ 备份不存在：{backup_name}")
            return None
        
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        print(f"  ♻️  恢复备份：{backup_name}")
        
        return backup_data.get("data", {})
    
    def list_backups(self) -> List[Dict]:
        """获取备份列表"""
        return sorted(self.backups, key=lambda x: x["timestamp"], reverse=True)
    
    def delete_backup(self, backup_name: str) -> bool:
        """删除备份"""
        backup_file = self.backup_dir / f"{backup_name}.json"
        
        if not backup_file.exists():
            return False
        
        backup_file.unlink()
        
        self.backups = [b for b in self.backups if b["name"] != backup_name]
        
        print(f"  🗑️  删除备份：{backup_name}")
        
        return True
    
    def _cleanup_old_backups(self):
        """清理旧备份"""
        if len(self.backups) <= self.max_backups:
            return
        
        # 删除最旧的备份
        backups_to_delete = self.backups[:-self.max_backups]
        
        for backup in backups_to_delete:
            backup_file = Path(backup["file"])
            if backup_file.exists():
                backup_file.unlink()
        
        self.backups = self.backups[-self.max_backups:]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total_size = sum(b.get("size", 0) for b in self.backups)
        
        return {
            "total_backups": len(self.backups),
            "total_size": total_size,
            "max_backups": self.max_backups,
            "latest_backup": self.backups[-1]["timestamp"] if self.backups else None,
        }
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stats": self.get_stats(),
            "backups": self.list_backups()[:5],
        }


# 单例
_backup_manager: Optional[BackupManager] = None


def get_backup_manager(backup_dir: str = "backups") -> BackupManager:
    """获取备份管理器单例"""
    global _backup_manager
    if _backup_manager is None:
        _backup_manager = BackupManager(backup_dir)
    return _backup_manager


# 工厂函数
def create_backup_manager(backup_dir: str = "backups") -> BackupManager:
    """创建备份管理器"""
    return BackupManager(backup_dir)
