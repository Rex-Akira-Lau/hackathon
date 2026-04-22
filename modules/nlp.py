from openai import OpenAI
import re

class NLPProcessor:
    def __init__(self, model_config):
        self.client = OpenAI(
            base_url=model_config.get('base_url'),
            api_key=model_config.get('api_key'),
        )
        self.model_name = model_config.get('model_name')

    def parse_intent(self, user_input, history=[]):
        context = ""
        if history:
            recent_history = history[-10:]
            for msg in recent_history:
                if msg['role'] == 'user':
                    context += f"用户: {msg['content']}\n"
                else:
                    context += f"助手: {msg['content']}\n"

        prompt = f"""你是一个操作系统智能代理助手，负责理解用户的系统管理意图。

对话历史（最近的上下文）：
{context if context else "无"}

当前用户输入：{user_input}

请分析用户输入，判断其系统管理意图。

支持的意图类型：
1. 磁盘使用 - 查询磁盘使用情况、剩余空间
2. 文件搜索 - 搜索文件或目录
3. 进程状态 - 查看进程状态
4. 用户管理 - 管理系统用户（创建/删除用户）
5. 内存使用 - 查看内存使用情况
6. 用户指引 - 获取系统操作指引和帮助
7. 网络工具 - 使用网络诊断工具
8. 服务管理 - 管理系统服务
9. 软件包管理 - 安装、卸载软件包
10. other - 无法归类到上述类型的其他请求

请返回JSON格式的意图识别结果：
{{"intent": "意图名称", "confidence": 0.0-1.0, "needs_clarification": true/false}}

直接返回JSON，不要包含其他内容。"""

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=200,
                timeout=30
            )
            result_text = response.choices[0].message.content.strip()

            if result_text.startswith('```json'):
                result_text = result_text[7:]
            if result_text.startswith('```'):
                result_text = result_text[3:]
            if result_text.endswith('```'):
                result_text = result_text[:-3]

            import json
            result = json.loads(result_text.strip())

            intent = result.get('intent', 'other')
            confidence = result.get('confidence', 0.0)

            if confidence < 0.4:
                return 'other'

            return intent

        except Exception as e:
            print(f"意图识别出错: {e}")
            return 'other'

    def generate_response(self, user_input, context_info, history=[]):
        context = ""
        if history:
            recent_history = history[-10:]
            for msg in recent_history:
                if msg['role'] == 'user':
                    context += f"用户: {msg['content']}\n"
                else:
                    context += f"助手: {msg['content']}\n"

        prompt = f"""你是一个操作系统智能代理助手，用自然语言反馈系统命令的执行结果。

对话历史（最近的上下文）：
{context if context else "无"}

用户请求：{user_input}

执行结果信息：
{context_info}

请用清晰、友好的自然语言向用户解释执行结果。返回自然语言描述即可，不需要包含命令。"""

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"生成响应出错: {e}")
            return str(context_info)
