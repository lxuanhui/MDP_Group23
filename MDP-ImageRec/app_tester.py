import os

import requests


def imagerec(image_path):
    # Set the URL of the predict endpoint
    url = 'http://localhost:5000/predict'

    # Set the image file path
    # image_path = r'/Users/abc/Downloads/content/datasets/MDP_Proj-1/test/images/IMG_20230130_192715_jpg.rf.1be6043ac7e4e386c947c3ccea1544a8.jpg'

    # Load the image file into a bytes object
    with open(image_path, 'rb') as f:
        image_bytes = f.read()


    # Create a dictionary of files to send with the request
    files = {'image': ('image.jpg', image_bytes)}

    # Make the request with the files dictionary
    response = requests.post(url, files=files)
    return response.content.decode()


if __name__ == "__main__":
    print(imagerec('server_image.jpg'))
    # for img in os.listdir('/Users/abc/Downloads/mdp_test_images'):
    #     x = imagerec((os.path.join('/Users/abc/Downloads/mdp_test_images', img)))
    #     print (img, x, "type:", type(x))