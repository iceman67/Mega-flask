from flask import Flask
import time

import threading
from w1thermsensor import W1ThermSensor
import json

currentTemp = {}

class ThermThreading(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        self.w1sensor = dict()

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def get():
        global currentTemp 
        currentTemp = self.w1sensor
        if self.w1sensor is None:
           return []
        else:
           return  self.w1sensor

    def run(self):
        """ Method that runs forever """
        global currentTemp
        while True:
            # Do something
            print('Doing something imporant in the background')
            for sensor in W1ThermSensor.get_available_sensors():
               self.w1sensor[sensor.id] =  sensor.get_temperature()
            currentTemp = self.w1sensor
            time.sleep(self.interval)

app = Flask(__name__)
 
@app.route("/w1-dev")
def w1term_dev():
    global currentTemp
    L = [] 
    for k in currentTemp.keys():
       L.append(k)
    return  (json.dumps(L)) 


@app.route("/w1")
def w1term():
    global currentTemp
    return  (json.dumps(currentTemp)) 

# return a string with commar seperated temperatures
def build_temp_str(w1sensor):
    L = []
    for k, v in w1sensor.items():
      print ("({0}, {1})".format(k,v))
      L.append(v)
    temp_str = ','.join(str(x) for x in L)
    return temp_str
 
   
@app.route("/")
def hello():
    w1sensor = dict()
    for sensor in W1ThermSensor.get_available_sensors():
      w1sensor[sensor.id] =  sensor.get_temperature()

    return build_temp_str(w1sensor)
    #return  (json.dumps(L))  # list of termperatures
    #return  (json.dumps(w1sensor)) # dictionary of a pair of sensor id and its temperature

 
if __name__ == "__main__":
   example = ThermThreading()
   time.sleep(3)
   app.run(host='0.0.0.0', port=8000)
