"""
Класс сетки для мини-игр: хранение данных, доступ к ячейкам, подсчёт.
"""
class Grid:
    def __init__(self, width: int, height: int, default_value=0):
        self._width = width
        self._height = height
        self._data = [[default_value for _ in range(width)] for _ in range(height)]

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def get_cell(self, x: int, y: int):
        """Возвращает значение клетки или None, если координаты вне границ."""
        if 0 <= x < self._width and 0 <= y < self._height:
            return self._data[y][x]
        return None

    def set_cell(self, x: int, y: int, value) -> None:
        """Устанавливает значение клетки, если координаты корректны."""
        if 0 <= x < self._width and 0 <= y < self._height:
            self._data[y][x] = value

    def get_neighbors(self, x: int, y: int) -> list:
        """Возвращает список координат соседей (4-связность)."""
        neighbors = []
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if self.get_cell(nx, ny) is not None:
                neighbors.append((nx, ny))
        return neighbors

    def count_cells(self, value) -> int:
        """Подсчитывает количество клеток с заданным значением."""
        count = 0
        for row in self._data:
            for cell in row:
                if cell == value:
                    count += 1
        return count