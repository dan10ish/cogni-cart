from .base_agent import BaseAgent
from typing import Dict, Any, List
import random

class ReviewAnalyzerAgent(BaseAgent):
    """Agent responsible for analyzing product reviews and sentiment"""
    
    def __init__(self):
        super().__init__()
        self.mock_reviews = self._load_mock_reviews()
        
    def _load_mock_reviews(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load mock review data for demonstration"""
        return {
            "vac001": [
                {
                    "id": "rev001",
                    "rating": 5,
                    "title": "Great for pet hair!",
                    "text": "This vacuum is amazing for removing pet hair from carpets and furniture. The lift-away feature makes cleaning stairs so much easier. It's a bit heavy but the suction power makes up for it.",
                    "verified_purchase": True,
                    "helpful_votes": 45,
                    "date": "2024-01-15"
                },
                {
                    "id": "rev002", 
                    "rating": 4,
                    "title": "Good value for money",
                    "text": "Works well for the price. The HEPA filter is great for allergies. Only complaint is that it can be a bit loud during operation.",
                    "verified_purchase": True,
                    "helpful_votes": 23,
                    "date": "2024-01-20"
                },
                {
                    "id": "rev003",
                    "rating": 3,
                    "title": "Decent but not amazing",
                    "text": "It does the job but I expected better suction. The canister is easy to empty though. Would be better if it was quieter.",
                    "verified_purchase": False,
                    "helpful_votes": 12,
                    "date": "2024-01-25"
                }
            ],
            "vac002": [
                {
                    "id": "rev004",
                    "rating": 5,
                    "title": "Best vacuum I've ever owned",
                    "text": "The laser dust detection is incredible - you can see dust you never knew was there! Very quiet operation and the battery lasts a long time. Worth every penny.",
                    "verified_purchase": True,
                    "helpful_votes": 78,
                    "date": "2024-01-10"
                },
                {
                    "id": "rev005",
                    "rating": 4,
                    "title": "Expensive but effective",
                    "text": "Great suction and the LCD screen is helpful. Battery life could be better for larger homes. The laser feature is more of a gimmick than useful.",
                    "verified_purchase": True,
                    "helpful_votes": 34,
                    "date": "2024-01-18"
                }
            ],
            "lap001": [
                {
                    "id": "rev006",
                    "rating": 5,
                    "title": "Perfect for students and professionals",
                    "text": "The M2 chip is incredibly fast and the battery life is outstanding. Perfect for coding, design work, and everyday tasks. The fanless design keeps it completely silent.",
                    "verified_purchase": True,
                    "helpful_votes": 156,
                    "date": "2024-01-12"
                },
                {
                    "id": "rev007",
                    "rating": 4,
                    "title": "Great laptop, limited ports",
                    "text": "Amazing performance and build quality. My only complaint is the limited number of ports - you'll need adapters for everything.",
                    "verified_purchase": True,
                    "helpful_votes": 89,
                    "date": "2024-01-22"
                }
            ]
        }
    
    async def analyze_reviews(self, product_id: str, focus_features: List[str] = None) -> Dict[str, Any]:
        """Analyze reviews for a specific product"""
        
        reviews = self.mock_reviews.get(product_id, [])
        if not reviews:
            return {"error": "No reviews found for this product"}
        
        # Prepare context for AI analysis
        focus_context = ""
        if focus_features:
            focus_context = f"\nPay special attention to mentions of: {', '.join(focus_features)}"
        
        prompt = f"""
Analyze these product reviews and provide comprehensive insights.

Reviews: {reviews}

{focus_context}

Provide analysis in this JSON format:
{{
    "overall_sentiment": "positive/neutral/negative",
    "sentiment_breakdown": {{
        "positive_percentage": number,
        "neutral_percentage": number, 
        "negative_percentage": number
    }},
    "key_themes": {{
        "positive": ["theme1", "theme2", "theme3"],
        "negative": ["issue1", "issue2", "issue3"]
    }},
    "feature_sentiment": {{
        "feature_name": {{"sentiment": "positive/negative/neutral", "mentions": number}},
        "feature_name2": {{"sentiment": "positive/negative/neutral", "mentions": number}}
    }},
    "common_complaints": ["complaint1", "complaint2"],
    "common_praises": ["praise1", "praise2"], 
    "recommendation_confidence": "high/medium/low",
    "summary": "brief summary of review consensus",
    "red_flags": ["any serious issues mentioned"],
    "best_use_cases": ["use case based on reviews"]
}}
"""
        
        return await self.parse_json_response(prompt)
    
    async def compare_review_sentiments(self, product_ids: List[str], comparison_features: List[str] = None) -> Dict[str, Any]:
        """Compare review sentiments across multiple products"""
        
        all_analyses = {}
        for product_id in product_ids:
            analysis = await self.analyze_reviews(product_id, comparison_features)
            if "error" not in analysis:
                all_analyses[product_id] = analysis
        
        if not all_analyses:
            return {"error": "No review data available for comparison"}
        
        prompt = f"""
Compare the review analyses for these products and provide insights.

Product Analyses: {all_analyses}

Comparison Features Focus: {comparison_features or 'general comparison'}

Provide comparison in this JSON format:
{{
    "winner_overall": "product_id with best overall sentiment",
    "feature_winners": {{
        "feature1": "product_id that performs best for this feature",
        "feature2": "product_id that performs best for this feature"
    }},
    "pros_cons_comparison": {{
        "product_id1": {{"pros": ["pro1", "pro2"], "cons": ["con1", "con2"]}},
        "product_id2": {{"pros": ["pro1", "pro2"], "cons": ["con1", "con2"]}}
    }},
    "recommendation_by_use_case": {{
        "use_case1": "recommended_product_id",
        "use_case2": "recommended_product_id"
    }},
    "summary": "brief comparison summary"
}}
"""
        
        return await self.parse_json_response(prompt)
    
    async def extract_feature_feedback(self, product_id: str, feature: str) -> Dict[str, Any]:
        """Extract specific feedback about a particular feature"""
        
        reviews = self.mock_reviews.get(product_id, [])
        if not reviews:
            return {"error": "No reviews found"}
        
        prompt = f"""
Extract all mentions and sentiment about the specific feature: "{feature}"

Reviews: {reviews}

Focus specifically on: {feature}

Return analysis in JSON format:
{{
    "feature": "{feature}",
    "total_mentions": number,
    "sentiment_breakdown": {{
        "positive": number,
        "neutral": number,
        "negative": number
    }},
    "specific_feedback": [
        {{"quote": "relevant quote from review", "sentiment": "positive/negative/neutral", "rating": review_rating}},
        {{"quote": "another relevant quote", "sentiment": "positive/negative/neutral", "rating": review_rating}}
    ],
    "summary": "summary of feedback about this feature",
    "improvement_suggestions": ["suggestion1", "suggestion2"]
}}
"""
        
        return await self.parse_json_response(prompt)
    
    async def get_review_summary(self, product_id: str) -> str:
        """Get a concise review summary for display"""
        
        analysis = await self.analyze_reviews(product_id)
        if "error" in analysis:
            return "No reviews available for this product."
        
        return analysis.get("summary", "Review analysis not available.") 