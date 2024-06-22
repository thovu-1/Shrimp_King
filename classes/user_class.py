import math
import pygame
import pickle
import random
from dotenv import load_dotenv
import os
from classes.food.pellet_class import *
from classes.shrimp.shrimp_sub_classes.crystal_red_class import *
from classes.shrimp.shrimp_sub_classes.shadow_panda_class import *
from classes.shrimp.shrimp_sub_classes.crystal_black_class import *

class User:
    next_id = 1
    def __init__(self, pellets, selected_pellet, gold, id=None, shrimps=None):
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
        self.gold = gold

    def add_shrimp(self, shrimp):
        if shrimp.species in self.shrimps:
            print("Shrimp species exists:", shrimp.species)
            self.shrimps[shrimp.species] = {shrimp.id: shrimp}
            print("Dictionary after adding shrimp that exists:", self.shrimps)
        else:
            self.shrimps[shrimp.species] = {shrimp.id: shrimp}
            print("Shrimp does not exist current shrimp dict:", self.shrimps)
    def get_gold(self, current_shrimp):
        self.gold += current_shrimp.passive_gold_generation

    def __getstate__(self):
        state = {
            'id': self.id,
            'gold' : self.gold,
            'selected_pellet': self.selected_pellet}
        shrimps = {}
        pellets = {}
        for pellet in self.pellets:
            pellets.update(pellet.get_state())
            #pellets.append(pellet.get_state())
        print("PELLETS state[pellets]:", pellets)
        state['pellets'] = pellets
        print("Shrimps dict here", self.shrimps)
        if self.shrimps is not None:
            for species, shrimp_dict in self.shrimps.items():
                for id, shrimp in shrimp_dict.items():
                    if species in shrimps:
                        shrimps[species].update(shrimp.get_state())
                    else:
                        shrimps[species] = shrimp.get_state()
        state['shrimps'] = shrimps
        print('SAVING STATE: ', state)
        return state
    def __setstate__(self, state):
        print("LOADING STATE:", state)

        self.id = state['id']
        self.gold = state['gold']
        self.selected_pellet = state['selected_pellet']
        self.pellets = Pellet.get_state_pellets(state['pellets'])
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



# Function to create a new user
def create_new_user():
    print("Current user not found, creating new user...")
    # if there is no user, create a user with a crs in the shrimps state
    # crs = [Shrimp(DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y, 1, 0, 'Crystal_Red', DIRECTION ),   \
    #        Shrimp(DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y, 2, 0, 'Crystal_Red', DIRECTION ), \
    #         Shrimp(DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y, 3, 0, 'Crystal_Red', DIRECTION)]
    # d = {crs[0].id: crs[0], crs[1].id: crs[1], crs[2].id: crs[2]}

    crs = [Crystal_Red(DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y, 1, 0)]
    shadow_panda = [Shadow_Panda(DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y, 1, 0)]
    crystal_black = [Crystal_Black(DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y, 1, 0)]
    pellet = Pellet(0,0,'food_images/algae_wafer.png', 'algae_wafer', 10000)
    new_user = User([pellet], 'algae_wafer', 100, 1)
    new_user.shrimps['Crystal_Red'] = {crs[0].id: crs[0]}
    new_user.shrimps['Shadow_Panda'] = {shadow_panda[0].id: shadow_panda[0]}
    new_user.shrimps['Crystal_Black'] = {crystal_black[0].id: crystal_black[0]}
    print("Created new user: ", new_user)
    return new_user
# Function to load an existing user using the load_data function in User class
def load_existing_user(filename):
    user_data = User.load_data(filename) # returns true or false
    print("User_data: ", user_data)
    if user_data is not False:
        new_user = User(user_data.pellets, user_data.selected_pellet, user_data.gold, user_data.id, user_data.shrimps)
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
        
def get_state_shrimps(state):
    shrimps = {}
    for id, shrimp in state.items():
        match shrimp['species']:
            case 'Crystal_Red':
                print("Getting State For Shrimp: ", state)
                new_shrimp = Crystal_Red(DEFAULT_SPAWN_X,DEFAULT_SPAWN_Y, shrimp['level'], shrimp['food_bar'], id=shrimp['id'])
                print("New Crystal_Red Shrimp HEERE", new_shrimp)
                if 'Crystal_Red' in shrimps:
                    shrimps['Crystal_Red'].update({new_shrimp.id: new_shrimp})
                else:
                    shrimps['Crystal_Red'] = {new_shrimp.id: new_shrimp}
            case 'Shadow_Panda':
                print("Getting State For Shrimp: ", state)
                new_shrimp = Shadow_Panda(DEFAULT_SPAWN_X,DEFAULT_SPAWN_Y, shrimp['level'], shrimp['food_bar'], id=shrimp['id'])
                print("New Shadow Panda Shrimp HEERE", new_shrimp)
                if 'Shadow_Panda' in shrimps:
                    shrimps['Shadow_Panda'].update({new_shrimp.id: new_shrimp})
                else:
                    shrimps['Shadow_Panda'] = {new_shrimp.id: new_shrimp}

            case 'Crystal_Black':
                print("Getting State For Shrimp: ", state)
                new_shrimp = Crystal_Black(DEFAULT_SPAWN_X,DEFAULT_SPAWN_Y, shrimp['level'], shrimp['food_bar'], id=shrimp['id'])
                print("New Crystal_Black Shrimp HEERE", new_shrimp)
                if 'Crystal_Black' in shrimps:
                    shrimps['Crystal_Black'].update({new_shrimp.id: new_shrimp})
                else:
                    shrimps['Crystal_Black'] = {new_shrimp.id: new_shrimp}
            case _:
                print("ADD OTHER SHRIMPS WHEN LOADING USER STATES")
    return shrimps