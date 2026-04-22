import requests
import json

BASE_URL = 'http://localhost:5001/api'

def test_endpoint(endpoint, method='GET', data=None):
    url = f'{BASE_URL}{endpoint}'
    if method == 'POST':
        response = requests.post(url, json=data)
    else:
        response = requests.get(url)
    
    print(f"Testing {endpoint}...")
    print(f"Status code: {response.status_code}")
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        return data
    except:
        print(f"Response content: {response.text}")
        return None
    print("-" * 60)

def test_process(input_text):
    print(f"\nTesting process: {input_text}")
    data = test_endpoint('/process', method='POST', data={'input': input_text})
    return data

# 测试环境信息
print("=" * 60)
print("Testing environment info...")
test_endpoint('/env')

# 测试能力列表
print("\n" + "=" * 60)
print("Testing capabilities...")
test_endpoint('/capabilities')

# 测试各种命令
print("\n" + "=" * 60)
print("Testing commands...")

# 测试磁盘使用情况
test_process("查询当前磁盘剩余空间")

# 测试进程状态
test_process("查看系统进程状态")

# 测试文件搜索
test_process("搜索名为nginx的配置文件")

# 测试内存使用情况
test_process("查看内存使用情况")

print("\n" + "=" * 60)
print("All tests completed!")