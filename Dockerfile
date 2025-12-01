FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory for SQLite with proper permissions
# This directory will be used for SQLite database when mounted
RUN mkdir -p /app/data && chmod 755 /app/data

# Expose port (Railway will override with $PORT)
EXPOSE 8000

# Run migrations and start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
