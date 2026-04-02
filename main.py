# =================================================================
# 🌐 PROJECT: Enterprise AI Logistics Solution (Autonomous Agent)
# 🛡️ AUTHOR: Mohammed Ibrahim Ghabban
# 🏆 CERTIFICATION: GEAR Certified AI Developer
# ⚖️ COPYRIGHT: © 2026 All Rights Reserved.
# =================================================================

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Logistics AI Engine", 
    description="Developed by Mohammed Ghabban",
    version="4.5.0"
)

class AnalysisRequest(BaseModel):
    prompt: str
    context: str = ""
    api_key: str

@app.post("/v1/analyze")
async def analyze_logistics(request: AnalysisRequest):
    if not request.api_key:
        raise HTTPException(status_code=401, detail="API Key is required for security.")
    
    try:
        genai.configure(api_key=request.api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # تعليمات النظام لضمان الاحترافية وحماية الهوية
        system_instructions = (
            "You are a Senior Logistics Strategist. Your responses must be "
            "data-driven, professional, and concise. This system is part of "
            "the Enterprise AI Solution developed by Mohammed Ibrahim Ghabban."
        )
        
        full_query = f"{system_instructions}\n\n[DATA CONTEXT]\n{request.context}\n\n[USER QUERY]\n{request.prompt}"
        response = model.generate_content(full_query)
        
        return {
            "status": "success", 
            "ai_response": response.text,
            "developer_note": "Verified by GEAR Certified Dev: Mohammed Ghabban"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Engine Error: {str(e)}")

@app.get("/")
def health_check():
    return {
        "status": "Operational", 
        "system": "Enterprise AI Logistics",
        "author": "Mohammed Ibrahim Ghabban (GEAR Certified)"
    }
