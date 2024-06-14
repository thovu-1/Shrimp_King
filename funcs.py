import pygame
import sys
import pickle
import asyncio
import atexit
import random
import os
from enum import Enum
import pygame

# Defining Global Variables and setting up the display
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
DEFAULT_SPAWN_X = SCREEN_WIDTH // 2
DEFAULT_SPAWN_Y = SCREEN_HEIGHT // 2
SAVE_FILE = 'save_files/user_data.pkl'

class DIRECTION(Enum):
    RIGHT = "right"
    LEFT = "left"
    UP = "up"
    DOWN = "down"

# Helper function to grow the shrimp
def get_shrimp_size(image_path, level):
    shrimp_image = pygame.image.load(image_path)
    shrimp_image_height = shrimp_image.get_height()
    shrimp_image_width = shrimp_image.get_width()
    ADULT_SIZE = shrimp_image_width // 3, shrimp_image_height // 3
    JUVENILE__SIZE = shrimp_image_width // 4, shrimp_image_width // 4
    SHRIMPLET_SIZE = shrimp_image_width // 5, shrimp_image_width // 5
    if level > 5: # if age is above 5, then the shrimp should be an adult
        return pygame.transform.scale(pygame.image.load(image_path), ADULT_SIZE)
    elif level > 2:
        return pygame.transform.scale(pygame.image.load(image_path), JUVENILE__SIZE)
    else:
        return pygame.transform.scale(pygame.image.load(image_path), SHRIMPLET_SIZE)


