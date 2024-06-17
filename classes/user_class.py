import math
import pygame
import pickle
import random
from dotenv import load_dotenv
import os
from funcs_and_variables import *
from classes.pellet_class import *
from classes.shrimp_class import *
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
        pellets = {}
        for pellet in self.pellets:
            pellets.update(pellet.get_state())
            #pellets.append(pellet.get_state())
        print("PELLETS state[pellets]:", pellets)
        state['pellets'] = pellets
        if self.shrimps is not None:
            for species, shrimp_dict in self.shrimps.items():
                for id, shrimp in shrimp_dict.items():
                    shrimps[id] = shrimp.get_state()
        state['shrimps'] = shrimps
        print('SAVING STATE: ', state)
        return state
    def __setstate__(self, state):
        print("LOADING STATE:", state)

        self.id = state['id']
        self.money = state['money']
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
    # crs = [Shrimp(DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y, 1, 0, 'CRS', DIRECTION ),   \
    #        Shrimp(DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y, 2, 0, 'CRS', DIRECTION ), \
    #         Shrimp(DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y, 3, 0, 'CRS', DIRECTION)]
    # d = {crs[0].id: crs[0], crs[1].id: crs[1], crs[2].id: crs[2]}

    crs = [Shrimp(DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y, 2, 0, 'CRS', DIRECTION )]
    d = {crs[0].id: crs[0]}
    pellet = Pellet(0,0,'food_images/algae_wafer.png', 'algae_wafer', 10000)
    new_user = User([pellet], 'algae_wafer', 100, 1)
    new_user.shrimps['CRS'] = d
    print("Created new user: ", new_user)
    return new_user
# Function to load an existing user using the load_data function in User class
def load_existing_user(filename):
    user_data = User.load_data(filename) # returns true or false
    print("User_data: ", user_data)
    if user_data is not False:
        print("Creating new user: ", user_data)
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
