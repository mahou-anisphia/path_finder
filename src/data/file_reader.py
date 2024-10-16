import logging
import os


def read_input_file(filename):
    """
    Reads the input file and returns the raw content.
    Raises an error if the file is not a .txt file.
    """
    logger = logging.getLogger(__name__)

    try:
        if not filename.lower().endswith('.txt'):
            raise ValueError("Input file must be a .txt file")

        with open(filename, 'r') as file:
            logger.info(f"Successfully read input file: {filename}")
            return file.readlines()
    except FileNotFoundError:
        logger.error(f"File not found: {filename}")
        raise
    except IOError as e:
        logger.error(
            f"IO error occurred while reading file {filename}: {str(e)}")
        raise
    except Exception as e:
        logger.error(
            f"Unexpected error occurred while reading file {filename}: {str(e)}")
        raise
