from flask import Flask, request, jsonify
import base64
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

@app.route("/predict", methods=["POST"])
def predict():

    image = request.json.get("image")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "حلل السيارة في الصورة وأعطني: brand, model, category, color, year"
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

    return jsonify(response.choices[0].message.content)