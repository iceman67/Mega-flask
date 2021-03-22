from sensor.DS18B20 import DS18B20
import time
from sensor.LCD1602 import LCD1602
import netifaces
import datetime


def get_DS18B20_temp():
   ds = DS18B20('28-041592661eff')
   t = ds.temperature()  # read temperature
   return str(t.C)

def display_LCD_whoiam():
   # I2C bus=1, Address=0x27
   lcd = LCD1602(1, 0x27)

   addrs = netifaces.ifaddresses('eth0')
   ip = addrs[netifaces.AF_INET][0]['addr']
   now = datetime.datetime.now()

   lcd.display("IP:{}".format(ip), 1)   
   lcd.display("Temp:{}".format(get_DS18B20_temp()), 2)  
   lcd.display("Date:{}".format(now.strftime("%Y-%m-%d")),3)
#   lcd.display("Time:{}".format(now.strftime("%H:%M:%S")),4)
   time.sleep(50) 
   lcd.clear()

display_LCD_whoiam()
