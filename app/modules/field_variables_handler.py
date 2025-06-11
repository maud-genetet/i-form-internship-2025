# -*- coding: utf-8 -*-
"""
Gestionnaire du menu Field Variables
Gère l'affichage des différentes variables sur le maillage
"""

from PyQt5.QtWidgets import QMessageBox


class FieldVariablesHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.current_variable = None
        
        # Mapping entre les noms de méthodes et les clés du mesh
        self.variable_mapping = {
            # VELOCITY (pas dans MeshBuilder mais on garde la structure)
            "Velocity_X": "Velocity X(r)",
            "Velocity_Y": "Velocity Y(z)",
            "Total_Velocity": "Total Velocity",
            
            # FORCE (pas dans MeshBuilder mais on garde la structure)
            "Force_X": "Force X(r)",
            "Force_Y": "Force Y(z)",
            "Total_Force": "Total Force",
            
            # TEMPERATURE (pas dans MeshBuilder mais on garde la structure)
            "Temperature_Rate": "Temperature Rate",
            "Temperature": "Temperature",
            
            # STRAIN RATE - Correspondance avec MeshBuilder
            "Strain_Rate_X": "Strain rate x(r)",
            "Strain_Rate_Y": "Strain rate y(z)",
            "Strain_Rate_Z": "Strain rate z(theta)",
            "Strain_Rate_XY": "Strain rate xy(rz)",
            "Effective_Strain_Rate": "Effective strain rate",
            
            # STRAIN - Correspondance avec MeshBuilder
            "Deformation_XX": "Strain x(r)",
            "Deformation_YY": "Strain y(z)",
            "Deformation_ZZ": "Strain z(theta)",
            "Deformation_XY": "Strain xy(rz)",
            "Deformation": "Effective strain",
            "Volumetric_Strain": "Volumetric Strain",  # Pas dans MeshBuilder
            "Strain_1": "Strain 1",
            "Strain_2": "Strain 2",  # Pas dans MeshBuilder
            "Strain_3": "Strain 3",
            
            # STRESS - Correspondance avec MeshBuilder
            "Stress_X": "Stress x(r)",
            "Stress_Y": "Stress y(z)",
            "Stress_ZZ": "Stress z(theta)",
            "Stress_XY": "Stress xy(rz)",
            "Contrainte": "Effective stress",
            "Average_Stress": "Average stress",
            "Stress_1": "Stress 1",  # Pas dans MeshBuilder
            "Stress_2": "Stress 2",  # Pas dans MeshBuilder
            "Stress_3": "Stress 3",  # Pas dans MeshBuilder
        }
        
    def get_visualization_manager(self):
        """Récupère le gestionnaire de visualisation"""
        return self.main_window.visualization_manager
    
    def _apply_variable_to_mesh(self, variable_key, display_name):
        """Applique une variable au mesh actuel"""
        visualization_manager = self.get_visualization_manager()
        
        if not visualization_manager.current_mesh:
            QMessageBox.warning(
                self.main_window,
                "Aucun maillage",
                "Veuillez d'abord charger un maillage."
            )
            return
        
        mesh = visualization_manager.current_mesh
        
        # Vérifier si la variable existe dans le mesh
        if variable_key not in mesh.cell_data:
            # Essayer de trouver une correspondance dans le mapping
            mesh_key = self.variable_mapping.get(variable_key, variable_key)
            if mesh_key not in mesh.cell_data:
                # Lister les variables disponibles pour le debug
                available_vars = list(mesh.cell_data.keys())
                print(f"Variables disponibles dans le mesh: {available_vars}")
                
                QMessageBox.information(
                    self.main_window,
                    "Variable non disponible",
                    f"La variable '{display_name}' n'est pas disponible pour ce maillage.\n"
                    f"Variables disponibles: {', '.join(available_vars[:5])}{'...' if len(available_vars) > 5 else ''}"
                )
                return
            variable_key = mesh_key
        
        # Effacer la visualisation actuelle
        visualization_manager.clear()
        
        # Afficher le mesh avec la variable
        visualization_manager.display_manager.display_variable(
            visualization_manager.plotter, 
            mesh, 
            variable_key, 
            display_name,
            visualization_manager.default_edge_color
        )
        
        # Ajouter les dies après l'affichage de la variable
        visualization_manager._add_dies_to_plot()
        
        # Mémoriser la variable actuelle
        self.current_variable = variable_key
        
        print(f"Variable affichée: {display_name} (clé: {variable_key})")
        
        # Forcer le rendu
        visualization_manager.plotter.render()
    
    def _show_geometry_only(self):
        """Affiche seulement la géométrie sans variables"""
        visualization_manager = self.get_visualization_manager()
        
        if not visualization_manager.current_data:
            QMessageBox.warning(
                self.main_window,
                "Aucune donnée",
                "Veuillez d'abord charger un maillage."
            )
            return
        
        # Relancer la visualisation normale du mesh (avec dies)
        visualization_manager.visualize_mesh(show_edges=True, show_nodes=False, show_dies=True)
        self.current_variable = None
        print("Affichage géométrie seule (avec dies)")
    
    def reapply_current_variable(self):
        """Réapplique la variable actuellement sélectionnée (utile lors du changement de fichier)"""
        if self.current_variable:
            # Trouver le nom d'affichage correspondant en inversant le mapping
            display_name = None
            for key, mesh_key in self.variable_mapping.items():
                if mesh_key == self.current_variable:
                    display_name = mesh_key
                    break
            
            if not display_name:
                display_name = self.current_variable
            
            print(f"Réapplication de la variable: {display_name}")
            self._apply_variable_to_mesh(self.current_variable, display_name)
        else:
            # Afficher la géométrie seule
            self._show_geometry_only()
    
    def get_available_variables(self):
        """Retourne la liste des variables disponibles dans le mesh actuel"""
        visualization_manager = self.get_visualization_manager()
        if visualization_manager.current_mesh:
            return list(visualization_manager.current_mesh.cell_data.keys())
        return []
    
    # === STANDARD OPTIONS ===
    def standard_options(self):
        """Options standard - affiche la géométrie seule"""
        self._show_geometry_only()
    
    # === VELOCITY ===
    def velocity_x_r(self):
        """Affiche la vitesse X (ou r en coordonnées cylindriques)"""
        self._apply_variable_to_mesh("Velocity_X", "Velocity X(r)")
    
    def velocity_y_z(self):
        """Affiche la vitesse Y (ou z en coordonnées cylindriques)"""
        self._apply_variable_to_mesh("Velocity_Y", "Velocity Y(z)")
    
    def total_velocity(self):
        """Affiche la vitesse totale"""
        self._apply_variable_to_mesh("Total_Velocity", "Total Velocity")
    
    # === FORCE ===
    def force_x_r(self):
        """Affiche la force X (ou r)"""
        self._apply_variable_to_mesh("Force_X", "Force X(r)")
    
    def force_y_z(self):
        """Affiche la force Y (ou z)"""
        self._apply_variable_to_mesh("Force_Y", "Force Y(z)")
    
    def total_force(self):
        """Affiche la force totale"""
        self._apply_variable_to_mesh("Total_Force", "Total Force")
    
    # === TEMPERATURE ===
    def temperature_rate(self):
        """Affiche le taux de température"""
        self._apply_variable_to_mesh("Temperature_Rate", "Temperature Rate")
    
    def temperature(self):
        """Affiche la température"""
        self._apply_variable_to_mesh("Temperature", "Temperature")
    
    # === STRAIN RATE ===
    def strain_rate_x_r(self):
        """Affiche le taux de déformation X (r)"""
        self._apply_variable_to_mesh("Strain rate x(r)", "Strain Rate X(r)")
    
    def strain_rate_y_z(self):
        """Affiche le taux de déformation Y (z)"""
        self._apply_variable_to_mesh("Strain rate y(z)", "Strain Rate Y(z)")
    
    def strain_rate_z_theta(self):
        """Affiche le taux de déformation Z (theta)"""
        self._apply_variable_to_mesh("Strain rate z(theta)", "Strain Rate Z(theta)")
    
    def strain_rate_xy_rz(self):
        """Affiche le taux de déformation XY (rz)"""
        self._apply_variable_to_mesh("Strain rate xy(rz)", "Strain Rate XY(rz)")
    
    def effective_strain_rate(self):
        """Affiche le taux de déformation effectif"""
        self._apply_variable_to_mesh("Effective strain rate", "Effective Strain Rate")
    
    # === STRAIN ===
    def strain_x_r(self):
        """Affiche la déformation X (r)"""
        self._apply_variable_to_mesh("Strain x(r)", "Strain X(r)")
    
    def strain_y_z(self):
        """Affiche la déformation Y (z)"""
        self._apply_variable_to_mesh("Strain y(z)", "Strain Y(z)")
    
    def strain_z_theta(self):
        """Affiche la déformation Z (theta)"""
        self._apply_variable_to_mesh("Strain z(theta)", "Strain Z(theta)")
    
    def strain_xy_rz(self):
        """Affiche la déformation XY (rz)"""
        self._apply_variable_to_mesh("Strain xy(rz)", "Strain XY(rz)")
    
    def effective_strain(self):
        """Affiche la déformation effective"""
        self._apply_variable_to_mesh("Effective strain", "Effective Strain")
    
    def volumetric_strain(self):
        """Affiche la déformation volumétrique"""
        self._apply_variable_to_mesh("Volumetric_Strain", "Volumetric Strain")
    
    def strain_1(self):
        """Affiche la déformation principale 1"""
        self._apply_variable_to_mesh("Strain 1", "Strain 1")
    
    def strain_2(self):
        """Affiche la déformation principale 2"""
        self._apply_variable_to_mesh("Strain_2", "Strain 2")
    
    def strain_3(self):
        """Affiche la déformation principale 3"""
        self._apply_variable_to_mesh("Strain 3", "Strain 3")
    
    # === STRESS ===
    def stress_x_r(self):
        """Affiche la contrainte X (r)"""
        self._apply_variable_to_mesh("Stress x(r)", "Stress X(r)")
    
    def stress_y_z(self):
        """Affiche la contrainte Y (z)"""
        self._apply_variable_to_mesh("Stress y(z)", "Stress Y(z)")
    
    def stress_z_theta(self):
        """Affiche la contrainte Z (theta)"""
        self._apply_variable_to_mesh("Stress z(theta)", "Stress Z(theta)")
    
    def stress_xy_rz(self):
        """Affiche la contrainte XY (rz)"""
        self._apply_variable_to_mesh("Stress xy(rz)", "Stress XY(rz)")
    
    def effective_stress(self):
        """Affiche la contrainte effective"""
        self._apply_variable_to_mesh("Effective stress", "Effective Stress")
    
    def average_stress(self):
        """Affiche la contrainte moyenne"""
        self._apply_variable_to_mesh("Average stress", "Average Stress")
    
    def stress_1(self):
        """Affiche la contrainte principale 1"""
        self._apply_variable_to_mesh("Stress_1", "Stress 1")
    
    def stress_2(self):
        """Affiche la contrainte principale 2"""
        self._apply_variable_to_mesh("Stress_2", "Stress 2")
    
    def stress_3(self):
        """Affiche la contrainte principale 3"""
        self._apply_variable_to_mesh("Stress_3", "Stress 3")
    
    # === MÉTHODES UTILITAIRES ===
    def list_available_variables(self):
        """Liste toutes les variables disponibles dans le mesh actuel"""
        available = self.get_available_variables()
        if available:
            print("Variables disponibles dans le mesh:")
            for var in sorted(available):
                print(f"  - {var}")
        else:
            print("Aucun mesh chargé ou aucune variable disponible")
        return available
    
    def debug_mesh_data(self):
        """Affiche des informations de debug sur le mesh actuel"""
        visualization_manager = self.get_visualization_manager()
        if not visualization_manager.current_mesh:
            print("Aucun mesh chargé")
            return
        
        mesh = visualization_manager.current_mesh
        print(f"\n=== DEBUG MESH ===")
        print(f"Nombre de cellules: {mesh.n_cells}")
        print(f"Nombre de points: {mesh.n_points}")
        print(f"Variables disponibles ({len(mesh.cell_data)}):")
        
        for key, data in mesh.cell_data.items():
            if hasattr(data, 'shape'):
                print(f"  - {key}: {data.shape} (min: {data.min():.3f}, max: {data.max():.3f})")
            else:
                print(f"  - {key}: {type(data)}")
        print("===================\n")