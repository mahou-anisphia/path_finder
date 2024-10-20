import customtkinter as ctk
from tkinter import filedialog, messagebox
import logging
import random
from src.data.file_reader import read_input_file
from src.data.environment_parser import parse_environment
from src.visualizers.grid_visualizer import GridVisualizer
from src.algorithms.bfs import BFS
from src.algorithms.dfs import DFS
from src.algorithms.gbfs import GBFS
from src.algorithms.astar import AStar
from src.algorithms.iddfs import IDDFS
from src.algorithms.best_first_search import BestFirstSearch
from src.algorithms.bidirectional_astar import BidirectionalAStar


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

        self.random_grid_button = ctk.CTkButton(
            self.sidebar, text="Generate Random Grid", command=self.generate_random_grid)
        self.random_grid_button.pack(pady=10, padx=20, fill="x")

        # Add buttons for each algorithm
        self.bfs_button = ctk.CTkButton(
            self.sidebar, text="Run BFS", command=lambda: self.run_algorithm(BFS))
        self.bfs_button.pack(pady=10, padx=20, fill="x")

        self.dfs_button = ctk.CTkButton(
            self.sidebar, text="Run DFS", command=lambda: self.run_algorithm(DFS))
        self.dfs_button.pack(pady=10, padx=20, fill="x")

        self.gbfs_button = ctk.CTkButton(
            self.sidebar, text="Run GBFS", command=lambda: self.run_algorithm(GBFS))
        self.gbfs_button.pack(pady=10, padx=20, fill="x")

        self.astar_button = ctk.CTkButton(
            self.sidebar, text="Run A*", command=lambda: self.run_algorithm(AStar))
        self.astar_button.pack(pady=10, padx=20, fill="x")

        self.iddfs_button = ctk.CTkButton(
            self.sidebar, text="Run IDDFS", command=lambda: self.run_algorithm(IDDFS))
        self.iddfs_button.pack(pady=10, padx=20, fill="x")

        self.best_first_button = ctk.CTkButton(
            self.sidebar, text="Run Best-First Search", command=lambda: self.run_algorithm(BestFirstSearch))
        self.best_first_button.pack(pady=10, padx=20, fill="x")

        # self.bidirectional_astar_button = ctk.CTkButton(
        #     self.sidebar, text="Run Bidirectional A*", command=lambda: self.run_algorithm(BidirectionalAStar))
        # self.bidirectional_astar_button.pack(pady=10, padx=20, fill="x")

        self.environment = None
        self.current_algorithm = None

        self.logger.info("RobotNavigationApp initialized")

    def load_environment(self):
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt")])
            if filename:
                raw_data = read_input_file(filename)
                self.environment = parse_environment(raw_data)
                self.visualizer.initialize_grid(self.environment)
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
            self.current_algorithm = None
            self.logger.info("Grid cleared")
        except Exception as e:
            self.logger.error(f"Error clearing grid: {str(e)}")
            messagebox.showerror(
                "Error", f"Failed to clear grid: {str(e)}")

    def generate_random_grid(self):
        while True:
            rows, cols = random.randint(5, 15), random.randint(5, 15)
            start = (random.randint(0, cols-1), random.randint(0, rows-1))
            goals = [(random.randint(0, cols-1), random.randint(0, rows-1))
                     for _ in range(random.randint(1, 3))]

            num_walls = random.randint(3, 10)
            walls = []
            for _ in range(num_walls):
                x, y = random.randint(0, cols-1), random.randint(0, rows-1)
                width, height = random.randint(1, 3), random.randint(1, 3)
                walls.append((x, y, width, height))

            self.environment = {
                'dimensions': (rows, cols),
                'start': start,
                'goals': goals,
                'walls': walls
            }

            # Check if the grid has a solution
            bidirectional_astar = BidirectionalAStar(self.environment)
            path = bidirectional_astar.run()

            if path:
                self.visualizer.initialize_grid(self.environment)
                self.logger.info("Random grid generated with a valid solution")
                messagebox.showinfo(
                    "Random Grid", "A new random grid with a valid solution has been generated.")
                break
            else:
                self.logger.info("Generated grid has no solution, retrying...")

    def run_algorithm(self, algorithm_class):
        if not self.environment:
            messagebox.showerror("Error", "Please load an environment first.")
            return

        try:
            self.current_algorithm = algorithm_class(self.environment)
            path = self.current_algorithm.run(self.update_visualizer)
            if path:
                self.logger.info(
                    f"{algorithm_class.__name__} completed. Path found: {path}")
                messagebox.showinfo(
                    f"{algorithm_class.__name__} Complete", "Path to goal found!")
            else:
                self.logger.warning(
                    f"{algorithm_class.__name__} completed. No path to goal found.")
                messagebox.showwarning(
                    f"{algorithm_class.__name__} Complete", "No path to goal found.")
        except Exception as e:
            self.logger.error(
                f"Error running {algorithm_class.__name__}: {str(e)}")
            messagebox.showerror(
                "Error", f"Failed to run {algorithm_class.__name__}: {str(e)}")

    def update_visualizer(self, moves):
        self.visualizer.update_moves({move: 1 for move in moves})
        self.master.update()
