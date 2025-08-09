from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

# Request Models
class TextRequest(BaseModel):
    text: str = Field(..., description="Text to analyze", min_length=1, max_length=50000)

class KeywordRequest(BaseModel):
    text: str = Field(..., description="Text to extract keywords from", min_length=1, max_length=50000)
    max_keywords: int = Field(10, description="Maximum number of keywords to extract", ge=1, le=50)

class SummaryRequest(BaseModel):
    text: str = Field(..., description="Text to summarize", min_length=100, max_length=50000)
    max_length: int = Field(150, description="Maximum summary length", ge=50, le=500)
    min_length: int = Field(30, description="Minimum summary length", ge=10, le=200)

class ContentTypeEnum(str, Enum):
    blog_post = "blog_post"
    email = "email"
    social_media = "social_media"
    product_description = "product_description"
    article = "article"
    ad_copy = "ad_copy"

class ToneEnum(str, Enum):
    professional = "professional"
    casual = "casual"
    friendly = "friendly"
    formal = "formal"
    persuasive = "persuasive"
    creative = "creative"

class ContentRequest(BaseModel):
    prompt: str = Field(..., description="Content generation prompt", min_length=5, max_length=1000)
    content_type: ContentTypeEnum = Field(..., description="Type of content to generate")
    max_length: int = Field(300, description="Maximum content length", ge=50, le=2000)
    tone: ToneEnum = Field(ToneEnum.professional, description="Tone of the generated content")

class MetaRequest(BaseModel):
    content: str = Field(..., description="Content to generate meta description for", min_length=50, max_length=10000)
    max_length: int = Field(160, description="Maximum meta description length", ge=120, le=200)

# Response Models
class SentimentResponse(BaseModel):
    sentiment: str = Field(..., description="Overall sentiment (positive, negative, neutral)")
    confidence: float = Field(..., description="Confidence score (0-1)", ge=0, le=1)
    scores: Dict[str, float] = Field(..., description="Individual sentiment scores")

class LanguageResponse(BaseModel):
    language: str = Field(..., description="Detected language code (e.g., 'en', 'es', 'fr')")
    language_name: str = Field(..., description="Full language name")
    confidence: float = Field(..., description="Detection confidence (0-1)", ge=0, le=1)

class Keyword(BaseModel):
    word: str = Field(..., description="Extracted keyword")
    score: float = Field(..., description="Keyword importance score", ge=0, le=1)

class KeywordsResponse(BaseModel):
    keywords: List[Keyword] = Field(..., description="List of extracted keywords")
    total_keywords: int = Field(..., description="Total number of keywords found")

class SummaryResponse(BaseModel):
    summary: str = Field(..., description="Generated summary")
    original_length: int = Field(..., description="Original text length in characters")
    summary_length: int = Field(..., description="Summary length in characters")
    compression_ratio: float = Field(..., description="Compression ratio (summary/original)", ge=0, le=1)

class ContentResponse(BaseModel):
    content: str = Field(..., description="Generated content")
    content_type: str = Field(..., description="Type of content generated")
    word_count: int = Field(..., description="Word count of generated content")
    tone: str = Field(..., description="Tone used for generation")

class AIDetectionResponse(BaseModel):
    is_ai_generated: bool = Field(..., description="Whether text appears to be AI-generated")
    confidence: float = Field(..., description="Detection confidence (0-1)", ge=0, le=1)
    ai_probability: float = Field(..., description="Probability of being AI-generated (0-1)", ge=0, le=1)
    human_probability: float = Field(..., description="Probability of being human-written (0-1)", ge=0, le=1)

class ReadabilityResponse(BaseModel):
    flesch_kincaid_grade: float = Field(..., description="Flesch-Kincaid grade level")
    flesch_reading_ease: float = Field(..., description="Flesch reading ease score")
    gunning_fog_index: float = Field(..., description="Gunning Fog readability index")
    readability_level: str = Field(..., description="Overall readability level (easy, medium, hard)")
    average_sentence_length: float = Field(..., description="Average words per sentence")
    syllable_count: int = Field(..., description="Total syllable count")

class MetaDescriptionResponse(BaseModel):
    meta_description: str = Field(..., description="Generated meta description")
    length: int = Field(..., description="Meta description length")
    seo_score: float = Field(..., description="SEO optimization score (0-1)", ge=0, le=1)
    suggestions: List[str] = Field(..., description="SEO improvement suggestions")

# Enhanced Premium Response Models
class EnhancedAIDetectionResponse(BaseModel):
    is_ai_generated: bool = Field(..., description="Whether text appears to be AI-generated")
    confidence: float = Field(..., description="Detection confidence (0-1)", ge=0, le=1)
    ai_probability: float = Field(..., description="Probability of being AI-generated (0-1)", ge=0, le=1)
    human_probability: float = Field(..., description="Probability of being human-written (0-1)", ge=0, le=1)
    analysis_breakdown: Dict[str, float] = Field(..., description="Detailed analysis scores")

class TextComparisonRequest(BaseModel):
    text1: str = Field(..., description="First text for comparison", min_length=10, max_length=10000)
    text2: str = Field(..., description="Second text for comparison", min_length=10, max_length=10000)

class TextComparisonResponse(BaseModel):
    similarity_score: float = Field(..., description="Similarity score (0-1)", ge=0, le=1)
    semantic_similarity: float = Field(..., description="Semantic similarity (0-1)", ge=0, le=1)
    structural_similarity: float = Field(..., description="Structural similarity (0-1)", ge=0, le=1)
    common_keywords: List[str] = Field(..., description="Common keywords between texts")
    differences: List[str] = Field(..., description="Key differences identified")

class BatchRequest(BaseModel):
    texts: List[str] = Field(..., description="List of texts to analyze", min_items=2, max_items=100)
    analysis_type: str = Field(..., description="Type of analysis (sentiment, language, keywords)")

class BatchResponse(BaseModel):
    results: List[Dict[str, Any]] = Field(..., description="Analysis results for each text")
    summary: Dict[str, Any] = Field(..., description="Aggregate summary statistics")
    processing_time: float = Field(..., description="Total processing time in seconds")
