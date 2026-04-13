from flask import Flask, request, jsonifyimport base64
import numpy as np
import cv2

app = Flask(__name__)

@app.route("/predic
t", methods=["POST"])
def predict():

data = request.json.get("image")

if not data:
return jsonify({"error": "no image"}), 400

img_data = b
ase64.b64decode(data.split(",")[1])

np_arr = np.frombuffer(img_data, np.uint8)

h, w, _ = img.shape

# 🎨 لون تقريبي
centerimg = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

# 🔥 تحليل بسيط (مكان YOLO لاحقاً
) = img[h//2, w//2]

b, g, r = int(center[0]), int(center[1]), int(center[2])

color = "Unknown"

if r > 200 and g > 200:
color = "White"
er)
return jsonify({
"belif r < 80 and g < 80:
color = "Black"
elif r > 150 and g < 100:
color = "Red"
elif r > 120:
color = "Silver"

# 🚗 نتيجة (YOLO placehol
drand": "Toyota",
"model": "Camry",
"category": "GL",
"color": color,
"year": "2026"
})

if __name__ == "__main__":
app.run(host="0.0.0.0", port=10000)