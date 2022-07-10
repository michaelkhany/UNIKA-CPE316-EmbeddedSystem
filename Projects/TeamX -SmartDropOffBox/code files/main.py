from time import sleep_ms, ticks_ms,sleep
from machine import I2C, Pin,PWM
from i2c_lcd import I2cLcd 
from keypad import keypad
import utelegram
import network
import time


#Global Variables
isLocked = False
boxCode = ''
hasCode = False
ownerId = ''
hasOwner = False

#LCD initialization
AddressOfLcd = 0x27
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000) 
lcd = I2cLcd(i2c, AddressOfLcd, 2, 16)

#led initialization
led = Pin(5,Pin.OUT)
led.value(0)

#KeyPad initialization
rowPins = [13,12,14,27]
colPins = [26,25,33,32]
keypad = keypad(rowPins,colPins)

#Network & Bot
print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")

TOKEN = '5155092636:AAH5O0HYIHyP5tSySRVDLpDxGEECQOahKCc'
chat = '537775139'

bot = utelegram.Bot(TOKEN)

def lock():
  global isLocked 
  isLocked = True
  led.value(1)
  bot.send_message(chat,'Box has been LOCKED')

def unlock():
  global isLocked
  global boxCode
  isLocked = False
  led.value(0)
  bot.send_message(chat,'Box has been OPENED')
  
def check_password(userCode) :
  global boxCode
  if (boxCode != ''):
    if (userCode == boxCode):
      return True
  else : 
    return False

def check_owner(userId) :
  global ownerId
  if (ownerId != ''):
    if (userId == ownerId):
      return True
  else : 
    return False

def showStartupMessage() :
  lcd.move_to(4, 0)
  lcd.putstr("Welcome!")
  sleep_ms(200)
  lcd.move_to(0, 1)
  massage = "  Dropp of box"
  for i in range (0,14):
    lcd.putchar(massage[i])
    sleep_ms(100)
  bot.send_message(chat,'Smart box starting')
  sleep(0.2)

def inputSecretCode() :
  lcd.move_to(5, 1)
  lcd.putstr("[____]")
  lcd.move_to(6, 1)
  result = ""
  while (len(result) < 4) :
    key = keypad.getKey()
    if (key >= '0' and key <= '9') :
      lcd.putchar('*')
      result += key
  return result

def inputOwner() :
  lcd.move_to(5, 1)
  lcd.putstr("[_____]")
  lcd.move_to(6, 1)
  userInput = ""
  while (len(userInput) < 5) :
    key = keypad.getKey()
    if (key != '*' and key != '#') :
      lcd.putchar('*')
      userInput += key
  return userInput

def waitScreen(delayMil) :
  lcd.move_to(2, 1)
  lcd.putstr("[..........]")
  lcd.move_to(3, 1)
  for i in range (0,10):
    sleep_ms(delayMil)
    lcd.putstr('=')
    
def setNewCode() :
  global boxCode
  global hasCode
  lcd.clear()
  lcd.move_to(0, 0)
  lcd.putstr("Enter new code:")
  newCode = inputSecretCode()
  lcd.clear()
  lcd.move_to(0, 0)
  lcd.putstr("Confirm new code")
  confirmCode = inputSecretCode()
  if (newCode == confirmCode):
    boxCode = newCode
    hasCode = True
    waitScreen(200)
    bot.send_message(chat,"{} {} {}".format('A new Password has been set :', boxCode,'do not forget it'))
    return True
  else :
    lcd.clear()
    lcd.move_to(1, 0)
    lcd.putstr("Code mismatch")
    lcd.move_to(0, 1)
    lcd.putstr("Box not locked!")
    sleep_ms(700)
    return False

def setOwner() :
  global hasOwner
  global ownerId
  lcd.clear()
  lcd.move_to(0, 0)
  lcd.putstr("Enter owner Id:")
  newOwner = inputOwner()
  lcd.clear()
  lcd.move_to(0, 0)
  lcd.putstr("   Confirm Id")
  confirmID = inputOwner()
  if (newOwner == confirmID):
    ownerId = newOwner
    hasOwner = True
    waitScreen(200)
    bot.send_message(chat,"{} {}".format('The new Owner Id has been set : ', ownerId))    
    return True
  else :
    lcd.clear()
    lcd.move_to(1, 0)
    lcd.putstr("ID mismatch")
    lcd.move_to(1, 1)
    lcd.putstr("ID not set")
    sleep_ms(700)
    return False

def showUnlockMessage() :
  lcd.clear()
  lcd.move_to(4, 0)
  lcd.putstr("Unlocked!")
  sleep(0.5)

def boxUnlockedLogic():
  global boxCode
  global isLocked
  global hasCode
  global ownerId
  global hasOwner
  lcd.clear()
  lcd.move_to(2, 0)
  lcd.putstr(" # to lock")
  newOwnerNeeded = True
  newCodeNeeded = True

  if (hasCode == True and hasOwner == True):
    lcd.move_to(0, 1)
    lcd.putstr(" * : new code")
    newCodeNeeded = False
    newOwnerNeeded = False
  key = keypad.getKey()
  while (key != '*' and key != '#') :
    key = keypad.getKey()
  readyToLock = True
  if (key == '*' ) :
    if (hasOwner):
      lcd.clear()
      lcd.clear()
      lcd.putstr("    Enter Id")
      userInput = inputOwner()
      rightId = check_owner(userInput)
      waitScreen(300)

      if (rightId) :
        readyToLock = setNewCode()
  
      else :
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("ID mismatch")
        waitScreen(700)
  if (newOwnerNeeded):
    readyToLock = setOwner()
  if (newCodeNeeded == True and hasOwner) :
    readyToLock = setNewCode()
  '''
  if (newOwnerNeeded == True and hasCode) :
    readyToLock = setOwner()
  '''
  if (readyToLock == True) :
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("unlocked")
    lcd.putstr(">>")
    lcd.putstr("Locked")
    waitScreen(300)
    lock()

def boxLockedLogic() :
  lcd.clear()
  lcd.putstr("  Box Locked! ")
  sleep(1)
  lcd.clear()
  lcd.putstr(" Enter Password")
  userCode = inputSecretCode()
  unlockedSuccessfully = check_password(userCode)
  waitScreen(300)

  if (unlockedSuccessfully) :
    showUnlockMessage()
    unlock()
  
  else :
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("Access Denied!")
    waitScreen(700)
  
## main calls 
showStartupMessage()
while True:
  if (isLocked == True) :
    boxLockedLogic()
  else : 
    boxUnlockedLogic()
  
'''
while True :
  main()
  bot._read()
  sleep(1)
'''