from pydantic import BaseModel # Базовый класс для создания моделей с валидацией данных

# Модель для входных данных при запросе суммирования
class SummarizeInput(BaseModel):
    original_text: str  # Исходный текст, который нужно обработать
    instruction: str    # Инструкция для модели

# Модель для записи результата суммирования (расширяет входные данные)
class Summaries(SummarizeInput):
    result: str         # Ответ, который вернула модель Ollama

# Модель элемента истории с временной меткой
class HistoryItem(Summaries):
    created_at: int     # Unix-timestamp момента создания записи

# Полная модель записи в истории, которая хранится в базе данных
class HistoryRecord(HistoryItem):
    id: str             # Уникальный идентификатор записи (обычно UUID или автоинкремент)
    
