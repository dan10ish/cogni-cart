from .base_agent import BaseAgent
from .query_understanding_agent import QueryUnderstandingAgent
from .product_search_agent import ProductSearchAgent
from .review_analyzer_agent import ReviewAnalyzerAgent
from .deal_finder_agent import DealFinderAgent
from typing import Dict, Any, List
import asyncio

class CoordinatorAgent(BaseAgent):
    """Main coordinator agent that orchestrates all other agents"""
    
    def __init__(self):
        super().__init__()
        self.query_agent = QueryUnderstandingAgent()
        self.search_agent = ProductSearchAgent()
        self.review_agent = ReviewAnalyzerAgent()
        self.deal_agent = DealFinderAgent()
        
    async def process_user_query(self, user_input: str, conversation_context: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Main entry point for processing user queries using real web scraping"""
        
        try:
            print(f"🎯 Processing query: {user_input}")
            
            # Step 1: Understand the query
            parsed_query = await self.query_agent.parse_query(user_input)
            print(f"📝 Query understood: {parsed_query.get('product_type', 'N/A')}")
            
            # Step 2: Search for products using real scraping
            products = await self.search_agent.search_products(parsed_query)
            
            if not products:
                print("❌ No products found")
                return {
                    "type": "no_products_found",
                    "message": "I couldn't find any products matching your criteria using real-time search. Let me suggest some alternatives.",
                    "suggestions": [
                        "Try different brand names (e.g., Samsung, Sony, Apple)",
                        "Use more general terms (e.g., 'vacuum' instead of specific model)",
                        "Check spelling and try again",
                        "Expand your budget range"
                    ],
                    "parsed_query": parsed_query
                }
            
            print(f"✅ Found {len(products)} real products")
            
            # Step 3: Analyze real reviews and deals for top products
            top_products = products[:3]  # Analyze top 3 products
            enhanced_products = []
            
            for i, product in enumerate(top_products):
                print(f"📊 Analyzing product {i+1}: {product.get('title', '')[:50]}...")
                
                try:
                    # Get detailed product info with real reviews
                    detailed_product = await self.search_agent.get_product_details(product.get("id", ""))
                    
                    # Analyze real reviews from scraped data
                    review_analysis = await self.review_agent.analyze_product_reviews(detailed_product)
                    
                    # Find real deal information
                    deal_analysis = await self.deal_agent._analyze_product_for_deals(detailed_product)
                    
                    enhanced_product = {
                        **detailed_product,
                        "review_analysis": review_analysis,
                        "deal_analysis": deal_analysis,
                        "source": "real_scraping"
                    }
                    
                    enhanced_products.append(enhanced_product)
                    
                except Exception as e:
                    print(f"⚠️ Error analyzing product {i+1}: {e}")
                    # Add basic product info even if detailed analysis fails
                    enhanced_products.append({
                        **product,
                        "review_analysis": {
                            "overall_sentiment": "neutral",
                            "review_summary": "Unable to analyze reviews at this time"
                        },
                        "deal_analysis": {
                            "deal_type": "standard_pricing",
                            "value_assessment": "Price information available"
                        },
                        "source": "real_scraping"
                    })
            
            # Step 4: Generate comprehensive response
            print(f"📝 Generating response with real data...")
            response = await self._generate_comprehensive_response(
                user_input, parsed_query, enhanced_products, products[3:] if len(products) > 3 else []
            )
            
            return {
                "type": "product_recommendations",
                "response": response,
                "products": enhanced_products,
                "total_products_found": len(products),
                "parsed_query": parsed_query,
                "additional_products": products[3:] if len(products) > 3 else [],
                "data_source": "real_web_scraping"
            }
            
        except Exception as e:
            print(f"❌ Error in coordinator: {e}")
            return {
                "type": "error",
                "message": "I encountered an error while searching for real products. This could be due to network issues or website changes. Please try again with simpler search terms.",
                "error": str(e),
                "suggestions": [
                    "Try simpler search terms",
                    "Check internet connection", 
                    "Wait a moment and try again",
                    "Use different product categories"
                ]
            }
    
    async def compare_products(self, product_ids: List[str], comparison_aspects: List[str] = None) -> Dict[str, Any]:
        """Compare multiple products across different aspects"""
        
        try:
            # Get detailed product information
            product_details = []
            for product_id in product_ids:
                details = await self.search_agent.get_product_details(product_id)
                if details:
                    product_details.append(details)
            
            if len(product_details) < 2:
                return {
                    "type": "error",
                    "message": "I need at least 2 products to make a comparison."
                }
            
            # Parallel analysis
            tasks = [
                self.review_agent.compare_review_sentiments(product_ids, comparison_aspects),
                self.deal_agent.compare_deals(product_ids)
            ]
            
            review_comparison, deal_comparison = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Generate comparison response
            comparison_response = await self._generate_comparison_response(
                product_details, review_comparison, deal_comparison, comparison_aspects
            )
            
            return {
                "type": "product_comparison",
                "response": comparison_response,
                "products": product_details,
                "review_analysis": review_comparison if not isinstance(review_comparison, Exception) else {},
                "deal_analysis": deal_comparison if not isinstance(deal_comparison, Exception) else {},
                "comparison_aspects": comparison_aspects
            }
            
        except Exception as e:
            return {
                "type": "error", 
                "message": "Error comparing products.",
                "error": str(e)
            }
    
    async def get_detailed_product_info(self, product_id: str, focus_areas: List[str] = None) -> Dict[str, Any]:
        """Get comprehensive information about a specific product"""
        
        try:
            # Parallel data gathering
            tasks = [
                self.search_agent.get_product_details(product_id),
                self.review_agent.analyze_reviews(product_id, focus_areas),
                self.deal_agent.find_deals(product_id)
            ]
            
            product_details, review_analysis, deals = await asyncio.gather(*tasks, return_exceptions=True)
            
            if not product_details or isinstance(product_details, Exception):
                return {
                    "type": "error",
                    "message": "Product not found."
                }
            
            # Generate detailed response
            detailed_response = await self._generate_detailed_product_response(
                product_details, review_analysis, deals, focus_areas
            )
            
            return {
                "type": "detailed_product_info",
                "response": detailed_response,
                "product": product_details,
                "review_analysis": review_analysis if not isinstance(review_analysis, Exception) else {},
                "deals": deals if not isinstance(deals, Exception) else [],
                "focus_areas": focus_areas
            }
            
        except Exception as e:
            return {
                "type": "error",
                "message": "Error getting product details.",
                "error": str(e)
            }
    
    async def _generate_comprehensive_response(self, user_input: str, parsed_query: Dict[str, Any], 
                                             products: List[Dict[str, Any]], additional_products: List[Dict[str, Any]]) -> str:
        """Generate a comprehensive response using AI"""
        
        prompt = f"""
You are an expert e-commerce assistant. Create a helpful, personalized response for the user.

User Query: "{user_input}"
Parsed Requirements: {parsed_query}

Top Product Recommendations: {products}
Additional Products Available: {len(additional_products)} more products

Create a conversational response that:
1. Acknowledges their specific requirements
2. Presents the top 3 recommendations with key highlights
3. Mentions deals and review insights
4. Offers to help with comparisons or more details
5. Keeps it friendly and helpful

Make it feel like talking to a knowledgeable friend, not a chatbot.
"""
        
        return await self.generate_response(prompt)
    
    async def _generate_comparison_response(self, products: List[Dict[str, Any]], 
                                         review_comparison: Dict[str, Any], deal_comparison: Dict[str, Any],
                                         comparison_aspects: List[str]) -> str:
        """Generate a product comparison response"""
        
        prompt = f"""
Create a helpful comparison between these products:

Products: {products}
Review Analysis: {review_comparison}
Deal Analysis: {deal_comparison}
Focus Areas: {comparison_aspects or 'general comparison'}

Provide a clear, structured comparison that helps the user decide. Include:
1. Quick summary of each product's strengths
2. Side-by-side comparison of key features
3. Review sentiment insights
4. Deal recommendations
5. Final recommendation based on different use cases

Keep it conversational and actionable.
"""
        
        return await self.generate_response(prompt)
    
    async def _generate_detailed_product_response(self, product: Dict[str, Any], 
                                                review_analysis: Dict[str, Any], deals: List[Dict[str, Any]],
                                                focus_areas: List[str]) -> str:
        """Generate detailed product information response"""
        
        prompt = f"""
Create a comprehensive product overview:

Product: {product}
Review Analysis: {review_analysis}
Available Deals: {deals}
Focus Areas: {focus_areas or 'general overview'}

Provide detailed information including:
1. Product overview and key features
2. Pros and cons based on reviews
3. Best use cases
4. Current deals and savings opportunities
5. Any concerns or limitations to be aware of

Make it thorough but easy to understand.
"""
        
        return await self.generate_response(prompt)
    
    async def handle_follow_up(self, follow_up_query: str, previous_context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle follow-up questions with context"""
        
        # Determine intent of follow-up
        intent_prompt = f"""
Analyze this follow-up query in context:

Follow-up: "{follow_up_query}"
Previous Context: {previous_context}

What is the user trying to do? Return JSON:
{{
    "intent": "compare_products/get_details/find_alternatives/clarify_requirements/ask_about_deals",
    "entities": ["extracted relevant entities"],
    "requires_new_search": true/false
}}
"""
        
        try:
            intent_analysis = await self.parse_json_response(intent_prompt)
            intent = intent_analysis.get("intent", "clarify_requirements")
            
            if intent == "compare_products":
                product_ids = intent_analysis.get("entities", [])
                if len(product_ids) >= 2:
                    return await self.compare_products(product_ids)
            
            elif intent == "get_details":
                product_ids = intent_analysis.get("entities", [])
                if product_ids:
                    return await self.get_detailed_product_info(product_ids[0])
            
            elif intent == "find_alternatives":
                # Use previous query data to find alternatives
                if "parsed_query" in previous_context:
                    return await self.process_user_query(follow_up_query)
            
            # Default: Generate contextual response
            response = await self.generate_response(
                f"User follow-up: {follow_up_query}\nPrevious context: {previous_context}\nProvide a helpful response."
            )
            
            return {
                "type": "follow_up_response",
                "response": response,
                "context": previous_context
            }
            
        except Exception as e:
            return {
                "type": "error",
                "message": "Could you please rephrase your question?",
                "error": str(e)
            } 