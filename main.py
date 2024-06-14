import pygame
from shrimp_classes import *
from food_classes import *

pygame.init()

# Defining Global Variables and setting up the display
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
DEFAULT_SPAWN_X = SCREEN_WIDTH // 2
DEFAULT_SPAWN_Y = SCREEN_HEIGHT // 2
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shrimp King')

save_file = 'save_files/user_data.pkl'


# This function will 'unpickle' the data from the user save file.
def load_user_states(filename): 
    try:
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                money = pickle.load(f)
                selected_pellet = pickle.load(f)
                num_shrimps = pickle.load(f)
                shrimps = []
                pellets = []
                for _ in range(num_shrimps):
                    shrimp_state = pickle.load(f)  # Load shrimp state
                    
                    match shrimp_state['name']:
                        case 'CRS':
                            shrimp = CRS(DEFAULT_SPAWN_X, DEFAULT_SPAWN_Y, shrimp_state['level'], shrimp_state['food_bar'])
                            shrimps.append(shrimp)
                        case _:
                            print("ADD MORE SHRIMP SPECIES")

                num_pellets = pickle.load(f)
                for _ in range(num_pellets):
                    pellet_state = pickle.load(f)  # Load pellet state
                    match pellet_state['type']:
                        case 'Algae_Wafer':
                            pellet = Algae_Wafer(0,0)
                            pellets.append(pellet)
                        case _:
                            print("ADD OTHER PELLETS WHEN LOADING USER STATES")

                return User(shrimps, pellets, selected_pellet, money)
        else:
            # if there is no user, create a user with a crs in the shrimps state
            crs = [CRS(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0, 0), CRS(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0, 0)]
            pellets = Algae_Wafer(0,0) # Starting food is algae wafer
            new_user = User(crs, [pellets], 'Algae_Wafer', 100, 1)
            return new_user
    except EOFError as e:
        print(f"EOFError: {e}. Possibly ran out of data in {filename}.")

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
    shrimps_on_screen = current_user.shrimps
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
                if current_user.selected_pellet == 'Algae_Wafer':
                    pellets_on_screen.append(Algae_Wafer(x,y))
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
                
        for shrimp in shrimps_on_screen:
            shrimp.move(SCREEN_WIDTH, SCREEN_HEIGHT)
            shrimp.draw(screen)

        # Update screen
        pygame.display.flip()
        # Control frame rate
        pygame.time.Clock().tick(60)  

if __name__ == "__main__":
    asyncio.run(main())
# On exist save shrimp states asynchronously
