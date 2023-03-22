#!/usr/bin/python

import serial, string

output = " "
#ser = serial.Serial('/dev/ttyUSB0', 115200,8,'N',1,timeout=1)
ser = serial.Serial('/dev/ttyUSB0', 115200,timeout=1)
while True:
	print ("-----")
	while output != "":
		output = ser.readline()
		ser.write(b'a')
		print (output)

		
	#output = " "
		
