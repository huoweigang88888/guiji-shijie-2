#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Dashboard - 硅基世界 2 Web 仪表板 (Phase 6.1 - WebSocket 增强版)

轻量级 Web 界面，用于监控系统状态和管理任务
支持 WebSocket 实时推送
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

# Windows 编码支持
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 尝试导入 Flask
try:
    from flask import Flask, render_template, jsonify, request
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("[WARN] Flask 未安装，请运行：pip install flask")

# 尝试导入 Flask-SocketIO
try:
    from flask_socketio import SocketIO
    SOCKETIO_AVAILABLE = True
except ImportError:
    SOCKETIO_AVAILABLE = False

# 添加 agents 目录到路径
agents_dir = Path(__file__).parent.parent / "agents"
sys.path.insert(0, str(agents_dir))

# 导入 WebSocket 管理器
try:
    from websocket_manager import WebSocketManager, init_websocket
except ImportError:
    WebSocketManager = None
    init_websocket = None

# 导入认证模块
try:
    from auth import get_user_manager, get_auth_manager, init_auth, EVENT_LOGIN, EVENT_LOGOUT
    AUTH_AVAILABLE = True
except ImportError:
    AUTH_AVAILABLE = False
    get_user_manager = None
    get_auth_manager = None
    init_auth = None
    EVENT_LOGIN = 'login'
    EVENT_LOGOUT = 'logout'

# 导入审计日志模块
try:
    from audit_log import get_audit_logger, init_audit_logging
    AUDIT_AVAILABLE = True
except ImportError:
    AUDIT_AVAILABLE = False
    get_audit_logger = None
    init_audit_logging = None

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('web-ui')


