import tkinter as tk
from tkinter import filedialog
from src.data.file_reader import read_input_file
from src.data.environment_parser import parse_environment
from src.visualizers.grid_visualizer import GridVisualizer


def load_environment():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        raw_data = read_input_file(filename)
        environment = parse_environment(raw_data)
        visualizer.initialize_grid(environment)


if __name__ == "__main__":
    root = tk.Tk()
    visualizer = GridVisualizer(root)

    load_button = tk.Button(
        root, text="Load Environment", command=load_environment)
    load_button.pack()

    root.mainloop()
