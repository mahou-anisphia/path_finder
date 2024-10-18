import customtkinter as ctk
import logging


class GridVisualizer:
    def __init__(self, master):
        self.logger = logging.getLogger(__name__)
        self.master = master
        self.cell_size = 50
        self.canvas = ctk.CTkCanvas(self.master)
        self.canvas.pack(fill="both", expand=True)
        self.move_layer = {}  # Dictionary to store move rectangles
        self.logger.info("GridVisualizer initialized")

    def initialize_grid(self, environment):
        """
        Initializes and draws the grid based on the parsed environment.
        """
        try:
            self.clear_grid()  # Clear existing grid before initializing new one
            rows, cols = environment['dimensions']
            self.canvas.config(width=cols*self.cell_size,
                               height=rows*self.cell_size)

            # Layer 1 & 2: Background and Wall Layer
            for i in range(rows):
                for j in range(cols):
                    x1, y1 = j * self.cell_size, i * self.cell_size
                    x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")

            for wall in environment['walls']:
                x, y, width, height = wall
                for i in range(y, y + height):
                    for j in range(x, x + width):
                        x1, y1 = j * self.cell_size, i * self.cell_size
                        x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                        self.canvas.create_rectangle(
                            x1, y1, x2, y2, fill="gray")

            # Layer 3: Start Position Layer
            x, y = environment['start']
            self.canvas.create_oval(x*self.cell_size, y*self.cell_size,
                                    (x+1)*self.cell_size, (y+1)*self.cell_size, fill="red")

            # Layer 4: Goal Layer
            for goal in environment['goals']:
                x, y = goal
                self.canvas.create_rectangle(x*self.cell_size, y*self.cell_size,
                                             (x+1)*self.cell_size, (y+1)*self.cell_size, fill="green")

            self.logger.info("Grid initialized and drawn successfully")
        except KeyError as e:
            self.logger.error(
                f"Missing key in environment dictionary: {str(e)}")
            raise ValueError(
                f"Invalid environment structure: missing {str(e)}")
        except Exception as e:
            self.logger.error(
                f"Unexpected error occurred while initializing grid: {str(e)}")
            raise

    def clear_grid(self):
        """
        Clears the current grid.
        """
        try:
            self.canvas.delete("all")
            self.move_layer = {}
            self.logger.info("Grid cleared successfully")
        except Exception as e:
            self.logger.error(
                f"Unexpected error occurred while clearing grid: {str(e)}")
            raise

    def update_moves(self, move_map):
        """
        Updates the grid to show all cells the robot has moved on.
        """
        try:
            # Remove old move markers
            for rect_id in self.move_layer.values():
                self.canvas.delete(rect_id)
            self.move_layer.clear()

            # Add new move markers
            for (x, y), value in move_map.items():
                if value > 0:  # If the robot has moved on this cell
                    x1, y1 = x * self.cell_size, y * self.cell_size
                    x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                    rect_id = self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill="light blue", stipple="gray50")
                    self.move_layer[(x, y)] = rect_id

            self.logger.info(
                f"Move layer updated with {len(self.move_layer)} cells")
        except Exception as e:
            self.logger.error(
                f"Unexpected error occurred while updating moves: {str(e)}")
            raise
