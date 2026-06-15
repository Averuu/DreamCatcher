class AStarSolver:

    @staticmethod
    def _manhattan_distance(from_x, from_y, to_x, to_y):
        return abs(from_x - to_x) + abs(from_y - to_y)

    @staticmethod
    def _cell_is_blocked(grid, x, y):
        cell_value = grid.get_cell(x, y)
        if cell_value is None:
            return True
        if cell_value == 1 or cell_value == 2:
            return True
        return False

    @staticmethod
    def _pick_smallest_priority(open_list):
        best_index = 0
        for index in range(1, len(open_list)):
            if open_list[index][0] < open_list[best_index][0]:
                best_index = index
        return open_list.pop(best_index)

    @staticmethod
    def _build_path(came_from, start_x, start_y, end_x, end_y):
        path = []
        current_x = end_x
        current_y = end_y
        while (current_x, current_y) != (start_x, start_y):
            path.append((current_x, current_y))
            current_x, current_y = came_from[(current_x, current_y)]
        path.append((start_x, start_y))
        path.reverse()
        return path

    @staticmethod
    def find_path(grid, start_x, start_y, end_x, end_y):
        open_list = [(0, start_x, start_y)]
        came_from = {}
        path_cost = {(start_x, start_y): 0}

        while open_list:
            cost, current_x, current_y = AStarSolver._pick_smallest_priority(open_list)

            if current_x == end_x and current_y == end_y:
                return AStarSolver._build_path(came_from, start_x, start_y, end_x, end_y)

            for next_x, next_y in grid.get_neighbors(current_x, current_y):
                if AStarSolver._cell_is_blocked(grid, next_x, next_y):
                    continue

                new_cost = path_cost[(current_x, current_y)] + 1
                if (next_x, next_y) not in path_cost or new_cost < path_cost[(next_x, next_y)]:
                    path_cost[(next_x, next_y)] = new_cost
                    priority = new_cost + AStarSolver._manhattan_distance(
                        next_x, next_y, end_x, end_y
                    )
                    open_list.append((priority, next_x, next_y))
                    came_from[(next_x, next_y)] = (current_x, current_y)

        return []
