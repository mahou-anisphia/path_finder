import logging


def parse_environment(raw_data):
    """
    Parses the raw input data and returns a structured environment object.
    Raises an error if the parsing fails.
    """
    logger = logging.getLogger(__name__)

    try:
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

        environment = {
            'dimensions': (rows, cols),
            'start': start,
            'goals': goals,
            'walls': walls
        }

        logger.info("Successfully parsed environment data")
        return environment
    except IndexError:
        logger.error("Input data does not contain enough lines")
        raise ValueError("Input data does not contain enough lines")
    except ValueError as e:
        logger.error(f"Error parsing numeric values: {str(e)}")
        raise ValueError(f"Error parsing numeric values: {str(e)}")
    except Exception as e:
        logger.error(
            f"Unexpected error occurred while parsing environment: {str(e)}")
        raise
