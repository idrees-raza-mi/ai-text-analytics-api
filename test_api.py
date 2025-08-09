#!/usr/bin/env python3
"""
Test script for AI Text Analytics API
Run this to test all endpoints before deployment
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "SecureAI2024_TextAnalytics_789xyz"  # Change this to match your .env file

# Headers for all requests
HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Test data
TEST_DATA = {
    "short_text": "I love this amazing product! It works perfectly.",
    "long_text": """
    Artificial intelligence has revolutionized the way we approach technology and business.
    In recent years, AI has become increasingly sophisticated, enabling automation of complex tasks
    that were previously thought to require human intelligence. From natural language processing
    to computer vision, AI applications are now ubiquitous in our daily lives. Companies across
    industries are leveraging AI to improve efficiency, reduce costs, and create new revenue streams.
    However, the rapid advancement of AI also raises important questions about ethics, privacy,
    and the future of work. As we continue to develop more powerful AI systems, it is crucial
    that we consider these implications and work towards responsible AI development.
    """,
    "multilingual_text": "Bonjour, comment allez-vous? Je suis très heureux aujourd'hui!",
    "ai_generated_text": """
    Furthermore, it's important to note that artificial intelligence represents a paradigm shift
    in how we approach problem-solving. Moreover, AI technologies can optimize and streamline
    various processes across multiple industries. Additionally, machine learning algorithms
    facilitate the analysis of large datasets, consequently enabling organizations to leverage
    data-driven insights for strategic decision-making.
    """,
    "human_text": """Hey, I was just thinking... you know what really bugs me? When people say 'literally' 
    but they don't mean it literally! Like, my friend was like 'I literally died laughing' 
    and I'm like, no you didn't! You're still here! Anyway, that's just my random thought for today lol."""
}

def test_endpoint(endpoint: str, data: Dict[str, Any], description: str) -> bool:
    """Test a single endpoint"""
    print(f"\n🧪 Testing {description}...")
    print(f"   Endpoint: POST {endpoint}")
    
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", headers=HEADERS, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success! Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"   ❌ Failed! Status: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_health_endpoint() -> bool:
    """Test health endpoint"""
    print("\n🏥 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Health check passed: {response.json()}")
            return True
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False

def test_root_endpoint() -> bool:
    """Test root endpoint"""
    print("\n🏠 Testing Root Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Root endpoint working: {result['message']}")
            print(f"   Available endpoints: {', '.join(result['endpoints'])}")
            return True
        else:
            print(f"   ❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Root endpoint error: {e}")
        return False

def main():
    """Run all API tests"""
    print("🚀 AI Text Analytics API Test Suite")
    print("=" * 50)
    
    # Test server availability
    if not test_health_endpoint():
        print("\n❌ Server is not running or health check failed!")
        print("   Make sure to start the API server first: python main.py")
        return
    
    if not test_root_endpoint():
        print("\n❌ Root endpoint failed!")
        return
    
    # Test results tracking
    results = []
    
    # Test all endpoints
    test_cases = [
        {
            "endpoint": "/analyze-sentiment",
            "data": {"text": TEST_DATA["short_text"]},
            "description": "Sentiment Analysis"
        },
        {
            "endpoint": "/detect-language", 
            "data": {"text": TEST_DATA["multilingual_text"]},
            "description": "Language Detection"
        },
        {
            "endpoint": "/extract-keywords",
            "data": {"text": TEST_DATA["long_text"], "max_keywords": 5},
            "description": "Keyword Extraction"
        },
        {
            "endpoint": "/summarize-text",
            "data": {"text": TEST_DATA["long_text"], "max_length": 100, "min_length": 30},
            "description": "Text Summarization"
        },
        {
            "endpoint": "/generate-content",
            "data": {
                "prompt": "AI and machine learning benefits",
                "content_type": "blog_post",
                "max_length": 200,
                "tone": "professional"
            },
            "description": "Content Generation"
        },
        {
            "endpoint": "/detect-ai-content",
            "data": {"text": TEST_DATA["ai_generated_text"]},
            "description": "AI Content Detection (AI Text)"
        },
        {
            "endpoint": "/detect-ai-content",
            "data": {"text": TEST_DATA["human_text"]}, 
            "description": "AI Content Detection (Human Text)"
        },
        {
            "endpoint": "/analyze-readability",
            "data": {"text": TEST_DATA["long_text"]},
            "description": "Readability Analysis"
        },
        {
            "endpoint": "/generate-meta-description",
            "data": {"content": TEST_DATA["long_text"], "max_length": 160},
            "description": "Meta Description Generation"
        }
    ]
    
    # Run all tests
    for test_case in test_cases:
        success = test_endpoint(
            test_case["endpoint"],
            test_case["data"], 
            test_case["description"]
        )
        results.append({
            "test": test_case["description"],
            "success": success
        })
        
        # Small delay between requests
        time.sleep(0.5)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(1 for r in results if r["success"])
    total = len(results)
    
    for result in results:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"{status} - {result['test']}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Your API is ready for deployment!")
        print("\n📋 Next steps:")
        print("   1. Deploy to a cloud platform (Railway, Heroku, etc.)")
        print("   2. Register as a RapidAPI provider")
        print("   3. List your API on RapidAPI marketplace")
        print("   4. Start earning money! 💰")
    else:
        print(f"\n⚠️  {total-passed} tests failed. Please fix the issues before deployment.")

if __name__ == "__main__":
    main()
