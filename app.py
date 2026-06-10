import os
import re
import json
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = Flask(__name__, static_folder="static")

SUSPICIOUS_KEYWORDS = [
    "breaking", "shocking", "exclusive", "unbelievable", "urgent",
    "click here", "you won't believe", "scam", "hoax", "conspiracy",
    "miracle", "banned", "secret", "exposed", "share before deleted",
    "they don't want you", "mainstream media", "whistleblower",
    "cover-up", "deep state", "fake news", "radical", "crisis actor",
]

def find_suspicious(text):
    found = []
    for kw in SUSPICIOUS_KEYWORDS:
        if re.search(r'\b' + re.escape(kw) + r'\b', text, re.IGNORECASE):
            found.append(kw)
    return found


def generate(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip(), None
    except Exception as e:
        return None, str(e)


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "").strip()

    if not text or len(text.split()) < 25:
        return jsonify({"error": "Please provide at least 25 words."}), 400

    prompt = f"""
You are a professional news fact-checker and summarizer.
Return ONLY valid JSON with no extra text or explanation.

Article:
\"\"\"{text}\"\"\"

Return this exact JSON format:
{{
  "summary": "2-3 sentence summary here",
  "credibility_score": 75,
  "verdict": "credible",
  "red_flags": ["flag1", "flag2"],
  "positive_signals": ["signal1", "signal2"],
  "key_claims": ["claim1", "claim2"]
}}

Rules:
- credibility_score must be a number between 0 and 100
- verdict must be exactly one of: credible, misleading, uncertain
- all list fields must be arrays of strings
- return ONLY the JSON, nothing else
"""

    raw, error = generate(prompt)

    if error:
        if "429" in error or "rate_limit" in error.lower():
            return jsonify({"error": "Rate limit hit. Please wait a moment and try again."}), 429
        return jsonify({"error": f"API error: {error}"}), 500

    raw = re.sub(r"```json|```", "", raw).strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        return jsonify({"error": "Model returned invalid JSON. Please try again."}), 500

    result["suspicious_keywords"] = find_suspicious(text)
    return jsonify(result)


@app.route("/api/followup", methods=["POST"])
def followup():
    data = request.json

    article = data.get("article", "")
    summary = data.get("summary", "")
    verdict = data.get("verdict", "")
    score = data.get("score", "")
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "No question provided."}), 400

    prompt = f"""
You are a news fact-checker assistant.

Article: {article[:1500]}

Summary: {summary}
Verdict: {verdict} ({score}% credibility)

User question: {question}

Answer in 2-4 clear sentences. Be direct and factual.
"""

    answer, error = generate(prompt)

    if error:
        if "429" in error or "rate_limit" in error.lower():
            return jsonify({"error": "Rate limit hit. Please wait a moment and try again."}), 429
        return jsonify({"error": f"API error: {error}"}), 500

    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True, port=5000)