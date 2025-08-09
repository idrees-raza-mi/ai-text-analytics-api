import asyncio
import re
from typing import Dict, List, Any
from textblob import TextBlob
import random

class ContentGenerator:
    def __init__(self):
        # Content templates and patterns
        self.tone_modifiers = {
            "professional": ["leverage", "optimize", "streamline", "enhance", "facilitate"],
            "casual": ["awesome", "cool", "great", "fun", "easy"],
            "friendly": ["wonderful", "amazing", "fantastic", "delightful", "perfect"],
            "formal": ["furthermore", "therefore", "consequently", "moreover", "nevertheless"],
            "persuasive": ["proven", "guaranteed", "exclusive", "limited", "revolutionary"],
            "creative": ["innovative", "unique", "imaginative", "artistic", "original"]
        }
    
    async def generate_content(self, prompt: str, content_type: str, max_length: int = 300, tone: str = "professional") -> Dict[str, Any]:
        """Generate content based on prompt and specifications"""
        try:
            # Create content based on type
            if content_type == "blog_post":
                content = await self._generate_blog_post(prompt, max_length, tone)
            elif content_type == "email":
                content = await self._generate_email(prompt, max_length, tone)
            elif content_type == "social_media":
                content = await self._generate_social_media(prompt, max_length, tone)
            elif content_type == "product_description":
                content = await self._generate_product_description(prompt, max_length, tone)
            elif content_type == "article":
                content = await self._generate_article(prompt, max_length, tone)
            elif content_type == "ad_copy":
                content = await self._generate_ad_copy(prompt, max_length, tone)
            else:
                content = await self._generate_generic_content(prompt, max_length, tone)
            
            word_count = len(content.split())
            
            return {
                "content": content,
                "content_type": content_type,
                "word_count": word_count,
                "tone": tone
            }
            
        except Exception as e:
            return {
                "content": f"Error generating content: {str(e)}",
                "content_type": content_type,
                "word_count": 0,
                "tone": tone
            }
    
    async def _generate_blog_post(self, prompt: str, max_length: int, tone: str) -> str:
        """Generate a blog post"""
        tone_words = self.tone_modifiers.get(tone, [])
        
        # Extract key topics from prompt
        topics = self._extract_topics(prompt)
        
        # Generate introduction
        intro = f"In today's digital landscape, {prompt.lower()} has become increasingly important. "
        
        # Generate main content
        main_points = []
        for i, topic in enumerate(topics[:3], 1):
            if tone_words:
                modifier = random.choice(tone_words)
                point = f"{i}. {topic.capitalize()} is {modifier} for achieving your goals. "
            else:
                point = f"{i}. {topic.capitalize()} plays a crucial role in success. "
            main_points.append(point)
        
        main_content = "".join(main_points)
        
        # Generate conclusion
        conclusion = f"By implementing these strategies, you can {random.choice(tone_words) if tone_words else 'effectively'} improve your approach to {prompt.lower()}."
        
        full_content = intro + main_content + conclusion
        
        return self._trim_to_length(full_content, max_length)
    
    async def _generate_email(self, prompt: str, max_length: int, tone: str) -> str:
        """Generate an email"""
        if tone == "formal":
            greeting = "Dear Valued Customer,"
            closing = "Best regards,"
        elif tone == "casual":
            greeting = "Hi there!"
            closing = "Cheers!"
        else:
            greeting = "Hello,"
            closing = "Best regards,"
        
        # Generate email body
        body = f"I hope this email finds you well. I wanted to reach out regarding {prompt.lower()}. "
        
        if tone == "persuasive":
            body += f"This is an exclusive opportunity that I believe would be perfect for you. "
        elif tone == "friendly":
            body += f"I thought you might find this interesting and valuable. "
        else:
            body += f"I believe this information could be beneficial for you. "
        
        body += f"Please let me know if you have any questions or would like to discuss further."
        
        full_email = f"{greeting}\n\n{body}\n\n{closing}"
        
        return self._trim_to_length(full_email, max_length)
    
    async def _generate_social_media(self, prompt: str, max_length: int, tone: str) -> str:
        """Generate social media content"""
        # Social media is typically shorter
        max_length = min(max_length, 280)  # Twitter-like limit
        
        hashtags = self._generate_hashtags(prompt)
        
        if tone == "casual":
            content = f"Just discovered something amazing about {prompt.lower()}! 🚀 "
        elif tone == "professional":
            content = f"Insights on {prompt.lower()} that every professional should know: "
        elif tone == "creative":
            content = f"✨ Unleashing the power of {prompt.lower()} ✨ "
        else:
            content = f"Key insights about {prompt.lower()}: "
        
        # Add a brief point
        topics = self._extract_topics(prompt)
        if topics:
            content += f"Focus on {topics[0].lower()} for maximum impact. "
        
        content += f"{hashtags}"
        
        return self._trim_to_length(content, max_length)
    
    async def _generate_product_description(self, prompt: str, max_length: int, tone: str) -> str:
        """Generate product description"""
        topics = self._extract_topics(prompt)
        tone_words = self.tone_modifiers.get(tone, ["excellent"])
        
        # Product name from prompt
        product_name = prompt.title()
        
        description = f"Introducing {product_name} - the {random.choice(tone_words)} solution for your needs. "
        
        # Features
        features = []
        for topic in topics[:3]:
            feature = f"✓ {random.choice(tone_words).title()} {topic.lower()}"
            features.append(feature)
        
        if features:
            description += "Key features include: " + ", ".join(features) + ". "
        
        # Call to action
        if tone == "persuasive":
            description += "Don't miss out - order yours today!"
        else:
            description += "Perfect for anyone looking to improve their experience."
        
        return self._trim_to_length(description, max_length)
    
    async def _generate_article(self, prompt: str, max_length: int, tone: str) -> str:
        """Generate an article"""
        topics = self._extract_topics(prompt)
        
        # Article structure
        title = f"Understanding {prompt.title()}: A Comprehensive Guide"
        
        intro = f"In recent years, {prompt.lower()} has gained significant attention. This article explores the key aspects and implications."
        
        # Main sections
        sections = []
        for i, topic in enumerate(topics[:4], 1):
            section = f"\n\n{i}. {topic.title()}\n"
            section += f"When considering {topic.lower()}, it's important to understand the fundamental principles. "
            sections.append(section)
        
        conclusion = f"\n\nIn conclusion, {prompt.lower()} represents a significant opportunity for growth and improvement. By focusing on these key areas, you can achieve better results."
        
        full_article = intro + "".join(sections) + conclusion
        
        return self._trim_to_length(full_article, max_length)
    
    async def _generate_ad_copy(self, prompt: str, max_length: int, tone: str) -> str:
        """Generate advertising copy"""
        tone_words = self.tone_modifiers.get(tone, ["amazing"])
        
        # Headlines
        headlines = [
            f"Transform Your {prompt.title()} Today!",
            f"The {random.choice(tone_words).title()} {prompt.title()} Solution",
            f"Discover the Secret to Better {prompt.title()}"
        ]
        
        headline = random.choice(headlines)
        
        # Main copy
        body = f"Are you ready to revolutionize your approach to {prompt.lower()}? "
        body += f"Our {random.choice(tone_words)} solution delivers results that exceed expectations. "
        
        # Benefits
        topics = self._extract_topics(prompt)
        if topics:
            body += f"Experience improved {topics[0].lower()} and enhanced performance. "
        
        # Call to action
        cta = random.choice([
            "Get started today!",
            "Don't wait - act now!",
            "Transform your results today!",
            "Unlock your potential now!"
        ])
        
        full_copy = f"{headline}\n\n{body}{cta}"
        
        return self._trim_to_length(full_copy, max_length)
    
    async def _generate_generic_content(self, prompt: str, max_length: int, tone: str) -> str:
        """Generate generic content"""
        tone_words = self.tone_modifiers.get(tone, ["important"])
        
        content = f"{prompt.capitalize()} is {random.choice(tone_words)} in today's world. "
        
        topics = self._extract_topics(prompt)
        for topic in topics[:3]:
            content += f"Consider the impact of {topic.lower()} on your objectives. "
        
        content += f"By understanding these concepts, you can make more informed decisions about {prompt.lower()}."
        
        return self._trim_to_length(content, max_length)
    
    async def generate_meta_description(self, content: str, max_length: int = 160) -> Dict[str, Any]:
        """Generate SEO meta description"""
        try:
            # Extract key phrases from content
            blob = TextBlob(content)
            sentences = list(blob.sentences)
            
            if not sentences:
                meta_description = content[:max_length]
            else:
                # Use first sentence as base
                first_sentence = str(sentences[0])
                
                # Extract keywords
                keywords = self._extract_topics(content)
                
                # Create meta description
                if len(first_sentence) <= max_length:
                    meta_description = first_sentence
                else:
                    # Truncate and add keywords
                    meta_description = first_sentence[:max_length-10] + "..."
                
                # Ensure it includes important keywords
                for keyword in keywords[:2]:
                    if keyword.lower() not in meta_description.lower():
                        # Try to incorporate keyword
                        if len(meta_description) + len(keyword) + 2 <= max_length:
                            meta_description = meta_description.rstrip('.') + f", {keyword.lower()}."
                        break
            
            # Calculate SEO score
            seo_score = self._calculate_seo_score(meta_description, keywords)
            
            # Generate suggestions
            suggestions = self._generate_seo_suggestions(meta_description, keywords, max_length)
            
            return {
                "meta_description": meta_description[:max_length],
                "length": len(meta_description[:max_length]),
                "seo_score": seo_score,
                "suggestions": suggestions
            }
            
        except Exception as e:
            return {
                "meta_description": content[:max_length],
                "length": len(content[:max_length]),
                "seo_score": 0.5,
                "suggestions": ["Consider adding more specific keywords", "Ensure description is compelling"]
            }
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract key topics from text"""
        # Simple topic extraction
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        
        # Filter out common words
        stop_words = {'that', 'with', 'have', 'this', 'will', 'your', 'from', 'they', 'know', 'want', 'been', 'good', 'much', 'some', 'time', 'very', 'when', 'come', 'here', 'just', 'like', 'long', 'make', 'many', 'over', 'such', 'take', 'than', 'them', 'well', 'work'}
        
        topics = [word for word in words if word not in stop_words]
        
        # Return unique topics
        unique_topics = []
        for topic in topics:
            if topic not in unique_topics:
                unique_topics.append(topic)
        
        return unique_topics[:5]
    
    def _generate_hashtags(self, text: str) -> str:
        """Generate relevant hashtags"""
        topics = self._extract_topics(text)
        hashtags = [f"#{topic.replace(' ', '')}" for topic in topics[:3]]
        return " ".join(hashtags)
    
    def _trim_to_length(self, text: str, max_length: int) -> str:
        """Trim text to specified length"""
        if len(text) <= max_length:
            return text
        
        # Try to cut at sentence boundary
        sentences = text.split('. ')
        result = ""
        
        for sentence in sentences:
            if len(result + sentence + '. ') <= max_length:
                result += sentence + '. '
            else:
                break
        
        # If no complete sentence fits, cut at word boundary
        if not result:
            words = text.split()
            result = ""
            for word in words:
                if len(result + word + ' ') <= max_length:
                    result += word + ' '
                else:
                    break
        
        return result.strip()
    
    def _calculate_seo_score(self, description: str, keywords: List[str]) -> float:
        """Calculate SEO score for meta description"""
        score = 0.5  # Base score
        
        # Length score
        if 140 <= len(description) <= 160:
            score += 0.2
        elif 120 <= len(description) <= 180:
            score += 0.1
        
        # Keyword inclusion score
        description_lower = description.lower()
        keyword_count = sum(1 for keyword in keywords if keyword.lower() in description_lower)
        if keyword_count > 0:
            score += min(0.3, keyword_count * 0.15)
        
        return min(1.0, score)
    
    def _generate_seo_suggestions(self, description: str, keywords: List[str], max_length: int) -> List[str]:
        """Generate SEO improvement suggestions"""
        suggestions = []
        
        # Length suggestions
        if len(description) < 120:
            suggestions.append("Consider making the description longer (120-160 characters is optimal)")
        elif len(description) > 160:
            suggestions.append("Description is too long, consider shortening to under 160 characters")
        
        # Keyword suggestions
        description_lower = description.lower()
        missing_keywords = [kw for kw in keywords[:3] if kw.lower() not in description_lower]
        if missing_keywords:
            suggestions.append(f"Consider including keywords: {', '.join(missing_keywords)}")
        
        # Action word suggestions
        action_words = ['discover', 'learn', 'explore', 'find', 'get', 'start']
        has_action = any(word in description_lower for word in action_words)
        if not has_action:
            suggestions.append("Add an action word to make the description more compelling")
        
        return suggestions or ["Meta description looks good!"]
