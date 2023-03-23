import copy
import os
import datetime
from io import BytesIO
from pathlib import Path
from typing import List

import torch
from PIL import Image, ImageEnhance

from flask import Flask, jsonify, request

from labels_config import label_mapping_id
from utils.general import increment_path

category = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'S', 'T', 'U', 'V', 'W',
            'X', 'Y', 'Z', 'Bullseye', 'Down', 'Eight', 'Five', 'Four', 'Left', 'Nine', 'One', 'Right', 'Seven',
            'Six', 'Stop', 'Three', 'Two', 'Up']


def create_app():
    app = Flask(__name__)

    # Load the model during app setup
    model_path = r'/Users/abc/Downloads/best.pt'
    yolo_v5_dir = os.getcwd()
    model = torch.hub.load(yolo_v5_dir, 'custom', path=model_path, source='local')

    previously_detected = []

    def get_exp_number_from_foldername(exp_name):
        int_string = exp_name[3:]
        if int_string == "":
            return 1
        else:
            return int(int_string)

    def get_exp_number_from_folderpath(folderpath):
        return get_exp_number_from_foldername(folderpath.name)

    def get_latest_exp_folder_from_detect(detectpath, num_photos):
        return sorted(detectpath.glob("exp*"), key=get_exp_number_from_folderpath)[-num_photos:]

    def take_image_change_brightness(image, factor):
        enhancer_brightness = ImageEnhance.Brightness(image)
        bright_image = enhancer_brightness.enhance(factor)

        # do imagerec on bright_image
        results = model(bright_image)
        detection = results.pandas().xyxy[0].to_dict(orient="records")
        final_detected = None
        ref_area = 0
        for i, detect in enumerate(detection):
            if category[int(detect['class'])] == 'Bullseye':
                # ignore the bullseye
                continue

            x1 = int(detect['xmin'])
            y1 = int(detect['ymin'])
            x2 = int(detect['xmax'])
            y2 = int(detect['ymax'])
            width = x2 - x1
            height = y2 - y1

            bb_area = width * height  # Get the area of the box
            if ref_area < bb_area:  # Use the bigger box.
                ref_area = bb_area
                print("Updated area:", ref_area)
                final_detected = category[int(detect['class'])]
                print("Updated label:", final_detected)

        if final_detected is None or final_detected not in ['Left', 'Right']:
            print(f"Brightness augmentation by factor {factor} did not work")
            return None

        if final_detected == 'Left':
            results.save_mdp(21)
            return '39'
        if final_detected == 'Right':
            results.save_mdp(24)
            return '38'

    def take_image_change_contrast(image, factor):
        enhancer_contrast = ImageEnhance.Contrast(image)
        contrasted_image = enhancer_contrast.enhance(factor)

        # do imagerec on contrasted
        results = model(contrasted_image)
        detection = results.pandas().xyxy[0].to_dict(orient="records")
        final_detected = None
        ref_area = 0
        for i, detect in enumerate(detection):
            if category[int(detect['class'])] == 'Bullseye':
                # ignore the bullseye
                continue

            x1 = int(detect['xmin'])
            y1 = int(detect['ymin'])
            x2 = int(detect['xmax'])
            y2 = int(detect['ymax'])
            width = x2 - x1
            height = y2 - y1

            bb_area = width * height  # Get the area of the box
            if ref_area < bb_area:  # Use the bigger box.
                ref_area = bb_area
                print("Updated area:", ref_area)
                final_detected = category[int(detect['class'])]
                print("Updated label:", final_detected)

        if final_detected is None or final_detected not in ['Left', 'Right']:
            print(f"Contrast augmentation by factor {factor} did not work")
            return None

        if final_detected == 'Left':
            results.save_mdp(21)
            return '39'
        if final_detected == 'Right':
            results.save_mdp(24)
            return '38'

    @app.route('/showtiled', methods=['POST'])
    def show_tiled():
        previously_detected.clear()
        print(previously_detected)

        num_photos = request.json['num_photos']
        exp_num_list = get_latest_exp_folder_from_detect(Path("/Users/abc/yolov5/runs/detect"), num_photos)
        print(exp_num_list)

        # Load all images
        images = [Image.open(str(path) + '/image0.jpg') for path in exp_num_list]
        # Determine the number of rows and columns
        num_images = len(images)
        num_cols = 2 if num_images > 4 else 1
        num_rows = (num_images + num_cols - 1) // num_cols
        # Calculate the width and height of the tiled image
        max_width = max(img.width for img in images)
        max_height = max(img.height for img in images)
        tiled_width = max_width * num_cols
        tiled_height = max_height * num_rows
        # Create the tiled image
        tiled_image = Image.new('RGB', (tiled_width, tiled_height))
        # Paste each image into the tiled image
        for i, img in enumerate(images):
            col_idx = i % num_cols
            row_idx = i // num_cols
            x = col_idx * max_width
            y = row_idx * max_height
            tiled_image.paste(img, (x, y))
        tiled_image.save("/Users/abc/Desktop/"+"TiledImage_"+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".png")
        tiled_image.show()

        return "success"

    @app.route('/detect_w9_o1', methods=['POST'])
    def detect_w9_o1():
        # for the first obstacle
        # a or d for first image
        image_file = request.files['image']
        image = Image.open(BytesIO(image_file.read()))
        output = model(image).pred
        results = model(image)
        detection = results.pandas().xyxy[0].to_dict(orient="records")
        final_detected = None
        ref_area = 0
        for i, detect in enumerate(detection):
            if category[int(detect['class'])] == 'Bullseye':
                # ignore the bullseye
                continue

            x1 = int(detect['xmin'])
            y1 = int(detect['ymin'])
            x2 = int(detect['xmax'])
            y2 = int(detect['ymax'])
            width = x2 - x1
            height = y2 - y1

            bb_area = width * height  # Get the area of the box
            if ref_area < bb_area:  # Use the bigger box.
                ref_area = bb_area
                print("Updated area:", ref_area)
                final_detected = category[int(detect['class'])]
                print("Updated label:", final_detected)

        if final_detected is None or final_detected not in ['Left', 'Right']:
            print("Initiating some image enhancements")

            # 1) Increase brightness
            increase_brightness_result = take_image_change_brightness(image, 1.5)
            if increase_brightness_result is not None:
                return increase_brightness_result

            # 2) Decrease brightness
            decrease_brightness_result = take_image_change_brightness(image, 0.5)
            if decrease_brightness_result is not None:
                return decrease_brightness_result

            # 3) Increase contrast
            increase_contrast_result = take_image_change_contrast(image, 1.5)
            if increase_contrast_result is not None:
                return increase_contrast_result

            # 4) Decrease contrast
            decrease_contrast_result = take_image_change_contrast(image, 0.5)
            if decrease_contrast_result is not None:
                return decrease_contrast_result

            print("Either nothing detected or Non-bullseye detected that is not Left/Right arrow")
            print("Should return something to STM to let them know that something is not right")
            return '99'

        if final_detected == 'Left':
            results.save_mdp(21)
            return '39'
        if final_detected == 'Right':
            results.save_mdp(24)
            return '38'

    @app.route('/detect_w9_o2', methods=['POST'])
    def detect_w9_o2():
        # for the second obstacle
        # l or r for second image
        image_file = request.files['image']
        image = Image.open(BytesIO(image_file.read()))
        output = model(image).pred
        results = model(image)
        detection = results.pandas().xyxy[0].to_dict(orient="records")
        final_detected = None
        ref_area = 0
        for i, detect in enumerate(detection):
            if category[int(detect['class'])] == 'Bullseye':
                # ignore the bullseye
                continue

            x1 = int(detect['xmin'])
            y1 = int(detect['ymin'])
            x2 = int(detect['xmax'])
            y2 = int(detect['ymax'])
            width = x2 - x1
            height = y2 - y1

            bb_area = width * height  # Get the area of the box
            if ref_area < bb_area:  # Use the bigger box.
                ref_area = bb_area
                print("Updated area:", ref_area)
                final_detected = category[int(detect['class'])]
                print("Updated label:", final_detected)

        if final_detected is None or final_detected not in ['Left', 'Right']:
            print("Either nothing detected or Non-bullseye detected that is not Left/Right arrow")
            print("Should return something to STM to let them know that something is not right")
            return

        if final_detected == 'Left':
            return 'q'
        if final_detected == 'Right':
            return 'e'

    @app.route('/predict', methods=['POST'])
    def predict():
        print("previously detected", previously_detected)

        cs = -99
        # Get the image from the request
        print(request.files)
        image_file = request.files['image']
        image = Image.open(BytesIO(image_file.read()))
        # Convert the image to a tensor and do inference
        output = model(image).pred
        results = model(image)
        print("Results HERE:", results)
        detection = results.pandas().xyxy[0].to_dict(orient="records")
        ref_area = 0
        for i, detect in enumerate(detection):  # Xmin, ymin, Xmax, Ymax, conf, class id
            if detect['confidence'] < 0.31:
                continue
            x1 = int(detect['xmin'])
            y1 = int(detect['ymin'])
            x2 = int(detect['xmax'])
            y2 = int(detect['ymax'])
            width = x2 - x1
            height = y2 - y1
            bb_area = width * height  # Get the area of the box
            if ref_area < bb_area:  # Use the bigger box.
                ref_area = bb_area
                print("Updated area:", ref_area)
                cs = detect['class']  # CS = classID
            print("xyminmax", x1, y1, x2, y2)
            print("Current class", category[int(cs)])
            print("Current area:", ref_area)
        if cs != -99:  # If -99, means no image. else print the class identified
            if int(cs) not in previously_detected and category[int(cs)] != 'Bullseye':
                print("Class identified: ", category[int(cs)])
                previously_detected.append(int(cs))
                print(previously_detected)
            else:
                print("Bullseye or Has already been identified previously")
                # save image without BB being drawn
                save_dir = increment_path('runs/detect/exp', False, mkdir=True)
                image.save(str(save_dir) + '/image0.jpg')
                return '99'
        print(output)
        print("resultsxyxy", results.xyxy[0])

        # ONLY KEEP THE IMG WE WANT -- COMMENT AWAY IF DOESNT WORK
        if cs != -99:
            one_result = copy.deepcopy(results)
            # setattr(one_result, "pred", [results.pred[ref_index]])
            # setattr(one_result, "ims", [results.ims[ref_index]])
            # print("one_result pred", one_result.pred)
            one_result.save_mdp(cs)
        else:
            results.save()
        # print("ref_index", ref_index)
        # results.pred = [results.pred[ref_index]]
        # results.ims = [results.ims[ref_index]]
        # print("RESULTS", results)
        # results.save()

        num_detected = len(output[0])  # number of images detected
        print([label_mapping_id[category[int(output[0][i][-1])]] for i in range(len(output[0]))] if len(
            output[0]) else 'Nothing detected')

        x = [category[int(output[0][i][-1])] for i in range(len(output[0]))] if len(
            output[0]) else 'Nothing detected'
        print(x)
        if x == 'Nothing detected':
            return '99'
        elif x == ['Bullseye']:
            return '80'  # TBC!!!
        y = label_mapping_id[x[0]]  # Only returns one integer
        print("Mapped id :", y)
        print("Returning:", label_mapping_id[category[int(cs)]])
        # 80 - Bullseye
        # 99 - nothing
        # Return numbers because if return string incur some JSON ERROR
        return jsonify(label_mapping_id[category[int(cs)]])
        # return jsonify([category[int(output[0][i][-1])] for i in range(len(output[0]))] if len(
        # output[0]) else 'Nothing detected')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
