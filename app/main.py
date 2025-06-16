from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Create FastAPI instance
app = FastAPI(
    title="Weather App API",
    description="A simple weather application with FastAPI",
    version="1.0.0"
)

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Home page endpoint that returns HTML content from template
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
