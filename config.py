import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api-inference.modelscope.cn/v1')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'Qwen/Qwen3-235B-A22B-Instruct-2507')

    @classmethod
    def get_model_config(cls):
        return {
            'base_url': cls.OPENAI_BASE_URL,
            'api_key': cls.OPENAI_API_KEY,
            'model_name': cls.OPENAI_MODEL
        }

    @classmethod
    def update_config(cls, base_url=None, api_key=None, model_name=None):
        if base_url:
            cls.OPENAI_BASE_URL = base_url
        if api_key:
            cls.OPENAI_API_KEY = api_key
        if model_name:
            cls.OPENAI_MODEL = model_name

        config_path = os.path.join(os.path.dirname(__file__), '.env')
        with open(config_path, 'w') as f:
            f.write(f'# ModelScope API Configuration\n')
            f.write(f'OPENAI_BASE_URL={cls.OPENAI_BASE_URL}\n')
            f.write(f'OPENAI_API_KEY={cls.OPENAI_API_KEY}\n')
            f.write(f'OPENAI_MODEL={cls.OPENAI_MODEL}\n')

        return cls.get_model_config()
