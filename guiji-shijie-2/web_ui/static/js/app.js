/**
 * 硅基世界 2 - 主题切换和交互功能
 * Version: 2.0.0-alpha
 * Author: 三二 🐱
 */

// ========== 主题管理 ==========
class ThemeManager {
  constructor() {
    this.theme = localStorage.getItem('theme') || 'light';
    this.init();
  }

  init() {
    this.applyTheme();
    this.bindEvents();
  }

  applyTheme() {
    document.documentElement.setAttribute('data-theme', this.theme);
    localStorage.setItem('theme', this.theme);
    
    // 更新按钮图标
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
      toggleBtn.innerHTML = this.theme === 'dark' ? '☀️' : '🌙';
      toggleBtn.setAttribute('aria-label', `切换到${this.theme === 'dark' ? '浅色' : '暗黑'}模式`);
    }
  }

  toggle() {
    this.theme = this.theme === 'dark' ? 'light' : 'dark';
    this.applyTheme();
    
    // 触发自定义事件
    window.dispatchEvent(new CustomEvent('theme-change', { 
      detail: { theme: this.theme } 
    }));
  }

  bindEvents() {
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => this.toggle());
    }

    // 监听系统主题变化
    if (window.matchMedia) {
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
          this.theme = e.matches ? 'dark' : 'light';
          this.applyTheme();
        }
      });
    }
  }

  getTheme() {
    return this.theme;
  }

  isDark() {
    return this.theme === 'dark';
  }
}

// ========== API 客户端 ==========
class APIClient {
  constructor(baseURL = '') {
    this.baseURL = baseURL || window.location.origin;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      ...options,
      headers: {
        ...this.defaultHeaders,
        ...(options.headers || {}),
      },
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      }

      return await response.text();
    } catch (error) {
      console.error(`API 请求失败 [${endpoint}]:`, error);
      throw error;
    }
  }

  get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  }

  post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

// ========== 通知系统 ==========
class NotificationManager {
  constructor() {
    this.container = null;
    this.init();
  }

  init() {
    this.createContainer();
  }

  createContainer() {
    this.container = document.createElement('div');
    this.container.className = 'notification-container';
    this.container.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 10px;
    `;
    document.body.appendChild(this.container);
  }

  show(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
      padding: 1rem 1.5rem;
      border-radius: 0.5rem;
      background-color: var(--bg-primary);
      border-left: 4px solid var(--${type === 'error' ? 'error' : type === 'success' ? 'success' : type === 'warning' ? 'warning' : 'info'}-color);
      box-shadow: var(--shadow-lg);
      min-width: 300px;
      animation: slideIn 0.3s ease;
    `;
    notification.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: space-between;">
        <span>${message}</span>
        <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; cursor: pointer; font-size: 1.25rem; color: var(--text-muted);">&times;</button>
      </div>
    `;

    this.container.appendChild(notification);

    if (duration > 0) {
      setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
      }, duration);
    }

    return notification;
  }

  success(message, duration = 3000) {
    return this.show(message, 'success', duration);
  }

  error(message, duration = 5000) {
    return this.show(message, 'error', duration);
  }

  warning(message, duration = 4000) {
    return this.show(message, 'warning', duration);
  }

  info(message, duration = 3000) {
    return this.show(message, 'info', duration);
  }
}

// ========== 移动端导航 ==========
class MobileNav {
  constructor() {
    this.isOpen = false;
    this.init();
  }

  init() {
    this.bindEvents();
  }

  toggle() {
    this.isOpen = !this.isOpen;
    const nav = document.querySelector('.navbar-nav');
    const toggle = document.querySelector('.navbar-toggle');
    
    if (nav) {
      nav.style.display = this.isOpen ? 'flex' : 'none';
    }
    
    if (toggle) {
      toggle.innerHTML = this.isOpen ? '✕' : '☰';
    }
  }

  bindEvents() {
    const toggle = document.querySelector('.navbar-toggle');
    if (toggle) {
      toggle.addEventListener('click', () => this.toggle());
    }
  }
}

// ========== 数据表格 ==========
class DataTable {
  constructor(elementId, options = {}) {
    this.element = document.getElementById(elementId);
    this.options = {
      sortable: true,
      searchable: true,
      pageable: true,
      pageSize: 10,
      ...options,
    };
    this.data = [];
    this.currentPage = 1;
    this.init();
  }

  init() {
    if (!this.element) return;
    this.loadData();
    this.render();
  }

  loadData() {
    // 从表格中提取数据
    const rows = this.element.querySelectorAll('tbody tr');
    this.data = Array.from(rows).map(row => {
      const cells = row.querySelectorAll('td');
      return Array.from(cells).map(cell => cell.textContent.trim());
    });
  }

  render() {
    // 简化版本，实际应该更复杂
    console.log('DataTable render:', this.data.length, 'rows');
  }

  search(query) {
    // 实现搜索功能
  }

  sort(column, direction) {
    // 实现排序功能
  }

  page(pageNum) {
    // 实现分页功能
  }
}

// ========== WebSocket 客户端 ==========
class WebSocketClient {
  constructor(url) {
    this.url = url || `ws://${window.location.host}/ws`;
    this.ws = null;
    this.reconnectInterval = 3000;
    this.reconnectTimer = null;
    this.callbacks = {};
  }

  connect() {
    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        console.log('WebSocket 已连接');
        this.trigger('open');
      };

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('WebSocket 消息:', data);
        this.trigger('message', data);
      };

      this.ws.onclose = () => {
        console.log('WebSocket 已关闭，准备重连...');
        this.trigger('close');
        this.scheduleReconnect();
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket 错误:', error);
        this.trigger('error', error);
      };
    } catch (error) {
      console.error('WebSocket 连接失败:', error);
      this.scheduleReconnect();
    }
  }

  scheduleReconnect() {
    if (this.reconnectTimer) return;
    
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null;
      this.connect();
    }, this.reconnectInterval);
  }

  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    } else {
      console.warn('WebSocket 未连接，消息发送失败');
    }
  }

  on(event, callback) {
    if (!this.callbacks[event]) {
      this.callbacks[event] = [];
    }
    this.callbacks[event].push(callback);
  }

  off(event, callback) {
    if (this.callbacks[event]) {
      this.callbacks[event] = this.callbacks[event].filter(cb => cb !== callback);
    }
  }

  trigger(event, data) {
    if (this.callbacks[event]) {
      this.callbacks[event].forEach(callback => callback(data));
    }
  }

  disconnect() {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

// ========== 工具函数 ==========
function formatDate(date, format = 'YYYY-MM-DD HH:mm:ss') {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');
  const seconds = String(d.getSeconds()).padStart(2, '0');

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds);
}

function formatNumber(num) {
  return new Intl.NumberFormat('zh-CN').format(num);
}

function truncate(str, length = 50) {
  if (str.length <= length) return str;
  return str.substring(0, length) + '...';
}

function debounce(func, wait = 300) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

function throttle(func, limit = 300) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// ========== 初始化 ==========
document.addEventListener('DOMContentLoaded', () => {
  // 初始化主题管理器
  window.themeManager = new ThemeManager();
  
  // 初始化通知管理器
  window.notifications = new NotificationManager();
  
  // 初始化移动端导航
  window.mobileNav = new MobileNav();
  
  // 初始化 API 客户端
  window.api = new APIClient();
  
  console.log('🌍 硅基世界 2 - 前端初始化完成');
});

// 添加 CSS 动画
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from {
      transform: translateX(100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }
  
  @keyframes slideOut {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(100%);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);
