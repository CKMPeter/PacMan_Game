from PIL import Image, ImageTk, GifImagePlugin

class something_moves:
    def __init__(self, name, x, y, cdirection):
        self.name = name
        self.x = x
        self.y = y
        self.center_x = x + 5
        self.center_y = y + 6
        self.imgs = []
        self.cdirection = cdirection
        self.state = 1
        self.turn_allowed = [False, False, False, False]
        
class player(something_moves):
    def powerup(self):
        self.powerup = False
    def add_frame(self):
        for i in range (1, 5):
            self.imgs.append(Image.open(f'player/{i}.png').resize((30,30)))
            
class ghost(something_moves):
        
    def turn(self):
        self.turn
    def target(self, player_x, player_y):
        self.target_x = player_x
        self.target_y = player_y
    def add_info(self, file, Id, box):
        self.id = Id
        self.imgs.append(Image.open(f'ghost/{file}.png').resize((30, 30)))
        self.in_box = box
        #self.turns, self.in_box = self.check_collisions()
        # self.rect = self.draw()
        
        




