"""
CORS (Cross-Origin Resource Sharing) middleware configuration for the FastAPI application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def setup_cors_middleware(app: FastAPI) -> None:
    """
    Setup CORS middleware for the FastAPI application.
    
    Args:
        app: FastAPI application instance
    """
        
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify actual origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    