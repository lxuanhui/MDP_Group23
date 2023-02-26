import os
import socket

from bullseye_checker import imagerec


if __name__ == "__main__":
    # CONFIGURATIONS: remember to change

    # SOCKET STUFF
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM)  # AF_INET = IP, SOCKSTREAM = TCPserver.bind(('0.0.0.0', 1002))
    server.bind(('0.0.0.0', 1002))
    print("Starting server..")
    host = socket.gethostbyname(socket.gethostname())
    print(host)
    server.listen()

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
        imagerec('server_image.jpg')

        client_socket.close()
