# -*- coding: utf-8 -*-
"""
Gestionnaire du menu Mesh
Gère toutes les opérations liées au maillage
"""

import os
import sys
from PyQt5.QtWidgets import QMessageBox, QFileDialog

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
        working_directory = None
        if hasattr(self.main_window, 'file_handler') and self.main_window.file_handler.working_directory:
            working_directory = self.main_window.file_handler.working_directory
            print(f"Dir: {working_directory}")
            
            # We search FEM2.NEU
            fem2_path = os.path.join(working_directory, "FEM2.NEU")
            if not os.path.exists(fem2_path):
                raise FileNotFoundError(f"Le fichier {fem2_path} n'existe pas")
            else :
                self._load_and_display_mesh(fem2_path)
            
    
    def _load_and_display_mesh(self, file_path):
        self.current_neutral_file = ParserNeutralFile.parser_file(file_path)
        
        if not self.current_neutral_file:
            QMessageBox.warning(
                self.main_window,
                "Erreur de parsing",
                "Impossible de parser le fichier sélectionné.\n"
                "Vérifiez que le fichier est au bon format .neu"
            )
            return
        
        self.main_window.visualization_manager.load_neutral_file(self.current_neutral_file)    
        self.main_window.visualization_manager.set_as_central_widget()
            
    def deformed_mesh(self):
        """Affiche le maillage déformé"""
        
        # TODO: Implémenter l'affichage du maillage déformé