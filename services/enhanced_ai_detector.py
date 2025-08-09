"""
Enhanced AI Content Detection Service
More sophisticated algorithms for better accuracy
"""

import asyncio
import re
import math
from typing import Dict, List, Any, Tuple
from textblob import TextBlob
from collections import Counter
import numpy as np


class EnhancedAIDetector:
    def __init__(self):
        # Enhanced AI patterns with weights
        self.ai_patterns = [
            # Strong AI indicators (high weight)
            (r'\b(?:as an AI|I don\'t have personal|I cannot|I\'m not able to|I don\'t actually)\b', 0.9),
            (r'\b(?:furthermore|moreover|additionally|consequently|therefore)\b.*?\b(?:furthermore|moreover|additionally|consequently|therefore)\b', 0.8),
            (r'\b(?:it\'s important to note|it\'s worth mentioning|keep in mind)\b', 0.7),
            (r'\b(?:comprehensive guide|step-by-step|in-depth analysis)\b', 0.6),
            
            # Medium AI indicators  
            (r'\b(?:cutting-edge|state-of-the-art|revolutionary|innovative)\b.*?\b(?:cutting-edge|state-of-the-art|revolutionary|innovative)\b', 0.6),
            (r'\b(?:optimize|streamline|enhance|facilitate|leverage)\b.*?\b(?:optimize|streamline|enhance|facilitate|leverage)\b', 0.5),
            (r'\b(?:in conclusion|to summarize|in summary)\b', 0.5),
            (r'\b(?:paradigm shift|game-changer|unlock potential)\b', 0.6),
            
            # Subtle AI patterns
            (r'^\d+\.\s', 0.3),  # Numbered lists
            (r'\b(?:firstly|secondly|thirdly|finally)\b', 0.4),
            (r'\b(?:methodology|framework|systematic|strategic)\b', 0.3),
        ]
        
        # Human writing indicators (negative weights)
        self.human_patterns = [
            (r'\b(?:I think|I believe|in my opinion|personally|from my experience)\b', -0.4),
            (r'\b(?:um|uh|well|you know|like|actually)\b', -0.6),
            (r'[.!?]{2,}', -0.3),  # Multiple punctuation
            (r'\b(?:lol|haha|omg|wtf|tbh|imo)\b', -0.7),  # Internet slang
            (r'[\'\"]\w+[\'\"]\s', -0.2),  # Quotes with words
            (r'\b(?:kinda|sorta|gonna|wanna)\b', -0.5),  # Informal contractions
            (r'(?::\)|:\(|:D|;\)|xD)', -0.6),  # Emoticons
        ]
        
        # Common AI writing structures
        self.ai_structures = [
            r'\b\d+\.\s+\w+.*?(?=\n\d+\.|\n\n|\Z)',  # Numbered lists
            r'(?:First|Second|Third|Fourth|Fifth|Finally),?\s+',  # Sequential markers
            r'In\s+(?:conclusion|summary|essence),?\s+',  # Conclusion starters
        ]

    async def detect_ai_content(self, text: str) -> Dict[str, Any]:
        """Enhanced AI content detection with multiple algorithms"""
        try:
            # Run multiple detection algorithms
            pattern_score = self._pattern_analysis(text)
            linguistic_score = await self._linguistic_analysis(text)
            structural_score = self._structural_analysis(text)
            
            # Weighted combination of scores
            ai_probability = (
                pattern_score * 0.4 +
                linguistic_score * 0.4 +
                structural_score * 0.2
            )
            
            # Normalize to 0-1 range
            ai_probability = max(0.0, min(1.0, ai_probability))
            
            # Determine confidence based on consensus between methods
            scores = [pattern_score, linguistic_score, structural_score]
            confidence = 1.0 - (np.std(scores) / np.mean(scores)) if np.mean(scores) > 0 else 0.5
            confidence = max(0.5, min(0.95, confidence))
            
            # Classification threshold
            is_ai_generated = ai_probability > 0.6
            human_probability = 1.0 - ai_probability
            
            return {
                "is_ai_generated": is_ai_generated,
                "confidence": round(confidence, 3),
                "ai_probability": round(ai_probability, 3),
                "human_probability": round(human_probability, 3),
                "analysis_breakdown": {
                    "pattern_score": round(pattern_score, 3),
                    "linguistic_score": round(linguistic_score, 3),
                    "structural_score": round(structural_score, 3)
                }
            }
            
        except Exception as e:
            # Fallback to neutral
            return {
                "is_ai_generated": False,
                "confidence": 0.5,
                "ai_probability": 0.5,
                "human_probability": 0.5,
                "analysis_breakdown": {
                    "pattern_score": 0.5,
                    "linguistic_score": 0.5,
                    "structural_score": 0.5
                }
            }

    def _pattern_analysis(self, text: str) -> float:
        """Pattern-based AI detection"""
        score = 0.5  # Neutral starting point
        text_lower = text.lower()
        
        # Check AI patterns
        for pattern, weight in self.ai_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE | re.MULTILINE))
            if matches > 0:
                score += (matches * weight * 0.1)
        
        # Check human patterns
        for pattern, weight in self.human_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            if matches > 0:
                score += (matches * weight * 0.1)
        
        return max(0.0, min(1.0, score))

    async def _linguistic_analysis(self, text: str) -> float:
        """Linguistic feature analysis"""
        try:
            blob = TextBlob(text)
            sentences = list(blob.sentences)
            words = blob.words
            
            if not sentences or not words:
                return 0.5
            
            features = {}
            
            # Sentence length consistency (AI tends to be more consistent)
            sentence_lengths = [len(str(s).split()) for s in sentences]
            if len(sentence_lengths) > 1:
                cv = np.std(sentence_lengths) / np.mean(sentence_lengths)
                features['length_consistency'] = 1.0 - min(1.0, cv)  # Lower variation = more AI-like
            else:
                features['length_consistency'] = 0.5
            
            # Vocabulary sophistication
            word_lengths = [len(word) for word in words]
            avg_word_length = np.mean(word_lengths) if word_lengths else 0
            features['vocabulary_sophistication'] = min(1.0, (avg_word_length - 3) / 5)  # Normalize
            
            # Repetition patterns
            word_freq = Counter(word.lower() for word in words)
            max_freq = max(word_freq.values()) if word_freq else 0
            features['word_repetition'] = min(1.0, max_freq / len(words)) if words else 0
            
            # Sentence complexity variation
            complexity_scores = []
            for sentence in sentences:
                words_in_sent = str(sentence).split()
                commas = str(sentence).count(',')
                complex_score = (len(words_in_sent) + commas * 2) / 20  # Normalize
                complexity_scores.append(min(1.0, complex_score))
            
            if complexity_scores:
                features['complexity_variation'] = 1.0 - np.std(complexity_scores)
            else:
                features['complexity_variation'] = 0.5
            
            # Combine features
            score = np.mean(list(features.values()))
            return max(0.0, min(1.0, score))
            
        except Exception:
            return 0.5

    def _structural_analysis(self, text: str) -> float:
        """Structural analysis of text organization"""
        score = 0.5  # Neutral start
        
        # Check for AI-typical structures
        structure_indicators = 0
        
        # Numbered lists
        numbered_items = len(re.findall(r'^\s*\d+\.', text, re.MULTILINE))
        if numbered_items >= 3:
            structure_indicators += 0.3
        
        # Sequential markers
        sequential_markers = len(re.findall(
            r'\b(?:first|second|third|fourth|fifth|finally|in conclusion)\b', 
            text, re.IGNORECASE
        ))
        if sequential_markers >= 2:
            structure_indicators += 0.2
        
        # Paragraph consistency
        paragraphs = text.split('\n\n')
        if len(paragraphs) > 1:
            para_lengths = [len(p.split()) for p in paragraphs if p.strip()]
            if para_lengths:
                cv = np.std(para_lengths) / np.mean(para_lengths)
                if cv < 0.5:  # Very consistent paragraph lengths
                    structure_indicators += 0.2
        
        # Transition word density
        transitions = re.findall(
            r'\b(?:however|therefore|furthermore|moreover|additionally|consequently|nevertheless)\b',
            text, re.IGNORECASE
        )
        word_count = len(text.split())
        if word_count > 0:
            transition_density = len(transitions) / word_count
            if transition_density > 0.02:  # High transition word usage
                structure_indicators += 0.3
        
        return min(1.0, score + structure_indicators)

    def get_detailed_analysis(self, text: str) -> Dict[str, Any]:
        """Get detailed breakdown of AI detection analysis"""
        analysis = {
            "text_length": len(text),
            "word_count": len(text.split()),
            "sentence_count": len(TextBlob(text).sentences),
            "ai_indicators": [],
            "human_indicators": [],
            "structural_features": {}
        }
        
        # Find specific AI indicators
        for pattern, weight in self.ai_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                analysis["ai_indicators"].append({
                    "pattern": pattern,
                    "matches": matches,
                    "weight": weight,
                    "count": len(matches)
                })
        
        # Find specific human indicators
        for pattern, weight in self.human_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                analysis["human_indicators"].append({
                    "pattern": pattern,
                    "matches": matches,
                    "weight": weight,
                    "count": len(matches)
                })
        
        return analysis
