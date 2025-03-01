#!/usr/bin/env python3
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QDir
import qdarktheme

from src.ui.main_window import MainWindow
from src.utils.config import Config

def main():
    # Initialize configuration
    config = Config()
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Siro File Transfer")
    
    # Set application style
    theme = config.get_theme()
    if theme == "dark":
        app.setStyleSheet(qdarktheme.load_stylesheet())
    else:
        app.setStyleSheet(qdarktheme.load_stylesheet("light"))
    
    # Set current directory for file dialogs
    QDir.setCurrent(os.path.expanduser("~"))
    
    # Create and show main window
    main_window = MainWindow(config)
    main_window.show()
    
    # Execute application
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 