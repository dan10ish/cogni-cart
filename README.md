# AI Chat Application

A full-stack AI chat application with a FastAPI backend powered by Google Gemini AI and a modern Next.js frontend with Shadcn UI.

## Project Overview

This project demonstrates the integration of cutting-edge AI technology with modern web development practices:

- **Backend**: FastAPI with Google Gemini AI integration
- **Frontend**: Next.js 15 with TypeScript and Shadcn UI
- **AI Model**: Google Gemini 1.5 Flash for intelligent responses

## Project Structure

```
cogni-cart/
├── backend/              # FastAPI server with Google AI
│   ├── main.py          # FastAPI application
│   ├── run.py           # Development runner
│   ├── requirements.txt # Python dependencies
│   ├── .env.example     # Environment template
│   └── README.md        # Backend documentation
├── frontend/            # Next.js chat interface
│   ├── app/             # Next.js app directory
│   ├── components/      # Shadcn UI components
│   ├── lib/             # Utility functions
│   └── README.md        # Frontend documentation
└── README.md            # This file
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
   ```

## Features

### Backend Features
- ✅ FastAPI with automatic API documentation
- ✅ Google Gemini AI integration
- ✅ CORS enabled for frontend communication
- ✅ Comprehensive error handling
- ✅ Input validation with Pydantic models
- ✅ Health check endpoints

### Frontend Features
- ✅ Modern chat interface with message bubbles
- ✅ Real-time typing indicators
- ✅ Responsive design (mobile-first)
- ✅ Keyboard shortcuts (Enter to send)
- ✅ Error handling with user feedback
- ✅ Loading states and animations
- ✅ Clean, accessible UI with Shadcn components

## API Endpoints

### Backend API (`http://localhost:8000`)

- `GET /` - Welcome message
- `GET /health` - Health check
- `POST /generate` - Generate AI response
  ```json
  {
    "prompt": "Your message here"
  }
  ```

### Interactive Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

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