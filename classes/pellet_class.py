# Pellet class represents food that we feed our shrimp.
import pygame


class Pellet:
    next_id = 1
    def __init__(self, x, y, image_path, type, half_life, falling=True, x_vel=0, y_vel=0.5, id=None):
            if id == None:
                self.id = Pellet.next_id
                Pellet.next_id += 1
            else:
                self.id = id
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

            # Helper function to unpickle all saved pellets
    def get_state_pellets(state):
        pellet_list = []
        for type, pellet in state.items():
            match pellet:
                case 'algae_wafer':
                    pellet = Pellet(0,0,'food_images/algae_wafer.png', 'algae_wafer', 10000)
                    pellet_list.append(pellet)
                case _:
                    print("ADD OTHER PELLETS WHEN LOADING USER STATES")
        return pellet_list