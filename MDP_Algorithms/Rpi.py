# import socket
#
# def send_data(data):
#     # create a socket object
#     serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s = socket.socket()
#
#     # get local machine name
#     host = socket.gethostbyname(socket.gethostname())
#     print("HOST",host)
#     port = 1234
#
#     # raspberry pi's IP address or hostname
#     pi_host = "192.168.23.23"
#     serversocket.bind((host, port))
#
#     serversocket.listen(5)
#     (clientsocket, address) = serversocket.accept()
#     # connect to the raspberry pi
#     # s.connect((pi_host, port))
#
#     # send the data
#     clientsocket.send(data.encode())
#     # s.sendall(data.encode('utf-8'))
#
#     # receive the response from the raspberry pi
#     # response = s.recv(1024)
#     response = clientsocket.recv(1024)
#
#     # close the socket
#     clientsocket.close()
# #
#     # return the response
#     return response.decode('utf-8')
# # send_data("HI")
# # print(socket.gethostname())
# # print("sent")
# def receive_data(host, port):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind((host, port))
#         s.listen()
#         conn, addr = s.accept()
#         with conn:
#             print('Connected by', addr)
#             while True:
#                 data = conn.recv(1024)  # Receive up to 1024 bytes of data
#                 if not data:
#                     break
#                 # Do something with the received data
#                 print('Received:', data.decode())
#                 return data.decode()
#
# obs = receive_data('0.0.0.0',1234)
# print("FROM RPI " , obs)

import socket
from time import sleep

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())
# host = socket.gethostbyname("")
port = 1234
print(host)
print(port)
serversocket.bind((host, port))

serversocket.listen(5)
print('server started and listening')
while 1:
    (clientsocket, address) = serversocket.accept()
    print(address)
    print("connection found!")
    data = clientsocket.recv(1024).decode()
    print(data)
    sleep(5)

    clientsocket.send("This is the path".encode())


