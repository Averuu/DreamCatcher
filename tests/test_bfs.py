from src.models.mini_game_grid import Grid
from src.algorithms.bfs_matcher import BFSMatcher

WEED = 1


class TestBFSMatcher:

    def test_finds_connected_area(self):
        grid = Grid(4, 4)
        grid.set_cell(1, 1, WEED)
        grid.set_cell(1, 2, WEED)
        grid.set_cell(2, 1, WEED)
        grid.set_cell(2, 2, WEED)
        area = BFSMatcher.find_connected(grid, 1, 1, WEED)
        assert len(area) == 4
        assert (1, 1) in area
        assert (2, 2) in area

    def test_single_cell_returns_itself(self):
        grid = Grid(5, 5)
        grid.set_cell(3, 3, WEED)
        area = BFSMatcher.find_connected(grid, 3, 3, WEED)
        assert area == [(3, 3)]

    def test_no_match_returns_empty(self):
        grid = Grid(5, 5)
        grid.set_cell(0, 0, WEED)
        area = BFSMatcher.find_connected(grid, 1, 1, WEED)
        assert area == []

    def test_separated_groups_not_connected(self):
        grid = Grid(5, 5)
        grid.set_cell(0, 0, WEED)
        grid.set_cell(0, 1, WEED)
        grid.set_cell(4, 4, WEED)
        area = BFSMatcher.find_connected(grid, 0, 0, WEED)
        assert len(area) == 2
        assert (4, 4) not in area

    def test_diagonal_neighbors_not_connected(self):
        grid = Grid(3, 3)
        grid.set_cell(0, 0, WEED)
        grid.set_cell(1, 1, WEED)
        area = BFSMatcher.find_connected(grid, 0, 0, WEED)
        assert area == [(0, 0)]
