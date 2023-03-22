from picamera import PiCamera
from time import sleep


camera = PiCamera()
camera.start_preview()

camera.capture('/home/mdp-group23/Desktop/test.jpg')
camera.stop_preview()

