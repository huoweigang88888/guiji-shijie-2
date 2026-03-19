/**
 * 前端性能优化模块 - Phase 7
 * 功能：懒加载、资源预加载、性能监控
 */

// ========== 懒加载 ==========
class LazyLoader {
  constructor() {
    this.observers = new Map();
    this.init();
  }

  init() {
    if ('IntersectionObserver' in window) {
      this.observer = new IntersectionObserver(
        (entries) => this.handleIntersection(entries),
        { rootMargin: '50px' }
      );
    }
  }

  observe(element, callback) {
    if (this.observer) {
      this.observer.observe(element);
      this.observers.set(element, callback);
    } else {
      callback();
    }
  }

  handleIntersection(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const callback = this.observers.get(entry.target);
        if (callback) callback();
        this.observer.unobserve(entry.target);
        this.observers.delete(entry.target);
      }
    });
  }

  lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    images.forEach(img => {
      this.observe(img, () => {
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
      });
    });
  }
}

// ========== 资源预加载 ==========
class Preloader {
  constructor() {
    this.queue = [];
  }

  preload(urls) {
    urls.forEach(url => {
      const link = document.createElement('link');
      link.rel = 'preload';
      link.as = this.getResourceType(url);
      link.href = url;
      document.head.appendChild(link);
    });
  }

  getResourceType(url) {
    if (url.endsWith('.js')) return 'script';
    if (url.endsWith('.css')) return 'style';
    if (url.match(/\.(png|jpg|jpeg|gif|webp)$/)) return 'image';
    if (url.endsWith('.woff2')) return 'font';
    return 'fetch';
  }

  prefetch(urls) {
    urls.forEach(url => {
      const link = document.createElement('link');
      link.rel = 'prefetch';
      link.href = url;
      document.head.appendChild(link);
    });
  }
}

// ========== 性能监控 ==========
class PerformanceMonitor {
  constructor() {
    this.metrics = {
      loadTime: 0,
      domContentLoaded: 0,
      firstPaint: 0,
      firstContentfulPaint: 0,
      resourceTimings: []
    };
    this.init();
  }

  init() {
    if (window.performance) {
      this.recordLoadMetrics();
      this.recordPaintMetrics();
      this.recordResourceTimings();
    }
  }

  recordLoadMetrics() {
    window.addEventListener('load', () => {
      const timing = performance.timing;
      this.metrics.loadTime = timing.loadEventEnd - timing.navigationStart;
      this.metrics.domContentLoaded = timing.domContentLoadedEventEnd - timing.navigationStart;
      console.log(`[Performance] Load: ${this.metrics.loadTime}ms, DOMContentLoaded: ${this.metrics.domContentLoaded}ms`);
    });
  }

  recordPaintMetrics() {
    if ('PerformanceObserver' in window) {
      const observer = new PerformanceObserver((list) => {
        list.getEntries().forEach(entry => {
          if (entry.name === 'first-paint') {
            this.metrics.firstPaint = entry.startTime;
          }
          if (entry.name === 'first-contentful-paint') {
            this.metrics.firstContentfulPaint = entry.startTime;
          }
        });
      });
      observer.observe({ entryTypes: ['paint'] });
    }
  }

  recordResourceTimings() {
    if ('PerformanceObserver' in window) {
      const observer = new PerformanceObserver((list) => {
        this.metrics.resourceTimings.push(...list.getEntries());
      });
      observer.observe({ entryTypes: ['resource'] });
    }
  }

  getMetrics() {
    return {
      ...this.metrics,
      resourceCount: this.metrics.resourceTimings.length,
      totalResourceSize: this.metrics.resourceTimings.reduce((sum, r) => sum + (r.transferSize || 0), 0),
      timestamp: new Date().toISOString()
    };
  }

  getSlowResources(threshold = 500) {
    return this.metrics.resourceTimings
      .filter(r => r.duration > threshold)
      .map(r => ({
        url: r.name,
        duration: Math.round(r.duration),
        size: r.transferSize || 0
      }));
  }

  report() {
    const metrics = this.getMetrics();
    const slow = this.getSlowResources();
    console.log('[Performance] Metrics:', metrics);
    if (slow.length > 0) {
      console.warn(`[Performance] ${slow.length} slow resources detected:`);
      slow.forEach(r => console.warn(`  - ${r.url} (${r.duration}ms, ${r.size} bytes)`));
    }
    return { metrics, slowResources: slow };
  }
}

// ========== 防抖节流 ==========
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
  window.lazyLoader = new LazyLoader();
  window.preloader = new Preloader();
  window.performanceMonitor = new PerformanceMonitor();
  
  window.lazyLoader.lazyLoadImages();
  
  console.log('[Performance] Frontend optimization initialized');
});
