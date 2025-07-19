"""
Field Variables Menu Handler 
"""

from PyQt5.QtWidgets import QMessageBox
import pyvista as pv
import numpy as np


class FieldVariablesHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.current_variable = None
        
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
    
    def _get_current_options(self):
        """Get current options from toolbar manager"""
        visualization_manager = self.get_visualization_manager()
        
        # Try to get options from toolbar manager first
        if hasattr(visualization_manager, 'toolbar_manager'):
            return visualization_manager.toolbar_manager.get_current_options()
        else:
            # Fallback to local viz_options for backward compatibility
            return self.viz_options.get_current_options()
    
    def apply_variable(self, variable_key):
        """Apply variable to current mesh"""
        visualization_manager = self.get_visualization_manager()
        
        if not visualization_manager.current_mesh:
            QMessageBox.warning(self.main_window, "No Mesh", "Please load a mesh first.")
            return
        
        # Resolve variable key
        resolved_key = self._resolve_variable_key(variable_key)
        if not resolved_key:
            return
        
        # Apply the resolved variable
        self._apply_variable_to_mesh(resolved_key, variable_key)
    
    def _resolve_variable_key(self, variable_key):
        mesh = self.get_visualization_manager().current_mesh
        
        if variable_key in self.variable_mapping:
            mapped_name = self.variable_mapping[variable_key]
            if mapped_name in mesh.cell_data:
                return mapped_name
            else:
                # Show error with mapped name
                available_list = list(mesh.cell_data.keys())
                QMessageBox.information(
                    self.main_window,
                    "Variable Not Available",
                    f"The variable '{mapped_name}' (mapped from '{variable_key}') is not available in the mesh data.\n"
                    f"Available: {', '.join(available_list[:5])}{'...' if len(available_list) > 5 else ''}"
                )
                return None
        
        # Fallback: check if key is directly in mesh data (for backward compatibility)
        if variable_key in mesh.cell_data:
            return variable_key
        
        # Not found anywhere
        available_list = list(mesh.cell_data.keys())
        QMessageBox.information(
            self.main_window,
            "Variable Not Available",
            f"The variable key '{variable_key}' is not found in mapping or mesh data.\n"
            f"Available mesh data: {', '.join(available_list[:5])}{'...' if len(available_list) > 5 else ''}"
        )
        return None
    
    def _apply_variable_to_mesh(self, resolved_variable_name, original_key):
        visualization_manager = self.get_visualization_manager()
        
        # PREPARE EVERYTHING BEFORE CLEARING
        mesh = visualization_manager.current_mesh
        options = self._get_current_options()
        
        # Prepare variable mesh
        prepared_meshes = self._prepare_all_meshes_for_display(
            mesh, resolved_variable_name, original_key, 
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
        
        self.current_variable = resolved_variable_name
        
        # Reapply picking if needed
        visualization_manager.reapply_mesh_picking_if_needed()
    
    def _prepare_all_meshes_for_display(self, mesh, scalar_name, variable_display_name, edge_color, options):
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
        auto_scale_mode = options.get('auto_scale_mode', False)
        
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

        clim = None
        if auto_scale_mode:
            visualization_manager = self.get_visualization_manager()
            global_min, global_max = visualization_manager.get_global_scale_range_for_variable(scalar_name)
            if global_min is not None and global_max is not None:
                clim = [global_min, global_max]
                print(f"Using auto-scale for {scalar_name}: [{global_min:.6f}, {global_max:.6f}]")
        
        # Prepare main variable mesh
        if vector_mode:
            return self._prepare_vector_meshes(mesh, scalars_array, variable_display_name, options)
        elif line_contour_mode:
            return self._prepare_line_contour_meshes(mesh, scalars_array, variable_display_name, cmap, options)
        elif wireframe_mode:
            mesh_data = {
                'mesh': mesh,
                'scalars': scalars_array,
                'show_edges': False,
                'opacity': 1.0,
                'cmap': cmap,
                'clim': clim,
                'show_scalar_bar': True,
                'scalar_bar_args': {'title': variable_display_name},
                'label': f"Mesh - {variable_display_name}"
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
                'clim': clim,
                'show_scalar_bar': True,
                'scalar_bar_args': {'title': variable_display_name},
                'label': f"Mesh - {variable_display_name}"
            }
        
        prepared_meshes.append(mesh_data)
        
        if view_constraints and hasattr(mesh, '_constraint_info'):
            pass
    
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
    
    def standard_options(self):
        """Display only geometry - Standard Options"""
        visualization_manager = self.get_visualization_manager()
        
        if not visualization_manager.current_data:
            QMessageBox.warning(self.main_window, "No Data", "Please load a mesh first.")
            return
        
        # Get current options
        options = self._get_current_options()
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
            # Fallback to single color
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
            # Find the original key that corresponds to current variable
            original_key = None
            for key, value in self.variable_mapping.items():
                if value == self.current_variable:
                    original_key = key
                    break
            
            if original_key:
                self.apply_variable(original_key)
            else:
                # Direct application if not found in mapping (backward compatibility)
                self._apply_variable_to_mesh(self.current_variable, self.current_variable)
        else:
            # No variable active, display geometry only
            self.standard_options()
    
    def get_available_variables(self):
        visualization_manager = self.get_visualization_manager()
        
        if not visualization_manager.current_mesh:
            return {}
        
        mesh = visualization_manager.current_mesh
        available_vars = {}
        
        for key, mapped_name in self.variable_mapping.items():
            is_available = mapped_name in mesh.cell_data
            available_vars[key] = (mapped_name, is_available)
        
        return available_vars
    
    def get_current_variable_key(self):
        if not self.current_variable:
            return None
            
        # Find the key that maps to current variable
        for key, value in self.variable_mapping.items():
            if value == self.current_variable:
                return key
        
        return None