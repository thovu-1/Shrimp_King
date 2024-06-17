import math
import pygame
import pickle
import random
from dotenv import load_dotenv
import os
from funcs_and_variables import *
from classes.pellet_class import *


class Shrimp:
    next_id = 1
    def __init__(self, x, y, level, food_bar, species, direction: DIRECTION, x_vel=1, y_vel=1, id=None):
        # Attributes for identifying a shrimp
        if id is not None:
            self.id = id
        else:
            self.id = Shrimp.next_id
            Shrimp.next_id += 1
        self.species = species
        self.level = level
        self.food_bar = food_bar

        # Attributes for movement modifiers 
        self.direction = random.choice(list(DIRECTION))
        self.current_frame_index = 0
        self.animation_speed = 0.2  # Adjust animation speed as needed
        self.last_update_time = pygame.time.get_ticks()
        self.idle_timer = self.last_update_time
        self.boost_clock = self.last_update_time
        self.eatting_timer = self.last_update_time
        self.direction_change_cooldown = self.last_update_time
        self.cruising_bottom_timer = self.last_update_time
        self.cruising_top_timer = self.last_update_time
        self.max_speed = 5
        self.drag = 0.02
        self.min_speed = 1

        # Attributes for sprite and location tracking
        self.sprite_data = load_sprites()[self.level]  # Load sprites based on level
        self.sprite_sheet = self.sprite_data['sprite_sheet']
        self.frame_rects = self.sprite_data['frame_rects']
        self.first_frame_rect = self.frame_rects[0]  # Assuming frames are consistent in size
        self.rect = pygame.Rect(x, y, self.first_frame_rect.width, self.first_frame_rect.height)
        self.rect.x = x
        self.rect.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.closest_pellet = None 

        # Attributes for choosing behavior
        self.cruising_bottom = False
        self.wandering = True
        self.scavenging = False
        self.out_of_bounds = False
        self.eatting = False
        self.boosting = False
        self.idling = False
        

    # Functions for saving shrimp information
    def get_state(self):
        return {
                'id': self.id,
                'species': self.species,
                'level': self.level,
                'food_bar': self.food_bar,  
                }
    # Functions for loading shrimp information
    def set_state(self, state):
        # Set state from dictionary
        self.level = state['level']
        self.food_bar = state['food_bar']
        
    # Functions that will move and display the shrimp
    def move(self, screen_width, screen_height, pellets=None):
        # Check boundaries will change direction for us
        self.check_boundaries(screen_width, screen_height)
        if self.out_of_bounds:
            self.move_in_direction()
            print("Out of bounds")
        else:
            self.find_pellet_x_y(pellets)
             # If we havent hit a wall and there are pellets on the screen go towards to pellets
            if self.scavenging or self.eatting and not self.out_of_bounds:  
                # print("Scavening or eatting")
                # Find direction to go towards
                self.scavenge(self.rect.x, self.rect.y, self.closest_pellet.rect.x, self.closest_pellet.rect.y)
                # Only modifies speed
                self.boosto_boosto()
                # move
                self.move_in_direction()
    
            elif self.wandering and not self.out_of_bounds:
                now = pygame.time.get_ticks()
                # stop for 2500
                if now - self.idle_timer < 2500:
                    self.idling = True
                    self.x_vel = 0
                    self.y_vel = 0
                elif self.x_vel != self.min_speed or self.y_vel != self.min_speed and not self.idling:
                    self.slow_down() 
                #print(self.rect.y, BOTTOM_LAYER_BOTTOM, BOTTOM_LAYER_TOP)
                if self.rect.y <= BOTTOM_LAYER_BOTTOM and self.rect.y >= BOTTOM_LAYER_TOP:
                    
                    self.cruise_bottom_layer() # Means we cannot move down in any direction
                    self.move_in_direction()
                else: 
                    self.cruising_top_layer()
                    self.move_in_direction()
                if now - self.idle_timer > 20000:
                    self.idling = False
                    self.idle_timer = pygame.time.get_ticks()
                    self.x_vel = 0
                    self.y_vel = 0

           
                # Need to add functionality to check for collision with pellet, and if so, stop and eat the pellet.

        #() Idea for movement, shrimp will idle for random time between 10 - 30 seconds.
        # if they are idle, they should only be able to move left or right, and have the same fall functionality as the pellets

        self.update_animation_frame()
         
    def eat(self):
        print("ID:", self.id, 'Level:', self.level, 'Food:', self.food_bar)
        self.eatting = True
        self.x_vel = 0
        self.y_vel = 0
        self.food_bar += 1

    # Using Bresenhams line drawing algorithm to find the shortest path between the shrimp and the closest pellet
    # Returns DIRECTION
    def scavenge(self, x, y, target_x, target_y):
        dx = target_x - x
        dy = target_y - y
        angle = math.atan2(dy, dx)  # Calculate angle towards the target
        # Convert angle to one of the 8 cardinal or diagonal directions
        now = pygame.time.get_ticks()
        direction = self.direction
        if now - self.direction_change_cooldown > 500:
            if math.pi/8 <= angle <= 3*math.pi/8:
                direction = DIRECTION.DOWN_RIGHT
            elif 3*math.pi/8 < angle <= 5*math.pi/8:
                direction = DIRECTION.DOWN
            elif 5*math.pi/8 < angle <= 7*math.pi/8:
                direction = DIRECTION.DOWN_LEFT
            elif -7*math.pi/8 <= angle < -5*math.pi/8:
                direction = DIRECTION.UP_LEFT
            elif -5*math.pi/8 <= angle < -3*math.pi/8:
                direction = DIRECTION.UP
            elif -3*math.pi/8 <= angle < -math.pi/8:
                direction = DIRECTION.UP_RIGHT
            elif -math.pi/8 <= angle <= math.pi/8:
                direction = DIRECTION.RIGHT
            else:
                direction = DIRECTION.LEFT
        
            self.direction_change_cooldown = pygame.time.get_ticks()

        self.direction = direction
    # Move in self.direction
    # Void
    def move_in_direction(self):
        match self.direction:
            case DIRECTION.UP:
                self.rect.y -= self.y_vel
            case DIRECTION.DOWN:
                self.rect.y += self.y_vel
            case DIRECTION.LEFT:
                self.rect.x -= self.x_vel
            case DIRECTION.RIGHT:
                self.rect.x += self.x_vel
            case DIRECTION.UP_RIGHT:
                self.rect.x += self.x_vel
                self.rect.y -= self.y_vel
            case DIRECTION.UP_LEFT:
                self.rect.x -= self.x_vel
                self.rect.y -= self.y_vel
            case DIRECTION.DOWN_RIGHT:
                self.rect.x += self.x_vel
                self.rect.y += self.y_vel
            case DIRECTION.DOWN_LEFT:
                self.rect.x -= self.x_vel
                self.rect.y += self.y_vel
    def boosto_boosto(self):
        # Cap the velocity to max speed
        if self.boosting:
            if self.x_vel < self.max_speed:
                self.x_vel += 0.05
            if self.y_vel < self.max_speed:
                self.y_vel += 0.05
    def slow_down(self):
        # Apply minimum speed threshold
        if self.x_vel < self.min_speed or self.y_vel < self.min_speed:
            self.x_vel = self.min_speed
            self.y_vel = self.min_speed
        else:
            print("Applying Drag")
            self.x_vel *= self.drag
            self.y_vel *= self.drag
    def hang_around(self):
        now = pygame.time.get_ticks()
        elapsed_time = now - self.idle_timer
        num = random.randint(1000,15000)
        if elapsed_time > num:
            self.idle_timer = pygame.time.get_ticks()
            self.direction = random.choice(list(DIRECTION))
            self.x_vel = 0
            self.y_vel = 0
            self.boosto_boosto(math.pi/2)
    # Updating our animation for the shrimp. 0=idle 1-3=swimming 4-6=eatting 
    def update_animation_frame(self):
        # Update animation frame index
        now = pygame.time.get_ticks()
        elapsed_time = now - self.last_update_time
        boost_time = now - self.boost_clock

        if elapsed_time > 2500 * self.animation_speed:  # Convert animation speed to milliseconds
            self.last_update_time = now
            # Determine frame index based on wandering state
            if self.wandering or self.scavenging:
                # Switch between swimming frames (2-4)
                self.current_frame_index = (self.current_frame_index % 3) + 1  # Cycle through frames 1, 2, 3
                # self.current_frame_index = 6
            elif self.eatting:
                self.current_frame_index = (self.current_frame_index % 3) + 4   # Cycle through frames 4 5 6
            else:
                # Idle frame (frame 1)
                self.current_frame_index = 0
                self.x_vel, self.y_vel = self.min_speed
        
        # While scavenging, boost for 2500 seconds, and then cooldown for 1 second
        if self.scavenging:
            # timeout for 2.5 seconds   
            if boost_time < 2500:
                self.boosting = True
            else:
                self.boosting = False
            if boost_time > 5000:
                self.boosting = False
                self.boost_clock = now
                
    def cruise_bottom_layer(self):
        num = random.randint(0,10)
        current_time = pygame.time.get_ticks()
        # 0.005 % chance to leave bottom layer
        if current_time - self.cruising_bottom_timer > 2500:
            if num > 8:
                self.direction = random.choice([DIRECTION.UP, DIRECTION.UP_RIGHT,DIRECTION.UP_LEFT])
            else:
                self.direction = random.choice([DIRECTION.LEFT, DIRECTION.RIGHT])
            self.cruising_bottom_timer = current_time
    
    def cruising_top_layer(self):
        num = random.randint(0,10)
        current_time = pygame.time.get_ticks()
        # 0.005 % chance to leave bottom layer
        if current_time - self.cruising_top_timer > 2500:
            print(num)
            if num > 8:
                self.direction = random.choice([DIRECTION.UP, DIRECTION.UP_LEFT, DIRECTION.UP_RIGHT])
            else:
                self.direction = random.choice([DIRECTION.DOWN, DIRECTION.DOWN_RIGHT,DIRECTION.DOWN_LEFT, DIRECTION.LEFT, DIRECTION.RIGHT])
            self.cruising_top_timer = current_time

        
        
    # Account for collision with pellet
    def check_boundaries(self, screen_width, screen_height):
        # If i colide left, i should go the other way but i n
        x,y = self.rect.x, self.rect.y
        if x < 0:
            self.direction = DIRECTION.RIGHT
            self.out_of_bounds = True 
        elif x >= screen_width - self.rect.width: 
            self.direction = DIRECTION.LEFT
            self.out_of_bounds = True
        elif y < 0:
            self.direction = DIRECTION.DOWN
            self.out_of_bounds = True
        elif y >= screen_height - self.rect.height:
            self.direction = DIRECTION.UP
            self.out_of_bounds = True
        else:
            self.out_of_bounds = False
            # Shrimp.change_direction(self)    
    def change_direction(self):
        self.direction = random.choice(list(DIRECTION))
    
    # Function loops through pellets if they exist otherwise it sets wandering to True
    # Will update the closet pellet x,y pos if there is a pellet.
    def find_pellet_x_y(self, pellets):
        # Find pellet closest to CRS
        temp_pellet = None
        if pellets is not None and len(pellets) > 0:
            for pellet in pellets:
                if temp_pellet is None:
                    temp_pellet = pellet
                elif self.rect.x - pellet.rect.x < self.rect.x - temp_pellet.rect.x:
                    temp_pellet = pellet
            
            self.closest_pellet = temp_pellet
            self.scavenging = True
            self.wandering = False
        else:
            self.scavenging = False
            self.wandering = True
   
    # Function used to display the sprite onto the screen
    def draw(self, screen):
        
        frame_rect = self.frame_rects[self.current_frame_index]
        image = self.sprite_sheet

        if self.direction == DIRECTION.RIGHT :
                image = pygame.transform.flip(self.sprite_sheet, True, False)
        elif self.direction == DIRECTION.LEFT:
                image = pygame.transform.flip(self.sprite_sheet, False, False)

        screen.blit(image, self.rect, frame_rect)




# ----------------------------------------------------------------FUNCTIONS ---------------------------------------------------------------- #

