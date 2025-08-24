from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

# Create a simple web server for the frontend
app = FastAPI(title="AI Chat Companion Web Server")

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
