"""
Depth-First Search (DFS) Algorithm
Deep exploration unweighted search algorithm using a stack.
"""

from grid import NodeState

def solve_dfs(grid, allow_diagonals=False):
    start = grid.start_node
    end = grid.end_node
    
    if not start or not end:
        return

    stack = [start]
    visited = {start}
    start.g_score = 0
    visited_count = 0

    while stack:
        current = stack.pop()
        
        if current != start and current != end:
            current.state = NodeState.VISITED
            visited_count += 1
            yield {"type": "visit", "node": current, "visited_count": visited_count}

        if current == end:
            # Path found!
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

        # Reversed order so left/up branches explored logically
        neighbors = grid.get_neighbors(current, allow_diagonals=allow_diagonals)
        for neighbor, weight_cost in reversed(neighbors):
            if neighbor not in visited:
                visited.add(neighbor)
                neighbor.parent = current
                neighbor.g_score = current.g_score + weight_cost
                if neighbor != end:
                    neighbor.state = NodeState.VISITING
                stack.append(neighbor)

    yield {"type": "complete", "found": False, "visited_count": visited_count, "path_length": 0, "path_cost": 0}
