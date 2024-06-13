import pygame
import sys
import pickle
import asyncio
import atexit
import random
import os
from shrimp_funcs import *
# Function will be used for all shrimp classes to get shrimp size.




class CRS:
    def __init__(self, x, y, age, x_vel=1, y_vel=1, image_path='shrimp_models/CRS.png'):
        self.image_path = image_path
        self.age = age
        self.image = get_shrimp_size(self.image_path, self.age)
        self.rect = self.image.get_rect(x=x,y=y)
        self.rect.x = x
        self.rect.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel

    def get_state(self):
    # Return current state as a dictionary, this acts like a save point for our shrimp when we exit the program.
        return {'image_path': self.image_path,'x': self.rect.x,'y': self.rect.y, 'age': self.age, 'image': self.image}
    
    def set_state(self, state):
        # Set state from dictionary
        self.image_path = state['image_path']
        self.rect.x = state['x']
        self.rect.y = state['y']
        self.age = state['age']
        self.image = state['image']

    def move(self, screen_width, screen_height):
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