import RPi.GPIO as io
import time

io.setmode(io.BCM)

pin = 25

io.setup(25, io.IN)

while 1:
    if io.input(25):
        print ("Detected")
    else:
        print ("Not Detected")

    time.sleep(0.5)

GPIO.cleanup()
