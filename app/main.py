import ollama_llm
import aiohttp
import uvicorn
import database
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import models
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_session = aiohttp.ClientSession()
    app.state.pool = await database.init_db()

    yield

    app.state.http_session.close()
    database.close_db(app.state.pool)

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="main.html"
    )

@app.get("/historyPage", response_class=HTMLResponse)
async def historyPage(request: Request):
    return templates.TemplateResponse(
        request=request, name="history.html"
    )

@app.post("/summarize")
async def summarize(summarizeInput: models.SummarizeInput):
    result = await ollama_llm.summarize(app.state.http_session, summarizeInput)

    summary = models.Summaries(
        original_text=summarizeInput.original_text,
        instruction=summarizeInput.instruction,
        result=result
    )
    
    await database.save_to_history(app.state.pool, summary)
    return {"result": result}



@app.get("/history")
async def history():
    history = await database.get_history(app.state.pool)
    return history


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)