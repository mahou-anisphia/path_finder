import heapq
import time
import logging
from typing import List, Tuple, Dict
from src.utils.pathfinding_utils import get_neighbors, reconstruct_path, parse_walls, manhattan_distance

logger = logging.getLogger(__name__)


class BestFirstSearch:
    def __init__(self, environment: Dict):
        self.rows, self.cols = environment['dimensions']
        self.start = environment['start']
        self.goals = set(environment['goals'])
        self.walls = parse_walls(environment['walls'])
        self.moves = []

    def heuristic(self, node: Tuple[int, int]) -> float:
        return min(manhattan_distance(node, goal) for goal in self.goals)

    def run(self, callback) -> List[Tuple[int, int]]:
        """Run Best-First Search algorithm and return the path to the goal."""
        open_set = [(self.heuristic(self.start), self.start)]
        closed_set = set()
        parent = {self.start: None}

        while open_set:
            _, current = heapq.heappop(open_set)
            self.moves.append(current)

            # Update UI and wait
            callback(self.moves)
            time.sleep(0.1)

            if current in self.goals:
                logger.info(f"Goal reached at {current}")
                return reconstruct_path(parent, current)

            closed_set.add(current)

            for neighbor in get_neighbors(*current, self.rows, self.cols, self.walls):
                if neighbor in closed_set:
                    continue

                if neighbor not in [item[1] for item in open_set]:
                    parent[neighbor] = current
                    heapq.heappush(
                        open_set, (self.heuristic(neighbor), neighbor))

        logger.warning("No path to goal found")
        return []
