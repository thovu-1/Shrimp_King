import pygame
import sys
import pickle
import asyncio
import atexit
import random
import os

def get_shrimp_size(image_path, age):
    shrimp_image = pygame.image.load(image_path)
    shrimp_image_height = shrimp_image.get_height()
    shrimp_image_width = shrimp_image.get_width()
    ADULT_SIZE = shrimp_image_width // 3, shrimp_image_height // 3
    JUVENILE__SIZE = shrimp_image_width // 4, shrimp_image_width // 4
    SHRIMPLET_SIZE = shrimp_image_width // 5, shrimp_image_width // 5
    if age > 5: # if age is above 5, then the shrimp should be an adult
        return pygame.transform.scale(pygame.image.load(image_path), ADULT_SIZE)
    elif age > 2:
        return pygame.transform.scale(pygame.image.load(image_path), JUVENILE__SIZE)
    else:
        return pygame.transform.scale(pygame.image.load(image_path), SHRIMPLET_SIZE)
    
# Function to save shrimp state to file
def save_shrimp_states(shrimps, filename):
    with open(filename, 'wb') as f:
        pickle.dump([shrimp.get_state() for shrimp in shrimps], f)

# Function to load shrimp state from file

# Function to save shrimp states to file asynchronously
async def save_shrimp_states_async(shrimps, filename):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, save_shrimp_states, shrimps, filename)

