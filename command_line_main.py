import sys
import logging
from src.utils.logging import setup_logging
from src.data.file_reader import read_input_file
from src.data.environment_parser import parse_environment
from src.command_line_robot import CommandLineRobot


def main():
    log_path = setup_logging()
    logger = logging.getLogger(__name__)
    logger.info(f"Command-line application started. Log file: {log_path}")

    if len(sys.argv) != 3:
        print("Usage: python command_line_main.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2]

    try:
        raw_data = read_input_file(filename)
        environment = parse_environment(raw_data)
        robot = CommandLineRobot(environment)

        goal, num_nodes, path = robot.run_algorithm(method)
        output = robot.format_output(filename, method, goal, num_nodes, path)
        print(output)

        logger.info("Command-line application completed successfully")
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
