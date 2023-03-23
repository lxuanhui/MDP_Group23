"""Image Recognition with Drawing of Bounding Boxes

This script conducts image recognition, and produces results with bounding boxes.
"""

import os


def predict(weight_path, img_path):
    os.system(f'python modified_detect.py --weights {weight_path} --img 544 --source {img_path}')


if __name__ == "__main__":
    # CONFIGURATIONS: remember to change

    use_prev = True

    images_source = r'/Users/abc/Downloads/mdp_test_images_anh'

    if use_prev:
        best_weight_filename = "best.pt"
    else:
        best_weight_filename = "best_from_kai.pt"

    model_weights_folder = os.path.join(os.getcwd(), "weights")
    best_weight_path = os.path.join(model_weights_folder, best_weight_filename)

    predict(best_weight_path, images_source)
