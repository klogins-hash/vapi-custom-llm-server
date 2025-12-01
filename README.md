# Vapi Custom LLM FastAPI Server

A FastAPI server for integrating custom LLM models with Vapi. This server implements the Vapi Custom LLM API specification and uses OpenAI as the backend LLM provider.

## Features

- ✅ FastAPI-based custom LLM server for Vapi
- ✅ `/chat/completions` endpoint compatible with Vapi's specification
- ✅ OpenAI integration (supports all OpenAI models)
- ✅ Optional API Key authentication
- ✅ Health check endpoint
- ✅ Automatic API documentation (Swagger UI)
- ✅ Database support with SQLAlchemy (SQLite for local, PostgreSQL for production)
- ✅ Automatic LLM interaction logging and persistence
- ✅ Volume mounting for data persistence

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

## Database Support

This server includes built-in database support for storing and querying LLM interactions.

### Database Options

**SQLite (Local Development)**
- Default option for local development
- File-based, no server setup required
- Data stored in `vapi_custom_llm.db`
- Perfect for testing and small-scale deployments

**PostgreSQL (Production)**
- Recommended for production deployments
- Persistent data with full ACID compliance
- Supports concurrent access
- Easy scaling capabilities

### Local Development with Docker Compose

To use PostgreSQL locally with docker-compose:

```bash
# Copy environment template
cp .env.example .env

# Edit .env and set DATABASE_URL to PostgreSQL connection
# DATABASE_URL=postgresql+psycopg2://vapi:vapi@postgres:5432/vapi_db

# Start PostgreSQL and the app
docker-compose up -d

# Access the app at http://localhost:8000
```

The docker-compose setup includes:
- FastAPI application (port 8000)
- PostgreSQL database (port 5432)
- Automatic volume mounting for data persistence
- Health checks and restart policies

### Database Schema

**LLMInteraction Table:**
```sql
CREATE TABLE llm_interactions (
    id INTEGER PRIMARY KEY,
    user_message TEXT NOT NULL,
    assistant_response TEXT,
    model VARCHAR(255) DEFAULT 'gpt-3.5-turbo',
    temperature FLOAT DEFAULT 0.7,
    tokens_used INTEGER DEFAULT 0,
    error_message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Database API Endpoints

#### GET /interactions
Retrieve recent LLM interactions

**Query Parameters:**
- `limit`: Number of records to return (default: 100, max: 100)
- `offset`: Pagination offset (default: 0)

**Example:**
```bash
curl "http://localhost:8000/interactions?limit=10&offset=0"
```

**Response:**
```json
[
  {
    "id": 1,
    "user_message": "Hello, how are you?",
    "assistant_response": "I'm doing well, thank you for asking!",
    "model": "gpt-3.5-turbo",
    "tokens_used": 25,
    "created_at": "2024-12-01T10:30:00"
  }
]
```

#### GET /interactions/stats
Get statistics about LLM interactions

**Response:**
```json
{
  "total_interactions": 150,
  "total_tokens_used": 5230,
  "average_tokens_per_interaction": 35
}
```

### Railway Deployment with PostgreSQL

When deploying on Railway:

1. **Add PostgreSQL Add-on**
   - In Railway dashboard, click "Add Plugin"
   - Select "PostgreSQL"
   - Railway automatically injects `DATABASE_URL` environment variable

2. **Volume Configuration**
   - Railway handles persistent storage automatically with PostgreSQL add-on
   - No additional configuration needed

3. **Environment Variables**
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DATABASE_URL`: Auto-injected by Railway (PostgreSQL)

### Volume Mounting for Data Persistence

**Local Development (SQLite):**
```bash
# SQLite database is created in the working directory
# ./vapi_custom_llm.db
```

**Docker Compose (PostgreSQL):**
```yaml
volumes:
  postgres_data:
    # Named volume persists PostgreSQL data between container restarts
```

**Railway (PostgreSQL):**
- Data automatically persisted in Railway's managed PostgreSQL instance
- No manual volume configuration needed

### Backing Up Your Data

**SQLite:**
```bash
# Simple file copy backup
cp vapi_custom_llm.db vapi_custom_llm.db.backup
```

**PostgreSQL (local):**
```bash
# Using docker exec
docker exec postgres_container pg_dump -U vapi vapi_db > backup.sql

# Restore from backup
docker exec -i postgres_container psql -U vapi vapi_db < backup.sql
```

**Railway PostgreSQL:**
- Use Railway dashboard to manage backups
- PostgreSQL is automatically backed up by Railway
- See [Railway Backups Documentation](https://docs.railway.app/databases/postgresql)

## Troubleshooting

- **401 Unauthorized**: Check your API key authentication settings
- **500 Internal Server Error**: Verify your OpenAI API key is valid
- **Connection timeout**: Ensure ngrok tunnel is running and URL is correct
- **Database connection error**: Verify DATABASE_URL is correct in .env file
- **SQLAlchemy import errors**: Run `pip install -r requirements.txt` to ensure all dependencies are installed

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
