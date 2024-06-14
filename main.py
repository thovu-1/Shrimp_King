import pygame
from tier_1_classes import *
from tier_2_classes import *
from funcs import *
pygame.init()



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shrimp King')

save_file = 'save_files/user_data.pkl'


# This function will 'unpickle' the data from the user save file.
def load_user_states(filename): 

        user_data = User.load_data(filename)

        if user_data is not False:
            new_user = User(user_data.pellets, user_data.selected_pellet, user_data.money, user_data.id, user_data.shrimps)
            print("Loading existing user: ", new_user.id ,new_user.name)
            return new_user
        else:
            print("Current user not found, creating new user...")
            # if there is no user, create a user with a crs in the shrimps state
            crs = [CRS(DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y, 0, 0), CRS(DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y, 0, 0)]
            d = {crs[0].id: crs[0], crs[1].id: crs[1]}
            pellets = algae_wafer(0,0) # Starting food is algae wafer
            new_user = User([pellets], 'algae_wafer', 100, 1)
            new_user.shrimps['CRS'] = d
            print("Created new user: ", new_user)
            return new_user

def new_user_load(filename):
    print()
# This function calls load_user_states asynchronously
async def load_user_states_async(filename):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, load_user_states, filename)

# This function saves the user_states asynchronuously
async def save_user_states_async(user:User, filename):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, user.save_data, filename)



async def main():
    # First we set up variables and load in user_states into current_user
    current_user = await load_user_states_async(save_file)
    # shrimps_on_screen = current_user.shrimps.items()
    # for key, value in current_user.shrimps.items():
        

    #     print(f'{key}: {value}')
    pellets_on_screen = []

    # Start the game
    run = True
    while run:
        # Track keys 
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                await save_user_states_async(current_user, save_file)
                pygame.quit()
                sys.exit()
            # This is how we handle dropping the pellets
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                if current_user.selected_pellet == 'algae_wafer':
                    pellets_on_screen.append(algae_wafer(x,y))
                else:
                    print("ADD SOME DAMN PELLETS TO THE GAME")

        # This is how I am coloring the background currently.
        screen.fill((0,105,148))
        
        # Display and move objects 
        if len(pellets_on_screen) > 0:
            for pellet in pellets_on_screen:
                pellet.check_half_life()
                if pellet.expired:
                    pellets_on_screen.remove(pellet)
                else:
                    pellet.fall(SCREEN_HEIGHT)
                    pellet.draw(screen)
                
        for species, shrimps in current_user.shrimps.items():
            for id, shrimp in shrimps.items():
                shrimp.move(SCREEN_WIDTH, SCREEN_HEIGHT)
                shrimp.draw(screen)

        # Update screen
        pygame.display.flip()
        # Control frame rate
        pygame.time.Clock().tick(60)  

if __name__ == "__main__":
    asyncio.run(main())
# On exist save shrimp states asynchronously
