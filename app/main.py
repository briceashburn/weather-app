from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import logging
import uvicorn
import json
from .util.database import db_manager
from .models.api_response import ApiResponse
from .middleware.config import setup_middleware

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
    lifespan=lifespan,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure JSON response formatting for pretty printing
# Override default JSON response to enable pretty printing
class PrettyJSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        return json.dumps(
            jsonable_encoder(content),
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            separators=(",", ": "),
        ).encode("utf-8")

# Set as default response class
app.response_class = PrettyJSONResponse

# Setup middleware
setup_middleware(app)

# Setup templates
templates = Jinja2Templates(directory="app")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Home page endpoint that returns HTML content from template
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health", response_model=ApiResponse)
async def health_check():
    """
    Comprehensive health check endpoint including database connectivity
    """
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
