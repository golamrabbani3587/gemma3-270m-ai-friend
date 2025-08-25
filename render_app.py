#!/usr/bin/env python3
"""
Combined app for Render deployment
Includes both API and web server functionality
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import json
from typing import Optional
import uvicorn
import os

# Initialize FastAPI app
app = FastAPI(
    title="AI Chat Companion",
    description="Combined API and web server for conversational AI with emotional support",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[list] = []

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

# Global model variables
model = None
tokenizer = None

def load_model():
    """Load the fine-tuned model"""
    global model, tokenizer
    
    print("Loading AI model...")
    
    # Load the fine-tuned model
    base_model_id = "google/gemma-3-270m-it"
    adapter_path = "./trained_model"
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(base_model_id)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Load base model
    model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        device_map="auto",
        torch_dtype=torch.float32,
        token=True
    )
    
    # Load the fine-tuned adapter
    model = PeftModel.from_pretrained(model, adapter_path)
    model.eval()
    
    print("Model loaded successfully!")

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    load_model()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_index():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "message": "AI Chat Companion is running!",
        "model_loaded": model is not None,
        "tokenizer_loaded": tokenizer is not None
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    try:
        if model is None or tokenizer is None:
            raise HTTPException(status_code=500, detail="Model not loaded")
        
        # Build conversation context
        conversation = ""
        
        # Add only the last conversation for context (showing last Q&A)
        if request.conversation_history and len(request.conversation_history) > 0:
            # Get the last conversation
            last_msg = request.conversation_history[-1]
            if isinstance(last_msg, dict):
                user_msg = last_msg.get("user", "")
                bot_msg = last_msg.get("assistant", "")
            else:
                user_msg, bot_msg = last_msg
            
            if user_msg and bot_msg:
                conversation += f"<start_of_turn>user\n{user_msg}<end_of_turn>\n"
                conversation += f"<start_of_turn>model\n{bot_msg}<end_of_turn>\n"
        
        # Add current message
        conversation += f"<start_of_turn>user\n{request.message}<end_of_turn>\n<start_of_turn>model\n"
        
        # Tokenize
        inputs = tokenizer(conversation, return_tensors="pt", truncation=True, max_length=1024)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        # Generate response
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.8,
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.1,
                pad_token_id=tokenizer.eos_token_id,
            )
        
        # Decode response
        full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the model's response
        if "<start_of_turn>model\n" in full_response:
            response = full_response.split("<start_of_turn>model\n")[-1].split("<end_of_turn>")[0].strip()
        else:
            # Fallback: try to extract just the model part
            response = full_response.split("model\n")[-1].strip()
        
        # Clean up any remaining special tokens and user text
        response = response.replace("<start_of_turn>", "").replace("<end_of_turn>", "").strip()
        response = response.replace("user\n", "").replace("model\n", "").strip()
        
        # If response still contains the original message, remove it
        if request.message in response:
            response = response.replace(request.message, "").strip()
        
        return ChatResponse(response=response)
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)
