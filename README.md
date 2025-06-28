# CogniCart - Multi-Agent E-commerce Assistant

A sophisticated AI-powered e-commerce assistant that helps users find the best products through natural language queries, powered by Google Gemini AI and featuring a multi-agent architecture.

## 🚀 Project Overview

CogniCart revolutionizes online shopping by understanding complex, conversational queries and providing intelligent product recommendations:

- **Multi-Agent Architecture**: Specialized AI agents for different tasks
- **Natural Language Understanding**: Understands complex shopping queries
- **Review Analysis**: AI-powered sentiment analysis of product reviews  
- **Deal Discovery**: Finds the best deals and discounts automatically
- **Product Comparison**: Side-by-side comparison with AI insights
- **Modern UI**: Beautiful, responsive interface with Shadcn UI components

## 🤖 Multi-Agent System

### Backend Agents:
- **QueryUnderstandingAgent**: Parses natural language shopping queries
- **ProductSearchAgent**: Searches and ranks products based on requirements
- **ReviewAnalyzerAgent**: Analyzes customer reviews for sentiment and insights
- **DealFinderAgent**: Discovers deals, discounts, and best prices
- **CoordinatorAgent**: Orchestrates all agents for comprehensive responses

### Technology Stack:
- **Backend**: FastAPI with Google Gemini AI (multi-agent architecture)
- **Frontend**: Next.js 15 with TypeScript, Tailwind CSS, and Shadcn UI
- **AI Model**: Google Gemini 1.5 Flash (configurable)
- **Icons**: Lucide React for beautiful, consistent icons

## Project Structure

```
cogni-cart/
├── backend/                           # Multi-Agent FastAPI Server
│   ├── agents/                       # AI Agent System
│   │   ├── __init__.py              # Agent package
│   │   ├── base_agent.py            # Base agent class with Google AI integration
│   │   ├── coordinator_agent.py     # Main orchestrator agent
│   │   ├── query_understanding_agent.py  # Natural language query parser
│   │   ├── product_search_agent.py      # Product search and ranking
│   │   ├── review_analyzer_agent.py     # Review sentiment analysis  
│   │   └── deal_finder_agent.py         # Deal and discount discovery
│   ├── main.py                      # FastAPI application with multi-agent endpoints
│   ├── run.py                       # Development runner
│   ├── requirements.txt             # Python dependencies
│   ├── .env.example                 # Environment template
│   └── README.md                    # Backend documentation
├── frontend/                        # Next.js E-commerce Interface
│   ├── app/page.tsx                # Main e-commerce shopping interface
│   ├── components/                 # Custom e-commerce components
│   │   ├── product-card.tsx        # Product display cards with ratings & deals
│   │   ├── search-interface.tsx    # Advanced conversational search UI
│   │   └── product-details-modal.tsx  # Detailed product information popup
│   ├── components/ui/              # Shadcn UI components (Button, Card, etc.)
│   ├── lib/utils.ts               # Utility functions
│   ├── package.json               # Node.js dependencies with Lucide icons
│   └── README.md                  # Frontend documentation
├── .gitignore                     # Git ignore file
└── README.md                      # This file
```

## Quick Start

### Prerequisites

