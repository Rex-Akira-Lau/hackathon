import logging
import datetime
import os

class SecurityManager:
    def __init__(self):
        # 定义高风险操作列表
        self.high_risk_operations = [
            '用户管理',  # 用户管理操作
            '删除',  # 删除操作
            '格式化',  # 格式化操作
            'rm -rf',  # 危险的删除命令
            'systemctl stop',  # 停止系统服务
            'systemctl disable',  # 禁用系统服务
            'reboot',  # 重启系统
            'shutdown',  # 关闭系统
            'chmod 777',  # 危险的权限设置
            'sudo',  # 提升权限操作
        ]
        
        # 定义中风险操作列表
        self.medium_risk_operations = [
            '磁盘使用',  # 查看磁盘使用情况
            '文件搜索',  # 搜索文件
            '进程状态',  # 查看进程状态
            '内存使用',  # 查看内存使用情况
            'systemctl start',  # 启动系统服务
            'systemctl restart',  # 重启系统服务
        ]
        
        # 初始化日志记录
        self._init_logger()
        
        # 操作历史记录
        self.operation_history = []
    
    def _init_logger(self):
        # 初始化安全日志记录器
        self.logger = logging.getLogger('security')
        self.logger.setLevel(logging.INFO)
        
        # 检查是否已经有处理器，避免重复添加
        if not self.logger.handlers:
            # 创建日志目录
            log_dir = 'logs'
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # 创建文件处理器
            log_file = os.path.join(log_dir, 'security.log')
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.INFO)
            
            # 设置日志格式
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            
            # 添加处理器
            self.logger.addHandler(file_handler)
    
    def assess_risk(self, intent, user_input):
        # 评估操作风险级别
        user_input_lower = user_input.lower()
        
        # 记录操作
        self._log_operation(intent, user_input)
        
        # 检查意图是否为高风险
        if intent in ['用户管理']:
            return 'high'
        
        # 检查用户输入中是否包含高风险关键词
        for risk_op in self.high_risk_operations:
            if risk_op in user_input_lower:
                return 'high'
        
        # 检查系统核心文件或目录的删除操作
        core_files_dirs = [
            '/etc', '/usr', '/bin', '/sbin', '/boot', '/lib', '/lib64',
            'c:\\windows', 'c:\\system32', 'c:\\program files'
        ]
        for core_path in core_files_dirs:
            if ('删除' in user_input or 'delete' in user_input_lower or 'rm' in user_input_lower) and core_path in user_input_lower:
                return 'high'
        
        # 检查关键安全配置的篡改
        security_configs = [
            '/etc/passwd', '/etc/shadow', '/etc/sudoers', '/etc/ssh',
            'c:\\windows\\system32\\config', 'c:\\windows\\system32\\drivers\\etc'
        ]
        for config in security_configs:
            if ('修改' in user_input or 'edit' in user_input_lower or 'change' in user_input_lower) and config in user_input_lower:
                return 'high'
        
        # 检查大范围的用户权限变更
        if ('权限' in user_input or 'permission' in user_input_lower or 'chmod' in user_input_lower or 'chown' in user_input_lower) and \
           ('所有' in user_input or '全部' in user_input or 'recursive' in user_input_lower or '-r' in user_input_lower):
            return 'high'
        
        # 检查意图是否为中风险
        if intent in self.medium_risk_operations:
            return 'medium'
        
        return 'low'
    
    def get_risk_details(self, intent, user_input):
        # 提供风险详情
        details = []
        user_input_lower = user_input.lower()
        
        if intent == '用户管理':
            if '删除' in user_input or 'delete' in user_input_lower:
                details.append('删除用户操作可能导致数据丢失')
                details.append('请确认是否要执行此操作')
                details.append('建议在执行前备份用户数据')
            elif '创建' in user_input or 'add' in user_input_lower:
                details.append('创建用户操作需要管理员权限')
                details.append('请确认是否要执行此操作')
                details.append('建议设置强密码和适当的权限')
        
        if 'rm -rf' in user_input_lower:
            details.append('此命令可能导致重要文件被删除')
            details.append('请确认操作范围是否正确')
            details.append('建议先查看目录内容再执行')
        
        if '格式化' in user_input or 'format' in user_input_lower:
            details.append('格式化操作会清除所有数据')
            details.append('请确认是否要执行此操作')
            details.append('建议在执行前备份重要数据')
        
        if 'reboot' in user_input_lower or '重启' in user_input:
            details.append('重启操作会中断当前系统运行')
            details.append('请确认是否要执行此操作')
            details.append('建议在执行前保存所有工作')
        
        if 'shutdown' in user_input_lower or '关闭' in user_input:
            details.append('关闭操作会停止系统运行')
            details.append('请确认是否要执行此操作')
            details.append('建议在执行前保存所有工作')
        
        # 检查系统核心文件或目录的删除操作
        core_files_dirs = [
            '/etc', '/usr', '/bin', '/sbin', '/boot', '/lib', '/lib64',
            'c:\\windows', 'c:\\system32', 'c:\\program files'
        ]
        for core_path in core_files_dirs:
            if ('删除' in user_input or 'delete' in user_input_lower or 'rm' in user_input_lower) and core_path in user_input_lower:
                details.append('删除系统核心文件或目录可能导致系统崩溃')
                details.append('此操作风险极高，可能导致系统无法启动')
                details.append('建议不要执行此操作，或在执行前进行完整系统备份')
                break
        
        # 检查关键安全配置的篡改
        security_configs = [
            '/etc/passwd', '/etc/shadow', '/etc/sudoers', '/etc/ssh',
            'c:\\windows\\system32\\config', 'c:\\windows\\system32\\drivers\\etc'
        ]
        for config in security_configs:
            if ('修改' in user_input or 'edit' in user_input_lower or 'change' in user_input_lower) and config in user_input_lower:
                details.append('修改关键安全配置可能导致系统安全漏洞')
                details.append('此操作可能被恶意利用，造成安全风险')
                details.append('建议在执行前备份原始配置文件，并确保修改正确')
                break
        
        # 检查大范围的用户权限变更
        if ('权限' in user_input or 'permission' in user_input_lower or 'chmod' in user_input_lower or 'chown' in user_input_lower) and \
           ('所有' in user_input or '全部' in user_input or 'recursive' in user_input_lower or '-r' in user_input_lower):
            details.append('大范围的权限变更可能导致系统安全风险')
            details.append('错误的权限设置可能导致文件无法访问或被恶意利用')
            details.append('建议先在小范围内测试权限设置，确保不会影响系统运行')
        
        return details
    
    def validate_operation(self, intent, user_input):
        # 验证操作是否合法
        user_input_lower = user_input.lower()
        
        # 检查是否包含危险命令
        dangerous_commands = [
            'rm -rf /',
            'format c:',
            'shutdown -h now',
            'rm -rf /etc',
            'rm -rf /usr',
            'chmod 777 /',
            'chmod 777 /etc',
        ]
        
        for cmd in dangerous_commands:
            if cmd in user_input_lower:
                self.logger.warning(f'拒绝执行危险命令: {cmd}')
                return False
        
        # 检查系统核心文件或目录的删除操作
        core_files_dirs = [
            '/etc', '/usr', '/bin', '/sbin', '/boot', '/lib', '/lib64',
            'c:\\windows', 'c:\\system32', 'c:\\program files'
        ]
        for core_path in core_files_dirs:
            if ('删除' in user_input or 'delete' in user_input_lower or 'rm' in user_input_lower) and core_path in user_input_lower:
                self.logger.warning(f'拒绝执行核心文件删除操作: {user_input}')
                return False
        
        # 检查关键安全配置的篡改
        security_configs = [
            '/etc/passwd', '/etc/shadow', '/etc/sudoers', '/etc/ssh',
            'c:\\windows\\system32\\config', 'c:\\windows\\system32\\drivers\\etc'
        ]
        for config in security_configs:
            if ('修改' in user_input or 'edit' in user_input_lower or 'change' in user_input_lower) and config in user_input_lower:
                # 记录警告，但允许执行（需要二次确认）
                self.logger.warning(f'检测到关键安全配置修改操作: {user_input}')
                # 不返回False，因为需要二次确认
        
        # 检查大范围的用户权限变更
        if ('权限' in user_input or 'permission' in user_input_lower or 'chmod' in user_input_lower or 'chown' in user_input_lower) and \
           ('所有' in user_input or '全部' in user_input or 'recursive' in user_input_lower or '-r' in user_input_lower):
            # 记录警告，但允许执行（需要二次确认）
            self.logger.warning(f'检测到大范围权限变更操作: {user_input}')
            # 不返回False，因为需要二次确认
        
        return True
    
    def _log_operation(self, intent, user_input):
        # 记录操作
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f'操作: {intent} - 输入: {user_input}'
        self.logger.info(log_message)
        
        # 添加到操作历史
        self.operation_history.append({
            'timestamp': timestamp,
            'intent': intent,
            'input': user_input,
        })
        
        # 限制历史记录长度
        if len(self.operation_history) > 100:
            self.operation_history.pop(0)
    
    def get_operation_history(self, limit=10):
        # 获取操作历史
        return self.operation_history[-limit:]
    
    def get_security_summary(self):
        # 获取安全摘要
        high_risk_count = sum(1 for op in self.operation_history if op['intent'] == '用户管理')
        total_operations = len(self.operation_history)
        
        return {
            'total_operations': total_operations,
            'high_risk_count': high_risk_count,
            'last_operation': self.operation_history[-1] if self.operation_history else None
        }
    
    def get_security_explanation(self, intent, user_input):
        """生成安全判定的解释"""
        user_input_lower = user_input.lower()
        explanation = {
            'risk_level': self.assess_risk(intent, user_input),
            'is_valid': self.validate_operation(intent, user_input),
            'risk_factors': [],
            'disposition': '',
            'recommendations': []
        }
        
        # 分析风险因素
        if intent in ['用户管理']:
            explanation['risk_factors'].append('用户管理操作需要管理员权限，可能影响系统安全')
        
        # 检查高风险关键词
        for risk_op in self.high_risk_operations:
            if risk_op in user_input_lower:
                explanation['risk_factors'].append(f'包含高风险操作: {risk_op}')
        
        # 检查系统核心文件或目录的删除操作
        core_files_dirs = [
            '/etc', '/usr', '/bin', '/sbin', '/boot', '/lib', '/lib64',
            'c:\\windows', 'c:\\system32', 'c:\\program files'
        ]
        for core_path in core_files_dirs:
            if ('删除' in user_input or 'delete' in user_input_lower or 'rm' in user_input_lower) and core_path in user_input_lower:
                explanation['risk_factors'].append(f'尝试删除系统核心文件或目录: {core_path}')
                break
        
        # 检查关键安全配置的篡改
        security_configs = [
            '/etc/passwd', '/etc/shadow', '/etc/sudoers', '/etc/ssh',
            'c:\\windows\\system32\\config', 'c:\\windows\\system32\\drivers\\etc'
        ]
        for config in security_configs:
            if ('修改' in user_input or 'edit' in user_input_lower or 'change' in user_input_lower) and config in user_input_lower:
                explanation['risk_factors'].append(f'尝试修改关键安全配置: {config}')
                break
        
        # 检查大范围的用户权限变更
        if ('权限' in user_input or 'permission' in user_input_lower or 'chmod' in user_input_lower or 'chown' in user_input_lower) and \
           ('所有' in user_input or '全部' in user_input or 'recursive' in user_input_lower or '-r' in user_input_lower):
            explanation['risk_factors'].append('尝试进行大范围的权限变更')
        
        # 检查危险命令
        dangerous_commands = [
            'rm -rf /',
            'format c:',
            'shutdown -h now',
            'rm -rf /etc',
            'rm -rf /usr',
            'chmod 777 /',
            'chmod 777 /etc',
        ]
        for cmd in dangerous_commands:
            if cmd in user_input_lower:
                explanation['risk_factors'].append(f'包含危险命令: {cmd}')
                break
        
        # 确定处置结果
        if not explanation['is_valid']:
            explanation['disposition'] = '操作被拒绝: 此操作风险极高，可能导致系统损坏'
            explanation['recommendations'].append('系统已拒绝执行此高风险操作')
            explanation['recommendations'].append('请检查操作命令是否正确')
            explanation['recommendations'].append('如需执行此操作，请手动确认并使用系统命令行')
        elif explanation['risk_level'] == 'high':
            explanation['disposition'] = '需要二次确认: 此操作风险较高，可能影响系统安全'
            explanation['recommendations'].append('请确认是否要执行此操作')
            explanation['recommendations'].append('建议在执行前备份相关数据')
            explanation['recommendations'].append('确保您了解操作的后果')
        else:
            explanation['disposition'] = '操作安全: 此操作风险较低，可以安全执行'
            explanation['recommendations'].append('操作已通过安全检查')
        
        return explanation