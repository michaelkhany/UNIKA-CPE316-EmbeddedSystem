# demo 1

from machine import Pin
from time import sleep
class keypad :
    def __init__(self, r, c):
        # CONSTANTS
        self.KEY_UP   = 0
        self.KEY_DOWN = 1

        self.keys = [['1', '2', '3', 'A'], ['4', '5', '6', 'B'], ['7', '8', '9', 'C'], ['*', '0', '#', 'D']]

        # Pin names for Pico
        self.rows = r
        self.cols = c

        # set pins for rows as outputs
        self.row_pins = [Pin(pin_name, mode=Pin.OUT) for pin_name in self.rows]

        # set pins for cols as inputs
        self.col_pins = [Pin(pin_name, mode=Pin.IN, pull=Pin.PULL_DOWN) for pin_name in self.cols]

    def init(self):
      for row in range(0,4):
          for col in range(0,4):
              self.row_pins[row].off()
            

    def scan(self,row, col):
      """ scan the keypad """

     # set the current column to high
      self.row_pins[row].on()
      self.key = None

      # check for keypressed events
      if self.col_pins[col].value() == self.KEY_DOWN:
          self.key = self.KEY_DOWN
      if self.col_pins[col].value() == self.KEY_UP:
          self.key = self.KEY_UP
      self.row_pins[row].off()

      # return the key state
      return self.key

         #print("starting")

        # set all the columns to low
    

            
    def getKey(self):
      self.init()
      self.last_key_press  = None
      while self.last_key_press == None :
          for row in range(4):
              for col in range(4):
                  self.key = self.scan(row, col)
                  if self.key == self.KEY_DOWN:
                      #print("Key Pressed", keys[row][col])
                      self.last_key_press = self.keys[row][col]  
                      #i = i + 1  
                      sleep(0.1)      
                  self.init()

      return self.last_key_press
