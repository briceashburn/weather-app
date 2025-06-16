# Weather App Middleware

Simple and focused middleware for the Weather App FastAPI application providing request timing and logging capabilities.

## Overview

This middleware system is designed to be lightweight and provide essential monitoring capabilities for your FastAPI application. It focuses on two key areas:

- **Performance Monitoring**: Track request processing times
- **Request Logging**: Monitor incoming requests and responses

## Available Middleware

### 1. Request Timing Middleware (`timing.py`)

- **Purpose**: Measures and reports request processing times for all calls
- **Features**:
  - High-precision timing using `time.perf_counter()`
  - Logs timing information for every request
  - Automatic timing header injection
- **Headers Added**:
  - `X-Process-Time`: Request processing time in seconds (6 decimal precision)
- **Use Case**: Performance monitoring, identifying slow endpoints

### 2. Request Logging Middleware (`logging.py`)

- **Purpose**: Simple request and response logging for monitoring and debugging
- **Features**:
  - Logs all incoming requests with client IP address
  - Logs response status codes
  - Error tracking and exception logging
  - Clean, readable log format
- **Use Case**: Request monitoring, debugging, audit trails

### 3. CORS Middleware (`cors.py`)

- **Purpose**: Handles Cross-Origin Resource Sharing for frontend integration
- **Features**:
  - Configured for localhost:3000 (React development server)
  - Supports all common HTTP methods (GET, POST, PUT, DELETE, OPTIONS)
  - Allows credentials and all headers
- **Use Case**: Frontend-backend communication during development

## Setup

The middleware is automatically configured when the FastAPI application starts:

```python
from app.middleware.config import setup_middleware
setup_middleware(app)
```

No additional configuration is required - the middleware works out of the box.

## Middleware Execution Order

The middleware executes in the following order (important for proper functionality):

1. **Request Timing** - Starts timing measurement
2. **Request Logging** - Logs incoming request details
3. **CORS** - Handles cross-origin requests (should be last)

## Usage

### Starting the Application

```bash
# Option 1: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# Option 2: Using VS Code task (if in VS Code workspace)
# Cmd+Shift+P -> "Tasks: Run Task" -> "Run FastAPI Server"

# Option 3: Running Python module directly
python3 -m app.main
```

### Monitoring

1. **Check logs**: Watch the console for timing and request information
2. **View application**: Visit `http://localhost:8080/` for the main interface
3. **Health check**: Visit `http://localhost:8080/health` for system status
4. **API docs**: Visit `http://localhost:8080/docs` for interactive documentation
5. **Inspect headers**: Use browser dev tools to see the `X-Process-Time` header

## Example Log Output

When making requests to your application, you'll see logs like:

```
2025-06-16 10:30:15 - app.main - INFO - Starting up Weather App...
2025-06-16 10:30:15 - app.main - INFO - Database connection pool created
INFO - Request timing middleware initialized
INFO - All middleware configured successfully
2025-06-16 10:30:20 - app.main - INFO - Home page accessed from 127.0.0.1
INFO - REQUEST: GET / from 127.0.0.1
INFO - TIMING: GET / processed in 0.002341s
INFO - RESPONSE: GET / Status: 200
2025-06-16 10:30:25 - app.main - INFO - Health check requested
2025-06-16 10:30:25 - app.main - INFO - Database health check passed
INFO - REQUEST: GET /health from 127.0.0.1
INFO - TIMING: GET /health processed in 0.015678s
INFO - RESPONSE: GET /health Status: 200
```

## Response Headers

Each response will include timing information:

```http
X-Process-Time: 0.002341
```

## Error Handling

If an error occurs during request processing, it will be logged:

```
ERROR - ERROR: GET /health Error: Database connection failed
2025-06-16 10:30:30 - app.main - ERROR - Database health check failed: connection timeout
```

## Benefits

- **Performance Insights**: See which endpoints are slow with precise timing
- **Request Monitoring**: Track all incoming traffic with client IP logging
- **Database Health**: Monitor PostgreSQL connectivity and performance
- **Debugging Aid**: Detailed error logging with timestamps and context
- **Zero Configuration**: Works immediately after installation
- **Lightweight**: Minimal performance overhead (~1-2ms per request)
- **Development Friendly**: CORS enabled for local React/frontend development
- **Production Ready**: Structured logging with proper error handling
