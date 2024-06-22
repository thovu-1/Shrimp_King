from ..pellet_class import *
# Algae wafer is the lowest grade food. It provides 1 satiation.
class algae_wafer(Pellet):
    def __init__(self, x, y, image_path='classes/food/food_images/algae_wafer.png', half_life=10000):
        super().__init__(x, y, image_path, 'algae_wafer', half_life, falling=True, x_vel=0, y_vel=0.5)
        self.image = pygame.image.load(image_path)
        self.satiation = 1
    def draw(self, screen):
        screen.blit(self.image, self.rect)
