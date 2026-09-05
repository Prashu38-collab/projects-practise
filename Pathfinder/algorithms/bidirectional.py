"""
Bidirectional BFS Algorithm
Dual-frontier search algorithm operating simultaneously from Start and End nodes.
"""

from collections import deque
from grid import NodeState

def solve_bidirectional(grid, allow_diagonals=False):
    start = grid.start_node
    end = grid.end_node
    
    if not start or not end:
        return

    # Forward queue from Start
    queue_s = deque([start])
    visited_s = {start: None} # node -> parent_from_start
    start.g_score = 0

    # Backward queue from End
    queue_e = deque([end])
    visited_e = {end: None}   # node -> parent_from_end

    intersect_node = None
    visited_count = 0

    while queue_s and queue_e:
        # Step 1: Expand forward frontier from Start
        if queue_s:
            curr_s = queue_s.popleft()

            if curr_s != start and curr_s != end:
                curr_s.state = NodeState.VISITED
                visited_count += 1
                yield {"type": "visit", "node": curr_s, "visited_count": visited_count}

            # Check if forward frontier intersects backward frontier
            if curr_s in visited_e:
                intersect_node = curr_s
                break

            for neighbor, weight_cost in grid.get_neighbors(curr_s, allow_diagonals=allow_diagonals):
                if neighbor not in visited_s:
                    visited_s[neighbor] = curr_s
                    neighbor.g_score = curr_s.g_score + weight_cost
                    if neighbor != end and neighbor != start:
                        neighbor.state = NodeState.VISITING
                    queue_s.append(neighbor)

        # Step 2: Expand backward frontier from End
        if queue_e:
            curr_e = queue_e.popleft()

            if curr_e != start and curr_e != end:
                curr_e.state = NodeState.VISITED_B
                visited_count += 1
                yield {"type": "visit", "node": curr_e, "visited_count": visited_count}

            # Check if backward frontier intersects forward frontier
            if curr_e in visited_s:
                intersect_node = curr_e
                break

            for neighbor, weight_cost in grid.get_neighbors(curr_e, allow_diagonals=allow_diagonals):
                if neighbor not in visited_e:
                    visited_e[neighbor] = curr_e
                    if neighbor != start and neighbor != end:
                        neighbor.state = NodeState.VISITED_B
                    queue_e.append(neighbor)

    if intersect_node:
        # Path found! Construct path from Start to Intersect, and Intersect to End
        path_s = []
        curr = intersect_node
        while curr and curr != start:
            path_s.append(curr)
            curr = visited_s.get(curr)

        path_e = []
        curr = visited_e.get(intersect_node)
        while curr and curr != end:
            path_e.append(curr)
            curr = visited_e.get(curr)

        full_path = path_s[::-1] + path_e
        path_cost = 0
        path_len = 0

        for node in full_path:
            if node != start and node != end:
                node.state = NodeState.PATH
                path_cost += node.weight
                path_len += 1
                yield {"type": "path", "node": node, "visited_count": visited_count, "path_length": path_len, "path_cost": path_cost}

        yield {
            "type": "complete",
            "found": True,
            "visited_count": visited_count,
            "path_length": len(full_path) + 1,
            "path_cost": path_cost + start.weight
        }
        return

    yield {"type": "complete", "found": False, "visited_count": visited_count, "path_length": 0, "path_cost": 0}
