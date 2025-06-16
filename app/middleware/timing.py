"""
Request timing middleware for measuring and reporting request processing times.
"""

import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable

logger = logging.getLogger(__name__)

class RequestTimingMiddleware(BaseHTTPMiddleware):
    """
    Simple middleware to measure and report request processing times for all calls.
    """
    
    def __init__(self, app):
        """
        Initialize the timing middleware.
        
        Args:
            app: The ASGI application
        """
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Measure request processing time and add timing headers.
        
        Args:
            request: The incoming HTTP request
            call_next: The next middleware/route handler in the chain
            
        Returns:
            The HTTP response with timing headers added
        """
        start_time = time.perf_counter()
        
        # Process the request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.perf_counter() - start_time
        
        # Add timing header
        response.headers["X-Process-Time"] = f"{process_time:.6f}"
        
        # Log the timing for all requests
        logger.info(
            f"TIMING: {request.method} {request.url.path} "
            f"processed in {process_time:.6f}s"
        )
        
        return response
