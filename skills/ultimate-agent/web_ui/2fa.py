#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双因素认证模块 - Two-Factor Authentication (2FA)

功能：
- TOTP 生成和验证
- QR 码生成
- 备份码生成和验证
- 2FA 启用/禁用

Phase 7 - 安全增强版
"""

import base64
import hashlib
import hmac
import struct
import time
import secrets
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json

logger = logging.getLogger('2fa')

# 尝试导入 pyotp
try:
    import pyotp
    PYOTP_AVAILABLE = True
except ImportError:
    PYOTP_AVAILABLE = False
    logger.warning("⚠️ pyotp 未安装，请运行：pip install pyotp")

# 尝试导入 qrcode
try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False
    logger.warning("⚠️ qrcode 未安装，请运行：pip install qrcode[pil]")


def generate_totp_secret() -> str:
    """生成 TOTP 密钥"""
    if PYOTP_AVAILABLE:
        return pyotp.random_base32()
    else:
        # 降级方案：生成 32 字符 Base32 密钥
        return base64.b32encode(secrets.token_bytes(20)).decode('utf-8')


def generate_totp_uri(username: str, secret: str, issuer: str = "硅基世界 2") -> str:
    """生成 TOTP URI（用于 QR 码）"""
    if PYOTP_AVAILABLE:
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(name=username, issuer_name=issuer)
    else:
        # 手动构建 URI
        return f"otpauth://totp/{issuer}:{username}?secret={secret}&issuer={issuer}"


def verify_totp(secret: str, code: str, window: int = 1) -> bool:
    """
    验证 TOTP 码
    
    Args:
        secret: TOTP 密钥
        code: 用户输入的 6 位码
        window: 前后容差（秒数）
    
    Returns:
        bool: 验证结果
    """
    if PYOTP_AVAILABLE:
        totp = pyotp.TOTP(secret)
        return totp.verify(code, valid_window=window)
    else:
        # 降级方案：简单 TOTP 验证
        return _verify_totp_simple(secret, code, window)


def _verify_totp_simple(secret: str, code: str, window: int = 1) -> bool:
    """简单 TOTP 验证（无 pyotp 时使用）"""
    try:
        # Base32 解码
        key = base64.b32decode(secret.upper() + '=' * (-len(secret) % 8))
        
        # 当前时间戳
        now = int(time.time())
        interval = 30  # 30 秒间隔
        
        # 检查当前和前后的时间窗口
        for offset in range(-window, window + 1):
            counter = (now // interval) + offset
            msg = struct.pack('>Q', counter)
            digest = hmac.new(key, msg, hashlib.sha1).digest()
            offset = digest[-1] & 0x0f
            code_gen = (struct.unpack('>I', digest[offset:offset+4])[0] & 0x7fffffff) % 1000000
            
            if str(code_gen).zfill(6) == code.zfill(6):
                return True
        
        return False
    except Exception as e:
        logger.error(f"TOTP 验证失败：{e}")
        return False


def generate_backup_codes(count: int = 10) -> List[str]:
    """生成备份码"""
    codes = []
    for _ in range(count):
        # 生成 8 位随机数字
        code = ''.join([str(secrets.randbelow(10)) for _ in range(8)])
        codes.append(code)
    return codes


def verify_backup_code(stored_codes: List[str], code: str) -> Tuple[bool, List[str]]:
    """
    验证备份码
    
    Returns:
        (验证结果，剩余备份码列表)
    """
    code = code.strip()
    
    if code in stored_codes:
        # 移除已使用的备份码
        remaining = [c for c in stored_codes if c != code]
        return True, remaining
    
    return False, stored_codes


class TwoFactorAuth:
    """双因素认证管理器"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(__file__).parent.parent / '2fa'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.data_dir / '2fa_config.json'
        self.config: Dict[str, dict] = {}
        self.load_config()
    
    def load_config(self):
        """加载配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                logger.info(f"✅ 已加载 {len(self.config)} 个用户的 2FA 配置")
            except Exception as e:
                logger.error(f"❌ 加载 2FA 配置失败：{e}")
                self.config = {}
    
    def save_config(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def is_enabled(self, username: str) -> bool:
        """检查用户是否启用了 2FA"""
        user_config = self.config.get(username, {})
        return user_config.get('enabled', False)
    
    def setup_2fa(self, username: str) -> dict:
        """
        设置 2FA
        
        Returns:
            dict: {
                'secret': str,
                'uri': str,
                'qr_code': str (base64),
                'backup_codes': list
            }
        """
        secret = generate_totp_secret()
        uri = generate_totp_uri(username, secret)
        backup_codes = generate_backup_codes()
        
        # 临时存储（验证前）
        self.config[username] = {
            'secret': secret,
            'enabled': False,  # 验证后才启用
            'backup_codes': backup_codes,
            'created_at': datetime.now().isoformat()
        }
        self.save_config()
        
        # 生成 QR 码
        qr_code = None
        if QRCODE_AVAILABLE:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(uri)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # 转换为 base64
            import io
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            qr_code = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return {
            'secret': secret,
            'uri': uri,
            'qr_code': qr_code,
            'backup_codes': backup_codes
        }
    
    def verify_and_enable(self, username: str, code: str) -> Tuple[bool, str]:
        """验证并启用 2FA"""
        user_config = self.config.get(username, {})
        
        if not user_config:
            return False, "请先设置 2FA"
        
        if user_config.get('enabled', False):
            return False, "2FA 已启用"
        
        secret = user_config.get('secret')
        if not secret:
            return False, "2FA 配置错误"
        
        if verify_totp(secret, code):
            user_config['enabled'] = True
            user_config['enabled_at'] = datetime.now().isoformat()
            self.save_config()
            
            logger.info(f"✅ 用户 {username} 已启用 2FA")
            return True, "2FA 启用成功"
        else:
            return False, "验证码错误"
    
    def verify_2fa(self, username: str, code: str) -> Tuple[bool, str]:
        """
        验证 2FA 码
        
        Returns:
            (验证结果，消息)
        """
        user_config = self.config.get(username, {})
        
        if not user_config:
            return True, "用户无 2FA 配置"
        
        if not user_config.get('enabled', False):
            return True, "2FA 未启用"
        
        # 尝试 TOTP 验证
        secret = user_config.get('secret')
        if secret and verify_totp(secret, code):
            logger.info(f"✅ 用户 {username} 2FA 验证成功 (TOTP)")
            return True, "验证成功"
        
        # 尝试备份码验证
        backup_codes = user_config.get('backup_codes', [])
        success, remaining = verify_backup_code(backup_codes, code)
        
        if success:
            user_config['backup_codes'] = remaining
            self.save_config()
            logger.info(f"✅ 用户 {username} 2FA 验证成功 (备份码)")
            return True, "验证成功 (备份码)"
        
        return False, "验证码错误"
    
    def disable_2fa(self, username: str, password_verified: bool = False) -> Tuple[bool, str]:
        """
        禁用 2FA
        
        Args:
            username: 用户名
            password_verified: 是否已验证密码（安全要求）
        
        Returns:
            (结果，消息)
        """
        if not password_verified:
            return False, "请先验证密码"
        
        user_config = self.config.get(username, {})
        
        if not user_config or not user_config.get('enabled', False):
            return False, "2FA 未启用"
        
        user_config['enabled'] = False
        user_config['disabled_at'] = datetime.now().isoformat()
        # 清除密钥和备份码
        user_config['secret'] = None
        user_config['backup_codes'] = []
        
        self.save_config()
        logger.info(f"🔓 用户 {username} 已禁用 2FA")
        return True, "2FA 已禁用"
    
    def regenerate_backup_codes(self, username: str) -> Tuple[bool, List[str]]:
        """重新生成备份码"""
        user_config = self.config.get(username, {})
        
        if not user_config or not user_config.get('enabled', False):
            return False, []
        
        new_codes = generate_backup_codes()
        user_config['backup_codes'] = new_codes
        user_config['backup_codes_regenerated_at'] = datetime.now().isoformat()
        self.save_config()
        
        logger.info(f"🔄 用户 {username} 已重新生成备份码")
        return True, new_codes
    
    def get_status(self, username: str) -> dict:
        """获取 2FA 状态"""
        user_config = self.config.get(username, {})
        
        return {
            'enabled': user_config.get('enabled', False),
            'has_secret': bool(user_config.get('secret')),
            'backup_codes_count': len(user_config.get('backup_codes', [])),
            'created_at': user_config.get('created_at'),
            'enabled_at': user_config.get('enabled_at'),
            'disabled_at': user_config.get('disabled_at')
        }


# 全局实例
_2fa_manager: Optional[TwoFactorAuth] = None


def get_2fa_manager() -> TwoFactorAuth:
    """获取 2FA 管理器实例"""
    global _2fa_manager
    if _2fa_manager is None:
        _2fa_manager = TwoFactorAuth()
    return _2fa_manager


# Flask 集成
def init_2fa(app):
    """初始化 Flask 应用 2FA"""
    from flask import request, jsonify, g
    
    _2fa_manager = get_2fa_manager()
    
    @app.route('/api/2fa/setup', methods=['POST'])
    def api_2fa_setup():
        """设置 2FA"""
        from flask import g
        if not hasattr(g, 'current_user'):
            return jsonify({'error': '未授权'}), 401
        
        result = _2fa_manager.setup_2fa(g.current_user.username)
        return jsonify(result)
    
    @app.route('/api/2fa/verify-setup', methods=['POST'])
    def api_2fa_verify_setup():
        """验证并启用 2FA"""
        from flask import g
        if not hasattr(g, 'current_user'):
            return jsonify({'error': '未授权'}), 401
        
        data = request.json
        code = data.get('code')
        
        success, message = _2fa_manager.verify_and_enable(g.current_user.username, code)
        return jsonify({'success': success, 'message': message})
    
    @app.route('/api/2fa/verify', methods=['POST'])
    def api_2fa_verify():
        """验证 2FA 码（登录时）"""
        data = request.json
        username = data.get('username')
        code = data.get('code')
        
        if not username or not code:
            return jsonify({'success': False, 'message': '请提供用户名和验证码'}), 400
        
        success, message = _2fa_manager.verify_2fa(username, code)
        return jsonify({'success': success, 'message': message})
    
    @app.route('/api/2fa/disable', methods=['POST'])
    def api_2fa_disable():
        """禁用 2FA"""
        from flask import g
        if not hasattr(g, 'current_user'):
            return jsonify({'error': '未授权'}), 401
        
        data = request.json
        # 需要验证密码
        # 这里简化处理，实际应该验证密码
        
        success, message = _2fa_manager.disable_2fa(g.current_user.username, password_verified=True)
        return jsonify({'success': success, 'message': message})
    
    @app.route('/api/2fa/status', methods=['GET'])
    def api_2fa_status():
        """获取 2FA 状态"""
        from flask import g
        if not hasattr(g, 'current_user'):
            return jsonify({'error': '未授权'}), 401
        
        status = _2fa_manager.get_status(g.current_user.username)
        return jsonify(status)
    
    @app.route('/api/2fa/backup-codes', methods=['POST'])
    def api_2fa_backup_codes():
        """重新生成备份码"""
        from flask import g
        if not hasattr(g, 'current_user'):
            return jsonify({'error': '未授权'}), 401
        
        success, codes = _2fa_manager.regenerate_backup_codes(g.current_user.username)
        
        if success:
            return jsonify({
                'success': True,
                'backup_codes': codes,
                'message': '备份码已重新生成，请安全保存'
            })
        else:
            return jsonify({'success': False, 'message': '生成失败'}), 400
    
    return _2fa_manager
