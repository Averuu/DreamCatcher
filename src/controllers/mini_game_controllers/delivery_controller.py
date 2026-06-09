import pygame
import random
from .base_mini_game import BaseMiniGameController
from src.algorithms.astar import AStarSolver
from src.models.mini_game_grid import Grid


class DeliveryController(BaseMiniGameController):

    OBSTACLE_CHANCE = 0.28
    SCORE_MULTIPLIER = 80
    PERFECT_ROUTE_BONUS = 20

    ROAD = 0
    HOUSE = 1
    FENCE = 2
    GOAL = 3

    def __init__(self, grid: Grid, view):
        super().__init__(grid, view)
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.player_path = []
        self.optimal_path = []
        self.hint = None
        self.hint_was_used = False

    def setup(self, data=None) -> None:
        self.start_x = 0
        self.start_y = self.grid.height - 1
        self.end_x = self.grid.width - 1
        self.end_y = 0

        for y in range(self.grid.height):
            for x in range(self.grid.width):
                self.grid.set_cell(x, y, self.ROAD)

        self.grid.set_cell(self.end_x, self.end_y, self.GOAL)

        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if (x, y) == (self.start_x, self.start_y):
                    continue
                if (x, y) == (self.end_x, self.end_y):
                    continue
                if random.random() < self.OBSTACLE_CHANCE:
                    if random.random() < 0.5:
                        self.grid.set_cell(x, y, self.HOUSE)
                    else:
                        self.grid.set_cell(x, y, self.FENCE)

        self._make_sure_path_exists()

        self.optimal_path = AStarSolver.find_path(
            self.grid, self.start_x, self.start_y, self.end_x, self.end_y
        )
        self.player_path = [(self.start_x, self.start_y)]
        self._score = 0
        self._finished = False
        self._score_added_to_player = False
        self.hint = None
        self.hint_was_used = False

    def _make_sure_path_exists(self):
        path = AStarSolver.find_path(
            self.grid, self.start_x, self.start_y, self.end_x, self.end_y
        )
        if path:
            return

        obstacle_cells = []
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell_value = self.grid.get_cell(x, y)
                if cell_value == self.HOUSE or cell_value == self.FENCE:
                    obstacle_cells.append((x, y))

        while not path and obstacle_cells:
            random_x, random_y = random.choice(obstacle_cells)
            self.grid.set_cell(random_x, random_y, self.ROAD)
            obstacle_cells.remove((random_x, random_y))
            path = AStarSolver.find_path(
                self.grid, self.start_x, self.start_y, self.end_x, self.end_y
            )

    def _cell_is_walkable(self, x, y):
        cell_value = self.grid.get_cell(x, y)
        if cell_value is None:
            return False
        if cell_value == self.HOUSE or cell_value == self.FENCE:
            return False
        return True

    def _cells_are_neighbors(self, first_x, first_y, second_x, second_y):
        distance_x = abs(first_x - second_x)
        distance_y = abs(first_y - second_y)
        return distance_x + distance_y == 1

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

        player_route_length = len(self.player_path) - 1
        optimal_route_length = len(self.optimal_path) - 1
        if optimal_route_length == 0 or player_route_length == 0:
            return 0

        base_score = (optimal_route_length / player_route_length) * self.SCORE_MULTIPLIER
        final_score = int(base_score)

        if player_route_length == optimal_route_length:
            final_score += self.PERFECT_ROUTE_BONUS

        return final_score

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
        return "Доставщик"

    @property
    def progress_text(self) -> str:
        player_steps = 0
        if len(self.player_path) > 0:
            player_steps = len(self.player_path) - 1
        optimal_steps = len(self.optimal_path) - 1
        return f"Шагов: {player_steps} / лучших {optimal_steps}"
