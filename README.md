# Customer Support Assistant

This project converts the uploaded n8n workflow into a small Flask + HTML/CSS + JavaScript web application using Google Gemini.

## Features
- Customer Support Assistant chat interface
- Gemini-powered answers
- Conversation context (last 10 exchanges, stored in the Flask session)
- Suggested questions, typing indicator, and New chat button
- Responsive layout for desktop and mobile

## Requirements
- Python 3.10 or newer
- A Google Gemini API key
- Internet connection

## Setup (Windows)
1. Extract this ZIP file.
2. Open the project folder in VS Code.
3. Open Terminal in VS Code.
4. Create a virtual environment:

   `py -m venv .venv`

5. Activate it:

   PowerShell: `.\.venv\Scripts\Activate.ps1`

   If PowerShell blocks activation, use Command Prompt and run:
   `.venv\Scripts\activate.bat`

6. Install the packages:

   `pip install -r requirements.txt`

7. Copy `.env.example` and rename the copy to `.env`.
8. Open `.env` and replace `your_gemini_api_key_here` with your own API key. Keep the key private.
9. Start the application:

   `python app.py`

10. Open `http://127.0.0.1:5000` in your browser.

## Important
- Do not upload your `.env` file or API key to GitHub.
- This is a learning/demo project. It does not connect to a real store, order database, CRM, or refund system.
- For production use, turn off debug mode, use a secure session configuration, add rate limiting, and configure deployment security.
