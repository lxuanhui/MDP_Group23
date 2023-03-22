#!/usr/bin/python
##Sending w,a,s,d movement from android to STM
import serial, string
import socket

import time

output = " "
#ser = serial.Serial('/dev/ttyUSB0', 115200,8,'N',1,timeout=1)
serSTM = serial.Serial('/dev/ttyUSB0', 115200,timeout=1) ##STM Board
serBluetooth = serial.Serial('/dev/rfcomm0',9600)
"""
s = socket.socket()
host = "192.168.23.24"
port = 1234
s.connect((host,port))

s.send('{"obstacle":[16,[2,6],N]}'.encode())
data = s.recv(1024).decode()
print (data)
s.close
buffer = b'' #Bytes
"""

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

"""
x =b''
while True:
	## print(serSTM.readline())
	serSTM.write(b'w100)')
	print("sent h1")
	#print(serSTM.readline())
	
	while (x != b'next'):
		x = serSTM.readline()
	x = b''
	time.sleep(2)
	serSTM.write(b's100)')
	print("Sent S100")
	x =b''
	"""
	#print(serSTM.readline())
	#print(x)
	#if(x == b'next'):
#		print("OK")
	
	#while x == '':
	#	x = serSTM.readline()
	#	print(x)
	#	if (x != ''):
	#		break
	#print("exited")
	
	#time.sleep(5)
	#serSTM.write(b's100)')
	#print("Sent r100")
	#time.sleep(5)
"""
	serSTM.write(b'h2')
	print("sent h2")
	time.sleep(5)
	serSTM.write(b'[s,50)')
	print("sent s,50)")
	time.sleep(60)
	serSTM.write(b'w,50)')
	time.sleep(60)
	
"""
"""
TODO !!!
Android send coordinates to RPI
RPI Send to LAPTOP (For path processing)
Laptop returns path 
Path must send to STM
!!!
"""	



#Receive from BT android & Send to STM
# test for checklist
buffer = b'' #Bytes
while True:
	result = serBluetooth.read()
	buffer = buffer + result
	if (result == b'#'):
		print(buffer[0:-1]) ## Receive whole string, print without last char
		
		serSTM.write(buffer[0:-1]) ## Sending to STM Board
		print("Sent to STM")
		buffer = b''
	
		

	
	
"""
while True:
	result = serBluetooth.read()
	print (result)
	"""
#output = " "
		
