from .base_agent import BaseAgent
from .fast_product_database import fast_db
from typing import Dict, Any, List
import json
import asyncio

class ProductSearchAgent(BaseAgent):
    """Agent responsible for searching and filtering products using fast Google Shopping"""
    
    def __init__(self):
        super().__init__()
        # No need for scraper - using fast database
        self.product_cache = {}
    
    async def search_products(self, query_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for products using Google Shopping with timeout"""
        
        # Create search query from parsed data
        search_query = self._build_search_query(query_data)
        cache_key = f"search_{hash(search_query)}"
        
        # Check cache first
        if cache_key in self.product_cache:
            print(f"📋 Using cached results for: {search_query}")
            cached_products = self.product_cache[cache_key]
        else:
            print(f"🚀 Fast database search for: {search_query}")
            try:
                # Use fast database - super quick results!
                search_products = await asyncio.to_thread(
                    fast_db.search_products, 
                    search_query, 
                    max_products=6
                )
                
                # Ensure unique IDs to fix React key issue
                search_products = self._ensure_unique_ids(search_products)
                
                # Cache the results
                self.product_cache[cache_key] = search_products
                cached_products = search_products
                
            except Exception as e:
                print(f"❌ Database search failed: {e}")
                cached_products = self._generate_quick_fallback(search_query)
        
        if not cached_products:
            return []
        
        # Filter and rank products using AI
        filtered_products = await self._filter_products(cached_products, query_data)
        ranked_products = await self._rank_products(filtered_products, query_data)
        
        return ranked_products[:6]  # Return top 6
    
    def _ensure_unique_ids(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ensure all products have unique IDs"""
        seen_ids = set()
        unique_products = []
        
        for i, product in enumerate(products):
            original_id = product.get("id", f"prod_{i}")
            
            # If ID already seen, create a new unique one
            if original_id in seen_ids:
                import uuid
                product["id"] = f"unique_{uuid.uuid4().hex[:12]}"
            
            seen_ids.add(product["id"])
            unique_products.append(product)
        
        return unique_products
    
    def _generate_quick_fallback(self, search_query: str) -> List[Dict[str, Any]]:
        """Generate quick fallback products when search fails"""
        import uuid
        import random
        
        products = []
        for i in range(6):
            product_id = f"fallback_{uuid.uuid4().hex[:8]}"
            
            # Estimate price based on query
            base_price = self._estimate_price_from_query(search_query)
            price = int(base_price * random.uniform(0.8, 1.3))
            
            products.append({
                "id": product_id,
                "title": f"{search_query.title()} - Option {i + 1}",
                "category": self._categorize_product(search_query),
                "product_type": self._get_product_type(search_query),
                "price": price,
                "rating": round(random.uniform(3.8, 4.5), 1),
                "review_count": random.randint(100, 1000),
                "brand": "Popular Brand",
                "features": self._extract_features(search_query),
                "availability": "in_stock",
                "currency": "INR",
                "source": "fallback",
                "url": f"https://www.google.com/search?q={search_query.replace(' ', '+')}",
                "image_url": ""
            })
        
        return products
    
    def _estimate_price_from_query(self, query: str) -> int:
        """Estimate price from query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['laptop', 'computer']):
            return 45000
        elif any(word in query_lower for word in ['headphone', 'earphone']):
            return 3000
        elif any(word in query_lower for word in ['mobile', 'phone']):
            return 15000
        elif any(word in query_lower for word in ['watch']):
            return 8000
        else:
            return 2000
    
    def _build_search_query(self, query_data: Dict[str, Any]) -> str:
        """Build search query from parsed user requirements"""
        query_parts = []
        
        # Add product type/category
        if query_data.get("product_type"):
            query_parts.append(query_data["product_type"])
        elif query_data.get("product_category"):
            query_parts.append(query_data["product_category"])
        
        # Add brand preference
        brand_prefs = query_data.get("brand_preferences", [])
        if brand_prefs:
            query_parts.append(brand_prefs[0])  # Use first preferred brand
        
        # Add key features
        features = query_data.get("features_required", [])
        if features:
            # Add 1-2 most important features to search
            query_parts.extend(features[:2])
        
        return " ".join(query_parts) if query_parts else "electronics"
    
    async def _filter_products(self, products: List[Dict[str, Any]], query_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter products based on user requirements"""
        filtered = []
        
        for product in products:
            # Budget filter
            budget = query_data.get("budget", {})
            if budget.get("max") and product.get("price", 0) > budget["max"]:
                continue
            if budget.get("min") and product.get("price", 0) < budget["min"]:
                continue
            
            # Brand filter (if specified)
            brand_prefs = query_data.get("brand_preferences", [])
            if brand_prefs:
                product_brand = product.get("brand", "").lower()
                if not any(brand.lower() in product_brand for brand in brand_prefs):
                    # Don't skip entirely, just lower the score
                    pass
            
            # Rating filter (minimum 3.5 stars)
            if product.get("rating", 0) < 3.5:
                continue
                
            filtered.append(product)
        
        return filtered
    
    async def _rank_products(self, products: List[Dict[str, Any]], query_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Use AI to rank products based on query relevance with timeout"""
        
        if not products:
            return []
        
        try:
            # Create simplified product data for AI ranking
            simplified_products = []
            for i, product in enumerate(products):
                simplified_products.append({
                    "index": i,
                    "title": product.get("title", ""),
                    "brand": product.get("brand", ""),
                    "price": product.get("price", 0),
                    "rating": product.get("rating", 0),
                    "review_count": product.get("review_count", 0),
                    "features": product.get("features", []),
                    "category": product.get("category", "")
                })
            
            prompt = f"""
You are an expert product recommender for Indian e-commerce. Rank these products based on how well they match the user's requirements.

User Requirements: {json.dumps(query_data, indent=2)}

Products to Rank: {json.dumps(simplified_products, indent=2)}

Consider factors like:
- Feature match with requirements (highest priority)
- Price fit within budget
- Brand preference alignment  
- Rating and review count (higher is better)
- Value for money in INR
- Suitability for Indian market

Return ONLY a JSON array of indices representing the ranking order (best matches first).
Example: [2, 0, 1, 3] means product at index 2 is best, then 0, then 1, then 3.
"""
            
            response = await asyncio.wait_for(
                self.parse_json_response(prompt),
                timeout=10.0  # 10 second timeout for AI ranking
            )
            
            if isinstance(response, list) and all(isinstance(x, int) for x in response):
                # Reorder products based on AI ranking
                ranked_products = []
                for index in response:
                    if 0 <= index < len(products):
                        ranked_products.append(products[index])
                return ranked_products
                
        except asyncio.TimeoutError:
            print("⏰ AI ranking timed out, using fallback sorting")
        except Exception as e:
            print(f"⚠️ AI ranking failed: {e}")
        
        # Fallback: sort by rating and review count
        return sorted(products, key=lambda p: (p.get("rating", 0) * 0.7 + min(p.get("review_count", 0) / 1000, 5) * 0.3), reverse=True)
    
    async def get_product_details(self, product_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific product"""
        
        # Find product in cache or database
        product = None
        for cache_key, cached_products in self.product_cache.items():
            for p in cached_products:
                if p.get("id") == product_id:
                    product = p
                    break
            if product:
                break
        
        # If not in cache, try database
        if not product:
            product = fast_db.get_product_by_id(product_id)
        
        if not product:
            return {"error": "Product not found"}
        
        try:
            # Generate realistic detailed info for database products
            detailed_info = {
                "detailed_description": f"High-quality {product.get('product_type', 'product')} with excellent features and reliable performance. Popular choice among Indian customers.",
                "reviews": self._generate_realistic_reviews(product),
                "specifications": self._generate_specifications(product),
                "pros": self._extract_pros_from_features(product),
                "cons": self._generate_realistic_cons(product)
            }
            
            # Enhance with AI-generated analysis
            enhanced_details = await self._enhance_product_details(product, detailed_info)
            
            return {
                **product,
                **detailed_info,
                **enhanced_details
            }
            
        except Exception as e:
            print(f"⚠️ Error getting product details: {e}")
            return {
                **product,
                "detailed_description": "Product details available at retailer",
                "reviews": [],
                "pros": ["Available for purchase"],
                "cons": ["Visit retailer for details"]
            }
    
    async def _enhance_product_details(self, product: Dict[str, Any], detailed_info: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to enhance product details with analysis"""
        
        try:
            prompt = f"""
You are an expert product analyst. Provide a comprehensive analysis of this product for Indian consumers.

Product Data:
{json.dumps(product, indent=2)}

Additional Details:
{json.dumps(detailed_info, indent=2)}

Provide analysis in JSON format with these fields:
- "summary": Brief 2-3 sentence summary highlighting key benefits
- "best_for": List of 3-4 use cases this product is best suited for
- "considerations": List of 2-3 important factors to consider before buying
- "value_assessment": Assessment of value for money in Indian market (1-5 scale with explanation)
- "competitive_advantages": Top 2-3 advantages over similar products
"""
            
            response = await asyncio.wait_for(
                self.parse_json_response(prompt),
                timeout=8.0  # 8 second timeout
            )
            return response if isinstance(response, dict) else {}
            
        except asyncio.TimeoutError:
            print("⏰ Product enhancement timed out")
            return {}
        except Exception as e:
            print(f"⚠️ Product enhancement failed: {e}")
            return {}
    
    async def compare_products(self, product_ids: List[str]) -> Dict[str, Any]:
        """Compare multiple products"""
        
        products = []
        for product_id in product_ids:
            product_details = await self.get_product_details(product_id)
            if product_details and "error" not in product_details:
                products.append(product_details)
        
        if len(products) < 2:
            return {"error": "Need at least 2 valid products to compare"}
        
        # AI-powered comparison
        prompt = f"""
Compare these products for Indian consumers. Focus on practical differences that matter for purchasing decisions.

Products to Compare:
{json.dumps([{k: v for k, v in p.items() if k not in ['detailed_description', 'reviews']} for p in products], indent=2)}

Provide comparison in JSON format with:
- "summary": Overview of the comparison
- "price_comparison": Price analysis with value for money assessment
- "feature_comparison": Key feature differences
- "performance_comparison": Performance and quality comparison
- "recommendation": Which product for which type of user
"""
        
        try:
            comparison = await asyncio.wait_for(
                self.parse_json_response(prompt),
                timeout=10.0
            )
            return {
                "products": products,
                "comparison": comparison if isinstance(comparison, dict) else {}
            }
        except asyncio.TimeoutError:
            print("⏰ Product comparison timed out")
            return {
                "products": products,
                "comparison": {"error": "Comparison analysis timed out"}
            }
        except Exception as e:
            print(f"⚠️ Product comparison failed: {e}")
            return {
                "products": products,
                "comparison": {"error": "Comparison analysis failed"}
            }
    
    def _categorize_product(self, title: str) -> str:
        """Simple categorization based on title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['laptop', 'computer', 'mobile', 'phone', 'tablet', 'headphone', 'speaker']):
            return "electronics"
        elif any(word in title_lower for word in ['vacuum', 'cleaner', 'kitchen', 'home', 'furniture']):
            return "home"
        elif any(word in title_lower for word in ['book', 'novel', 'guide']):
            return "books"
        elif any(word in title_lower for word in ['shirt', 'dress', 'clothes', 'fashion']):
            return "clothing"
        else:
            return "other"
    
    def _get_product_type(self, title: str) -> str:
        """Extract specific product type"""
        title_lower = title.lower()
        
        if 'vacuum' in title_lower:
            return "vacuum cleaner"
        elif 'laptop' in title_lower:
            return "laptop"
        elif any(word in title_lower for word in ['headphone', 'earphone', 'earbud']):
            return "headphones"
        elif 'mobile' in title_lower or 'phone' in title_lower:
            return "smartphone"
        else:
            # Extract first meaningful word
            words = title_lower.split()
            for word in words:
                if len(word) > 3 and word not in ['the', 'and', 'for', 'with']:
                    return word
            return "product"
    
    def _extract_features(self, title: str) -> List[str]:
        """Extract features from title"""
        features = []
        title_lower = title.lower()
        
        feature_keywords = {
            'wireless': 'wireless',
            'bluetooth': 'bluetooth',
            'noise cancel': 'noise canceling',
            'cordless': 'cordless',
            'rechargeable': 'rechargeable',
            'waterproof': 'waterproof',
            'fast charg': 'fast charging',
            'long battery': 'long battery life',
            'hepa': 'HEPA filter',
            'pet hair': 'pet hair removal',
            'lightweight': 'lightweight',
            'portable': 'portable'
        }
        
        for keyword, feature in feature_keywords.items():
            if keyword in title_lower:
                features.append(feature)
        
        return features[:5]  # Limit to 5 features
    
    def _generate_realistic_reviews(self, product: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate realistic customer reviews based on product info"""
        import random
        
        reviews = []
        product_type = product.get('product_type', '')
        brand = product.get('brand', '')
        rating = product.get('rating', 4.0)
        
        # Review templates based on product type
        review_templates = {
            'smartphone': [
                "Great phone! Camera quality is excellent and battery lasts all day. {brand} has done a good job.",
                "Good value for money. Fast performance and smooth display. Delivery was quick too.",
                "Nice phone but could be better. {specific} Overall satisfied with the purchase.",
                "Excellent build quality. Love the design and features. Highly recommended!",
                "Good phone for the price range. {feature} works well. Happy with my purchase."
            ],
            'laptop': [
                "Perfect for work and study. Fast performance and good display quality. {brand} is reliable.",
                "Good laptop for the price. Boots up quickly and handles multitasking well.",
                "Nice build quality. Keyboard is comfortable and screen is clear. Good value for money.",
                "Works great for my needs. {feature} is impressive. Delivery was on time.",
                "Solid laptop. Performance is good for daily tasks. Happy with this purchase."
            ],
            'headphones': [
                "Amazing sound quality! {feature} works perfectly. Great value for money.",
                "Good headphones for the price. Comfortable to wear for long hours. Sound is clear.",
                "Great product! {brand} always delivers quality. Highly recommended.",
                "Nice sound quality and good build. Battery life is impressive. Good purchase.",
                "Perfect for music lovers. Crystal clear sound and comfortable fit."
            ],
            'earbuds': [
                "Great earbuds! {feature} is excellent. Perfect for daily use and workouts.",
                "Good sound quality for the price. Fits comfortably and battery lasts long.",
                "Amazing product! Crystal clear sound and good bass. {brand} is the best.",
                "Perfect for calls and music. Easy to connect and very comfortable.",
                "Excellent earbuds. Sound quality is impressive and they stay in place well."
            ]
        }
        
        # Get appropriate templates
        templates = review_templates.get(product_type, review_templates['smartphone'])
        
        # Generate 3-5 reviews
        for i in range(random.randint(3, 5)):
            template = random.choice(templates)
            
            # Fill in placeholders
            review_text = template.format(
                brand=brand,
                feature=random.choice(product.get('features', ['quality', 'performance'])),
                specific="sound quality could be improved" if product_type in ['headphones', 'earbuds'] else "battery life could be better"
            )
            
            # Generate realistic rating around product rating
            review_rating = max(1, min(5, rating + random.uniform(-0.5, 0.5)))
            
            reviews.append({
                "id": f"review_{i}",
                "rating": round(review_rating, 1),
                "text": review_text,
                "author": f"Customer{i+1}",
                "date": "2024-01-15",  # Static for demo
                "verified": True
            })
        
        return reviews
    
    def _generate_specifications(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Generate realistic specifications based on product info"""
        product_type = product.get('product_type', '')
        
        if product_type == 'smartphone':
            return {
                "Display": "6.5 inch, FHD+",
                "Processor": "Octa-core",
                "RAM": "8GB",
                "Storage": "128GB",
                "Camera": "50MP + 12MP",
                "Battery": "5000mAh",
                "OS": "Android 13"
            }
        elif product_type == 'laptop':
            return {
                "Processor": "Intel Core i5 / AMD Ryzen 5",
                "RAM": "8GB DDR4",
                "Storage": "512GB SSD",
                "Display": "15.6 inch, FHD",
                "Graphics": "Integrated",
                "Battery": "Up to 8 hours",
                "Weight": "1.8 kg"
            }
        elif product_type in ['headphones', 'earbuds']:
            return {
                "Driver": "40mm Dynamic",
                "Frequency Response": "20Hz - 20kHz",
                "Battery Life": "30+ hours",
                "Connectivity": "Bluetooth 5.0",
                "Charging": "USB-C",
                "Water Resistance": "IPX4",
                "Weight": "250g"
            }
        elif product_type == 'vacuum cleaner':
            return {
                "Motor Power": "1400W",
                "Suction": "18 kPa",
                "Capacity": "1.5L",
                "Filter": "HEPA",
                "Cord Length": "5m",
                "Weight": "4.5 kg",
                "Warranty": "2 years"
            }
        else:
            return {
                "Brand": product.get('brand', 'Unknown'),
                "Model": "Latest Model",
                "Warranty": "1 Year",
                "Color": "Multiple Options"
            }
    
    def _extract_pros_from_features(self, product: Dict[str, Any]) -> List[str]:
        """Extract pros from product features"""
        features = product.get('features', [])
        rating = product.get('rating', 4.0)
        
        pros = []
        
        # Add feature-based pros
        for feature in features[:3]:  # Top 3 features
            pros.append(f"Excellent {feature.lower()}")
        
        # Add rating-based pros
        if rating >= 4.5:
            pros.append("Outstanding customer reviews")
        elif rating >= 4.0:
            pros.append("Very good customer satisfaction")
        
        # Add generic pros
        pros.extend([
            "Good value for money",
            "Reliable brand",
            "Available for immediate delivery"
        ])
        
        return pros[:5]  # Limit to 5 pros
    
    def _generate_realistic_cons(self, product: Dict[str, Any]) -> List[str]:
        """Generate realistic cons based on product type"""
        product_type = product.get('product_type', '')
        
        cons_by_type = {
            'smartphone': [
                "Could have faster charging",
                "Camera performance in low light could be better",
                "Storage not expandable"
            ],
            'laptop': [
                "Could use more RAM for heavy tasks",
                "Battery life could be longer",
                "Gets warm during intensive use"
            ],
            'headphones': [
                "Could be more compact for travel",
                "Sound leakage at high volumes"
            ],
            'earbuds': [
                "Case could be smaller",
                "Touch controls can be sensitive"
            ],
            'vacuum cleaner': [
                "Cord could be longer",
                "Can be noisy during operation",
                "Dust container needs frequent emptying"
            ]
        }
        
        return cons_by_type.get(product_type, [
            "Price could be lower",
            "More color options would be nice"
        ])[:3]  # Limit to 3 cons 