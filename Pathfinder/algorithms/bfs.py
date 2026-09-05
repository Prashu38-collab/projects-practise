"""
Breadth-First Search (BFS) Algorithm
Level-by-level unweighted search algorithm.
"""

from collections import deque
from grid import NodeState

def solve_bfs(grid, allow_diagonals=False):
    start = grid.start_node
    end = grid.end_node
    
    if not start or not end:
        return

    queue = deque([start])
    visited = {start}
    start.g_score = 0

    visited_count = 0

    while queue:
        current = queue.popleft()
        
        if current != start and current != end:
            current.state = NodeState.VISITED
            visited_count += 1
            yield {"type": "visit", "node": current, "visited_count": visited_count}

        if current == end:
            # Path found, reconstruct path
            path = []
            curr = end.parent
            path_cost = 0
            while curr and curr != start:
                path.append(curr)
                curr.state = NodeState.PATH
                path_cost += curr.weight
                yield {"type": "path", "node": curr, "visited_count": visited_count, "path_length": len(path) + 1, "path_cost": path_cost}
                curr = curr.parent

            # Final summary yield
            yield {
                "type": "complete",
                "found": True,
                "visited_count": visited_count,
                "path_length": len(path) + 1,
                "path_cost": path_cost + start.weight
            }
            return

        for neighbor, weight_cost in grid.get_neighbors(current, allow_diagonals=allow_diagonals):
            if neighbor not in visited:
                visited.add(neighbor)
                neighbor.parent = current
                neighbor.g_score = current.g_score + weight_cost
                if neighbor != end:
                    neighbor.state = NodeState.VISITING
                queue.append(neighbor)

    # If queue becomes empty without finding target
    yield {"type": "complete", "found": False, "visited_count": visited_count, "path_length": 0, "path_cost": 0}
