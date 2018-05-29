import RPi.GPIO as io
import time

io.setmode(io.BCM)

pin = 7

io.setup(pin, io.IN)

while 1:
    if io.input(pin)==True:
        print ("Detected")
    else:
        print ("Not Detected")

    time.sleep(0.5)

GPIO.cleanup()
