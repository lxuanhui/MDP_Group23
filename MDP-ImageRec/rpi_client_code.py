import socket

s = socket.socket()
# host = "192.168.23.45"
host = "0.0.0.0"
port = 1234
s.connect((host, port))

# open image
img_file = open(r'/Users/abc/Downloads/mdp_images/w0011.jpg', 'rb')
img_data = img_file.read()
size = len(img_data)

# txt file
with open(r'/Users/abc/yolov5/testfile.txt', 'r') as f:
    content = f.read()
    print(content)

s.send(content.encode())

s.sendall(img_data)

s.send('randomData'.encode())
data = ''
data = s.recv(1024).decode()
print(data)
s.close()