from .base_agent import BaseAgent
from typing import Dict, Any, List
import json

class ReviewAnalyzerAgent(BaseAgent):
    """Agent responsible for analyzing real product reviews from scraped data"""
    
    def __init__(self):
        super().__init__()
    
    async def analyze_product_reviews(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze reviews for a specific product using real scraped review data"""
        
        # Get real reviews from the product data
        reviews = product_data.get("reviews", [])
        
        if not reviews:
            return {
                "overall_sentiment": "neutral",
                "sentiment_breakdown": {"positive": 50, "neutral": 30, "negative": 20},
                "key_themes": [],
                "pros": [],
                "cons": [],
                "review_summary": "No reviews available for analysis",
                "red_flags": [],
                "recommendation_confidence": "low"
            }
        
        # Use AI to analyze the real reviews
        analysis = await self._analyze_reviews_with_ai(reviews, product_data)
        
        # Add review statistics
        analysis["review_statistics"] = self._calculate_review_stats(reviews)
        
        return analysis
    
    async def _analyze_reviews_with_ai(self, reviews: List[Dict[str, Any]], product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to analyze real customer reviews"""
        
        # Prepare review text for analysis
        review_texts = []
        for review in reviews:
            rating = review.get("rating", 0)
            title = review.get("title", "")
            text = review.get("text", "")
            verified = review.get("verified_purchase", False)
            
            review_summary = f"Rating: {rating}/5"
            if title:
                review_summary += f" | Title: {title}"
            if text:
                review_summary += f" | Review: {text[:300]}"
            if verified:
                review_summary += " | Verified Purchase"
            
            review_texts.append(review_summary)
        
        product_info = {
            "title": product_data.get("title", ""),
            "brand": product_data.get("brand", ""),
            "price": product_data.get("price", 0),
            "rating": product_data.get("rating", 0),
            "category": product_data.get("category", "")
        }
        
        prompt = f"""
You are an expert review analyzer for Indian e-commerce. Analyze these real customer reviews to provide actionable insights.

Product Information:
{json.dumps(product_info, indent=2)}

Real Customer Reviews:
{json.dumps(review_texts, indent=2)}

Provide analysis in JSON format with:
- "overall_sentiment": "positive", "neutral", or "negative"
- "sentiment_breakdown": {{"positive": X, "neutral": Y, "negative": Z}} (percentages that sum to 100)
- "key_themes": List of 4-5 main topics customers discuss
- "pros": List of 3-5 main advantages mentioned by customers
- "cons": List of 3-5 main disadvantages or complaints
- "review_summary": 2-3 sentence summary of overall customer sentiment
- "red_flags": List of serious issues that potential buyers should know about
- "recommendation_confidence": "high", "medium", or "low" based on review quality and consensus
- "value_for_money_sentiment": Customer perception of value for the price in INR
- "common_use_cases": How customers actually use this product based on reviews
"""
        
        try:
            analysis = await self.parse_json_response(prompt)
            return analysis if isinstance(analysis, dict) else {}
        except Exception as e:
            print(f"⚠️ Review analysis failed: {e}")
            return self._fallback_analysis(reviews)
    
    def _fallback_analysis(self, reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback analysis when AI fails"""
        
        # Simple sentiment analysis based on ratings
        positive_reviews = len([r for r in reviews if r.get("rating", 0) >= 4])
        negative_reviews = len([r for r in reviews if r.get("rating", 0) <= 2])
        neutral_reviews = len(reviews) - positive_reviews - negative_reviews
        
        total_reviews = len(reviews)
        
        if total_reviews == 0:
            sentiment_breakdown = {"positive": 50, "neutral": 30, "negative": 20}
        else:
            sentiment_breakdown = {
                "positive": round((positive_reviews / total_reviews) * 100),
                "neutral": round((neutral_reviews / total_reviews) * 100),
                "negative": round((negative_reviews / total_reviews) * 100)
            }
        
        overall_sentiment = "positive" if positive_reviews > negative_reviews else "negative" if negative_reviews > positive_reviews else "neutral"
        
        return {
            "overall_sentiment": overall_sentiment,
            "sentiment_breakdown": sentiment_breakdown,
            "key_themes": ["product quality", "value for money", "customer service"],
            "pros": ["Generally well-received by customers"],
            "cons": ["Some mixed feedback"],
            "review_summary": f"Based on {total_reviews} real customer reviews, the product shows {overall_sentiment} reception.",
            "red_flags": [],
            "recommendation_confidence": "medium",
            "value_for_money_sentiment": "neutral",
            "common_use_cases": ["General use as intended"]
        }
    
    def _calculate_review_stats(self, reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate basic review statistics"""
        
        if not reviews:
            return {
                "total_reviews": 0,
                "average_rating": 0,
                "rating_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                "verified_purchase_percentage": 0
            }
        
        total_reviews = len(reviews)
        total_rating = sum(r.get("rating", 0) for r in reviews)
        average_rating = total_rating / total_reviews if total_reviews > 0 else 0
        
        # Rating distribution
        rating_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        verified_count = 0
        
        for review in reviews:
            rating = review.get("rating", 0)
            if 1 <= rating <= 5:
                rating_dist[rating] += 1
            
            if review.get("verified_purchase", False):
                verified_count += 1
        
        verified_percentage = (verified_count / total_reviews) * 100 if total_reviews > 0 else 0
        
        return {
            "total_reviews": total_reviews,
            "average_rating": round(average_rating, 1),
            "rating_distribution": rating_dist,
            "verified_purchase_percentage": round(verified_percentage, 1)
        }
    
    async def compare_product_reviews(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare reviews across multiple products"""
        
        product_analyses = []
        
        for product in products:
            analysis = await self.analyze_product_reviews(product)
            product_analyses.append({
                "product_id": product.get("id", ""),
                "product_title": product.get("title", ""),
                "analysis": analysis
            })
        
        # AI-powered comparison of review patterns
        comparison = await self._compare_reviews_with_ai(product_analyses)
        
        return {
            "individual_analyses": product_analyses,
            "comparison": comparison
        }
    
    async def _compare_reviews_with_ai(self, product_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Use AI to compare review patterns across products"""
        
        prompt = f"""
Compare the review patterns and customer sentiment across these products based on real customer feedback.

Product Review Analyses:
{json.dumps(product_analyses, indent=2)}

Provide comparison in JSON format with:
- "summary": Overall comparison summary
- "sentiment_comparison": Which product has better overall customer satisfaction
- "strength_comparison": What each product excels at according to customers
- "weakness_comparison": What customers complain about for each product
- "recommendation": Which product based on real customer feedback and for what type of user
"""
        
        try:
            comparison = await self.parse_json_response(prompt)
            return comparison if isinstance(comparison, dict) else {}
        except Exception as e:
            print(f"⚠️ Review comparison failed: {e}")
            return {"error": "Unable to compare review patterns"}
    
    async def get_review_insights(self, query_data: Dict[str, Any], products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get review insights relevant to specific user query"""
        
        # Analyze reviews for all products
        insights = []
        
        for product in products:
            analysis = await self.analyze_product_reviews(product)
            insights.append({
                "product": {
                    "id": product.get("id", ""),
                    "title": product.get("title", ""),
                    "price": product.get("price", 0),
                    "rating": product.get("rating", 0)
                },
                "review_analysis": analysis
            })
        
        # Generate query-specific insights
        query_insights = await self._generate_query_specific_insights(query_data, insights)
        
        return {
            "product_insights": insights,
            "query_specific_insights": query_insights
        }
    
    async def _generate_query_specific_insights(self, query_data: Dict[str, Any], insights: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate insights specific to user query based on real reviews"""
        
        prompt = f"""
Based on real customer reviews and the user's specific requirements, provide targeted insights.

User Query Requirements:
{json.dumps(query_data, indent=2)}

Product Review Insights:
{json.dumps(insights, indent=2)}

Provide query-specific insights in JSON format with:
- "best_match_reasoning": Why certain products match the user's needs based on real customer feedback
- "potential_concerns": What real customers say about issues relevant to the user's requirements
- "user_type_recommendations": Recommendations based on similar customer profiles in reviews
- "price_value_insights": What customers say about value for money at these price points in INR
"""
        
        try:
            query_insights = await self.parse_json_response(prompt)
            return query_insights if isinstance(query_insights, dict) else {}
        except Exception as e:
            print(f"⚠️ Query-specific insights failed: {e}")
            return {"error": "Unable to generate query-specific insights"} 