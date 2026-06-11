import pygame
import random
from .base_mini_game import BaseMiniGameController
from src.algorithms.dijkstra import DijkstraSolver
from src.models.mini_game_grid import Grid


class AnalystController(BaseMiniGameController):

    NORMAL = 0
    WALL = 1
    ROUGH = 2
    GOAL = 3

    WALL_CHANCE = 0.12
    ROUGH_CHANCE = 0.22
    SCORE_MULTIPLIER = 80
    PERFECT_ROUTE_BONUS = 20

    def __init__(self, grid: Grid, view):
        super().__init__(grid, view)
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.player_path = []
        self.optimal_path = []
        self.optimal_cost = 0
        self.hint = None
        self.hint_was_used = False

    def setup(self, data=None) -> None:
        self.start_x = 0
        self.start_y = self.grid.height - 1
        self.end_x = self.grid.width - 1
        self.end_y = 0

        for y in range(self.grid.height):
            for x in range(self.grid.width):
                self.grid.set_cell(x, y, self.NORMAL)

        self.grid.set_cell(self.end_x, self.end_y, self.GOAL)

        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if (x, y) == (self.start_x, self.start_y):
                    continue
                if (x, y) == (self.end_x, self.end_y):
                    continue
                roll = random.random()
                if roll < self.WALL_CHANCE:
                    self.grid.set_cell(x, y, self.WALL)
                elif roll < self.WALL_CHANCE + self.ROUGH_CHANCE:
                    self.grid.set_cell(x, y, self.ROUGH)

        self._make_sure_path_exists()

        self.optimal_path = DijkstraSolver.find_path(
            self.grid, self.start_x, self.start_y, self.end_x, self.end_y
        )
        self.optimal_cost = self._calculate_path_cost(self.optimal_path)
        self.player_path = [(self.start_x, self.start_y)]
        self._score = 0
        self._finished = False
        self._score_added_to_player = False
        self.hint = None
        self.hint_was_used = False

    def _calculate_path_cost(self, path):
        total = 0
        for index in range(1, len(path)):
            cell_x, cell_y = path[index]
            total += self._cell_entry_cost(cell_x, cell_y)
        return total

    def _cell_entry_cost(self, x, y):
        cell_value = self.grid.get_cell(x, y)
        if cell_value == self.ROUGH:
            return 2
        return 1

    def _cell_is_walkable(self, x, y):
        cell_value = self.grid.get_cell(x, y)
        if cell_value is None:
            return False
        if cell_value == self.WALL:
            return False
        return True

    def _cells_are_neighbors(self, first_x, first_y, second_x, second_y):
        distance_x = abs(first_x - second_x)
        distance_y = abs(first_y - second_y)
        return distance_x + distance_y == 1

    def _make_sure_path_exists(self):
        path = DijkstraSolver.find_path(
            self.grid, self.start_x, self.start_y, self.end_x, self.end_y
        )
        if path:
            return

        wall_cells = []
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell_value = self.grid.get_cell(x, y)
                if cell_value == self.WALL:
                    wall_cells.append((x, y))

        while not path and wall_cells:
            random_x, random_y = random.choice(wall_cells)
            self.grid.set_cell(random_x, random_y, self.NORMAL)
            wall_cells.remove((random_x, random_y))
            path = DijkstraSolver.find_path(
                self.grid, self.start_x, self.start_y, self.end_x, self.end_y
            )

    def handle_event(self, event) -> None:
        if self._finished:
            return
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        mouse_x, mouse_y = event.pos
        clicked_x, clicked_y = self.view.get_cell_from_mouse(mouse_x, mouse_y)
        if clicked_x is None or clicked_y is None:
            return
        if not self._cell_is_walkable(clicked_x, clicked_y):
            return
        if len(self.player_path) == 0:
            return

        last_x, last_y = self.player_path[-1]

        if len(self.player_path) >= 2:
            previous_x, previous_y = self.player_path[-2]
            if clicked_x == previous_x and clicked_y == previous_y:
                self.player_path.pop()
                return

        if not self._cells_are_neighbors(last_x, last_y, clicked_x, clicked_y):
            return
        if (clicked_x, clicked_y) in self.player_path:
            return

        self.player_path.append((clicked_x, clicked_y))

        if clicked_x == self.end_x and clicked_y == self.end_y:
            self._finished = True
            self._score = self._count_final_score()

    def _count_final_score(self):
        if self.hint_was_used:
            return 0

        player_cost = self._calculate_path_cost(self.player_path)

        if player_cost == 0 or self.optimal_cost == 0:
            return 0

        base_score = int((self.optimal_cost / player_cost) * self.SCORE_MULTIPLIER)

        if player_cost == self.optimal_cost:
            base_score += self.PERFECT_ROUTE_BONUS

        return base_score

    def update(self, delta_time: float) -> None:
        pass

    def get_hint(self):
        if self._finished:
            return []
        self.hint_was_used = True
        self.hint = list(self.optimal_path)
        return self.hint

    @property
    def game_title(self) -> str:
        return "Аналитик"

    @property
    def progress_text(self) -> str:
        player_cost = 0
        if len(self.player_path) > 0:
            player_cost = self._calculate_path_cost(self.player_path)
        return f"Стоимость: {player_cost} / лучшая {self.optimal_cost}"
