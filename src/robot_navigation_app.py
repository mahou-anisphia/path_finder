import customtkinter as ctk
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

        # Set the theme
        # Modes: "System" (standard), "Dark", "Light"
        ctk.set_appearance_mode("System")
        # Themes: "blue" (standard), "green", "dark-blue"
        ctk.set_default_color_theme("blue")

        self.frame = ctk.CTkFrame(master)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.visualizer = GridVisualizer(self.frame)

        self.load_button = ctk.CTkButton(
            self.frame, text="Load Environment", command=self.load_environment)
        self.load_button.pack(pady=10)

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
