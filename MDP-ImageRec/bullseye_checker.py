import os
import subprocess

import requests
import json


def do_tiling(num_photos):
    # Set the URL of the predict endpoint
    url = 'http://localhost:5000/showtiled'
    response = requests.post(url, json={"num_photos": num_photos})
    print("HELLO", response.content.decode())
    # return json.loads(response.content.decode())


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

    # Parse the JSON response
    result = json.loads(response.content.decode())

    print("Printing results:", result)
    # return result

    with open('imagerec_result.txt', 'w') as f:
        f.write(str(result))
        # if 'Bullseye' in result:
        #     print("write here")
        #     # TODO Need to fix
        #     f.write(r"['Bullseye']")
        # else:
        #     f.write(str(result))

    # Send image result to rpi as txt file
    p = subprocess.Popen(["scp", "imagerec_result.txt", "mdp-group23@192.168.23.23:/home/mdp-group23/Desktop"])
    sts = os.waitpid(p.pid, 0)
    print("successfully send to rpi")

    # with open('imagerec_result.txt') as s:
    #     print(s.read())

    # print(result)

    # folder_path = r'/Users/abc/Downloads/OneDrive-2023-02-21'
    # file_list = os.listdir(folder_path)

    # # Print the file names
    # for file_name in file_list:
    #     image_path = os.path.join(folder_path, file_name)
    #     with open(image_path, 'rb') as f:
    #         image_bytes = f.read()
    #
    #     # Create a dictionary of files to send with the request
    #     files = {'image': ('image.jpg', image_bytes)}
    #
    #     # Make the request with the files dictionary
    #     response = requests.post(url, files=files)
    #
    #     # Parse the JSON response
    #     result = json.loads(response.content.decode())
    #     print(file_name, result)
