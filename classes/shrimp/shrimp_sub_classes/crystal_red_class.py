from classes.shrimp.shrimp_class import *

# ---------------------------------------------------------------- Shrimp Species Classification -------------------------------- #####

class Crystal_Red(Shrimp):
    def __init__(self, x, y, level, food_bar, id = None):
        super().__init__(x, y, level, food_bar, 'Crystal_Red', DIRECTION, id)
        self.level = level
        self.next_level =  0 
        self.passive_gold_generation = 1
        self.get_next_level()

    def eat(self, pellet_satiation):
        # print("ID:", self.id, 'Level:', self.level, 'Food:', self.food_bar, 'Next_Level:', self.next_level)
        self.eatting = True
        self.x_vel = 0
        self.y_vel = 0
        self.food_bar += pellet_satiation
        print("Yummy, Food_Bar:", self.food_bar, 'Next_Level:', self.next_level, 'Species:', self.species)
        if self.food_bar >= self.next_level:
            self.level_up()
    
    def get_next_level(self):
        if self.level == 1:
            self.next_level = 5
            self.passive_gold_generation = 1
        elif self.level == 2:
            self.next_level = 10
            self.passive_gold_generation = 2
        elif self.level >= 3:
            self.next_level = self.level * 10
            self.passive_gold_generation = self.passive_gold_generation * 2
        print("ID:", self.id, 'Level:', self.level, 'Gold_Generation:', self.passive_gold_generation)

    def level_up(self):
        self.level = self.level + 1
        self.get_next_level()
        if self.level <= 3:
            self.sprite_data = self.load_sprites()['Crystal_Red'][self.level]  # Update Sprite Data
            self.sprite_sheet = self.sprite_data['sprite_sheet']
            self.frame_rects = self.sprite_data['frame_rects']
            self.first_frame_rect = self.frame_rects[0]  # Assuming frames are consistent in size

    def load_sprites(self):
        d = {}
        # Load sprite sheets
        shrimplet_sprite_sheet = pygame.image.load('shrimp_images/Shrimplet_Crystal_Red.png').convert_alpha()
        juvenile_sprite_sheet = pygame.image.load('shrimp_images/Juvenile_Crystal_Red.png').convert_alpha()
        adult_sprite_sheet = pygame.image.load('shrimp_images/Adult_Crystal_Red.png').convert_alpha()

        # Load frame data from JSON files
        with open('shrimp_images/Shrimplet_Crystal_Red.json') as f:
            shrimplet_data = json.load(f)
        with open('shrimp_images/Juvenile_Crystal_Red.json') as f:
            juvenile_data = json.load(f)
        with open('shrimp_images/Adult_Crystal_Red.json') as f:
            adult_data = json.load(f)

        # Extract frame rectangles from JSON data
        shrimplet_rects = [pygame.Rect(frame['frame']['x'], frame['frame']['y']+6, frame['frame']['w'], frame['frame']['h']-15) for frame in shrimplet_data['frames'].values()]
        juvenile_rects = [pygame.Rect(frame['frame']['x'], frame['frame']['y']+15, frame['frame']['w'], frame['frame']['h']-35) for frame in juvenile_data['frames'].values()]
        adult_rects = [pygame.Rect(frame['frame']['x'], frame['frame']['y']+30, frame['frame']['w'], frame['frame']['h']-70) for frame in adult_data['frames'].values()]
        # Store sprite data in dictionary
        
        d2={}
        d2[1] = {'sprite_sheet': shrimplet_sprite_sheet, 'frame_rects': shrimplet_rects}
        d2[2] = {'sprite_sheet': juvenile_sprite_sheet, 'frame_rects': juvenile_rects}
        d2[3] = {'sprite_sheet': adult_sprite_sheet, 'frame_rects': adult_rects}
        d['Crystal_Red'] = d2
        return d

    # Functions for saving shrimp information
    def get_state(self):
        return {
                'id': self.id,
                'species': self.species,
                'level': self.level,
                'food_bar': self.food_bar,
                }
    # Functions for loading shrimp information
    def set_state(self, state):
        # Set state from dictionary
        self.level = state['level']
        self.food_bar = state['food_bar']
