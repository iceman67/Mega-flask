import telepot
import time
import RPi.GPIO as GPIO

BOT_TOKEN = "640789405:AAF1vjsGbDPzLTv9nHdCdJbiViBG6Qlf1w0"

LED_PIN=21

def greeting(cmd):
    return "good moring, {}".format(cmd)

def initGPIO():
   # to use Raspberry Pi board pin numbers
   GPIO.setwarnings(False)
   GPIO.setmode(GPIO.BCM)
   # set up GPIO output channel
   GPIO.setup(LED_PIN, GPIO.OUT)

def on(pin):
    GPIO.output(pin,GPIO.HIGH)
    return "on"

def off(pin):
    GPIO.output(pin,GPIO.LOW)
    return "off"


def tmsg_handle(msg):
    global bot, active_chats, authorized_ids
    content_type, chat_type, chat_id = telepot.glance(msg)
     
    chat_id = msg['chat']['id']
    command = msg['text']
    print ("Got command {}".format(command))

    if command == 'hello':
       bot.sendMessage(chat_id, greeting(command))

    elif command == 'on':
       bot.sendMessage(chat_id, on(LED_PIN))
    elif command =='off':
       bot.sendMessage(chat_id, off(LED_PIN))

def start_teleport():
   initGPIO()
   print ('Initializing GPIO...')
   bot = telepot.Bot(BOT_TOKEN)
   bot.message_loop(tmsg_handle)
   print ('I am listening...')
   while True:
      time.sleep(10)

if __name__ == "__main__":
   initGPIO()
   print ('Initializing GPIO...')
   bot = telepot.Bot(BOT_TOKEN)
   bot.message_loop(tmsg_handle)
   print ('I am listening...')
   while True:
      time.sleep(10)
