"""
Greedy Best-First Search Algorithm
Fast heuristic-only search algorithm.
"""

import heapq
from grid import NodeState
from algorithms.astar import heuristic

def solve_greedy(grid, allow_diagonals=False):
    start = grid.start_node
    end = grid.end_node
    
    if not start or not end:
        return

    count = 0
    start.h_score = heuristic(start, end, allow_diagonals)
    start.g_score = 0
    
    # Priority queue sorted strictly by heuristic distance h(n)
    pq = [(start.h_score, count, start)]
    visited = {start}
    visited_count = 0

    while pq:
        _, _, current = heapq.heappop(pq)

        if current != start and current != end:
            current.state = NodeState.VISITED
            visited_count += 1
            yield {"type": "visit", "node": current, "visited_count": visited_count}

        if current == end:
            # Reconstruct path
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
                "path_cost": path_cost + start.weight
            }
            return

        for neighbor, move_cost in grid.get_neighbors(current, allow_diagonals=allow_diagonals):
            if neighbor not in visited:
                visited.add(neighbor)
                neighbor.parent = current
                neighbor.g_score = current.g_score + move_cost
                neighbor.h_score = heuristic(neighbor, end, allow_diagonals)
                count += 1
                if neighbor != end:
                    neighbor.state = NodeState.VISITING
                heapq.heappush(pq, (neighbor.h_score, count, neighbor))

    yield {"type": "complete", "found": False, "visited_count": visited_count, "path_length": 0, "path_cost": 0}
