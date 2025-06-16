from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import logging
import uvicorn
from .util.database import db_manager

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

@app.get("/health")
async def health_check():
    """
    Comprehensive health check endpoint including database connectivity
    """
    logger.info("Health check requested")
    health_status = {
        "status": "healthy",
        "app": "healthy",
        "database": None,
        "timestamp": None
    }
    
    # Add timestamp
    health_status["timestamp"] = datetime.now(timezone.utc).isoformat()
    
    # Check database health
    try:
        async with db_manager.get_connection() as connection:
            # Get database version
            version = await connection.fetchval("SELECT version()")
            health_status["database"] = {
                "status": "healthy",
                "version": version
            }
        logger.info("Database health check passed")
    except Exception as e:
        health_status["database"] = {
            "status": "error",
            "error": str(e)
        }
        health_status["status"] = "degraded"
        logger.error(f"Database health check failed: {e}")
    
    return health_status

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8080,
        log_level="info",
        use_colors=True,
        access_log=True
    )
