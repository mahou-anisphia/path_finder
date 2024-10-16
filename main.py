import tkinter as tk
import logging
from src.utils.logging import setup_logging
from src.robot_navigation_app import RobotNavigationApp

if __name__ == "__main__":
    log_filename = setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Application started")

    root = tk.Tk()
    app = RobotNavigationApp(root)

    logger.info("GUI initialized")
    root.mainloop()
    logger.info("Application closed")
