import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())
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
    clientsocket.send("data is sent new".encode())
