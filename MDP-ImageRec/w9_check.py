import json
import os
import socket
import subprocess

import requests


def do_tiling(num_photos):
    # Set the URL of the predict endpoint
    url = 'http://localhost:5000/showtiled'
    response = requests.post(url, json={"num_photos": num_photos})
    print("HELLO", response.content.decode())
    # return json.loads(response.content.decode())

def l_r_imagerec(image_path):
    # Set the URL of the predict endpoint
    url = 'http://localhost:5000/detect_w9_o1'

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

    # Send image result to rpi as txt file
    p = subprocess.Popen(["scp", "imagerec_result.txt", "mdp-group23@192.168.23.23:/home/mdp-group23/Desktop"])
    sts = os.waitpid(p.pid, 0)
    print("successfully send to rpi")
    if str(result) in ['38', '39']:
        return True
    else:
        return False


if __name__ == "__main__":

    # SOCKET STUFF
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM)  # AF_INET = IP, SOCKSTREAM = TCPserver.bind(('0.0.0.0', 1002))
    server.bind(('0.0.0.0', 1002))
    print("Starting server..")
    host = socket.gethostbyname(socket.gethostname())
    print(host)
    server.listen()

    num_photos = 0

    while True:
        client_socket, client_address = server.accept()  # Accepts client addrprint("Client addr: ", client_address, "Connected")
        print("Client connected: ", client_address)
        file = open('server_image.jpg',
                    "wb")  # returns streamimage_chunk = client_socket.recv(2048) #Receive 2048 bytewhile image_chunk: #While we have our image    file.write(image_chunk)

        image_chunk = client_socket.recv(4096)  # Receive 2048 bytefile.close()
        while image_chunk:
            file.write(image_chunk)
            image_chunk = client_socket.recv(4096)

        file.close()

        # do image rec
        print("Doing image rec..")
        # image_id = imagerec('server_image.jpg')
        success_photo = l_r_imagerec('server_image.jpg')
        print("Photo successfully taken is", success_photo)
        if success_photo:
            num_photos += 1

        if num_photos == 2:
            client_socket.close()
            break

        client_socket.close()

    # trigger the tiling, but need the number of images captured!! How to get ahhh
    print("TILING TRIGGERED")
    # print(do_tiling(num_photos))
    print(num_photos)
    do_tiling(num_photos)
