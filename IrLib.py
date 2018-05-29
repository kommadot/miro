import RPi.GPIO as io
import time

io.setmode(io.BCM)

pin = 23

io.setup(23, io.IN)

while 1:
    if io.input(23)==True:
        print ("Detected")
    else:
        print ("Not Detected")

    time.sleep(0.5)

GPIO.cleanup()
