# 67
class Grid:
    def __init__(self, width, height, default=0):
        self.width = width
        self.height = height
        self.data = [[default for i in range(width)]
                     for j in range(height)]
        
        def get_cell(self, x, y):
            if x >= 0 and x <= self.width:
                if y >= 0 and y <= self.height:
                    return self.data[y][x]
            return None
    
        def set_cell(self, x, y, val):
            if self.get_cell(x, y):
                self.data[y][x] = val
        
        def get_neighbors(self, x, y):
            """Возвращает коорды клеток, которые находятся 
               вплотную к указанной"""
            neighbors = []

            # Это как если представить grid как координатную плоскость, 
            # а координаты - как векторы. Складываем векторы
            for ix, iy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                cell = self.get_cell(x + ix, y + iy)
                if cell:
                    neighbors.append((x + ix, y + iy))
            return neighbors