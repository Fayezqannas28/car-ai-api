from flask import Flask, request, jsonify
import os
from openai import OpenAI
import json

app = Flask(__name__)

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

        response = client.responses.create(
            model="gpt-4o-mini",
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text",
                     "text": """حلل السيارة وأرجع JSON فقط:
{
"brand":"",
"model":"",
"category":"",
"color":"",
"year":""
}""" },
                    {
                        "type": "input_image",
                        "image_url": image
                    }
                ]
            }]
        )

        content = response.output_text

        content = content.replace("```json","").replace("```","").strip()

        result = json.loads(content)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)