from w1thermsensor import W1ThermSensor
import time

total = 0
c = dict()
def current_temperature(getc):
    c =  getc
    global total 
    total += 1
    print ("total ", total)

def get_temperature(i):
   w1sensor = dict()
   for sensor in W1ThermSensor.get_available_sensors():
      w1sensor[sensor.id] =  sensor.get_temperature() 
      print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))

#   current_temperature(w1sensor)
   time.sleep(i)

   

if __name__ == "__main__":
   import threading
   
   i = 1
   t = threading.Thread(target=get_temperature, args=(i,))
#  t.daemon = True
   t.start()

   print ("getting temperature")
    
   for k, v in c.items():
      print ("({0}, {1})".format(k,v))

   t.join()
