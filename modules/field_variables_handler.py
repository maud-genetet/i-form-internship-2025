
"""
Field Variables Menu Handler
Manages display of different variables on the mesh
"""

from PyQt5.QtWidgets import QMessageBox


class FieldVariablesHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.current_variable = None
        
        # Mapping between method names and mesh keys
        self.variable_mapping = {
            # VELOCITY (not in MeshBuilder but keeping structure)
            "Velocity_X": "Velocity X(r)",
            "Velocity_Y": "Velocity Y(z)",
            "Total_Velocity": "Total Velocity",
            
            # FORCE (not in MeshBuilder but keeping structure)
            "Force_X": "Force X(r)",
            "Force_Y": "Force Y(z)",
            "Total_Force": "Total Force",
            
            # TEMPERATURE (not in MeshBuilder but keeping structure)
            "Temperature_Rate": "Temperature Rate",
            "Temperature": "Temperature",
            
            # STRAIN RATE - Correspondence with MeshBuilder
            "Strain_Rate_X": "Strain rate x(r)",
            "Strain_Rate_Y": "Strain rate y(z)",
            "Strain_Rate_Z": "Strain rate z(theta)",
            "Strain_Rate_XY": "Strain rate xy(rz)",
            "Effective_Strain_Rate": "Effective strain rate",
            
            # STRAIN - Correspondence with MeshBuilder
            "Deformation_XX": "Strain x(r)",
            "Deformation_YY": "Strain y(z)",
            "Deformation_ZZ": "Strain z(theta)",
            "Deformation_XY": "Strain xy(rz)",
            "Deformation": "Effective strain",
            "Volumetric_Strain": "Volumetric Strain",  # Not in MeshBuilder
            "Strain_1": "Strain 1",
            "Strain_2": "Strain 2",  # Not in MeshBuilder
            "Strain_3": "Strain 3",
            
            # STRESS - Correspondence with MeshBuilder
            "Stress_X": "Stress x(r)",
            "Stress_Y": "Stress y(z)",
            "Stress_ZZ": "Stress z(theta)",
            "Stress_XY": "Stress xy(rz)",
            "Contrainte": "Effective stress",
            "Average_Stress": "Average stress",
            "Stress_1": "Stress 1",  # Not in MeshBuilder
            "Stress_2": "Stress 2",  # Not in MeshBuilder
            "Stress_3": "Stress 3",  # Not in MeshBuilder
        }
        
    def get_visualization_manager(self):
        """Get visualization manager"""
        return self.main_window.visualization_manager
    
    def _apply_variable_to_mesh(self, variable_key, display_name):
        """Apply variable to current mesh"""
        visualization_manager = self.get_visualization_manager()
        
        if not visualization_manager.current_mesh:
            QMessageBox.warning(
                self.main_window,
                "No Mesh",
                "Please load a mesh first."
            )
            return
        
        mesh = visualization_manager.current_mesh
        
        # Check if variable exists in mesh
        if variable_key not in mesh.cell_data:
            # Try to find correspondence in mapping
            mesh_key = self.variable_mapping.get(variable_key, variable_key)
            if mesh_key not in mesh.cell_data:
                # List available variables for debug
                available_vars = list(mesh.cell_data.keys())
                print(f"Available variables in mesh: {available_vars}")
                
                QMessageBox.information(
                    self.main_window,
                    "Variable Not Available",
                    f"The variable '{display_name}' is not available for this mesh.\n"
                    f"Available variables: {', '.join(available_vars[:5])}{'...' if len(available_vars) > 5 else ''}"
                )
                return
            variable_key = mesh_key
        
        # Clear current visualization
        visualization_manager.clear()
        
        # Display mesh with variable
        visualization_manager.display_manager.display_variable(
            visualization_manager.plotter, 
            mesh, 
            variable_key, 
            display_name,
            visualization_manager.default_edge_color
        )
        
        # Add dies after variable display
        visualization_manager._add_dies_to_plot()
        
        # Store current variable
        self.current_variable = variable_key
        
        print(f"Variable displayed: {display_name} (key: {variable_key})")
        
        # Force rendering
        visualization_manager.plotter.render()
    
    def _show_geometry_only(self):
        """Display only geometry without variables"""
        visualization_manager = self.get_visualization_manager()
        
        if not visualization_manager.current_data:
            QMessageBox.warning(
                self.main_window,
                "No Data",
                "Please load a mesh first."
            )
            return
        
        # Restart normal mesh visualization (with dies)
        visualization_manager.visualize_mesh(show_edges=True, show_nodes=False, show_dies=True)
        self.current_variable = None
        print("Displaying geometry only (with dies)")
    
    def reapply_current_variable(self):
        """Reapply currently selected variable (useful when changing files)"""
        if self.current_variable:
            # Find corresponding display name by inverting mapping
            display_name = None
            for key, mesh_key in self.variable_mapping.items():
                if mesh_key == self.current_variable:
                    display_name = mesh_key
                    break
            
            if not display_name:
                display_name = self.current_variable
            
            print(f"Reapplying variable: {display_name}")
            self._apply_variable_to_mesh(self.current_variable, display_name)
        else:
            # Display geometry only
            self._show_geometry_only()
    
    def get_available_variables(self):
        """Return list of available variables in current mesh"""
        visualization_manager = self.get_visualization_manager()
        if visualization_manager.current_mesh:
            return list(visualization_manager.current_mesh.cell_data.keys())
        return []
    
    # === STANDARD OPTIONS ===
    def standard_options(self):
        """Standard options - display geometry only"""
        self._show_geometry_only()
    
    # === VELOCITY ===
    def velocity_x_r(self):
        """Display velocity X (or r in cylindrical coordinates)"""
        self._apply_variable_to_mesh("Velocity_X", "Velocity X(r)")
    
    def velocity_y_z(self):
        """Display velocity Y (or z in cylindrical coordinates)"""
        self._apply_variable_to_mesh("Velocity_Y", "Velocity Y(z)")
    
    def total_velocity(self):
        """Display total velocity"""
        self._apply_variable_to_mesh("Total_Velocity", "Total Velocity")
    
    # === FORCE ===
    def force_x_r(self):
        """Display force X (or r)"""
        self._apply_variable_to_mesh("Force_X", "Force X(r)")
    
    def force_y_z(self):
        """Display force Y (or z)"""
        self._apply_variable_to_mesh("Force_Y", "Force Y(z)")
    
    def total_force(self):
        """Display total force"""
        self._apply_variable_to_mesh("Total_Force", "Total Force")
    
    # === TEMPERATURE ===
    def temperature_rate(self):
        """Display temperature rate"""
        self._apply_variable_to_mesh("Temperature_Rate", "Temperature Rate")
    
    def temperature(self):
        """Display temperature"""
        self._apply_variable_to_mesh("Temperature", "Temperature")
    
    # === STRAIN RATE ===
    def strain_rate_x_r(self):
        """Display strain rate X (r)"""
        self._apply_variable_to_mesh("Strain rate x(r)", "Strain Rate X(r)")
    
    def strain_rate_y_z(self):
        """Display strain rate Y (z)"""
        self._apply_variable_to_mesh("Strain rate y(z)", "Strain Rate Y(z)")
    
    def strain_rate_z_theta(self):
        """Display strain rate Z (theta)"""
        self._apply_variable_to_mesh("Strain rate z(theta)", "Strain Rate Z(theta)")
    
    def strain_rate_xy_rz(self):
        """Display strain rate XY (rz)"""
        self._apply_variable_to_mesh("Strain rate xy(rz)", "Strain Rate XY(rz)")
    
    def effective_strain_rate(self):
        """Display effective strain rate"""
        self._apply_variable_to_mesh("Effective strain rate", "Effective Strain Rate")
    
    # === STRAIN ===
    def strain_x_r(self):
        """Display strain X (r)"""
        self._apply_variable_to_mesh("Strain x(r)", "Strain X(r)")
    
    def strain_y_z(self):
        """Display strain Y (z)"""
        self._apply_variable_to_mesh("Strain y(z)", "Strain Y(z)")
    
    def strain_z_theta(self):
        """Display strain Z (theta)"""
        self._apply_variable_to_mesh("Strain z(theta)", "Strain Z(theta)")
    
    def strain_xy_rz(self):
        """Display strain XY (rz)"""
        self._apply_variable_to_mesh("Strain xy(rz)", "Strain XY(rz)")
    
    def effective_strain(self):
        """Display effective strain"""
        self._apply_variable_to_mesh("Effective strain", "Effective Strain")
    
    def volumetric_strain(self):
        """Display volumetric strain"""
        self._apply_variable_to_mesh("Volumetric_Strain", "Volumetric Strain")
    
    def strain_1(self):
        """Display principal strain 1"""
        self._apply_variable_to_mesh("Strain 1", "Strain 1")
    
    def strain_2(self):
        """Display principal strain 2"""
        self._apply_variable_to_mesh("Strain_2", "Strain 2")
    
    def strain_3(self):
        """Display principal strain 3"""
        self._apply_variable_to_mesh("Strain 3", "Strain 3")
    
    # === STRESS ===
    def stress_x_r(self):
        """Display stress X (r)"""
        self._apply_variable_to_mesh("Stress x(r)", "Stress X(r)")
    
    def stress_y_z(self):
        """Display stress Y (z)"""
        self._apply_variable_to_mesh("Stress y(z)", "Stress Y(z)")
    
    def stress_z_theta(self):
        """Display stress Z (theta)"""
        self._apply_variable_to_mesh("Stress z(theta)", "Stress Z(theta)")
    
    def stress_xy_rz(self):
        """Display stress XY (rz)"""
        self._apply_variable_to_mesh("Stress xy(rz)", "Stress XY(rz)")
    
    def effective_stress(self):
        """Display effective stress"""
        self._apply_variable_to_mesh("Effective stress", "Effective Stress")
    
    def average_stress(self):
        """Display average stress"""
        self._apply_variable_to_mesh("Average stress", "Average Stress")
    
    def stress_1(self):
        """Display principal stress 1"""
        self._apply_variable_to_mesh("Stress_1", "Stress 1")
    
    def stress_2(self):
        """Display principal stress 2"""
        self._apply_variable_to_mesh("Stress_2", "Stress 2")
    
    def stress_3(self):
        """Display principal stress 3"""
        self._apply_variable_to_mesh("Stress_3", "Stress 3")
    
    # === UTILITY METHODS ===
    def list_available_variables(self):
        """List all available variables in current mesh"""
        available = self.get_available_variables()
        if available:
            print("Available variables in mesh:")
            for var in sorted(available):
                print(f"  - {var}")
        else:
            print("No mesh loaded or no variables available")
        return available
    
    def debug_mesh_data(self):
        """Display debug information about current mesh"""
        visualization_manager = self.get_visualization_manager()
        if not visualization_manager.current_mesh:
            print("No mesh loaded")
            return
        
        mesh = visualization_manager.current_mesh
        print(f"\n=== DEBUG MESH ===")
        print(f"Number of cells: {mesh.n_cells}")
        print(f"Number of points: {mesh.n_points}")
        print(f"Available variables ({len(mesh.cell_data)}):")
        
        for key, data in mesh.cell_data.items():
            if hasattr(data, 'shape'):
                print(f"  - {key}: {data.shape} (min: {data.min():.3f}, max: {data.max():.3f})")
            else:
                print(f"  - {key}: {type(data)}")
        print("===================\n")