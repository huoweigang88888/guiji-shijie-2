"""
Web UI - Web 控制面板

提供基于浏览器的系统监控和控制界面
"""

import json
import logging
import threading
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('web-ui')

# 尝试导入 Flask，如果不可用则使用内置 HTTP 服务器
try:
    from flask import Flask, jsonify, render_template_string, request
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    logger.warning("Flask 未安装，使用简化版 Web UI")


# HTML 模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>硅基世界 2 - 控制面板</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        header {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        h1 { color: #667eea; }
        .status-bar {
            display: flex;
            gap: 20px;
            margin-top: 10px;
        }
        .status-item {
            background: #f0f0f0;
            padding: 10px 20px;
            border-radius: 5px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .card h2 {
            color: #333;
            margin-bottom: 15px;
            font-size: 18px;
        }
        .card-content {
            color: #666;
            line-height: 1.6;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
            font-size: 14px;
        }
        button:hover {
            background: #5568d3;
        }
        .action-buttons {
            margin-top: 15px;
        }
        .log-output {
            background: #1e1e1e;
            color: #00ff00;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            max-height: 300px;
            overflow-y: auto;
            margin-top: 10px;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
        .metric:last-child { border-bottom: none; }
        .metric-value {
            font-weight: bold;
            color: #667eea;
        }
        .success { color: #22c55e; }
        .warning { color: #f59e0b; }
        .error { color: #ef4444; }
        footer {
            text-align: center;
            color: white;
            margin-top: 30px;
            padding: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 硅基世界 2 - 控制面板</h1>
            <div class="status-bar">
                <div class="status-item">
                    <strong>系统状态:</strong> <span id="system-status" class="success">运行中</span>
                </div>
                <div class="status-item">
                    <strong>更新时间:</strong> <span id="update-time">--</span>
                </div>
            </div>
        </header>

        <div class="grid">
            <!-- 系统概览 -->
            <div class="card">
                <h2>📊 系统概览</h2>
                <div class="card-content" id="system-overview">
                    <div class="metric">
                        <span>版本</span>
                        <span class="metric-value" id="version">--</span>
                    </div>
                    <div class="metric">
                        <span>运行时间</span>
                        <span class="metric-value" id="uptime">--</span>
                    </div>
                    <div class="metric">
                        <span>活跃组件</span>
                        <span class="metric-value" id="active-components">--</span>
                    </div>
                </div>
            </div>

            <!-- 快速操作 -->
            <div class="card">
                <h2>⚡ 快速操作</h2>
                <div class="action-buttons">
                    <button onclick="runAction('heartbeat')">💓 心跳检查</button>
                    <button onclick="runAction('status')">📊 系统状态</button>
                    <button onclick="runAction('improvements')">💡 改进建议</button>
                    <button onclick="runAction('exec-tasks')">▶️ 执行任务</button>
                </div>
            </div>

            <!-- 向量搜索 -->
            <div class="card">
                <h2>🔍 向量搜索</h2>
                <div class="card-content">
                    <input type="text" id="vector-query" placeholder="输入搜索词..." 
                           style="width: 100%; padding: 8px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    <button onclick="vectorSearch()">搜索</button>
                    <div id="vector-results" style="margin-top: 10px;"></div>
                </div>
            </div>

            <!-- 知识图谱 -->
            <div class="card">
                <h2>🕸️ 知识图谱</h2>
                <div class="card-content" id="graph-stats">
                    <div class="metric">
                        <span>节点数</span>
                        <span class="metric-value" id="graph-nodes">--</span>
                    </div>
                    <div class="metric">
                        <span>关系数</span>
                        <span class="metric-value" id="graph-relations">--</span>
                    </div>
                    <button onclick="searchGraph()" style="margin-top: 10px;">搜索知识</button>
                </div>
            </div>

            <!-- 任务状态 -->
            <div class="card">
                <h2>📋 任务状态</h2>
                <div class="card-content" id="task-status">
                    <div class="metric">
                        <span>总任务</span>
                        <span class="metric-value" id="total-tasks">--</span>
                    </div>
                    <div class="metric">
                        <span>已完成</span>
                        <span class="metric-value success" id="completed-tasks">--</span>
                    </div>
                    <div class="metric">
                        <span>待处理</span>
                        <span class="metric-value warning" id="pending-tasks">--</span>
                    </div>
                </div>
            </div>

            <!-- 日志输出 -->
            <div class="card" style="grid-column: 1 / -1;">
                <h2>📝 操作日志</h2>
                <div class="log-output" id="log-output">
                    <div>等待操作...</div>
                </div>
            </div>
        </div>

        <footer>
            <p>硅基世界 2 - AI 代理系统 | Version 3.0</p>
            <p>GitHub: <a href="https://github.com/huoweigang88888/guiji-shijie-2" style="color: white;">huoweigang88888/guiji-shijie-2</a></p>
        </footer>
    </div>

    <script>
        let startTime = new Date();

        // 更新时间
        function updateTime() {
            document.getElementById('update-time').textContent = new Date().toLocaleString();
        }

        // 加载系统状态
        async function loadStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                document.getElementById('version').textContent = data.version || '3.0.0';
                
                const uptime = Math.floor((new Date() - startTime) / 1000);
                document.getElementById('uptime').textContent = formatUptime(uptime);
                
                const components = Object.keys(data.components || {}).length;
                document.getElementById('active-components').textContent = components;
                
                // 任务状态
                if (data.components && data.components.executor) {
                    document.getElementById('total-tasks').textContent = data.components.executor.total || 0;
                    document.getElementById('completed-tasks').textContent = data.components.executor.completed || 0;
                    document.getElementById('pending-tasks').textContent = data.components.executor.pending || 0;
                }
                
                // 知识图谱
                if (data.components && data.components.knowledge_graph) {
                    document.getElementById('graph-nodes').textContent = data.components.knowledge_graph.total_nodes || 0;
                    document.getElementById('graph-relations').textContent = data.components.knowledge_graph.total_relations || 0;
                }
                
                updateTime();
            } catch (error) {
                console.error('加载状态失败:', error);
                logOutput('加载状态失败：' + error.message, 'error');
            }
        }

        // 格式化运行时间
        function formatUptime(seconds) {
            const h = Math.floor(seconds / 3600);
            const m = Math.floor((seconds % 3600) / 60);
            const s = seconds % 60;
            return `${h}h ${m}m ${s}s`;
        }

        // 执行操作
        async function runAction(action) {
            logOutput(`执行操作：${action}...`, 'info');
            try {
                const response = await fetch(`/api/${action}`, { method: 'POST' });
                const data = await response.json();
                logOutput(JSON.stringify(data, null, 2), 'success');
                setTimeout(loadStatus, 1000);
            } catch (error) {
                logOutput('操作失败：' + error.message, 'error');
            }
        }

        // 向量搜索
        async function vectorSearch() {
            const query = document.getElementById('vector-query').value;
            if (!query) return;
            
            logOutput(`向量搜索：${query}...`, 'info');
            try {
                const response = await fetch(`/api/vector-search?query=${encodeURIComponent(query)}`);
                const data = await response.json();
                
                const resultsDiv = document.getElementById('vector-results');
                if (data.count > 0) {
                    resultsDiv.innerHTML = data.results.map((r, i) => 
                        `<div style="padding: 5px 0; border-bottom: 1px solid #eee;">
                            <strong>${i+1}.</strong> [${(r.score || 0).toFixed(2)}] ${r.content || ''}
                        </div>`
                    ).join('');
                } else {
                    resultsDiv.innerHTML = '<div>未找到结果</div>';
                }
                
                logOutput(`搜索完成：找到 ${data.count} 条结果`, 'success');
            } catch (error) {
                logOutput('搜索失败：' + error.message, 'error');
            }
        }

        // 搜索知识
        async function searchGraph() {
            const query = prompt('输入搜索词:');
            if (!query) return;
            
            logOutput(`知识搜索：${query}...`, 'info');
            try {
                const response = await fetch(`/api/graph-search?query=${encodeURIComponent(query)}`);
                const data = await response.json();
                
                if (data.count > 0) {
                    logOutput(`找到 ${data.count} 个知识节点:\\n` + 
                        data.results.map(r => `- ${r.title} [${r.category}]`).join('\\n'), 'success');
                } else {
                    logOutput('未找到相关知识', 'warning');
                }
            } catch (error) {
                logOutput('搜索失败：' + error.message, 'error');
            }
        }

        // 日志输出
        function logOutput(message, type = 'info') {
            const logDiv = document.getElementById('log-output');
            const timestamp = new Date().toLocaleTimeString();
            const color = type === 'error' ? '#ef4444' : type === 'success' ? '#22c55e' : '#00ff00';
            logDiv.innerHTML = `<div style="color: ${color}">[${timestamp}] ${message}</div>` + logDiv.innerHTML;
        }

        // 页面加载时获取状态
        loadStatus();
        
        // 每 30 秒刷新一次
        setInterval(loadStatus, 30000);
    </script>
</body>
</html>
"""


class WebUI:
    """
    Web UI 服务器
    
    提供基于浏览器的系统监控和控制界面
    """
    
    def __init__(self, system_instance=None, host='0.0.0.0', port=8080):
        """
        初始化 Web UI
        
        Args:
            system_instance: GuijiWorld2 系统实例
            host: 监听地址
            port: 监听端口
        """
        self.system = system_instance
        self.host = host
        self.port = port
        self.server = None
        self.start_time = datetime.now()
        
        if FLASK_AVAILABLE:
            self.app = Flask(__name__)
            self._setup_flask_routes()
        else:
            self.app = None
    
    def _setup_flask_routes(self):
        """设置 Flask 路由"""
        @self.app.route('/')
        def index():
            return render_template_string(HTML_TEMPLATE)
        
        @self.app.route('/api/status')
        def api_status():
            if self.system:
                return jsonify(self.system.get_status())
            return jsonify({'error': 'System not initialized'})
        
        @self.app.route('/api/heartbeat', methods=['POST'])
        def api_heartbeat():
            if self.system:
                result = self.system.run_heartbeat()
                return jsonify(result)
            return jsonify({'error': 'System not initialized'})
        
        @self.app.route('/api/improvements', methods=['POST'])
        def api_improvements():
            if self.system:
                result = self.system.get_improvements()
                return jsonify(result)
            return jsonify({'error': 'System not initialized'})
        
        @self.app.route('/api/exec-tasks', methods=['POST'])
        def api_exec_tasks():
            if self.system:
                result = self.system.execute_tasks()
                return jsonify(result)
            return jsonify({'error': 'System not initialized'})
        
        @self.app.route('/api/vector-search')
        def api_vector_search():
            if self.system:
                query = request.args.get('query', '')
                result = self.system.vector_search_query(query)
                return jsonify(result)
            return jsonify({'error': 'System not initialized'})
        
        @self.app.route('/api/graph-search')
        def api_graph_search():
            if self.system:
                query = request.args.get('query', '')
                result = self.system.graph_search(query)
                return jsonify(result)
            return jsonify({'error': 'System not initialized'})
    
    def start(self, blocking=True):
        """
        启动 Web 服务器
        
        Args:
            blocking: 是否阻塞运行
        """
        if FLASK_AVAILABLE and self.app:
            logger.info(f"Starting Flask Web UI on http://{self.host}:{self.port}")
            if blocking:
                self.app.run(host=self.host, port=self.port, debug=False, threaded=True)
            else:
                thread = threading.Thread(
                    target=self.app.run,
                    kwargs={'host': self.host, 'port': self.port, 'debug': False, 'threaded': True}
                )
                thread.daemon = True
                thread.start()
                logger.info(f"Web UI started in background")
        else:
            # 简化版 HTTP 服务器
            logger.info(f"Starting simple HTTP server on http://{self.host}:{self.port}")
            
            class Handler(SimpleHTTPRequestHandler):
                def do_GET(self):
                    if self.path == '/':
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html; charset=utf-8')
                        self.end_headers()
                        self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
                    else:
                        self.send_response(404)
                        self.end_headers()
            
            self.server = HTTPServer((self.host, self.port), Handler)
            if blocking:
                self.server.serve_forever()
            else:
                thread = threading.Thread(target=self.server.serve_forever)
                thread.daemon = True
                thread.start()
    
    def stop(self):
        """停止服务器"""
        if self.server:
            self.server.shutdown()
            logger.info("Web UI stopped")


def main():
    """测试 Web UI"""
    print("="*60)
    print("Web UI Test")
    print("="*60)
    
    # 尝试导入主系统
    try:
        from main import GuijiWorld2
        system = GuijiWorld2()
        print("\nSystem initialized")
    except:
        system = None
        print("\nSystem not available (running standalone)")
    
    print("\nStarting Web UI...")
    print("Open http://localhost:8080 in your browser")
    print("Press Ctrl+C to stop\n")
    
    ui = WebUI(system_instance=system, port=8080)
    
    try:
        ui.start(blocking=True)
    except KeyboardInterrupt:
        print("\nShutting down...")
        ui.stop()


if __name__ == '__main__':
    main()
