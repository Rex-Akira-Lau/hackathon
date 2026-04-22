import requests
import json

BASE_URL = 'http://localhost:5001/api'

def test_security_features():
    print("测试安全管理功能...")
    print("=" * 60)
    
    # 测试高风险操作
    test_high_risk_operation("创建一个名为testuser的用户")
    test_high_risk_operation("删除用户testuser")
    test_high_risk_operation("执行rm -rf /命令")
    test_high_risk_operation("重启系统")
    
    # 测试安全信息API
    test_security_info()
    
    print("\n" + "=" * 60)
    print("安全管理功能测试完成！")

def test_high_risk_operation(input_text):
    print(f"\n测试高风险操作: {input_text}")
    url = f'{BASE_URL}/process'
    data = {'input': input_text}
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"状态: {result['status']}")
            print(f"意图: {result['intent']}")
            if result['status'] == 'risk':
                print(f"风险提示: {result['message']}")
                if result['details']:
                    for detail in result['details']:
                        print(f"  - {detail}")
            else:
                print(f"结果: {result['result']}")
        else:
            print(f"错误: {response.status_code}")
    except Exception as e:
        print(f"执行错误: {str(e)}")

def test_security_info():
    print("\n测试安全信息API")
    url = f'{BASE_URL}/security'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            print(f"状态: 成功")
            print(f"总操作数: {result['summary']['total_operations']}")
            print(f"高风险操作数: {result['summary']['high_risk_count']}")
            if result['history']:
                print(f"最近操作数: {len(result['history'])}")
                print("最近3条操作:")
                for i, op in enumerate(result['history'][-3:], 1):
                    print(f"  {i}. {op['timestamp']} - {op['intent']}: {op['input']}")
        else:
            print(f"错误: {response.status_code}")
    except Exception as e:
        print(f"执行错误: {str(e)}")

if __name__ == '__main__':
    test_security_features()