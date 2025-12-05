import asyncio
import aiohttp


OLLAMA_URL = "http://ollama:11434/api/chat"


async def summarize(text: str, instruction: str) -> str:
    messages = [
        {
            'role': 'system',
            'content': "You\'re text summarizer, do **not** add explanations, greetings, or any other words."
            "You get json with field \"text\" - that text you need analyze, and field \"instruction\" - what you need to do with text."
            "The result have to be usual text, like main keyword of text, summarized sentence and etc, do **not** make lists and json of it"
        },
        {
            'role': 'user',
            'content': 
            "{"
            f"\'text\': {text}"
            f"\'instruction\': {instruction}"
            "}"
        }
    ]
    data = {
       "model": "gemma3",
       "messages": messages,
       "stream": False,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(OLLAMA_URL, json=data) as response:
            response.raise_for_status()
            result = await response.json()
            
            return result["message"]["content"]


async def main():
    with open("text.txt", encoding="utf-8") as f:
        text = f.read()
    
    tasks = [
        summarize(text, "Суммаризируй текст в одно предложение"),
        summarize(text, "Выдели 3 главных ключевых слова как список, разделённый запятыми"),
        summarize(text, "Переведи на английский язык"),
        summarize(text, "Сделай краткую выжимку этого текста в 3 предложениях")
    ]
    results = await asyncio.gather(*tasks)

    for res in results:
        print(res)


if __name__ == "__main__":
    asyncio.run(main())