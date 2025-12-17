import ollama_llm                              # Модуль для общения с Ollama
import aiohttp                                 # Асинхронный HTTP-клиент, нужен для запросов к модели
import uvicorn                                 # Cервер для запуска FastAPI-приложения
import database                                # Модуль работы с базой данных
from fastapi import FastAPI, Request          
from fastapi.responses import HTMLResponse     # Ответ в виде HTML-страницы
import models                                  # Pydantic-модели
from fastapi.templating import Jinja2Templates # Шаблонизатор Jinja2
from contextlib import asynccontextmanager     # Менеджер жизненного цикла приложения


# Менеджер контекста, который выполняется при старте и завершении приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём общую aiohttp-сессию для всех запросов к Ollama
    app.state.http_session = aiohttp.ClientSession()
    # Инициализируем пул соединений с PostgreSQL
    app.state.pool = await database.init_db()

    yield

    # После завершения работы приложения закрываем ресурсы
    app.state.http_session.close()
    database.close_db(app.state.pool)

# Создание экземпляр FastAPI с указанным lifespan
app = FastAPI(lifespan=lifespan)

# Настройка Jinja2 для рендеринга HTML-шаблонов из папки templates
templates = Jinja2Templates(directory="templates")

# Главная страница — передача index-шаблон
@app.get("/",
         summary="Главная страница приложения",
         response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="main.html"
    )

# Страница с историей суммаризаций
@app.get("/historyPage",
        summary="Страница с историей суммаризаций",
        response_class=HTMLResponse)
async def historyPage(request: Request):
    return templates.TemplateResponse(
        request=request, name="history.html"
    )

# Эндпоинт для выполнения суммаризации текста
@app.post("/summarize",
          summary="Суммаризирует входной текст по входной инструкции",
          )
async def summarize(summarizeInput: models.SummarizeInput):
    # Получаем результат от локальной модели через ollama_llm
    result = await ollama_llm.summarize(app.state.http_session, summarizeInput)

    # Формирование записи для сохранения в историю
    summary = models.Summaries(
        original_text=summarizeInput.original_text,
        instruction=summarizeInput.instruction,
        result=result
    )
    
    # Сохранение записи в базу данных
    await database.save_to_history(app.state.pool, summary)
    # Возвращаем клиенту только результат суммирования
    return {"result": result}


# Эндпоинт для получения всей истории суммирований (для фронтенда)
@app.get("/history",
         summary="Возвращает историю запросов пользователя")
async def history():
    history = await database.get_history(app.state.pool)
    return history

# Точка входа — запуск сервера
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)