from jguvc_eip import basic_io as bio
from jguvc_eip import image_objects as io
from jguvc_eip.colors import *
from time import sleep
from numpy import random


if __name__ == "__main__":

 def game_over():
    #draw Background (Day 2)
    bio.draw_image(0, 0, background_day)
    move_terrain(wall_speed) 
    #draw message
    bio.print_message("Game over")
    bio.print_message("Press 'r' to restart")
    player1.print_score()
    return True
    
 
 def build_walls(level_width, level_gab_size, first_wall):
    #first wall
    wall_position = [first_wall]
    #generate walls
    for i in range(level_width):
        wall_position.append(wall_position[i] + level_gab_size)
        
    #create holes
    holes = random.randint(130, image_size_y-200, size=(level_width + 1))
    return wall_position, holes


 def build_terrain():
    terrain_position = [0,image_size_x]
    return terrain_position
         
         
 def move_terrain(wall_speed):
    for i in range(2):
        terrain_position[i] -= wall_speed
        bio.draw_image(int(terrain_position[i]), 600, terrain)
        if terrain_position[i] <= -1280:
            terrain_position[i] = 1280
    
    
 def draw_walls(wall_position, holes, wall_speed):
    #draw walls
    for i in range(len(wall_position)):
        wall_position[i] -= wall_speed
        bio.draw_image(int(wall_position[i]-26), int(holes[i]-75-500), pylon_green_down)
        bio.draw_image(int(wall_position[i]-26), int(holes[i]+75), pylon_green_up)
        
        
 def draw_score(score_number):
     str_number = str(score_number)
     for i in range(len(str_number)):
         bio.draw_image(int(image_size_x/2 + i*28), 150, numbers[int(str_number[i])])

        
 class Player:
        def __init__(self, pos, size, lower_border, upper_border, speed = 0, acceleration = 0.2, color = RED, score = 0, highscore = 0, score_pos = 0):
            #initalising attributes
            self.pos_x = pos[0]
            self.pos_y = pos[1]
            self.size = size
            self.lower_border = lower_border
            self.upper_border = upper_border
            self.speed = speed
            self.acceleration = acceleration
            self.score = score
            self.highscore = highscore
            self.new_highscore = False
            self.score_pos = score_pos
        
            #draw function
        def draw(self, colour):
            if self.speed < -1:
                bio.draw_image(self.pos_x, int(self.pos_y), birds[3+colour])
            elif self.speed > 1:
                bio.draw_image(self.pos_x, int(self.pos_y), birds[6+colour])
            else:
                bio.draw_image(self.pos_x, int(self.pos_y), birds[colour])
            
        #move function
        def move(self, direction: str):
            if direction == "up":
                if self.pos_y <= self.upper_border:
                    self.pos_y = self.upper_border
                else:
                    self.pos_y -= int(self.speed)
                    
            if direction == "down":
                if self.pos_y >= lower_border - player_size:
                    self.pos_y = lower_border - player_size
                else:
                    self.pos_y += int(self.speed)
                    
        #jump function
        def jump(self):
            if bio.get_last_key_pressed_event() == "u":
                self.speed = -4
            # speed constantly increases by acceleration
            self.speed += self.acceleration
            # normal falling
            self.pos_y += self.speed
            
            if self.pos_y < self.upper_border:
                self.pos_y = self.upper_border
                self.speed = 0

            # boundary check for bottom
            if self.pos_y >= 580:
                self.pos_y = 580
                self.speed = 0
            
        def check_collision(self):
            for i in range(level_width):
                if (player1.pos_y < holes[i] - 77 and player1.pos_x > wall_position[i] - player_size - 25 and player1.pos_x < wall_position[i] + player_size) or (player1.pos_y + 30 > holes[i] + 85 and player1.pos_x > wall_position[i] - player_size - 25 and player1.pos_x < wall_position[i] + player_size): 
                    sleep(1)
                    bio.draw_image(500,200,gameover)
                    return game_over()
            return False
        
        def add_score(self, wall_speed, level_gab_size, first_wall):
            self.score_pos += wall_speed
            if self.score_pos >= first_wall:
                self.score += 1
                self.score_pos = first_wall - level_gab_size
                bio.print_message(str(self.score))
        
        def reset_score(self):
            self.score = 0
            self.score_pos = 0
            self.new_highscore = False
        
        def print_score(self):
            bio.print_message(f"Your Score is: {str(self.score)}")
            bio.print_message(f"Your High-Score is: {str(self.highscore)}")
        
        def draw_results(self):
            str_score = str(self.score)
            str_highscore = str(self.highscore)
            
            #frame + new_record
            bio.draw_image(0, 20, highscore_frame)
            if self.new_highscore == True:
                bio.draw_image(0, 50, new_record)
            #score numbers
            for i in range(len(str_score)):
                bio.draw_image(725  + i*28, 295, numbers[int(str_score[i])])
            for i in range(len(str_highscore)):    
                bio.draw_image(725  + i*28, 395, numbers[int(str_highscore[i])])

        def save_highscore(self):
            if self.score > self.highscore:
                self.highscore = self.score
                self.new_highscore = True
                
        
                
            
            
 bio.start()

 #initalizing some attributes
 image_size_x, image_size_y = 1280, 720
 upper_border = 0                        
 lower_border = 720                      #adjust border related to resolution size
 player_size = 30                       
 level_width = 25                        #number of walls in total
 level_gab_size = 300                    #gab-size between walls
 first_wall = 1280                       #coordinate where firt wall is generated
 wall_speed = 5                          #level speed/difficulty
 starter = 0                             #counts seconds to display "get ready"
 first_start = True                      #gets false after first game-over
 game_lost = True                        #start parameter for main-loop
 colour = 0
 
 
 

 #creating object (class Player) 
 player1 = Player([100, int(lower_border/2)], player_size, lower_border, upper_border)
 
 #stuff for buffering
 active_buffer = 0
 visible_buffer = 1
 
 terrain_position = build_terrain()
 
 #load image components (Day 2)
 background_day = bio.load_image("image_elements/background_day.png")
 pylon_green_up = bio.load_image("image_elements/pylon_green_up.png")
 pylon_green_down = bio.load_image("image_elements/pylon_green_down.png")
 get_ready = bio.load_image("image_elements/get_ready.png")
 terrain = bio.load_image("image_elements/terrain.png")
 
 #load image components High-Score (Day 5)
 highscore_frame = bio.load_image("image_elements/Highscore_Frame.png")
 new_record = bio.load_image("image_elements/New_Record.png")
 
 #load image components Flappybird numbers
 numbers = [bio.load_image("image_elements/counter/counter_0.png"), bio.load_image("image_elements/counter/counter_1.png"), bio.load_image("image_elements/counter/counter_2.png"), bio.load_image("image_elements/counter/counter_3.png"), bio.load_image("image_elements/counter/counter_4.png"), bio.load_image("image_elements/counter/counter_5.png"), bio.load_image("image_elements/counter/counter_6.png"), bio.load_image("image_elements/counter/counter_7.png"), bio.load_image("image_elements/counter/counter_8.png"), bio.load_image("image_elements/counter/counter_9.png")]
 
 #load image components Bird in different colors
 birds = [bio.load_image("image_elements/birds/bird_red_wings_level.png"), bio.load_image("image_elements/birds/bird_blue_wings_level.png"), bio.load_image("image_elements/birds/bird_orange_wings_level.png"), bio.load_image("image_elements/birds/bird_red_wings_down.png"), bio.load_image("image_elements/birds/bird_blue_wings_down.png"), bio.load_image("image_elements/birds/bird_orange_wings_down.png"), bio.load_image("image_elements/birds/bird_red_wings_up.png"), bio.load_image("image_elements/birds/bird_blue_wings_up.png"), bio.load_image("image_elements/birds/bird_orange_wings_up.png")]
 
 #load image components Start Screen
 logo = bio.load_image("image_elements/flappy_birds_logo.png")
 start_button = bio.load_image("image_elements/PressR.png")
 black_bird = bio.load_image("image_elements/black_bird.png")

 gameover = bio.load_image("image_elements/game_over.png")
 
 #main-loop
 while True:
     #generate level
     wall_position, holes = build_walls(level_width, level_gab_size, first_wall)
     
     #resolution
     bio.resize_image(image_size_x, image_size_y)
     
     #key-inputs for start/restart
     keys = bio.get_current_keys_down()
     if "r" in keys:
        game_lost = False
        bio.print_message("Game started")
     if "b" in keys:
         colour = 1
     if "o" in keys:
         colour = 2
         
     #draw Background (Day 2)
     bio.draw_image(0, 0, background_day)
     
     #draw Start Screen
     if first_start == True:
         move_terrain(wall_speed)
         bio.draw_image(550, 70, logo)
         bio.draw_image(550, 160,get_ready)
         bio.draw_image(550, 270,birds[colour])
         bio.draw_image(605, 250,black_bird)
         #bio.draw_text(100, 160, "Start the game! Press 'r' to start", color=BLUE, background_color=None, font_height=20)
         bio.draw_image(470, 350, start_button)
         player1.draw
     #draw Game-Over Screen
     else:
         move_terrain(wall_speed)
         bio.draw_image(550, 40, logo)
         bio.draw_image(550, 110, gameover)
         #bio.draw_text(100, 160, "Start the game! Press 'r' to start", color=BLUE, background_color=None, font_height=20)
         bio.draw_image(470, 550, start_button)
         player1.draw
         player1.draw_results()
        
     #stuff for buffering
     bio.set_active_image(active_buffer)
     bio.set_visible_image(visible_buffer)
     bio.copy_image(visible_buffer, active_buffer)
     active_buffer, visible_buffer = visible_buffer, active_buffer
     bio.clear_image()
     sleep(0.016)
     
     #reset_score
     if game_lost == False:
        player1.reset_score()
        first_start = False
 
     #game-loop
     while game_lost == False:
        
        #stuff for buffering
        bio.set_active_image(active_buffer)
        bio.set_visible_image(visible_buffer)
        bio.copy_image(visible_buffer, active_buffer)
        active_buffer, visible_buffer = visible_buffer, active_buffer
        bio.clear_image()
        
        #resolution
        bio.resize_image(image_size_x, image_size_y)
        
        #key-inputs
        #keys = bio.get_current_keys_down()
        #if "w" in keys:
            #player1.move("up")
        #if "s" in keys:
            #player1.move("down")
        #key-inputs
        #if bio.get_last_key_pressed_event() == "u":
            #speed = -4 
        
        #draw Background (Day 2)
        bio.draw_image(0, 0, background_day)
        move_terrain(wall_speed)
        
        #jump player (Day 3)
        player1.jump()
        
        #draw player colour red = 0, blue = 1, orange = 2
        player1.draw(colour)
        
        #score + collision + drawing
        draw_walls(wall_position, holes, wall_speed)
        player1.add_score(wall_speed, level_gab_size, first_wall)
        game_lost = player1.check_collision()
        
        # get ready (Day 2)
        if starter < 150:
            bio.draw_image(548, 335, get_ready)
            starter += 1
        
        #draw score
        player1.save_highscore()        
        draw_score(player1.score)
       
        sleep(0.016)
        
    
 bio.wait_close()
 
