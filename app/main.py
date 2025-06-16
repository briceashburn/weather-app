from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import logging
import uvicorn
from .util.database import db_manager
from .models.api_response import ApiResponse

# Configure colorized logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Get logger for this module
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle events"""
    # Startup
    logger.info("Starting up Weather App...")
    await db_manager.create_pool()
    logger.info("Database connection pool created")
    yield
    # Shutdown
    logger.info("Shutting down Weather App...")
    await db_manager.close_pool()
    logger.info("Database connection pool closed")

# Create FastAPI instance
app = FastAPI(
    title="Weather App API",
    description="A simple weather application with FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

# Setup templates
templates = Jinja2Templates(directory="app")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Home page endpoint that returns HTML content from template
    """
    logger.info(f"Home page accessed from {request.client.host}")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health", response_model=ApiResponse)
async def health_check():
    """
    Comprehensive health check endpoint including database connectivity
    """
    logger.info("Health check requested")
    health_data = {
        "app": "healthy",
        "database": None
    }
    
    # Check database health
    try:
        async with db_manager.get_connection() as connection:
            # Get database version
            version = await connection.fetchval("SELECT version()")
            health_data["database"] = {
                "status": "healthy",
                "version": version
            }
        logger.info("Database health check passed")
        return ApiResponse.success(
            data=health_data,
            message="All systems operational"
        )
    except Exception as e:
        health_data["database"] = {
            "status": "error",
            "error": str(e)
        }
        logger.error(f"Database health check failed: {e}")
        return ApiResponse.error(
            message="System degraded - database connection issues",
            code=503,
            data=health_data
        )

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8080,
        log_level="info",
        use_colors=True,
        access_log=True
    )
