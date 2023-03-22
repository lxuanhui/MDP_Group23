import socket
from picamera import PiCamera
from time import sleep
import os
camera = PiCamera()



client = socket.socket(socket.AF_INET,  socket.SOCK_STREAM) 
client.connect(('192.168.23.45',1002)) 

camera.resolution = (64,64)
camera.capture('/home/mdp-group23/Desktop/square_img.jpg')

file = open('/home/mdp-group23/Desktop/square_img.jpg' ,'rb')
#file = open('Checklist_Bullseye.py' , 'rb')


image_data = file.read(4096)

while image_data:
	client.send(image_data)
	image_data = file.read(4096)
	#print("HERE")

#os.remove("imagerec_result.txt")
print("Send success")
file.close()

#data = client.recv(1024)
#print(data)

client.close()
#client = socket.socket(socket.AF_INET,  socket.SOCK_STREAM) 
#client.connect(('192.168.23.45',1002))
#data = client.recv(1024)
#print(data)
