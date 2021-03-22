import time

import threading
from w1thermsensor import W1ThermSensor
import json


from sensor.DS18B20 import DS18B20
from sensor.LCD1602 import LCD1602
import netifaces
import datetime


currentTemp = {}
INT_VAL=0.5

class ThermThreading(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=INT_VAL):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        self.w1sensor = dict()

        self.num_w1sensor= len(W1ThermSensor.get_available_sensors())

        self.avg_temp= 0.0
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



    def _get_DS18B20_temp(self):
        ds = DS18B20('28-041592661eff')
        t = ds.temperature()  # read temperature
        return str(t.C)


    def _display_LCD_temp(self):
        # I2C bus=1, Address=0x27
        lcd = LCD1602(1, 0x27)

        addrs = netifaces.ifaddresses('eth0')
        ip = addrs[netifaces.AF_INET][0]['addr']
        now = datetime.datetime.now()

        if lcd != None: 
           lcd.display("IP:{}".format(ip), 1)   
           lcd.display("Temp:{}".format(self._get_DS18B20_temp()), 2)  
           lcd.display("Date:{}".format(now.strftime("%Y-%m-%d")),3)
           lcd.display("Time:{}".format(now.strftime("%H:%M:%S")),4)

           time.sleep(1) 
           lcd.clear()


    def run(self):
        """ Method that runs forever """
        global currentTemp
        while True:
            # Do something
            self._display_LCD_temp()
            print('Proving temperature from  w1 device in the background:{}'.format(self.avg_temp))
            for sensor in W1ThermSensor.get_available_sensors():
                self.w1sensor[sensor.id] =  sensor.get_temperature()
            
            # compute the average of temperatures    
            currentTemp = self.w1sensor
            sum = 0
            for k, v in currentTemp.items():
               sum += float(v)
            self.avg_temp = sum /len(currentTemp) 
 
            # print ("temp", json.dumps(currentTemp))
            time.sleep(self.interval)


if __name__ == "__main__":
   example = ThermThreading()

   print ("num of sensors", example.num_w1sensor)
   while True:
      print ("temp", json.dumps(currentTemp))
      time.sleep(3)

