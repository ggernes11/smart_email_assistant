#!/usr/bin/env python3
"""
Email Response Assistant - Startup Script
Run this file to start the Flask application
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if OpenAI API key is set
if not os.getenv('OPENAI_API_KEY'):
    print("❌ Error: OPENAI_API_KEY not found in environment variables.")
    print("Please set your OpenAI API key in the .env file:")
    print("OPENAI_API_KEY=your_api_key_here")
    sys.exit(1)

# Check if emails.csv exists
if not os.path.exists('emails.csv'):
    print("❌ Error: emails.csv not found.")
    print("Please make sure you have an emails.csv file in the project directory.")
    print("You can use the provided sample emails.csv file.")
    sys.exit(1)

# Import and run the Flask app
try:
    from app import app
    
    print("🚀 Starting Email Response Assistant...")
    print(f"📧 Processing up to {os.getenv('EMAIL_COUNT', 10)} emails")
    print("🌐 Open your browser to: http://localhost:5000")
    print("💡 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
    
except ImportError as e:
    print(f"❌ Error importing required modules: {e}")
    print("Please install required dependencies:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting application: {e}")
    sys.exit(1)