#!/usr/bin/python
##IMPORTANT TO NOTE!!
## ANDROID AND LAPTOP MUST BE CONNECTED FIRST

import serial, string
import socket

import time

output = " "
#ser = serial.Serial('/dev/ttyUSB0', 115200,8,'N',1,timeout=1)
#serSTM = serial.Serial('/dev/ttyUSB0', 115200,timeout=1) ##STM Board
serBluetooth = serial.Serial('/dev/rfcomm0',9600)

#Hard coded
#s.send('{"obstacle":[16,[2,6],N]}'.encode())
#Receive data
#data = s.recv(1024).decode()
#print (data)
#s.close
#buffer = b'' #Bytes


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
#while True:
	## print(serSTM.readline())
	#serSTM.write(b'k,1)')
	#time.sleep(200000)
	
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
		

buffer = b''
while True:
	#Receive coordinates from BT
	result = serBluetooth.read()
	buffer = buffer + result
	#to indicate end of string
	if (result == b'#'):
		print(buffer[0:-1]) #Receive whole string, print without last char
		#s.close
		#Reset buffer
		buffer = b''
		time.sleep(5)
		break

serBluetooth.write(b'End Challenge')
	
	
"""
while True:
	result = serBluetooth.read()
	print (result)
	"""
#output = " "
		
