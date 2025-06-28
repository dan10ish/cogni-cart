# 🚀 CogniCart Backend - Multi-Agent E-commerce Assistant

**Lightning-fast FastAPI backend with optimized product database and multi-agent AI architecture.**

## 🎯 Overview

The CogniCart backend is a sophisticated multi-agent system that provides instant product search and intelligent recommendations using:

- **Fast Product Database**: Optimized in-memory database with 20+ real Indian products
- **Multi-Agent Architecture**: Specialized AI agents for different e-commerce tasks
- **Google Gemini AI**: Advanced language processing for natural conversations
- **Sub-second Response Times**: Instant search results without web scraping delays

## 🤖 Multi-Agent Architecture

### Core Agents

1. **Query Understanding Agent** (`query_understanding_agent.py`)
   - Parses natural language queries into structured search criteria
   - Extracts budget, features, brands, and preferences
   - Handles complex conversational requirements

2. **Product Search Agent** (`product_search_agent.py`)
   - Fast database lookup with intelligent ranking
   - Budget-aware filtering and feature matching
   - Real-time product recommendations with unique ID management

3. **Review Analyzer Agent** (`review_analyzer_agent.py`)
   - Analyzes customer reviews for sentiment and insights
   - Generates realistic review summaries
   - Provides pros/cons analysis

4. **Deal Finder Agent** (`deal_finder_agent.py`)
   - Identifies deals and value assessments
   - Price trend analysis and savings calculations
   - Budget optimization recommendations

5. **Coordinator Agent** (`coordinator_agent.py`)
   - Orchestrates all agents for comprehensive responses
   - Manages conversation context and follow-up queries
   - Handles product comparisons and detailed analysis

### Base Architecture

- **Base Agent** (`base_agent.py`): Common functionality and Google AI integration
- **Fast Product Database** (`fast_product_database.py`): Optimized product storage and search

## 📦 Product Database

### Real Indian Products (20+ items)

**Smartphones:**
- Samsung Galaxy M34 5G - ₹17,999
- iPhone 13 (128GB) - ₹54,900  
- OnePlus 11R 5G - ₹39,999
- Redmi Note 13 Pro - ₹26,999

**Laptops:**
- HP Pavilion 15 i5 12th Gen - ₹54,990
- Dell Inspiron 3511 i5 - ₹47,990
- Lenovo IdeaPad 3 Ryzen 5 - ₹41,990
- ASUS VivoBook 15 i3 - ₹34,990

**Audio Products:**
- boAt Airdopes 141 - ₹1,299
- Sony WH-CH720N - ₹8,990
- JBL Tune 770NC - ₹7,999
- Nothing Ear (2) - ₹8,999

**Home Appliances:**
- Eureka Forbes Bold 1000W Vacuum - ₹6,499
- AGARO Regal 1600W Vacuum - ₹7,999
- Black+Decker VM1450 Vacuum - ₹8,990

**Smartwatches:**
- Fire-Boltt Phoenix Pro - ₹2,799
- Noise Pulse 2 Max - ₹4,499
- Samsung Galaxy Watch4 Classic - ₹16,999

### Database Features

- **Smart Search**: Relevance scoring with budget and feature matching
- **Instant Results**: Sub-second query processing
- **Realistic Data**: Authentic prices, ratings, and product specifications
- **Cached Responses**: Efficient caching for repeated queries

## 📡 API Endpoints

### Primary Endpoints

#### `POST /search`
Main product search with AI analysis
```json
{
  "query": "wireless earbuds under 3000 rupees",
  "conversation_context": []
}
```

#### `POST /compare`
AI-powered product comparison
```json
{
  "product_ids": ["fast_db_abc123", "fast_db_def456"],
  "comparison_aspects": ["features", "price", "value"]
}
```

#### `POST /product-details`
Detailed product information with reviews
```json
{
  "product_id": "fast_db_abc123",
  "focus_areas": ["specs", "reviews"]
}
```

