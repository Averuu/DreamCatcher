from src.models.mini_game_grid import Grid
from src.algorithms.astar import AStarSolver

HOUSE = 1
FENCE = 2


class TestAStarSolver:

    def test_empty_grid_path_found(self):
        grid = Grid(10, 10)
        path = AStarSolver.find_path(grid, 0, 9, 9, 0)
        assert len(path) > 0
        assert path[-1] == (9, 0)

    def test_start_equals_end(self):
        grid = Grid(5, 5)
        path = AStarSolver.find_path(grid, 3, 3, 3, 3)
        assert path == [(3, 3)]

    def test_no_path_when_blocked(self):
        grid = Grid(3, 3)
        grid.set_cell(0, 1, HOUSE)
        grid.set_cell(1, 0, FENCE)
        grid.set_cell(1, 1, HOUSE)
        grid.set_cell(1, 2, FENCE)
        grid.set_cell(2, 1, HOUSE)
        path = AStarSolver.find_path(grid, 0, 0, 2, 2)
        assert path == []

    def test_avoids_obstacles(self):
        grid = Grid(5, 5)
        for x in range(5):
            grid.set_cell(x, 2, HOUSE)
        path = AStarSolver.find_path(grid, 0, 4, 4, 0)
        for cell_x, cell_y in path:
            assert cell_y != 2

    def test_finds_path_around_obstacle_row(self):
        grid = Grid(5, 5)
        for x in range(3):
            grid.set_cell(x, 2, FENCE)
        path = AStarSolver.find_path(grid, 0, 4, 4, 0)
        assert len(path) > 0
        assert path[-1] == (4, 0)
        for cell_x, cell_y in path:
            assert not (cell_x < 3 and cell_y == 2)
