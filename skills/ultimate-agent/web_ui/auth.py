#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户认证模块 - User Authentication

功能：
- 用户登录/登出
- JWT Token 认证
- 密码加密存储
- 会话管理
- 权限验证

Phase 6.3 - 安全增强版
"""

import hashlib
import secrets
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass, asdict
import json

logger = logging.getLogger('auth')

# 尝试导入 jwt
try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    logger.warning("⚠️ PyJWT 未安装，请运行：pip install pyjwt")

# 尝试导入 bcrypt
try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False
    logger.warning("⚠️ bcrypt 未安装，请运行：pip install bcrypt")


@dataclass
class User:
    """用户数据类"""
    username: str
    password_hash: str
    email: str = ""
    role: str = "user"  # admin, user, guest
    created_at: str = None
    last_login: str = None
    is_active: bool = True
    password_changed_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.password_changed_at is None:
            self.password_changed_at = self.created_at


def validate_password_strength(password: str) -> tuple:
    """
    验证密码强度
    
    返回: (is_valid, message)
    """
    if len(password) < 8:
        return False, "密码长度至少 8 位"
    
    if len(password) > 128:
        return False, "密码长度不能超过 128 位"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    strength_count = sum([has_upper, has_lower, has_digit, has_special])
    
    if strength_count < 3:
        return False, "密码必须包含以下至少 3 种：大写字母、小写字母、数字、特殊字符"
    
    # 检查常见弱密码
    weak_passwords = ['password', 'admin', '123456', 'qwerty', 'letmein', 'welcome']
    if password.lower() in weak_passwords:
        return False, "密码过于常见，请使用更安全的密码"
    
    return True, "密码强度符合要求"


@dataclass
class AuthToken:
    """认证 Token"""
    token: str
    username: str
    expires_at: str
    role: str


class UserManager:
    """用户管理器"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(__file__).parent.parent / 'users'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.users_file = self.data_dir / 'users.json'
        self.users: Dict[str, User] = {}
        self.load_users()
    
    def load_users(self):
        """加载用户数据"""
        if self.users_file.exists():
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for username, user_data in data.items():
                        self.users[username] = User(**user_data)
                logger.info(f"✅ 已加载 {len(self.users)} 个用户")
            except Exception as e:
                logger.error(f"❌ 加载用户数据失败：{e}")
                self._create_default_admin()
        else:
            self._create_default_admin()
    
    def _create_default_admin(self):
        """创建默认管理员账户"""
        logger.info("📝 创建默认管理员账户...")
        admin = User(
            username='admin',
            password_hash=self._hash_password('admin123'),
            email='admin@localhost',
            role='admin',
            is_active=True
        )
        self.users['admin'] = admin
        self.save_users()
        logger.info("✅ 默认管理员已创建 (用户名：admin, 密码：admin123)")
    
    def save_users(self):
        """保存用户数据"""
        data = {username: asdict(user) for username, user in self.users.items()}
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _hash_password(self, password: str) -> str:
        """密码哈希"""
        if BCRYPT_AVAILABLE:
            salt = bcrypt.gensalt()
            return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        else:
            # 降级方案：SHA-256 + salt
            salt = secrets.token_hex(16)
            hash_obj = hashlib.sha256((salt + password).encode('utf-8'))
            return f"{salt}${hash_obj.hexdigest()}"
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """验证密码"""
        if BCRYPT_AVAILABLE:
            try:
                return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
            except:
                return False
        else:
            # 降级方案
            try:
                salt, hash_value = password_hash.split('$')
                hash_obj = hashlib.sha256((salt + password).encode('utf-8'))
                return hash_obj.hexdigest() == hash_value
            except:
                return False
    
    def create_user(self, username: str, password: str, email: str = "", role: str = "user") -> Optional[User]:
        """创建用户"""
        if username in self.users:
            logger.warning(f"用户已存在：{username}")
            return None
        
        user = User(
            username=username,
            password_hash=self._hash_password(password),
            email=email,
            role=role,
            is_active=True
        )
        self.users[username] = user
        self.save_users()
        logger.info(f"✅ 用户已创建：{username} (角色：{role})")
        return user
    
    def get_user(self, username: str) -> Optional[User]:
        """获取用户"""
        return self.users.get(username)
    
    def delete_user(self, username: str) -> bool:
        """删除用户"""
        if username in self.users and username != 'admin':
            del self.users[username]
            self.save_users()
            logger.info(f"🗑️ 用户已删除：{username}")
            return True
        return False
    
    def update_user(self, username: str, **kwargs) -> Optional[User]:
        """更新用户信息"""
        user = self.users.get(username)
        if not user:
            return None
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        self.save_users()
        return user
    
    def list_users(self) -> List[Dict]:
        """列出所有用户（不含密码）"""
        return [
            {
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'created_at': user.created_at,
                'last_login': user.last_login,
                'is_active': user.is_active
            }
            for user in self.users.values()
        ]


