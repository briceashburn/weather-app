"""
Middleware configuration and setup for the Weather App.
"""

import logging
from fastapi import FastAPI
from .cors import setup_cors_middleware
from .logging import RequestLoggingMiddleware
from .timing import RequestTimingMiddleware

logger = logging.getLogger(__name__)

def setup_middleware(app: FastAPI) -> None:
    """
    Setup all middleware for the FastAPI application.
    
    Args:
        app: FastAPI application instance
    """
    logger.info("Setting up middleware...")
    
    # 1. Request Timing Middleware
    app.add_middleware(RequestTimingMiddleware)
    
    # 2. Request Logging Middleware
    app.add_middleware(RequestLoggingMiddleware)
    
    # 3. CORS Middleware (should be last to handle preflight requests)
    setup_cors_middleware(app)
    
    logger.info("All middleware configured successfully")

def get_middleware_info() -> dict:
    """
    Get information about configured middleware.
    
    Returns:
        Dictionary containing middleware information
    """
    return {
        "middleware": [
            {
                "name": "RequestTimingMiddleware",
                "description": "Measures and reports request processing times",
                "order": 1
            },
            {
                "name": "RequestLoggingMiddleware",
                "description": "Logs all incoming requests and responses",
                "order": 2
            }
        ]
    }
