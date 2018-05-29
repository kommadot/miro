import RPi.GPIO as io
import time

class screensaverAPI():
	def __init__(self):
		#self.time=10
		io.setmode(io.BCM)
		self.pin = 7
		io.setup(self.pin, io.IN)

	def test(self):
		#time.sleep(self.time)
		cnt = 0
		while True:
			if io.input(self.pin)==True:
				print ("detacted!")
				cnt += 1
				if cnt == 3:
					break
			else:
				cnt = 0
			time.sleep(0.7)
		print ("success!")
