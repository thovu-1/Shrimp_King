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
BOTTOM_LAYER_TOP = 650
BOTTOM_LAYER_BOTTOM = 710
class DIRECTION(Enum):
    RIGHT = "right"
    LEFT = "left"
    UP = "up"
    DOWN = "down"
    UP_LEFT = "up-left"
    UP_RIGHT = "up-right"
    DOWN_LEFT = "down-left"
    DOWN_RIGHT = "down-right"

def load_background():
    background_sheet = pygame.image.load('other_images/aquarium_background_sprite.png').convert_alpha()
    with open('other_images/aquarium_background_sprite.json') as f:
        background_data = json.load(f)

    background_frames = [pygame.Rect(frame['frame']['x'], frame['frame']['y'], frame['frame']['w'], frame['frame']['h']) for frame in background_data['frames'].values()]

    return background_sheet, background_frames
      
async def load_background_async():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, load_background)

def display_user_gold(user, font, color):
    
    return font.render(user.gold, False, color)

def load_user_shrimps(user):
    shrimp_id_dict ={}
    for species, shrimp_dicts in user.shrimps.items():
        for id, shrimp in shrimp_dicts.items():
            if species in shrimp_id_dict:
                # print("Updating species ")
                shrimp_id_dict[species].append(id)
            else:
                shrimp_id_dict[species] = [id]
    return shrimp_id_dict

def handle_shrimp_scavenging(pellets_on_screen, pellet_index, current_shrimp):
    current_time = pygame.time.get_ticks()
    if pellet_index!= -1 and len(pellets_on_screen) >= pellet_index:
        if current_shrimp.level == 1 and current_time - current_shrimp.eatting_timer > 250:
            current_shrimp.eat(pellets_on_screen[pellet_index].satiation)
            pellets_on_screen[pellet_index].expired = True
            current_shrimp.eatting_timer = current_time
        elif current_shrimp.level == 2 and current_time - current_shrimp.eatting_timer > 500:
            current_shrimp.eat(pellets_on_screen[pellet_index].satiation)
            pellets_on_screen[pellet_index].expired = True
            current_shrimp.eatting_timer = current_time
        elif current_shrimp.level >= 3 and current_time - current_shrimp.eatting_timer > 750:
            current_shrimp.eat(pellets_on_screen[pellet_index].satiation)
            # Remove pellet
            pellets_on_screen[pellet_index].expired = True
            current_shrimp.eatting_timer = current_time
    else:
        current_shrimp.eatting = False