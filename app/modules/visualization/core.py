# -*- coding: utf-8 -*-
"""
Module principal de visualisation - Configuration et contrôles principaux
"""

import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QCheckBox, QSpinBox)
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
        
        # Contrôles pour maillage déformé (cachés par défaut)
        self.deformed_controls_layout = QHBoxLayout()
        
        # Bouton précédent
        self.prev_mesh_btn = QPushButton("◀")
        self.prev_mesh_btn.setMaximumWidth(30)
        self.prev_mesh_btn.clicked.connect(self._previous_mesh)
        self.prev_mesh_btn.setVisible(False)
        self.deformed_controls_layout.addWidget(self.prev_mesh_btn)
        
        # SpinBox pour sélection directe
        self.mesh_spinbox = QSpinBox()
        self.mesh_spinbox.setMinimumWidth(50)
        self.mesh_spinbox.setMaximumWidth(60)
        self.mesh_spinbox.valueChanged.connect(self._on_mesh_spinbox_changed)
        self.mesh_spinbox.setVisible(False)
        self.deformed_controls_layout.addWidget(self.mesh_spinbox)
        
        # Bouton suivant
        self.next_mesh_btn = QPushButton("▶")
        self.next_mesh_btn.setMaximumWidth(30)
        self.next_mesh_btn.clicked.connect(self._next_mesh)
        self.next_mesh_btn.setVisible(False)
        self.deformed_controls_layout.addWidget(self.next_mesh_btn)
        
        # Variables pour le maillage déformé
        self.neu_files = []
        self.working_directory = None
        self.load_mesh_callback = None
        self.current_mesh_index = 0
        
        toolbar_layout.addLayout(self.deformed_controls_layout)
        
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
    
    # === MÉTHODES POUR MAILLAGE DÉFORMÉ ===
    
    def add_deformed_mesh_controls(self, neu_files, working_directory, load_callback):
        """Ajoute les contrôles de navigation pour le maillage déformé"""
        self.neu_files = neu_files
        self.working_directory = working_directory
        self.load_mesh_callback = load_callback
        self.current_mesh_index = 0
        
        # Configurer le spinbox
        self.mesh_spinbox.setMinimum(1)
        self.mesh_spinbox.setMaximum(len(neu_files))
        self.mesh_spinbox.setValue(1)
        
        # Afficher les contrôles
        self.prev_mesh_btn.setVisible(True)
        self.mesh_spinbox.setVisible(True)
        self.next_mesh_btn.setVisible(True)
        
        # Mettre à jour l'état des boutons
        self._update_mesh_controls_state()
        
    def hide_deformed_mesh_controls(self):
        """Cache les contrôles de navigation du maillage déformé"""
        self.prev_mesh_btn.setVisible(False)
        self.mesh_spinbox.setVisible(False)
        self.next_mesh_btn.setVisible(False)
    
    def _previous_mesh(self):
        """Charge le fichier de maillage précédent"""
        if self.current_mesh_index > 0:
            self.current_mesh_index -= 1
            self._load_current_mesh()
            self._update_mesh_controls_state()
    
    def _next_mesh(self):
        """Charge le fichier de maillage suivant"""
        if self.current_mesh_index < len(self.neu_files) - 1:
            self.current_mesh_index += 1
            self._load_current_mesh()
            self._update_mesh_controls_state()
    
    def _on_mesh_spinbox_changed(self, value):
        """Callback pour le changement de valeur du spinbox"""
        new_index = value - 1  # Conversion 1-based vers 0-based
        if 0 <= new_index < len(self.neu_files):
            self.current_mesh_index = new_index
            self._load_current_mesh()
            self._update_mesh_controls_state()
    
    def _load_current_mesh(self):
        """Charge le fichier de maillage actuel"""
        if self.neu_files and self.working_directory and self.load_mesh_callback:
            current_file = self.neu_files[self.current_mesh_index]
            file_path = f"{self.working_directory}/{current_file}"
            print(f"Chargement du fichier {self.current_mesh_index + 1}/{len(self.neu_files)}: {current_file}")
            self.load_mesh_callback(file_path)
    
    def _update_mesh_controls_state(self):
        """Met à jour l'état des contrôles de navigation"""
        # Boutons précédent/suivant
        self.prev_mesh_btn.setEnabled(self.current_mesh_index > 0)
        self.next_mesh_btn.setEnabled(self.current_mesh_index < len(self.neu_files) - 1)
        
        # SpinBox (bloquer les signaux pour éviter la récursion)
        self.mesh_spinbox.blockSignals(True)
        self.mesh_spinbox.setValue(self.current_mesh_index + 1)
        self.mesh_spinbox.blockSignals(False)
    
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
        
        # Visualiser le maillage avec dies
        self.visualize_mesh(show_edges=True, show_nodes=False, show_dies=True)
        
        # Réappliquer la variable actuellement sélectionnée si elle existe
        if hasattr(self.main_window, 'field_variables_handler'):
            self.main_window.field_variables_handler.reapply_current_variable()

    def set_working_directory(self, dir_name):
        """Définit le répertoire de travail"""
        self.current_dir = dir_name
    
    def visualize_mesh(self, show_edges=True, show_nodes=False, show_dies=True):
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

        except Exception as e:
            print(f"Erreur lors de la visualisation: {e}")
        
        # Forcer le rendu pour s'assurer que tout est affiché
        if self.plotter:
            self.plotter.render()
    
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
        
        if not dies:
            print("Aucun die trouvé dans les données")
            return
        
        print(f"Affichage de {len(dies)} die(s)")
        
        for i, die in enumerate(dies):
            try:
                die_mesh = self.mesh_builder.create_die_mesh(die)
                if die_mesh:
                    self.display_manager.display_die(
                        self.plotter, die_mesh, die.get_id()
                    )
                    print(f"Die {die.get_id()} ajouté")
                else:
                    print(f"Impossible de créer le mesh pour le die {die.get_id()}")
            except Exception as e:
                print(f"Erreur lors de l'ajout du die {i}: {e}")
    
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