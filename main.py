import os
import google.generativeai as genai
from fastapi import FastAPI, Security, HTTPException, status, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel

# 1. إعداد واجهة التطبيق (FastAPI)
app = FastAPI(title="Global AI Logistics API", version="2.0.0")

# 2. إعداد مفتاح Gemini (سيتم جلبه من إعدادات السيرفر لاحقاً للأمان)
# استبدل 'YOUR_API_KEY' بمفتاحك الخاص للتجربة
GENAI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

# 3. نظام الأمان: مفاتيح الشركات العالمية (API Keys)
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# قاعدة بيانات تجريبية للمفاتيح المباعة للشركات
TRUSTED_CLIENTS = {
    "DHL-GLOBAL-2026": "DHL International",
    "AMAZON-LOG-XYZ": "Amazon Logistics",
    "FEDEX-CORP-AGENT": "FedEx Global"
}

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key in TRUSTED_CLIENTS:
        return TRUSTED_CLIENTS[api_key]
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Unauthorized: Invalid API Key. Contact Mohammed (GEAR Certified)."
    )

# 4. نموذج طلب العميل (Data Schema)
class ShipmentQuery(BaseModel):
    text_query: str
    language: str = "en"

# 5. نقطة النهاية (Endpoint): معالجة تتبع الشحنات بالذكاء الاصطناعي
@app.post("/v1/track")
async def track_shipment(request: ShipmentQuery, client_name: str = Depends(verify_api_key)):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # تعليمات النظام لـ Gemini (System Instruction)
        prompt = f"""
        You are a Senior Logistics Expert for {client_name}.
        Answer the following customer query professionally: {request.text_query}
        Language: {request.language}
        If a tracking ID is missing, ask for it politely.
        """
        
        response = model.generate_content(prompt)
        
        return {
            "client": client_name,
            "status": "success",
            "ai_response": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Engine Error: {str(e)}")

# لتشغيل السيرفر محلياً: uvicorn main:app --reload
