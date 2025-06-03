# -*- coding: utf-8 -*-
"""
Module de gestion des interactions utilisateur (zoom au clic, raccourcis clavier)
"""

import numpy as np


class InteractionHandler:
    """
    Gestionnaire des interactions utilisateur avec la visualisation
    """
    
    def __init__(self):
        self.zoom_speed = 1.5
        self.plotter = None
    
    def setup(self, plotter):
        """Configure les interactions sur le plotter"""
        self.plotter = plotter
        self._setup_keyboard_shortcuts()
    
    def _setup_keyboard_shortcuts(self):
        """Configure les raccourcis clavier"""
        try:
            self.plotter.add_key_event('plus', self._zoom_in_custom)
            self.plotter.add_key_event('minus', self._zoom_out_custom)
            self.plotter.add_key_event('r', self._reset_view_custom)
            
        except Exception as e:
            print(f"⚠️ Erreur configuration raccourcis: {e}")
    
    def _zoom_in_custom(self):
        """Zoom in avec raccourci"""
        self.plotter.camera.zoom(self.zoom_speed)
        self.plotter.render()
    
    def _zoom_out_custom(self):
        """Zoom out avec raccourci"""
        self.plotter.camera.zoom(1.0 / self.zoom_speed)
        self.plotter.render()
    
    def _reset_view_custom(self):
        """Reset vue avec raccourci"""
        self.plotter.reset_camera()
        self.plotter.view_xy()
    
    def set_front_view(self):
        """Met la vue de face (XY plane) en gardant le zoom"""
        if self.plotter:
            # Sauvegarder la position actuelle de la caméra
            camera = self.plotter.camera
            current_position = camera.position
            current_focal_point = camera.focal_point
            
            # Calculer la distance actuelle (pour garder le zoom)
            current_distance = np.linalg.norm(
                np.array(current_position) - np.array(current_focal_point)
            )
            
            # Nouvelle position: au-dessus du focal point à la même distance
            new_position = [
                current_focal_point[0],
                current_focal_point[1],
                current_focal_point[2] + current_distance
            ]
            
            # Appliquer la vue de face
            camera.position = new_position
            camera.focal_point = current_focal_point
            camera.view_up = [0, 1, 0]  # Y vers le haut
            
            self.plotter.render()
            print("Vue de face activée (zoom conservé)")
    
    def enable_click_tracking(self, plotter):
        """Active le suivi des clics pour le zoom"""
        try:
            # Tracking de la position des clics
            if hasattr(plotter, 'track_click_position'):
                plotter.track_click_position(self._on_click_callback)
            else:
                # Méthode alternative avec les événements VTK
                plotter.iren.AddObserver('LeftButtonPressEvent', self._on_left_click)
                
        except Exception as e:
            print(f"Erreur activation zoom au clic: {e}")
    
    def _on_click_callback(self, point):
        """Callback appelé lors d'un clic avec track_click_position"""
        if point is not None:
            print(f"Clic en: {point}")
            self.zoom_to_point_coordinates(point)
    
    def _on_left_click(self, obj, event):
        """Callback alternatif pour les clics (méthode VTK)"""
        try:
            # Récupération de la position du clic
            iren = self.plotter.iren
            x, y = iren.GetEventPosition()
            
            # Conversion en coordonnées monde
            picker = self.plotter.picker
            if picker.Pick(x, y, 0, self.plotter.renderer):
                world_pos = picker.GetPickPosition()
                print(f"Clic détecté en: {world_pos}")
                self.zoom_to_point_coordinates(world_pos)
            
        except Exception as e:
            print(f"Erreur lors du clic: {e}")
    
    def zoom_to_point_coordinates(self, target_point):
        """Zoom vers un point spécifique en coordonnées 3D"""
        if not target_point or len(target_point) < 2:
            return
        
        try:
            camera = self.plotter.camera
            current_pos = np.array(camera.position)
            target_pos = np.array([target_point[0], target_point[1], target_point[2] if len(target_point) > 2 else 0])
            
            # Calcul de la nouvelle position de la caméra
            direction = target_pos - current_pos
            zoom_factor = 1.0 / self.zoom_speed
            new_pos = current_pos + direction * (1 - zoom_factor)
            
            # Mise à jour de la caméra
            camera.position = new_pos
            camera.focal_point = target_pos
            
            # Rendu
            self.plotter.render()
            
        except Exception as e:
            print(f"Erreur lors du zoom vers point: {e}")