import requests
import json

BASE_URL = 'http://localhost:5001/api'

def test_high_risk_operations():
    print("测试高风险操作识别和处理...")
    print("=" * 60)
    
    # 测试系统核心文件或目录的删除操作
    test_high_risk_operation("删除 /etc 目录", "系统核心文件删除")
    test_high_risk_operation("删除 /usr/bin 目录", "系统核心文件删除")
    test_high_risk_operation("rm -rf /boot", "系统核心文件删除")
    
    # 测试关键安全配置的篡改
    test_high_risk_operation("修改 /etc/passwd 文件", "关键安全配置篡改")
    test_high_risk_operation("编辑 /etc/shadow 文件", "关键安全配置篡改")
    test_high_risk_operation("修改 /etc/sudoers 文件", "关键安全配置篡改")
    
    # 测试大范围的用户权限变更
    test_high_risk_operation("递归修改所有文件权限为 777", "大范围权限变更")
    test_high_risk_operation("chmod -r 777 /var", "大范围权限变更")
    test_high_risk_operation("递归更改所有文件的所有者", "大范围权限变更")
    
    # 测试危险命令
    test_high_risk_operation("rm -rf /", "危险命令")
    test_high_risk_operation("chmod 777 /", "危险命令")
    
    print("\n" + "=" * 60)
    print("高风险操作测试完成！")

def test_high_risk_operation(input_text, test_type):
    print(f"\n测试 {test_type}: {input_text}")
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
            elif result['status'] == 'error':
                print(f"错误提示: {result['message']}")
                if result['details']:
                    for detail in result['details']:
                        print(f"  - {detail}")
            else:
                print(f"结果: {result['result']}")
        else:
            print(f"错误: {response.status_code}")
    except Exception as e:
        print(f"执行错误: {str(e)}")

if __name__ == '__main__':
    test_high_risk_operations()