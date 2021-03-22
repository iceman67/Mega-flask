from flask import Flask, request
'''
import threading
'''
from w1thermsensor import W1ThermSensor
import json

# wrapper class for w1thermsensor as a thread
from therm import ThermThreading
import time


# return a string with commar seperated temperatures
def build_temp_str(w1sensor):
    L = []
    for k, v in w1sensor.items():
      print ("({0}, {1})".format(k,v))
      L.append(v)
    temp_str = ','.join(str(x) for x in L)
    return temp_str
 
WATCHDOG_DELAY = 0.2 
MAX_TRY = 2

app = Flask(__name__)
@app.route("/w1-dev")
def w1term_dev():
    global t
    cnt = 0
    available = False
    while True:
       if len(t.w1sensor) ==  t.num_w1sensor:
          available = True
          break
       else:
         if cnt > MAX_TRY: 
            break
         cnt += 1
         time.sleep(WATCHDOG_DELAY)

    if available is False: 
       return json.dump("[NA]") 
    else:
       L = [] 
       for k in t.w1sensor.keys():
          L.append(k)
       return  (json.dumps(L)) 


@app.route("/w1-id")
def w1term_id():
    global t
    sid = request.args.get('id')
    return (json.dumps(t.w1sensor[sid]))


@app.route("/w1")
def w1term():
    global t
    cnt = 0
    available = False
    while True:
       if len(t.w1sensor) ==  t.num_w1sensor:
          available = True
          break
       else:
         if cnt > 2: 
            break
         cnt += 1
         time.sleep(WATCHDOG_DELAY)

    if available is False: 
       return json.dump("[NA]") 
    else: 
        return (json.dumps(t.w1sensor)) 

   
@app.route("/")
def hello():
    w1sensor = dict()
    for sensor in W1ThermSensor.get_available_sensors():
      w1sensor[sensor.id] =  sensor.get_temperature()

    return build_temp_str(w1sensor)
    #return  (json.dumps(L))  # list of termperatures
    #return  (json.dumps(w1sensor)) # dictionary of a pair of sensor id and its temperature


def get_Host_name_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name) 
        print("Hostname :  ",host_name) 
        print("IP : ",host_ip) 
    except: 
        print("Unable to get Hostname and IP") 

    return host_ip 

from sensor.LCD1602 import LCD1602
def display_LCD(ip, temp):
   # I2C bus=1, Address=0x27
   lcd = LCD1602(1, 0x27)

   lcd.display("IP : {}".format(ip), 1)   # my name on line 1
   lcd.display("Temp : {}".format(temp), 2)  # my city on line 2
   time.sleep(10) 
   lcd.clear()

 
if __name__ == "__main__":
   import requests
   import socket 

   t = ThermThreading()
   time.sleep(3)


   app.run(host='0.0.0.0', port=8000)
