
import pygame
import pickle
import random
from dotenv import load_dotenv
import os
from funcs import *
from shrimp_funcs import *

# Shrimps is a dictionary of a dictionary structured as {'CRS': {id:shrimp, id:shrimp}, 'OEBT': {id:shrimp,...}, ...}
class User:
    next_id = 1
    def __init__(self, pellets, selected_pellet, money, id=None, shrimps=None):
        if id is not None:
            self.id = id
        else:
            self.id = User.next_id
            User.next_id += 1
        if shrimps is not None and isinstance(shrimps, dict):
            self.shrimps = shrimps
        else:
            print("Creating shrimp dict in initalizer...")
            self.shrimps = {}

        self.name = 'King_Skrimp'
        self.pellets = pellets
        self.selected_pellet = selected_pellet
        self.money = money

    def add_shrimp(self, shrimp):
        if shrimp.species in self.shrimps:
            print("Shrimp species exists:", shrimp.species)
            self.shrimps[shrimp.species] = {shrimp.id: shrimp}
            print("Dictionary after adding shrimp that exists:", self.shrimps)
        else:
            self.shrimps[shrimp.species] = {shrimp.id: shrimp}
            print("Shrimp does not exist current shrimp dict:", self.shrimps)
    def get_money(self):
        for shrimp_species, shrimp in self.shrimps.items():
            match shrimp.species:
                case 'CRS':
                    self.money += shrimp.level * 1
                
    def __getstate__(self):
        state = {
            'id': self.id,
            'money' : self.money,
            'selected_pellet': self.selected_pellet}
        shrimps = {}
        pellets = []
        for pellet in self.pellets:
            pellets.append(pellet.get_state())

        state['pellets'] = pellets
        if self.shrimps is not None:
            for species, shrimp_dict in self.shrimps.items():
                for id, shrimp in shrimp_dict.items():
                    shrimps[id] = shrimp.get_state()
        state['shrimps'] = shrimps
        print('SAVING STATE: ', state)
        return state
    def __setstate__(self, state):
        self.id = state['id']
        self.money = state['money']
        self.selected_pellet = state['selected_pellet']
        self.pellets = get_state_pellets(state['pellets'])
        self.shrimps = get_state_shrimps(state['shrimps'])

    def save_data(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def load_data(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        else:
            return False


class Shrimp:
    next_id = 1
    def __init__(self, x, y, level, food_bar, species, direction: DIRECTION, image_path, x_vel=1, y_vel=1, id=None):
        if id is not None:
            self.id = id
        else:
            self.id = Shrimp.next_id
            Shrimp.next_id += 1
        self.species = species
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
        return {
                'id': self.id,
                'species': self.species,
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


# Pellet class represents food that we feed our shrimp.
class Pellet:
    def __init__(self, x, y, image_path, type, half_life, falling=True, x_vel=0, y_vel=0.5 ):
            food_image = pygame.image.load(image_path)
            self.creation_time = pygame.time.get_ticks()
            self.half_life = half_life
            self.type = type
            self.falling = falling
            self.image = food_image
            self.x_vel = x_vel
            self.y_vel = y_vel
            self.rect = self.image.get_rect(x=x,y=y)
            self.rect.x = x
            self.rect.y = y
            self.expired = False

    def check_half_life(self):
        time = pygame.time.get_ticks()
        if time - self.creation_time > self.half_life:
            self.expired = True
    # Need to grab the type, because a user can have multiple types of food.
    def get_state(self):
        return {
            'type': self.type,
        }
    # Dropping the pellets to the bottom slowly
    def fall(self, screen_height):
        if self.falling == True:
            self.rect.y += self.y_vel
        # Check boundaries and bounce if necessary
        if self.rect.y < 0 or self.rect.y + 25 > screen_height - self.rect.height:
            self.falling = False   


def get_state_pellets(state):
    pellets = []

    for pellet in state:
        match pellet['type']:
            case 'algae_wafer':
                pellet = Pellet(0,0,'food_images/algae_wafer.png', 'algae_wafer', 10000)
                pellets.append(pellet)
            case _:
                print("ADD OTHER PELLETS WHEN LOADING USER STATES")
    return pellets
         

def get_state_shrimps(state):
    shrimps = {}

    for id, shrimp in state.items():
        match shrimp['species']:
            case 'CRS':
                new_shrimp = Shrimp(DEFAULT_SPAWN_X,DEFAULT_SPAWN_Y, shrimp['level'], shrimp['food_bar'], shrimp['species'], DIRECTION, 'shrimp_images/CRS.png', id=shrimp['id'])
                if 'CRS' in shrimps:
                    shrimps['CRS'].update({new_shrimp.id: new_shrimp})
                else:
                    shrimps['CRS'] = {new_shrimp.id: new_shrimp}
            case _:
                print("ADD OTHER SHRIMPS WHEN LOADING USER STATES")
    return shrimps