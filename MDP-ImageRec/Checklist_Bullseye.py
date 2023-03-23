#!/usr/bin/python

import serial, string
import socket

import time
from picamera import PiCamera
from time import sleep

camera = PiCamera()

output = " "
#ser = serial.Serial('/dev/ttyUSB0', 115200,8,'N',1,timeout=1)
serSTM = serial.Serial('/dev/ttyUSB0', 115200,timeout=1) ##STM Board
#serBluetooth = serial.Serial('/dev/rfcomm0',9600)
"""
s = socket.socket()
host = "192.168.23.24"
port = 1234
s.connect((host,port))

#s.send('{"obstacle":[16,[2,6],N]}'.encode())
#data = s.recv(1024).decode()
#print (data)
#s.close
#buffer = b'' #Bytes
"""

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('192.168.23.45', 1002))

""" while True:
	print ("-----")
	while output != "":
		output = ser.readline()
		ser.write(b'a')
		print (output)
"""

## Sender must send '#' behind

#serBluetooth.write(b'{"status" : "<hello>"}') ##SEND TO BT
#TEST FOR CONNECTION TO STM
while True:

	obstacle =  serSTM.readline()
	# If obstacle is infront sent by STM
	if obstacle == "front":

		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(('192.168.23.45', 1002))

		#Take image
		camera.capture('/home/mdp-group23/Desktop/bull_check.jpg')
		file = open('bull_check.jpg', 'rb')
		image_data = file.read(4096)
		#Send image over to laptop
		while image_data:
			client.send(image_data)
			image_data = file.read(4096)
			print("Succesfully send image")


		file.close()
		#Close connection with server
		client.close()

		#Wait for laptop image rec
		sleep(3)
		#Read text file to know which image is captured
		with open('imagerec_result.txt') as s:
			rec_image = s.read()

		##Send to STM which image is detected
		serSTM.write(b'rec_image')
		#Reset obstacle variable
		obstacle = ""


#serSTM.write(b'w,1)')
#	time.sleep(200000)
	
"""
TODO !!!
Android send coordinates to RPI
RPI Send to LAPTOP (For path processing)
Laptop returns path 
Path must send to STM
!!!
"""	


"""
#Receive from BT android & Send to STM
# test for checklist

while True:
	result = serBluetooth.read()
	buffer = buffer + result
	if (result == b'#'):
		print(buffer[0:-1]) ## Receive whole string, print without last char
		serSTM.write(buffer[0:-1]) ## Sending to STM Board
		buffer = b''
	"""	
		

	
	
"""
while True:
	result = serBluetooth.read()
	print (result)
	"""
#output = " "
		
