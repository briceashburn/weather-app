"""
Request logging middleware for tracking and monitoring HTTP requests.
"""

import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all incoming HTTP requests with basic information.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and log relevant information.
        
        Args:
            request: The incoming HTTP request
            call_next: The next middleware/route handler in the chain
            
        Returns:
            The HTTP response
        """
        # Extract client information
        client_host = getattr(request.client, 'host', 'unknown') if request.client else 'unknown'
        
        # Log request details
        logger.info(
            f"REQUEST: {request.method} {request.url.path} from {client_host}"
        )
        
        # Process the request
        try:
            response = await call_next(request)
            
            # Log response details
            logger.info(
                f"RESPONSE: {request.method} {request.url.path} Status: {response.status_code}"
            )
            
            return response
            
        except Exception as e:
            logger.error(
                f"ERROR: {request.method} {request.url.path} Error: {str(e)}"
            )
            raise
