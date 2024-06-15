
import math
import pygame
import pickle
import random
from dotenv import load_dotenv
import os
from funcs import *

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
    def __init__(self, x, y, level, food_bar, species, direction: DIRECTION, x_vel=1, y_vel=1, id=None):
        if id is not None:
            self.id = id
        else:
            self.id = Shrimp.next_id
            Shrimp.next_id += 1
        
        self.species = species
        self.level = level
        self.food_bar = food_bar
        self.sprite_data = load_sprites()[self.level]  # Load sprites based on level
        self.sprite_sheet = self.sprite_data['sprite_sheet']
        self.frame_rects = self.sprite_data['frame_rects']
        # self.image = get_shrimp_size(self.image_path, self.level)
        # self.rect = self.image.get_rect(x=x,y=y)
        self.direction = random.choice(list(DIRECTION))
        self.wandering = True
        self.scavenging = False
        self.current_frame_index = 0
        self.animation_speed = 0.2  # Adjust animation speed as needed
        self.last_update_time = pygame.time.get_ticks()

        # Determine rect dimensions based on first frame rect
        first_frame_rect = self.frame_rects[0]  # Assuming frames are consistent in size
        self.rect = pygame.Rect(x, y, first_frame_rect.width, first_frame_rect.height)
        self.rect.x = x
        self.rect.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel

        print(self.level)
        
    # Make an accelleration function that sends the shrimp in a certain direction, - the acceleration each tick until it 
    # stops and then change direction.If collision then change direction early
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
        

    def move(self, screen_width, screen_height, pellets=None):

        if self.wandering:
                # 5% chance to change direction randomly.
                num = random.randint(0,1000)
                if num <= 5:
                    Shrimp.change_direction(self)
                    # print("Changing direction: ", self.direction)

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
                        self.rect.x -= self.x_vel
                        self.rect.y += self.y_vel
                    case DIRECTION.DOWN_LEFT:
                        self.rect.x += self.x_vel
                        self.rect.y -= self.y_vel
                # Update animation frame based on movement

                self.update_animation_frame()

        Shrimp.check_boundaries(self, screen_width, screen_height)
    
    def update_animation_frame(self):
        # Update animation frame index
        now = pygame.time.get_ticks()
        elapsed_time = now - self.last_update_time

        if elapsed_time > 1000 * self.animation_speed:  # Convert animation speed to milliseconds
            self.last_update_time = now

            # Determine frame index based on wandering state
            if self.wandering:
                # Switch between swimming frames (2-4)
                self.current_frame_index = (self.current_frame_index % 3) + 2  # Cycle through frames 2, 3, 4
            else:
                # Idle frame (frame 1)
                self.current_frame_index = 1

    def check_boundaries(self, screen_width, screen_height):
        # If i colide left, i should go the other way but i n
        if self.rect.x < 0:
            self.direction = DIRECTION.RIGHT 
        if self.rect.x >= screen_width - self.rect.width + 10: 
            self.direction = DIRECTION.LEFT
        if self.rect.y < 0:
            self.direction = DIRECTION.DOWN
        if self.rect.y >= screen_height - self.rect.height + 10:
            self.direction = DIRECTION.UP
            
            # Shrimp.change_direction(self)    
    def change_direction(self):
        self.direction = random.choice(list(DIRECTION))
    
    def find_pellet(self, pellets):
        # Find pellet closest to CRS
        closest_pellet = None
        if pellets is not None:
            for pellet in pellets:
                if closest_pellet is None:
                    closest_pellet = pellet
                elif self.rect.x - pellet.rect.x < self.rect.x - closest_pellet.rect.x:
                    closest_pellet = pellet
            # Calculate direction vector towards closest pellet
            direction_x = closest_pellet.rect.x - self.rect.x
            direction_y = closest_pellet.rect.y - self.rect.y
             # Calculate distance to pellet (optional, for further use)
            distance = math.hypot(direction_x, direction_y)

             # Normalize direction vector (convert to unit vector)
            if distance != 0:
                print(direction_x, direction_y)
                direction_x /= distance
                direction_y /= distance
                

            # Update shrimp position based on velocity
            # Need to move towards direction_x and direction_y

            self.rect.x += self.x_vel
            self.rect.y += self.y_vel

            
    def draw(self, screen):
        # Draw CRS onto the screen
        frame_rect = self.frame_rects[self.current_frame_index]
        screen.blit(self.sprite_sheet, self.rect, frame_rect)

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

# ----------------------------------------------------------------FUNCTIONS ---------------------------------------------------------------- #

# Helper function to unpickle all saved pellets
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
         

# Helper function to unpickle all saved shrimps
def get_state_shrimps(state):
    shrimps = {}

    for id, shrimp in state.items():
        match shrimp['species']:
            case 'CRS':
                new_shrimp = Shrimp(DEFAULT_SPAWN_X,DEFAULT_SPAWN_Y, shrimp['level'], shrimp['food_bar'], shrimp['species'], DIRECTION, id=shrimp['id'])
                if 'CRS' in shrimps:
                    shrimps['CRS'].update({new_shrimp.id: new_shrimp})
                else:
                    shrimps['CRS'] = {new_shrimp.id: new_shrimp}
            case _:
                print("ADD OTHER SHRIMPS WHEN LOADING USER STATES")
    return shrimps

# Function to create a new user
def create_new_user():
    print("Current user not found, creating new user...")
    # if there is no user, create a user with a crs in the shrimps state

    crs = [Shrimp(DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y, 1, 0, 'CRS', DIRECTION ), \
           Shrimp(DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y, 2, 0, 'CRS', DIRECTION ), \
            Shrimp(DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y, 3, 0, 'CRS', DIRECTION)]
    d = {crs[0].id: crs[0], crs[1].id: crs[1], crs[2].id: crs[2]}
    pellets = Pellet(0,0,'food_images/algae_wafer.png', 'algae_wafer', 10000)
    new_user = User([pellets], 'algae_wafer', 100, 1)
    new_user.shrimps['CRS'] = d
    print("Created new user: ", new_user)
    return new_user
# Function to load an existing user using the load_data function in User class
def load_existing_user(filename):
    user_data = User.load_data(filename) # returns true or false

    if user_data is not False:
        new_user = User(user_data.pellets, user_data.selected_pellet, user_data.money, user_data.id, user_data.shrimps)
        print("Loading existing user: ", new_user.id ,new_user.name)
        return new_user
    return user_data

# This function calls load_user_states asynchronously
async def load_user_states_async(filename):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, load_user_states, filename)

# This function saves the user_states asynchronuously
async def save_user_states_async(user:User, filename):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, user.save_data, filename)

# This function will 'unpickle' the data from the user save file.
def load_user_states(filename): 
        existing_user = load_existing_user(filename)
        if existing_user:
            return existing_user
        else:
            return create_new_user()