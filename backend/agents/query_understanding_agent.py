from .base_agent import BaseAgent
from typing import Dict, Any, List
import asyncio

class QueryUnderstandingAgent(BaseAgent):
    """Agent responsible for understanding and parsing user queries"""
    
    def __init__(self):
        super().__init__()
        
    async def parse_query(self, user_query: str) -> Dict[str, Any]:
        """Parse natural language query into structured data"""
        
        prompt = f"""
You are an expert at understanding e-commerce search queries. Parse the following user query into structured data.

User Query: "{user_query}"

Extract the following information and return as JSON:
{{
    "product_category": "main category (e.g., electronics, clothing, home)",
    "product_type": "specific product type (e.g., laptop, vacuum cleaner, headphones)",
    "features_required": ["list of required features mentioned"],
    "budget": {{
        "min": number or null,
        "max": number or null,
        "currency": "USD" or detected currency
    }},
    "brand_preferences": ["preferred brands mentioned"],
    "size_requirements": "size specifications if any",
    "color_preferences": ["color preferences"],
    "use_case": "intended use or scenario",
    "priority_features": ["most important features ranked by importance"],
    "deal_preferences": {{
        "wants_deals": true/false,
        "deal_types": ["discount", "coupon", "bundle", "free_shipping"]
    }},
    "urgency": "immediate/soon/flexible",
    "sentiment": "positive/neutral/negative",
    "comparison_intent": true/false
}}

Be thorough but only include information that's actually mentioned or strongly implied.
"""
        
        return await self.parse_json_response(prompt)
    
    async def refine_query(self, original_query: str, parsed_data: Dict[str, Any], clarification: str) -> Dict[str, Any]:
        """Refine the parsed query based on user clarification"""
        
        prompt = f"""
The user provided this clarification: "{clarification}"

Update the parsed query data based on this new information.

Original Query: "{original_query}"
Current Parsed Data: {parsed_data}
User Clarification: "{clarification}"

Return the updated JSON structure with the same format as before.
"""
        
        return await self.parse_json_response(prompt)
    
    async def suggest_clarifications(self, parsed_data: Dict[str, Any]) -> List[str]:
        """Suggest clarifying questions based on parsed data"""
        
        prompt = f"""
Based on this parsed query data, suggest 2-3 clarifying questions that would help find better products.

Parsed Data: {parsed_data}

Focus on missing important information like:
- Budget if not specified
- Specific use cases
- Important features not mentioned
- Size/compatibility requirements

Return as JSON array of strings:
["question1", "question2", "question3"]
"""
        
        try:
            response = await self.parse_json_response(prompt)
            if isinstance(response, list):
                return response
            return response.get("questions", [])
        except:
            return [] 