from flask import Flask, request, jsonify
from google import genai

# 🔐 Put your real Gemini API key here
API_KEY = "YOUR_REAL_API_KEY"

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

app = Flask(__name__)

# -----------------------------
# Gemini Analysis Function
# -----------------------------
def analyze_complaint(text):

    prompt = f"""
You are an anti-ragging complaint analyzer.

Return ONLY in this format:

Category:
Priority:
Summary:

Complaint:
{text}
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    output = response.text if response.text else ""

    category = "Unknown"
    priority = "Medium"
    summary = "Not provided"

    for line in output.split("\n"):
        if line.startswith("Category"):
            category = line.split(":", 1)[1].strip()
        elif line.startswith("Priority"):
            priority = line.split(":", 1)[1].strip()
        elif line.startswith("Summary"):
            summary = line.split(":", 1)[1].strip()

    return {
        "category": category,
        "priority": priority,
        "summary": summary
    }

# -----------------------------
# Homepage Route
# -----------------------------
@app.route("/")
def home():
    return "Anti-Ragging Backend is Running"

# -----------------------------
# Analyze Route (POST)
# -----------------------------
@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    if not data or "complaint" not in data:
        return jsonify({"error": "Complaint text is required"}), 400

    complaint_text = data["complaint"].strip()

    if not complaint_text:
        return jsonify({"error": "Complaint cannot be empty"}), 400

    try:
        result = analyze_complaint(complaint_text)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Health Check
# -----------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Server running"}), 200

# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
