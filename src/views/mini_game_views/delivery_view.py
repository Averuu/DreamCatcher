import pygame
from src.views.interfaces import IGameView


class DeliveryView(IGameView):

    COLOR_ROAD = (190, 190, 190)
    COLOR_HOUSE = (178, 34, 34)
    COLOR_FENCE = (105, 105, 105)
    COLOR_GOAL = (255, 215, 0)
    COLOR_PATH = (100, 149, 237)
    COLOR_HINT = (255, 255, 0)
    COLOR_COURIER = (30, 144, 255)

    def __init__(self, cell_size=40):
        self.grid = None
        self.cell_size = cell_size

    def sync_grid(self, grid):
        self.grid = grid
        self._offset_x = 0
        self._offset_y = 0

    def set_offset(self, offset_x, offset_y):
        self._offset_x = offset_x
        self._offset_y = offset_y

    def get_cell_from_mouse(self, mouse_x, mouse_y):
        local_x = mouse_x - self._offset_x
        local_y = mouse_y - self._offset_y
        if local_x < 0 or local_y < 0:
            return (None, None)
        grid_x = local_x // self.cell_size
        grid_y = local_y // self.cell_size
        if 0 <= grid_x < self.grid.width and 0 <= grid_y < self.grid.height:
            return (grid_x, grid_y)
        return (None, None)

    def _make_cell_rect(self, grid_x, grid_y):
        return pygame.Rect(
            self._offset_x + grid_x * self.cell_size,
            self._offset_y + grid_y * self.cell_size,
            self.cell_size,
            self.cell_size
        )

    def _pick_cell_color(self, cell_value):
        if cell_value == 1:
            return self.COLOR_HOUSE
        if cell_value == 2:
            return self.COLOR_FENCE
        if cell_value == 3:
            return self.COLOR_GOAL
        return self.COLOR_ROAD

    def render(self, screen, offset_x=0, offset_y=0, hint=None, player_path=None):
        if player_path is None:
            player_path = []

        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell_rect = self._make_cell_rect(x, y)
                cell_color = self._pick_cell_color(self.grid.get_cell(x, y))
                pygame.draw.rect(screen, cell_color, cell_rect)
                pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)

        for path_x, path_y in player_path:
            path_rect = self._make_cell_rect(path_x, path_y)
            path_overlay = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
            path_overlay.fill((100, 149, 237, 90))
            screen.blit(path_overlay, path_rect)

        if hint:
            for hint_x, hint_y in hint:
                hint_rect = self._make_cell_rect(hint_x, hint_y)
                hint_overlay = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                hint_overlay.fill((255, 255, 0, 128))
                screen.blit(hint_overlay, hint_rect)
                pygame.draw.rect(screen, self.COLOR_HINT, hint_rect, 3)

        if player_path:
            courier_x, courier_y = player_path[-1]
            courier_rect = self._make_cell_rect(courier_x, courier_y)
            inner_size = self.cell_size // 2
            inner_x = courier_rect.x + (self.cell_size - inner_size) // 2
            inner_y = courier_rect.y + (self.cell_size - inner_size) // 2
            pygame.draw.rect(
                screen,
                self.COLOR_COURIER,
                pygame.Rect(inner_x, inner_y, inner_size, inner_size)
            )
