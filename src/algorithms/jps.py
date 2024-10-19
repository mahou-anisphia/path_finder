import heapq
import time
import logging
from typing import List, Tuple, Dict, Set
from src.utils.pathfinding_utils import is_valid_move, manhattan_distance, reconstruct_path, parse_walls

logger = logging.getLogger(__name__)


class JPS:
    def __init__(self, environment: Dict):
        self.rows, self.cols = environment['dimensions']
        self.start = environment['start']
        self.goals = set(environment['goals'])
        self.walls = parse_walls(environment['walls'])
        self.moves = []

    def jump(self, x: int, y: int, dx: int, dy: int) -> Tuple[int, int] | None:
        nx, ny = x + dx, y + dy

        if not is_valid_move(nx, ny, self.rows, self.cols, self.walls):
            return None

        if (nx, ny) in self.goals:
            return (nx, ny)

        if dx != 0 and dy != 0:
            if (is_valid_move(nx, y, self.rows, self.cols, self.walls) and
                not is_valid_move(nx - dx, y, self.rows, self.cols, self.walls)) or \
               (is_valid_move(x, ny, self.rows, self.cols, self.walls) and
                    not is_valid_move(x, ny - dy, self.rows, self.cols, self.walls)):
                return (nx, ny)

        if dx != 0:
            if (is_valid_move(nx, y + 1, self.rows, self.cols, self.walls) and
                not is_valid_move(x, y + 1, self.rows, self.cols, self.walls)) or \
               (is_valid_move(nx, y - 1, self.rows, self.cols, self.walls) and
                    not is_valid_move(x, y - 1, self.rows, self.cols, self.walls)):
                return (nx, ny)
        else:
            if (is_valid_move(x + 1, ny, self.rows, self.cols, self.walls) and
                not is_valid_move(x + 1, y, self.rows, self.cols, self.walls)) or \
               (is_valid_move(x - 1, ny, self.rows, self.cols, self.walls) and
                    not is_valid_move(x - 1, y, self.rows, self.cols, self.walls)):
                return (nx, ny)

        return self.jump(nx, ny, dx, dy)

    def get_successors(self, node: Tuple[int, int], parent: Tuple[int, int]) -> List[Tuple[int, int]]:
        successors = []
        x, y = node
        px, py = parent

        neighbors = []
        if x != px:
            neighbors.append((x + (x - px), y))
            if y != py:
                neighbors.append((x + (x - px), y + (y - py)))
                neighbors.append((x, y + (y - py)))
            else:
                neighbors.append((x, y + 1))
                neighbors.append((x, y - 1))
        else:
            neighbors.append((x, y + (y - py)))
            neighbors.append((x + 1, y))
            neighbors.append((x - 1, y))

        for nx, ny in neighbors:
            jump_point = self.jump(x, y, nx - x, ny - y)
            if jump_point:
                successors.append(jump_point)

        return successors

    def run(self, callback) -> List[Tuple[int, int]]:
        """Run JPS algorithm and return the path to the goal."""
        open_set = [(0, self.start)]
        closed_set = set()
        g_score = {self.start: 0}
        f_score = {self.start: min(manhattan_distance(
            self.start, goal) for goal in self.goals)}
        parent = {self.start: self.start}

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

            for successor in self.get_successors(current, parent[current]):
                if successor in closed_set:
                    continue

                tentative_g_score = g_score[current] + \
                    manhattan_distance(current, successor)

                if successor not in [item[1] for item in open_set] or tentative_g_score < g_score.get(successor, float('inf')):
                    parent[successor] = current
                    g_score[successor] = tentative_g_score
                    f_score[successor] = g_score[successor] + \
                        min(manhattan_distance(successor, goal)
                            for goal in self.goals)
                    if successor not in [item[1] for item in open_set]:
                        heapq.heappush(
                            open_set, (f_score[successor], successor))
                    else:
                        # Update priority
                        open_set = [(f_score[item[1]], item[1]) if item[1]
                                    == successor else item for item in open_set]
                        heapq.heapify(open_set)

        logger.warning("No path to goal found")
        return []
