class DijkstraSolver:

    @staticmethod
    def _cell_is_blocked(grid, x, y):
        cell_value = grid.get_cell(x, y)
        if cell_value is None:
            return True
        if cell_value == 1:
            return True
        return False

    @staticmethod
    def _cell_entry_cost(grid, x, y):
        cell_value = grid.get_cell(x, y)
        if cell_value == 2:
            return 2
        return 1

    @staticmethod
    def _pick_smallest_cost(open_list):
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
        cost_so_far = {(start_x, start_y): 0}

        while open_list:
            current_cost, current_x, current_y = DijkstraSolver._pick_smallest_cost(open_list)

            if current_x == end_x and current_y == end_y:
                return DijkstraSolver._build_path(came_from, start_x, start_y, end_x, end_y)

            for next_x, next_y in grid.get_neighbors(current_x, current_y):
                if DijkstraSolver._cell_is_blocked(grid, next_x, next_y):
                    continue

                entry_cost = DijkstraSolver._cell_entry_cost(grid, next_x, next_y)
                new_cost = cost_so_far[(current_x, current_y)] + entry_cost

                if (next_x, next_y) not in cost_so_far or new_cost < cost_so_far[(next_x, next_y)]:
                    cost_so_far[(next_x, next_y)] = new_cost
                    open_list.append((new_cost, next_x, next_y))
                    came_from[(next_x, next_y)] = (current_x, current_y)

        return []
