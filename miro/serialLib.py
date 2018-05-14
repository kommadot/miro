import serial

class serialAPI():
   def __init__(self):
      self.ser=serial.Serial('/dev/ttyAMA0', 115200)

   def connectTest(self):      #connection test
      self.ser.write(b'V')

      output = self.ser.readline()
      output = output.decode()[:-1]
      if output.find("OK") != -1:
         return "Success"
      else:
         return "Fail"

   def login(self):
      self.ser.write(b'V+LOGIN9876')

      output = self.ser.readline()
      output = output.decode()[:-1]
      if output.find("LOGIN") != -1:
         return "Success"
      else:
         return "Fail"

   def logout(self):
      self.ser.write(b'V+LOGOUT9876')

      output = self.ser.readline()
      output = output.decode()[:-1]
      if output.find("LOGOUT") != -1:
         return "Success"
      else:
         return "Fail"
   
   def userRegistration(self, userNum):
      sendStr = "V+UFREG" + str(userNum)
      self.ser.write(bytes(sendStr, encoding = 'ascii'))

      self.ser.readline()
      while True:
         output = self.ser.read()
         print (output)
         if output == b'O' or output == b'F' or output == b'E':
            break
      output = self.ser.readline().decode()[:-1]
      if output.find("ALI") != -1:
         return "Fail"
      elif output.find("K") != -1:
         return "Success"
      elif output.find("ULL") != -1:
         return "Full"
      elif output.find("XIST") != -1:
         return "Exist"
      else:
         return output

   def userRecognition(self):
      self.ser.write(b'V+UFREC')
      output = self.ser.readline().decode()[:-1]
      if output.find("AIL") != -1:
         return "Fail"
      else:
         return output[-4:]


