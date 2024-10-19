import time
import logging
from typing import List, Tuple, Dict, Set
from src.utils.pathfinding_utils import get_neighbors, reconstruct_path, parse_walls

logger = logging.getLogger(__name__)


class DFS:
    def __init__(self, environment: Dict):
        self.rows, self.cols = environment['dimensions']
        self.start = environment['start']
        self.goals = set(environment['goals'])
        self.walls = parse_walls(environment['walls'])
        self.moves = []

    def run(self, callback) -> List[Tuple[int, int]]:
        """Run DFS algorithm and return the path to the goal."""
        stack = [self.start]
        visited = set()
        parent = {self.start: None}

        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                self.moves.append(current)

                # Update UI and wait
                callback(self.moves)
                time.sleep(0.5)

                if current in self.goals:
                    logger.info(f"Goal reached at {current}")
                    return reconstruct_path(parent, current)

                for neighbor in get_neighbors(*current, self.rows, self.cols, self.walls):
                    if neighbor not in visited:
                        stack.append(neighbor)
                        parent[neighbor] = current

        logger.warning("No path to goal found")
        return []
