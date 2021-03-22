from flask import Flask, request
from ttelepot2 import Ttelepot
import sys
'''
3.1
- apply argv[1] as port number
- handle multiple connection  
- waiting time for therm thread to 0.5 second 

3.2
- handle command line arguments for server's port number
- handle no available sensors [NA]

3.3
- handle LED (ttelepot.py ) 
- handle LCD  (therm.py)
- client (ds1820_flask3_client.py)

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

@app.route("/on")
def on():
    global tele
    tele.on_red_led(21)


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

    if len(w1sensor) == 0:
       return "[NA]"
    else:
       return build_temp_str(w1sensor)
    #return  (json.dumps(L))  # list of termperatures
    #return  (json.dumps(w1sensor)) # dictionary of a pair of sensor id and its temperature

'''
disply IP and temp on LCD 
'''

from sensor.DS18B20 import DS18B20
def get_DS18B20_temp():
   ds = DS18B20('28-041592661eff')
   t = ds.temperature()  # read temperature
   return str(t.C)

from sensor.LCD1602 import LCD1602
import netifaces

def display_LCD_temp(temp="25"):
   # I2C bus=1, Address=0x27
   lcd = LCD1602(1, 0x27)

   addrs = netifaces.ifaddresses('eth0')
   ip = addrs[netifaces.AF_INET][0]['addr']

   lcd.display("IP:{}".format(ip), 1)   # my name on line 1
   lcd.display("Temp:{}".format(get_DS18B20_temp()), 2)  # my city on line 2
   time.sleep(10) 
   lcd.clear()

if __name__ == "__main__":

   if len(sys.argv) != 2:
      sys.stderr.write("wrong argument: check port number\n")
      exit(4)
   t = ThermThreading()
   time.sleep(3)

   # Error occurred by Ttelepot
   tele = Ttelepot(t)
   tele.on_red_led(21)
   tele.off_red_led(21)

#   display_LCD_temp(temp="25")

   #to use threading and to spawn three processes to handle incoming requests.
   try:
      app.run(host='0.0.0.0', port=int(sys.argv[1]), threaded=True)
   except KeyboardInterrupt:
      print("press control-c again to quit")  
