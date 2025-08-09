import asyncio
import re
from typing import Dict, List, Any
from textblob import TextBlob
import numpy as np

class AIDetector:
    def __init__(self):
        # Patterns that suggest AI-generated content
        self.ai_patterns = [
            # Common AI phrases
            r'\b(?:as an AI|I don\'t have personal|I cannot|I\'m not able to|I don\'t actually)\b',
            r'\b(?:furthermore|moreover|additionally|consequently|therefore)\b',
            r'\b(?:it\'s important to note|it\'s worth mentioning|keep in mind)\b',
            r'\b(?:comprehensive guide|step-by-step|in-depth analysis)\b',
            r'\b(?:cutting-edge|state-of-the-art|revolutionary|innovative)\b',
            
            # Repetitive patterns
            r'(\w+)\s+\1',  # Repeated words
            r'\b(?:optimize|streamline|enhance|facilitate|leverage)\b.*?\b(?:optimize|streamline|enhance|facilitate|leverage)\b',
            
            # Generic conclusions
            r'\b(?:in conclusion|to summarize|in summary)\b',
            r'\b(?:game-changer|paradigm shift|unlock potential)\b'
        ]
        
        # Human writing indicators
        self.human_patterns = [
            r'\b(?:I think|I believe|in my opinion|personally|from my experience)\b',
            r'\b(?:um|uh|well|you know|like|actually)\b',
            r'[.!?]{2,}',  # Multiple punctuation
            r'\b(?:lol|haha|omg|wtf)\b',  # Internet slang
            r'[\'\"]\w+[\'\"]\s',  # Quotes with words
        ]
    
    async def detect_ai_content(self, text: str) -> Dict[str, Any]:
        """Detect if content appears to be AI-generated"""
        try:
            # Calculate various features
            features = self._extract_features(text)
            
            # Calculate AI probability based on features
            ai_probability = self._calculate_ai_probability(features, text)
            
            # Determine if likely AI-generated (threshold = 0.6)
            is_ai_generated = ai_probability > 0.6
            
            # Calculate confidence based on feature strength
            confidence = min(0.95, 0.5 + abs(ai_probability - 0.5))
            
            human_probability = 1.0 - ai_probability
            
            return {
                "is_ai_generated": is_ai_generated,
                "confidence": confidence,
                "ai_probability": ai_probability,
                "human_probability": human_probability
            }
            
        except Exception as e:
            # Default to neutral prediction on error
            return {
                "is_ai_generated": False,
                "confidence": 0.5,
                "ai_probability": 0.5,
                "human_probability": 0.5
            }
    
    def _extract_features(self, text: str) -> Dict[str, float]:
        """Extract features that may indicate AI generation"""
        blob = TextBlob(text)
        sentences = list(blob.sentences)
        words = blob.words
        
        features = {}
        
        # Text length features
        features['word_count'] = len(words)
        features['sentence_count'] = len(sentences)
        features['avg_sentence_length'] = len(words) / len(sentences) if sentences else 0
        
        # Vocabulary diversity
        unique_words = set(word.lower() for word in words)
        features['vocabulary_diversity'] = len(unique_words) / len(words) if words else 0
        
        # Repetition features
        features['word_repetition'] = self._calculate_word_repetition(words)
        features['phrase_repetition'] = self._calculate_phrase_repetition(text)
        
        # Sentence structure variety
        features['sentence_variety'] = self._calculate_sentence_variety(sentences)
        
        # Punctuation patterns
        features['punctuation_variety'] = self._calculate_punctuation_variety(text)
        
        # Formal language indicators
        features['formal_language_ratio'] = self._calculate_formal_language_ratio(text)
        
        return features
    
    def _calculate_ai_probability(self, features: Dict[str, float], text: str) -> float:
        """Calculate probability that text is AI-generated"""
        ai_score = 0.0
        total_weight = 0.0
        
        # Pattern matching
        ai_pattern_matches = sum(1 for pattern in self.ai_patterns if re.search(pattern, text, re.IGNORECASE))
        human_pattern_matches = sum(1 for pattern in self.human_patterns if re.search(pattern, text, re.IGNORECASE))
        
        pattern_score = (ai_pattern_matches - human_pattern_matches) / max(1, ai_pattern_matches + human_pattern_matches)
        ai_score += pattern_score * 0.3
        total_weight += 0.3
        
        # Sentence length consistency (AI tends to be more consistent)
        avg_length = features.get('avg_sentence_length', 0)
        if 15 <= avg_length <= 25:  # AI sweet spot
            ai_score += 0.2
        total_weight += 0.2
        
        # Vocabulary diversity (AI often has lower diversity)
        vocab_diversity = features.get('vocabulary_diversity', 0)
        if vocab_diversity < 0.6:  # Lower diversity suggests AI
            ai_score += 0.15
        elif vocab_diversity > 0.8:  # Higher diversity suggests human
            ai_score -= 0.1
        total_weight += 0.15
        
        # Word repetition (AI tends to repeat less)
        word_repetition = features.get('word_repetition', 0)
        if word_repetition < 0.1:  # Very low repetition
            ai_score += 0.1
        elif word_repetition > 0.3:  # High repetition suggests human
            ai_score -= 0.05
        total_weight += 0.1
        
        # Formal language ratio (AI tends to be more formal)
        formal_ratio = features.get('formal_language_ratio', 0)
        if formal_ratio > 0.3:
            ai_score += formal_ratio * 0.15
        total_weight += 0.15
        
        # Punctuation variety (humans use more varied punctuation)
        punct_variety = features.get('punctuation_variety', 0)
        if punct_variety < 0.2:
            ai_score += 0.1
        total_weight += 0.1
        
        # Normalize and bound the score
        if total_weight > 0:
            ai_score = ai_score / total_weight
        
        # Convert to probability (0-1 range)
        probability = max(0.0, min(1.0, 0.5 + ai_score))
        
        return probability
    
    def _calculate_word_repetition(self, words: List[str]) -> float:
        """Calculate word repetition ratio"""
        if not words:
            return 0.0
        
        word_counts = {}
        for word in words:
            word_lower = word.lower()
            word_counts[word_lower] = word_counts.get(word_lower, 0) + 1
        
        repeated_words = sum(1 for count in word_counts.values() if count > 1)
        return repeated_words / len(word_counts)
    
    def _calculate_phrase_repetition(self, text: str) -> float:
        """Calculate phrase repetition"""
        # Look for repeated 2-3 word phrases
        words = text.lower().split()
        if len(words) < 4:
            return 0.0
        
        phrases = []
        for i in range(len(words) - 2):
            phrase = ' '.join(words[i:i+3])
            phrases.append(phrase)
        
        phrase_counts = {}
        for phrase in phrases:
            phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1
        
        repeated_phrases = sum(1 for count in phrase_counts.values() if count > 1)
        return repeated_phrases / len(phrases) if phrases else 0.0
    
    def _calculate_sentence_variety(self, sentences) -> float:
        """Calculate sentence structure variety"""
        if not sentences:
            return 0.0
        
        sentence_lengths = [len(str(sentence).split()) for sentence in sentences]
        
        if len(sentence_lengths) < 2:
            return 0.0
        
        # Calculate coefficient of variation
        mean_length = sum(sentence_lengths) / len(sentence_lengths)
        variance = sum((length - mean_length) ** 2 for length in sentence_lengths) / len(sentence_lengths)
        std_dev = variance ** 0.5
        
        cv = std_dev / mean_length if mean_length > 0 else 0
        return min(1.0, cv)  # Normalize to 0-1
    
    def _calculate_punctuation_variety(self, text: str) -> float:
        """Calculate punctuation variety"""
        punctuation_marks = ['.', '!', '?', ',', ';', ':', '-', '(', ')', '"', "'"]
        
        punct_counts = {}
        for char in text:
            if char in punctuation_marks:
                punct_counts[char] = punct_counts.get(char, 0) + 1
        
        unique_punct = len(punct_counts)
        total_punct = sum(punct_counts.values())
        
        if total_punct == 0:
            return 0.0
        
        # Shannon diversity index for punctuation
        diversity = 0
        for count in punct_counts.values():
            if count > 0:
                p = count / total_punct
                diversity -= p * np.log2(p)
        
        # Normalize by max possible diversity
        max_diversity = np.log2(len(punctuation_marks))
        return diversity / max_diversity if max_diversity > 0 else 0.0
    
    def _calculate_formal_language_ratio(self, text: str) -> float:
        """Calculate ratio of formal language indicators"""
        formal_words = [
            'furthermore', 'moreover', 'additionally', 'consequently', 'therefore',
            'comprehensive', 'extensive', 'significant', 'substantial', 'considerable',
            'optimize', 'enhance', 'facilitate', 'leverage', 'implement',
            'methodology', 'framework', 'paradigm', 'systematic', 'strategic'
        ]
        
        words = text.lower().split()
        if not words:
            return 0.0
        
        formal_count = sum(1 for word in words if any(formal_word in word for formal_word in formal_words))
        return formal_count / len(words)
