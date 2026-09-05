"""
A* Search Algorithm
Informed heuristic-driven weighted shortest path algorithm.
"""

import heapq
import math
from grid import NodeState

def heuristic(node1, node2, allow_diagonals=False):
    dx = abs(node1.row - node2.row)
    dy = abs(node1.col - node2.col)
    
    if allow_diagonals:
        # Octile distance for 8-directional grid
        D = 1.0
        D2 = math.sqrt(2)
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
    else:
        # Manhattan distance for 4-directional grid
        return dx + dy

def solve_astar(grid, allow_diagonals=False):
    start = grid.start_node
    end = grid.end_node
    
    if not start or not end:
        return

    count = 0
    start.g_score = 0
    start.h_score = heuristic(start, end, allow_diagonals)
    start.f_score = start.g_score + start.h_score

    # Priority queue: (f_score, h_score, count, node)
    pq = [(start.f_score, start.h_score, count, start)]
    visited = set()
    visited_count = 0

    while pq:
        current_f, _, _, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)

        if current != start and current != end:
            current.state = NodeState.VISITED
            visited_count += 1
            yield {"type": "visit", "node": current, "visited_count": visited_count}

        if current == end:
            # Reconstruct shortest path
            path = []
            curr = end.parent
            path_cost = 0
            while curr and curr != start:
                path.append(curr)
                curr.state = NodeState.PATH
                path_cost += curr.weight
                yield {"type": "path", "node": curr, "visited_count": visited_count, "path_length": len(path) + 1, "path_cost": path_cost}
                curr = curr.parent

            yield {
                "type": "complete",
                "found": True,
                "visited_count": visited_count,
                "path_length": len(path) + 1,
                "path_cost": end.g_score
            }
            return

        for neighbor, move_cost in grid.get_neighbors(current, allow_diagonals=allow_diagonals):
            new_g = current.g_score + move_cost
            if new_g < neighbor.g_score:
                neighbor.g_score = new_g
                neighbor.h_score = heuristic(neighbor, end, allow_diagonals)
                neighbor.f_score = new_g + neighbor.h_score
                neighbor.parent = current
                count += 1
                if neighbor != end and neighbor not in visited:
                    neighbor.state = NodeState.VISITING
                heapq.heappush(pq, (neighbor.f_score, neighbor.h_score, count, neighbor))

    yield {"type": "complete", "found": False, "visited_count": visited_count, "path_length": 0, "path_cost": 0}
