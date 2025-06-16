# FastAPI Weather App

A modern FastAPI application starter template for a weather app with database connectivity, middleware, pretty-printed JSON responses, and a beautiful web interface.

## Features

- HTML home page with modern weather-themed UI
- **Pretty-printed JSON responses by default** - All API responses are formatted with proper indentation for better readability
- Comprehensive health check with database connectivity testing
- Database connection pooling with PostgreSQL
- **Enhanced request middleware with data response logging** - Logs response data for API endpoints
- Request timing and logging middleware
- CORS support for frontend development
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

### Option 2: Using VS Code Task

If you're using VS Code, you can run the preconfigured task:

- Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
- Type "Tasks: Run Task"
- Select "Run FastAPI Server"

### Option 3: Running the Python file directly

```bash
python3 -m app.main
```

## API Endpoints

Once the server is running, you can access:

- **Home page**: http://localhost:8080/

  - Returns: Beautiful HTML interface with weather app styling
  - Features modern glassmorphism design with gradient backgrounds

- **Health check**: http://localhost:8080/health
  - Returns: Comprehensive health status including database connectivity
  - **Note**: All JSON responses are now pretty-printed with proper indentation
  - Example response:
    ```json
    {
      "code": 200,
      "message": "All systems operational",
      "timestamp": "2025-06-16T10:30:00.123456Z",
      "data": {
        "app": "healthy",
        "database": {
          "status": "healthy",
          "version": "PostgreSQL 14.x..."
        }
      }
    }
    ```

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

## Development

The `--reload` flag enables auto-reloading during development, so the server will restart automatically when you make changes to the code.

### Database Setup

The application uses PostgreSQL with connection pooling. Configure your database connection using environment variables:

```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=weatherapp
DB_USER=devweatherappuser
DB_PASSWORD=your_password
DB_SCHEMA=weatherapp
```

### Middleware Features

The application includes several middleware components:

- **Request Timing**: Adds `X-Process-Time` headers to all responses
- **Enhanced Request Logging**:
  - Logs all incoming requests and responses with comprehensive details
  - **NEW**: Includes response data logging for API endpoints (JSON responses)
  - Automatically truncates large responses to prevent log bloat
  - Excludes HTML responses from data logging to keep logs clean
- **CORS**: Configured for localhost:3000 development

### JSON Response Formatting

**NEW**: All API responses are automatically formatted with pretty printing:

- Proper indentation (2 spaces)
- Clean separators for better readability
- UTF-8 encoding support
- Improved developer experience when testing APIs

### Project Structure

This is a starter template that includes:

- Database connectivity with PostgreSQL
- Modern middleware system with enhanced logging capabilities
- **Pretty-printed JSON responses for better API development**
- **Response data logging in middleware for debugging and monitoring**
- Beautiful frontend interface
- Comprehensive health monitoring
- Ready for weather API integration
