from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# IMPORTANT: You must configure your own API key
# for the Gemini API.
genai.configure(api_key="AIzaSyAuxAcOoCs9243BsVujwLAKXmG9JPS92Wo")
model = genai.GenerativeModel('models/gemini-2.5-flash-image-preview')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    image = Image.open(image_file.stream)

    response = model.generate_content(["Analyze the face in this image and suggest a hairstyle.", image])

    return jsonify({'recommendations': response.text})

if __name__ == '__main__':
    app.run(debug=True, port=5000)