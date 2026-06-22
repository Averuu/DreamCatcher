import pygame
from src.views.interfaces import IGameView

class GardenerView(IGameView):
    COLOR_GROUND = (139, 69, 19)
    COLOR_WEED = (50, 210, 50)
    COLOR_HINT = (255, 255, 0)

    def __init__(self, cell_size=40):
        self.grid = None
        self.cell_size = cell_size

    def sync_grid(self, grid):
        self.grid = grid
        self._offset_x = 0
        self._offset_y = 0

    def set_offset(self, ox, oy):
        self._offset_x = ox
        self._offset_y = oy

    def get_cell_from_mouse(self, mouse_x: int, mouse_y: int) -> tuple:
        local_x = mouse_x - self._offset_x
        local_y = mouse_y - self._offset_y
        if local_x < 0 or local_y < 0:
            return (None, None)
        gx = local_x // self.cell_size
        gy = local_y // self.cell_size
        if 0 <= gx < self.grid.width and 0 <= gy < self.grid.height:
            return (gx, gy)
        return (None, None)

    def render(self, screen, offset_x=0, offset_y=0, hint=None) -> None:
        ox, oy = self._offset_x, self._offset_y
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                rect = pygame.Rect(
                    ox + x * self.cell_size,
                    oy + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                if self.grid.get_cell(x, y) == 1:
                    color = self.COLOR_WEED
                else:
                    color = self.COLOR_GROUND
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

        if hint:
            for hx, hy in hint:
                rect = pygame.Rect(
                    ox + hx * self.cell_size,
                    oy + hy * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                overlay = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                overlay.fill((255, 255, 0, 128))
                screen.blit(overlay, rect)
                pygame.draw.rect(screen, self.COLOR_HINT, rect, 3)