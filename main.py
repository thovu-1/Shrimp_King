from classes.shrimp.shrimp_class import *
from classes.shrimp.shrimp_sub_classes.crystal_red_class import *
from Models.funcs_and_variables import *
from classes.user_class import *
from classes.food.sub_food_classes.algae_wafer_class import *

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shrimp King')

minecraft_font = pygame.font.Font('fonts/minecraft_font.ttf', 64)
gold_color = (253,203,23)



icon = pygame.image.load('other_images/icon.png')
icon = icon.convert()

pygame.display.set_icon(icon)
async def main():
    # First we set up variables and load in user_states into current_user
    current_user = await load_user_states_async(SAVE_FILE)
    loaded_user_shrimp_ids = load_user_shrimps(current_user)
    shrimps = current_user.shrimps
    pellets_on_screen = []
    bg,bg_frames = await load_background_async()
    current_frame = 0
    last_frame_update = pygame.time.get_ticks() 
    gold_tick_buffer = pygame.time.get_ticks()
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
                    print(x,y)
                else:
                    print("ADD SOME DAMN PELLETS TO THE GAME")

        # This is how I am coloring the background currently.
        screen.fill((0,105,148))

        current_time = pygame.time.get_ticks()
        if current_time - last_frame_update > 1000:
            current_frame = (current_frame + 1) % len(bg_frames)
            last_frame_update = current_time
        
        screen.blit(bg, (0, 0), bg_frames[current_frame])
        # Blit the background image to the screen

        # Display and move objects 
        if len(pellets_on_screen) > 0:
            for pellet in pellets_on_screen:
                pellet.check_half_life()
                if pellet.expired:
                    pellets_on_screen.remove(pellet)
                else:
                    pellet.fall(SCREEN_HEIGHT)
                    pellet.draw(screen)

        for species, id_list in loaded_user_shrimp_ids.items():
            for id in id_list: 
                current_shrimp = current_user.shrimps[species][id]
                pellet_index = current_shrimp.rect.collidelist(pellets_on_screen)
            # Keep track of current time for food eatting cooldowns
                handle_shrimp_scavenging(pellets_on_screen, pellet_index, current_shrimp)
                gold_timer = pygame.time.get_ticks()
                if gold_timer - gold_tick_buffer > 500:
                    current_user.get_gold(current_shrimp)
                    gold_tick_buffer = pygame.time.get_ticks()
                current_shrimp.move(SCREEN_WIDTH, SCREEN_HEIGHT, pellets_on_screen if len(pellets_on_screen) > 0 else None)
                screen.blit(minecraft_font.render('$ ' + str(current_user.gold), False, gold_color), (0,10))
                current_shrimp.draw(screen)
        # Update screen
        pygame.display.flip()
        # Control frame rate
        pygame.time.Clock().tick(30)  

if __name__ == "__main__":
    asyncio.run(main())
# On exist save shrimp states asynchronously


