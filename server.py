import os
import uvicorn
from main import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    print(f"🚀 Starting AI Text Analytics API on port {port}")
    print(f"💡 Environment: PORT={os.environ.get('PORT')}, API_KEY configured: {bool(os.environ.get('API_KEY'))}")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
