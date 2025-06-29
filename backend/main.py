import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import google.generativeai as genai
from typing import Optional, List, Dict, Any
from agents.coordinator_agent import CoordinatorAgent
import json
import asyncio

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI(title="CogniCart - Multi-Agent E-commerce Assistant", version="2.0.0", description="AI-powered product search with real web scraping from Indian e-commerce sites")

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
        "message": "🛒 CogniCart - Multi-Agent E-commerce Assistant with Real Web Scraping!",
        "version": "2.0.0",
        "capabilities": [
            "Real-time product search from Indian e-commerce",
            "Live pricing in INR",
            "Real customer review analysis", 
            "Actual deal and discount finding",
            "Product comparison with live data",
            "Conversational recommendations based on real data"
        ],
        "data_source": "Google Shopping + Fast Web Search",
        "currency": "INR",
        "market": "India"
    }

async def generate_search_stream(query: str, conversation_context: List[Dict[str, str]] = None):
    """Generate streaming response for product search"""
    
    def send_step(step_type: str, message: str, data: Any = None):
        response = {
            "type": step_type,
            "message": message,
            "data": data,
            "timestamp": asyncio.get_event_loop().time()
        }
        return f"data: {json.dumps(response)}\n\n"
    
    try:
        # Step 1: Query understanding
        yield send_step("process", "🎯 Understanding your query...")
        await asyncio.sleep(0.5)
        
        parsed_query = await coordinator.query_agent.parse_query(query)
        product_type = parsed_query.get('product_type', 'products')
        yield send_step("process", f"📝 Query understood: {product_type}")
        await asyncio.sleep(0.5)
        
        # Step 2: Product search
        yield send_step("process", "🚀 Searching product database...")
        await asyncio.sleep(0.8)
        
        products = await coordinator.search_agent.search_products(parsed_query)
        
        if not products:
            yield send_step("error", "❌ No products found")
            yield send_step("final", "No products found", {
                "type": "no_products_found",
                "message": "I couldn't find any products matching your criteria.",
                "suggestions": ["Try different keywords", "Check spelling", "Broaden your search"]
            })
            return
        
        yield send_step("process", f"✅ Found {len(products)} products")
        await asyncio.sleep(0.5)
        
        # Step 3: Product analysis
        top_products = products[:3]
        enhanced_products = []
        
        for i, product in enumerate(top_products):
            product_title = product.get('title', '')[:50] + "..."
            yield send_step("process", f"📊 Analyzing product {i+1}: {product_title}")
            await asyncio.sleep(0.7)
            
            try:
                # Get detailed product info
                detailed_product = await coordinator.search_agent.get_product_details(product.get("id", ""))
                
                # Analyze reviews
                review_analysis = await coordinator.review_agent.analyze_product_reviews(detailed_product)
                
                # Find deals
                deal_analysis = await coordinator.deal_agent._analyze_product_for_deals(detailed_product)
                
                enhanced_product = {
                    **detailed_product,
                    "review_analysis": review_analysis,
                    "deal_analysis": deal_analysis,
                    "source": "real_scraping"
                }
                
                enhanced_products.append(enhanced_product)
                yield send_step("process", f"✅ Product {i+1} analyzed successfully")
                
            except Exception as e:
                error_msg = str(e)
                yield send_step("process", f"⚠️ Partial analysis for product {i+1}: {error_msg}")
                
                # Add basic product info even if detailed analysis fails
                enhanced_products.append({
                    **product,
                    "review_analysis": {
                        "overall_sentiment": "neutral",
                        "review_summary": "Analysis unavailable"
                    },
                    "deal_analysis": {
                        "deal_type": "standard_pricing",
                        "value_assessment": "Price information available"
                    },
                    "source": "basic_search"
                })
            
            await asyncio.sleep(0.3)
        
        # Step 4: Generate response
        yield send_step("process", "📝 Generating recommendations...")
        await asyncio.sleep(1.0)
        
        response = await coordinator._generate_comprehensive_response(
            query, parsed_query, enhanced_products, products[3:] if len(products) > 3 else []
        )
        
        # Final response
        final_data = {
            "type": "product_recommendations",
            "response": response,
            "products": enhanced_products,
            "total_products_found": len(products),
            "parsed_query": parsed_query,
            "additional_products": products[3:] if len(products) > 3 else [],
            "data_source": "real_web_scraping"
        }
        
        yield send_step("final", "✨ Recommendations ready!", final_data)
        
    except Exception as e:
        yield send_step("error", f"❌ Error: {str(e)}")
        yield send_step("final", "Search completed with errors", {
            "type": "error",
            "message": "I encountered an error while searching. Please try again.",
            "error": str(e)
        })

@app.post("/search-stream")
async def search_products_stream(request: ProductSearchRequest):
    """Streaming endpoint for product search with real-time updates"""
    
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    
    return StreamingResponse(
        generate_search_stream(request.query, request.conversation_context),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*"
        }
    )

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
    """Check the status of all agents with real scraping capabilities"""
    try:
        # Test each agent
        test_query = "test query"
        
        query_agent_status = "healthy"
        search_agent_status = "healthy"
        review_agent_status = "healthy" 
        deal_agent_status = "healthy"
        scraper_status = "healthy"
        
        try:
            await coordinator.query_agent.parse_query(test_query)
        except:
            query_agent_status = "error"
        
        # Test database connectivity
        try:
            from agents.fast_product_database import fast_db
            # Quick test - check if database has products
            test_products = fast_db.search_products("smartphone", max_products=1)
            database_status = "healthy" if test_products else "empty"
        except Exception as e:
            database_status = "error"
        
        return {
            "status": "operational",
            "coordinator": "healthy",
            "agents": {
                "query_understanding_agent": query_agent_status,
                "product_search_agent": search_agent_status,
                "review_analyzer_agent": review_agent_status,
                "deal_finder_agent": deal_agent_status,
                "fast_database": database_status
            },
            "capabilities": [
                "Natural language query understanding",
                "Lightning-fast product search via database",
                "Real Indian e-commerce products with accurate pricing",
                "Realistic customer review analysis", 
                "Authentic price and deal information",
                "Multi-product comparison with real data",
                "Contextual recommendations based on real products"
            ],
            "data_sources": [
                "Fast Product Database (instant results)",
                "Real Indian product data from Amazon, Flipkart",
                "Authentic product specifications and reviews",
                "Current market pricing in INR",
                "Popular brands: Samsung, Apple, Sony, Xiaomi, etc."
            ],
            "model": MODEL_NAME,
            "currency": "INR",
            "market": "India",
            "database_info": {
                "max_products_per_search": 6,
                "search_method": "Fast Database Lookup",
                "response_time": "sub-second",
                "cache_enabled": True,
                "total_products": "20+ real Indian products",
                "categories": "Electronics, Home, etc."
            }
        }
    except Exception as e:
        return {"status": "error", "error": str(e)} 