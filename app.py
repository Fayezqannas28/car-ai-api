from flask import Flask, request, jsonify
import os
from openai import OpenAI
import json

app = Flask(__name__)

# 🔑 OpenAI API Key من Render Environment Variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "AI Car API is running ✔"

@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()
        image = data.get("image")

        if not image:
            return jsonify({"error": "No image provided"}), 400

        # 🧠 إرسال الصورة لـ OpenAI Vision
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """
حلل السيارة في الصورة وأعد فقط JSON بدون شرح بهذا الشكل:
{
  "brand": "Toyota",
  "model": "Camry",
  "category": "Sedan / SUV / Pickup",
  "color": "White",
  "year": "2026"
}
إذا لم تعرف اكتب Unknown
"""
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

        # 🧹 تنظيف الناتج (مهم جداً)
        content = content.replace("```json", "").replace("```", "").strip()

        try:
            result = json.loads(content)
        except:
            # لو OpenAI رجع نص غير JSON
            result = {
                "raw": content,
                "error": "invalid_json_from_ai"
            }

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)