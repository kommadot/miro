import RPi.GPIO as io
import time

io.setmode(io.BCM)

pin = 24

io.setup(24, io.IN)

while 1:
    if io.input(24):
        print ("Detected")
    else:
        print ("Not Detected")

    time.sleep(0.5)

GPIO.cleanup()
