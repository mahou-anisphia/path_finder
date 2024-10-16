import tkinter as tk
from tkinter import filedialog, messagebox
import logging
from src.data.file_reader import read_input_file
from src.data.environment_parser import parse_environment
from src.visualizers.grid_visualizer import GridVisualizer


class RobotNavigationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Robot Navigation")
        self.logger = logging.getLogger(__name__)

        self.visualizer = GridVisualizer(self.master)

        self.load_button = tk.Button(
            self.master, text="Load Environment", command=self.load_environment)
        self.load_button.pack()

        self.logger.info("RobotNavigationApp initialized")

    def load_environment(self):
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt")])
            if filename:
                raw_data = read_input_file(filename)
                environment = parse_environment(raw_data)
                self.visualizer.initialize_grid(environment)
                self.logger.info(
                    f"Environment loaded and visualized: {filename}")
        except Exception as e:
            self.logger.error(f"Error loading environment: {str(e)}")
            messagebox.showerror(
                "Error", f"Failed to load environment: {str(e)}")
