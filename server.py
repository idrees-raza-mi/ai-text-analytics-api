"""
Simple server.py file for Railway deployment
This acts as a wrapper around our main.py to ensure proper startup
"""

import os
import uvicorn

if __name__ == "__main__":
    # Get port from Railway environment
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    print(f"Environment variables: PORT={os.environ.get('PORT')}, API_KEY set: {bool(os.environ.get('API_KEY'))}")
    
    # Run the server with the app from main.py
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