- **Python 3.9+** for backend
- **Node.js 18+** for frontend
- **Google AI API Key** from [Google AI Studio](https://ai.google.dev/)

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd cogni-cart
```

### 2. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Run the backend
python run.py
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install Node.js dependencies
npm install

# Run the frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 4. Get Your Google AI API Key

1. Visit [Google AI Studio](https://ai.google.dev/)
2. Create a new project or select an existing one
3. Generate an API key
4. Add it to `backend/.env`:
   ```
   GOOGLE_API_KEY=your_api_key_here
   MODEL_NAME=gemini-1.5-flash
   ```

## ✨ Features

### 🤖 AI-Powered Features
- **Natural Language Search**: "I need a quiet, pet-friendly vacuum cleaner under $300"
- **Intelligent Product Ranking**: AI ranks products based on your specific requirements
- **Review Sentiment Analysis**: Analyzes thousands of reviews to extract key insights
- **Deal Discovery**: Automatically finds discounts, coupons, and best prices
- **Product Comparison**: AI-powered side-by-side comparisons with detailed insights
- **Contextual Follow-ups**: Remembers conversation context for better recommendations

### 🖥️ Backend Features
- ✅ **Multi-Agent Architecture**: Specialized AI agents working together
- ✅ **FastAPI**: Modern async Python framework with automatic docs
- ✅ **Google Gemini AI**: Configurable AI models (Flash/Pro)
- ✅ **Advanced Query Parsing**: Extracts budget, features, brands from natural language
- ✅ **Review Analysis Engine**: Sentiment analysis with pros/cons extraction
- ✅ **Deal Tracking**: Mock deal database with expiration tracking
- ✅ **CORS & Error Handling**: Production-ready API with comprehensive error handling

### 🎨 Frontend Features
- ✅ **Beautiful E-commerce UI**: Modern, responsive design with Shadcn UI
- ✅ **Product Cards**: Rich product displays with ratings, deals, and features
- ✅ **Advanced Search Interface**: Conversational search with examples and history
- ✅ **Product Details Modal**: Tabbed interface with specs, reviews, and deals
- ✅ **Comparison System**: Select up to 3 products for AI-powered comparison
- ✅ **Lucide Icons**: Beautiful, consistent iconography throughout
- ✅ **Responsive Design**: Perfect on desktop, tablet, and mobile
- ✅ **Loading States**: Smooth animations and loading indicators

## 📡 API Endpoints

### Multi-Agent E-commerce API (`http://localhost:8000`)

#### Core Endpoints
- `GET /` - Service information and capabilities
- `GET /health` - Health check for all services
- `GET /agents-status` - Status of all AI agents

#### Multi-Agent Shopping Endpoints
- `POST /search` - **Main product search with AI analysis**
  ```json
  {
    "query": "I need a quiet, pet-friendly vacuum cleaner under $300",
    "conversation_context": []
  }
  ```

- `POST /compare` - **AI-powered product comparison**
  ```json
  {
    "product_ids": ["vac001", "vac002"],
    "comparison_aspects": ["noise_level", "pet_hair_removal"]
  }
  ```

- `POST /product-details` - **Detailed product information with reviews & deals**
  ```json
  {
    "product_id": "vac001",
    "focus_areas": ["noise_level", "pet_features"]
  }
  ```

- `POST /follow-up` - **Contextual follow-up questions**
  ```json
  {
    "follow_up_query": "What about the Dyson option?",
    "previous_context": { /* previous search results */ }
  }
  ```

#### Legacy Support
- `POST /generate` - Legacy endpoint (auto-routes to multi-agent system for product queries)

### 📚 Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 💡 Example Usage

### Natural Language Queries
Try these example searches in the frontend:

1. **Complex Requirements**: 
   ```
   "I need a quiet, pet-friendly vacuum cleaner under $300 for hardwood floors and area rugs"
   ```

2. **Brand and Budget Preferences**:
   ```
   "Find me a gaming laptop from ASUS or MSI under $1500 with good graphics"
   ```

3. **Feature-Focused Search**:
   ```
   "Best noise-canceling headphones for travel with long battery life"
   ```

4. **Comparison Request**:
   ```
   "Compare the top 3 robot vacuums for pet hair under $600"
   ```

### Multi-Agent Workflow
1. **Query Understanding** → Parses your natural language requirements
2. **Product Search** → Finds and ranks relevant products using AI
3. **Review Analysis** → Analyzes customer feedback for insights  
4. **Deal Discovery** → Finds current discounts and best prices
5. **Intelligent Response** → Presents comprehensive recommendations

### Frontend Features Demo
- 🔍 **Smart Search**: Type naturally, get intelligent results
- 📊 **Product Cards**: See ratings, deals, and key features at a glance
- 🔍 **Detailed Views**: Click "Details" for comprehensive product information
- ⚖️ **Comparison**: Select products and click "Compare" for AI analysis
- 📱 **Responsive**: Works perfectly on mobile, tablet, and desktop

## Development Workflow

### Running Both Services

**Terminal 1 (Backend):**
```bash
cd backend
python run.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

### Making Changes

- **Backend changes**: The server auto-reloads with `uvicorn --reload`
- **Frontend changes**: Next.js provides hot reloading
- **UI components**: Add new Shadcn components with `npx shadcn@latest add [component]`

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Google Generative AI**: Latest Gemini model integration
- **Uvicorn**: ASGI server for production
- **Pydantic**: Data validation and serialization
- **Python-dotenv**: Environment variable management

### Frontend
- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Shadcn UI**: Beautiful, accessible components
- **Tailwind CSS**: Utility-first styling
- **Radix UI**: Headless UI primitives

## Deployment

### Backend Deployment
- Can be deployed to any platform supporting Python/FastAPI
- Recommended: Railway, Render, or DigitalOcean
- Ensure `GOOGLE_API_KEY` is set in production environment

### Frontend Deployment
- Optimized for Vercel (created by Next.js team)
- Can also deploy to Netlify, Railway, or any static hosting
- Update backend URL in production build

### Environment Variables
```bash
# Backend (.env)
GOOGLE_API_KEY=your_google_api_key
MODEL_NAME=gemini-1.5-flash

# Frontend (if needed for production)
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both backend and frontend
5. Submit a pull request

## Troubleshooting

### Common Issues

**Backend not starting:**
- Check Python version (3.9+)
- Verify Google API key is set
- Install dependencies: `pip install -r requirements.txt`

**Frontend not connecting:**
- Ensure backend is running on port 8000
- Check for CORS errors in browser console
- Verify fetch URL in `frontend/app/page.tsx`

**AI responses not working:**
- Validate Google API key
- Check API quota/billing in Google Cloud Console
- Review backend logs for detailed errors

### Logs and Debugging

**Backend logs:**
```bash
cd backend
python run.py
# Check terminal output for errors
```

**Frontend logs:**
```bash
cd frontend
npm run dev
# Check browser console for errors
```

## License

This project is open source and available under the [MIT License](LICENSE).

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Google AI Documentation](https://ai.google.dev/docs)
- [Shadcn UI Components](https://ui.shadcn.com/)
- [Tailwind CSS](https://tailwindcss.com/docs) 