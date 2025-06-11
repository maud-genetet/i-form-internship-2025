# -*- coding: utf-8 -*-
"""
Gestionnaire du menu File
Gère toutes les opérations liées aux fichiers
"""

from PyQt5.QtWidgets import QFileDialog


class FileHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.working_directory = None
    
    def set_working_directory(self):
        """Définit le répertoire de travail"""
        directory = QFileDialog.getExistingDirectory(
            self.main_window,
            "Sélectionner le répertoire de travail",
            self.working_directory
        )
        if directory:
            self.working_directory = directory
            self.main_window.visualization_manager.set_working_directory(directory)
            self.main_window.visualization_manager._update_data_info()
            
            # Activer le click tracking UNE SEULE FOIS quand on définit le working directory
            visualization_manager = self.main_window.visualization_manager
            visualization_manager.interaction_handler.enable_click_tracking(visualization_manager.plotter)
    
    def print_document(self):
        """Lance l'impression du document actuel"""
        pass
    
    def save_document(self):
        """Sauvegarde le document actuel"""
        # TODO: Implémenter la sauvegarde
        pass
    
    def export_as_dxf(self):
        """Exporte le document au format DXF"""
        # TODO: Implémenter l'export DXF
        filename, _ = QFileDialog.getSaveFileName(
            self.main_window,
            "Exporter en DXF",
            self.working_directory,
            "Fichiers DXF (*.dxf)"
        )
        if filename:
            # TODO: Logique d'export DXF
            pass
    
    def export_as_ascii(self):
        """Exporte le document au format ASCII"""
        # TODO: Implémenter l'export ASCII
        filename, _ = QFileDialog.getSaveFileName(
            self.main_window,
            "Exporter en ASCII",
            self.working_directory,
            "Fichiers texte (*.txt)"
        )
        if filename:
            # TODO: Logique d'export ASCII
            pass
    
    def export_as_rst(self):
        """Exporte le document au format RST"""
        # TODO: Implémenter l'export RST
        filename, _ = QFileDialog.getSaveFileName(
            self.main_window,
            "Exporter en RST",
            self.working_directory,
            "Fichiers RST (*.rst)"
        )
        if filename:
            # TODO: Logique d'export RST
            pass