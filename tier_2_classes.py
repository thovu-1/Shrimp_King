from tier_1_classes import *

# ---------------------------------------------------------------- Shrimp Species Classification -------------------------------- #####

class CRS(Shrimp):
    def __init__(self, x, y, level, food_bar, image_path='shrimp_images/CRS.png'):
        super().__init__(x, y, level, food_bar, 'CRS', DIRECTION, image_path)


# ---------------------------------------------------------------- Food Type Classification ------------------------------------- #####
# Algae wafer is the lowest grade food. It provides 1 satiation.
class algae_wafer(Pellet):
    def __init__(self, x, y, image_path='food_images/algae_wafer.png', half_life=10000):
        super().__init__(x, y, image_path, 'algae_wafer', half_life, falling=True, x_vel=0, y_vel=0.5)
        self.image = pygame.image.load(image_path)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

