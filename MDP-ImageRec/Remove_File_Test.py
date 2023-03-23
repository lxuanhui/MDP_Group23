import os
import time


try:
    os.remove('asd.txt')
    print("Successfullly removed TXT")
except OSError:
    print("File does not exist")
    pass


while not os.path.exists('asd.txt'):
    time.sleep(1)
    print("waiting")

with open('asd.txt','r') as f:
    "opening file:"
    print(f.read())

