from .base_agent import BaseAgent
from typing import Dict, Any, List
import random
from datetime import datetime, timedelta

class DealFinderAgent(BaseAgent):
    """Agent responsible for finding deals, discounts, and coupons"""
    
    def __init__(self):
        super().__init__()
        self.mock_deals = self._load_mock_deals()
        
    def _load_mock_deals(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load mock deal data for demonstration"""
        return {
            "vac001": [
                {
                    "id": "deal001",
                    "type": "discount",
                    "title": "20% Off Shark Navigator",
                    "description": "Limited time discount on Shark Navigator vacuum cleaners",
                    "discount_percentage": 20,
                    "original_price": 179.99,
                    "sale_price": 143.99,
                    "savings": 36.00,
                    "coupon_code": None,
                    "valid_until": "2024-02-15",
                    "retailer": "Amazon",
                    "availability": "limited_stock",
                    "terms": "While supplies last"
                },
                {
                    "id": "deal002", 
                    "type": "coupon",
                    "title": "$25 Off with Coupon",
                    "description": "Apply coupon code for $25 off",
                    "discount_amount": 25.00,
                    "original_price": 179.99,
                    "sale_price": 154.99,
                    "savings": 25.00,
                    "coupon_code": "CLEAN25",
                    "valid_until": "2024-02-28",
                    "retailer": "Target",
                    "availability": "in_stock"
                }
            ],
            "vac002": [
                {
                    "id": "deal003",
                    "type": "bundle",
                    "title": "Dyson V15 + Extra Tools Bundle",
                    "description": "Get free extra cleaning tools worth $150",
                    "bundle_value": 150.00,
                    "original_price": 749.99,
                    "sale_price": 749.99,
                    "savings": 150.00,
                    "valid_until": "2024-02-20",
                    "retailer": "Best Buy",
                    "availability": "in_stock",
                    "bundle_items": ["Pet hair tool", "Crevice tool", "Extension wand"]
                }
            ],
            "lap001": [
                {
                    "id": "deal004",
                    "type": "student_discount",
                    "title": "Student Discount - MacBook Air M2",
                    "description": "Educational pricing for students and teachers",
                    "discount_percentage": 10,
                    "original_price": 1199.99,
                    "sale_price": 1079.99,
                    "savings": 120.00,
                    "valid_until": "2024-12-31",
                    "retailer": "Apple",
                    "availability": "in_stock",
                    "eligibility": "Students, teachers, and staff"
                },
                {
                    "id": "deal005",
                    "type": "trade_in",
                    "title": "Trade-in Your Old Laptop",
                    "description": "Get up to $500 trade-in credit",
                    "trade_in_value": 500.00,
                    "original_price": 1199.99,
                    "effective_price": 699.99,
                    "savings": 500.00,
                    "retailer": "Apple",
                    "availability": "in_stock",
                    "terms": "Value depends on condition and model"
                }
            ]
        }
    
    async def find_deals(self, product_id: str, deal_preferences: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Find available deals for a specific product"""
        
        deals = self.mock_deals.get(product_id, [])
        if not deals:
            return []
        
        # Filter deals based on preferences
        if deal_preferences:
            preferred_types = deal_preferences.get("deal_types", [])
            if preferred_types:
                deals = [deal for deal in deals if deal["type"] in preferred_types]
        
        # Sort deals by savings amount
        deals.sort(key=lambda x: x.get("savings", 0), reverse=True)
        
        return deals
    
    async def compare_deals(self, product_ids: List[str]) -> Dict[str, Any]:
        """Compare deals across multiple products"""
        
        all_deals = {}
        for product_id in product_ids:
            deals = await self.find_deals(product_id)
            if deals:
                all_deals[product_id] = deals
        
        if not all_deals:
            return {"message": "No deals found for the selected products"}
        
        prompt = f"""
Analyze and compare these deals across products to help the user make the best decision.

Product Deals: {all_deals}

Provide comparison in JSON format:
{{
    "best_overall_deal": {{
        "product_id": "product with best deal",
        "deal_id": "specific deal id", 
        "reason": "why this is the best deal"
    }},
    "biggest_savings": {{
        "product_id": "product_id",
        "deal_id": "deal_id",
        "savings_amount": number
    }},
    "deal_recommendations": {{
        "budget_conscious": "product_id with best value",
        "premium_buyer": "product_id with best premium deal",
        "student": "product_id with student-friendly deals"
    }},
    "time_sensitive_deals": [
        {{"product_id": "id", "deal_id": "id", "expires": "date", "urgency": "high/medium/low"}}
    ],
    "summary": "brief comparison of deal landscape"
}}
"""
        
        return await self.parse_json_response(prompt)
    
    async def check_deal_validity(self, deal_id: str) -> Dict[str, Any]:
        """Check if a specific deal is still valid"""
        
        # Find deal across all products
        for product_deals in self.mock_deals.values():
            for deal in product_deals:
                if deal["id"] == deal_id:
                    # Check expiration
                    valid_until = datetime.strptime(deal["valid_until"], "%Y-%m-%d")
                    is_valid = valid_until > datetime.now()
                    
                    return {
                        "deal_id": deal_id,
                        "is_valid": is_valid,
                        "expires": deal["valid_until"],
                        "days_left": (valid_until - datetime.now()).days if is_valid else 0,
                        "availability": deal.get("availability", "unknown"),
                        "deal": deal
                    }
        
        return {"error": "Deal not found"}
    
    async def suggest_deal_alerts(self, product_ids: List[str], user_preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest deal alerts based on user preferences"""
        
        budget_max = user_preferences.get("budget", {}).get("max", float('inf'))
        deal_types = user_preferences.get("deal_preferences", {}).get("deal_types", [])
        
        suggestions = []
        
        for product_id in product_ids:
            deals = await self.find_deals(product_id)
            
            # Find deals that match user preferences
            matching_deals = []
            for deal in deals:
                sale_price = deal.get("sale_price", deal.get("effective_price", 0))
                if sale_price <= budget_max:
                    if not deal_types or deal["type"] in deal_types:
                        matching_deals.append(deal)
            
            if matching_deals:
                best_deal = max(matching_deals, key=lambda x: x.get("savings", 0))
                suggestions.append({
                    "product_id": product_id,
                    "recommended_deal": best_deal,
                    "alert_reason": "Matches your budget and deal preferences",
                    "urgency": "high" if (datetime.strptime(best_deal["valid_until"], "%Y-%m-%d") - datetime.now()).days < 7 else "medium"
                })
        
        return suggestions
    
    async def get_deal_summary(self, product_id: str) -> str:
        """Get a brief deal summary for display"""
        
        deals = await self.find_deals(product_id)
        if not deals:
            return "No current deals available"
        
        best_deal = deals[0]  # Already sorted by savings
        
        if best_deal["type"] == "discount":
            return f"Save ${best_deal['savings']:.2f} ({best_deal.get('discount_percentage', 0)}% off)"
        elif best_deal["type"] == "coupon":
            return f"Save ${best_deal['savings']:.2f} with code {best_deal.get('coupon_code', 'N/A')}"
        elif best_deal["type"] == "bundle":
            return f"Free extras worth ${best_deal['bundle_value']:.2f}"
        else:
            return f"Save ${best_deal['savings']:.2f}"
    
    async def estimate_price_trends(self, product_id: str) -> Dict[str, Any]:
        """Estimate price trends and suggest best time to buy"""
        
        prompt = f"""
Based on typical e-commerce patterns, estimate price trends for product ID: {product_id}

Consider factors like:
- Seasonal patterns
- New product releases
- Holiday sales
- End-of-year clearances

Return analysis in JSON format:
{{
    "current_trend": "rising/falling/stable",
    "best_time_to_buy": "now/wait_1_month/wait_for_holiday/wait_for_clearance",
    "confidence": "high/medium/low",
    "reasoning": "explanation of recommendation",
    "expected_savings": "estimated savings if waiting",
    "seasonal_patterns": ["when prices typically drop"],
    "upcoming_sales_events": ["Black Friday", "End of year clearance"]
}}
"""
        
        return await self.parse_json_response(prompt) 