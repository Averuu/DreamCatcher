from src.models.mini_game_grid import Grid
from src.algorithms.dijkstra import DijkstraSolver

NORMAL = 0
WALL = 1
ROUGH = 2
GOAL = 3


class TestDijkstraSolver:

    def test_empty_grid_path_found(self):
        grid = Grid(10, 10)
        path = DijkstraSolver.find_path(grid, 0, 9, 9, 0)
        assert len(path) > 0
        assert path[0] == (0, 9)
        assert path[-1] == (9, 0)

    def test_start_equals_end(self):
        grid = Grid(5, 5)
        path = DijkstraSolver.find_path(grid, 2, 2, 2, 2)
        assert path == [(2, 2)]

    def test_no_path_when_blocked(self):
        grid = Grid(3, 3)
        grid.set_cell(0, 1, WALL)
        grid.set_cell(1, 0, WALL)
        grid.set_cell(1, 1, WALL)
        grid.set_cell(1, 2, WALL)
        grid.set_cell(2, 1, WALL)
        path = DijkstraSolver.find_path(grid, 0, 0, 2, 2)
        assert path == []

    def test_avoids_walls(self):
        grid = Grid(5, 5)
        for x in range(5):
            grid.set_cell(x, 2, WALL)
        path = DijkstraSolver.find_path(grid, 0, 4, 4, 0)
        for cell_x, cell_y in path:
            assert cell_y != 2

    def test_avoids_rough_when_possible(self):
        grid = Grid(3, 4)
        grid.set_cell(1, 1, ROUGH)
        grid.set_cell(2, 1, ROUGH)
        path = DijkstraSolver.find_path(grid, 0, 2, 3, 0)
        for step_x, step_y in path:
            assert step_x != 1 or step_y != 1
            assert step_x != 2 or step_y != 1

    def test_uses_rough_when_necessary(self):
        grid = Grid(3, 3)
        grid.set_cell(0, 0, WALL)
        grid.set_cell(1, 0, NORMAL)
        grid.set_cell(2, 0, GOAL)
        grid.set_cell(0, 1, NORMAL)
        grid.set_cell(1, 1, ROUGH)
        grid.set_cell(2, 1, WALL)
        grid.set_cell(0, 2, NORMAL)
        grid.set_cell(1, 2, WALL)
        grid.set_cell(2, 2, WALL)
        grid.set_cell(2, 0, GOAL)
        path = DijkstraSolver.find_path(grid, 0, 2, 2, 0)
        assert (1, 1) in path

    def test_cost_goes_through_rough_over_many_normal(self):
        grid = Grid(3, 5)
        grid.set_cell(0, 0, WALL)
        grid.set_cell(0, 1, WALL)
        grid.set_cell(0, 2, WALL)
        grid.set_cell(0, 3, WALL)
        grid.set_cell(2, 1, WALL)
        grid.set_cell(2, 2, WALL)
        grid.set_cell(2, 3, WALL)
        grid.set_cell(2, 4, WALL)
        grid.set_cell(1, 1, ROUGH)
        grid.set_cell(1, 2, ROUGH)
        grid.set_cell(1, 3, ROUGH)
        grid.set_cell(2, 0, GOAL)
        path = DijkstraSolver.find_path(grid, 0, 4, 2, 0)
        assert len(path) > 0
        assert (1, 1) in path
        assert (1, 2) in path

    def test_only_one_cell_away(self):
        grid = Grid(3, 3)
        grid.set_cell(0, 1, WALL)
        grid.set_cell(1, 1, WALL)
        grid.set_cell(2, 0, WALL)
        grid.set_cell(2, 1, WALL)
        path = DijkstraSolver.find_path(grid, 0, 0, 1, 0)
        assert path == [(0, 0), (1, 0)]
