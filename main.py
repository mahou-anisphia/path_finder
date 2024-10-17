import customtkinter as ctk
import logging
import os
from src.utils.logging import setup_logging
from src.robot_navigation_app import RobotNavigationApp

if __name__ == "__main__":
    log_path = setup_logging()
    logger = logging.getLogger(__name__)
    logger.info(f"Application started. Log file: {log_path}")

    root = ctk.CTk()
    root.geometry("800x600")
    app = RobotNavigationApp(root)

    logger.info("GUI initialized")
    root.mainloop()
    logger.info("Application closed")
