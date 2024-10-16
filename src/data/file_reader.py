def read_input_file(filename):
    """
    Reads the input file and returns the raw content.
    """
    with open(filename, 'r') as file:
        return file.readlines()
