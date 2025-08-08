"""
Mesh Menu Handler
Manages all mesh-related operations
"""

import os
from PyQt5.QtWidgets import QMessageBox
import re
from preloader.preloader_manager import PreloaderManager
from parser import parser_neutral_file
import logging
logger = logging.getLogger(__name__)


class MeshHandler:
    def __init__(self, main_window):
        self.main_window = main_window

        # Initialize preloader manager
        self.preloader_manager = PreloaderManager(
            main_window.visualization_manager)
        self.neu_files = []
        self.working_directory = None

    def initial_mesh(self):
        """Load initial mesh (FEM1.NEU)"""
        working_directory = None
        if hasattr(self.main_window, 'file_handler') and self.main_window.file_handler.working_directory:
            working_directory = self.main_window.file_handler.working_directory
            logger.info(f"Dir: {working_directory}")

            # Search for FEM1.NEU
            fem1_path = os.path.join(working_directory, "FEM1.NEU")
            if not os.path.exists(fem1_path):
                raise FileNotFoundError(f"File {fem1_path} does not exist")
            else:
                self._load_and_display_mesh(fem1_path)
                # reset the visualization manager to default state
                self.main_window.visualization_manager.reset_view()

    def _load_and_display_mesh(self, file_path):
        """Load and display mesh file"""
        try:
            neutral_file = parser_neutral_file.parser_file(file_path)

            if not neutral_file:
                QMessageBox.warning(
                    self.main_window,
                    "Parsing Error",
                    "Cannot parse selected file.\n"
                    "Check that file is in correct .neu format"
                )
                return

            self.main_window.visualization_manager.load_neutral_file(
                neutral_file)
            self.main_window.visualization_manager.set_as_central_widget()

            # Display loaded filename
            filename = os.path.basename(file_path)
            logger.info(f"Mesh loaded: {filename}")

        except Exception as e:
            QMessageBox.critical(
                self.main_window,
                "Loading Error",
                f"Error loading mesh file:\n{str(e)}"
            )

    def _fast_load_and_display_mesh(self, file_index):
        """Fast load using preloaded data"""
        try:
            preloaded_data = self.preloader_manager.get_preloaded_data(
                file_index)

            if preloaded_data:
                logger.info(f"Using preloaded data for file {file_index + 1}")
                self.main_window.visualization_manager.load_neutral_file(
                    preloaded_data)
                filename = self.neu_files[file_index] if file_index < len(
                    self.neu_files) else "Unknown"
                logger.info(f"Fast mesh loaded: {filename}")
            else:
                if file_index < len(self.neu_files):
                    file_path = os.path.join(
                        self.working_directory, self.neu_files[file_index])
                    logger.info(
                        f"Preload not ready, loading from disk: {self.neu_files[file_index]}")
                    self._load_and_display_mesh(file_path)
        except Exception as e:
            logger.exception(f"Error in fast load: {e}")
            # Fallback to normal loading
            if file_index < len(self.neu_files):
                file_path = os.path.join(
                    self.working_directory, self.neu_files[file_index])
                self._load_and_display_mesh(file_path)

    def _smart_load_callback(self, file_path):
        """Smart loading callback that uses preloaded data when available"""
        try:
            filename = os.path.basename(file_path)
            if filename in self.neu_files:
                file_index = self.neu_files.index(filename)
                self._fast_load_and_display_mesh(file_index)
            else:
                self._load_and_display_mesh(file_path)

            self.main_window.visualization_manager._update_data_info()

        except Exception as e:
            logger.exception(f"Error in smart load: {e}")
            self._load_and_display_mesh(file_path)
            # Update data info even on error
            self.main_window.visualization_manager._update_data_info()

    def deformed_mesh(self):
        """Display deformed mesh"""
        working_directory = None
        if hasattr(self.main_window, 'file_handler') and self.main_window.file_handler.working_directory:
            working_directory = self.main_window.file_handler.working_directory
            self.working_directory = working_directory

            # Search for all .NEU files in directory
            try:
                neu_files = [f for f in os.listdir(
                    working_directory) if f.endswith('.NEU')]
                number_of_neu_files = len(neu_files)

                if number_of_neu_files == 0:
                    QMessageBox.warning(
                        self.main_window,
                        "No Files Found",
                        "No .NEU files found in working directory."
                    )
                    return

                # Sort files numerically (FEM1, FEM2, FEM10, FEM11...)
                def natural_sort_key(filename):
                    """Natural sorting function for filenames with numbers"""
                    parts = re.split(r'(\d+)', filename)
                    return [int(part) if part.isdigit() else part for part in parts]

                neu_files.sort(key=natural_sort_key)
                self.neu_files = neu_files

                first_file_path = os.path.join(working_directory, neu_files[0])
                self._load_and_display_mesh(first_file_path)

                # Add navigation controls in toolbar
                self.main_window.visualization_manager.add_deformed_mesh_controls(
                    neu_files, working_directory, self._smart_load_callback
                )

                # Start preloading other files in background (starting from index 1)
                if len(neu_files) > 1:
                    self.preloader_manager.start_preloading(
                        neu_files, working_directory, first_file_loaded_index=1
                    )
                else:
                    if hasattr(self.main_window.visualization_manager, 'toolbar_manager'):
                        self.main_window.visualization_manager.toolbar_manager.enable_auto_scale_after_loading()

                self.main_window.visualization_manager.reset_view()

            except Exception as e:
                QMessageBox.critical(
                    self.main_window,
                    "Error",
                    f"Error searching for files: {str(e)}"
                )
        else:
            QMessageBox.warning(
                self.main_window,
                "Working Directory Not Set",
                "Please first set a working directory via File > Set Working Directory."
            )
