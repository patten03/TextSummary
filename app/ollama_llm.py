import asyncio
import aiohttp
import json
import models

OLLAMA_URL = "http://ollama:11434/api/chat"


async def summarize(session: aiohttp.ClientSession, summarizeInput: models.SummarizeInput) -> str:
    content = json.dumps({"text": summarizeInput.original_text, "instruction": summarizeInput.instruction}, ensure_ascii=False) 

    messages = [
        {
            'role': 'system',
            'content': "You\'re text summarizer, do **not** add explanations, greetings, or any other words."
            "You get json with field \"text\" - that text you need analyze, and field \"instruction\" - what you need to do with text."
            "The result have to be usual text, like main keyword of text, summarized sentence and etc, do **not** make lists and json of it"
        },
        {
            'role': 'user',
            'content': content
        }
    ]
    data = {
       "model": "gemma3",
       "messages": messages,
       "stream": False,
    }

    async with session.post(OLLAMA_URL, json=data) as response:
        response.raise_for_status()
        result = await response.json()
        
        return result["message"]["content"]