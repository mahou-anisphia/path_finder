import queue
import time
import logging
from typing import List, Tuple, Dict, Set
from src.utils.pathfinding_utils import parse_walls, is_valid_move, get_neighbors, reconstruct_path

logger = logging.getLogger(__name__)


class BFS:
    def __init__(self, environment: Dict):
        self.rows, self.cols = environment['dimensions']
        self.start = environment['start']
        self.goals = set(environment['goals'])
        self.walls = parse_walls(environment['walls'], self.rows, self.cols)
        self.moves = []

    def run(self, callback) -> List[Tuple[int, int]]:
        """Run BFS algorithm and return the path to the goal."""
        q = queue.Queue()
        q.put(self.start)
        visited = set([self.start])
        parent = {self.start: None}

        while not q.empty():
            current = q.get()
            self.moves.append(current)

            # Update UI and wait
            callback(self.moves)
            time.sleep(0.5)

            if current in self.goals:
                logger.info(f"Goal reached at {current}")
                return reconstruct_path(parent, current)

            for neighbor in get_neighbors(*current, self.rows, self.cols, self.walls):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    q.put(neighbor)

        logger.warning("No path to goal found")
        return []
