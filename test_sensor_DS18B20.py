"""
https://github.com/nickoala/sensor
"""

from sensor.DS18B20 import DS18B20

ds = DS18B20('28-041592661eff')
t = ds.temperature()  # read temperature

print(t)    # this is a namedtuple
print(t.C)  # Celcius
print(t.F)  # Fahrenheit
print(t.K)  # Kelvin
