"""
Middleware configuration and setup for the Weather App.
"""

import logging
from fastapi import FastAPI
from .cors import setup_cors_middleware
from .request_middleware import RequestMiddleware

logger = logging.getLogger(__name__)

def setup_middleware(app: FastAPI) -> None:
    """
    Setup all middleware for the FastAPI application.
    
    Args:
        app: FastAPI application instance
    """
    logger.info("Setting up middleware...")
    
    # 1. Combined Request Middleware (handles both logging and timing)
    app.add_middleware(RequestMiddleware)
    
    # 2. CORS Middleware (should be last to handle preflight requests)
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
                "name": "RequestMiddleware",
                "description": "Combined middleware for request logging and timing",
                "features": [
                    "Request/response logging",
                    "Performance timing measurement",
                    "Error tracking with timing",
                    "Client information logging"
                ],
                "order": 1
            }
        ]
    }
