
"""
Mesh Menu Handler
Manages all mesh-related operations
"""

import os
import sys
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
parser_dir = os.path.join(current_dir, 'parser')
if parser_dir not in sys.path:
    sys.path.append(parser_dir)
from ParserNeutralFile import ParserNeutralFile

class MeshHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.current_neutral_file = None
        
    def initial_mesh(self):
        """Load initial mesh (FEM1.NEU)"""
        working_directory = None
        if hasattr(self.main_window, 'file_handler') and self.main_window.file_handler.working_directory:
            working_directory = self.main_window.file_handler.working_directory
            print(f"Dir: {working_directory}")
            
            # Search for FEM1.NEU
            fem1_path = os.path.join(working_directory, "FEM1.NEU")
            if not os.path.exists(fem1_path):
                raise FileNotFoundError(f"File {fem1_path} does not exist")
            else:
                self._load_and_display_mesh(fem1_path)
    
    def _load_and_display_mesh(self, file_path):
        """Load and display mesh file"""
        self.current_neutral_file = ParserNeutralFile.parser_file(file_path)
        
        if not self.current_neutral_file:
            QMessageBox.warning(
                self.main_window,
                "Parsing Error",
                "Cannot parse selected file.\n"
                "Check that file is in correct .neu format"
            )
            return
        
        self.main_window.visualization_manager.load_neutral_file(self.current_neutral_file)    
        self.main_window.visualization_manager.set_as_central_widget()
        
        # Display loaded filename
        filename = os.path.basename(file_path)
        print(f"Mesh loaded: {filename}")
            
    def deformed_mesh(self):
        """Display deformed mesh"""
        working_directory = None
        if hasattr(self.main_window, 'file_handler') and self.main_window.file_handler.working_directory:
            working_directory = self.main_window.file_handler.working_directory

            # Search for all .NEU files in directory
            try:
                neu_files = [f for f in os.listdir(working_directory) if f.endswith('.NEU')]
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
                
                # Add navigation controls in toolbar
                self.main_window.visualization_manager.add_deformed_mesh_controls(
                    neu_files, working_directory, self._load_and_display_mesh
                )
                
                # Load first file by default
                if neu_files:
                    first_file_path = os.path.join(working_directory, neu_files[0])
                    self._load_and_display_mesh(first_file_path)
                        
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