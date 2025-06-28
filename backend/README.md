# AI Chat Backend

A FastAPI backend powered by Google Gemini AI for generating intelligent responses to user prompts.

## Features

- **FastAPI Framework**: High-performance Python web framework
- **Google Gemini AI Integration**: Powered by Google's latest AI model (`gemini-1.5-flash`)
- **CORS Enabled**: Configured for frontend communication
- **Input Validation**: Pydantic models for request/response validation
- **Error Handling**: Comprehensive error handling with meaningful messages

## Prerequisites

- Python 3.9+
- Google AI API Key (from [Google AI Studio](https://ai.google.dev/))

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your configuration:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   MODEL_NAME=gemini-1.5-flash
   ```

## Getting Your Google API Key

1. Go to [Google AI Studio](https://ai.google.dev/)
2. Create a new API key
3. Copy the key and add it to your `.env` file

## Running the Application

### Development Mode
```bash
python run.py
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

## API Endpoints

### Health Check
- **GET** `/health` - Check server status

### Root
- **GET** `/` - Welcome message

### Generate Text
- **POST** `/generate`
  - **Request Body**:
    ```json
    {
      "prompt": "Your prompt here"
    }
    ```
  - **Response**:
    ```json
    {
      "response": "AI generated response"
    }
    ```

## API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── main.py           # FastAPI application
├── run.py            # Development runner
├── requirements.txt  # Python dependencies
├── .env.example     # Environment variables template
└── README.md        # This file
```

## Environment Variables

- `GOOGLE_API_KEY`: Your Google AI API key (required)
- `MODEL_NAME`: Gemini model to use (optional, defaults to `gemini-1.5-flash`)

Available Gemini models:
- `gemini-1.5-flash` (default) - Fast and efficient
- `gemini-1.5-pro` - More capable but slower
- `gemini-1.0-pro` - Previous generation model

## Dependencies

- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `google-generativeai`: Google AI SDK
- `python-multipart`: Form data support
- `python-dotenv`: Environment variable loading

## Error Handling

The API includes comprehensive error handling:
- Empty prompts return 400 Bad Request
- AI generation failures return 500 Internal Server Error
- CORS issues are handled with proper middleware

## CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:3000` (Frontend development server)

To add more origins, modify the `allow_origins` list in `main.py`. 