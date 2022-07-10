from Max7219 import Max7219
from machine import Pin,SPI,ADC
from engine import Game
from time import sleep
from config import *
import strawberries


class Menu:
  def __init__(self,screen):
    self.screen = screen
    self.menu_index = 0
    self.mode_index = 0
    self.state = ""  
    self.arrow = [[0,0],[0,1],[0,2],[0,3],[0,4],[1,1],[1,2],[1,3],[2,2]]

  def get_joystick_state(self):
    xRef = xAxis.read_u16()
    yRef = yAxis.read_u16()

    if yRef == 0:
      self.state = "down"
    if yRef == 65535:
      self.state = "up"
    if xRef == 0:
      self.state = "right"
    if xRef == 65535:
      self.state = "left"

  def display_menu_default(self):
    self.screen.fill(0)
    self.screen.text("MENU",0,32,1)
    self.screen.text("PLAY",0,2,1)
    self.screen.text("MODE",0,12,1)
    self.screen.text("EXIT",0,23,1)

  def display_mode_default(self):
    self.screen.fill(0)
    self.screen.text("E",10,3,1)
    self.screen.text("N",10,13,1)
    self.screen.text("H",10,23,1)
    self.screen.text("MODE",0,32,1)
  
  

  def draw_pointer(self,index):
    for pixel in self.arrow:
      self.screen.pixel(pixel[0]+5,pixel[1]+index*10+4,1)


  def display_menu(self):
    while 1:
      self.display_menu_default()
      self.get_joystick_state()

      if self.state == "down" and self.menu_index<2:
        self.menu_index +=1
        self.state = ""
      if self.state == "up" and self.menu_index>0:
        self.menu_index -=1
        self.state = ""

      
      if self.menu_index==0:
        self.display_menu_default()
        self.screen.rect(0,0,32,11,1)

      if self.menu_index==1:
        self.display_menu_default()
        self.screen.rect(0,10,32,11,1)

      if self.menu_index==2:
        self.display_menu_default()
        self.screen.rect(0,21,32,11,1)

      self.screen.show()

      if not SW.value():
        
        break

      sleep(0.01)
    return self.menu_index,self.mode_index

  

  def display_mode(self):
    self.display_mode_default()

    self.draw_pointer(self.mode_index)
    self.screen.show()
    

    while True:
      self.display_mode_default()
      self.get_joystick_state()
      if self.state == "down" and self.mode_index<2:
        self.mode_index +=1
        self.state = ""
      if self.state == "up" and self.mode_index>0:
        self.mode_index -=1
        self.state = "" 
      self.draw_pointer(self.mode_index)
      self.screen.show()
      if not SW.value():
        break



menu = Menu(screen)
game = Game(screen)

strawberries.display(screen)
sleep(0.5)
screen.fill(0)

while True:
  menu_index,mode_index = menu.display_menu()
  if menu_index == 0:
    if mode_index == 0:
      game.easy_mode()
    elif mode_index == 1:
      game.normal_mode()
    elif mode_index == 2:
      game.hard_mode()
  elif menu_index == 1:
    menu.display_mode()
  elif menu_index == 2:
    break

strawberries.display(screen)
sleep(2)
screen.fill(0)
screen.show()



  