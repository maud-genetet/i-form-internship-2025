"""
Field Variables Menu Handler 
"""

from PyQt5.QtWidgets import QMessageBox

from modules.visualization_options import VisualizationOptions


class FieldVariablesHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.current_variable = None
        
        # Initialize unified visualization options
        self.viz_options = VisualizationOptions(main_window)
        
        self.variable_mapping = {
            "Velocity_X": "Velocity X(r)",
            "Velocity_Y": "Velocity Y(z)",
            "Total_Velocity": "Total Velocity",
            
            "Force_X": "Force X(r)",
            "Force_Y": "Force Y(z)",
            "Total_Force": "Total Force",
            
            "Temperature_Rate": "Temperature Rate",
            "Temperature": "Temperature",
            
            "Strain_Rate_X": "Strain rate x(r)",
            "Strain_Rate_Y": "Strain rate y(z)",
            "Strain_Rate_Z": "Strain rate z(theta)",
            "Strain_Rate_XY": "Strain rate xy(rz)",
            "Effective_Strain_Rate": "Effective strain rate",
            "Volumetric_Strain_Rate": "Volumetric strain rate",
            
            "Strain_X": "Strain x(r)",
            "Strain_Y": "Strain y(z)",
            "Strain_Z": "Strain z(theta)",
            "Strain_XY": "Strain xy(rz)",
            "Effective_Strain": "Effective strain",
            "Volumetric_Strain": "Volumetric Strain",
            "Strain_1": "Strain 1",
            "Strain_2": "Strain 2",
            "Strain_3": "Strain 3",
            
            "Stress_X": "Stress x(r)",
            "Stress_Y": "Stress y(z)",
            "Stress_ZZ": "Stress z(theta)",
            "Stress_XY": "Stress xy(rz)",
            "Effective_stress": "Effective stress",
            "Average_Stress": "Average stress",
            "Stress_1": "Stress 1",
            "Stress_2": "Stress 2",
            "Stress_3": "Stress 3",
            
            "Thickness_Plane_Stress": "Thickness (Plane Stress)",
            "Relative_Density": "Relative Density",
            "Ductile_Damage": "Ductile Damage",
            
            "Electric_Potential": "Electric Potential",
            "Electric_Current_Density": "Electric Current Density", 
            "Electric_Resistivity": "Electric Resistivity",
            
            "Stress_Y_Ef_Stress": "Stress y(z)/Ef.Stress",
            "Stress_XY_Ef_Stress": "Stress xy(rz)/Ef.Stress",
            "Average_Stress_Ef_Stress": "Average Stress/Ef.Stress",
            "Pressure": "Pressure",
            "Pressure_Ef_Stress": "Pressure/Ef.Stress",
            "Surface_Enlargement_Ratio": "Surface Enlargement Ratio",
            "Element_Quality": "Element Quality",
        }
    
    def get_visualization_manager(self):
        """Get visualization manager"""
        return self.main_window.visualization_manager
    
    def _apply_variable_to_mesh(self, variable_key):
        """Apply variable to current mesh"""
        visualization_manager = self.get_visualization_manager()
        
        if not visualization_manager.current_mesh:
            QMessageBox.warning(self.main_window, "No Mesh", "Please load a mesh first.")
            return
        
        # Resolve variable key
        resolved_key = self._resolve_variable_key(variable_key)
        if not resolved_key:
            return
        
        # Clear and display with all current options
        visualization_manager.clear()
        visualization_manager.display_manager.display_variable_with_options(
            visualization_manager.plotter,
            visualization_manager.current_mesh,
            resolved_key,
            variable_key,
            visualization_manager.default_edge_color,
            self.viz_options.get_current_options()
        )
        
        # Add dies
        visualization_manager._add_dies_to_plot()
        
        self.current_variable = resolved_key
        print(f"Variable displayed: {variable_key}")
        visualization_manager.plotter.render()
        
        # Reapply picking if needed
        visualization_manager.reapply_mesh_picking_if_needed()
    
    def _resolve_variable_key(self, variable_key):
        """Resolve and validate variable key"""
        mesh = self.get_visualization_manager().current_mesh
        
        if variable_key not in mesh.cell_data:
            mesh_key = self.variable_mapping.get(variable_key)
            if mesh_key not in mesh.cell_data:
                available_list = list(mesh.cell_data.keys())
                QMessageBox.information(
                    self.main_window,
                    "Variable Not Available",
                    f"The variable '{variable_key}' is not available.\n"
                    f"Available: {', '.join(available_list[:5])}{'...' if len(available_list) > 5 else ''}"
                )
                return None
            variable_key = mesh_key
        return variable_key
    
    def _show_geometry_only(self):
        """Display only geometry"""
        visualization_manager = self.get_visualization_manager()
        
        if not visualization_manager.current_data:
            QMessageBox.warning(self.main_window, "No Data", "Please load a mesh first.")
            return
        
        # Get current options
        options = self.viz_options.get_current_options()
        show_edges = options['show_mesh_edges']
        show_constraints = options['view_constraints']
        
        # Use enhanced visualize_mesh method with constraints support
        visualization_manager.visualize_mesh(
            show_edges=show_edges, 
            show_nodes=False, 
            show_dies=True,
            show_constraints=show_constraints
        )
        self.current_variable = None
        print("Displaying geometry only")
    
    def reapply_current_variable(self):
        """Reapply current variable with current options"""
        if self.current_variable:
            self._apply_variable_to_mesh(self.current_variable)
        else:
            self._show_geometry_only()
    
    # === STANDARD OPTIONS ===
    def standard_options(self):
        self._show_geometry_only()
    
    # === VELOCITY ===
    def velocity_x_r(self):
        self._apply_variable_to_mesh("Velocity X(r)")
    
    def velocity_y_z(self):
        self._apply_variable_to_mesh("Velocity Y(z)")
    
    def total_velocity(self):
        self._apply_variable_to_mesh("Total Velocity")
    
    # === FORCE ===
    def force_x_r(self):
        self._apply_variable_to_mesh("Force X(r)")
    
    def force_y_z(self):
        self._apply_variable_to_mesh("Force Y(z)")
    
    def total_force(self):
        self._apply_variable_to_mesh("Total Force")
    
    # === TEMPERATURE ===
    def temperature_rate(self):
        self._apply_variable_to_mesh("Temperature Rate")
    
    def temperature(self):
        self._apply_variable_to_mesh("Temperature")
    
    # === STRAIN RATE ===
    def strain_rate_x_r(self):
        self._apply_variable_to_mesh("Strain rate x(r)")
    
    def strain_rate_y_z(self):
        self._apply_variable_to_mesh("Strain rate y(z)")
    
    def strain_rate_z_theta(self):
        self._apply_variable_to_mesh("Strain rate z(theta)")
    
    def strain_rate_xy_rz(self):
        self._apply_variable_to_mesh("Strain rate xy(rz)")
    
    def effective_strain_rate(self):
        self._apply_variable_to_mesh("Effective strain rate")
    
    def volumetric_strain_rate(self):
        self._apply_variable_to_mesh("Volumetric strain rate")
    
    # === STRAIN ===
    def strain_x_r(self):
        self._apply_variable_to_mesh("Strain x(r)")
    
    def strain_y_z(self):
        self._apply_variable_to_mesh("Strain y(z)")
    
    def strain_z_theta(self):
        self._apply_variable_to_mesh("Strain z(theta)")
    
    def strain_xy_rz(self):
        self._apply_variable_to_mesh("Strain xy(rz)")
    
    def effective_strain(self):
        self._apply_variable_to_mesh("Effective strain")
    
    def volumetric_strain(self):
        self._apply_variable_to_mesh("Volumetric Strain")
    
    def strain_1(self):
        self._apply_variable_to_mesh("Strain 1")
    
    def strain_2(self):
        self._apply_variable_to_mesh("Strain 2")
    
    def strain_3(self):
        self._apply_variable_to_mesh("Strain 3")
    
    # === STRESS ===
    def stress_x_r(self):
        self._apply_variable_to_mesh("Stress x(r)")
    
    def stress_y_z(self):
        self._apply_variable_to_mesh("Stress y(z)")
    
    def stress_z_theta(self):
        self._apply_variable_to_mesh("Stress z(theta)")
    
    def stress_xy_rz(self):
        self._apply_variable_to_mesh("Stress xy(rz)")
    
    def effective_stress(self):
        self._apply_variable_to_mesh("Effective stress")
    
    def average_stress(self):
        self._apply_variable_to_mesh("Average stress")
    
    def stress_1(self):
        self._apply_variable_to_mesh("Stress 1")
    
    def stress_2(self):
        self._apply_variable_to_mesh("Stress 2")
    
    def stress_3(self):
        self._apply_variable_to_mesh("Stress 3")
    
    # === MATERIAL PROPERTIES ===
    def thickness_plane_stress(self):
        self._apply_variable_to_mesh("Thickness (Plane Stress)")
    
    def relative_density(self):
        self._apply_variable_to_mesh("Relative Density")
    
    def ductile_damage(self):
        self._apply_variable_to_mesh("Ductile Damage")
    
    # === ELECTRIC ===
    def electric_potential(self):
        self._apply_variable_to_mesh("Electric Potential")
    
    def electric_current_density(self):
        self._apply_variable_to_mesh("Electric Current Density")
    
    def electric_resistivity(self):
        self._apply_variable_to_mesh("Electric Resistivity")
    
    # === SPECIAL OPTIONS ===
    def stress_y_z_ef_stress(self):
        self._apply_variable_to_mesh("Stress y(z)/Ef.Stress")
    
    def stress_xy_rz_ef_stress(self):
        self._apply_variable_to_mesh("Stress xy(rz)/Ef.Stress")
    
    def average_stress_ef_stress(self):
        self._apply_variable_to_mesh("Average Stress/Ef.Stress")
    
    def pressure(self):
        self._apply_variable_to_mesh("Pressure")
    
    def pressure_ef_stress(self):
        self._apply_variable_to_mesh("Pressure/Ef.Stress")
    
    def surface_enlargement_ratio(self):
        self._apply_variable_to_mesh("Surface Enlargement Ratio")
    
    def element_quality(self):
        self._apply_variable_to_mesh("Element Quality")