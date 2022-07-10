import time
import random
from config import *

dis_width = 32
dis_height = 32

 
class Game:
  def __init__(self,screen):
    self.screen = screen
    self.isAviable = []

  def display_level(self,level):
    self.screen.fill_rect(0, 32, 32, 8, 0)
    self.screen.text("lvl",0,32,1)
    self.screen.text(str(level),23,32,1)
    self.screen.show()
    time.sleep(0.5)

  def game_over_display(self,score):
    self.screen.fill(0)
    self.screen.text("GAME",0,6,1)
    self.screen.text("OVER",0,18,1)
    self.score_board(score)
    self.screen.show()

    time.sleep(2)

  def score_board(self,score):
    self.screen.text(str(score),(4-len(str(score)))*4,32,1) 
 
  def our_snake(self,snake_list):
    for x in snake_list:
      self.screen.pixel(int(x[0]), int(x[1]),1)

  def message(self,msg):
    self.screen.text(msg,0,32,1) 
  
  def get_joystick_state(self):
    return xAxis.read_u16(), yAxis.read_u16()

  def is_aviable_list(self,wall_list):
    for wall in wall_list:
      if wall[0] == wall[2]:
        for i in range(wall[1],wall[3]+1):
          self.isAviable.append([wall[0],i])


      elif wall[1] == wall[3]:
        for i in range(wall[0],wall[2]+1):
          self.isAviable.append([i,wall[1]])

  def easy_mode(self):
    self.isAviable = []
    game_over = False
    game_close = False
    x1 = dis_width / 2 
    y1 = dis_height / 2  

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = random.randrange(0, 31)

    foody = random.randrange(0, 31)

    state="down"

    

    while not game_over:
      while game_close == True:
        self.game_over_display(Length_of_snake-1)
        return 
    
      
      xRef,yRef = self.get_joystick_state()

    

      if (yRef < 10000 or state=="down") and not state=="up":
        state = "down"
      if (yRef > 40000 or state=="up") and not state=="down":
        state = "up"
      if (xRef < 10000 or state=="right") and not state=="left":
        state = "right"
      if (xRef > 40000 or state=="left") and not state=="right":
        state = "left"
      

      # if (yRef == 0 or state=="down") and not state=="up":
      #   state = "down"
      # if (yRef == 65535 or state=="up") and not state=="down":
      #   state = "up"
      # if (xRef == 0 or state=="right") and not state=="left":
      #   state = "right"
      # if (xRef == 65535 or state=="left") and not state=="right":
      #   state = "left"
      


      if state == "left":
        x1_change = -1
        y1_change = 0
      elif state == "right":
        x1_change = 1
        y1_change = 0
      elif state == "up":
        y1_change = -1
        x1_change = 0
      elif state == "down":
        y1_change = 1
        x1_change = 0




      if x1==31 and state=="right":
        x1=0
        x1 -= x1_change
      elif x1==0  and state=="left":
        x1=31
        x1 -= x1_change
      elif y1==0 and state=="up":
        y1=31
        y1 -= y1_change
      elif y1==31 and state=="down":
        y1=0
        y1 -= y1_change
      
      x1 += x1_change
      y1 += y1_change

      self.screen.pixel(foodx,foody,1)

      snake_Head = []
      snake_Head.append(x1)
      snake_Head.append(y1)
      snake_List.append(snake_Head)
      if len(snake_List) > Length_of_snake:
        del snake_List[0]

      for x in snake_List[:-1]:
        if x == snake_Head:
          game_close = True

      self.our_snake(snake_List)
      self.score_board(Length_of_snake - 1)

    
      if x1 == foodx and y1 == foody:
        foodx = random.randrange(0,31)
        foody = random.randrange(0,31)
        Length_of_snake += 1
        

      
      self.screen.show()
      self.screen.fill(0)
 
  def normal_mode(self):
    self.isAviable = []
    game_over = False
    game_close = False
    x1 = dis_width / 2 
    y1 = dis_height / 2  
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = random.randrange(0, 31)

    foody = random.randrange(0, 31)

    state="down"

    while not game_over:
      self.screen.rect(0,0,32,32,1)

      while game_close == True:
        self.game_over_display(Length_of_snake-1)
        return 
      

      
      xRef,yRef = self.get_joystick_state()

    
     
      if (yRef == 0 or state=="down") and not state=="up":
        state = "down"
      if (yRef == 65535 or state=="up") and not state=="down":
        state = "up"
      if (xRef == 0 or state=="right") and not state=="left":
        state = "right"
      if (xRef == 65535 or state=="left") and not state=="right":
        state = "left"
      


      if state == "left":
        x1_change = -1
        y1_change = 0
      elif state == "right":
        x1_change = 1
        y1_change = 0
      elif state == "up":
        y1_change = -1
        x1_change = 0
      elif state == "down":
        y1_change = 1
        x1_change = 0


      
      x1 += x1_change
      y1 += y1_change

      if x1<1 or x1>30 or y1<1 or y1>30:
        game_close = True

      self.screen.pixel(foodx,foody,1)

      snake_Head = []
      snake_Head.append(x1)
      snake_Head.append(y1)
      snake_List.append(snake_Head)
      if len(snake_List) > Length_of_snake:
        del snake_List[0]

      for x in snake_List[:-1]:
        if x == snake_Head:
          game_close = True

      self.our_snake(snake_List)
      self.score_board(Length_of_snake - 1)

    
      if x1 == foodx and y1 == foody:
        foodx = random.randrange(0,31)
        foody = random.randrange(0,31)
        Length_of_snake += 1
      
      self.screen.show()
      self.screen.fill(0)

  def draw_obstacle(self,line):
    self.screen.line(line[0],line[1],line[2],line[3],1)

  def random_obstacle_generator(self):
    x1 = random.randrange(4,27)
    y1 = random.randrange(4,27)
    
    if random.randrange(0,2) == 0:
      x2 = x1+5
      y2 = y1
      if x2>31:
        x2 = 31
    else:
      x2 = x1
      y2 = y1+5
      if y2>31:
        y2 = 31
    return x1,y1,x2,y2


  def random_food_generator(self):
    isSuccess = False
    while not isSuccess:
      foodx = random.randrange(1, 30)
      foody = random.randrange(1, 30)
      isSuccess = True
      for pixel in self.isAviable:
          if pixel[0] == foodx and pixel[1] == foody:
            isSuccess = False
    return foodx,foody
        
  def hard_mode(self):
    self.isAviable = []
    abstacle_count = 5
    extra_obstacle_count = 1
    game_over = False
    game_close = False
    x1 = dis_width / 2 
    y1 = dis_height / 2  
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 7
    foodx,foody = self.random_food_generator()

    state="down"


    wall_list = []
    for i in range(abstacle_count):
      wall_list.append(self.random_obstacle_generator())
    self.is_aviable_list(wall_list)

  

 
    

    self.display_level(1)

    while not game_over:
      self.screen.rect(0,0,32,32,1)
      for wall in wall_list:
        self.draw_obstacle(wall)

      while game_close == True:
        self.game_over_display(Length_of_snake-1)
        return 
      
      xRef,yRef = self.get_joystick_state()

   
      if (yRef == 0 or state=="down") and not state=="up":
        state = "down"
      if (yRef == 65535 or state=="up") and not state=="down":
        state = "up"
      if (xRef == 0 or state=="right") and not state=="left":
        state = "right"
      if (xRef == 65535 or state=="left") and not state=="right":
        state = "left"
      


      if state == "left":
        x1_change = -1
        y1_change = 0
      elif state == "right":
        x1_change = 1
        y1_change = 0
      elif state == "up":
        y1_change = -1
        x1_change = 0
      elif state == "down":
        y1_change = 1
        x1_change = 0


      
      x1 += x1_change
      y1 += y1_change

      if x1<1 or x1>30 or y1<1 or y1>30:
        game_close = True
      for pixel in self.isAviable:
        if pixel[0] == x1 and pixel[1] == y1:
          game_close = True

      self.screen.pixel(foodx,foody,1)

      snake_Head = []
      snake_Head.append(x1)
      snake_Head.append(y1)
      snake_List.append(snake_Head)
      if len(snake_List) > Length_of_snake:
        del snake_List[0]

      for x in snake_List[:-1]:
        if x == snake_Head:
          game_close = True

      self.our_snake(snake_List)
      self.score_board(Length_of_snake - 1)

    
      if x1 == foodx and y1 == foody:
        Length_of_snake += 1
        if (Length_of_snake-1)%10==0 and not Length_of_snake==1:
          self.display_level((Length_of_snake-1)/10+1)
          for i in range(extra_obstacle_count):
            wall_list.append(self.random_obstacle_generator())
          self.is_aviable_list(wall_list)
        foodx,foody = self.random_food_generator()
      
      
      self.screen.show()
      self.screen.fill(0)
 
