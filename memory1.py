# Memory V1
# In this version of the game, 16 items appear on the screen, in a random order 
# every time the game is run. There is no user entry for clicking on images, 
# and there is no score counted. 

from uagame import Window
import pygame
import random
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
        #self.default_image = pygame.image.load('image0.bmp')        
        self.input_images()        
        self.init_grid()
        
    def init_grid(self):
        gap = 2
        tile_size = (100, 100)
        self.grid = [ ]
        x_coord = gap
        y_coord = gap
        for row_num in range(0,4):
            row = [ ]
            x_coord = gap
            for column_num in range(0,4):
                tile_location = (x_coord, y_coord)
                tile = Tile(tile_size, tile_location)
                row.append(tile)
                x_coord += tile_size[0] + gap                
            self.grid.append(row)
            y_coord += tile_size[1] + gap
            
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
            self.update()
                
    def handle_events(self):
        # check if window is trying to be closed. If it is, set bool to true
        #pygame.event.clear(MOUSEMOTION)
        event = pygame.event.poll()
        
        if event.type == pygame.QUIT:
            self.close_clicked = True
            
    def draw_frame(self):
        # draw/redraw everything on the screen
        self.window.clear() 
        self.draw_tiles()
        self.window.update()
        
    def draw_tiles(self):
        tile_number = 0
        for row in self.grid:
            for tile in row:
                tile.draw(self.image_list[tile_number])
                tile_number += 1
                
    def update(self):
        pass
    
class Tile:    
    window = None
    fg_color = 'white'
    border_width = 2
    
    @classmethod
    def set_window (cls, window):
        cls.window = window
    
    def __init__(self, size, tile_location):
        self.left = tile_location[0]
        self.top = tile_location[1]

    #def is_filled(self):
        #return self.content != ''
    
    def draw(self, image):
        self.window.get_surface().blit(pygame.image.load(image), (self.left, self.top))
        
main()