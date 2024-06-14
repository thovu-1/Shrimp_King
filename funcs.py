import pygame
import sys
import pickle
import asyncio
import atexit
import random
import os

# Function will be used for all shrimp classes to get shrimp size which changes depending on their level.
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

def save_user_states(user_data, filename):
    with open(filename, 'wb') as f:
        for user in user_data:
            pickle.dump(user.__dict__, f)  # Save user object attributes
            # Save shrimps
            pickle.dump(len(user.shrimps), f)  # Save number of shrimps for iteration during load
            for shrimp in user.shrimps:
                pickle.dump({'name': shrimp.name}, f)  # Save pellet attributes
            # Save pellets
            pickle.dump(len(user.pellets), f)  # Save number of pellets for iteration during load
            for pellet in user.pellets:
                pickle.dump({'type': pellet.type}, f)  # Save pellet attributes