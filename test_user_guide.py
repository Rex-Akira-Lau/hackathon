import requests
import json

BASE_URL = 'http://localhost:5001/api'

def test_user_guide():
    print("测试用户指引功能...")
    print("=" * 60)
    
    # 测试系统初始设置指南
    test_request("系统初始设置指南")
    
    # 测试网络配置指南
    test_request("网络配置帮助")
    
    # 测试安全加固指南
    test_request("安全加固指南")
    
    # 测试性能优化指南
    test_request("性能优化指南")
    
    # 测试存储管理指南
    test_request("存储管理指南")
    
    # 测试备份指南
    test_request("系统备份指南")
    
    print("\n" + "=" * 60)
    print("用户指引功能测试完成！")

def test_request(input_text):
    print(f"\n测试: {input_text}")
    url = f'{BASE_URL}/process'
    data = {'input': input_text}
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"状态: {result['status']}")
            print(f"意图: {result['intent']}")
            if result['result']:
                # 只显示前100个字符，避免输出过长
                preview = result['result'][:500] + ('...' if len(result['result']) > 500 else '')
                print(f"结果预览: {preview}")
        else:
            print(f"错误: {response.status_code}")
    except Exception as e:
        print(f"执行错误: {str(e)}")

if __name__ == '__main__':
    test_user_guide()