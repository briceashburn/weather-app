"""
Combined request middleware for logging and timing HTTP requests.
"""

import time
import logging
import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable

logger = logging.getLogger(__name__)

class RequestMiddleware(BaseHTTPMiddleware):
    """
    Combined middleware to log all incoming HTTP requests with timing information.
    Provides comprehensive request/response logging with performance metrics and response data.
    """
    
    def __init__(self, app):
        """
        Initialize the request middleware.
        
        Args:
            app: The ASGI application
        """
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request, measure timing, and log comprehensive information including response data.
        
        Args:
            request: The incoming HTTP request
            call_next: The next middleware/route handler in the chain
            
        Returns:
            The HTTP response with timing headers added
        """
        start_time = time.perf_counter()
        
        # Extract client information
        client_host = getattr(request.client, 'host', 'unknown') if request.client else 'unknown'
        
        # Process the request
        try:
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.perf_counter() - start_time
            
            # Add timing header
            response.headers["X-Process-Time"] = f"{process_time:.6f}"
            
            # Capture response data for JSON responses
            response_data_log = await self._capture_and_log_response(response)
            
            # Log single comprehensive entry with all request info and response data
            logger.info(
                f"{request.method} {request.url.path} | "
                f"Status: {response.status_code} | "
                f"Time: {process_time:.6f}s | "
                f"Client: {client_host}"
                f"{response_data_log}"
            )
            
            return response
            
        except Exception as e:
            # Calculate processing time even for errors
            process_time = time.perf_counter() - start_time
            
            # Log error with timing information
            logger.error(
                f"ERROR: {request.method} {request.url.path} | "
                f"Error: {str(e)} | "
                f"Time: {process_time:.6f}s | "
                f"Client: {client_host}"
            )
            raise
    
    async def _capture_and_log_response(self, response: Response) -> str:
        """
        Capture response data by reading the response body.
        
        Args:
            response: The response object
            
        Returns:
            Formatted string for logging
        """
        content_type = response.headers.get("content-type", "")
        
        # Only process JSON responses
        if not content_type.startswith("application/json"):
            return ""
        
        try:
            # Read the response body
            response_body = b""
            async for chunk in response.body_iterator:
                if isinstance(chunk, bytes):
                    response_body += chunk
                elif isinstance(chunk, str):
                    response_body += chunk.encode('utf-8')
            
            # Decode the body
            body_str = response_body.decode('utf-8')
            
            # Parse and pretty-format the JSON
            response_data = json.loads(body_str)
            pretty_json = json.dumps(response_data, indent=2, ensure_ascii=False)
            
            # Create a new response with the same body
            async def new_body_iterator():
                yield response_body
            
            response.body_iterator = new_body_iterator()
            
            # Format for logging (truncate if too long)
            if len(pretty_json) > 500:
                return f" | Response:\n{pretty_json[:500]}..."
            else:
                return f" | Response:\n{pretty_json}"
                
        except Exception as e:
            # If we can't capture the body, create a new empty iterator
            async def empty_iterator():
                yield b""
            response.body_iterator = empty_iterator()
            return f" | Response: [Error reading body: {str(e)}]"
