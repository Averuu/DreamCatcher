from abc import ABC
from abc import abstractmethod

class BaseMiniGameController(ABC):
    def __init__(self, grid, view):
        self.grid = grid
        self.view = view
        self.score = 0
        self.finished = False
    
    @abstractmethod
    def setup(self, data=None):
        pass
    
    @abstractmethod
    def handle_event(self, event):
        pass
    
    @abstractmethod
    def update(self, val):
        pass
    
    def get_score(self):
        return self.score
    
    def is_finished(self):
        return self.finished
    
    @abstractmethod
    def get_hint(self):
        pass
