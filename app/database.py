import asyncpg                   # Асинхронный драйвер PostgreSQL
from dotenv import load_dotenv   # Загрузка переменных окружения из .env
import os
import models                    # Pydantic-модели
from typing import List

# Загружаем переменные окружения из файла .env (POSTGRES_DB, POSTGRES_USER и т.д.)
load_dotenv()

# Создание пула соединений с PostgreSQL и инициализируем таблицу
async def init_db():
    # Формирование пула соединений, хост "db" — имя сервиса в docker-compose
    pool = await asyncpg.create_pool(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="db",
        command_timeout=60
    )

    # Получение соединения из пула для создания структуры БД
    async with pool.acquire() as con:
        # Включение расширение для генерации UUID, если его ещё нет
        await con.execute('''
            CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        ''')
        # Создание таблицу history, если она ещё не существует
        await con.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                original_text TEXT NOT NULL,
                instruction TEXT NOT NULL,
                result TEXT NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );
        ''')

    return pool

# Корректно закрытие пула соединений при завершении работы приложения
async def close_db(pool: asyncpg.pool.Pool):
    await pool.close()

# Сохранение одной записи о суммировании в таблицу history
async def save_to_history(pool: asyncpg.pool.Pool, summary: models.Summaries):
    async with pool.acquire() as con:
        await con.execute('''
        INSERT INTO history (original_text, instruction, result)
            VALUES ($1, $2, $3)
    ''', summary.original_text, summary.instruction, summary.result)

# Получение последних 100 записей из истории
async def get_history(pool: asyncpg.pool.Pool)->List[models.HistoryItem]:
    history_items = []

    try:
        raw_records = []
        # Получение соединение и выполняем запрос с сортировкой по времени (от новых к старым)
        async with pool.acquire() as con:
            raw_records = await con.fetch('''
                SELECT
                    original_text, 
                    instruction, 
                    result, 
                    created_at
                FROM history
                ORDER BY created_at DESC
                LIMIT 100
            ''')
        
        # Преобразование каждой строки БД в HistoryItem
        history_items = [
            models.HistoryItem(
                original_text=record["original_text"],
                instruction=record["instruction"],
                result=record["result"],
                created_at=int(record["created_at"].timestamp()) # Перевод datetime в Unix-timestamp
            )
            for record in raw_records
        ]
    except:
        pass

    return history_items