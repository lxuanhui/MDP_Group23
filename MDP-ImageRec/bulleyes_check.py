import os
import socket
import imagesize

from bullseye_checker import imagerec, do_tiling

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

        # TODO: When entire image rec process is done, need to show tiled image!!
        # RPI needs to send me something, then I trigger POST request to tile image??
        # actually, don't even need post request?
        width, height = imagesize.get('server_image.jpg')
        if width == 64 and height == 64:
            client_socket.close()
            break  # dont do image rec if it's the small square photo sent

        # do image rec
        print("Doing image rec..")
        # image_id = imagerec('server_image.jpg')
        imagerec('server_image.jpg')

        # print(image_id)
        # client_socket.send(image_id.encode())
        print("Testt2")
        client_socket.send("ASD".encode())
        # print("image id sent success")
        print("testq")

        num_photos += 1

        client_socket.close()

    # trigger the tiling, but need the number of images captured!! How to get ahhh
    print("TILING TRIGGERED")
    # print(do_tiling(num_photos))
    do_tiling(num_photos)
