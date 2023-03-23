import os

from PIL import Image
import torch


def get_image_from(image_path: str) -> Image.Image:
    """Load image from a file. Close the file without losing the image"""
    with Image.open(image_path) as image:
        image.load()
    return image


def infer(image):
    category = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'S', 'T', 'U', 'V', 'W',
                'X', 'Y', 'Z', 'Bullseye', 'Down', 'Eight', 'Five', 'Four', 'Left', 'Nine', 'One', 'Right', 'Seven',
                'Six', 'Stop', 'Three', 'Two', 'Up']
    '''
    category = {0: 'A; ID 20', 1: 'B; ID 21', 2: 'Bullseye', 3: 'C; ID 22', 4: 'D; ID 23', 5: 'DownArrow; ID 37',
                6: 'E; ID 24',
                7: 'Eight; ID 18', 8: 'F; ID 25', 9: 'Five; ID 15', 10: 'Four; ID 14', 11: 'G; ID 26', 12: 'H; ID 27',
                13: 'LeftArrow; ID 39', 14: 'Nine; ID 19', 15: 'One; ID 11', 16: 'RightArrow; ID 38', 17: 'S; ID 28',
                18: 'Seven; ID 17', 19: 'Six; ID 16', 20: 'Stop; ID 40', 21: 'T; ID 29', 22: 'Three; ID 13',
                23: 'Two; ID 12',
                24: 'U; ID 30', 25: 'UpArrow; ID 36', 26: 'V; ID 31', 27: 'W; ID 32', 28: 'X; ID 33', 29: 'Y; ID 34',
                30: 'Z; ID 35'}
    '''

    label_mapping = {
        'A': 'A; ID 20', 'B': 'B; ID 21', 'C': 'C; ID 22', 'D': 'D; ID 23', 'E': 'E; ID 24', 'F': 'F; ID 25',
        'G': 'G; ID 26', 'H': 'H; ID 27', 'S': 'S; ID 28', 'T': 'T; ID 29', 'U': 'U; ID 30', 'V': 'V; ID 31',
        'W': 'W; ID 32', 'X': 'X; ID 33', 'Y': 'Y; ID 34', 'Z': 'Z; ID 35', 'bullseye': 'Bullseye',
        'downarrow': 'DownArrow; ID 37', 'eight': 'Eight; ID 18', 'five': 'Five; ID 15', 'four': 'Four; ID 14',
        'leftarrow': 'LeftArrow; ID 39', 'nine': 'Nine; ID 19', 'one': 'One; ID 11', 'rightarrow': 'RightArrow; ID 38',
        'seven': 'Seven; ID 17', 'six': 'Six; ID 16', 'stop': 'Stop; ID 40', 'three': 'Three; ID 13',
        'two': 'Two; ID 12', 'uparrow': 'UpArrow; ID 36'
    }


    model_path = r'/Users/abc/Downloads/best.pt'
    yolo_v5_dir = os.getcwd()
    model = torch.hub.load(yolo_v5_dir, 'custom', path=model_path, source='local')
    output = model(image).pred
    return [category[int(output[0][i][-1])] for i in range(len(output[0]))] if len(output[0]) else 'Nothing detected'


if __name__ == "__main__":
    # CONFIGURATIONS: remember to change

    use_prev = True

    images_source = r'/Users/abc/Downloads/mdp_images'

    if use_prev:
        best_weight_filename = "best.pt"
    else:
        best_weight_filename = "best_13feb.pt"

    test_image_path = r'/Users/abc/Downloads/content/datasets/MDP_Proj-1/test/images/IMG_20230130_192715_jpg.rf.1be6043ac7e4e386c947c3ccea1544a8.jpg'
    # test_image_path = r'/Users/abc/Downloads/content/datasets/MDP_Proj-1/test/images/IMG_20230130_192735_jpg.rf.070727a556d8609095e372e5f00b2784.jpg'
    img = get_image_from(test_image_path)
    res = infer(img)
    print(res)
