"""
Dijkstra's Algorithm
Guaranteed weighted shortest path algorithm using a min-priority queue.
"""

import heapq
from grid import NodeState

def solve_dijkstra(grid, allow_diagonals=False):
    start = grid.start_node
    end = grid.end_node
    
    if not start or not end:
        return

    # Counter to break tie in priority queue tuple (g_score, count, node)
    count = 0
    start.g_score = 0
    pq = [(0, count, start)]
    visited = set()
    visited_count = 0

    while pq:
        current_g, _, current = heapq.heappop(pq)

        if current in visited:
            continue
            
        visited.add(current)

        if current != start and current != end:
            current.state = NodeState.VISITED
            visited_count += 1
            yield {"type": "visit", "node": current, "visited_count": visited_count}

        if current == end:
            # Shortest path found
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
                neighbor.parent = current
                count += 1
                if neighbor != end and neighbor not in visited:
                    neighbor.state = NodeState.VISITING
                heapq.heappush(pq, (new_g, count, neighbor))

    yield {"type": "complete", "found": False, "visited_count": visited_count, "path_length": 0, "path_cost": 0}
