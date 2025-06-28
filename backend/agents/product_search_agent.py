from .base_agent import BaseAgent
from typing import Dict, Any, List
import json
import random

class ProductSearchAgent(BaseAgent):
    """Agent responsible for searching and filtering products"""
    
    def __init__(self):
        super().__init__()
        self.mock_products = self._load_mock_products()
        
    def _load_mock_products(self) -> List[Dict[str, Any]]:
        """Load mock product data for demonstration"""
        return [
            {
                "id": "vac001",
                "title": "Shark Navigator Lift-Away Professional NV356E",
                "category": "home",
                "product_type": "vacuum cleaner",
                "price": 179.99,
                "rating": 4.4,
                "review_count": 15420,
                "brand": "Shark",
                "features": ["pet hair removal", "HEPA filter", "lift-away canister", "lightweight"],
                "noise_level": "moderate",
                "weight": "12.5 lbs",
                "image_url": "https://example.com/shark-navigator.jpg",
                "availability": "in_stock"
            },
            {
                "id": "vac002", 
                "title": "Dyson V15 Detect Absolute",
                "category": "home",
                "product_type": "vacuum cleaner", 
                "price": 749.99,
                "rating": 4.6,
                "review_count": 8920,
                "brand": "Dyson",
                "features": ["laser dust detection", "LCD screen", "pet hair removal", "cordless"],
                "noise_level": "quiet",
                "weight": "6.8 lbs",
                "image_url": "https://example.com/dyson-v15.jpg",
                "availability": "in_stock"
            },
            {
                "id": "vac003",
                "title": "Bissell CrossWave Pet Pro All-in-One Wet Dry Vacuum",
                "category": "home", 
                "product_type": "vacuum cleaner",
                "price": 329.99,
                "rating": 4.2,
                "review_count": 12150,
                "brand": "Bissell",
                "features": ["wet and dry cleaning", "pet hair removal", "multi-surface", "easy empty"],
                "noise_level": "moderate",
                "weight": "11.5 lbs", 
                "image_url": "https://example.com/bissell-crosswave.jpg",
                "availability": "in_stock"
            },
            {
                "id": "lap001",
                "title": "Apple MacBook Air M2",
                "category": "electronics",
                "product_type": "laptop",
                "price": 1199.99,
                "rating": 4.7,
                "review_count": 3240,
                "brand": "Apple",
                "features": ["M2 chip", "13-inch display", "18-hour battery", "fanless design"],
                "weight": "2.7 lbs",
                "screen_size": "13.6 inches",
                "image_url": "https://example.com/macbook-air-m2.jpg",
                "availability": "in_stock"
            },
            {
                "id": "lap002", 
                "title": "Dell XPS 13 Plus",
                "category": "electronics",
                "product_type": "laptop",
                "price": 1299.99,
                "rating": 4.3,
                "review_count": 1850,
                "brand": "Dell",
                "features": ["12th Gen Intel Core i7", "13.4-inch OLED", "premium design", "fast charging"],
                "weight": "2.73 lbs",
                "screen_size": "13.4 inches", 
                "image_url": "https://example.com/dell-xps-13.jpg",
                "availability": "in_stock"
            },
            {
                "id": "head001",
                "title": "Sony WH-1000XM5 Wireless Noise Canceling Headphones",
                "category": "electronics",
                "product_type": "headphones",
                "price": 399.99,
                "rating": 4.6,
                "review_count": 5670,
                "brand": "Sony", 
                "features": ["active noise canceling", "30-hour battery", "quick charge", "premium comfort"],
                "noise_canceling": "excellent",
                "wireless": True,
                "image_url": "https://example.com/sony-wh1000xm5.jpg",
                "availability": "in_stock"
            }
        ]
    
    async def search_products(self, query_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for products based on parsed query data"""
        
        # Filter products based on query criteria
        filtered_products = []
        
        for product in self.mock_products:
            matches = True
            
            # Category filter
            if query_data.get("product_category"):
                if product["category"] != query_data["product_category"]:
                    continue
                    
            # Product type filter  
            if query_data.get("product_type"):
                if product["product_type"] != query_data["product_type"]:
                    continue
                    
            # Budget filter
            budget = query_data.get("budget", {})
            if budget.get("max") and product["price"] > budget["max"]:
                continue
            if budget.get("min") and product["price"] < budget["min"]:
                continue
                
            # Brand filter
            brand_prefs = query_data.get("brand_preferences", [])
            if brand_prefs and product["brand"] not in brand_prefs:
                continue
                
            # Feature matching
            required_features = query_data.get("features_required", [])
            product_features = product.get("features", [])
            
            if required_features:
                feature_matches = 0
                for req_feature in required_features:
                    for prod_feature in product_features:
                        if req_feature.lower() in prod_feature.lower():
                            feature_matches += 1
                            break
                
                # Require at least 50% feature match
                if feature_matches / len(required_features) < 0.5:
                    continue
            
            filtered_products.append(product)
        
        # Rank products using AI
        if filtered_products:
            ranked_products = await self._rank_products(filtered_products, query_data)
            return ranked_products[:10]  # Return top 10
        
        return []
    
    async def _rank_products(self, products: List[Dict[str, Any]], query_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Use AI to rank products based on query relevance"""
        
        prompt = f"""
You are an expert product recommender. Rank these products based on how well they match the user's requirements.

User Requirements: {json.dumps(query_data, indent=2)}

Products to Rank: {json.dumps(products, indent=2)}

Consider factors like:
- Feature match with requirements
- Price fit within budget
- Brand preference alignment  
- Rating and review count
- Specific use case fit

Return the products in ranked order (best matches first) as a JSON array of the original product objects.
"""
        
        try:
            response = await self.parse_json_response(prompt)
            if isinstance(response, list):
                return response
            return products  # Return original order if ranking fails
        except:
            return products
    
    async def get_product_details(self, product_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific product"""
        
        product = next((p for p in self.mock_products if p["id"] == product_id), None)
        if not product:
            return {}
            
        # Enhance with AI-generated detailed description
        prompt = f"""
Create a detailed product description and specifications for this product:

Product: {json.dumps(product, indent=2)}

Return a JSON object with:
{{
    "detailed_description": "compelling product description",
    "key_specifications": {{"spec1": "value1", "spec2": "value2"}},
    "pros": ["advantage1", "advantage2", "advantage3"],
    "cons": ["limitation1", "limitation2"],
    "best_for": ["use case1", "use case2"],
    "similar_products": ["suggestion1", "suggestion2"]
}}
"""
        
        try:
            ai_details = await self.parse_json_response(prompt)
            product.update(ai_details)
            return product
        except:
            return product 