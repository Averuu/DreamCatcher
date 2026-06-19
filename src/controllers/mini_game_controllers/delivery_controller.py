import pygame
from .base_mini_game import BaseMiniGameController
from src.models.delivery_game import DeliveryGame
from src.models.mini_game_grid import Grid


class DeliveryController(BaseMiniGameController):

    def __init__(self, view):
        super().__init__(view)
        self.model = DeliveryGame()
        self.view.sync_grid(self.model.grid)

    def setup(self, data=None) -> None:
        self.model = DeliveryGame()
        self.model.setup()
        self.view.sync_grid(self.model.grid)
        self._score_added_to_player = False

    def handle_event(self, event) -> None:
        if self.model.finished:
            return
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        mouse_x, mouse_y = event.pos
        clicked_x, clicked_y = self.view.get_cell_from_mouse(mouse_x, mouse_y)
        if clicked_x is None or clicked_y is None:
            return

        self.model.handle_move(clicked_x, clicked_y)

    def update(self, delta_time: float) -> None:
        pass

    def get_hint(self):
        return self.model.get_hint_path()

    def is_finished(self):
        return self.model.finished

    def get_score(self):
        return self.model.score

    @property
    def game_title(self) -> str:
        return "Доставщик"

    @property
    def progress_text(self) -> str:
        return self.model.progress_text

    @property
    def player_path(self):
        return self.model.player_path

    @property
    def hint(self):
        return self.model.hint

    @property
    def hint_was_used(self):
        return self.model.hint_was_used
