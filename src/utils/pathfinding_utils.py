from typing import List, Tuple, Set, Dict
import math

def parse_walls(walls: List[List[int]], rows: int, cols: int) -> Set[Tuple[int, int]]:
    """Convert wall rectangles to individual cell coordinates."""
    wall_cells = set()
    for wall in walls:
        x, y, width, height = wall
        for i in range(y, y + height):
            for j in range(x, x + width):
                wall_cells.add((j, i))
    return wall_cells

def is_valid_move(x: int, y: int, rows: int, cols: int, walls: Set[Tuple[int, int]]) -> bool:
    """Check if the given coordinates are within the grid and not a wall."""
    return 0 <= x < cols and 0 <= y < rows and (x, y) not in walls

def get_neighbors(x: int, y: int, rows: int, cols: int, walls: Set[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Get valid neighboring cells."""
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    return [(x + dx, y + dy) for dx, dy in directions if is_valid_move(x + dx, y + dy, rows, cols, walls)]

def reconstruct_path(parent: Dict[Tuple[int, int], Tuple[int, int]], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Reconstruct the path from start to goal."""
    path = []
    current = goal
    while current:
        path.append(current)
        current = parent[current]
    return list(reversed(path))

# Heuristic functions

def manhattan_distance(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """Calculate the Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean_distance(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def chebyshev_distance(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """Calculate the Chebyshev distance between two points."""
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

def octile_distance(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    """Calculate the octile distance between two points."""
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)
