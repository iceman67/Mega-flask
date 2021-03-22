from therm import ThermThreading
from w1thermsensor import W1ThermSensor


import time
import json

t = ThermThreading()

while True:
   if  len(t.w1sensor) ==  len(W1ThermSensor.get_available_sensors()):
      print ( len(t.w1sensor))
      json.dumps(t.w1sensor)
      break
   else:
      time.sleep(1)

