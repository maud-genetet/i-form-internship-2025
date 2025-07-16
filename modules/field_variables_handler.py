"""
Field Variables Menu Handler 
"""

from PyQt5.QtWidgets import QMessageBox
import numpy as np

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
        
        # PREPARE EVERYTHING BEFORE CLEARING
        mesh = visualization_manager.current_mesh
        options = self.viz_options.get_current_options()
        
        # Prepare variable mesh
        prepared_meshes = self._prepare_all_meshes_for_display(
            mesh, resolved_key, variable_key, 
            visualization_manager.default_edge_color, options
        )
        
        # Prepare dies
        prepared_dies = self._prepare_dies_for_display(visualization_manager)
        
        # NOW DO EVERYTHING ATOMICALLY
        visualization_manager.clear()
        
        # Add all prepared meshes in one go
        for mesh_data in prepared_meshes:
            visualization_manager.plotter.add_mesh(**mesh_data)
        
        # Add all prepared dies in one go
        for die_data in prepared_dies:
            visualization_manager.plotter.add_mesh(**die_data)
        
        # Single final render
        visualization_manager.plotter.render()
        
        self.current_variable = resolved_key
        
        # Reapply picking if needed
        visualization_manager.reapply_mesh_picking_if_needed()
    
    def _prepare_all_meshes_for_display(self, mesh, scalar_name, variable_name, edge_color, options):
        """Prepare all meshes for atomic display"""
        prepared_meshes = []

        mesh._size_options = {
            'constraint_size_factor': options.get('constraint_size_factor', 1.0),
            'vector_size_factor': options.get('vector_size_factor', 1.0)
        }
        
        # Get options
        wireframe_mode = options.get('wireframe_mode', False)
        show_mesh_edges = options.get('show_mesh_edges', True)
        monochromatic_mode = options.get('monochromatic_mode', False)
        high_definition_contour = options.get('high_definition_contour', False)
        view_constraints = options.get('view_constraints', False)
        line_contour_mode = options.get('line_contour_mode', False)
        vector_mode = options.get('vector_mode', False)
        
        # Apply HD contour if needed
        if high_definition_contour:
            mesh = mesh.cell_data_to_point_data()
        
        # Choose colormap
        cmap = 'Blues' if monochromatic_mode else 'turbo'
        
        # Get scalar data
        if high_definition_contour and scalar_name in mesh.point_data:
            scalars_array = mesh.point_data[scalar_name]
        else:
            scalars_array = mesh.cell_data[scalar_name]
        
        # Prepare main variable mesh
        if vector_mode:
            return self._prepare_vector_meshes(mesh, scalars_array, variable_name, options)
        elif line_contour_mode:
            return self._prepare_line_contour_meshes(mesh, scalars_array, variable_name, cmap, options)
        elif wireframe_mode:
            mesh_data = {
                'mesh': mesh,
                'scalars': scalars_array,
                'show_edges': False,
                'opacity': 1.0,
                'cmap': cmap,
                'show_scalar_bar': True,
                'scalar_bar_args': {'title': variable_name},
                'label': f"Mesh - {variable_name}"
            }
        else:
            mesh_data = {
                'mesh': mesh,
                'scalars': scalars_array,
                'show_edges': show_mesh_edges,
                'edge_color': edge_color if show_mesh_edges else None,
                'line_width': 1,
                'opacity': 1.0,
                'cmap': cmap,
                'show_scalar_bar': True,
                'scalar_bar_args': {'title': variable_name},
                'label': f"Mesh - {variable_name}"
            }
        
        prepared_meshes.append(mesh_data)
    
        return prepared_meshes
    
    def _prepare_vector_meshes(self, mesh, scalars_array, variable_name, options):
        """Prepare meshes for vector display"""
        prepared_meshes = []
        
        # Get options
        show_mesh_edges = options.get('show_mesh_edges', True)
        edge_color = self.get_visualization_manager().default_edge_color
        
        # Add base mesh with transparency
        base_mesh_data = {
            'mesh': mesh,
            'color': 'lightgray',
            'show_edges': show_mesh_edges,
            'edge_color': edge_color if show_mesh_edges else None,
            'line_width': 1,
            'opacity': 0.1,
            'label': "Base Mesh"
        }
        prepared_meshes.append(base_mesh_data)
        
        try:
            vector_mesh_data = self._prepare_vector_field(mesh, scalars_array, variable_name)
            if vector_mesh_data:
                prepared_meshes.append(vector_mesh_data)
        except Exception as e:
            print(f"Error generating vectors: {e}")
            # Fallback to normal display
            fallback_mesh_data = {
                'mesh': mesh,
                'scalars': scalars_array,
                'cmap': 'turbo',
                'show_scalar_bar': True,
                'scalar_bar_args': {'title': variable_name},
                'label': f"Mesh - {variable_name} (fallback)"
            }
            prepared_meshes.append(fallback_mesh_data)
        
        return prepared_meshes

    def _prepare_vector_field(self, mesh, scalars_array, variable_name):
        """Prepare vector field data"""
        try:
            display_manager = self.get_visualization_manager().display_manager
            
            cell_centers = mesh.cell_centers()
            points = cell_centers.points
            vectors = display_manager._calculate_vectors_from_variable(mesh, scalars_array, variable_name)
            
            if vectors is not None and len(vectors) == len(points):
                # Create vector field
                import pyvista as pv
                import numpy as np
                
                vector_mesh = pv.PolyData(points)
                vector_mesh['vectors'] = vectors
                magnitudes = np.linalg.norm(vectors, axis=1)
                vector_mesh['magnitude'] = magnitudes
                
                # Filter out zero vectors
                non_zero_mask = magnitudes > 1e-10
                if np.any(non_zero_mask):
                    filtered_points = points[non_zero_mask]
                    filtered_vectors = vectors[non_zero_mask]
                    filtered_magnitudes = magnitudes[non_zero_mask]
                    
                    vector_mesh = pv.PolyData(filtered_points)
                    vector_mesh['vectors'] = filtered_vectors
                    vector_mesh['magnitude'] = filtered_magnitudes
                    
                    # Calculate scale factor
                    mesh_bounds = mesh.bounds
                    mesh_size = max(mesh_bounds[1] - mesh_bounds[0], mesh_bounds[3] - mesh_bounds[2])
                    max_magnitude = np.max(filtered_magnitudes)
                    
                    if max_magnitude > 0:
                        scale_factor = (mesh_size * 0.03) / max_magnitude
                    else:
                        scale_factor = mesh_size * 0.01
                    
                    if hasattr(mesh, '_size_options') and mesh._size_options:
                        vector_size_factor = mesh._size_options.get('vector_size_factor', 1.0)
                    else:
                        vector_size_factor = 1.0
                    
                    scale_factor *= vector_size_factor
                    
                    arrows = vector_mesh.glyph(
                        orient='vectors',
                        scale='magnitude',
                        factor=scale_factor,
                        geom=pv.Arrow(shaft_radius=0.05, tip_radius=0.1)
                    )
                    
                    return {
                        'mesh': arrows,
                        'scalars': 'magnitude',
                        'cmap': 'plasma',
                        'show_scalar_bar': True,
                        'scalar_bar_args': {'title': f"{variable_name} Vectors"},
                        'label': f"Vectors - {variable_name}"
                    }
            
            return None
            
        except Exception as e:
            print(f"Error in vector preparation: {e}")
            return None
    
    def _prepare_line_contour_meshes(self, mesh, scalars_array, variable_name, cmap, options):
        """Prepare meshes for line contour display"""
        prepared_meshes = []
        
        # Add base mesh with transparency
        show_mesh_edges = options.get('show_mesh_edges', True)
        edge_color = self.get_visualization_manager().default_edge_color
        
        base_mesh_data = {
            'mesh': mesh,
            'color': 'white',
            'show_edges': show_mesh_edges,
            'edge_color': edge_color if show_mesh_edges else None,
            'line_width': 1,
            'opacity': 0.1,
            'label': "Base Mesh"
        }
        prepared_meshes.append(base_mesh_data)
        
        # Generate contours
        try:
            n_contours = 10
            scalar_min = np.min(scalars_array)
            scalar_max = np.max(scalars_array)
            
            if scalar_min != scalar_max:
                contour_levels = np.linspace(scalar_min, scalar_max, n_contours)
                mesh_with_scalars = mesh.copy()
                
                if len(scalars_array) == mesh.n_cells:
                    mesh_with_scalars.cell_data['scalars'] = scalars_array
                    mesh_with_scalars = mesh_with_scalars.cell_data_to_point_data()
                else:
                    mesh_with_scalars.point_data['scalars'] = scalars_array
                
                contours = mesh_with_scalars.contour(
                    scalars='scalars',
                    isosurfaces=contour_levels
                )
                
                if contours.n_cells > 0:
                    contour_mesh_data = {
                        'mesh': contours,
                        'scalars': 'scalars',
                        'cmap': cmap,
                        'line_width': 2,
                        'style': 'surface',
                        'show_scalar_bar': True,
                        'scalar_bar_args': {'title': variable_name},
                        'label': f"Contours - {variable_name}"
                    }
                    prepared_meshes.append(contour_mesh_data)
                    
        except Exception as e:
            print(f"Error generating contours: {e}")
        
        return prepared_meshes
    
    def _prepare_dies_for_display(self, visualization_manager):
        """Prepare dies for atomic display"""
        prepared_dies = []
        
        if not visualization_manager.current_data:
            return prepared_dies
        
        dies = visualization_manager.current_data.get_dies()
        
        for die in dies:
            die_mesh = visualization_manager.mesh_builder.create_die_mesh(die)
            if die_mesh:
                die_data = {
                    'mesh': die_mesh,
                    'color': 'lightgrey',
                    'opacity': 1.0,
                    'show_edges': True,
                    'edge_color': 'black',
                    'line_width': 1,
                    'label': f"Die {die.get_id()}"
                }
                prepared_dies.append(die_data)
        
        return prepared_dies
    
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
        
        # PREPARE EVERYTHING BEFORE CLEARING pour éviter les saccades
        mesh = visualization_manager.current_mesh
        
        # Store size options in mesh
        mesh._size_options = {
            'constraint_size_factor': options.get('constraint_size_factor', 1.0),
            'vector_size_factor': options.get('vector_size_factor', 1.0)
        }
        
        # Prepare mesh de base
        prepared_meshes = []
        
        # Check if we have material colors
        if 'Material_Colors' in mesh.cell_data:
            # Use material colors
            mesh_data = {
                'mesh': mesh,
                'show_edges': show_edges,
                'edge_color': visualization_manager.default_edge_color,
                'line_width': 1,
                'scalars': 'Material_Colors',
                'rgb': True,
                'opacity': 1.0,
                'label': "Mesh - Materials"
            }
        else:
            # Original behavior - fallback to single color
            mesh_data = {
                'mesh': mesh,
                'show_edges': show_edges,
                'edge_color': visualization_manager.default_edge_color,
                'line_width': 1,
                'color': visualization_manager.default_mesh_color,
                'opacity': 1.0,
                'label': "Mesh"
            }
        
        prepared_meshes.append(mesh_data)
        
        # Prepare dies
        prepared_dies = self._prepare_dies_for_display(visualization_manager)
        
        # NOW DO EVERYTHING ATOMICALLY
        visualization_manager.clear()
        
        # Add all prepared meshes in one go
        for mesh_data in prepared_meshes:
            visualization_manager.plotter.add_mesh(**mesh_data)
        
        # Add all prepared dies in one go
        for die_data in prepared_dies:
            visualization_manager.plotter.add_mesh(**die_data)
        
        if show_constraints and hasattr(mesh, '_constraint_info'):
            visualization_manager.display_manager._add_all_constraints(visualization_manager.plotter, mesh)
        
        # Single final render
        visualization_manager.plotter.render()
        
        self.current_variable = None
        
        # Reapply picking if needed
        visualization_manager.reapply_mesh_picking_if_needed()
    
    def reapply_current_variable(self):
        """Reapply current variable with current options"""
        if self.current_variable:
            self._apply_variable_to_mesh(self.current_variable)
        else:
            # Si pas de variable active, afficher juste la géométrie
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