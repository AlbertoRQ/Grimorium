import heapq


def find_path(room, start, goal):
    if not room.is_walkable_cell(*start):
        return []

    if not room.is_walkable_cell(*goal):
        return []

    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    cost_so_far = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            break

        for neighbor in get_neighbors(room, current):
            new_cost = cost_so_far[current] + 1

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(open_set, (priority, neighbor))
                came_from[neighbor] = current

    if goal not in came_from and goal != start:
        return []

    return reconstruct_path(came_from, start, goal)


def get_neighbors(room, cell):
    row, col = cell

    candidates = [
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1),
    ]

    return [
        candidate
        for candidate in candidates
        if room.is_walkable_cell(*candidate)
    ]


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]

    while current != start:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path