import os
from io import BytesIO

import torch
from PIL import Image

from flask import Flask, jsonify, request

from labels_config import label_mapping_id

category = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'S', 'T', 'U', 'V', 'W',
            'X', 'Y', 'Z', 'Bullseye', 'Down', 'Eight', 'Five', 'Four', 'Left', 'Nine', 'One', 'Right', 'Seven',
            'Six', 'Stop', 'Three', 'Two', 'Up']


def create_app():
    app = Flask(__name__)

    # Load the model during app setup
    model_path = r'/Users/abc/Downloads/best_from_anh.pt'
    yolo_v5_dir = os.getcwd()
    model = torch.hub.load(yolo_v5_dir, 'custom', path=model_path, source='local')

    @app.route('/predict', methods=['POST'])
    def predict():
        cs = 0.0
        # Get the image from the request
        print(request.files)
        image_file = request.files['image']
        image = Image.open(BytesIO(image_file.read()))
        # Convert the image to a tensor and do inference
        output = model(image).pred
        results = model(image)
        detection = results.pandas().xyxy[0].to_dict(orient="records")
        area = 0
        for detect in detection:
            x1 = int(detect['xmin'])
            y1 = int(detect['ymin'])
            x2 = int(detect['xmax'])
            y2 = int(detect['ymax'])
            width = x2 - x1
            height = y2 - y1
            reference = width * height
            if (area < reference):
                area = reference
                print("Updated area:", area)
                cs = detect['class']
            print("xyminmax", x1, y1, x2, y2)
            print("Current class" , category[int(cs)])
            print("Current area:" , area)
            # area = (x2-x1) * (y2-y1)
        if (cs != 0.0):
            print("Class identified: " , category[int(cs)])
        print("pandas", results.pandas())
        print(output)
        print("resultsxyxy", results.xyxy[0])
        results.save()
        num_detected = len(output[0])  # number of images detected
        print([label_mapping_id[category[int(output[0][i][-1])]] for i in range(len(output[0]))] if len(
         output[0]) else 'Nothing detected')

        x = [category[int(output[0][i][-1])] for i in range(len(output[0]))] if len(
            output[0]) else 'Nothing detected'
        print(x)
        if x == 'Nothing detected':
            return '99'
        y = label_mapping_id[x[0]]
        print("Mapped id :" , y)
        print("Returning:" ,label_mapping_id[category[int(cs)]])
        #80 - Bullseye
        # 99 - nothing
        # Return numbers because if return string incur some JSON ERROR
        return jsonify(label_mapping_id[category[int(cs)]])
        # return jsonify([category[int(output[0][i][-1])] for i in range(len(output[0]))] if len(
             #output[0]) else 'Nothing detected')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
