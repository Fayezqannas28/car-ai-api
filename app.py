from flask import Flask, request, jsonify
import os
import json
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/", methods=["GET"])
def home():
    return "AI Car API is running ✔"


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "status": "error",
                "error": "Invalid JSON body"
            }), 400

        image = data.get("image")

        if not image:
            return jsonify({
                "status": "error",
                "error": "No image provided"
            }), 400

        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": """
حلل صورة السيارة وأرجع JSON فقط بدون أي شرح أو markdown أو ```json

يجب أن يكون الرد بهذا الشكل فقط:
{
  "brand": "",
  "model": "",
  "category": "",
  "color": "",
  "year": ""
}

القواعد:
- إذا لم تعرف القيمة اكتب "غير معروف"
- category مثل: سيدان / SUV / بيك أب / كوبيه / هاتشباك / فان / شاحنة
- year يجب أن يكون رقم تقريبي إن أمكن، وإذا غير واضح اكتب "غير معروف"
- لا ترجع أي نص إضافي خارج JSON
"""
                        },
                        {
                            "type": "input_image",
                            "image_url": image
                        }
                    ]
                }
            ]
        )

        content = response.output_text.strip()

        clean_content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:
            result = json.loads(clean_content)
        except Exception:
            return jsonify({
                "status": "error",
                "error": "Model did not return valid JSON",
                "raw_output": content
            }), 500

        brand = str(result.get("brand", "غير معروف")).strip() or "غير معروف"
        model = str(result.get("model", "غير معروف")).strip() or "غير معروف"
        category = str(result.get("category", "غير معروف")).strip() or "غير معروف"
        color = str(result.get("color", "غير معروف")).strip() or "غير معروف"
        year = str(result.get("year", "غير معروف")).strip() or "غير معروف"

        return jsonify({
            "status": "success",
            "brand": brand,
            "model": model,
            "category": category,
            "color": color,
            "year": year
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)