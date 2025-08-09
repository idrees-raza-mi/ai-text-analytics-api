from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
import time
from collections import defaultdict, deque
from dotenv import load_dotenv
import uvicorn
import hashlib
import json

# Load environment variables
load_dotenv()

# Import AI services
from services.text_analyzer import TextAnalyzer
from services.content_generator import ContentGenerator
from services.ai_detector import AIDetector
from models.responses import *

# Initialize FastAPI app
app = FastAPI(
    title="AI Text Analytics API",
    description="Comprehensive AI-powered text analysis and generation API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key authentication
API_KEY = os.getenv("API_KEY", "SecureAI2024_TextAnalytics_789xyz")
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(request: Request):
    # Check for RapidAPI headers first
    rapidapi_key = request.headers.get("X-RapidAPI-Key")
    rapidapi_host = request.headers.get("X-RapidAPI-Host")
    
    # If request comes from RapidAPI, validate differently
    if rapidapi_key and rapidapi_host:
        # RapidAPI requests are valid if they have the proper headers
        # RapidAPI handles the actual authentication
        return "rapidapi"
    
    # For direct requests, check our API key
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

# Initialize AI services
text_analyzer = TextAnalyzer()
content_generator = ContentGenerator()
ai_detector = AIDetector()

@app.get("/")
async def root():
    return {
        "message": "AI Text Analytics API",
        "version": "1.0.0",
        "endpoints": [
            "/analyze-sentiment",
            "/detect-language",
            "/extract-keywords",
            "/summarize-text",
            "/generate-content",
            "/detect-ai-content",
            "/analyze-readability",
            "/generate-meta-description"
        ]
    }

@app.post("/analyze-sentiment", response_model=SentimentResponse)
async def analyze_sentiment(
    text_request: TextRequest,
    api_key: str = Depends(verify_api_key)
):
    """Analyze sentiment of text (positive, negative, neutral)"""
    try:
        result = await text_analyzer.analyze_sentiment(text_request.text)
        return SentimentResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/detect-language", response_model=LanguageResponse)
async def detect_language(
    request: TextRequest,
    api_key: str = Depends(verify_api_key)
):
    """Detect the language of input text"""
    try:
        result = await text_analyzer.detect_language(request.text)
        return LanguageResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract-keywords", response_model=KeywordsResponse)
async def extract_keywords(
    request: KeywordRequest,
    api_key: str = Depends(verify_api_key)
):
    """Extract important keywords and phrases from text"""
    try:
        result = await text_analyzer.extract_keywords(
            request.text, 
            max_keywords=request.max_keywords
        )
        return KeywordsResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize-text", response_model=SummaryResponse)
async def summarize_text(
    request: SummaryRequest,
    api_key: str = Depends(verify_api_key)
):
    """Generate a summary of the input text"""
    try:
        result = await text_analyzer.summarize_text(
            request.text,
            max_length=request.max_length,
            min_length=request.min_length
        )
        return SummaryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-content", response_model=ContentResponse)
async def generate_content(
    request: ContentRequest,
    api_key: str = Depends(verify_api_key)
):
    """Generate content based on prompt and type"""
    try:
        result = await content_generator.generate_content(
            prompt=request.prompt,
            content_type=request.content_type,
            max_length=request.max_length,
            tone=request.tone
        )
        return ContentResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/detect-ai-content", response_model=AIDetectionResponse)
async def detect_ai_content(
    request: TextRequest,
    api_key: str = Depends(verify_api_key)
):
    """Detect if text was generated by AI"""
    try:
        result = await ai_detector.detect_ai_content(request.text)
        return AIDetectionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-readability", response_model=ReadabilityResponse)
async def analyze_readability(
    request: TextRequest,
    api_key: str = Depends(verify_api_key)
):
    """Analyze text readability and complexity"""
    try:
        result = await text_analyzer.analyze_readability(request.text)
        return ReadabilityResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-meta-description", response_model=MetaDescriptionResponse)
async def generate_meta_description(
    request: MetaRequest,
    api_key: str = Depends(verify_api_key)
):
    """Generate SEO meta description for content"""
    try:
        result = await content_generator.generate_meta_description(
            content=request.content,
            max_length=request.max_length
        )
        return MetaDescriptionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.get("/debug")
async def debug_info():
    return {
        "api_key_configured": bool(API_KEY and API_KEY != "your-secret-api-key-here"),
        "api_key_length": len(API_KEY) if API_KEY else 0,
        "api_key_starts_with": API_KEY[:10] + "..." if API_KEY and len(API_KEY) > 10 else "Not set",
        "environment": "production" if os.getenv("RAILWAY_ENVIRONMENT") else "local"
    }

if __name__ == "__main__":
    import os
    
    # Handle PORT environment variable properly
    try:
        port = int(os.getenv("PORT", "8000"))
    except (ValueError, TypeError):
        print(f"Warning: Invalid PORT value '{os.getenv('PORT')}', using default 8000")
        port = 8000
    
    print(f"Starting server on host 0.0.0.0 port {port}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Disable reload in production
    )
