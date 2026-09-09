from typing import List, Dict, Set, Tuple, Optional
from collections import deque, defaultdict
from backend.app.models.roadmap import Topic, TopicRelationship


class LearningGraph:
    """
    Graph engine for analyzing learning paths.
    Supports BFS, DFS, shortest path, divergence detection, and rabbit hole classification.
    """
    
    def __init__(self, topics: List[Topic], relationships: List[TopicRelationship]):
        self.topics = {topic.id: topic for topic in topics}
        self.topic_names = {topic.id: topic.title for topic in topics}
        self.name_to_id = {topic.title.lower(): topic.id for topic in topics}
        
        # Build adjacency list
        self.adjacency: Dict[int, List[int]] = defaultdict(list)
        self.prerequisites: Dict[int, List[int]] = defaultdict(list)
        
        for rel in relationships:
            self.adjacency[rel.from_topic_id].append(rel.to_topic_id)
            if rel.relationship_type == "prerequisite":
                self.prerequisites[rel.to_topic_id].append(rel.from_topic_id)
    
    def get_topic_id_by_name(self, name: str) -> Optional[int]:
        """Get topic ID by name (case-insensitive)."""
        return self.name_to_id.get(name.lower())
    
    def get_topic_name(self, topic_id: int) -> str:
        """Get topic name by ID."""
        return self.topic_names.get(topic_id, f"Unknown Topic ({topic_id})")
    
    def bfs(self, start_id: int) -> List[int]:
        """Breadth-first search from start node."""
        visited = set()
        queue = deque([start_id])
        result = []
        
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                result.append(node)
                for neighbor in self.adjacency.get(node, []):
                    if neighbor not in visited:
                        queue.append(neighbor)
        
        return result
    
    def dfs(self, start_id: int) -> List[int]:
        """Depth-first search from start node."""
        visited = set()
        result = []
        
        def _dfs(node):
            if node not in visited:
                visited.add(node)
                result.append(node)
                for neighbor in self.adjacency.get(node, []):
                    _dfs(neighbor)
        
        _dfs(start_id)
        return result
    
    def shortest_path(self, start_id: int, end_id: int) -> Optional[List[int]]:
        """Find shortest path between two nodes using BFS."""
        if start_id == end_id:
            return [start_id]
        
        visited = {start_id}
        queue = deque([(start_id, [start_id])])
        
        while queue:
            node, path = queue.popleft()
            for neighbor in self.adjacency.get(node, []):
                if neighbor == end_id:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def get_all_paths(self, start_id: int, end_id: int, max_depth: int = 10) -> List[List[int]]:
        """Find all paths between two nodes (up to max_depth)."""
        all_paths = []
        
        def _dfs_paths(node, path, visited):
            if len(path) > max_depth:
                return
            if node == end_id:
                all_paths.append(path[:])
                return
            
            for neighbor in self.adjacency.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    _dfs_paths(neighbor, path, visited)
                    path.pop()
                    visited.remove(neighbor)
        
        _dfs_paths(start_id, [start_id], {start_id})
        return all_paths
    
    def get_prerequisites(self, topic_id: int) -> List[int]:
        """Get all prerequisites for a topic."""
        return self.prerequisites.get(topic_id, [])
    
    def get_dependents(self, topic_id: int) -> List[int]:
        """Get all topics that depend on this topic."""
        dependents = []
        for rel_from, rel_to_list in self.adjacency.items():
            if topic_id in rel_to_list:
                dependents.append(rel_from)
        return dependents
    
    def get_node_depth(self, start_id: int, target_id: int) -> Optional[int]:
        """Get depth of target node from start node."""
        if start_id == target_id:
            return 0
        
        visited = {start_id}
        queue = deque([(start_id, 0)])
        
        while queue:
            node, depth = queue.popleft()
            for neighbor in self.adjacency.get(node, []):
                if neighbor == target_id:
                    return depth + 1
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1))
        
        return None
    
    def find_divergence_point(self, planned_path: List[str], actual_path: List[str]) -> Optional[str]:
        """
        Find the point where actual path diverges from planned path.
        Returns the topic name where divergence occurs.
        """
        for i, (planned, actual) in enumerate(zip(planned_path, actual_path)):
            if planned.lower() != actual.lower():
                if i > 0:
                    return planned_path[i - 1]
                return None
        return None
    
    def find_rejoin_point(self, planned_path: List[str], actual_path: List[str], divergence_idx: int) -> Optional[str]:
        """
        Find where actual path rejoins planned path after divergence.
        Returns the topic name where rejoin occurs.
        """
        planned_remaining = set(p.lower() for p in planned_path[divergence_idx:])
        
        for actual_topic in actual_path:
            if actual_topic.lower() in planned_remaining:
                return actual_topic
        return None
    
    def find_common_path(self, path1: List[str], path2: List[str]) -> List[str]:
        """Find the common prefix of two paths."""
        common = []
        for p1, p2 in zip(path1, path2):
            if p1.lower() == p2.lower():
                common.append(p1)
            else:
                break
        return common
    
    def find_skipped_topics(self, planned_path: List[str], actual_path: List[str]) -> List[str]:
        """Find topics in planned path that were skipped in actual path."""
        actual_set = set(t.lower() for t in actual_path)
        return [t for t in planned_path if t.lower() not in actual_set]
    
    def find_extra_topics(self, planned_path: List[str], actual_path: List[str]) -> List[str]:
        """Find topics in actual path that are not in planned path."""
        planned_set = set(t.lower() for t in planned_path)
        return [t for t in actual_path if t.lower() not in planned_set]
    
    def classify_rabbit_hole(self, divergence_point: str, rejoin_point: Optional[str], 
                            topics_explored: List[str], planned_path: List[str]) -> str:
        """
        Classify a rabbit hole based on exploration behavior.
        
        Classifications:
        - ON_PATH: Followed planned path exactly
        - RELATED: Explored related topics
        - OPTIONAL: Explored optional/supplementary topics
        - OFF_PATH: Explored unrelated topics
        - DEEP_RABBIT_HOLE: Long exploration away from planned path
        """
        if not topics_explored:
            return "ON_PATH"
        
        # Check if any explored topics are in the roadmap
        roadmap_topics = set(t.lower() for t in planned_path)
        related_count = sum(1 for t in topics_explored if t.lower() in roadmap_topics)
        
        depth = len(topics_explored)
        
        # Classify based on relationship to planned path
        if related_count == depth:
            return "ON_PATH"
        elif related_count > depth * 0.5:
            return "RELATED"
        elif depth > 3:
            return "DEEP_RABBIT_HOLE"
        elif related_count > 0:
            return "OPTIONAL"
        else:
            return "OFF_PATH"
    
    def analyze_exploration(self, planned_path: List[str], actual_path: List[str]) -> Dict:
        """
        Complete analysis of actual vs planned exploration.
        Returns detailed comparison results.
        """
        if not planned_path or not actual_path:
            return {
                "planned_path": planned_path,
                "actual_path": actual_path,
                "common_path": [],
                "divergence_point": None,
                "rejoin_point": None,
                "rabbit_holes": [],
                "skipped_topics": [],
                "extra_topics": [],
            }
        
        # Find common path
        common_path = self.find_common_path(planned_path, actual_path)
        
        # Find divergence point
        divergence_point = None
        divergence_idx = 0
        if len(common_path) < len(planned_path) and len(common_path) < len(actual_path):
            divergence_point = common_path[-1] if common_path else None
            divergence_idx = len(common_path)
        
        # Find rejoin point
        rejoin_point = None
        rejoin_idx = -1
        if divergence_point:
            rejoin_point = self.find_rejoin_point(planned_path, actual_path, divergence_idx)
            if rejoin_point:
                rejoin_idx = actual_path.index(rejoin_point)
        
        # Extract rabbit holes (segments between divergence and rejoin)
        rabbit_holes = []
        if divergence_point and rejoin_point:
            rabbit_hole_topics = actual_path[divergence_idx:rejoin_idx]
            classification = self.classify_rabbit_hole(
                divergence_point, rejoin_point, rabbit_hole_topics, planned_path
            )
            rabbit_holes.append({
                "divergence_point": divergence_point,
                "rejoin_point": rejoin_point,
                "depth": len(rabbit_hole_topics),
                "classification": classification,
                "topics_explored": rabbit_hole_topics,
                "description": f"Explored {len(rabbit_hole_topics)} topics between {divergence_point} and {rejoin_point}",
            })
        elif divergence_point and not rejoin_point:
            rabbit_hole_topics = actual_path[divergence_idx:]
            classification = self.classify_rabbit_hole(
                divergence_point, None, rabbit_hole_topics, planned_path
            )
            rabbit_holes.append({
                "divergence_point": divergence_point,
                "rejoin_point": None,
                "depth": len(rabbit_hole_topics),
                "classification": classification,
                "topics_explored": rabbit_hole_topics,
                "description": f"Explored {len(rabbit_hole_topics)} topics starting from {divergence_point} without rejoining",
            })
        
        # Find skipped topics
        skipped_topics = self.find_skipped_topics(planned_path, actual_path)
        
        # Find extra topics
        extra_topics = self.find_extra_topics(planned_path, actual_path)
        
        return {
            "planned_path": planned_path,
            "actual_path": actual_path,
            "common_path": common_path,
            "divergence_point": divergence_point,
            "rejoin_point": rejoin_point,
            "rabbit_holes": rabbit_holes,
            "skipped_topics": skipped_topics,
            "extra_topics": extra_topics,
        }
