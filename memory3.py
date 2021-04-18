# Memory V3
# This is the full and final version of the game.
# In this version of the game, at start, 16 items appear on the screen, with the 
# default starting image being the question mark. Whenever a tile is clicked,
# the image (which is randomly ordered for all tiles, but stays consistent per 
# tile) is revealed. When another tile is clicked, it is also revealed. If the 
# tiles match, they both permanently stay revealed. If they are different, 
# there is asmall pause and both dissapear. There is a timer in the top right 
# which indicates score. When all tiles are revealed, the timer stops 
# increasing.

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
        self.mismatched_tiles = False
        self.wrong_guess = False
        self.clear_inputs = False
        self.tile_revealed = [0]*16        
        self.successful_selection = [0]*16
        
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
        if self.clear_inputs == False:        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close_clicked = True
                if self.continue_game == True:
                        if event.type == pygame.MOUSEBUTTONUP:
                            self.mouse_location = pygame.mouse.get_pos()
                            self.update_tiles(self.mouse_location)     
        elif self.clear_inputs == True:
            pygame.event.clear()
            self.clear_inputs = False
                
    def update_tiles(self, mouse_location):
        tile_number = 0
        for row in self.grid:
            for tile in row:
                self.mismatched_tiles = tile.select(mouse_location, self.tile_size, self.check_list, self.tiles_drawn, tile, self.mismatched_tiles, tile_number, self.successful_selection, self.tile_revealed)
                if self.mismatched_tiles == True:
                    self.wrong_guess = True
                tile_number += 1
                        
    def draw_default(self):
        for row in self.grid:
            for tile in row:
                tile.draw_default(self.default_image)
                
    def draw_score(self):
        self.text_size = 80 
        self.window.set_font_size(self.text_size)        
        x_coord = (self.window.get_width()) - (self.window.get_string_width(str(int(self.score))))
        y_coord = 0
        self.window.draw_string(str(int(self.score)), x_coord, y_coord) 
        
    def draw_frame(self):
        # draw/redraw everything on the screen  
        self.window.clear() 
        self.draw_default()
        self.draw_tiles()
        self.draw_score()
        self.window.update()
        
    def draw_tiles(self):
        tile_number = 0
        for row in self.grid:
            for tile in row:
                for tile_test in self.check_list:
                    if tile == tile_test:                        
                        if len(self.check_list) == 1:
                            tile.draw(self.image_list[tile_number], self.successful_selection, tile_number, self.tiles_drawn, 'draw_num')
                        elif len(self.check_list) == 2:
                            if tile == self.check_list[0]:
                                tile.draw(self.image_list[tile_number], self.successful_selection, tile_number, self.tiles_drawn, '')   
                            elif tile == self.check_list[1]:
                                tile.draw(self.image_list[tile_number], self.successful_selection, tile_number, self.tiles_drawn, 'draw_num')
                for tile_test in self.tiles_drawn:
                    if tile == tile_test:
                        tile.draw(self.image_list[tile_number], self.successful_selection, tile_number, self.tiles_drawn, 'perm')
                tile_number += 1      
                
    def update_state(self):
        self.score = time.time() - self.start_time
        if self.wrong_guess == True:
            time.sleep(0.8)
            self.clear_inputs = True
            self.wrong_guess = False
        if (len(self.check_list) == 2):
            self.check_list.clear()   
        if (len(self.tiles_drawn) == 16):
            self.continue_game = False
        time.sleep(0.2)
    
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
        cls.image_num = ''
        cls.text_size = 50         
    
    def draw(cls, image_num, successful_selection, tile_number, tiles_drawn, check_drawn):
        cls.window.get_surface().blit(pygame.image.load(image_num), (cls.left, cls.top))
        cls.image_num = image_num
        cls.window.set_font_size(cls.text_size)
        if check_drawn == 'draw_num':
            cls.window.draw_string(str(int(successful_selection[tile_number])), cls.tile_location[0], cls.tile_location[1])
        if check_drawn == 'perm':
            if len(tiles_drawn) > 0:       
                cls.window.draw_string(str(int(successful_selection[tile_number])), cls.tile_location[0], cls.tile_location[1])
        
    def draw_default(cls, default_image):
        cls.window.get_surface().blit(pygame.image.load(default_image), (cls.left, cls.top))
    
    def get_location(cls):
        return cls.tile_location
    
    def get_image_num(cls):
        return cls.image_num
    
    def select(cls, mouse_location, tile_size, check_list, tiles_drawn, tile, mismatched_tiles, tile_number, successful_selection, tile_revealed):
        if (mouse_location[0] > cls.tile_location[0] and mouse_location[1] > cls.tile_location[1] and mouse_location[0] < (cls.tile_location[0] + tile_size[0]) and mouse_location[1] < (cls.tile_location[1] + tile_size[1])):
            if(len(check_list) < 2):
                already_in_check_list = False
                already_in_drawn_list = False
                for list_check in check_list:
                    if (list_check == tile):
                        already_in_check_list = True
                for drawn_check in tiles_drawn:
                    if (drawn_check == tile):
                        already_in_drawn_list = True
                if ((already_in_check_list == False) and (already_in_drawn_list == False)):
                    check_list.append(tile) 
                    successful_selection[tile_number] += 1
                        
            if(len(check_list) == 2):
                if (len(tiles_drawn) >= 0):
                    already_in_list = False
                    for check in tiles_drawn:
                        if (check == tile):
                            already_in_list = True
                    if already_in_list == False:
                        if check_list[0].get_image_num() == check_list[1].get_image_num():
                            tiles_drawn.append(check_list[0])
                            tiles_drawn.append(check_list[1]) 
                        else:
                            mismatched_tiles = True
                            return mismatched_tiles
main()