import os
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

SYSTEM_PROMPT = """
You are a friendly, knowledgeable customer support assistant.
Answer questions clearly, politely, and helpfully.
Keep track of the conversation and ask a short clarifying question if a request is ambiguous.
Use short paragraphs or lists for longer answers.
Never invent company policies, order statuses, refunds, or account details.
If the user asks about an order or account and no connected company system is available,
explain that you cannot access their private account information.
If you do not know something, say so honestly.
"""

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    if client is None:
        return jsonify({
            "reply": "The chatbot is not configured yet. Add your GEMINI_API_KEY to the .env file and restart the app."
        }), 500

    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"reply": "Please type a message first."}), 400

    # Keep the most recent 10 user/assistant messages in the browser session.
    history = session.get("history", [])
    history.append({"role": "user", "text": message})
    history = history[-20:]  # up to 10 exchanges

    contents = []
    for item in history:
        role = "user" if item["role"] == "user" else "model"
        contents.append({
            "role": role,
            "parts": [{"text": item["text"]}]
        })

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "temperature": 0.4,
            },
        )
        reply = (response.text or "").strip()
        if not reply:
            reply = "Sorry, I couldn't create a response. Please try asking in a different way."
    except Exception as exc:
        app.logger.exception("Gemini API request failed")
        return jsonify({
            "reply": "Sorry, I couldn't connect to the AI service. Check your API key, internet connection, and model configuration."
        }), 502

    history.append({"role": "assistant", "text": reply})
    session["history"] = history[-20:]
    session.modified = True
    return jsonify({"reply": reply})


@app.route("/reset", methods=["POST"])
def reset_chat():
    session.pop("history", None)
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    # Local development server. Do not use debug=True in production.
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=True)
