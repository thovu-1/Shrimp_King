from classes.shrimp_class import *
from classes.tier_2_classes import *
from funcs_and_variables import *
from classes.user_class import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shrimp King')

background = pygame.image.load('other_images/aquarium_background1.png')
background = background.convert()

icon = pygame.image.load('other_images/icon.png')
icon = icon.convert()

pygame.display.set_icon(icon)
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
        # Blit the background image to the screen
        screen.blit(background, (0, 0))
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
                pellet_index = shrimp.rect.collidelist(pellets_on_screen)
                current_time = pygame.time.get_ticks()
                if pellet_index!= -1 and len(pellets_on_screen) >= pellet_index:
                    if shrimp.level == 1 and current_time - shrimp.eatting_timer > 500:
                        pellets_on_screen[pellet_index].expired = True
                        shrimp.eat()
                        shrimp.eatting_timer = current_time
                    elif shrimp.level == 2 and current_time - shrimp.eatting_timer > 1000:
                        pellets_on_screen[pellet_index].expired = True
                        shrimp.eat()
                        shrimp.eatting_timer = current_time
                    elif shrimp.level >= 3 and current_time - shrimp.eatting_timer > 1500:
                        # Remove pellet
                        pellets_on_screen[pellet_index].expired = True
                        shrimp.eat()
                        shrimp.eatting_timer = current_time
                else:
                    shrimp.eatting = False

                shrimp.move(SCREEN_WIDTH, SCREEN_HEIGHT, pellets_on_screen if len(pellets_on_screen) > 0 else None)
                shrimp.draw(screen)

        # Update screen
        pygame.display.flip()
        # Control frame rate
        pygame.time.Clock().tick(30)  

if __name__ == "__main__":
    asyncio.run(main())
# On exist save shrimp states asynchronously
