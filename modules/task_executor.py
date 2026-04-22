import os
import subprocess
import psutil
import platform
from modules.user_guide import UserGuide
from openai import OpenAI

class TaskExecutor:
    def __init__(self, model_config):
        self.os_type = platform.system()
        self.env_detector = None
        self.user_guide = UserGuide()

        self.client = OpenAI(
            base_url=model_config.get('base_url'),
            api_key=model_config.get('api_key'),
        )
        self.model_name = model_config.get('model_name')

    def set_env_detector(self, env_detector):
        self.env_detector = env_detector

    def execute_task(self, intent, user_input, env_info, history=[]):
        if intent == '磁盘使用':
            return self.get_disk_usage()
        elif intent == '文件搜索':
            return self.search_files(user_input)
        elif intent == '进程状态':
            return self.get_process_status()
        elif intent == '用户管理':
            return self.manage_user(user_input)
        elif intent == '内存使用':
            return self.get_memory_usage()
        elif intent == '用户指引':
            return self.user_guide.get_guide(user_input)
        elif intent == 'other':
            return self.handle_other_intent(user_input, env_info, history)
        else:
            return f"暂不支持该操作类型：{intent}"

    def get_disk_usage(self):
        try:
            if self.os_type == 'Windows':
                partitions = psutil.disk_partitions()
                result = []
                for partition in partitions:
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        result.append({
                            'filesystem': partition.device,
                            'total': self._format_bytes(usage.total),
                            'used': self._format_bytes(usage.used),
                            'free': self._format_bytes(usage.free),
                            'percent': usage.percent
                        })
                    except:
                        pass
                if not result:
                    usage = psutil.disk_usage('C:\\')
                    result.append({
                        'filesystem': 'C:\\',
                        'total': self._format_bytes(usage.total),
                        'used': self._format_bytes(usage.used),
                        'free': self._format_bytes(usage.free),
                        'percent': usage.percent
                    })
                output = "磁盘使用情况：\n"
                output += f"{'文件系统':<15} {'总大小':<12} {'已用':<12} {'可用':<12} {'使用率':<8}\n"
                for d in result:
                    output += f"{d['filesystem']:<15} {d['total']:<12} {d['used']:<12} {d['free']:<12} {d['percent']}%\n"
                return output
            else:
                result = subprocess.run(['df', '-h'], capture_output=True, text=True)
                return result.stdout
        except Exception as e:
            return f"获取磁盘使用情况失败：{str(e)}"

    def search_files(self, user_input):
        import re
        match = re.search(r'名为\s*([^\s的]+)\s*的?文件', user_input)
        if not match:
            match = re.search(r'搜索\s*([^\s]+)', user_input)
        if not match:
            match = re.search(r'查找\s*([^\s]+)', user_input)
        if not match:
            filename = 'config'
        else:
            filename = match.group(1)

        try:
            if self.os_type == 'Windows':
                result = subprocess.run(['where', '/r', 'C:\\', filename], capture_output=True, text=True, timeout=10)
                if result.returncode != 0 or not result.stdout.strip():
                    result = subprocess.run(['where', '/r', 'D:\\', filename], capture_output=True, text=True, timeout=10)
            else:
                search_paths = ['/etc', '/home', '/var', '/opt', '/usr']
                result = subprocess.run(['find'] + search_paths + ['-name', filename, '-type', 'f'], capture_output=True, text=True, timeout=10)
            if result.stdout.strip():
                files = result.stdout.strip().split('\n')
                if len(files) > 20:
                    return f"找到 {len(files)} 个匹配文件，显示前20个：\n" + '\n'.join(files[:20])
                return f"找到 {len(files)} 个匹配文件：\n" + result.stdout.strip()
            else:
                return f"未找到名为 {filename} 的文件"
        except Exception as e:
            return f"搜索文件失败：{str(e)}"

    def get_process_status(self):
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except:
                    pass
            processes.sort(key=lambda x: x.get('cpu_percent', 0) or 0, reverse=True)
            output = "PID\tName\tCPU%\tMemory%\n"
            for p in processes[:15]:
                name = p.get('name', 'unknown')[:20]
                pid = p.get('pid', 0)
                cpu = p.get('cpu_percent', 0) or 0
                mem = p.get('memory_percent', 0) or 0
                output += f"{pid}\t{name}\t{cpu:.1f}%\t{mem:.1f}%\n"
            return output
        except Exception as e:
            return f"获取进程状态失败：{str(e)}"

    def manage_user(self, user_input):
        import re
        is_windows = self.os_type == 'Windows'
        if is_windows:
            return "Windows系统用户管理需要通过控制面板或net user命令完成，请在PowerShell中执行相应操作。"
        if '创建' in user_input or '新增' in user_input:
            match = re.search(r'名为\s*(\w+)', user_input)
            if not match:
                match = re.search(r'用户\s*(\w+)', user_input)
            if match:
                username = match.group(1)
                try:
                    result = subprocess.run(['sudo', 'useradd', username], capture_output=True, text=True)
                    if result.returncode == 0:
                        return f"用户 {username} 创建成功"
                    else:
                        return f"创建用户失败：{result.stderr}"
                except Exception as e:
                    return f"创建用户失败：{str(e)}"
            else:
                return "请提供用户名，例如：创建一个名为testuser的用户"
        elif '删除' in user_input:
            match = re.search(r'用户\s*(\w+)', user_input)
            if match:
                username = match.group(1)
                try:
                    result = subprocess.run(['sudo', 'userdel', '-r', username], capture_output=True, text=True)
                    if result.returncode == 0:
                        return f"用户 {username} 删除成功"
                    else:
                        return f"删除用户失败：{result.stderr}"
                except Exception as e:
                    return f"删除用户失败：{str(e)}"
            else:
                return "请提供要删除的用户名"
        else:
            return "用户管理支持创建和删除用户操作"

    def get_memory_usage(self):
        try:
            mem = psutil.virtual_memory()
            output = "内存使用情况：\n"
            output += f"总内存: {self._format_bytes(mem.total)}\n"
            output += f"已用内存: {self._format_bytes(mem.used)}\n"
            output += f"可用内存: {self._format_bytes(mem.available)}\n"
            output += f"使用百分比: {mem.percent}%\n"
            return output
        except Exception as e:
            return f"获取内存使用情况失败：{str(e)}"

    def handle_other_intent(self, user_input, env_info, history=[]):
        context = ""
        if history:
            recent_history = history[-10:]
            for msg in recent_history:
                if msg['role'] == 'user':
                    context += f"用户: {msg['content']}\n"
                else:
                    context += f"助手: {msg['content']}\n"
        env_desc = f"操作系统: {env_info.get('system', 'Unknown')}"
        if env_info.get('distro'):
            env_desc += f" ({env_info.get('distro')})"
        prompt = f"""你是一个操作系统智能代理助手。用户请求了一个无法直接归类到标准意图类型的操作。

当前环境信息：{env_desc}

对话历史（最近的上下文）：
{context if context else "无"}

用户当前请求：{user_input}

请判断这个请求的性质：
1. 如果是合理的系统管理请求，请返回自然语言说明该操作的功能和用途
2. 如果是恶意的、危险的操作请求（如删除系统文件、格式化磁盘等），请返回安全警告
3. 如果是不相关的闲聊，请礼貌地引导用户回到系统管理话题

只返回自然语言描述，不需要包含命令。"""

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
            return f"处理请求时出错：{str(e)}"

    def _format_bytes(self, bytes_val):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.2f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.2f} PB"
