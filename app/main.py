from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from .util.database import db_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle events"""
    # Startup
    await db_manager.create_pool()
    yield
    # Shutdown
    await db_manager.close_pool()

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
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """
    Comprehensive health check endpoint including database connectivity
    """
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
    except Exception as e:
        health_status["database"] = {
            "status": "error",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    return health_status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
