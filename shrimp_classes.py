from enum import Enum
import pygame
import sys
import pickle
import asyncio
import atexit
import random
import os
from funcs import *
# Function will be used for all shrimp classes to get shrimp size.
class DIRECTION(Enum):
    RIGHT = "right"
    LEFT = "left"
    UP = "up"
    DOWN = "down"


class User:
    next_id = 1
    def __init__(self, shrimps, pellets, selected_pellet, money, ID=None):
        if ID is not None:
            self.ID = ID
        else:
            self.ID = User.next_id
            User.next_id += 1
        self.name = 'King_Skrimp'
        self.shrimps = shrimps
        self.pellets = pellets
        self.selected_pellet = selected_pellet
        self.money = money

    def save_data(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.money, f)
            pickle.dump(str(self.selected_pellet), f)
            pickle.dump(len(self.shrimps), f)
            for shrimp in self.shrimps:
                pickle.dump(shrimp.get_state(), f)
            pickle.dump(len(self.pellets), f)
            for pellet in self.pellets:
                pickle.dump(pellet.get_state(), f)
                


class Shrimp:
    def __init__(self, x, y, level, food_bar, name, direction: DIRECTION, image_path, x_vel=1, y_vel=1):
        self.name = name
        self.level = level
        self.food_bar = food_bar
        self.image_path = image_path
        self.image = get_shrimp_size(self.image_path, self.level)
        self.rect = self.image.get_rect(x=x,y=y)
        self.rect.x = x
        self.rect.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.direction = random.choice(list(DIRECTION))

    def get_state(self):
    # Return current state as a dictionary, this acts like a save point for our shrimp when we exit the program.
        return {
                'name': self.name,
                'level': self.level,
                'food_bar': self.food_bar,  
                }
    
    def set_state(self, state):
        # Set state from dictionary
        self.level = state['level']
        self.food_bar = state['food_bar']
        

    def move(self, screen_width, screen_height):

        # match self.direction:
        #     case 
        # Update CRS position
        self.rect.x -= self.x_vel
        self.rect.y -= self.y_vel

        # Add random variation to velocity for more natural movement
        self.rect.x += random.randint(-1, 1)
        self.rect.y += random.randint(-1, 1)
        # Check boundaries and bounce if necessary
        if self.rect.x < 0 or self.rect.x > screen_width - self.rect.width:
            self.x_vel = -self.x_vel
            self.image = pygame.transform.flip(self.image, True, False)
        if self.rect.y < 0 or self.rect.y > screen_height - self.rect.height:
            self.y_vel = -self.y_vel

    def draw(self, screen):
        # Draw CRS onto the screen
        screen.blit(self.image, self.rect)
    
    def find_pellet(self, pellets):
        # Find pellet closest to CRS
        closest_pellet = None
        for pellet in pellets:
            if closest_pellet is None:
                closest_pellet = pellet
            elif self.rect.x - pellet.rect.x < self.rect.x - closest_pellet.rect.x:
                closest_pellet = pellet
        return closest_pellet


class CRS(Shrimp):
    def __init__(self, x, y, level, food_bar, image_path='shrimp_images/CRS.png'):
        super().__init__(x, y, level, food_bar, 'CRS', DIRECTION, image_path)
