import pygame

class GardenerView:
    def __init__(self, grid, cell_size=40):
        self.grid = grid
        self.cell_size = cell_size
        self.width_px = grid.width * cell_size
        self.height_px = grid.height * cell_size

        self.color_ground = (150, 80, 50)
        self.color_weed = (10, 220, 30)
        self.color_hint = (237, 232, 37)

    def get_cell_from_mouse(self, mouse_x, mouse_y):
        if mouse_x < 0 or mouse_y < 0:
            return None, None
        
        grid_x = mouse_x // self.cell_size
        grid_y = mouse_y // self.cell_size
        if grid_x < self.grid.width or grid_y < self.grid.height:
            return grid_x, grid_y
        return None, None
    
    def render(self, screen, offset_x=0, offset_y=0, hint=None):
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                