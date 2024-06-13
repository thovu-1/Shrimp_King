import pygame
from shrimp_classes import *


pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shrimp King')

save_file = 'crs_states.pkl'
# async def save_on_exit_async():
#     await save_shrimp_states_async(shrimps, save_file)

# # Load CRS states asynchronously
# async def load_states():
#     return await load_shrimp_states_async(save_file)

# # On exist save shrimp states asynchronously
# atexit.register(asyncio.run, save_on_exit_async())
# Function to load shrimp states from file asynchronously

def load_shrimp_states(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            states = pickle.load(f)
            shrimps=[]
            for state in states:
                if 'CRS' in filename:
                    shrimp = CRS(state['x'], state['y'], state['age'])
                    shrimps.append(shrimp)
            return shrimps
        
async def load_shrimp_states_async(filename):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, load_shrimp_states, filename)
# shrimps = asyncio.run(load_states())
shrimps = []
crs = CRS(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0)
shrimps.append(crs)
# Function to save shrimp states on exit
# if not shrimps:
#     # If you don't have any shrimps, start with a CRS
#     shrimps = [CRS(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0)]
run = True

while run:
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            run = False

    screen.fill((0,105,148))
 
    for shrimp in shrimps:
        shrimp.move(SCREEN_WIDTH, SCREEN_HEIGHT)


    # Draw all shrimps
    for shrimp in shrimps:
        shrimp.draw(screen)

    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(60)  
