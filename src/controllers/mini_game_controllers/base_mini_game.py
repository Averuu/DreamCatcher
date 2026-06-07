"""
Абстрактный базовый контроллер для всех мини-игр.
"""
from abc import ABC, abstractmethod
from src.views.interfaces import IGameView

class BaseMiniGameController(ABC):
    def __init__(self, grid, view: IGameView):
        self.grid = grid
        self.view = view          # зависит от абстракции
        self._score = 0
        self._finished = False
        self._score_added_to_player = False   # флаг для предотвращения двойного начисления

    @abstractmethod
    def setup(self, data=None) -> None:
        """Подготовка игры (генерация поля и т.п.)."""
        pass

    @abstractmethod
    def handle_event(self, event) -> None:
        """Обработка событий Pygame."""
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """Обновление состояния (таймеры, анимации)."""
        pass

    @abstractmethod
    def get_hint(self):
        """Возвращает подсказку (координаты, список задач и т.д.)."""
        pass

    def get_score(self) -> int:
        return self._score

    def is_finished(self) -> bool:
        return self._finished

    def was_score_added(self) -> bool:
        return self._score_added_to_player

    def mark_score_added(self) -> None:
        self._score_added_to_player = True