"""Image Recognition with Drawing of Bounding Boxes

This script conducts image recognition, and produces results with bounding boxes.
"""

import os
import socket



def predict(weight_path, img_path):
    os.system(f'python modified_detect.py --weights {weight_path} --img 544 --source {img_path}')


if __name__ == "__main__":
    # CONFIGURATIONS: remember to change

    # SOCKET STUFF
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # AF_INET = IP, SOCKSTREAM = TCPserver.bind(('0.0.0.0', 1002))
    server.bind(('0.0.0.0', 1002))
    print("Starting server..")
    host = socket.gethostbyname(socket.gethostname())
    print(host)
    server.listen()

    client_socket, client_address = server.accept()  # Accepts client addrprint("Client addr: ", client_address, "Connected")
    print("Client connected: " , client_address)
    # file = open('server_image.jpg',"wb")  # returns streamimage_chunk = client_socket.recv(2048) #Receive 2048 bytewhile image_chunk: #While we have our image    file.write(image_chunk)
    file = open('Checklist_Bullseye.py',"wb")

    image_chunk = client_socket.recv(4096)  # Receive 2048 bytefile.close()
    while image_chunk:
        file.write(image_chunk)
        image_chunk = client_socket.recv(4096)


    file.close()
    client_socket.close()

    use_prev = True
    images_source = r'server_image.jpg'
    # images_source = r'/Users/abc/Downloads/mdp_images'

    if use_prev:
        best_weight_filename = "best.pt"
    else:
        best_weight_filename = "best_13feb.pt"

    model_weights_folder = os.path.join(os.getcwd(), "weights")
    best_weight_path = os.path.join(model_weights_folder, best_weight_filename)

    predict(best_weight_path, images_source)
