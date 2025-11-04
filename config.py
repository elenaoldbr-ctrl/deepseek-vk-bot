import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Для Render используем os.getenv() напрямую
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    VK_GROUP_TOKEN = os.getenv('VK_GROUP_TOKEN')
    VK_GROUP_ID = os.getenv('VK_GROUP_ID')
    API_VERSION = '5.131'
    
    @classmethod
    def validate(cls):
        """Проверка что все переменные загружены"""
        required = {
            'DEEPSEEK_API_KEY': cls.DEEPSEEK_API_KEY,
            'VK_GROUP_TOKEN': cls.VK_GROUP_TOKEN,
            'VK_GROUP_ID': cls.VK_GROUP_ID
        }
        
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")

# Проверяем при импорте
Config.validate()
