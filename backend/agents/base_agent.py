import os
import google.generativeai as genai
from typing import Dict, Any, Optional
import json

class BaseAgent:
    """Base class for all e-commerce agents"""
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or os.getenv("MODEL_NAME", "gemini-1.5-flash")
        self.model = genai.GenerativeModel(self.model_name)
        
    async def generate_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate AI response with optional context"""
        try:
            if context:
                full_prompt = f"Context: {json.dumps(context, indent=2)}\n\nTask: {prompt}"
            else:
                full_prompt = prompt
                
            response = self.model.generate_content(full_prompt)
            return response.text if response.text else ""
        except Exception as e:
            print(f"Error generating response: {e}")
            return ""
    
    async def parse_json_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate and parse JSON response"""
        try:
            json_prompt = f"{prompt}\n\nIMPORTANT: Respond ONLY with valid JSON. No additional text."
            response = await self.generate_response(json_prompt, context)
            
            # Clean response to extract JSON
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            return json.loads(response)
        except Exception as e:
            print(f"Error parsing JSON response: {e}")
            return {} 