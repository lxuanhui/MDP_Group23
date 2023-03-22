#!/usr/bin/python

from picamera import PiCamera
from time import sleep
import os
camera = PiCamera()

import serial, string
import socket
import json
#import time

output = " "
#ser = serial.Serial('/dev/ttyUSB0', 115200,8,'N',1,timeout=1)
serSTM = serial.Serial('/dev/ttyUSB0', 115200,timeout=1) ##STM Board
serBluetooth = serial.Serial('/dev/rfcomm0',9600) #Android


s = socket.socket()
#host = "192.168.23.35" #Algo team laptop (xuanhui)
host = "192.168.23.25" # brandon
port = 1234
s.connect((host,port)) #Connect to algo laptop

#
# print("From STM" , serSTM.readline())
# x = b''
# while ( x != b'photo'):
# 	x =  serSTM.readline()
		
buffer = b''
x = b''
count = 0
resend = 0
while True:
	#Receive coordinates from BT
	print("Receiving from bluetooth..")
	result = serBluetooth.read()
	buffer = buffer + result
	#to indicate end of string
	if (result == b'#'):
		print("Bluetooth received: ", buffer[0:-1]) #Receive whole string, print without last char
		s.send(buffer[0:-1]) #Send whatever received from BT To Algo team
		#Receive data from ALGO
		# data = s.recv(1024).decode()
		#print data from Laptop(ALGO Team)
		# print ("Received data from algo:", data, "type:", type(data)) #Should be string
		#Read JSON data, sent by ALGO
		#time.sleep(2)
		sleep(4)
		with open('route.json','r') as f:
			datas = json.load(f)
		# parse data received from Algo
		#instructions = data.split('#')
		#json_data = json.loads(data)
		print(datas)
		for data in datas: # Loop through all the commands
			print("Count:" , count)
			count += 1
			if data["reached"] == 0: #Havent reach obstacle, send stm commands
				#Send STM Movement
				print("Data Type:", type(data["movement"])) #Print the type of data)
				print("Data sent to STM: ", data["movement"])
				serSTM.write(str.encode(data['movement'])) # Send to STM the movement
				# serBluetooth.write(str.encode(data["robotPosition"]))
				print("Data sent to Bluetooth", r'{{"robotPosition":{0}}}'.format(data["robotPosition"]))
				serBluetooth.write(str.encode(r'{{"robotPosition":{0}}}'.format(data["robotPosition"])))
				print("Successfully Sent To STM & BT")
				# STM Waiting on next movement command
				#resend = 0
				while (x != b'next'):
					x = serSTM.readline()
					resend += 1
					if (resend == 20):
						serSTM.write(str.encode(data['movement'])) #resend the data to STM
						print("Resent Data :" ,data["movement"])
						resend=0
						x=b''
					print("Waiting for STM")
					#sleep(1)
				x = b''
				resend = 0
			else: #Reached obstacle, likely robot is infront
				# if ( x == b'next'): #And if ROBOT is infront of Obstacle,
				client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				client.connect(('192.168.23.45', 1002))
				print("Server Connected")
				#Take image
				camera.capture('/home/mdp-group23/Desktop/check_image.jpg')
				file = open('check_image.jpg', 'rb')
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
				sleep(5)
				#Read text file to know which image is captured
				with open('imagerec_result.txt') as s:
					rec_image = s.read()
				print("Received image" , rec_image , "Type: " , type(rec_image))
				if (rec_image == "['Bullseye']"):
					print("BULL LOOP")
					pass
				else: #if not bullseye, send to BT WHAT IMAGE IS BEING DETECTED AT WHAT OBSTACLE
					serBluetooth.write(str.encode(r'{{"target":[{0},{1}]}}'.format(data["obstacle"],rec_image)))##SEND TO BT
					print("Obstacle ID and image ID: " + rec_image + "Sent")
					# time.sleep(2)


			# print(type(datas["m"])) #Mvement
			# print(type(datas["obstacle"])) # Obs ID
			# print(type(datas["reached"])) # 0 - On the way, 1 - reached obstacle
			# print(type(datas["robotPosition"])) # Send to BT

		#print("instructions", instructions)
		#for instruction in instructions[:-1]: # ignore the last element
			#print("send stuff to STM here - to be implemented")
			#print(instruction)
			#serSTM.write(str.encode(instruction))
			# wait for acknowledgment from STM??
		#s.close
		#Reset buffer
		buffer = b''

		# DONE LOOPING THROUGH ALL COMMANDS, SEND SQUARE IMG TO LAPTOP AS SIGNAL TO DO TILING
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(('192.168.23.45', 1002))
		print("Server Connected")

		file1 = open('square_img.jpg', 'rb')
		image_data1 = file1.read(4096)
		#Send image over to laptop
		while image_data1:
			client.send(image_data1)
			image_data1 = file1.read(4096)
			print("Succesfully send SQUARE image")
		file1.close()
		#Close connection with server
		client.close()

#	data = s.recv(1024).decode()
#	print(data)
#	s.close
