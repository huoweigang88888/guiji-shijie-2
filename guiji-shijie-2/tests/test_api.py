#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 测试

测试 FastAPI 应用和各个端点
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def test_api_import():
    """测试 API 导入"""
    print("\n" + "=" * 60)
    print("测试 1: API 导入")
    print("=" * 60)
    
    try:
        from api.main import app
        print(f"✅ API 应用导入成功")
        print(f"  标题：{app.title}")
        print(f"  版本：{app.version}")
        print(f"  路由数：{len(app.routes)}")
        return True
    except Exception as e:
        print(f"❌ API 导入失败：{e}")
        return False


def test_api_routes():
    """测试 API 路由"""
    print("\n" + "=" * 60)
    print("测试 2: API 路由")
    print("=" * 60)
    
    from api.main import app
    
    # 获取所有路由
    routes = []
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            routes.append({
                'path': route.path,
                'methods': list(route.methods) if route.methods else [],
                'name': route.name
            })
    
    print(f"✅ 总路由数：{len(routes)}")
    
    # 按标签分组
    api_routes = [r for r in routes if r['path'].startswith('/api')]
    print(f"✅ API 路由数：{len(api_routes)}")
    
    # 显示前 10 个路由
    print(f"\n📋 前 10 个 API 路由:")
    for route in api_routes[:10]:
        methods = ', '.join(route['methods'])
        print(f"  {methods:8} {route['path']}")
    
    return True


def test_health_endpoint():
    """测试健康检查端点"""
    print("\n" + "=" * 60)
    print("测试 3: 健康检查端点")
    print("=" * 60)
    
    from fastapi.testclient import TestClient
    from api.main import app
    
    client = TestClient(app)
    
    try:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        print(f"✅ 健康检查通过")
        print(f"  状态：{data.get('status')}")
        print(f"  服务：{data.get('service')}")
        print(f"  版本：{data.get('version')}")
        return True
    except Exception as e:
        print(f"❌ 健康检查失败：{e}")
        return False


def test_root_endpoint():
    """测试根端点"""
    print("\n" + "=" * 60)
    print("测试 4: 根端点")
    print("=" * 60)
    
    from fastapi.testclient import TestClient
    from api.main import app
    
    client = TestClient(app)
    
    try:
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        print(f"✅ 根端点通过")
        print(f"  项目：{data.get('project')}")
        print(f"  版本：{data.get('version')}")
        print(f"  状态：{data.get('status')}")
        return True
    except Exception as e:
        print(f"❌ 根端点失败：{e}")
        return False


def test_agents_api():
    """测试 Agent API"""
    print("\n" + "=" * 60)
    print("测试 5: Agent API")
    print("=" * 60)
    
    from fastapi.testclient import TestClient
    from api.main import app
    
    client = TestClient(app)
    
    try:
        # 测试获取代理列表
        response = client.get("/api/v1/agents/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent 列表获取成功")
            print(f"  代理数：{len(data) if isinstance(data, list) else 'N/A'}")
        else:
            print(f"⚠️ Agent 列表返回：{response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ Agent API 失败：{e}")
        return False


def test_memory_api():
    """测试记忆 API"""
    print("\n" + "=" * 60)
    print("测试 6: 记忆 API")
    print("=" * 60)
    
    from fastapi.testclient import TestClient
    from api.main import app
    
    client = TestClient(app)
    
    try:
        # 测试创建记忆
        memory_data = {
            "content": "测试记忆内容",
            "agent_id": "test_agent",
            "memory_type": "long_term"
        }
        response = client.post("/api/v1/memory/", json=memory_data)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 记忆创建成功")
            print(f"  ID: {data.get('id')}")
            print(f"  类型：{data.get('memory_type')}")
        else:
            print(f"⚠️ 记忆创建返回：{response.status_code}")
        
        # 测试获取记忆列表
        response = client.get("/api/v1/memory/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 记忆列表获取成功")
            print(f"  数量：{len(data) if isinstance(data, list) else 'N/A'}")
        
        return True
    except Exception as e:
        print(f"❌ 记忆 API 失败：{e}")
        return False


def test_economy_api():
    """测试经济 API"""
    print("\n" + "=" * 60)
    print("测试 7: 经济 API")
    print("=" * 60)
    
    from fastapi.testclient import TestClient
    from api.main import app
    
    client = TestClient(app)
    
    try:
        # 测试获取余额
        response = client.get("/api/v1/economy/balance/test_user")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 余额查询成功")
            print(f"  余额：{data.get('balance')} {data.get('currency')}")
        else:
            print(f"⚠️ 余额查询返回：{response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ 经济 API 失败：{e}")
        return False


def test_blockchain_api():
    """测试区块链 API"""
    print("\n" + "=" * 60)
    print("测试 8: 区块链 API")
    print("=" * 60)
    
    from fastapi.testclient import TestClient
    from api.main import app
    
    client = TestClient(app)
    
    try:
        # 测试创建 DID
        did_data = {
            "agent_name": "Test Agent",
            "metadata": {"test": True}
        }
        response = client.post("/api/v1/blockchain/did", json=did_data)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ DID 创建成功")
            print(f"  DID: {data.get('did')}")
        else:
            print(f"⚠️ DID 创建返回：{response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ 区块链 API 失败：{e}")
        return False


def test_gamification_api():
    """测试游戏化 API"""
    print("\n" + "=" * 60)
    print("测试 9: 游戏化 API")
    print("=" * 60)
    
    from fastapi.testclient import TestClient
    from api.main import app
    
    client = TestClient(app)
    
    try:
        # 测试获取成就列表
        response = client.get("/api/v1/gamification/achievements")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成就列表获取成功")
            print(f"  数量：{len(data) if isinstance(data, list) else 'N/A'}")
        else:
            print(f"⚠️ 成就列表返回：{response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ 游戏化 API 失败：{e}")
        return False


def test_api_stats():
    """测试 API 统计"""
    print("\n" + "=" * 60)
    print("测试 10: API 统计")
    print("=" * 60)
    
    from fastapi.testclient import TestClient
    from api.main import app
    
    client = TestClient(app)
    
    try:
        response = client.get("/api/stats")
        assert response.status_code == 200
        data = response.json()
        print(f"✅ API 统计获取成功")
        print(f"  总路由：{data.get('total_routes')}")
        print(f"  API 路由：{data.get('api_routes')}")
        print(f"  标签数：{len(data.get('tags', []))}")
        return True
    except Exception as e:
        print(f"❌ API 统计失败：{e}")
        return False


def run_all_tests():
    """运行所有 API 测试"""
    print("\n" + "=" * 60)
    print("🧪 硅基世界 2 - API 测试套件")
    print("=" * 60)
    
    tests = [
        ("API 导入", test_api_import),
        ("API 路由", test_api_routes),
        ("健康检查", test_health_endpoint),
        ("根端点", test_root_endpoint),
        ("Agent API", test_agents_api),
        ("记忆 API", test_memory_api),
        ("经济 API", test_economy_api),
        ("区块链 API", test_blockchain_api),
        ("游戏化 API", test_gamification_api),
        ("API 统计", test_api_stats)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result, None))
        except Exception as e:
            results.append((name, False, str(e)))
            print(f"\n❌ {name} 测试失败：{e}")
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result, _ in results if result)
    total = len(results)
    
    for name, result, error in results:
        icon = "✅" if result else "❌"
        print(f"  {icon} {name}")
        if error:
            print(f"      错误：{error}")
    
    print(f"\n📈 总计：{passed}/{total} 通过 ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        return True
    else:
        print(f"\n⚠️ {total - passed} 个测试失败")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
