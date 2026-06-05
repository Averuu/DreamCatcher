import random

import pygame

from .base_mini_game import BaseMiniGameController
from src.algoritms.bfs_matcher import BFSMatcher


class GardenerContorller(BaseMiniGameController):
    def __init__(self, grid, view):
        super().__init__(grid, view)
        self.target_type = 1
        self.total_weeds = 0
        self.cleared_weeds = 0

    def setup(self, data=None):
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if random.randint(1, 6) <= 2:
                    self.grid.set_cell(x, y, 1)
                    self.total_weeds += 1
                else:
                    self.grid.set_cell(x, y, 0)
        self.finished = False
        self.score = 0
        self.cleared_weeds = 0
    
    def handle_event(self, event):
        if self.finished == True:
            return None
        
        if event.type == pygame.MOUSEBUTONDOWN and event.button == 1:
            x, y = event.pos
            square_x, square_y = self.view.get_cell_from_mouse(x, y)
            if square_x is not None and square_y is not None:
                if self.grid.get_cell(square_x, square_y) == self.target_type:
                    squares = BFSMatcher.find_connected(
                        self.grid, square_x, square_y, self.target_type
                    ):
                    if squares:
                        for weed_x, weed_y in squares:
                            self.grid.set_cell(weed_x, weed_y, 0)
                        self.cleared_weeds += len(squares)
                        self.score += len(squares)

                        weeds_left = 0
                        for y in range(self.grid.height):
                            for x in range(self.grid.width):
                                target = self.target_type
                                if self.grid.get_cell(x, y) == target:
                                    weeds_left += 1
                        
                        if weeds_left == 0:
                            self.finished = True
                            self.score += self.bonus
    
    def update(self, val):
        pass

    def get_hint(self):
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if self.grid.get_cell(x, y) == self.target_type:
                    squares = BFSMatcher.find_connected(self.grid,
                                                        x, y,
                                                        self.target_type)
                    if squares:
                        return squares
        return []