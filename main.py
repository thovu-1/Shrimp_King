from tier_1_classes import *
from tier_2_classes import *
from funcs import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shrimp King')



async def main():
    # First we set up variables and load in user_states into current_user
    current_user = await load_user_states_async(SAVE_FILE)
    shrimps = current_user.shrimps
    pellets_on_screen = []

    # Start the game
    run = True
    while run:
        # Track keys 
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                await save_user_states_async(current_user, SAVE_FILE)
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
                shrimp.move(SCREEN_WIDTH, SCREEN_HEIGHT, pellets_on_screen if len(pellets_on_screen) > 0 else None)
                shrimp.draw(screen)

        # Update screen
        pygame.display.flip()
        # Control frame rate
        pygame.time.Clock().tick(30)  

if __name__ == "__main__":
    asyncio.run(main())
# On exist save shrimp states asynchronously
