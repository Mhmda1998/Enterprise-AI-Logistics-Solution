import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Logistics AI Engine", version="4.1.0")

class AnalysisRequest(BaseModel):
    prompt: str
    context: str = ""
    api_key: str

@app.post("/v1/analyze")
async def analyze_logistics(request: AnalysisRequest):
    if not request.api_key:
        raise HTTPException(status_code=401, detail="Missing Gemini API Key")
    
    try:
        genai.configure(api_key=request.api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        instructions = "You are a Senior Logistics Strategist. Analyze the following data and provide expert operational recommendations."
        full_query = f"{instructions}\n\n[CONTEXT DATA]\n{request.context}\n\n[USER QUERY]\n{request.prompt}"
        
        response = model.generate_content(full_query)
        return {"status": "success", "ai_response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "Operational", "developer": "Mohammed Ghabban"}
