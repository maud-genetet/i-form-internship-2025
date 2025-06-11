# -*- coding: utf-8 -*-
"""
Gestionnaire du menu Mesh
Gère toutes les opérations liées au maillage
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
        working_directory = None
        if hasattr(self.main_window, 'file_handler') and self.main_window.file_handler.working_directory:
            working_directory = self.main_window.file_handler.working_directory
            print(f"Dir: {working_directory}")
            
            # We search FEM1.NEU
            fem1_path = os.path.join(working_directory, "FEM1.NEU")
            if not os.path.exists(fem1_path):
                raise FileNotFoundError(f"Le fichier {fem1_path} n'existe pas")
            else:
                self._load_and_display_mesh(fem1_path)
    
    def _load_and_display_mesh(self, file_path):
        """Charge et affiche un fichier de maillage"""
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
        
        # Afficher le nom du fichier chargé
        filename = os.path.basename(file_path)
        print(f"Maillage chargé: {filename}")
            
    def deformed_mesh(self):
        """Affiche le maillage déformé"""
        working_directory = None
        if hasattr(self.main_window, 'file_handler') and self.main_window.file_handler.working_directory:
            working_directory = self.main_window.file_handler.working_directory

            # Recherche de tous les fichiers .NEU dans le répertoire
            try:
                neu_files = [f for f in os.listdir(working_directory) if f.endswith('.NEU')]
                number_of_neu_files = len(neu_files)
                
                if number_of_neu_files == 0:
                    QMessageBox.warning(
                        self.main_window,
                        "Aucun fichier trouvé",
                        "Aucun fichier .NEU trouvé dans le répertoire de travail."
                    )
                    return
                
                # Trier les fichiers numériquement (FEM1, FEM2, FEM10, FEM11...)
                def natural_sort_key(filename):
                    """Fonction de tri naturel pour les noms de fichiers avec numéros"""
                    parts = re.split(r'(\d+)', filename)
                    return [int(part) if part.isdigit() else part for part in parts]
                
                neu_files.sort(key=natural_sort_key)
                
                # Ajouter les contrôles de navigation dans la toolbar
                self.main_window.visualization_manager.add_deformed_mesh_controls(
                    neu_files, working_directory, self._load_and_display_mesh
                )
                
                # Charger le premier fichier par défaut
                if neu_files:
                    first_file_path = os.path.join(working_directory, neu_files[0])
                    self._load_and_display_mesh(first_file_path)
                        
            except Exception as e:
                QMessageBox.critical(
                    self.main_window,
                    "Erreur",
                    f"Erreur lors de la recherche des fichiers: {str(e)}"
                )
        else:
            QMessageBox.warning(
                self.main_window,
                "Répertoire de travail non défini",
                "Veuillez d'abord définir un répertoire de travail via File > Set Working Directory."
            )