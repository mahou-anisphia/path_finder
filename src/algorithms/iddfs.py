import time
import logging
from typing import List, Tuple, Dict, Set
from src.utils.pathfinding_utils import get_neighbors, reconstruct_path

logger = logging.getLogger(__name__)


class IDDFS:
    def __init__(self, environment: Dict):
        self.rows, self.cols = environment['dimensions']
        self.start = environment['start']
        self.goals = set(environment['goals'])
        self.walls = set((x, y) for x, y, w, h in environment['walls'] for dx in range(
            w) for dy in range(h))
        self.moves = []

    def dfs(self, node, depth, parent, callback):
        self.moves.append(node)
        callback(self.moves)
        time.sleep(0.5)

        if node in self.goals:
            return node

        if depth <= 0:
            return None

        for neighbor in get_neighbors(*node, self.rows, self.cols, self.walls):
            if neighbor not in parent:
                parent[neighbor] = node
                result = self.dfs(neighbor, depth - 1, parent, callback)
                if result is not None:
                    return result

        return None

    def run(self, callback) -> List[Tuple[int, int]]:
        """Run IDDFS algorithm and return the path to the goal."""
        max_depth = self.rows * self.cols  # Maximum possible path length

        for depth in range(max_depth):
            parent = {self.start: None}
            result = self.dfs(self.start, depth, parent, callback)
            if result is not None:
                logger.info(f"Goal reached at {result}")
                return reconstruct_path(parent, result)

        logger.warning("No path to goal found")
        return []
