import time
import RPi.GPIO as GPIO
from therm import ThermThreading
import threading



'''
36 GPIO16 BLUE
38 GPIO20 GREEN
40 GPIO21 RED
'''
LED_PIN=21
BLUE_PIN=16
GREEN_PIN=20
RED_PIN=21

INT_VAL=0.5

HIGH_TEMP=30
GOOD_TEMP=20
LOW_TEMP=10


class Ttelepot():

   def __init__(self, t, interval=INT_VAL):
      """ Constructor
      :type interval: int
      :param interval: Check interval, in seconds
      """
      self.interval = interval

      self.color = { 21:"RED", 20:"GREEN", 16:"BLUE"}
      self.led = LED_PIN
      self.green = GREEN_PIN
      self.blue = BLUE_PIN
      self.red = RED_PIN
      self.tthread = t

      self.initGPIO()
      print ('Initializing GPIO...')

      t = threading.Thread(target=self.run, args=())
#      t.daemon = True                            # Daemonize thread
      t.start() 

   def run(self):
      print ('I am listening...')
      while True:
          time.sleep(10)

   def greeting(self, cmd):
      return "good moring, {}".format(cmd)

   def initGPIO(self):
      # to use Raspberry Pi board pin numbers
      GPIO.setwarnings(False)
      GPIO.setmode(GPIO.BCM)
      # set up GPIO output channel
      GPIO.setup(self.red, GPIO.OUT)
      GPIO.setup(self.green, GPIO.OUT)
      GPIO.setup(self.blue, GPIO.OUT)

   # 21 /on_red
   def on_red_led(self,pin):
      GPIO.output(self.red,GPIO.HIGH)
      return "on"

   # 21 /off_red
   def off_red_led(self,pin):
      GPIO.output(self.red,GPIO.LOW)
      return "off"


   # 20 /on_green
   def on_green_led(self,pin):
      GPIO.output(self.green,GPIO.HIGH)
      return "on"

   # 20 /off_green
   def off_green_led(self,pin):
      GPIO.output(self.green,GPIO.LOW)
      return "off"

   # 16 /on_blue
   def on_blue_led(self,pin):
      GPIO.output(self.blue,GPIO.HIGH)
      return "on"

   # 20 /off_blue
   def off_blue_led(self,pin):
      GPIO.output(self.blue,GPIO.LOW)
      return "off"

   # /on RGB 
   def on(self,pin):
      self.led = pin 
      GPIO.output(self.led,GPIO.HIGH)
  
      return "on {}".format(self.color[pin])

   # /off RGB
   def off(self,pin):
      self.led = pin 
      GPIO.output(self.led,GPIO.LOW)
      return "off {}".format(self.color[pin])

   def get_temp(self):
      L = []
      sum = 0
      avg = 0
      for k, v in self.tthread.w1sensor.items():
        sum += float(v)
        L.append(v)
      avg = sum / len(L)

      if avg > HIGH_TEMP:
         self.on(RED_PIN)
         time.sleep(5)
         self.off(RED_PIN)
      elif avg > GOOD_TEMP:
         self.on(GREEN_PIN)
         time.sleep(5)
         self.off(GREEN_PIN)
      else:
         self.on(BLUE_PIN)
         time.sleep(5)
         self.off(BLUE_PIN)
     
 
      temp_str = ','.join(str(x) for x in L)
      return temp_str


   def tmsg_handle(self,msg):
      content_type, chat_type, chat_id = telepot.glance(msg)
     
      chat_id = msg['chat']['id']

      # replace message to lower case
      command = msg['text'].strip().lower()
      print ("Got command {}".format(command))

      if command == '/hello':
         self.bot.sendMessage(chat_id, self.greeting(command))
      elif command == '/on':
         self.bot.sendMessage(chat_id, self.on(LED_PIN))
      elif command =='/off':
         self.bot.sendMessage(chat_id, self.off(LED_PIN))
      elif command == '/on-red':
         self.bot.sendMessage(chat_id, self.on(RED_PIN))
      elif command =='/off-red':
         self.bot.sendMessage(chat_id, self.off(RED_PIN))
      elif command == '/on-blue':
         self.bot.sendMessage(chat_id, self.on(BLUE_PIN))
      elif command =='/off-blue':
         self.bot.sendMessage(chat_id, self.off(BLUE_PIN))
      elif command == '/on-green':
         self.bot.sendMessage(chat_id, self.on(GREEN_PIN))
      elif command =='/off-green':
         self.bot.sendMessage(chat_id, self.off(GREEN_PIN))
      elif command =='/temp':
         self.bot.sendMessage(chat_id, self.get_temp())

def start_teleport():
   initGPIO()
   print ('Initializing GPIO...')
   bot = telepot.Bot(BOT_TOKEN)
   bot.message_loop(tmsg_handle)
   print ('I am listening...')
   while True:
      time.sleep(10)
"""
if __name__ == "__main__":
   initGPIO()
   print ('Initializing GPIO...')
   bot = telepot.Bot(BOT_TOKEN)
   bot.message_loop(tmsg_handle)
   print ('I am listening...')
   bot.sendMessage(id,  "hello")
   while True:
      time.sleep(10)
"""
if __name__ == "__main__":
    tt= ThermThreading()

    t = Ttelepot(tt)
    t.on_red_led(LED_PIN)
    t.off_red_led(LED_PIN)
