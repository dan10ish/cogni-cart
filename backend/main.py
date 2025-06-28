import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from typing import Optional

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI(title="AI Chat Backend", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class PromptRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    response: str

# Get model name from environment variable with default fallback
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")
print(f"🤖 Initializing Gemini model: {MODEL_NAME}")

# Initialize the Gemini model
model = genai.GenerativeModel(MODEL_NAME)

@app.get("/")
async def root():
    return {"message": "AI Chat Backend is running!"}

@app.post("/generate", response_model=PromptResponse)
async def generate_text(request: PromptRequest):
    try:
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        # Generate content using Gemini
        response = model.generate_content(request.prompt)
        
        if not response.text:
            raise HTTPException(status_code=500, detail="Failed to generate response")
        
        return PromptResponse(response=response.text)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Chat Backend"} 