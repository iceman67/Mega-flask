from sensor.LCD1602 import LCD1602
import time

# I2C bus=1, Address=0x27
lcd = LCD1602(1, 0x27)

lcd.display('Nick Lee', 1)   # my name on line 1
lcd.display('Hong Kong', 2)  # my city on line 2


time.sleep(20)
lcd.clear()
