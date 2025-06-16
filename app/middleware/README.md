# Weather App Middleware

Efficient and comprehensive middleware for the Weather App FastAPI application providing combined request logging and timing capabilities.

## Overview

This middleware system is designed to be lightweight and provide essential monitoring capabilities for your FastAPI application. It combines performance monitoring and request logging into a single, efficient middleware that reduces overhead while providing comprehensive request tracking.

- **Combined Performance & Logging**: Single middleware handles both timing and logging
- **Comprehensive Request Tracking**: Monitor all requests with detailed information
- **Error Handling**: Track errors with timing information

## Available Middleware

### 1. Request Middleware (`request_middleware.py`)

- **Purpose**: Combined middleware for comprehensive request/response logging with performance timing
- **Features**:
  - High-precision timing using `time.perf_counter()`
  - Comprehensive request logging with client information
  - Response status code tracking
  - Error logging with timing information
  - Automatic timing header injection
  - Single middleware reduces processing overhead
- **Headers Added**:
  - `X-Process-Time`: Request processing time in seconds (6 decimal precision)
- **Log Format**:
  - Request: `REQUEST: {method} {path} from {client_ip}`
  - Response: `RESPONSE: {method} {path} Status: {status} Time: {time}s Client: {client_ip}`
  - Error: `ERROR: {method} {path} Error: {error} Time: {time}s Client: {client_ip}`
- **Use Case**: Complete request monitoring, performance analysis, debugging, audit trails

### 2. CORS Middleware (`cors.py`)

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

1. **Request Middleware** - Combined logging and timing (handles both request logging and response timing)
2. **CORS** - Handles cross-origin requests (should be last)

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
INFO - All middleware configured successfully
2025-06-16 10:30:20 - app.main - INFO - Home page accessed from 127.0.0.1
INFO:app.middleware.request_middleware:GET / | Status: 200 | Time: 0.002341s | Client: 127.0.0.1
2025-06-16 10:30:25 - app.main - INFO - Health check requested
2025-06-16 10:30:25 - app.main - INFO - Database health check passed
INFO:app.middleware.request_middleware:GET /health | Status: 200 | Time: 0.015678s | Client: 127.0.0.1
```

## Response Headers

Each response will include timing information:

```http
X-Process-Time: 0.002341
```

## Error Handling

If an error occurs during request processing, it will be logged with timing information:

```
ERROR:app.middleware.request_middleware:ERROR: GET /health | Error: Database connection failed | Time: 0.001234s | Client: 127.0.0.1
2025-06-16 10:30:30 - app.main - ERROR - Database health check failed: connection timeout
```

## Benefits

- **Enhanced Performance Insights**: Combined timing and logging provides complete request lifecycle visibility
- **Comprehensive Request Monitoring**: Track all incoming traffic with client IP, status, and timing in one log entry
- **Efficient Processing**: Single middleware reduces overhead compared to separate timing and logging middleware
- **Database Health**: Monitor PostgreSQL connectivity and performance
- **Enhanced Debugging**: Detailed error logging with timestamps, timing, and context
- **Zero Configuration**: Works immediately after installation
- **Lightweight**: Minimal performance overhead with combined processing
- **Development Friendly**: CORS enabled for local React/frontend development
- **Production Ready**: Structured logging with proper error handling and comprehensive metrics
