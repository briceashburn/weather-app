# FastAPI Hello World Weather App

A simple FastAPI application that serves as a "Hello World" example for a weather app.

## Features

- Root endpoint that returns a hello world message
- Personalized greeting endpoint
- Health check endpoint
- Auto-generated interactive API documentation

## Installation

1. Install the required dependencies:

```bash
pip3 install -r requirements.txt
```

## Running the Application

### Option 1: Using uvicorn directly

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### Option 2: Running the Python file directly

```bash
python3 -m app.main
```

## API Endpoints

Once the server is running, you can access:

- **Root endpoint**: http://localhost:8080/

  - Returns: `{"message": "Hello World from FastAPI!"}`

- **Personalized greeting**: http://localhost:8080/hello/{name}

  - Example: http://localhost:8080/hello/Brice
  - Returns: `{"message": "Hello Brice!"}`

- **Health check**: http://localhost:8080/health
  - Returns: `{"status": "healthy"}`

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

## Development

The `--reload` flag enables auto-reloading during development, so the server will restart automatically when you make changes to the code.
