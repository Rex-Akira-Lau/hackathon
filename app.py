from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

from config import Config
from modules.nlp import NLPProcessor
from modules.task_executor import TaskExecutor
from modules.security import SecurityManager
from modules.environment import EnvironmentDetector

nlp_processor = NLPProcessor(Config.get_model_config())
security_manager = SecurityManager()
env_detector = EnvironmentDetector()
task_executor = TaskExecutor(Config.get_model_config())
task_executor.set_env_detector(env_detector)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_request():
    data = request.get_json()
    user_input = data.get('input', '')
    history = data.get('history', [])

    env_info = env_detector.get_environment_info()

    intent = nlp_processor.parse_intent(user_input, history)

    risk_level = security_manager.assess_risk(intent, user_input)

    security_explanation = security_manager.get_security_explanation(intent, user_input)

    if not security_explanation['is_valid']:
        return jsonify({
            'status': 'error',
            'intent': intent,
            'message': security_explanation['disposition'],
            'details': security_explanation['recommendations'],
            'security_explanation': security_explanation
        })

    if risk_level == 'high':
        return jsonify({
            'status': 'risk',
            'intent': intent,
            'message': '此操作风险较高，需要确认后执行',
            'details': security_manager.get_risk_details(intent, user_input),
            'security_explanation': security_explanation
        })

    result = task_executor.execute_task(intent, user_input, env_info, history)

    return jsonify({
        'status': 'success',
        'intent': intent,
        'result': result,
        'environment': env_info
    })

@app.route('/api/env', methods=['GET'])
def get_environment():
    env_info = env_detector.get_environment_info()
    package_manager = env_detector.get_package_manager()
    service_manager = env_detector.get_service_manager()
    network_tools = env_detector.get_network_tools()

    return jsonify({
        'env_info': env_info,
        'package_manager': package_manager,
        'service_manager': service_manager,
        'network_tools': network_tools
    })

@app.route('/api/capabilities', methods=['GET'])
def get_capabilities():
    capabilities = {
        'intents': [
            {'name': '磁盘使用', 'description': '查询磁盘使用情况', 'examples': ['查询当前磁盘剩余空间', '查看磁盘使用情况']},
            {'name': '文件搜索', 'description': '搜索文件或目录', 'examples': ['搜索名为config的文件', '查找test文件']},
            {'name': '进程状态', 'description': '查看进程状态', 'examples': ['查看系统进程状态', '查看占用CPU最多的进程']},
            {'name': '用户管理', 'description': '管理系统用户', 'examples': ['创建一个名为testuser的用户', '删除用户testuser']},
            {'name': '内存使用', 'description': '查看内存使用情况', 'examples': ['查看内存使用情况', '查询内存剩余空间']},
            {'name': '用户指引', 'description': '获取系统操作指引', 'examples': ['系统初始设置指南', '网络配置帮助', '安全加固指南']},
        ],
        'features': [
            {'name': '跨平台支持', 'description': '支持Ubuntu、CentOS、openEuler等多种Linux发行版'},
            {'name': '智能风险评估', 'description': '自动识别高风险操作并提醒确认'},
            {'name': '环境自动检测', 'description': '自动检测操作系统类型和发行版'},
            {'name': '自然语言反馈', 'description': '以自然语言形式反馈执行结果'},
            {'name': '新用户指引', 'description': '为刚安装系统的用户提供详细操作指南'},
            {'name': '安全日志记录', 'description': '记录所有操作并提供安全摘要'},
        ]
    }
    return jsonify(capabilities)

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify({
        'base_url': Config.OPENAI_BASE_URL,
        'model_name': Config.OPENAI_MODEL
    })

@app.route('/api/config', methods=['POST'])
def update_config():
    data = request.get_json()
    base_url = data.get('base_url')
    api_key = data.get('api_key')
    model_name = data.get('model_name')

    new_config = Config.update_config(base_url, api_key, model_name)

    global nlp_processor, task_executor
    nlp_processor = NLPProcessor(new_config)
    task_executor = TaskExecutor(new_config)
    task_executor.set_env_detector(env_detector)

    return jsonify({
        'status': 'success',
        'message': '配置已更新',
        'config': {
            'base_url': new_config['base_url'],
            'api_key': '****' + new_config['api_key'][-4:] if len(new_config['api_key']) > 4 else '****',
            'model_name': new_config['model_name']
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
