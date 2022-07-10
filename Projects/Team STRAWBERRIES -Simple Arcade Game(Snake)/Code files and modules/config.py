from Max7219 import Max7219
from machine import Pin,SPI,ADC

spi = SPI(1, baudrate=40000000)
screen = Max7219(32,40, spi, Pin(15))
xAxis = ADC(Pin(35))
yAxis = ADC(Pin(32)) 
SW = Pin(22,Pin.IN, Pin.PULL_UP)