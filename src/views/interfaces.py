"""
Интерфейс для представлений мини-игр.
"""
from abc import ABC, abstractmethod

class IGameView(ABC):
    @abstractmethod
    def get_cell_from_mouse(self, mouse_x: int, mouse_y: int) -> tuple:
        """Преобразует экранные координаты мыши в индексы клетки (x, y) или (None, None)."""
        pass

    @abstractmethod
    def render(self, screen, offset_x: int, offset_y: int, hint=None) -> None:
        """Отрисовывает игровое поле."""
        pass