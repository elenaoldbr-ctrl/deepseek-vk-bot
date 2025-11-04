import requests
import json
from config import Config
import logging

logger = logging.getLogger(__name__)

class DeepSeekClient:
    def __init__(self):
        self.api_key = Config.DEEPSEEK_API_KEY
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        logger.info("DeepSeek client initialized")
    
    def send_message(self, message, conversation_history=None):
        if conversation_history is None:
            conversation_history = []
        
        # Ограничиваем историю сообщений для экономии токенов
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]
            logger.info("Conversation history truncated to 10 messages")
        
        messages = conversation_history + [
            {"role": "user", "content": message}
        ]
        
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "stream": False,
            "max_tokens": 2048,
            "temperature": 0.7
        }
        
        try:
            logger.info(f"Sending request to DeepSeek API (message length: {len(message)})")
            
            response = requests.post(
                self.base_url, 
                headers=self.headers, 
                json=payload,
                timeout=60
            )
            
            # Логируем статус ответа
            logger.info(f"API response status: {response.status_code}")
            
            response.raise_for_status()
            
            result = response.json()
            
            # Проверяем наличие ожидаемых полей в ответе
            if 'choices' not in result or len(result['choices']) == 0:
                raise KeyError("No choices in API response")
            
            reply = result['choices'][0]['message']['content']
            
            # Логируем длину ответа
            logger.info(f"Successfully received response (length: {len(reply)})")
            
            return reply
            
        except requests.exceptions.Timeout:
            error_msg = "⏰ Время ожидания ответа истекло. Пожалуйста, попробуйте еще раз."
            logger.error("DeepSeek API timeout after 60 seconds")
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                error_msg = "🔑 Ошибка аутентификации API. Проверьте API ключ."
            elif e.response.status_code == 429:
                error_msg = "🚫 Превышен лимит запросов. Попробуйте позже."
            elif e.response.status_code == 500:
                error_msg = "🔧 Внутренняя ошибка сервера API. Попробуйте позже."
            else:
                error_msg = f"🔌 Ошибка HTTP {e.response.status_code}: {str(e)}"
            logger.error(f"HTTP error: {e}")
            
        except requests.exceptions.RequestException as e:
            error_msg = f"🔌 Ошибка соединения: {str(e)}"
            logger.error(f"Request exception: {e}")
            
        except KeyError as e:
            error_msg = "🔧 Ошибка в формате ответа от API"
            logger.error(f"KeyError in API response: {e}, response: {result if 'result' in locals() else 'No result'}")
            
        except json.JSONDecodeError as e:
            error_msg = "🔧 Ошибка обработки ответа от API"
            logger.error(f"JSON decode error: {e}")
            
        except Exception as e:
            error_msg = f"⚠️ Произошла непредвиденная ошибка: {str(e)}"
            logger.error(f"Unexpected error: {e}", exc_info=True)
        
        return error_msg