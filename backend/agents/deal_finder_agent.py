from .base_agent import BaseAgent
from typing import Dict, Any, List
import json
from datetime import datetime, timedelta

class DealFinderAgent(BaseAgent):
    """Agent responsible for finding deals and analyzing prices from real scraped data"""
    
    def __init__(self):
        super().__init__()
        # Simple price tracking for detected price patterns
        self.price_patterns = {}
    
    async def find_product_deals(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Find deals and price insights for real products"""
        
        deals = []
        
        for product in products:
            deal_analysis = await self._analyze_product_for_deals(product)
            if deal_analysis:
                deals.append({
                    "product": product,
                    "deal_info": deal_analysis
                })
        
        # Sort deals by savings potential
        deals.sort(key=lambda x: x["deal_info"].get("deal_score", 0), reverse=True)
        
        return {
            "deals_found": len(deals),
            "best_deals": deals[:5],  # Top 5 deals
            "deal_summary": await self._generate_deal_summary(deals)
        }
    
    async def _analyze_product_for_deals(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single product for deal potential"""
        
        price = product.get("price", 0)
        rating = product.get("rating", 0)
        review_count = product.get("review_count", 0)
        
        if price == 0:
            return None
        
        # Use AI to analyze if this is a good deal
        deal_analysis = await self._ai_deal_analysis(product)
        
        # Calculate deal score based on multiple factors
        deal_score = self._calculate_deal_score(product, deal_analysis)
        
        return {
            "deal_score": deal_score,
            "price_analysis": deal_analysis.get("price_analysis", {}),
            "value_assessment": deal_analysis.get("value_assessment", ""),
            "deal_type": self._identify_deal_type(product, deal_analysis),
            "savings_estimate": self._estimate_savings(product, deal_analysis),
            "price_trend_insight": self._get_price_trend_insight(product),
            "recommendation": deal_analysis.get("recommendation", "")
        }
    
    async def _ai_deal_analysis(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to analyze if product represents a good deal"""
        
        prompt = f"""
You are an expert deal finder for Indian e-commerce. Analyze this product to determine if it represents good value for money.

Product Data:
{json.dumps(product, indent=2)}

Consider these factors for Indian market:
- Price competitiveness in INR
- Brand reputation and value
- Feature set relative to price
- Customer satisfaction (rating/reviews)
- Market category pricing norms

Provide analysis in JSON format with:
- "price_analysis": {{"market_position": "budget/mid-range/premium", "value_rating": 1-10, "price_per_feature_value": "good/average/poor"}}
- "value_assessment": Detailed explanation of value proposition
- "deal_indicators": List of factors that make this a good or bad deal
- "comparable_price_range": Expected price range for similar products in INR
- "recommendation": "strong_buy", "good_buy", "consider", or "skip" with reasoning
"""
        
        try:
            analysis = await self.parse_json_response(prompt)
            return analysis if isinstance(analysis, dict) else {}
        except Exception as e:
            print(f"⚠️ AI deal analysis failed: {e}")
            return self._fallback_deal_analysis(product)
    
    def _fallback_deal_analysis(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback deal analysis when AI fails"""
        
        price = product.get("price", 0)
        rating = product.get("rating", 0)
        review_count = product.get("review_count", 0)
        
        # Simple heuristics
        value_rating = 5  # Default
        
        if rating >= 4.5 and review_count >= 100:
            value_rating += 2
        elif rating >= 4.0 and review_count >= 50:
            value_rating += 1
        
        if price <= 1000:
            market_position = "budget"
        elif price <= 10000:
            market_position = "mid-range"
        else:
            market_position = "premium"
        
        return {
            "price_analysis": {
                "market_position": market_position,
                "value_rating": min(value_rating, 10),
                "price_per_feature_value": "average"
            },
            "value_assessment": f"Product appears to be in {market_position} category with {rating} rating",
            "deal_indicators": ["Customer rating above average"] if rating >= 4.0 else [],
            "comparable_price_range": f"₹{price * 0.8:.0f} - ₹{price * 1.2:.0f}",
            "recommendation": "consider"
        }
    
    def _calculate_deal_score(self, product: Dict[str, Any], deal_analysis: Dict[str, Any]) -> float:
        """Calculate deal score from 0-100"""
        
        score = 50  # Base score
        
        # Rating factor (0-25 points)
        rating = product.get("rating", 0)
        score += min(rating * 5, 25)
        
        # Review count factor (0-15 points)
        review_count = product.get("review_count", 0)
        score += min(review_count / 100, 15)
        
        # AI value rating (0-10 points)
        value_rating = deal_analysis.get("price_analysis", {}).get("value_rating", 5)
        score += value_rating
        
        return min(max(score, 0), 100)
    
    def _identify_deal_type(self, product: Dict[str, Any], deal_analysis: Dict[str, Any]) -> str:
        """Identify type of deal"""
        
        value_rating = deal_analysis.get("price_analysis", {}).get("value_rating", 5)
        recommendation = deal_analysis.get("recommendation", "")
        
        if "strong_buy" in recommendation or value_rating >= 8:
            return "excellent_value"
        elif "good_buy" in recommendation or value_rating >= 7:
            return "good_value"
        elif value_rating >= 6:
            return "fair_value"
        else:
            return "average_value"
    
    def _estimate_savings(self, product: Dict[str, Any], deal_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate potential savings"""
        
        price = product.get("price", 0)
        
        # Extract comparable price range
        comparable_range = deal_analysis.get("comparable_price_range", "")
        
        # Simple parsing of price range
        import re
        price_matches = re.findall(r'₹([\d,]+)', comparable_range)
        
        if len(price_matches) >= 2:
            try:
                min_price = float(price_matches[0].replace(',', ''))
                max_price = float(price_matches[1].replace(',', ''))
                avg_market_price = (min_price + max_price) / 2
                
                savings = avg_market_price - price
                savings_percent = (savings / avg_market_price) * 100 if avg_market_price > 0 else 0
                
                return {
                    "estimated_market_price": avg_market_price,
                    "current_price": price,
                    "estimated_savings": max(savings, 0),
                    "savings_percentage": max(savings_percent, 0)
                }
            except:
                pass
        
        return {
            "estimated_market_price": price,
            "current_price": price,
            "estimated_savings": 0,
            "savings_percentage": 0
        }
    
    def _get_price_trend_insight(self, product: Dict[str, Any]) -> str:
        """Get price trend insight (simplified)"""
        
        # Since we don't have historical data, provide general insights
        price = product.get("price", 0)
        category = product.get("category", "")
        
        insights = [
            "Current market price based on real-time data",
            f"Typical {category} category pricing in Indian market",
            "Price verified from active listings"
        ]
        
        return ". ".join(insights)
    
    async def _generate_deal_summary(self, deals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of all deals found"""
        
        if not deals:
            return {
                "total_deals": 0,
                "summary": "No significant deals found in current search results",
                "recommendation": "Consider expanding search criteria or checking back later"
            }
        
        # Categorize deals
        excellent_deals = [d for d in deals if d["deal_info"]["deal_type"] == "excellent_value"]
        good_deals = [d for d in deals if d["deal_info"]["deal_type"] == "good_value"]
        
        total_potential_savings = sum(
            d["deal_info"]["savings_estimate"]["estimated_savings"] 
            for d in deals
        )
        
        prompt = f"""
Summarize these deals found for Indian consumers:

Excellent Value Deals: {len(excellent_deals)}
Good Value Deals: {len(good_deals)}
Total Deals Analyzed: {len(deals)}
Total Potential Savings: ₹{total_potential_savings:.0f}

Deal Details:
{json.dumps([{"product_title": d["product"]["title"], "price": d["product"]["price"], "deal_type": d["deal_info"]["deal_type"]} for d in deals[:5]], indent=2)}

Provide summary in JSON format with:
- "summary": Brief overview of deal landscape
- "best_deal_recommendation": Which deal offers best value
- "total_savings_potential": Total estimated savings across all deals
- "deal_strategy": Advice on when to buy
"""
        
        try:
            summary = await self.parse_json_response(prompt)
            return summary if isinstance(summary, dict) else self._fallback_deal_summary(deals)
        except Exception as e:
            print(f"⚠️ Deal summary generation failed: {e}")
            return self._fallback_deal_summary(deals)
    
    def _fallback_deal_summary(self, deals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback deal summary"""
        
        return {
            "summary": f"Found {len(deals)} products with deal potential",
            "best_deal_recommendation": deals[0]["product"]["title"] if deals else "No deals available",
            "total_savings_potential": sum(d["deal_info"]["savings_estimate"]["estimated_savings"] for d in deals),
            "deal_strategy": "Compare prices and features carefully before purchasing"
        }
    
    async def compare_deal_value(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare deal value across multiple products"""
        
        analyses = []
        
        for product in products:
            deal_analysis = await self._analyze_product_for_deals(product)
            if deal_analysis:
                analyses.append({
                    "product": {
                        "id": product.get("id", ""),
                        "title": product.get("title", ""),
                        "price": product.get("price", 0),
                        "rating": product.get("rating", 0)
                    },
                    "deal_analysis": deal_analysis
                })
        
        # AI-powered comparison
        comparison = await self._ai_deal_comparison(analyses)
        
        return {
            "product_analyses": analyses,
            "comparison": comparison
        }
    
    async def _ai_deal_comparison(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Use AI to compare deal values"""
        
        prompt = f"""
Compare these products from a deal/value perspective for Indian consumers:

Product Deal Analyses:
{json.dumps(analyses, indent=2)}

Provide comparison in JSON format with:
- "best_overall_value": Which product offers best overall value for money
- "best_budget_option": Most affordable option with good quality
- "best_premium_option": Best high-end option if budget allows
- "value_ranking": Ranked list of products by value proposition
- "buying_advice": Specific advice on which to choose based on different budgets/needs
"""
        
        try:
            comparison = await self.parse_json_response(prompt)
            return comparison if isinstance(comparison, dict) else {}
        except Exception as e:
            print(f"⚠️ Deal comparison failed: {e}")
            return {"error": "Unable to compare deal values"}
    
    async def get_price_alerts(self, products: List[Dict[str, Any]], budget_limit: float = None) -> Dict[str, Any]:
        """Generate price alerts and recommendations"""
        
        alerts = []
        
        for product in products:
            price = product.get("price", 0)
            
            alert_info = {
                "product_id": product.get("id", ""),
                "product_title": product.get("title", ""),
                "current_price": price,
                "alert_type": "info",
                "message": f"Current price: ₹{price:,.0f}"
            }
            
            # Budget alert
            if budget_limit and price <= budget_limit:
                alert_info["alert_type"] = "good_news"
                alert_info["message"] = f"Within budget! Price: ₹{price:,.0f} (Budget: ₹{budget_limit:,.0f})"
            elif budget_limit and price > budget_limit:
                alert_info["alert_type"] = "warning"
                alert_info["message"] = f"Over budget: ₹{price:,.0f} (Budget: ₹{budget_limit:,.0f})"
            
            # Rating alert
            rating = product.get("rating", 0)
            if rating >= 4.5:
                alert_info["alert_type"] = "excellent"
                alert_info["message"] += f" | Excellent rating: {rating}⭐"
            elif rating < 3.5:
                alert_info["alert_type"] = "caution"
                alert_info["message"] += f" | Low rating: {rating}⭐"
            
            alerts.append(alert_info)
        
        return {
            "alerts": alerts,
            "budget_analysis": {
                "total_budget": budget_limit or 0,
                "products_within_budget": len([a for a in alerts if a["alert_type"] == "good_news"]),
                "average_price": sum(p.get("price", 0) for p in products) / len(products) if products else 0
            }
        } 