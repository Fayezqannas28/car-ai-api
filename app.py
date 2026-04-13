from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Car API is running ✔"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json.get("image", "")

    return jsonify({
        "brand": "Toyota",
        "model": "Camry",
        "category": "GL",
        "color": "White",
        "year": "2026"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)