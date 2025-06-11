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
        self.plotter = None
    
    def setup(self, plotter):
        """Configure les interactions sur le plotter"""
        self.plotter = plotter
    
    def enable_click_tracking(self, plotter):
        """Active le suivi des clics"""
        try:
            # Tracking de la position des clics
            if hasattr(plotter, 'track_click_position'):
                plotter.track_click_position(self._on_click_callback)
            else:
                # Méthode alternative avec les événements VTK
                plotter.iren.AddObserver('LeftButtonPressEvent', self._on_left_click)
                
        except Exception as e:
            print(f"Erreur activation au clic: {e}")
    
    def _on_click_callback(self, point):
        """Callback appelé lors d'un clic avec track_click_position"""
        if point is not None:
            print(f"Clic en: {point}")
            self.zoom_to_point_coordinates(point)
    
    def _on_left_click(self):
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
            new_pos = current_pos
            
            # Mise à jour de la caméra
            camera.position = new_pos
            camera.focal_point = target_pos
            
            # Rendu
            #self.set_front_view()
            self.plotter.render()
            
            
        except Exception as e:
            print(f"Erreur lors du zoom vers point: {e}")