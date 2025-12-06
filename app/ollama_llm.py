import aiohttp # Асинхронный HTTP-клиент для запросов к Ollama
import json
import models  # Локальный модуль с Pydantic-моделями

# Константа с адресом API Ollama, запущенного в Docker-сети
OLLAMA_URL = "http://ollama:11434/api/chat"

# Асинхронная функция для получения краткого содержания текста через Ollama
async def summarize(session: aiohttp.ClientSession, summarizeInput: models.SummarizeInput) -> str:
    # Формирование JSON-строки с исходным текстом и инструкцией для модели
    # ensure_ascii=False сохраняет кириллицу и другие символы без экранирования
    content = json.dumps({"text": summarizeInput.original_text, "instruction": summarizeInput.instruction}, ensure_ascii=False) 
    # Список сообщений в формате, понятном Ollama API
    messages = [
        {
            # Системное сообщение задаёт правила поведения модели
            'role': 'system',
            'content': "You\'re text summarizer, do **not** add explanations, greetings, or any other words."
            "You get json with field \"text\" - that text you need analyze, and field \"instruction\" - what you need to do with text."
            "The result have to be usual text, like main keyword of text, summarized sentence and etc, do **not** make lists and json of it"
        },
        {
            # Пользовательское сообщение — передача подготовленного JSON
            'role': 'user',
            'content': content
        }
    ]
    # Тело запроса к Ollama: указание модель, сообщения и отключение потокового режим
    data = {
       "model": "gemma3",
       "messages": messages,
       "stream": False,
    }

    # Отправка POST-запрос к Ollama API
    async with session.post(OLLAMA_URL, json=data) as response:
        response.raise_for_status()    # Вызов исключений при HTTP-ошибке
        result = await response.json() # Парсинг JSON-ответ
        
        # Возвращиение только текст ответа модели
        return result["message"]["content"]