def create_app(system_instance=None):
    """
    创建 Flask 应用
    
    Args:
        system_instance: GuijiWorld2 系统实例（可选）
    """
    if not FLASK_AVAILABLE:
        return None
    
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    app.config['SECRET_KEY'] = 'guiji-world-2-secret-key-phase61'
    
    # 系统实例
    system = system_instance
    
    # 初始化认证
    user_manager = None
    auth_manager = None
    
    if AUTH_AVAILABLE:
        user_manager, auth_manager = init_auth(app)
        logger.info("✅ 用户认证已启用")
    else:
        logger.warning("⚠️ 用户认证不可用")
    
    # 初始化审计日志
    audit_logger = None
    
    if AUDIT_AVAILABLE:
        audit_logger = init_audit_logging(app)
        logger.info("✅ 审计日志已启用")
    else:
        logger.warning("⚠️ 审计日志不可用")
    
    # 初始化 WebSocket
    ws_manager = None
    socketio = None
    
    if SOCKETIO_AVAILABLE and WebSocketManager:
        ws_manager = WebSocketManager(app)
        ws_manager.set_system(system)
        socketio = ws_manager.socketio
        logger.info("✅ WebSocket 已启用")
    else:
        logger.warning("⚠️ WebSocket 不可用，将使用轮询模式")
    
    # 存储到 app config 供路由使用
    app.config['ws_manager'] = ws_manager
    app.config['socketio'] = socketio
    app.config['system'] = system
    
    # ========== 路由 ==========
    
    @app.route('/')
    def index():
        """仪表板首页"""
        return render_template('index.html', websocket_enabled=SOCKETIO_AVAILABLE)
    
    @app.route('/agents.html')
    def agents():
        """代理管理页面"""
        return render_template('agents.html', websocket_enabled=SOCKETIO_AVAILABLE)
    
    @app.route('/tasks.html')
    def tasks():
        """任务队列页面"""
        return render_template('tasks.html', websocket_enabled=SOCKETIO_AVAILABLE)
    
    @app.route('/graph.html')
    def graph():
        """知识图谱页面"""
        return render_template('graph.html', websocket_enabled=SOCKETIO_AVAILABLE)
    
    @app.route('/logs.html')
    def logs():
        """日志查看器页面"""
        return render_template('logs.html', websocket_enabled=SOCKETIO_AVAILABLE)
    
    @app.route('/config.html')
    def config():
        """代理配置页面"""
        return render_template('config.html', websocket_enabled=SOCKETIO_AVAILABLE)
    
    @app.route('/notifications.html')
    def notifications():
        """通知中心页面"""
        return render_template('notifications.html', websocket_enabled=SOCKETIO_AVAILABLE)
    
    @app.route('/reports.html')
    def reports():
        """报告预览页面"""
        return render_template('reports.html', websocket_enabled=SOCKETIO_AVAILABLE)
    
    @app.route('/login.html')
    def login_page():
        """登录页面"""
        return render_template('login.html')
    
    @app.route('/settings.html')
    def settings():
        """账户设置页面"""
        return render_template('settings.html', websocket_enabled=SOCKETIO_AVAILABLE)
    
    @app.route('/2fa.html')
    def two_fa():
        """双因素认证页面"""
        return render_template('2fa.html', websocket_enabled=SOCKETIO_AVAILABLE)
    
    @app.route('/api/password-strength', methods=['POST'])
    def api_check_password_strength():
        """检查密码强度"""
        if not AUTH_AVAILABLE:
            return jsonify({'error': '认证模块不可用'}), 503
        
        from auth import validate_password_strength
        data = request.json
        password = data.get('password', '')
        
        is_valid, message = validate_password_strength(password)
        return jsonify({
            'valid': is_valid,
            'message': message
        })
    
    @app.route('/api/login', methods=['POST'])
    def api_login():
        """用户登录 API"""
        if not AUTH_AVAILABLE:
            return jsonify({'error': '认证模块不可用'}), 503
        
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'message': '请提供用户名和密码'}), 400
        
        auth_manager = get_auth_manager()
        token, message = auth_manager.login(username, password)
        
        if token:
            # 审计日志
            if AUDIT_AVAILABLE:
                audit_logger = get_audit_logger()
                audit_logger.log(
                    event_type=EVENT_LOGIN,
                    action='user_login',
                    username=username,
                    resource='/api/login',
                    ip_address=request.remote_addr or '',
                    user_agent=request.headers.get('User-Agent', '')
                )
            
            return jsonify({
                'status': 'success',
                'message': message,
                'token': token.token,
                'username': token.username,
                'role': token.role,
                'expires_at': token.expires_at
            })
        else:
            return jsonify({'status': 'error', 'message': message}), 401
    
    @app.route('/api/logout', methods=['POST'])
    def api_logout():
        """用户登出 API"""
        if not AUTH_AVAILABLE:
            return jsonify({'error': '认证模块不可用'}), 503
        
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        auth_manager = get_auth_manager()
        
        # 获取用户名用于审计
        auth_token = auth_manager.verify_token(token)
        username = auth_token.username if auth_token else 'unknown'
        
        auth_manager.logout(token)
        
        # 审计日志
        if AUDIT_AVAILABLE:
            audit_logger = get_audit_logger()
            from flask import g
            audit_logger.log(
                event_type=EVENT_LOGOUT,
                action='user_logout',
                username=username,
                resource='/api/logout',
                ip_address=request.remote_addr or '',
                user_agent=request.headers.get('User-Agent', '')
            )
        
        return jsonify({'status': 'success'})
    
    @app.route('/api/auth/refresh', methods=['POST'])
    def api_refresh_token():
        """Token 续期 API"""
        if not AUTH_AVAILABLE:
            return jsonify({'error': '认证模块不可用'}), 503
        
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        auth_manager = get_auth_manager()
        new_token = auth_manager.refresh_token(token)
        
        if new_token:
            return jsonify({
                'status': 'success',
                'token': new_token.token,
                'expires_at': new_token.expires_at
            })
        else:
            return jsonify({'status': 'error', 'message': 'Token 无效或已过期'}), 401
    
    @app.route('/api/auth/change-password', methods=['POST'])
    def api_change_password():
        """修改密码 API"""
        if not AUTH_AVAILABLE:
            return jsonify({'error': '认证模块不可用'}), 503
        
        from flask import g
        if not hasattr(g, 'current_user'):
            return jsonify({'status': 'error', 'message': '未授权'}), 401
        
        data = request.json
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            return jsonify({'status': 'error', 'message': '请提供原密码和新密码'}), 400
        
        auth_manager = get_auth_manager()
        success, message = auth_manager.change_password(
            g.current_user.username,
            old_password,
            new_password
        )
        
        if success:
            # 审计日志
            if AUDIT_AVAILABLE:
                audit_logger = get_audit_logger()
                audit_logger.log(
                    event_type='password_change',
                    action='change_password',
                    username=g.current_user.username,
                    resource='/api/auth/change-password',
                    ip_address=request.remote_addr or '',
                    user_agent=request.headers.get('User-Agent', '')
                )
            
            return jsonify({'status': 'success', 'message': message})
        else:
            return jsonify({'status': 'error', 'message': message}), 400
    
    @app.route('/api/auth/verify', methods=['GET'])
    def api_verify_auth():
        """验证 Token"""
        if not AUTH_AVAILABLE:
            return jsonify({'valid': False, 'error': '认证模块不可用'}), 503
        
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        auth_manager = get_auth_manager()
        auth_token = auth_manager.verify_token(token)
        
        if auth_token:
            return jsonify({
                'valid': True,
                'username': auth_token.username,
                'role': auth_token.role
            })
        else:
            return jsonify({'valid': False}), 401
    
    @app.route('/api/users', methods=['GET'])
    def api_get_users():
        """获取用户列表（需要管理员权限）"""
        if not AUTH_AVAILABLE:
            return jsonify({'error': '认证模块不可用'}), 503
        
        from flask import g
        if not hasattr(g, 'current_user') or g.current_user.role != 'admin':
            return jsonify({'error': '需要管理员权限'}), 403
        
        user_manager = get_user_manager()
        return jsonify(user_manager.list_users())
    
    @app.route('/api/users', methods=['POST'])
    def api_create_user():
        """创建用户（需要管理员权限）"""
        if not AUTH_AVAILABLE:
            return jsonify({'error': '认证模块不可用'}), 503
        
        from flask import g
        if not hasattr(g, 'current_user') or g.current_user.role != 'admin':
            return jsonify({'error': '需要管理员权限'}), 403
        
        data = request.json
        username = data.get('username')
        password = data.get('password')
        email = data.get('email', '')
        role = data.get('role', 'user')
        
        if not username or not password:
            return jsonify({'status': 'error', 'message': '用户名和密码必填'}), 400
        
        user_manager = get_user_manager()
        user = user_manager.create_user(username, password, email, role)
        
        if user:
            # 审计日志
            audit_logger = get_audit_logger()
            audit_logger.log(
                event_type='user_create',
                action=f'create_user:{username}',
                username=g.current_user.username,
                resource=f'/api/users/{username}',
                details={'role': role, 'email': email},
                ip_address=request.remote_addr or ''
            )
            return jsonify({'status': 'success', 'message': f'用户 {username} 已创建'})
        else:
            return jsonify({'status': 'error', 'message': '用户已存在'}), 400
    
    @app.route('/api/users/<username>/status', methods=['POST'])
    def api_toggle_user_status(username):
        """切换用户状态（需要管理员权限）"""
        if not AUTH_AVAILABLE:
            return jsonify({'error': '认证模块不可用'}), 503
        
        from flask import g
        if not hasattr(g, 'current_user') or g.current_user.role != 'admin':
            return jsonify({'error': '需要管理员权限'}), 403
        
        if username == 'admin':
            return jsonify({'status': 'error', 'message': '不能修改默认管理员状态'}), 400
        
        data = request.json
        is_active = data.get('is_active', True)
        
        user_manager = get_user_manager()
        user = user_manager.update_user(username, is_active=is_active)
        
        if user:
            audit_logger = get_audit_logger()
            audit_logger.log(
                event_type='user_update',
                action=f'toggle_status:{username}',
                username=g.current_user.username,
                resource=f'/api/users/{username}/status',
                details={'is_active': is_active},
                ip_address=request.remote_addr or ''
            )
            return jsonify({'status': 'success', 'message': f'用户 {username} 已{"启用" if is_active else "禁用"}'})
        else:
            return jsonify({'status': 'error', 'message': '用户不存在'}), 404
    
    @app.route('/api/users/<username>', methods=['DELETE'])
    def api_delete_user(username):
        """删除用户（需要管理员权限）"""
        if not AUTH_AVAILABLE:
            return jsonify({'error': '认证模块不可用'}), 503
        
        from flask import g
        if not hasattr(g, 'current_user') or g.current_user.role != 'admin':
            return jsonify({'error': '需要管理员权限'}), 403
        
        if username == 'admin':
            return jsonify({'status': 'error', 'message': '不能删除默认管理员'}), 400
        
        user_manager = get_user_manager()
        success = user_manager.delete_user(username)
        
        if success:
            audit_logger = get_audit_logger()
            audit_logger.log(
                event_type='user_delete',
                action=f'delete_user:{username}',
                username=g.current_user.username,
                resource=f'/api/users/{username}',
                ip_address=request.remote_addr or ''
            )
            return jsonify({'status': 'success', 'message': f'用户 {username} 已删除'})
        else:
            return jsonify({'status': 'error', 'message': '用户不存在'}), 404
    
    @app.route('/api/audit/logs', methods=['GET'])
    def api_get_audit_logs():
        """获取审计日志（需要管理员权限）"""
        if not AUTH_AVAILABLE:
            return jsonify({'error': '认证模块不可用'}), 503
        
        from flask import g
        if not hasattr(g, 'current_user') or g.current_user.role != 'admin':
            return jsonify({'error': '需要管理员权限'}), 403
        
        audit_logger = get_audit_logger()
        
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        event_type = request.args.get('event_type')
        username = request.args.get('username')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        search = request.args.get('search')
        
        if search:
            logs = audit_logger.search(search, limit)
        else:
            logs = audit_logger.get_entries(
                limit=limit,
                offset=offset,
                event_type=event_type,
                username=username,
                start_date=start_date,
                end_date=end_date
            )
        
        return jsonify({'logs': logs, 'total': len(logs)})
    
    @app.route('/api/audit/stats', methods=['GET'])
    def api_get_audit_stats():
        """获取审计统计（需要管理员权限）"""
        if not AUTH_AVAILABLE:
            return jsonify({'error': '认证模块不可用'}), 503
        
        from flask import g
        if not hasattr(g, 'current_user') or g.current_user.role != 'admin':
            return jsonify({'error': '需要管理员权限'}), 403
        
        audit_logger = get_audit_logger()
        days = request.args.get('days', 7, type=int)
        return jsonify(audit_logger.get_statistics(days=days))
    
    @app.route('/api/audit/export', methods=['GET'])
    def api_export_audit():
        """导出审计日志（需要管理员权限）"""
        if not AUTH_AVAILABLE:
            return jsonify({'error': '认证模块不可用'}), 503
        
        from flask import g, send_file
        if not hasattr(g, 'current_user') or g.current_user.role != 'admin':
            return jsonify({'error': '需要管理员权限'}), 403
        
        audit_logger = get_audit_logger()
        output_file = audit_logger.data_dir / 'export.csv'
        count = audit_logger.export_csv(output_file)
        
        return send_file(
            output_file,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'audit-logs-{datetime.now().strftime("%Y%m%d")}.csv'
        )
    
    @app.route('/api/notifications/<int:notif_id>/read', methods=['POST'])
    def api_mark_notification_read(notif_id):
        """标记通知为已读"""
        logger.info(f"标记通知 {notif_id} 为已读")
        if ws_manager:
            ws_manager.push_notification({
                'event': 'read',
                'id': notif_id
            })
        return jsonify({'status': 'success'})
    
    @app.route('/api/reports', methods=['GET'])
    def api_get_reports():
        """获取报告列表"""
        # 从 reports 目录读取报告
        reports_dir = Path(__file__).parent.parent / 'reports'
        reports = []
        
        if reports_dir.exists():
            for f in reports_dir.glob('*.*'):
                reports.append({
                    'id': int(f.stem.split('_')[-1]) if '_' in f.stem else hash(f.name) % 10000,
                    'title': f.stem.replace('_', ' ').title(),
                    'format': f.suffix[1:] if f.suffix else 'text',
                    'size': f'{f.stat().st_size / 1024:.1f} KB',
                    'createdAt': datetime.fromtimestamp(f.stat().st_mtime).isoformat()
                })
        
        return jsonify(reports if reports else [])
    
    @app.route('/api/reports', methods=['POST'])
    def api_create_report():
        """生成新报告"""
        data = request.json
        title = data.get('title', 'Untitled Report')
        format = data.get('format', 'markdown')
        
        logger.info(f"生成报告：{title} ({format})")
        
        # 推送报告生成事件
        if ws_manager:
            ws_manager.push_notification({
                'event': 'report_generated',
                'title': title
            })
        
        return jsonify({
            'status': 'success',
            'message': f'报告生成中：{title}'
        })
    
    @app.route('/api/status')
    def api_status():
        """获取系统状态"""
        if system:
            return jsonify(system.get_status())
        return jsonify({
            'system': '硅基世界 2',
            'version': '3.2.0',
            'timestamp': datetime.now().isoformat(),
            'status': 'ok',
            'websocket': SOCKETIO_AVAILABLE
        })
    
    @app.route('/api/agents')
    def api_agents():
        """获取代理状态"""
        # 优先读取公司多智能体系统配置
        company_config_path = Path(__file__).parent.parent / "configs" / "company-agents.json"
        
        if company_config_path.exists():
            try:
                with open(company_config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # 转换为前端格式
                agents = {}
                
                # 添加 CEO 协调器
                agents['ceo_coordinator'] = {
                    'name': config.get('orchestrator', {}).get('name', 'CEO Coordinator'),
                    'role': config.get('orchestrator', {}).get('role', 'Coordinator'),
                    'status': 'active',
                    'capabilities': config.get('orchestrator', {}).get('capabilities', []),
                    'agent_count': len(config.get('agents', []))
                }
                
                # 添加所有代理
                for agent in config.get('agents', []):
                    agent_key = agent['id'].replace('agent-', '')
                    agents[agent_key] = {
                        'name': agent['name'],
                        'role': agent['role'],
                        'status': 'active',
                        'capabilities': agent.get('capabilities', []),
                        'workspace': agent.get('workspace', ''),
                        'triggers': agent.get('triggers', [])
                    }
                
                # 添加工作流信息
                agents['_workflows'] = {
                    'count': len(config.get('workflows', [])),
                    'workflows': config.get('workflows', [])
                }
                
                return jsonify(agents)
            except Exception as e:
                logger.error(f"读取公司代理配置失败：{e}")
        
        # 回退到原有逻辑
        if system:
            status = system.get_status()
            return jsonify(status.get('components', {}))
        return jsonify({})
    
    @app.route('/api/tasks', methods=['GET'])
    def api_tasks():
        """获取任务队列"""
        if system and hasattr(system, 'task_queue'):
            return jsonify(system.task_queue.get_queue_status())
        return jsonify({
            'total': 0,
            'pending': 0,
            'running': 0,
            'completed': 0,
            'failed': 0,
            'tasks': []
        })
    
    @app.route('/api/tasks', methods=['POST'])
    def api_create_task():
        """创建新任务"""
        data = request.json
        description = data.get('description', 'Unnamed Task')
        priority = data.get('priority', 'normal')
        
        logger.info(f"创建任务：{description} (优先级：{priority})")
        
        # 推送任务更新通知
        if ws_manager:
            ws_manager.push_task_update({
                'event': 'task_created',
                'description': description,
                'priority': priority,
                'timestamp': datetime.now().isoformat()
            })
        
        return jsonify({
            'status': 'success',
            'message': f'任务已创建：{description}',
            'task': {
                'description': description,
                'priority': priority,
                'created_at': datetime.now().isoformat()
            }
        })
    
    @app.route('/api/tasks/start', methods=['POST'])
    def api_start_queue():
        """启动任务队列"""
        logger.info("启动任务队列")
        
        if ws_manager:
            ws_manager.push_task_update({
                'event': 'queue_started',
                'timestamp': datetime.now().isoformat()
            })
        
        return jsonify({
            'status': 'success',
            'message': '任务队列已启动'
        })
    
    @app.route('/api/tasks/clear-completed', methods=['POST'])
    def api_clear_completed():
        """清空已完成任务"""
        logger.info("清空已完成任务")
        
        if ws_manager:
            ws_manager.push_task_update({
                'event': 'completed_cleared',
                'timestamp': datetime.now().isoformat()
            })
        
        return jsonify({
            'status': 'success',
            'message': '已完成任务已清空'
        })
    
    @app.route('/api/notifications')
    def api_notifications():
        """获取通知历史"""
        if system and hasattr(system, 'notifier'):
            history = system.notifier.get_history(limit=20)
            return jsonify(history)
        return jsonify([])
    
    @app.route('/api/config', methods=['GET'])
    def api_config_get():
        """获取配置"""
        if system and hasattr(system, 'config_manager'):
            return jsonify(system.config_manager.get_all())
        return jsonify({})
    
    @app.route('/api/config', methods=['POST'])
    def api_config_set():
        """更新配置"""
        if system and hasattr(system, 'config_manager'):
            data = request.json
            for key, value in data.items():
                system.config_manager.set(key, value)
            return jsonify({'status': 'success'})
        return jsonify({'status': 'error', 'message': 'Config manager not available'})
    
    @app.route('/api/knowledge-graph')
    def api_knowledge_graph():
        """获取知识图谱数据"""
        if system and hasattr(system, 'knowledge_graph'):
            graph = system.knowledge_graph
            nodes = [
                {'id': k, 'label': v.name, 'category': v.category}
                for k, v in graph.nodes.items()
            ]
            links = [
                {'source': r.from_node, 'target': r.to_node, 'type': r.relation_type}
                for r in graph.relations.values()
            ]
            return jsonify({'nodes': nodes, 'links': links})
        return jsonify({'nodes': [], 'links': []})
    
    @app.route('/api/ws-stats')
    def api_ws_stats():
        """获取 WebSocket 连接统计"""
        if ws_manager:
            return jsonify(ws_manager.get_client_info())
        return jsonify({'error': 'WebSocket not available'})
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': 'Internal server error'}), 500
    
    logger.info("Web UI 应用已创建 (Phase 6.1 - WebSocket 增强版)")
    return app


def run_dashboard(host: str = '127.0.0.1', port: int = 5000, debug: bool = False, system_instance=None):
    """
    运行 Web 仪表板
    
    Args:
        host: 监听地址
        port: 端口号
        debug: 调试模式
        system_instance: GuijiWorld2 系统实例
    """
    if not FLASK_AVAILABLE:
        logger.error("Flask 未安装，无法启动 Web UI")
        print("\n❌ Flask 未安装，请运行：pip install flask")
        return
    
    app = create_app(system_instance)
    if not app:
        return
    
    socketio = app.config.get('socketio')
    
    if socketio:
        # 使用 SocketIO 启动
        logger.info(f"启动 Web 仪表板（WebSocket 模式）：http://{host}:{port}")
        print(f"\n🌐 硅基世界 2 Web 仪表板 (Phase 6.1)")
        print(f"   地址：http://{host}:{port}")
        print(f"   WebSocket: ✅ 已启用")
        print(f"   调试模式：{'开启' if debug else '关闭'}")
        print()
        socketio.run(app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)
    else:
        # 使用 Flask 原生启动
        logger.info(f"启动 Web 仪表板（轮询模式）：http://{host}:{port}")
        print(f"\n🌐 硅基世界 2 Web 仪表板")
        print(f"   地址：http://{host}:{port}")
        print(f"   WebSocket: ❌ 未启用 (请安装 flask-socketio)")
        print(f"   调试模式：{'开启' if debug else '关闭'}")
        print()
        app.run(host=host, port=port, debug=debug)


# 独立运行测试
if __name__ == '__main__':
    print("🧪 Web UI 测试模式 (Phase 6.1)")
    print("=" * 50)
    
    if not FLASK_AVAILABLE:
        print("❌ Flask 未安装")
        print("\n请安装依赖:")
        print("  pip install flask flask-socketio")
    elif not SOCKETIO_AVAILABLE:
        print("⚠️ Flask 已安装，但 Flask-SocketIO 未安装")
        print("\n请安装 WebSocket 支持:")
        print("  pip install flask-socketio")
        print("\n或者使用轮询模式启动:")
        print("  python app.py")
    else:
        print("✅ Flask 已安装")
        print("✅ Flask-SocketIO 已安装")
        print(f"✅ 模板目录：{Path(__file__).parent / 'templates'}")
        print(f"✅ 静态文件：{Path(__file__).parent / 'static'}")
        print("\n🚀 启动 WebSocket 测试服务器...")
        run_dashboard(debug=True)
