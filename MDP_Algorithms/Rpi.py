import socket

def send_data(data):
    # create a socket object
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = socket.socket()

    # get local machine name
    host = socket.gethostbyname(socket.gethostname())
    print("HOST",host)
    port = 1234

    # raspberry pi's IP address or hostname
    pi_host = "192.168.23.23"
    serversocket.bind((host, port))

    serversocket.listen(5)
    (clientsocket, address) = serversocket.accept()
    # connect to the raspberry pi
    # s.connect((pi_host, port))

    # send the data
    clientsocket.send(data.encode())
    # s.sendall(data.encode('utf-8'))

    # receive the response from the raspberry pi
    # response = s.recv(1024)
    response = clientsocket.recv(1024)

    # close the socket
    clientsocket.close()

    # return the response
    return response.decode('utf-8')
# send_data("HI")
# print(socket.gethostname())
# print("sent")