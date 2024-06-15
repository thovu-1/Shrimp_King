import pygame
import sys
import pickle
import asyncio
import atexit
import random
import os
from enum import Enum
import pygame
import json
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
    UP_LEFT = "up-left"
    UP_RIGHT = "up-right"
    DOWN_LEFT = "down-left"
    DOWN_RIGHT = "down-right"

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

def movement(shrimps, pellets):
    if len(pellets) > 0:
            for pellet in pellets:
                pellet.check_half_life()
                if pellet.expired:
                    pellets.remove(pellet)
                else:
                    pellet.fall(SCREEN_HEIGHT)
            for species, shrimps in shrimps.items():
                for id, shrimp in shrimps.items():
                    shrimp.move(SCREEN_WIDTH, SCREEN_HEIGHT, pellets)
    else:
        for species, shrimps in shrimps.items():
                for id, shrimp in shrimps.items():
                    shrimp.move(SCREEN_WIDTH, SCREEN_HEIGHT, None)

def load_sprites():
    d = {}
    # Load sprite sheets
    shrimplet_sprite_sheet = pygame.image.load('shrimp_images/Shrimplet_Crystal_Red.png').convert_alpha()
    juvenile_sprite_sheet = pygame.image.load('shrimp_images/Juvenile_Crystal_Red.png').convert_alpha()
    adult_sprite_sheet = pygame.image.load('shrimp_images/Adult_Crystal_Red.png').convert_alpha()

    # Load frame data from JSON files
    with open('shrimp_images/Shrimplet_Crystal_Red.json') as f:
        shrimplet_data = json.load(f)
    with open('shrimp_images/Juvenile_Crystal_Red.json') as f:
        juvenile_data = json.load(f)
    with open('shrimp_images/Adult_Crystal_Red.json') as f:
        adult_data = json.load(f)

    # Extract frame rectangles from JSON data
    shrimplet_rects = [pygame.Rect(frame['frame']['x'], frame['frame']['y'], frame['frame']['w'], frame['frame']['h']) for frame in shrimplet_data['frames'].values()]
    juvenile_rects = [pygame.Rect(frame['frame']['x'], frame['frame']['y'], frame['frame']['w'], frame['frame']['h']) for frame in juvenile_data['frames'].values()]
    adult_rects = [pygame.Rect(frame['frame']['x'], frame['frame']['y'], frame['frame']['w'], frame['frame']['h']) for frame in adult_data['frames'].values()]

    # Store sprite data in dictionary
    d[1] = {'sprite_sheet': shrimplet_sprite_sheet, 'frame_rects': shrimplet_rects}
    d[2] = {'sprite_sheet': juvenile_sprite_sheet, 'frame_rects': juvenile_rects}
    d[3] = {'sprite_sheet': adult_sprite_sheet, 'frame_rects': adult_rects}

    return d

async def load_sprites_async():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, load_sprites)

