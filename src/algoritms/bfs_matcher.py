class BFSMatcher:
    @staticmethod
    def find_connected(grid, x, y, val):
        if grid.get_cell(x, y) != val:
            return []
        
        width = grid.width
        height = grid.height

        visited = [[False] * width for i in height]

        queue = [(x, y)]  # начальная точка
        head = 0
        visited[y][x] = True
        result = []

        while head < len(queue):
            new_x = queue[head][0]
            new_y = queue[head][1]

            head += 1

            for neigh_x, neigh_y in grid.get_neighbors(new_x, new_y):
                if not visited[neigh_y][neigh_x]:
                    if grid.get_cell(neigh_x, neigh_y) == val:
                        visited[neigh_y][neigh_x] = True
                        queue.append((neigh_x, neigh_y))
        return result