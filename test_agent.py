import unittest
from modules.nlp import NLPProcessor
from modules.task_executor import TaskExecutor
from modules.security import SecurityManager
from modules.environment import EnvironmentDetector

class TestAgentModules(unittest.TestCase):
    def setUp(self):
        self.nlp_processor = NLPProcessor()
        self.task_executor = TaskExecutor()
        self.security_manager = SecurityManager()
        self.env_detector = EnvironmentDetector()
    
    def test_environment_detection(self):
        """测试环境检测模块"""
        env_info = self.env_detector.get_environment_info()
        self.assertIn('system', env_info)
        self.assertIn('user', env_info)
        self.assertIn('hostname', env_info)
    
    def test_security_assessment(self):
        """测试安全风险评估模块"""
        # 测试高风险操作
        high_risk_result = self.security_manager.assess_risk('user_management', '删除用户 testuser')
        self.assertEqual(high_risk_result, 'high')
        
        # 测试低风险操作
        low_risk_result = self.security_manager.assess_risk('disk_usage', '查询磁盘使用情况')
        self.assertEqual(low_risk_result, 'low')
    
    def test_task_executor_initialization(self):
        """测试任务执行器初始化"""
        self.assertIsInstance(self.task_executor, TaskExecutor)

if __name__ == '__main__':
    unittest.main()