class AuthManager:
    """认证管理器"""
    
    def __init__(self, user_manager: UserManager, secret_key: str = None):
        self.user_manager = user_manager
        self.secret_key = secret_key or secrets.token_hex(32)
        self.token_expiry_hours = 24
        self.sessions: Dict[str, AuthToken] = {}
        
        # 登录失败限制（防爆破）
        self.failed_attempts: Dict[str, list] = {}  # username -> [timestamps]
        self.max_failed_attempts = 5
        self.lockout_duration_minutes = 30
        self.failed_attempt_window_minutes = 15
    
    def _check_lockout(self, username: str) -> tuple:
        """检查用户是否被锁定"""
        now = datetime.now()
        window_start = now - timedelta(minutes=self.failed_attempt_window_minutes)
        
        # 清理过期记录
        if username in self.failed_attempts:
            self.failed_attempts[username] = [
                t for t in self.failed_attempts[username]
                if t > window_start
            ]
        
        # 检查是否被锁定
        if username in self.failed_attempts:
            attempts = self.failed_attempts[username]
            if len(attempts) >= self.max_failed_attempts:
                # 检查锁定时间
                last_attempt = max(attempts)
                lockout_end = last_attempt + timedelta(minutes=self.lockout_duration_minutes)
                if now < lockout_end:
                    remaining = int((lockout_end - now).total_seconds() / 60)
                    return False, f"账户已锁定，请 {remaining} 分钟后再试"
                else:
                    # 锁定时间已过，重置
                    self.failed_attempts[username] = []
        
        return True, ""
    
    def _record_failed_attempt(self, username: str):
        """记录失败尝试"""
        now = datetime.now()
        if username not in self.failed_attempts:
            self.failed_attempts[username] = []
        self.failed_attempts[username].append(now)
    
    def _clear_failed_attempts(self, username: str):
        """清除失败记录（登录成功后）"""
        if username in self.failed_attempts:
            del self.failed_attempts[username]
    
    def login(self, username: str, password: str) -> tuple:
        """
        用户登录
        
        返回: (AuthToken, message) 或 (None, error_message)
        """
        # 检查是否被锁定
        is_allowed, lockout_msg = self._check_lockout(username)
        if not is_allowed:
            logger.warning(f"登录失败：账户已锁定 - {username}")
            return None, lockout_msg
        
        user = self.user_manager.get_user(username)
        
        if not user:
            self._record_failed_attempt(username)
            logger.warning(f"登录失败：用户不存在 - {username}")
            return None, "用户名或密码错误"
        
        if not user.is_active:
            self._record_failed_attempt(username)
            logger.warning(f"登录失败：用户已禁用 - {username}")
            return None, "账户已被禁用，请联系管理员"
        
        if not self.user_manager.verify_password(password, user.password_hash):
            self._record_failed_attempt(username)
            attempts_left = self.max_failed_attempts - len(self.failed_attempts.get(username, []))
            logger.warning(f"登录失败：密码错误 - {username} (剩余尝试：{attempts_left})")
            return None, f"用户名或密码错误 (剩余尝试：{attempts_left} 次)"
        
        # 登录成功，清除失败记录
        self._clear_failed_attempts(username)
        
        # 更新最后登录时间
        user.last_login = datetime.now().isoformat()
        self.user_manager.save_users()
        
        # 生成 Token
        token = self._generate_token(user)
        self.sessions[token.token] = token
        
        logger.info(f"✅ 用户登录成功：{username}")
        return token, "登录成功"
    
    def logout(self, token: str) -> bool:
        """用户登出"""
        if token in self.sessions:
            del self.sessions[token]
            logger.info("✅ 用户已登出")
            return True
        return False
    
    def _generate_token(self, user: User) -> AuthToken:
        """生成认证 Token"""
        expires_at = datetime.now() + timedelta(hours=self.token_expiry_hours)
        
        if JWT_AVAILABLE:
            # 使用 JWT
            payload = {
                'username': user.username,
                'role': user.role,
                'exp': expires_at,
                'iat': datetime.now()
            }
            token_str = jwt.encode(payload, self.secret_key, algorithm='HS256')
        else:
            # 降级方案：简单 Token
            token_str = secrets.token_urlsafe(32)
        
        return AuthToken(
            token=token_str,
            username=user.username,
            expires_at=expires_at.isoformat(),
            role=user.role
        )
    
    def verify_token(self, token: str) -> Optional[AuthToken]:
        """验证 Token"""
        # 检查会话
        if token in self.sessions:
            auth_token = self.sessions[token]
            expires_at = datetime.fromisoformat(auth_token.expires_at)
            if datetime.now() < expires_at:
                return auth_token
            else:
                del self.sessions[token]
                return None
        
        # 验证 JWT
        if JWT_AVAILABLE:
            try:
                payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
                user = self.user_manager.get_user(payload['username'])
                if user and user.is_active:
                    return AuthToken(
                        token=token,
                        username=user.username,
                        expires_at=payload['exp'],
                        role=payload['role']
                    )
            except jwt.ExpiredSignatureError:
                logger.warning("Token 已过期")
            except jwt.InvalidTokenError as e:
                logger.warning(f"Token 无效：{e}")
        
        return None
    
    def get_current_user(self, token: str) -> Optional[User]:
        """获取当前用户"""
        auth_token = self.verify_token(token)
        if auth_token:
            return self.user_manager.get_user(auth_token.username)
        return None
    
    def require_role(self, token: str, required_role: str) -> bool:
        """验证用户角色"""
        auth_token = self.verify_token(token)
        if not auth_token:
            return False
        
        role_hierarchy = {'guest': 0, 'user': 1, 'admin': 2}
        user_role = role_hierarchy.get(auth_token.role, 0)
        required = role_hierarchy.get(required_role, 0)
        
        return user_role >= required
    
    def refresh_token(self, token: str) -> Optional[AuthToken]:
        """Token 续期（延长有效期）"""
        auth_token = self.verify_token(token)
        if not auth_token:
            return None
        
        # 生成新 Token（延长 24 小时）
        user = self.user_manager.get_user(auth_token.username)
        if not user or not user.is_active:
            return None
        
        new_token = self._generate_token(user)
        self.sessions[new_token.token] = new_token
        
        # 撤销旧 Token
        if token in self.sessions:
            del self.sessions[token]
        
        logger.info(f"🔄 Token 已续期：{auth_token.username}")
        return new_token
    
    def change_password(self, username: str, old_password: str, new_password: str) -> tuple:
        """
        修改密码
        
        返回: (success, message)
        """
        # 验证新密码强度
        is_valid, strength_msg = validate_password_strength(new_password)
        if not is_valid:
            return False, strength_msg
        
        user = self.user_manager.get_user(username)
        if not user:
            return False, "用户不存在"
        
        # 验证旧密码
        if not self.user_manager.verify_password(old_password, user.password_hash):
            return False, "原密码错误"
        
        # 更新密码
        user.password_hash = self._hash_password(new_password)
        user.password_changed_at = datetime.now().isoformat()
        self.user_manager.save_users()
        
        # 撤销所有 Token（强制重新登录）
        sessions_to_remove = [t for t, auth in self.sessions.items() if auth.username == username]
        for t in sessions_to_remove:
            del self.sessions[t]
        
        logger.info(f"🔑 密码已修改：{username}")
        return True, "密码修改成功，请重新登录"


# 全局实例
_user_manager: Optional[UserManager] = None
_auth_manager: Optional[AuthManager] = None


def get_user_manager() -> UserManager:
    """获取用户管理器实例"""
    global _user_manager
    if _user_manager is None:
        _user_manager = UserManager()
    return _user_manager


def get_auth_manager() -> AuthManager:
    """获取认证管理器实例"""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager(get_user_manager())
    return _auth_manager


# Flask 集成
def init_auth(app):
    """初始化 Flask 应用认证"""
    from flask import request, jsonify, g
    
    user_manager = get_user_manager()
    auth_manager = get_auth_manager()
    
    @app.before_request
    def check_auth():
        """检查认证（排除公开路由）"""
        public_routes = ['/', '/index.html', '/login.html', '/api/login', '/api/register']
        
        if request.path.startswith('/api/') and request.path not in public_routes:
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            
            if not token:
                return jsonify({'error': '未授权', 'message': '请提供认证 Token'}), 401
            
            user = auth_manager.get_current_user(token)
            if not user:
                return jsonify({'error': '未授权', 'message': 'Token 无效或已过期'}), 401
            
            g.current_user = user
            g.current_token = token
    
    return user_manager, auth_manager
