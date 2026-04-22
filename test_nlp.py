from modules.nlp import NLPProcessor

nlp = NLPProcessor()

# 测试不同的用户输入
test_inputs = [
    "查询当前磁盘剩余空间",
    "搜索名为config的文件",
    "查看系统进程状态",
    "创建一个名为testuser的用户",
    "删除用户testuser",
    "你好，今天天气怎么样"
]

print("测试意图识别:")
print("=" * 50)

for input_text in test_inputs:
    intent = nlp.parse_intent(input_text)
    print(f"输入: {input_text}")
    print(f"意图: {intent}")
    print("-" * 50)