from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# 🔑 من Render Environment Variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "AI Car API is running ✔"

@app.route("/predict", methods=["POST"])
def predict():

    data = request.json
    image = data.get("image")

    if not image:
        return jsonify({"error": "no image provided"}), 400

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "حلل السيارة في الصورة وأرجع JSON فقط يحتوي: brand, model, category, color, year"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image
                        }
                    }
                ]
            }
        ]
    )

    content = response.choices[0].message.content

    return jsonify({
        "result": content
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)