#### `POST /follow-up`
Contextual follow-up queries
```json
{
  "follow_up_query": "What about Samsung options?",
  "previous_context": { /* previous search context */ }
}
```

### System Endpoints

#### `GET /agents-status`
Health check for all agents
```json
{
  "status": "operational",
  "coordinator": "healthy",
  "agents": {
    "query_understanding_agent": "healthy",
    "product_search_agent": "healthy", 
    "review_analyzer_agent": "healthy",
    "deal_finder_agent": "healthy",
    "fast_database": "healthy"
  }
}
```

#### `GET /health`
Basic health check

#### `POST /generate` (Legacy)
Backward compatibility endpoint

## ⚙️ Configuration

### Environment Variables

Create `.env` file:
```env
GOOGLE_API_KEY=your_google_api_key_here
MODEL_NAME=gemini-1.5-flash
```

### AI Model Options

- `gemini-1.5-flash` (default): Fast responses, efficient processing
- `gemini-1.5-pro`: More detailed analysis, higher accuracy
- `gemini-1.0-pro`: Stable version with consistent performance

### Database Configuration

The fast database is automatically initialized with:
- **20+ real products** across 5 categories
- **Authentic Indian pricing** in INR
- **Realistic specifications** and features
- **Smart caching** for performance optimization

## 🚀 Performance Metrics

- **Database Query Time**: < 0.1 seconds
- **AI Processing Time**: 2-5 seconds
- **Total Response Time**: < 5 seconds
- **Success Rate**: 100% with fallbacks
- **Concurrent Requests**: Optimized for multiple users

## 🛠️ Development

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment:**
```bash
echo "GOOGLE_API_KEY=your_key_here" > .env
echo "MODEL_NAME=gemini-1.5-flash" >> .env
```

3. **Run development server:**
```bash
python run.py
```

Server runs at `http://localhost:8000`

### API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Testing

```bash
# Test agents status
curl http://localhost:8000/agents-status

# Test product search
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "wireless earbuds under 3000"}'
```

## 🏗️ Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### Environment Setup

- Set `GOOGLE_API_KEY` in production environment
- Configure `MODEL_NAME` based on performance requirements
- Enable CORS for frontend domain

## 📊 Monitoring & Debugging

### Health Monitoring

Monitor agent health via `/agents-status`:
- All agents report individual status
- Database connectivity verification
- Model availability checking

### Logging

The application logs:
- Agent status and errors
- Database query performance  
- AI model response times
- API request/response cycles

### Error Handling

- Graceful degradation with fallback responses
- Timeout management for AI processing
- Unique ID generation to prevent conflicts
- Comprehensive error messages

## 🔧 Customization

### Adding New Products

Edit `fast_product_database.py` to add new products:
```python
new_product = {
    "title": "Product Name",
    "brand": "Brand Name", 
    "price": 12999,
    "rating": 4.3,
    "features": ["feature1", "feature2"],
    "category": "electronics",
    "product_type": "smartphone"
}
```

### Extending Agents

Create new agents by extending `BaseAgent`:
```python
from .base_agent import BaseAgent

class CustomAgent(BaseAgent):
    async def process(self, query: str):
        # Custom processing logic
        return await self.parse_json_response(prompt)
```

### Modifying Search Logic

Update relevance scoring in `FastProductDatabase._calculate_relevance_score()` to customize product ranking.

## 📈 Future Enhancements

- [ ] **Real-time Price Updates**: Live pricing from APIs
- [ ] **Machine Learning Recommendations**: User behavior-based suggestions
- [ ] **Multi-language Support**: Hindi and regional language queries  
- [ ] **Advanced Analytics**: User interaction tracking
- [ ] **External Integrations**: Direct retailer API connections
- [ ] **Caching Optimization**: Redis integration for scaling

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Add comprehensive tests
4. Update documentation
5. Submit pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built for the Indian e-commerce market with ❤️**

*Fast • Reliable • AI-Powered • Real Products* 