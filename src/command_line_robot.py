import logging
from typing import List, Tuple, Dict
from src.data.environment_parser import parse_environment
from src.algorithms.bfs import BFS
from src.algorithms.dfs import DFS
from src.algorithms.gbfs import GBFS
from src.algorithms.astar import AStar
from src.algorithms.iddfs import IDDFS
from src.algorithms.best_first_search import BestFirstSearch

logger = logging.getLogger(__name__)


class CommandLineRobot:
    def __init__(self, environment: Dict):
        self.environment = environment
        self.algorithms = {
            'BFS': BFS,
            'DFS': DFS,
            'GBFS': GBFS,
            'AS': AStar,
            'IDDFS': IDDFS,
            'CUS1': IDDFS,  # Assuming IDDFS as Custom Search 1
            'CUS2': BestFirstSearch  # Assuming BestFirstSearch as Custom Search 2
        }

    def run_algorithm(self, method: str) -> Tuple[str, int, List[Tuple[int, int]]]:
        if method not in self.algorithms:
            raise ValueError(f"Unknown method: {method}")

        algorithm = self.algorithms[method](self.environment)
        # No UI updates for command-line version
        path = algorithm.run(lambda x: None)

        if path:
            goal = path[-1]
            num_nodes = len(algorithm.moves)
            return goal, num_nodes, path
        else:
            num_nodes = len(algorithm.moves)
            return None, num_nodes, []

    @staticmethod
    def path_to_moves(path: List[Tuple[int, int]]) -> List[str]:
        moves = []
        for i in range(1, len(path)):
            prev_x, prev_y = path[i-1]
            curr_x, curr_y = path[i]
            if curr_x < prev_x:
                moves.append('left')
            elif curr_x > prev_x:
                moves.append('right')
            elif curr_y < prev_y:
                moves.append('up')
            elif curr_y > prev_y:
                moves.append('down')
        return moves

    @staticmethod
    def format_output(filename: str, method: str, goal: Tuple[int, int], num_nodes: int, path: List[Tuple[int, int]]) -> str:
        if goal:
            moves = CommandLineRobot.path_to_moves(path)
            return f"{filename} {method}\n{goal} {num_nodes}\n{moves}"
        else:
            return f"{filename} {method}\nNo goal is reachable; {num_nodes}"
