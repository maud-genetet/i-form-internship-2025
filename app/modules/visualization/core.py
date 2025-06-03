# -*- coding: utf-8 -*-
"""
Module principal de visualisation - Configuration et contrôles principaux
"""

import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QComboBox, QCheckBox)
from pyvistaqt import QtInteractor
import pyvista as pv

try:
    from .mesh_builder import MeshBuilder
    from .interaction_handler import InteractionHandler
    from .display_modes import DisplayModeManager
except ImportError:
    # Fallback pour import direct
    from modules.visualization.mesh_builder import MeshBuilder
    from modules.visualization.interaction_handler import InteractionHandler
    from modules.visualization.display_modes import DisplayModeManager


class VisualizationManager:
    """
    Gestionnaire centralisé pour la visualisation PyVista
    Partagé entre tous les modules de l'application
    """
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.plotter = None
        self.visualization_widget = None
        self.current_data = None
        self.current_dir = None
        self.current_mesh = None
        
        # Configuration par défaut
        self.default_mesh_color = 'yellow'
        self.default_edge_color = 'black'
        self.default_node_color = 'black'
        
        # Modules spécialisés
        self.mesh_builder = MeshBuilder()
        self.interaction_handler = InteractionHandler()
        self.display_manager = DisplayModeManager()
        
        self._setup_visualization_widget()
    
    def _setup_visualization_widget(self):
        """Configure le widget de visualisation principal"""
        self.visualization_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Barre d'outils
        self._create_toolbar(main_layout)
        
        # Zone de visualisation PyVista
        self.plotter = QtInteractor(self.visualization_widget)
        main_layout.addWidget(self.plotter.interactor)
        
        self.visualization_widget.setLayout(main_layout)
        
        # Configuration du plotter
        self._configure_plotter()
    
    def _configure_plotter(self):
        """Configure le plotter avec zoom au clic automatique"""
        self.plotter.show_axes()
        self.plotter.view_xy()
        
        # Initialisation du gestionnaire d'interactions
        self.interaction_handler.setup(self.plotter)
    
    def _create_toolbar(self, main_layout):
        """Crée la barre d'outils de contrôle"""
        toolbar_layout = QHBoxLayout()
        
        # Informations sur les données
        self.data_info_label = QLabel("No data")
        toolbar_layout.addWidget(self.data_info_label)
        
        toolbar_layout.addStretch()
        
        # Sélecteur de variable
        self.variable_combo = QComboBox()
        self.variable_combo.addItems([
            "Géométrie", "Contrainte", "Déformation", 
            "Vitesse", "Force", "Température"
        ])
        self.variable_combo.currentTextChanged.connect(self._on_variable_changed)
        toolbar_layout.addWidget(QLabel("Afficher:"))
        toolbar_layout.addWidget(self.variable_combo)

        # Checkbox wireframe
        self.wireframe_checkbox = QCheckBox("Wireframe")
        self.wireframe_checkbox.toggled.connect(self._on_wireframe_toggled)
        toolbar_layout.addWidget(self.wireframe_checkbox)
        
        # Boutons de contrôle
        reset_btn = QPushButton("Reset Vue")
        reset_btn.clicked.connect(self.reset_view)
        toolbar_layout.addWidget(reset_btn)
        
        # Bouton vue de face
        front_view_btn = QPushButton("Vue Face")
        front_view_btn.clicked.connect(self.set_front_view)
        toolbar_layout.addWidget(front_view_btn)
        
        clear_btn = QPushButton("Effacer")
        clear_btn.clicked.connect(self.clear)
        toolbar_layout.addWidget(clear_btn)
        
        # Assemblage
        toolbar_widget = QWidget()
        toolbar_widget.setLayout(toolbar_layout)
        toolbar_widget.setMaximumHeight(40)
        main_layout.addWidget(toolbar_widget)
    
    def _on_wireframe_toggled(self, checked):
        """Callback pour le mode wireframe"""
        self.display_manager.set_wireframe_mode(checked)
        print(f"Mode wireframe: {'ON' if checked else 'OFF'}")
        
        if self.current_data:
            self.visualize_mesh()
    
    def _on_variable_changed(self, variable_name):
        """Callback pour changement de variable"""
        self._apply_current_variable()
    
    # === MÉTHODES PUBLIQUES ===
    
    def get_widget(self):
        """Retourne le widget de visualisation"""
        return self.visualization_widget
    
    def set_as_central_widget(self):
        """Définit comme widget central"""
        self.main_window.setCentralWidget(self.visualization_widget)
    
    def load_neutral_file(self, neutral_file):
        """Charge un fichier neutral pour visualisation"""
        self.current_data = neutral_file
        self._update_data_info()
        self.visualize_mesh()
        # Activation automatique du zoom au clic
        self.interaction_handler.enable_click_tracking(self.plotter)

    def set_working_directory(self, dir_name):
        """Définit le répertoire de travail"""
        self.current_dir = dir_name
    
    def visualize_mesh(self, show_edges=True, show_nodes=True, show_dies=True):
        """Visualise le maillage avec les options spécifiées"""
        if not self.current_data:
            return
        
        self.clear()
        
        try:
            # Création du mesh via le builder
            mesh = self.mesh_builder.create_pyvista_mesh(self.current_data)
            if mesh:
                self.current_mesh = mesh
                
                # Affichage selon le mode
                self.display_manager.display_mesh(
                    self.plotter, mesh, 
                    self.default_mesh_color, self.default_edge_color,
                    show_edges
                )
                
                # Éléments additionnels
                if show_nodes:
                    self._add_nodes_to_plot()
                
                if show_dies:
                    self._add_dies_to_plot()
                
                # Application de la variable sélectionnée
                self._apply_current_variable()
                
        except Exception as e:
            print(f"Erreur lors de la visualisation: {e}")
    
    def _update_data_info(self):
        """Met à jour les informations affichées"""
        if self.current_data and self.current_dir:
            info = (f"Directory: {self.current_dir} | "
                   f"Nodes: {self.current_data.get_nb_nodes()} | "
                   f"Elements: {self.current_data.get_nb_elements()}")
            self.data_info_label.setText(info)
        elif self.current_dir:
            self.data_info_label.setText(f"Directory: {self.current_dir} | No data loaded")
        else:
            self.data_info_label.setText("No data")
    
    def _add_nodes_to_plot(self):
        """Ajoute les nœuds à la visualisation"""
        if not self.current_data:
            return
        
        nodes = self.current_data.get_nodes()
        points = []
        
        for node in nodes:
            x = node.get_coordX() if node.get_coordX() is not None else 0.0
            y = node.get_coordY() if node.get_coordY() is not None else 0.0
            points.append([x, y, 0.0])
        
        if points:
            points_mesh = pv.PolyData(np.array(points))
            self.plotter.add_mesh(
                points_mesh,
                color=self.default_node_color,
                point_size=3,
                render_points_as_spheres=True,
                label="Node"
            )
    
    def _add_dies_to_plot(self):
        """Ajoute les dies à la visualisation"""
        if not self.current_data:
            return
        
        dies = self.current_data.get_dies()
        
        for i, die in enumerate(dies):
            die_mesh = self.mesh_builder.create_die_mesh(die)
            if die_mesh:
                self.display_manager.display_die(
                    self.plotter, die_mesh, die.get_id()
                )
    
    def _apply_current_variable(self):
        """Applique la variable sélectionnée au mesh"""
        if not self.current_mesh:
            return
        
        variable = self.variable_combo.currentText()
        variable_mapping = {
            'Contrainte': 'Contrainte',
            'Déformation': 'Deformation',
            'Vitesse': 'Vitesse',
            'Force': 'Force',
            'Température': 'Temperature'
        }
        
        if variable in variable_mapping and variable_mapping[variable] in self.current_mesh.cell_data:
            self.display_manager.display_variable(
                self.plotter, self.current_mesh, 
                variable_mapping[variable], variable,
                self.default_edge_color
            )
    
    def clear(self):
        """Efface la visualisation"""
        if self.plotter:
            self.plotter.clear()
    
    def reset_view(self):
        """Remet la vue à zéro"""
        if self.plotter:
            self.plotter.reset_camera()
            self.plotter.view_xy()
    
    def set_front_view(self):
        """Met la vue de face (XY plane) en gardant le zoom actuel"""
        if self.plotter:
            # Sauvegarder la position actuelle de la caméra pour garder le zoom
            camera = self.plotter.camera
            current_position = camera.position
            current_focal_point = camera.focal_point
            
            # Calculer la distance actuelle (pour garder le zoom)
            import numpy as np
            current_distance = np.linalg.norm(
                np.array(current_position) - np.array(current_focal_point)
            )
            
            # Définir la nouvelle orientation (vue de face XY)
            # Position: au-dessus du point focal, regardant vers le bas
            new_position = [
                current_focal_point[0],  # même X que le focal point
                current_focal_point[1],  # même Y que le focal point  
                current_focal_point[2] + current_distance  # Z = focal + distance
            ]
            
            # Appliquer la nouvelle vue
            camera.position = new_position
            camera.focal_point = current_focal_point
            camera.view_up = [0, 1, 0]  # Y vers le haut
            
            # Rendu
            self.plotter.render()
            print("Vue de face activée (zoom conservé)")
    
    def export_image(self, filename):
        """Exporte la vue actuelle en image"""
        if self.plotter:
            self.plotter.screenshot(filename)
    
    def get_current_data(self):
        """Retourne les données actuellement chargées"""
        return self.current_data
    
    def add_custom_mesh(self, mesh, **kwargs):
        """Ajoute un mesh personnalisé à la visualisation"""
        if self.plotter:
            self.plotter.add_mesh(mesh, **kwargs)