from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import requests, os
from datetime import datetime

escalations = []

load_dotenv()
app = Flask(__name__)

# YOUR C++ engine address — already running at 9090
YOUR_ENGINE = "http://localhost:9090"

# Confidence threshold — from YOUR cosine distance function
ESCALATE_THRESHOLD = 0.55

def ask_your_engine(question):
    """
    Calls YOUR /doc/ask endpoint.
    YOUR main.cpp does:
      1. ollama.embed(question)
      2. docDB.search() via HNSW
      3. ollama.generate(context + question)
    Returns answer + contexts with distances.
    """
    try:
        r = requests.post(
            f"{YOUR_ENGINE}/doc/ask",
            json={"question": question, "k": 3},
            timeout=120
        )
        return r.json()
    except:
        return {"error": "Engine offline"}

def should_escalate(result):
    """
    Uses YOUR engine's cosine distance to decide.
    Low distance = confident match in YOUR HNSW index.
    High distance = no good match = escalate to human.
    """
    if result.get("error"):
        return True, "Engine error"
    contexts = result.get("contexts", [])
    if not contexts:
        return True, "No relevant docs found in HNSW index"
    min_dist = min(c.get("distance", 1) for c in contexts)
    if min_dist > ESCALATE_THRESHOLD:
        return True, f"Low confidence (distance {min_dist:.3f})"
    answer = result.get("answer", "").lower()
    uncertain = ["don't know", "not sure", "cannot help",
                 "escalate", "human agent", "unable to"]
    if any(p in answer for p in uncertain):
        return True, "Bot expressed uncertainty"
    return False, "resolved"

# ── WHATSAPP WEBHOOK ──────────────────────────────────────────────
# Twilio calls this when someone messages your WhatsApp number
@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    msg    = request.form.get("Body", "").strip()
    sender = request.form.get("From", "unknown")
    print(f"[WhatsApp] {sender}: {msg}")

    # Ask YOUR C++ RAG engine
    result   = ask_your_engine(msg)
    answer   = result.get("answer", "Sorry, I couldn't process that.")
    escalate, reason = should_escalate(result)

    if escalate:
        answer += f"\n\n⚡ Our support team has been notified and will follow up shortly."
        print(f"[ESCALATED] reason: {reason}")
        escalations.insert(0, {
            "id": len(escalations) + 1,
            "sender": sender,
            "message": msg,
            "bot_reply": result.get("answer", ""),
            "reason": reason,
            "time": datetime.now().strftime("%I:%M %p")
        })

    # Send reply via Twilio back to WhatsApp
    resp = MessagingResponse()
    resp.message(answer)
    return str(resp)

# ── WEB CHAT (used by your index.html dashboard) ──────────────────
@app.route("/chat", methods=["POST"])
def web_chat():
    data   = request.json or {}
    msg    = data.get("message", "")
    result = ask_your_engine(msg)
    escalate, reason = should_escalate(result)
    return jsonify({
        "answer":    result.get("answer", "Engine offline"),
        "escalated": escalate,
        "reason":    reason,
        "contexts":  result.get("contexts", [])
    })

# ── DASHBOARD ROUTES ──────────────────────────────────────────────
@app.route("/api/escalations")
def api_escalations():
    return jsonify(escalations)

@app.route("/dashboard")
def dashboard():
    try:
        with open("dashboard.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Dashboard file not found.", 404

# ── STATUS CHECK ──────────────────────────────────────────────────
@app.route("/status")
def status():
    try:
        r = requests.get(f"{YOUR_ENGINE}/status", timeout=3)
        return jsonify({"flask": "online", "engine": r.json()})
    except:
        return jsonify({"flask": "online", "engine": "offline"})

if __name__ == "__main__":
    print("Flask middleware running at http://localhost:5000")
    print(f"Calling YOUR engine at {YOUR_ENGINE}")
    app.run(debug=True, port=5000)