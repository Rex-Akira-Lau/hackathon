import requests
import json

BASE_URL = 'http://localhost:5001/api'

def test_other_intent():
    print("测试other意图处理功能...")
    print("=" * 60)
    
    # 测试一些不会被识别为其他意图的问题
    test_request("今天天气怎么样")
    test_request("你好，能帮我做什么")
    test_request("什么是人工智能")
    test_request("如何学习编程")
    test_request("北京有哪些景点")
    
    print("\n" + "=" * 60)
    print("other意图处理测试完成！")

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
                # 只显示前500个字符，避免输出过长
                preview = result['result'][:500] + ('...' if len(result['result']) > 500 else '')
                print(f"结果预览: {preview}")
        else:
            print(f"错误: {response.status_code}")
    except Exception as e:
        print(f"执行错误: {str(e)}")

if __name__ == '__main__':
    test_other_intent()