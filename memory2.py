# Memory V2
# In this version of the game, 16 items appear on the screen, in a random order 
# every time the game is run. There is a score counter in the top right corner.
# Every time a tile is clicked, the tile is revealed permanently.

from uagame import Window
import pygame
import random
import time
from pygame.locals import *

def main():
    # main algorithm: create the window and play the game
    window = Window('Memory', 512, 410)
    window.set_auto_update(False) # tell the window to only update when told, not automatically
    game = Game(window)
    game.play() # call .play() method to run game which is a Game object
    #window.close(), this doesn't work for some reason
    pygame.display.quit()   # close display
    
class Game:
    def __init__(self, window):
        # set up new Game object
        # self - the Game to initialize
        # window - uagame.Window object
        self.window = window
        Tile.set_window(window)
        self.close_clicked = False  # tells us if the window is trying to be closed
        self.continue_game = True
        self.image_list = []
        self.default_image = 'image0.bmp'     
        self.input_images()   
        self.tiles_drawn = []
        self.check_list = []
        self.temp_list = []
        
        self.text_size = 80
        self.text_color = "white"
        window.set_font_size(self.text_size)
        window.set_font_color(self.text_color)
        self.start_time = time.time()
        self.score = 0.0
        self.start_test = time.perf_counter()
        self.score_test = 0.0
        self.mouse_location = [0,0]
        self.gap = 2
        self.tile_size = (100, 100)        
        self.game_pause_time = 0.2
        
        self.init_grid()
        
    def init_grid(self):
        self.grid = [ ]
        x_coord = self.gap
        y_coord = self.gap
        for row_num in range(0,4):
            row = [ ]
            x_coord = self.gap
            for column_num in range(0,4):
                tile_location = (x_coord, y_coord)
                tile = Tile(self.tile_size, tile_location)
                row.append(tile)
                x_coord += self.tile_size[0] + self.gap                
            self.grid.append(row)
            y_coord += self.tile_size[1] + self.gap
            
    def input_images(self):
        for image in range(1,9):
            self.image_list.append('image' + str(image) + '.bmp')
        self.image_list += self.image_list
        for times_shuffled in range(0, random.randint(1,5)):    
            random.shuffle(self.image_list)
        
    def play(self):
        # while window is not trying to be closed, run the game
        while self.close_clicked == False:
            self.handle_events()      
            self.draw_frame()  
            if self.continue_game == True:
                self.update_state()                
                
    def handle_events(self):
        # check if window is trying to be closed. If it is, set bool to true
        #pygame.event.clear(MOUSEMOTION)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_location = pygame.mouse.get_pos()
                self.update_position(self.mouse_location)                
                
    def update_position(self, mouse_location):
        for row in self.grid:
            for tile in row:    
                tile.select(mouse_location, self.tile_size, self.tiles_drawn, tile)
                            
    def draw_default(self):
        for row in self.grid:
            for tile in row:
                tile.draw_default(self.default_image)
        
    def draw_frame(self):
        # draw/redraw everything on the screen
        self.window.clear() 
        self.draw_default()
        self.draw_tiles()
        self.draw_score()
        self.window.update()
    
    def draw_score(self):
        x_coord = (self.window.get_width()) - (self.window.get_string_width(str(int(self.score))))
        y_coord = 0
        self.window.draw_string(str(int(self.score)), x_coord, y_coord)
        
    def draw_tiles(self):
        tile_number = 0
        for row in self.grid:
            for tile in row:
                for tiles_test in self.tiles_drawn:
                    if tile == tiles_test:
                        tile.draw(self.image_list[tile_number])
                        break
                tile_number += 1                
        
    def update_state(self):
        self.score = time.time() - self.start_time
        time.sleep(self.game_pause_time)      
        if (len(self.tiles_drawn) == 16):
            self.continue_game = False        
    
class Tile:    
    window = None
    border_color = 'black'
    border_width = 2
    @classmethod
    def set_window (cls, window):
        cls.window = window
    
    def __init__(cls, size, tile_location):
        cls.tile_location = tile_location
        cls.left = tile_location[0]
        cls.top = tile_location[1]
        cls.border = Rect((0,0),(100,cls.window.get_height())) 
    
    def draw(cls, image_num):
        cls.window.get_surface().blit(pygame.image.load(image_num), (cls.left, cls.top))
        
    def draw_default(cls, default_image):
        cls.window.get_surface().blit(pygame.image.load(default_image), (cls.left, cls.top))
    
    def get_location(cls):
        return cls.tile_location
    
    def select(cls, mouse_location, tile_size, tiles_drawn, tile):
        if (mouse_location[0] > cls.tile_location[0] and mouse_location[1] > cls.tile_location[1] and mouse_location[0] < (cls.tile_location[0] + tile_size[0]) and mouse_location[1] < (cls.tile_location[1] + tile_size[1])):
            if (len(tiles_drawn) == 0):
                tiles_drawn.append(tile)
            elif (len(tiles_drawn) > 0):
                already_in_list = False
                for check in tiles_drawn:
                    if (check == tile):
                        already_in_list = True
                if already_in_list == False:
                    tiles_drawn.append(tile)
main()