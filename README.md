# Vapi Custom LLM FastAPI Server

A FastAPI server for integrating custom LLM models with Vapi. This server implements the Vapi Custom LLM API specification and uses OpenAI as the backend LLM provider.

## Features

- ✅ FastAPI-based custom LLM server for Vapi
- ✅ `/chat/completions` endpoint compatible with Vapi's specification
- ✅ OpenAI integration (supports all OpenAI models)
- ✅ Optional API Key authentication
- ✅ Health check endpoint
- ✅ Automatic API documentation (Swagger UI)

## Prerequisites

- Python 3.8+
- OpenAI API key (from https://platform.openai.com/api-keys)
- Vapi account and project

## Setup

### 1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 4. Run the server
```bash
python main.py
```

The server will start on `http://localhost:8000`

## Exposing to the Internet

For Vapi to communicate with your server, you need to expose it to the internet using a tunneling service like ngrok:

```bash
# Install ngrok: https://ngrok.com/download
ngrok http 8000
```

This will provide you with a public URL like `https://your-unique-id.ngrok.io`

## Configuration in Vapi

1. Go to your Vapi dashboard
2. Create or edit an assistant/call
3. Select "Custom LLM" as the model
4. Set the server URL to your ngrok URL (e.g., `https://your-unique-id.ngrok.io`)
5. (Optional) Add authentication headers if you set `VAPI_API_KEY`

## API Endpoints

### POST /chat/completions
Main endpoint for LLM requests from Vapi

**Request Body:**
```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
  "model": "gpt-3.5-turbo",
  "temperature": 0.7,
  "max_tokens": 1000,
  "system_prompt": "Optional system prompt"
}
```

**Response:**
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ],
  "model": "gpt-3.5-turbo",
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 12,
    "total_tokens": 22
  }
}
```

### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "service": "vapi-custom-llm"
}
```

## Development

- **API Documentation**: Available at `http://localhost:8000/docs`
- **Swagger UI**: Available at `http://localhost:8000/swagger-ui`
- **ReDoc**: Available at `http://localhost:8000/redoc`

## Authentication (Optional)

To add API key authentication:

1. Set `VAPI_API_KEY` in your `.env` file
2. In the Vapi dashboard, add a header:
   - Key: `Authorization`
   - Value: `Bearer YOUR_VAPI_API_KEY`

The server will validate incoming requests against this key.

## Supported Models

This server uses OpenAI's API, so it supports all OpenAI models:
- gpt-4
- gpt-4-turbo-preview
- gpt-3.5-turbo
- And other OpenAI models

## Customization

To use a different LLM provider:

1. Replace the `openai.ChatCompletion.create()` call in `main.py`
2. Ensure your response matches the expected format
3. Update `requirements.txt` with your provider's SDK

## Troubleshooting

- **401 Unauthorized**: Check your API key authentication settings
- **500 Internal Server Error**: Verify your OpenAI API key is valid
- **Connection timeout**: Ensure ngrok tunnel is running and URL is correct

## References

- [Vapi Custom LLM Documentation](https://docs.vapi.ai/customization/custom-llm/using-your-server)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)


## Deployment on Railway

Railway makes it easy to deploy this FastAPI server. Follow these steps:

### 1. Connect Your GitHub Repository
- Go to [Railway.app](https://railway.app)
- Click "New Project"
- Select "Deploy from GitHub"
- Authorize Railway and select the `vapi-custom-llm-server` repository

### 2. Configure Environment Variables
In the Railway dashboard:
1. Go to your project settings
2. Add environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `VAPI_API_KEY`: (Optional) Your Vapi API key for authentication

### 3. Deploy
Railway will automatically detect the Dockerfile and deploy your application. You'll get a public URL like:
```
https://vapi-custom-llm-server-production.up.railway.app
```

### 4. Configure Vapi
Use the Railway URL (without trailing slash) in your Vapi dashboard:
```
https://vapi-custom-llm-server-production.up.railway.app
```

### Railway Features Included
- ✅ Dockerfile for containerized deployment
- ✅ Procfile for flexible start command
- ✅ railway.json for Railway-specific configuration
- ✅ .dockerignore to keep image size small
- ✅ Automatic environment variable handling (PORT)
- ✅ Auto-scaling support
- ✅ Health checks compatible

### Monitoring on Railway
Railway provides:
- Real-time logs
- Deployment history
- Resource usage metrics
- Automatic restarts on failure

### Setting Custom Domain (Optional)
In Railway dashboard:
1. Go to Settings
2. Add your custom domain
3. Configure DNS pointing to Railway

For more information, see [Railway Documentation](https://docs.railway.app)
