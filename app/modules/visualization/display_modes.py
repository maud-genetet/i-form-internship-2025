# -*- coding: utf-8 -*-
"""
Module de gestion des modes d'affichage (normal, wireframe, variables)
"""


class DisplayModeManager:
    """
    Gestionnaire des différents modes d'affichage
    """
    
    def __init__(self):
        self.wireframe_mode = False
    
    def set_wireframe_mode(self, enabled):
        """Active/désactive le mode wireframe"""
        self.wireframe_mode = enabled
    
    def display_mesh(self, plotter, mesh, mesh_color, edge_color, show_edges=True):
        """Affiche le mesh principal selon le mode courant"""
        if self.wireframe_mode:
            # Mode wireframe: seulement les arêtes
            plotter.add_mesh(
                mesh,
                style='wireframe', 
                color=edge_color,
                line_width=1,
                label="Maillage - Wireframe"
            )
        else:
            # Mode normal: mesh opaque avec edges
            plotter.add_mesh(
                mesh,
                show_edges=show_edges,
                edge_color=edge_color,
                line_width=1,
                color=mesh_color,
                opacity=1.0,
                label="Maillage"
            )
    
    def display_die(self, plotter, die_mesh, die_id):
        """Affiche un die selon le mode courant"""
        if self.wireframe_mode:
            # Mode wireframe: seulement les contours
            plotter.add_mesh(
                die_mesh,
                style='wireframe',
                color='red',
                line_width=1,
                label=f"Die {die_id} - Wireframe"
            )
        else:
            # Mode normal: die opaque
            plotter.add_mesh(
                die_mesh,
                color='lightgrey',
                opacity=1.0,
                show_edges=True,
                edge_color='black',
                line_width=1,
                label=f"Die {die_id}"
            )
    
    def display_variable(self, plotter, mesh, scalar_name, variable_name, edge_color):
        """Affiche les variables selon le mode courant"""
        plotter.add_mesh(
            mesh,
            scalars=scalar_name,
            show_edges=True,
            edge_color=edge_color,
            line_width=1,
            opacity=1.0,
            cmap='turbo',  # Colormap avec plus de couleurs
            show_scalar_bar=True,
            label=f"Maillage - {variable_name}"
        )