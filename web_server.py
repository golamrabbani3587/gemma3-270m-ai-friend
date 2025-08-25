from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import httpx
import os

# Create a simple web server for the frontend
app = FastAPI(title="AI Chat Companion Web Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_index():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Web server is running"}

@app.post("/chat")
async def proxy_chat(request: Request):
    """Proxy chat requests to the API server"""
    try:
        # Get the request body
        body = await request.json()
        
        # Determine API server URL
        api_url = os.environ.get('API_URL', 'http://localhost:8001')
        
        # Forward the request to the API server
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{api_url}/chat", json=body, timeout=30.0)
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)
