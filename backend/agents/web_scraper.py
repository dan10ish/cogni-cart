import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict, Any
import re
from urllib.parse import urljoin, quote

class SimpleEcommerceScraper:
    """Simple web scraper for Indian e-commerce sites"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
    def search_amazon_in(self, query: str, max_products: int = 5) -> List[Dict[str, Any]]:
        """Search Amazon.in for products"""
        try:
            search_url = f"https://www.amazon.in/s?k={quote(query)}&ref=sr_pg_1"
            
            print(f"🔍 Searching Amazon.in for: {query}")
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code != 200:
                print(f"❌ Amazon search failed with status: {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            products = []
            
            # Find product containers
            product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})[:max_products]
            
            for container in product_containers:
                try:
                    product = self._extract_amazon_product(container)
                    if product:
                        products.append(product)
                        time.sleep(random.uniform(0.5, 1.0))  # Be respectful
                except Exception as e:
                    print(f"⚠️ Error extracting product: {e}")
                    continue
            
            print(f"✅ Found {len(products)} products from Amazon.in")
            return products
            
        except Exception as e:
            print(f"❌ Amazon search error: {e}")
            return []
    
    def _extract_amazon_product(self, container) -> Dict[str, Any]:
        """Extract product data from Amazon container"""
        try:
            # Product title
            title_elem = container.find('h2', class_='a-size-mini')
            if not title_elem:
                title_elem = container.find('span', class_='a-size-medium')
            title = title_elem.get_text(strip=True) if title_elem else "Unknown Product"
            
            # Price in INR
            price_elem = container.find('span', class_='a-price-whole')
            if not price_elem:
                price_elem = container.find('span', class_='a-offscreen')
            
            price = 0
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_numbers = re.findall(r'[\d,]+', price_text.replace('₹', ''))
                if price_numbers:
                    price = float(price_numbers[0].replace(',', ''))
            
            # Rating
            rating_elem = container.find('span', class_='a-icon-alt')
            rating = 0
            if rating_elem:
                rating_text = rating_elem.get_text()
                rating_match = re.search(r'(\d\.\d)', rating_text)
                if rating_match:
                    rating = float(rating_match.group(1))
            
            # Review count
            review_elem = container.find('span', class_='a-size-base')
            review_count = 0
            if review_elem and review_elem.get_text():
                review_text = review_elem.get_text()
                review_numbers = re.findall(r'([\d,]+)', review_text)
                if review_numbers:
                    review_count = int(review_numbers[0].replace(',', ''))
            
            # Product link for detailed scraping
            link_elem = container.find('h2').find('a') if container.find('h2') else None
            product_url = urljoin("https://www.amazon.in", link_elem['href']) if link_elem else ""
            
            # Generate product ID
            product_id = f"amz_{hash(title) % 10000}"
            
            # Determine category and features
            category = self._categorize_product(title)
            features = self._extract_features(title)
            
            return {
                "id": product_id,
                "title": title[:100],  # Limit length
                "category": category,
                "product_type": self._get_product_type(title),
                "price": price,
                "rating": rating,
                "review_count": review_count,
                "brand": self._extract_brand(title),
                "features": features,
                "availability": "in_stock",
                "currency": "INR",
                "source": "amazon.in",
                "url": product_url,
                "image_url": self._extract_image_url(container)
            }
            
        except Exception as e:
            print(f"⚠️ Error extracting Amazon product: {e}")
            return None
    
    def _extract_image_url(self, container) -> str:
        """Extract product image URL"""
        try:
            img_elem = container.find('img')
            if img_elem and img_elem.get('src'):
                return img_elem['src']
        except:
            pass
        return ""
    
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
    
    def _extract_brand(self, title: str) -> str:
        """Extract brand from title"""
        common_brands = [
            'Apple', 'Samsung', 'Sony', 'LG', 'Dyson', 'Shark', 'Bissell',
            'HP', 'Dell', 'Lenovo', 'ASUS', 'Acer', 'OnePlus', 'Xiaomi',
            'Realme', 'Vivo', 'Oppo', 'Boat', 'JBL', 'Bose'
        ]
        
        for brand in common_brands:
            if brand.lower() in title.lower():
                return brand
        
        # Try to extract first word as brand
        words = title.split()
        if words:
            return words[0]
        
        return "Unknown"
    
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
    
    def get_detailed_product_info(self, product_url: str) -> Dict[str, Any]:
        """Get detailed product information including reviews"""
        try:
            if not product_url:
                return {}
            
            print(f"🔍 Getting details for: {product_url}")
            response = self.session.get(product_url, timeout=10)
            
            if response.status_code != 200:
                return {}
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract reviews (simple approach)
            reviews = self._extract_amazon_reviews(soup)
            
            # Extract specifications
            specs = self._extract_specifications(soup)
            
            return {
                "detailed_description": self._extract_description(soup),
                "key_specifications": specs,
                "reviews": reviews[:5],  # Limit to 5 reviews
                "pros": self._extract_pros_from_reviews(reviews),
                "cons": self._extract_cons_from_reviews(reviews),
            }
            
        except Exception as e:
            print(f"⚠️ Error getting product details: {e}")
            return {}
    
    def _extract_amazon_reviews(self, soup) -> List[Dict[str, Any]]:
        """Extract reviews from Amazon product page"""
        reviews = []
        try:
            review_elements = soup.find_all('div', {'data-hook': 'review'})[:5]
            
            for review_elem in review_elements:
                try:
                    # Rating
                    rating_elem = review_elem.find('i', class_='a-icon-star')
                    rating = 0
                    if rating_elem:
                        rating_text = rating_elem.get_text()
                        rating_match = re.search(r'(\d)', rating_text)
                        if rating_match:
                            rating = int(rating_match.group(1))
                    
                    # Review text
                    text_elem = review_elem.find('span', {'data-hook': 'review-body'})
                    text = text_elem.get_text(strip=True) if text_elem else ""
                    
                    # Title
                    title_elem = review_elem.find('a', {'data-hook': 'review-title'})
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    
                    if text and rating:
                        reviews.append({
                            "rating": rating,
                            "title": title,
                            "text": text[:500],  # Limit length
                            "verified_purchase": "Verified Purchase" in review_elem.get_text(),
                        })
                        
                except Exception as e:
                    print(f"⚠️ Error extracting review: {e}")
                    continue
        except Exception as e:
            print(f"⚠️ Error extracting reviews: {e}")
        
        return reviews
    
    def _extract_description(self, soup) -> str:
        """Extract product description"""
        try:
            desc_elem = soup.find('div', id='productDescription')
            if desc_elem:
                return desc_elem.get_text(strip=True)[:500]
        except:
            pass
        return "Product description not available"
    
    def _extract_specifications(self, soup) -> Dict[str, str]:
        """Extract product specifications"""
        specs = {}
        try:
            spec_table = soup.find('table', id='productDetails_techSpec_section_1')
            if spec_table:
                rows = spec_table.find_all('tr')
                for row in rows[:5]:  # Limit to 5 specs
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        key = cells[0].get_text(strip=True)
                        value = cells[1].get_text(strip=True)
                        specs[key] = value
        except:
            pass
        return specs
    
    def _extract_pros_from_reviews(self, reviews: List[Dict]) -> List[str]:
        """Extract pros from reviews using simple keyword analysis"""
        pros = []
        positive_keywords = ['good', 'great', 'excellent', 'amazing', 'perfect', 'love', 'best']
        
        for review in reviews:
            if review.get('rating', 0) >= 4:
                text = review.get('text', '').lower()
                for keyword in positive_keywords:
                    if keyword in text:
                        # Extract sentence with positive keyword
                        sentences = text.split('.')
                        for sentence in sentences:
                            if keyword in sentence and len(sentence.strip()) > 10:
                                pros.append(sentence.strip()[:100])
                                break
                        if len(pros) >= 3:
                            break
            if len(pros) >= 3:
                break
        
        return pros[:3]
    
    def _extract_cons_from_reviews(self, reviews: List[Dict]) -> List[str]:
        """Extract cons from reviews using simple keyword analysis"""
        cons = []
        negative_keywords = ['bad', 'poor', 'terrible', 'worst', 'hate', 'problem', 'issue']
        
        for review in reviews:
            if review.get('rating', 0) <= 2:
                text = review.get('text', '').lower()
                for keyword in negative_keywords:
                    if keyword in text:
                        sentences = text.split('.')
                        for sentence in sentences:
                            if keyword in sentence and len(sentence.strip()) > 10:
                                cons.append(sentence.strip()[:100])
                                break
                        if len(cons) >= 3:
                            break
            if len(cons) >= 3:
                break
        
        return cons[:3] 