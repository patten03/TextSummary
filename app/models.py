from pydantic import BaseModel
# from datetime import datetime

class SummarizeInput(BaseModel):
    original_text: str
    instruction: str

class Summaries(SummarizeInput):
    result: str

class HistoryItem(Summaries):
    created_at: int

class HistoryRecord(HistoryItem):
    id: str 
    
