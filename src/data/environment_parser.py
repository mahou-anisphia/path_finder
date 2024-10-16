def parse_environment(raw_data):
    """
    Parses the raw input data and returns a structured environment object.
    """
    lines = [line.strip() for line in raw_data]

    # Parse grid dimensions
    dimensions = lines[0][1:-1].split(',')
    rows, cols = map(int, dimensions)

    # Parse start position
    start = tuple(map(int, lines[1][1:-1].split(',')))

    # Parse goal positions
    goals = [tuple(map(int, goal.strip()[1:-1].split(',')))
             for goal in lines[2].split('|')]

    # Parse walls
    walls = [list(map(int, line[1:-1].split(',')))
             for line in lines[3:] if line]

    return {
        'dimensions': (rows, cols),
        'start': start,
        'goals': goals,
        'walls': walls
    }
