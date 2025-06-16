from fastapi import FastAPI

# Create FastAPI instance
app = FastAPI(
    title="Weather App API",
    description="A simple FastAPI Hello World application",
    version="1.0.0"
)

@app.get("/")
async def read_root():
    """
    Root endpoint that returns a hello world message
    """
    return {"message": "Hello World from FastAPI!"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
