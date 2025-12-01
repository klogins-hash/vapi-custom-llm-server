# Vapi Custom LLM FastAPI Server

A FastAPI server for integrating custom LLM models with Vapi.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the server:
```bash
python main.py
```

The server will be available at `http://localhost:8000`

## API Endpoints

- `POST /v1/message` - Send a message to the custom LLM
- `GET /health` - Health check endpoint

## Development

- FastAPI documentation available at `http://localhost:8000/docs`
- Swagger UI available at `http://localhost:8000/swagger-ui`

