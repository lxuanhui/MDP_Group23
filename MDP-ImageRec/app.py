import os
from io import BytesIO

import torch
from PIL import Image

from flask import Flask, jsonify, request

category = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'S', 'T', 'U', 'V', 'W',
            'X', 'Y', 'Z', 'Bullseye', 'Down', 'Eight', 'Five', 'Four', 'Left', 'Nine', 'One', 'Right', 'Seven',
            'Six', 'Stop', 'Three', 'Two', 'Up']


def get_image_from(image_path: str) -> Image.Image:
    """Load image from a file. Close the file without losing the image"""
    with Image.open(image_path) as image:
        image.load()
    return image


def create_app():
    app = Flask(__name__)

    # Load the model during app setup
    model_path = r'/Users/abc/Downloads/best_from_anh.pt'
    yolo_v5_dir = os.getcwd()
    model = torch.hub.load(yolo_v5_dir, 'custom', path=model_path, source='local')

    @app.route('/predict', methods=['POST'])
    def predict():
        # Get the image from the request
        print(request.files)
        # image = request.files['image'].read()
        image_file = request.files['image']
        image = Image.open(BytesIO(image_file.read()))
        # Convert the image to a tensor and do inference
        output = model(image).pred
        return jsonify([category[int(output[0][i][-1])] for i in range(len(output[0]))] if len(
            output[0]) else 'Nothing detected')

        # Convert the result to a JSON response
        response = jsonify(result)
        return response

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
