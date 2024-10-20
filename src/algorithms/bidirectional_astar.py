import heapq
from typing import List, Tuple, Dict, Set
from src.utils.pathfinding_utils import get_neighbors, manhattan_distance, parse_walls

class BidirectionalAStar:
    def __init__(self, environment: Dict):
        self.rows, self.cols = environment['dimensions']
        self.start = environment['start']
        self.goals = set(environment['goals'])
        self.walls = parse_walls(environment['walls'])
        self.moves = []

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return manhattan_distance(a, b)

    def search(self, start: Tuple[int, int], goals: Set[Tuple[int, int]], reverse: bool = False):
        open_set = [(0, start)]
        closed_set = set()
        g_score = {start: 0}
        f_score = {start: min(self.heuristic(start, goal) for goal in goals)}
        parent = {start: None}

        while open_set:
            current_f, current = heapq.heappop(open_set)

            if current in goals:
                return current, parent, g_score

            closed_set.add(current)

            for neighbor in get_neighbors(*current, self.rows, self.cols, self.walls):
                if neighbor in closed_set:
                    continue

                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    parent[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = g_score[neighbor] + min(self.heuristic(neighbor, goal) for goal in goals)
                    heapq.heappush(open_set, (f_score, neighbor))

        return None, parent, g_score

    def run(self, callback=None) -> List[Tuple[int, int]]:
        forward_goal, forward_parent, forward_g = self.search(self.start, self.goals)
        backward_start, backward_parent, backward_g = self.search(list(self.goals)[0], {self.start}, reverse=True)

        if forward_goal is None or backward_start is None:
            return []

        intersection = set(forward_g.keys()) & set(backward_g.keys())
        if not intersection:
            return []

        meeting_point = min(intersection, key=lambda x: forward_g[x] + backward_g[x])

        path = []
        current = meeting_point
        while current:
            path.append(current)
            current = forward_parent[current]
        path = path[::-1]

        current = backward_parent[meeting_point]
        while current:
            path.append(current)
            current = backward_parent[current]

        self.moves = path
        return path
