import random
from src.models.mini_game_grid import Grid
from src.algorithms.bfs_matcher import BFSMatcher


class GardenerGame:

    WEED_PROBABILITY = 0.3
    BONUS_COMPLETE = 20
    TARGET_TYPE = 1

    def __init__(self):
        self.grid = Grid(10, 10)
        self.remaining_weeds = 0
        self.cleared_weeds = 0
        self.score = 0
        self.finished = False
        self.hint = None

    def setup(self):
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if random.random() < self.WEED_PROBABILITY:
                    self.grid.set_cell(x, y, self.TARGET_TYPE)
                else:
                    self.grid.set_cell(x, y, 0)

        self.remaining_weeds = self.grid.count_cells(self.TARGET_TYPE)
        self.cleared_weeds = 0
        self.score = 0
        self.finished = False
        self.hint = None

    def handle_clear(self, grid_x, grid_y):
        if self.finished:
            return
        cell_value = self.grid.get_cell(grid_x, grid_y)
        if cell_value != self.TARGET_TYPE:
            return

        area = BFSMatcher.find_connected(self.grid, grid_x, grid_y, self.TARGET_TYPE)
        if not area:
            return

        for connect_x, connect_y in area:
            self.grid.set_cell(connect_x, connect_y, 0)
        self.cleared_weeds += len(area)
        self.score += len(area)
        self.remaining_weeds -= len(area)
        self.hint = None

        if self.remaining_weeds == 0:
            self.finished = True
            self.score += self.BONUS_COMPLETE

    def get_hint_area(self):
        if self.finished:
            return []
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if self.grid.get_cell(x, y) == self.TARGET_TYPE:
                    area = BFSMatcher.find_connected(self.grid, x, y, self.TARGET_TYPE)
                    if area:
                        self.hint = area
                        return area
        self.hint = []
        return []

    @property
    def progress_text(self):
        total = self.remaining_weeds + self.cleared_weeds
        return f"Сорняков: {self.cleared_weeds}/{total}"
