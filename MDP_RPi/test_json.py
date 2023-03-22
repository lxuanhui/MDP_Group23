import serial, string
import socket
import json

import time

output = " "
#ser = serial.Serial('/dev/ttyUSB0', 115200,8,'N',1,timeout=1)
#serSTM = serial.Serial('/dev/ttyUSB0', 115200,timeout=1) ##STM Board
#serBluetooth = serial.Serial('/dev/rfcomm0',9600)

s = socket.socket()
host = "192.168.23.24"
port = 1234
s.connect((host,port))


#s.send('{"obstacle":[16,[2,6],N]}'.encode())
s.send('test_from_rpi'.encode())
#Receive data
data = b''

#data = s.recv(8192).decode()
while True:
#	#x = x + data
	part = s.recv(4096)
	data += part

	if len(part) <= 4096:
		break
	



print ("Original Data:", data)
#
# print("type of data: " , type(data))
# #Set to json
# json_type = json.loads(data)
# print(json_type)
# #for i in json_type:
# #	print(i["name"])
#
# #print("REASD",json_type[0])
# for datas in json_type:
# 			#print(type(datas["movement"])) # Send to STM
# 			#print(type(datas["obstacle"])) # Obs ID
# 			#print(type(datas["reached"])) # 0 - On the way, 1 - reached obstacle
# 			#print(type(datas["robotPosition"])) # Send to
#
# 			#print((datas["movement"]))
# 			print(datas)
#

#print(json_type)
#print(json_type["name"])

#s.close
#buffer = b'' #Bytes
