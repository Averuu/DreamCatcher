import pygame
from .base_mini_game import BaseMiniGameController
from src.models.gardener_game import GardenerGame
from src.models.mini_game_grid import Grid


class GardenerController(BaseMiniGameController):

    def __init__(self, view):
        super().__init__(view)
        self.model = GardenerGame()
        self.view.sync_grid(self.model.grid)

    def setup(self, data=None) -> None:
        self.model = GardenerGame()
        self.model.setup()
        self.view.sync_grid(self.model.grid)
        self._score_added_to_player = False

    def handle_event(self, event) -> None:
        if self.model.finished:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            grid_x, grid_y = self.view.get_cell_from_mouse(mouse_x, mouse_y)
            if grid_x is None or grid_y is None:
                return
            self.model.handle_clear(grid_x, grid_y)

    def update(self, delta_time: float) -> None:
        pass

    def get_hint(self):
        if self.model.finished:
            return []
        area = self.model.get_hint_area()
        return area

    def is_finished(self):
        return self.model.finished

    def get_score(self):
        return self.model.score

    @property
    def game_title(self) -> str:
        return "Садовник"

    @property
    def progress_text(self) -> str:
        return self.model.progress_text

    @property
    def hint(self):
        return self.model.hint
