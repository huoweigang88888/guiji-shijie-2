#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 集成框架 - API Integration Framework

统一第三方 API 接口，支持：
- API 密钥管理
- 请求限流和重试
- 预集成服务（天气、新闻、股票、翻译等）

功能：
- 统一的 API 调用接口
- 自动重试机制
- 请求缓存
- 密钥安全存储
"""

import json
import logging
import time
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum

# 可选依赖 requests
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logging.getLogger('api-integration').warning("requests 模块未安装，API 集成功能将受限")

logger = logging.getLogger('api-integration')


class ApiServiceType(Enum):
    """API 服务类型"""
    WEATHER = "weather"
    NEWS = "news"
    STOCK = "stock"
    TRANSLATION = "translation"
    SEARCH = "search"
    CUSTOM = "custom"


@dataclass
class ApiConfig:
    """API 配置"""
    name: str
    base_url: str
    api_key: Optional[str] = None
    timeout: int = 30
    rate_limit: int = 100  # 每分钟请求数
    retry_count: int = 3
    retry_delay: float = 1.0
    headers: Dict[str, str] = None
    
    def __post_init__(self):
        if self.headers is None:
            self.headers = {}


@dataclass
class ApiRequest:
    """API 请求"""
    service: str
    endpoint: str
    method: str = "GET"
    params: Dict[str, Any] = None
    data: Dict[str, Any] = None
    headers: Dict[str, str] = None


@dataclass
class ApiResponse:
    """API 响应"""
    success: bool
    status_code: int
    data: Any
    error: Optional[str] = None
    cached: bool = False
    request_time: float = 0.0


class RateLimiter:
    """限流器"""
    
    def __init__(self, rate_limit: int):
        self.rate_limit = rate_limit
        self.requests = []
        
    def acquire(self):
        """获取请求许可"""
        now = time.time()
        # 清理 60 秒前的请求
        self.requests = [t for t in self.requests if now - t < 60]
        
        if len(self.requests) >= self.rate_limit:
            wait_time = 60 - (now - self.requests[0])
            if wait_time > 0:
                logger.info(f"限流中，等待 {wait_time:.2f} 秒")
                time.sleep(wait_time)
        
        self.requests.append(time.time())


class CacheManager:
    """缓存管理器"""
    
    def __init__(self, cache_dir: Path, ttl_seconds: int = 3600):
        self.cache_dir = cache_dir
        self.ttl_seconds = ttl_seconds
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_cache_key(self, request: ApiRequest) -> str:
        """生成缓存键"""
        key_str = f"{request.service}:{request.endpoint}:{json.dumps(request.params or {})}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, request: ApiRequest) -> Optional[Any]:
        """获取缓存"""
        cache_key = self._get_cache_key(request)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached = json.load(f)
            
            cached_at = datetime.fromisoformat(cached['cached_at'])
            if datetime.now() - cached_at < timedelta(seconds=self.ttl_seconds):
                logger.debug(f"缓存命中：{cache_key}")
                return cached['data']
            else:
                cache_file.unlink()
        except Exception as e:
            logger.warning(f"读取缓存失败：{e}")
        
        return None
    
    def set(self, request: ApiRequest, data: Any):
        """设置缓存"""
        cache_key = self._get_cache_key(request)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'cached_at': datetime.now().isoformat(),
                    'data': data
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"写入缓存失败：{e}")


class ApiIntegration:
    """API 集成框架"""
    
    def __init__(self, config_dir: Path = None):
        self.config_dir = config_dir or Path(__file__).parent.parent / "api-configs"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.cache_dir = self.config_dir / "cache"
        self.configs: Dict[str, ApiConfig] = {}
        self.rate_limiters: Dict[str, RateLimiter] = {}
        self.cache_manager = CacheManager(self.cache_dir)
        
        self._load_configs()
    
    def _load_configs(self):
        """加载 API 配置"""
        config_file = self.config_dir / "apis.json"
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for name, cfg in data.items():
                    self.configs[name] = ApiConfig(**cfg)
                    self.rate_limiters[name] = RateLimiter(cfg.get('rate_limit', 100))
                
                logger.info(f"已加载 {len(self.configs)} 个 API 配置")
            except Exception as e:
                logger.error(f"加载配置失败：{e}")
    
    def save_configs(self):
        """保存 API 配置"""
        config_file = self.config_dir / "apis.json"
        data = {name: asdict(cfg) for name, cfg in self.configs.items()}
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info("API 配置已保存")
    
    def register_api(self, config: ApiConfig):
        """注册 API"""
        self.configs[config.name] = config
        self.rate_limiters[config.name] = RateLimiter(config.rate_limit)
        self.save_configs()
        logger.info(f"已注册 API: {config.name}")
    
    def _execute_request(self, request: ApiRequest, config: ApiConfig) -> ApiResponse:
        """执行 API 请求"""
        start_time = time.time()
        
        if not REQUESTS_AVAILABLE:
            return ApiResponse(
                success=False,
                status_code=0,
                data=None,
                error="requests 模块未安装，无法执行 HTTP 请求",
                request_time=time.time() - start_time
            )
        
        url = f"{config.base_url}/{request.endpoint}"
        headers = {**config.headers, **(request.headers or {})}
        
        if config.api_key:
            headers['Authorization'] = f"Bearer {config.api_key}"
        
        try:
            response = requests.request(
                method=request.method,
                url=url,
                params=request.params,
                json=request.data,
                headers=headers,
                timeout=config.timeout
            )
            
            request_time = time.time() - start_time
            
            if response.ok:
                return ApiResponse(
                    success=True,
                    status_code=response.status_code,
                    data=response.json() if response.headers.get('content-type') == 'application/json' else response.text,
                    request_time=request_time
                )
            else:
                return ApiResponse(
                    success=False,
                    status_code=response.status_code,
                    data=None,
                    error=f"HTTP {response.status_code}: {response.text}",
                    request_time=request_time
                )
                
        except requests.exceptions.RequestException as e:
            request_time = time.time() - start_time
            return ApiResponse(
                success=False,
                status_code=0,
                data=None,
                error=str(e),
                request_time=request_time
            )
    
    def call(self, request: ApiRequest, use_cache: bool = True) -> ApiResponse:
        """
        调用 API
        
        Args:
            request: API 请求
            use_cache: 是否使用缓存
            
        Returns:
            API 响应
        """
        if request.service not in self.configs:
            return ApiResponse(
                success=False,
                status_code=0,
                data=None,
                error=f"未知服务：{request.service}"
            )
        
        config = self.configs[request.service]
        
        # 检查缓存
        if use_cache:
            cached = self.cache_manager.get(request)
            if cached is not None:
                return ApiResponse(
                    success=True,
                    status_code=200,
                    data=cached,
                    cached=True
                )
        
        # 限流
        rate_limiter = self.rate_limiters[request.service]
        rate_limiter.acquire()
        
        # 执行请求（带重试）
        last_error = None
        for attempt in range(config.retry_count):
            response = self._execute_request(request, config)
            
            if response.success:
                # 缓存成功响应
                if use_cache:
                    self.cache_manager.set(request, response.data)
                return response
            
            last_error = response.error
            if attempt < config.retry_count - 1:
                logger.warning(f"请求失败，{config.retry_delay}秒后重试 ({attempt + 1}/{config.retry_count})")
                time.sleep(config.retry_delay)
        
        return ApiResponse(
            success=False,
            status_code=last_error.get('status_code', 0) if isinstance(last_error, dict) else 0,
            data=None,
            error=last_error
        )
    
    # 预定义的便捷方法
    def get_weather(self, location: str) -> ApiResponse:
        """获取天气"""
        return self.call(ApiRequest(
            service="weather",
            endpoint="current",
            params={"location": location}
        ))
    
    def translate(self, text: str, source: str = "auto", target: str = "en") -> ApiResponse:
        """翻译文本"""
        return self.call(ApiRequest(
            service="translation",
            endpoint="translate",
            data={"text": text, "source": source, "target": target}
        ))
    
    def get_news(self, category: str = "general", count: int = 10) -> ApiResponse:
        """获取新闻"""
        return self.call(ApiRequest(
            service="news",
            endpoint="top-headlines",
            params={"category": category, "count": count}
        ))
    
    def get_stock(self, symbol: str) -> ApiResponse:
        """获取股票信息"""
        return self.call(ApiRequest(
            service="stock",
            endpoint="quote",
            params={"symbol": symbol}
        ))
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "registered_apis": len(self.configs),
            "apis": list(self.configs.keys()),
            "cache_dir": str(self.cache_dir)
        }


# 预配置的 API 模板
PRESET_APIS = {
    "wttr_weather": ApiConfig(
        name="wttr_weather",
        base_url="https://wttr.in",
        timeout=10,
        rate_limit=60,
        headers={"User-Agent": "curl/7.68.0"}
    ),
    "openweather": ApiConfig(
        name="openweather",
        base_url="https://api.openweathermap.org/data/2.5",
        timeout=10,
        rate_limit=60
    ),
    "newsapi": ApiConfig(
        name="newsapi",
        base_url="https://newsapi.org/v2",
        timeout=15,
        rate_limit=30
    ),
    "deepl_translate": ApiConfig(
        name="deepl_translate",
        base_url="https://api.deepl.com/v2",
        timeout=20,
        rate_limit=50
    )
}


def setup_default_apis(api_integration: ApiIntegration):
    """设置默认 API"""
    for name, config in PRESET_APIS.items():
        if name not in api_integration.configs:
            api_integration.register_api(config)
            logger.info(f"已注册默认 API: {name}")


if __name__ == "__main__":
    # 测试
    logging.basicConfig(level=logging.INFO)
    
    api = ApiIntegration()
    setup_default_apis(api)
    
    print("API 集成框架测试")
    print("=" * 40)
    print(f"已注册 API: {api.get_stats()}")
    
    # 示例：调用天气 API（wttr.in 不需要 API key）
    print("\n测试天气 API...")
    # response = api.get_weather("Beijing")
    # print(f"响应：{response}")
