#REMEMBER TO RENAME FILE TO main.py BEFORE UPLOAING TO THE BOARD

#THIS SIMPLE EXAMPLE IS USED TO TURN AN LED CONNECTED TO PIN 2 ON AND OFF BY SENDING MESSAGGES TO THE BOT,
#IT IS ALSO POSSIBLE TO KNOW THE CURRENT STATE OF THE PIN
from utelegram import Bot
from machine import Pin
import time

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect("Osama NET", "asdrasdr1")
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    
do_connect()

TOKEN = '5386986012:AAExQa_A_dJiaCH__1dzlxTzUKfvjR-OcPY'

bot = Bot(TOKEN)
led = Pin(32, Pin.OUT)
c = Pin(34, Pin.IN, Pin.PULL_DOWN)


@bot.add_command_handler('start')
def detect(update):
    while c.value():
        time.sleep(1)
    update.reply('.')
    time.sleep_ms(200)
    update.reply('.')
    time.sleep_ms(200)
    update.reply('Door is opened')
    time.sleep_ms(200)
    update.reply('.')
    time.sleep_ms(200)
    update.reply('.')
    time.sleep_ms(200)
    update.reply('/WarningLight')
    

@bot.add_command_handler('WarningLight')
def on(update):
    led.on()
    time.sleep_ms(500)
    led.off()
    time.sleep_ms(500)
    led.on()
    time.sleep_ms(500)
    led.off()
    time.sleep_ms(500)
    led.on()
    time.sleep_ms(500)
    led.off()
    time.sleep_ms(500)
    led.on()
    time.sleep_ms(500)
    led.off()
    time.sleep_ms(500)
    led.on()
    time.sleep_ms(500)
    led.off()
    time.sleep_ms(500)
    led.on()
    time.sleep_ms(500)
    led.off()


bot.start_loop()