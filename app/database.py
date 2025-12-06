import asyncio
import asyncpg
from dotenv import load_dotenv
import os
from datetime import datetime
import models
from typing import List

load_dotenv()

async def init_db():
    pool = await asyncpg.create_pool(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="db",
        command_timeout=60
    )

    async with pool.acquire() as con:
        await con.execute('''
            CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        ''')
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

async def close_db(pool: asyncpg.pool.Pool):
    await pool.close()

async def save_to_history(pool: asyncpg.pool.Pool, summary: models.Summaries):
    async with pool.acquire() as con:
        await con.execute('''
        INSERT INTO history (original_text, instruction, result)
            VALUES ($1, $2, $3)
    ''', summary.original_text, summary.instruction, summary.result)

async def get_history(pool: asyncpg.pool.Pool)->List[models.HistoryItem]:
    history_items = []

    try:
        raw_records = []
        async with pool.acquire() as con:
            raw_records = await con.fetch('''
                SELECT
                    original_text, 
                    instruction, 
                    result, 
                    created_at
                FROM history
                ORDER BY created_at DESC
            ''')

        history_items = [
            models.HistoryItem(
                original_text=record["original_text"],
                instruction=record["instruction"],
                result=record["result"],
                created_at=int(record["created_at"].timestamp())
            )
            for record in raw_records
        ]
    except:
        pass

    return history_items