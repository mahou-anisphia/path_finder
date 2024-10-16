import customtkinter as ctk
from tkinter import filedialog, messagebox
import logging
from src.data.file_reader import read_input_file
from src.data.environment_parser import parse_environment
from src.visualizers.grid_visualizer import GridVisualizer
from src.algorithms.bfs import BFS


class RobotNavigationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Robot Navigation")
        self.logger = logging.getLogger(__name__)

        # Set the theme
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Create main frame
        self.main_frame = ctk.CTkFrame(master)
        self.main_frame.pack(fill="both", expand=True)

        # Create sidebar
        self.sidebar = ctk.CTkFrame(
            self.main_frame, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        # Create content area
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(side="right", fill="both",
                                expand=True, padx=10, pady=10)

        self.visualizer = GridVisualizer(self.content_frame)

        # Add buttons to sidebar
        self.load_button = ctk.CTkButton(
            self.sidebar, text="Load Environment", command=self.load_environment)
        self.load_button.pack(pady=10, padx=20, fill="x")

        self.clear_button = ctk.CTkButton(
            self.sidebar, text="Clear Grid", command=self.clear_grid)
        self.clear_button.pack(pady=10, padx=20, fill="x")

        # Add BFS button
        self.bfs_button = ctk.CTkButton(
            self.sidebar, text="Run BFS", command=self.run_bfs)
        self.bfs_button.pack(pady=10, padx=20, fill="x")

        self.environment = None
        self.bfs = None

        self.logger.info("RobotNavigationApp initialized")

    def load_environment(self):
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt")])
            if filename:
                raw_data = read_input_file(filename)
                self.environment = parse_environment(raw_data)
                self.visualizer.initialize_grid(self.environment)
                self.bfs = BFS(self.environment)
                self.logger.info(
                    f"Environment loaded and visualized: {filename}")
        except Exception as e:
            self.logger.error(f"Error loading environment: {str(e)}")
            messagebox.showerror(
                "Error", f"Failed to load environment: {str(e)}")

    def clear_grid(self):
        try:
            self.visualizer.clear_grid()
            self.environment = None
            self.bfs = None
            self.logger.info("Grid cleared")
        except Exception as e:
            self.logger.error(f"Error clearing grid: {str(e)}")
            messagebox.showerror(
                "Error", f"Failed to clear grid: {str(e)}")

    def run_bfs(self):
        if not self.environment or not self.bfs:
            messagebox.showerror("Error", "Please load an environment first.")
            return

        try:
            path = self.bfs.run(self.update_visualizer)
            if path:
                self.logger.info(f"BFS completed. Path found: {path}")
                messagebox.showinfo("BFS Complete", "Path to goal found!")
            else:
                self.logger.warning("BFS completed. No path to goal found.")
                messagebox.showwarning(
                    "BFS Complete", "No path to goal found.")
        except Exception as e:
            self.logger.error(f"Error running BFS: {str(e)}")
            messagebox.showerror("Error", f"Failed to run BFS: {str(e)}")

    def update_visualizer(self, moves):
        self.visualizer.update_moves({move: 1 for move in moves})
        self.master.update()
