import pygame
import random
from .base_mini_game import BaseMiniGameController
from src.algorithms.bfs_matcher import BFSMatcher
from src.models.mini_game_grid import Grid

class GardenerController(BaseMiniGameController):
    WEED_PROBABILITY = 0.3
    BONUS_COMPLETE = 20
    TARGET_TYPE = 1  # что ищем

    def __init__(self, grid: Grid, view):
        super().__init__(grid, view)
        self._remaining_weeds = 0
        self._cleared_weeds = 0
        self.hint = None  # подсказка

    def setup(self, data=None) -> None:
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if random.random() < self.WEED_PROBABILITY:
                    self.grid.set_cell(x, y, self.TARGET_TYPE)
                else:
                    self.grid.set_cell(x, y, 0)

        self._remaining_weeds = self.grid.count_cells(self.TARGET_TYPE)
        self._cleared_weeds = 0
        self._score = 0
        self._finished = False
        self._score_added_to_player = False
        self.hint = None

    def handle_event(self, event) -> None:
        if self._finished:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            grid_x, grid_y = self.view.get_cell_from_mouse(mouse_x, mouse_y)
            if grid_x is None or grid_y is None:
                return
            cell_value = self.grid.get_cell(grid_x, grid_y)
            if cell_value != self.TARGET_TYPE:
                return

            area = BFSMatcher.find_connected(self.grid, grid_x, grid_y, self.TARGET_TYPE)
            if not area:
                return

            for connect_x, connect_y in area:
                self.grid.set_cell(connect_x, connect_y, 0)
            self._cleared_weeds += len(area)
            self._score += len(area)
            self._remaining_weeds -= len(area)
            self.hint = None

            if self._remaining_weeds == 0:
                self._finished = True
                self._score += self.BONUS_COMPLETE

    def update(self, dt: float) -> None:
        pass

    def get_hint(self):
        """
        Находит первую связную область сорняков и возвращает её координаты,
        а также сохраняет в self.hint для отрисовки.
        """
        if self._finished:
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
    def game_title(self) -> str:
        return "Садовник"

    @property
    def progress_text(self) -> str:
        total = self._remaining_weeds + self._cleared_weeds
        return f"Сорняков: {self._cleared_weeds}/{total}"

    @property
    def remaining_weeds(self) -> int:
        return self._remaining_weeds

    @property
    def cleared_weeds(self) -> int:
        return self._cleared_weeds