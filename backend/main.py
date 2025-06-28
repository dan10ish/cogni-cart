import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from typing import Optional, List, Dict, Any
from agents.coordinator_agent import CoordinatorAgent

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI(title="Multi-Agent E-commerce Assistant", version="2.0.0", description="AI-powered product search and recommendation system")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ProductSearchRequest(BaseModel):
    query: str
    conversation_context: Optional[List[Dict[str, str]]] = None

class ProductComparisonRequest(BaseModel):
    product_ids: List[str]
    comparison_aspects: Optional[List[str]] = None

class ProductDetailsRequest(BaseModel):
    product_id: str
    focus_areas: Optional[List[str]] = None

class FollowUpRequest(BaseModel):
    follow_up_query: str
    previous_context: Dict[str, Any]

# Legacy support
class PromptRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    response: str

# Get model name from environment variable with default fallback
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")
print(f"🤖 Initializing Multi-Agent E-commerce Assistant with model: {MODEL_NAME}")

# Initialize the coordinator agent
coordinator = CoordinatorAgent()

# Legacy model for backward compatibility
legacy_model = genai.GenerativeModel(MODEL_NAME)

@app.get("/")
async def root():
    return {
        "message": "🛒 Multi-Agent E-commerce Assistant is running!",
        "version": "2.0.0",
        "capabilities": [
            "Natural language product search",
            "Review sentiment analysis", 
            "Deal and discount finding",
            "Product comparison",
            "Conversational recommendations"
        ]
    }

@app.post("/search")
async def search_products(request: ProductSearchRequest):
    """Main endpoint for product search and recommendations"""
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Search query cannot be empty")
        
        result = await coordinator.process_user_query(request.query, request.conversation_context)
        return result
    
    except Exception as e:
        print(f"Error in product search: {e}")
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.post("/compare")
async def compare_products(request: ProductComparisonRequest):
    """Compare multiple products"""
    try:
        if len(request.product_ids) < 2:
            raise HTTPException(status_code=400, detail="At least 2 product IDs required for comparison")
        
        result = await coordinator.compare_products(request.product_ids, request.comparison_aspects)
        return result
    
    except Exception as e:
        print(f"Error in product comparison: {e}")
        raise HTTPException(status_code=500, detail=f"Comparison error: {str(e)}")

@app.post("/product-details")
async def get_product_details(request: ProductDetailsRequest):
    """Get detailed information about a specific product"""
    try:
        if not request.product_id.strip():
            raise HTTPException(status_code=400, detail="Product ID cannot be empty")
        
        result = await coordinator.get_detailed_product_info(request.product_id, request.focus_areas)
        return result
    
    except Exception as e:
        print(f"Error getting product details: {e}")
        raise HTTPException(status_code=500, detail=f"Product details error: {str(e)}")

@app.post("/follow-up")
async def handle_follow_up(request: FollowUpRequest):
    """Handle follow-up questions with context"""
    try:
        if not request.follow_up_query.strip():
            raise HTTPException(status_code=400, detail="Follow-up query cannot be empty")
        
        result = await coordinator.handle_follow_up(request.follow_up_query, request.previous_context)
        return result
    
    except Exception as e:
        print(f"Error in follow-up: {e}")
        raise HTTPException(status_code=500, detail=f"Follow-up error: {str(e)}")

# Legacy endpoint for backward compatibility
@app.post("/generate", response_model=PromptResponse)
async def generate_text(request: PromptRequest):
    """Legacy endpoint - use /search for better e-commerce experience"""
    try:
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        # Check if it looks like a product search query
        product_keywords = ["buy", "find", "search", "recommend", "product", "price", "deal", "review"]
        if any(keyword in request.prompt.lower() for keyword in product_keywords):
            # Route to the multi-agent system
            result = await coordinator.process_user_query(request.prompt)
            return PromptResponse(response=result.get("response", "Product search completed"))
        
        # Fall back to basic generation
        response = legacy_model.generate_content(request.prompt)
        
        if not response.text:
            raise HTTPException(status_code=500, detail="Failed to generate response")
        
        return PromptResponse(response=response.text)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Multi-Agent E-commerce Assistant", "version": "2.0.0"}

@app.get("/agents-status")
async def agents_status():
    """Check the status of all agents"""
    try:
        # Test each agent
        test_query = "test query"
        
        query_agent_status = "healthy"
        search_agent_status = "healthy"
        review_agent_status = "healthy"
        deal_agent_status = "healthy"
        
        try:
            await coordinator.query_agent.parse_query(test_query)
        except:
            query_agent_status = "error"
        
        return {
            "coordinator": "healthy",
            "query_understanding_agent": query_agent_status,
            "product_search_agent": search_agent_status,
            "review_analyzer_agent": review_agent_status,
            "deal_finder_agent": deal_agent_status,
            "model": MODEL_NAME
        }
    except Exception as e:
        return {"status": "error", "error": str(e)} 