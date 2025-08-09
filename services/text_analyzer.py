import asyncio
import re
from textblob import TextBlob
from langdetect import detect, DetectorFactory
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from typing import Dict, List, Any

# Set seed for consistent language detection
DetectorFactory.seed = 0

class TextAnalyzer:
    def __init__(self):
        # Initialize without heavy models for now
        self.sentiment_analyzer = None
        self.summarizer = None
        
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using TextBlob"""
        # TextBlob analysis
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Determine sentiment
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
            
        # Create confidence score based on polarity strength and subjectivity
        confidence = min(0.95, abs(polarity) * 0.8 + subjectivity * 0.2)
        
        # Calculate individual scores
        if sentiment == "positive":
            pos_score = (polarity + 1) / 2  # Normalize to 0-1
            neg_score = 0.0
            neu_score = 1 - pos_score
        elif sentiment == "negative":
            neg_score = abs(polarity)
            pos_score = 0.0
            neu_score = 1 - neg_score
        else:
            neu_score = 1 - abs(polarity)
            pos_score = max(0, polarity) * 0.5
            neg_score = max(0, -polarity) * 0.5
        
        scores = {
            "positive": round(pos_score, 3),
            "negative": round(neg_score, 3),
            "neutral": round(neu_score, 3),
            "textblob_polarity": round(polarity, 3),
            "textblob_subjectivity": round(subjectivity, 3)
        }
        
        return {
            "sentiment": sentiment,
            "confidence": round(confidence, 3),
            "scores": scores
        }
    
    async def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect language of the text"""
        try:
            # Clean text
            clean_text = re.sub(r'[^\w\s]', '', text.lower())
            
            if len(clean_text.strip()) < 3:
                return {
                    "language": "unknown",
                    "language_name": "Unknown",
                    "confidence": 0.0
                }
            
            detected_lang = detect(text)
            
            # Language code to name mapping
            lang_names = {
                'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
                'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
                'ko': 'Korean', 'zh': 'Chinese', 'ar': 'Arabic', 'hi': 'Hindi',
                'nl': 'Dutch', 'sv': 'Swedish', 'da': 'Danish', 'no': 'Norwegian',
                'fi': 'Finnish', 'tr': 'Turkish', 'pl': 'Polish', 'cs': 'Czech'
            }
            
            language_name = lang_names.get(detected_lang, detected_lang.capitalize())
            
            # Calculate confidence based on text length
            confidence = min(0.9, 0.5 + (len(text) / 1000))
            
            return {
                "language": detected_lang,
                "language_name": language_name,
                "confidence": confidence
            }
            
        except Exception as e:
            return {
                "language": "unknown",
                "language_name": "Unknown",
                "confidence": 0.0
            }
    
    async def extract_keywords(self, text: str, max_keywords: int = 10) -> Dict[str, Any]:
        """Extract keywords using TF-IDF"""
        # Clean and preprocess text
        clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
        sentences = [clean_text]
        
        # Use TF-IDF for keyword extraction
        vectorizer = TfidfVectorizer(
            max_features=max_keywords * 2,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform(sentences)
            feature_names = vectorizer.get_feature_names_out()
            tfidf_scores = tfidf_matrix.toarray()[0]
            
            # Create keyword list with scores
            keyword_scores = list(zip(feature_names, tfidf_scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            keywords = [
                {"word": word, "score": float(score)}
                for word, score in keyword_scores[:max_keywords]
                if score > 0
            ]
            
            return {
                "keywords": keywords,
                "total_keywords": len(keywords)
            }
            
        except Exception as e:
            return {
                "keywords": [],
                "total_keywords": 0
            }
    
    async def summarize_text(self, text: str, max_length: int = 150, min_length: int = 30) -> Dict[str, Any]:
        """Summarize text using simple extractive method"""
        try:
            # Simple extractive summary
            sentences = text.split('. ')
            
            # If text is short, return it as is
            if len(text) <= max_length:
                return {
                    "summary": text.strip(),
                    "original_length": len(text),
                    "summary_length": len(text),
                    "compression_ratio": 1.0
                }
            
            # Take first few sentences that fit within max_length
            summary_sentences = []
            current_length = 0
            
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                    
                # Add period if missing
                if not sentence.endswith('.'):
                    sentence += '.'
                    
                if current_length + len(sentence) + 1 <= max_length:
                    summary_sentences.append(sentence)
                    current_length += len(sentence) + 1
                else:
                    break
            
            # If no sentences fit, truncate first sentence
            if not summary_sentences and sentences:
                first_sentence = sentences[0].strip()
                if len(first_sentence) > max_length:
                    summary = first_sentence[:max_length-3] + '...'
                else:
                    summary = first_sentence + '.'
            else:
                summary = ' '.join(summary_sentences)
            
            # Ensure minimum length
            if len(summary) < min_length and len(text) > min_length:
                words = text.split()
                word_summary = []
                current_length = 0
                
                for word in words:
                    if current_length + len(word) + 1 <= max_length:
                        word_summary.append(word)
                        current_length += len(word) + 1
                    else:
                        break
                        
                summary = ' '.join(word_summary) + '...'
                
            return {
                "summary": summary,
                "original_length": len(text),
                "summary_length": len(summary),
                "compression_ratio": len(summary) / len(text) if len(text) > 0 else 0
            }
            
        except Exception as e:
            # Final fallback
            summary = text[:max_length] + '...' if len(text) > max_length else text
            return {
                "summary": summary,
                "original_length": len(text),
                "summary_length": len(summary),
                "compression_ratio": len(summary) / len(text) if len(text) > 0 else 0
            }
    
    async def analyze_readability(self, text: str) -> Dict[str, Any]:
        """Analyze text readability using various metrics"""
        try:
            blob = TextBlob(text)
            sentences = blob.sentences
            words = blob.words
            
            if not sentences or not words:
                return self._default_readability_response()
            
            # Basic counts
            sentence_count = len(sentences)
            word_count = len(words)
            syllable_count = sum(self._count_syllables(str(word)) for word in words)
            
            if sentence_count == 0 or word_count == 0:
                return self._default_readability_response()
            
            # Calculate metrics
            avg_sentence_length = word_count / sentence_count
            avg_syllables_per_word = syllable_count / word_count
            
            # Flesch Reading Ease
            flesch_reading_ease = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
            
            # Flesch-Kincaid Grade Level
            flesch_kincaid_grade = 0.39 * avg_sentence_length + 11.8 * avg_syllables_per_word - 15.59
            
            # Gunning Fog Index (simplified)
            complex_words = sum(1 for word in words if self._count_syllables(str(word)) >= 3)
            gunning_fog = 0.4 * (avg_sentence_length + 100 * (complex_words / word_count))
            
            # Determine readability level
            if flesch_reading_ease >= 60:
                readability_level = "easy"
            elif flesch_reading_ease >= 30:
                readability_level = "medium"
            else:
                readability_level = "hard"
            
            return {
                "flesch_kincaid_grade": round(flesch_kincaid_grade, 2),
                "flesch_reading_ease": round(flesch_reading_ease, 2),
                "gunning_fog_index": round(gunning_fog, 2),
                "readability_level": readability_level,
                "average_sentence_length": round(avg_sentence_length, 2),
                "syllable_count": syllable_count
            }
            
        except Exception as e:
            return self._default_readability_response()
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word"""
        word = word.lower().strip()
        if not word:
            return 1
            
        syllables = 0
        vowels = "aeiouy"
        
        if word[0] in vowels:
            syllables += 1
        
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                syllables += 1
        
        if word.endswith("e") and syllables > 1:
            syllables -= 1
        
        if syllables == 0:
            syllables = 1
            
        return syllables
    
    def _default_readability_response(self) -> Dict[str, Any]:
        """Default response for readability analysis errors"""
        return {
            "flesch_kincaid_grade": 0.0,
            "flesch_reading_ease": 0.0,
            "gunning_fog_index": 0.0,
            "readability_level": "unknown",
            "average_sentence_length": 0.0,
            "syllable_count": 0
        }
