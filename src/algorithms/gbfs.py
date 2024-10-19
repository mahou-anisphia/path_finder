import heapq
import time
import logging
from typing import List, Tuple, Dict, Set
from src.utils.pathfinding_utils import get_neighbors, reconstruct_path, manhattan_distance

logger = logging.getLogger(__name__)


class GBFS:
    def __init__(self, environment: Dict):
        self.rows, self.cols = environment['dimensions']
        self.start = environment['start']
        self.goals = set(environment['goals'])
        self.walls = set((x, y) for x, y, w, h in environment['walls'] for dx in range(
            w) for dy in range(h))
        self.moves = []

    def run(self, callback) -> List[Tuple[int, int]]:
        """Run GBFS algorithm and return the path to the goal."""
        open_set = [(0, self.start)]
        closed_set = set()
        parent = {self.start: None}

        while open_set:
            _, current = heapq.heappop(open_set)
            self.moves.append(current)

            # Update UI and wait
            callback(self.moves)
            time.sleep(0.5)

            if current in self.goals:
                logger.info(f"Goal reached at {current}")
                return reconstruct_path(parent, current)

            closed_set.add(current)

            for neighbor in get_neighbors(*current, self.rows, self.cols, self.walls):
                if neighbor in closed_set:
                    continue

                if neighbor not in [item[1] for item in open_set]:
                    parent[neighbor] = current
                    h = min(manhattan_distance(neighbor, goal)
                            for goal in self.goals)
                    heapq.heappush(open_set, (h, neighbor))

        logger.warning("No path to goal found")
        return []
