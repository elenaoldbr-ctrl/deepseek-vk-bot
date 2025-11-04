import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    VK_TOKEN = os.getenv('vk1.a.GWmNQdwn9Kr90KQ4MMVJRVyGyYYHbANIfqQWf6EHUa1sttCVVcKUmN6dPA7nuwl6JFPXHHde--WJLGDmhLDtlrxSOHctpT0jeuc4kRMtbxpYLRvj_CBQq307wzL0gH90oaw4AeVfYzWDG4HEvFo_eBHmubaOeF0Z_1g6tMsFloWpvx9HoyxMzBTo2Mu5DUg7JecPAX6Z96G3q0r5mv2Ykw')
    DEEPSEEK_API_KEY = os.getenv('sk-ff8a6de2aa754a44819c9b85477a212f')
    GROUP_ID = os.getenv('174277209')
    API_VERSION = '5.131'
    
    @classmethod
    def validate(cls):
        """Проверка наличия всех необходимых переменных"""
        required_vars = ['VK_TOKEN', 'DEEPSEEK_API_KEY', 'GROUP_ID']
        missing = [var for var in required_vars if not getattr(cls, var)]
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")