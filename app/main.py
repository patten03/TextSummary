import ollama_model
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


class SummarizeInput(BaseModel):
    text: str
    instruction: str

app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
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
async def summarize(summarizeInput: SummarizeInput):
    result = await ollama_model.summarize(summarizeInput.text, summarizeInput.instruction)
    return {"result": result}



@app.get("/history")
async def history():
    history = [
        {
            "text": "Global temperatures have risen by approximately 1.1°C since the pre-industrial era, primarily due to human activities such as burning fossil fuels and deforestation. The Intergovernmental Panel on Climate Change (IPCC) warns that exceeding 1.5°C of warming will significantly increase the risk of severe weather events, sea-level rise, and irreversible damage to ecosystems. Countries around the world committed under the Paris Agreement to limit warming to well below 2°C, preferably 1.5°C, through nationally determined contributions (NDCs).",
            "instruction": "Summarize this article in 2-3 sentences, focusing on the key facts and the urgency of the situation.",
            "result": "Global temperatures have already increased by 1.1°C due to human activities like burning fossil fuels and deforestation. The IPCC warns that surpassing 1.5°C warming will trigger severe and potentially irreversible climate impacts. The Paris Agreement aims to keep warming well below 2°C, ideally at 1.5°C.",
            "timestamp": 1763193423
        },
        {
            "text": "Researchers at Stanford University have developed a new lithium-metal battery that can achieve 600 charge cycles while retaining 80% of its original capacity. Traditional lithium-ion batteries typically degrade much faster when using lithium-metal anodes because of dendrite formation. The new design uses a novel electrolyte and a protective layer that prevents dendrites from piercing the separator, dramatically improving both safety and lifespan.",
            "instruction": "Provide a concise summary (1-2 sentences) highlighting the main breakthrough and its benefits.",
            "result": "Stanford researchers created a lithium-metal battery that lasts 600 cycles with 80% capacity retention by using a special electrolyte and protective layer that stop dendrite growth. This breakthrough significantly improves both the lifespan and safety compared to conventional lithium-ion batteries.",
            "timestamp": 1793813425
        },
        {
            "text": "The European Union announced yesterday that it will ban the sale of new gasoline and diesel cars starting in 2035 as part of its Green Deal initiative. Hybrid vehicles will also be phased out under the new regulation. Carmakers must transition entirely to electric or hydrogen vehicles to meet the bloc’s goal of climate neutrality by 2050. Several member states had pushed for exceptions, but the final agreement includes no loopholes for combustion engines.",
            "instruction": "Summarize in one sentence.",
            "result": "The EU will completely ban the sale of new gasoline, diesel, and hybrid cars from 2035 to achieve climate neutrality by 2050.",
            "timestamp": 1793803520
        },
        {
            "text": "A new study published in Nature Medicine found that regular consumption of olive oil is associated with a 20-30% lower risk of cardiovascular disease and all-cause mortality. The research followed over 90,000 participants for 28 years and showed the strongest benefits when olive oil replaced margarine, butter, or mayonnaise in the diet. Even modest amounts (half a tablespoon per day) showed protective effects.",
            "instruction": "Summarize the key findings in 2 sentences suitable for a health newsletter.",
            "result": "A 28-year study of over 90,000 people found that regular olive oil consumption reduces the risk of cardiovascular disease and overall mortality by 20-30%. Replacing butter, margarine, or mayonnaise with olive oil—even just half a tablespoon daily—provides significant protective benefits.",
            "timestamp": 1793111425
        },
        {
            "text": "OpenAI released GPT-4o, its latest flagship model, which processes and generates text, vision, and audio in real time. The 'o' stands for 'omni'. During the live demo, the model solved complex math problems, translated languages instantly, and even recognized and described emotions from a person’s facial expression through a phone camera. It is now available to all ChatGPT Plus users and will roll out to free users with usage limits.",
            "instruction": "Write a short summary (3 sentences max) for a tech news site.",
            "result": "OpenAI launched GPT-4o ('omni'), a multimodal model that handles text, images, and audio natively with real-time performance. In demos, it solved advanced math problems, performed instant translation, and even detected emotions from live video. The model is immediately available to ChatGPT Plus subscribers and will gradually reach free users.",
            "timestamp": 1793809825
        },
        {
            "text": "Global temperatures have risen by approximately 1.1°C since the pre-industrial era, primarily due to human activities such as burning fossil fuels and deforestation. The Intergovernmental Panel on Climate Change (IPCC) warns that exceeding 1.5°C of warming will significantly increase the risk of severe weather events, sea-level rise, and irreversible damage to ecosystems. Countries around the world committed under the Paris Agreement to limit warming to well below 2°C, preferably 1.5°C, through nationally determined contributions (NDCs).",
            "instruction": "Summarize this article in 2-3 sentences, focusing on the key facts and the urgency of the situation.",
            "result": "Global temperatures have already increased by 1.1°C due to human activities like burning fossil fuels and deforestation. The IPCC warns that surpassing 1.5°C warming will trigger severe and potentially irreversible climate impacts. The Paris Agreement aims to keep warming well below 2°C, ideally at 1.5°C.",
            "timestamp": 1763893425
        },
        {
            "text": "Researchers at Stanford University have developed a new lithium-metal battery that can achieve 600 charge cycles while retaining 80% of its original capacity. Traditional lithium-ion batteries typically degrade much faster when using lithium-metal anodes because of dendrite formation. The new design uses a novel electrolyte and a protective layer that prevents dendrites from piercing the separator, dramatically improving both safety and lifespan.",
            "instruction": "Provide a concise summary (1-2 sentences) highlighting the main breakthrough and its benefits.",
            "result": "Stanford researchers created a lithium-metal battery that lasts 600 cycles with 80% capacity retention by using a special electrolyte and protective layer that stop dendrite growth. This breakthrough significantly improves both the lifespan and safety compared to conventional lithium-ion batteries.",
            "timestamp": 1793813425
        },
        {
            "text": "The European Union announced yesterday that it will ban the sale of new gasoline and diesel cars starting in 2035 as part of its Green Deal initiative. Hybrid vehicles will also be phased out under the new regulation. Carmakers must transition entirely to electric or hydrogen vehicles to meet the bloc’s goal of climate neutrality by 2050. Several member states had pushed for exceptions, but the final agreement includes no loopholes for combustion engines.",
            "instruction": "Summarize in one sentence.",
            "result": "The EU will completely ban the sale of new gasoline, diesel, and hybrid cars from 2035 to achieve climate neutrality by 2050.",
            "timestamp": 1793803520
        },
        {
            "text": "A new study published in Nature Medicine found that regular consumption of olive oil is associated with a 20-30% lower risk of cardiovascular disease and all-cause mortality. The research followed over 90,000 participants for 28 years and showed the strongest benefits when olive oil replaced margarine, butter, or mayonnaise in the diet. Even modest amounts (half a tablespoon per day) showed protective effects.",
            "instruction": "Summarize the key findings in 2 sentences suitable for a health newsletter.",
            "result": "A 28-year study of over 90,000 people found that regular olive oil consumption reduces the risk of cardiovascular disease and overall mortality by 20-30%. Replacing butter, margarine, or mayonnaise with olive oil—even just half a tablespoon daily—provides significant protective benefits.",
            "timestamp": 1793111425
        },
        {
            "text": "OpenAI released GPT-4o, its latest flagship model, which processes and generates text, vision, and audio in real time. The 'o' stands for 'omni'. During the live demo, the model solved complex math problems, translated languages instantly, and even recognized and described emotions from a person’s facial expression through a phone camera. It is now available to all ChatGPT Plus users and will roll out to free users with usage limits.",
            "instruction": "Write a short summary (3 sentences max) for a tech news site.",
            "result": "OpenAI launched GPT-4o ('omni'), a multimodal model that handles text, images, and audio natively with real-time performance. In demos, it solved advanced math problems, performed instant translation, and even detected emotions from live video. The model is immediately available to ChatGPT Plus subscribers and will gradually reach free users.",
            "timestamp": 1793809825
        }
    ]

    return history


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)