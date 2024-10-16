import tkinter as tk


class GridVisualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("Robot Navigation")
        self.cell_size = 50
        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def initialize_grid(self, environment):
        """
        Initializes and draws the grid based on the parsed environment.
        """
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
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray")

        # Layer 3: Start Position Layer
        x, y = environment['start']
        self.canvas.create_oval(x*self.cell_size, y*self.cell_size,
                                (x+1)*self.cell_size, (y+1)*self.cell_size, fill="red")

        # Layer 4: Goal Layer
        for goal in environment['goals']:
            x, y = goal
            self.canvas.create_rectangle(x*self.cell_size, y*self.cell_size,
                                         (x+1)*self.cell_size, (y+1)*self.cell_size, fill="green")
