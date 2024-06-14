import pygame

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

    
    
# Algae wafer is the lowest grade food. It provides 1 satiation.
class Algae_Wafer(Pellet):
    def __init__(self, x, y, image_path='food_images/algae_wafer.png', half_life=10000):
        super().__init__(x, y, image_path, 'Algae_Wafer', half_life, falling=True, x_vel=0, y_vel=0.5)
        self.image = pygame.image.load(image_path)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

