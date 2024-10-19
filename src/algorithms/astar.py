import heapq
import time
import logging
from typing import List, Tuple, Dict, Set
from src.utils.pathfinding_utils import get_neighbors, reconstruct_path, manhattan_distance, parse_walls

logger = logging.getLogger(__name__)


class AStar:
    def __init__(self, environment: Dict):
        self.rows, self.cols = environment['dimensions']
        self.start = environment['start']
        self.goals = set(environment['goals'])
        self.walls = parse_walls(environment['walls'])
        self.moves = []

    def run(self, callback) -> List[Tuple[int, int]]:
        """Run A* algorithm and return the path to the goal."""
        open_set = [(0, self.start)]
        closed_set = set()
        g_score = {self.start: 0}
        f_score = {self.start: min(manhattan_distance(
            self.start, goal) for goal in self.goals)}
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

                tentative_g_score = g_score[current] + 1

                if neighbor not in [item[1] for item in open_set]:
                    parent[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + \
                        min(manhattan_distance(neighbor, goal)
                            for goal in self.goals)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                elif tentative_g_score < g_score[neighbor]:
                    parent[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + \
                        min(manhattan_distance(neighbor, goal)
                            for goal in self.goals)
                    # Update priority
                    open_set = [(f_score[item[1]], item[1]) if item[1]
                                == neighbor else item for item in open_set]
                    heapq.heapify(open_set)

        logger.warning("No path to goal found")
        return []
