"""
Unified Display Modes Management Module
Handles all display modes in one place
"""

import numpy as np
import pyvista as pv


class DisplayModeManager:
    """Unified manager for all display modes and options"""
    
    def __init__(self):
        self.wireframe_mode = False
    
    def set_wireframe_mode(self, enabled):
        """Enable/disable wireframe mode"""
        self.wireframe_mode = enabled
    
    def _calculate_proportional_size(self, mesh, base_factor=0.005):
        """Calculate proportional size based on mesh dimensions and element density"""
        if not mesh or not hasattr(mesh, 'bounds'):
            return 0.01  # Default fallback size
        
        bounds = mesh.bounds
        # Calculate mesh dimensions
        width = bounds[1] - bounds[0]   # X dimension
        height = bounds[3] - bounds[2]  # Y dimension
        depth = bounds[5] - bounds[4]   # Z dimension
        
        # Use the maximum dimension as reference
        max_dimension = max(width, height, depth)
        
        # Calculate mesh area for density calculation
        mesh_area = width * height
        if mesh_area <= 0:
            mesh_area = 1
        
        # Element density factor (more elements = smaller spheres)
        n_elements = mesh.n_cells if hasattr(mesh, 'n_cells') else 1000
        density_factor = min(1.0, 1000.0 / n_elements)  # Normalize by 1000 elements
        
        # Calculate proportional size (default 0.5% of max dimension, adjusted by density)
        proportional_size = max_dimension * base_factor * density_factor
        
        # Ensure minimum and maximum sizes
        min_size = max_dimension * 0.0001  # 0.01% minimum
        max_size = max_dimension * 0.02    # 2% maximum
        
        proportional_size = max(min_size, min(proportional_size, max_size))
        
        return proportional_size
    
    def display_mesh(self, plotter, mesh, mesh_color, edge_color, show_edges=True):
        """Display main mesh - MODIFIED to use material colors when available"""
        
        # Check if we have material colors - NEW
        if 'Material_Colors' in mesh.cell_data:
            # Use material colors
            if self.wireframe_mode:
                plotter.add_mesh(mesh, style='wireframe', scalars='Material_Colors', rgb=True, line_width=1, label="Mesh - Materials (Wireframe)")
            else:
                plotter.add_mesh(mesh, show_edges=show_edges, edge_color=edge_color, line_width=1, 
                               scalars='Material_Colors', rgb=True, opacity=1.0, label="Mesh - Materials")
        else:
            # Original behavior - fallback to single color
            if self.wireframe_mode:
                plotter.add_mesh(mesh, style='wireframe', color=edge_color, line_width=1, label="Mesh - Wireframe")
            else:
                plotter.add_mesh(mesh, show_edges=show_edges, edge_color=edge_color, line_width=1, 
                               color=mesh_color, opacity=1.0, label="Mesh")
    
    def display_die(self, plotter, die_mesh, die_id):
        """Display die"""
        if self.wireframe_mode:
            plotter.add_mesh(die_mesh, style='wireframe', color='red', line_width=1, 
                           label=f"Die {die_id} - Wireframe")
        else:
            plotter.add_mesh(die_mesh, color='lightgrey', opacity=1.0, show_edges=True, 
                           edge_color='black', line_width=1, label=f"Die {die_id}")
    
    def display_variable_with_options(self, plotter, mesh, scalar_name, variable_name, edge_color, options):
        """Display variables with all options"""
        
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
            mesh = self._apply_hd_contour(mesh, scalar_name)
        
        # Choose colormap
        cmap = 'Blues' if monochromatic_mode else 'turbo'
        
        # Get scalar data
        scalars_array, use_point_data = self._get_scalar_data(mesh, scalar_name, high_definition_contour)
        
        # Handle vector mode
        if vector_mode:
            self._display_vector_field(plotter, mesh, scalar_name, variable_name, show_mesh_edges, edge_color)
        elif line_contour_mode:
            self._display_line_contours(plotter, mesh, scalars_array, variable_name, cmap, show_mesh_edges, edge_color)
        else:
            # Normal display modes
            if wireframe_mode:
                # Show variable colors with wireframe overlay
                plotter.add_mesh(
                    mesh,
                    scalars=scalars_array,
                    show_edges=False,  # No regular edges
                    opacity=1.0,
                    cmap=cmap,
                    show_scalar_bar=True,
                    scalar_bar_args={
                        'title': variable_name,
                    },
                    label=f"Mesh - {variable_name}"
                )
            else:
                # Normal display with options
                plotter.add_mesh(
                    mesh,
                    scalars=scalars_array,
                    show_edges=show_mesh_edges,
                    edge_color=edge_color if show_mesh_edges else None,
                    line_width=1,
                    opacity=1.0,
                    cmap=cmap,
                    show_scalar_bar=True,
                    scalar_bar_args={
                        'title': variable_name,
                    },
                    label=f"Mesh - {variable_name}"
                )
        
        # Add constraints if enabled
        if view_constraints:
            self._add_constraints_visualization(plotter, mesh)
        
        if use_point_data:
            print(f"HD Contour: Using smooth interpolation for {variable_name}")
    
    def _display_vector_field(self, plotter, mesh, scalar_name, variable_name, show_mesh_edges, edge_color):
        """Display vector field for stress/strain variables"""
        
        # First, add the base mesh with light transparency
        if show_mesh_edges:
            plotter.add_mesh(
                mesh,
                color='lightgray',
                show_edges=True,
                edge_color=edge_color,
                line_width=1,
                opacity=0.3,
                label="Base Mesh"
            )
        else:
            plotter.add_mesh(
                mesh,
                color='lightgray',
                opacity=0.3,
                show_edges=False,
                label="Base Mesh"
            )
        
        try:
            # For velocity vectors, try different approaches
            if "Velocity" in variable_name:
                print(f"Processing velocity variable: {variable_name}")
                
                # Method 1: Try node data first
                points, vectors = self._get_velocity_vectors_from_nodes(mesh)
                
            else:
                # For other variables, use cell centers
                cell_centers = mesh.cell_centers()
                points = cell_centers.points
                vectors = self._calculate_vectors_from_variable(mesh, scalar_name, variable_name)
            
            if vectors is not None and len(vectors) == len(points):
                # Create vector field
                vector_mesh = pv.PolyData(points)
                vector_mesh['vectors'] = vectors
                
                # Calculate vector magnitudes for coloring
                magnitudes = np.linalg.norm(vectors, axis=1)
                vector_mesh['magnitude'] = magnitudes
                
                # Filter out zero vectors for better visualization
                non_zero_mask = magnitudes > 1e-10
                if np.any(non_zero_mask):
                    filtered_points = points[non_zero_mask]
                    filtered_vectors = vectors[non_zero_mask]
                    filtered_magnitudes = magnitudes[non_zero_mask]
                    
                    vector_mesh = pv.PolyData(filtered_points)
                    vector_mesh['vectors'] = filtered_vectors
                    vector_mesh['magnitude'] = filtered_magnitudes
                    
                    # Calculate appropriate scale factor
                    mesh_bounds = mesh.bounds
                    mesh_size = max(mesh_bounds[1] - mesh_bounds[0], mesh_bounds[3] - mesh_bounds[2])
                    max_magnitude = np.max(filtered_magnitudes)
                    
                    if max_magnitude > 0:
                        # Scale arrows to be about 3% of mesh size at maximum
                        scale_factor = (mesh_size * 0.03) / max_magnitude
                    else:
                        scale_factor = mesh_size * 0.01
                    
                    # Add arrows with automatic scaling
                    arrows = vector_mesh.glyph(
                        orient='vectors',
                        scale='magnitude',
                        factor=scale_factor,
                        geom=pv.Arrow()
                    )
                    
                    plotter.add_mesh(
                        arrows,
                        scalars='magnitude',
                        cmap='plasma',
                        show_scalar_bar=True,
                        scalar_bar_args={
                            'title': f"{variable_name} Vectors",
                        },
                        label=f"Vectors - {variable_name}"
                    )
                    
                    print(f"Generated {len(filtered_vectors)} vectors for {variable_name} (scale: {scale_factor:.6f})")
                else:
                    print(f"No significant vectors found for {variable_name}")
                    self._fallback_display(plotter, mesh, scalar_name, variable_name)
            else:
                print(f"Could not generate vectors for {variable_name}")
                # Fallback to normal display
                self._fallback_display(plotter, mesh, scalar_name, variable_name)
                
        except Exception as e:
            print(f"Error generating vectors for {variable_name}: {e}")
            # Fallback to normal display
            self._fallback_display(plotter, mesh, scalar_name, variable_name)
    
    def _calculate_vectors_from_variable(self, mesh, scalar_name, variable_name):
        """Calculate vector components based on the variable type"""
        
        # For stress and strain variables, try to get tensor components
        if "Stress" in variable_name or "Strain" in variable_name:
            return self._calculate_stress_strain_vectors(mesh, variable_name)
        elif "Velocity" in variable_name:
            return self._calculate_velocity_vectors(mesh)
        elif "Force" in variable_name:
            return self._calculate_force_vectors(mesh)
        else:
            # For scalar variables, create normal vectors scaled by the scalar value
            return self._calculate_scalar_normal_vectors(mesh, scalar_name)
    
    def _calculate_stress_strain_vectors(self, mesh, variable_name):
        """Calculate stress or strain vectors from tensor components"""
        try:
            # Try to get principal stress/strain components
            if "Stress" in variable_name:
                if 'Stress x(r)' in mesh.cell_data and 'Stress y(z)' in mesh.cell_data:
                    stress_x = mesh.cell_data['Stress x(r)']
                    stress_y = mesh.cell_data['Stress y(z)']
                    stress_z = np.zeros_like(stress_x)  # 2D case
                    
                    vectors = np.column_stack([stress_x, stress_y, stress_z])
                    return vectors
                    
            elif "Strain" in variable_name:
                if 'Strain x(r)' in mesh.cell_data and 'Strain y(z)' in mesh.cell_data:
                    strain_x = mesh.cell_data['Strain x(r)']
                    strain_y = mesh.cell_data['Strain y(z)']
                    strain_z = np.zeros_like(strain_x)  # 2D case
                    
                    vectors = np.column_stack([strain_x, strain_y, strain_z])
                    return vectors
            
            return None
            
        except Exception as e:
            print(f"Error calculating stress/strain vectors: {e}")
            return None
    
    def _calculate_velocity_vectors(self, mesh):
        """Calculate velocity vectors"""
        try:
            if 'Velocity X(r)' in mesh.cell_data and 'Velocity Y(z)' in mesh.cell_data:
                vel_x = mesh.cell_data['Velocity X(r)']
                vel_y = mesh.cell_data['Velocity Y(z)']
                vel_z = np.zeros_like(vel_x)  # 2D case
                
                # For velocity, the vectors represent direction of movement
                vectors = np.column_stack([vel_x, vel_y, vel_z])
                return vectors
            return None
            
        except Exception as e:
            print(f"Error calculating velocity vectors: {e}")
            return None
    
    def _calculate_force_vectors(self, mesh):
        """Calculate force vectors"""
        try:
            if 'Force X(r)' in mesh.cell_data and 'Force Y(z)' in mesh.cell_data:
                force_x = mesh.cell_data['Force X(r)']
                force_y = mesh.cell_data['Force Y(z)']
                force_z = np.zeros_like(force_x)  # 2D case
                
                vectors = np.column_stack([force_x, force_y, force_z])
                return vectors
            return None
            
        except Exception as e:
            print(f"Error calculating force vectors: {e}")
            return None
    
    def _calculate_scalar_normal_vectors(self, mesh, scalar_name):
        """Calculate normal vectors scaled by scalar values"""
        try:
            if scalar_name in mesh.cell_data:
                scalar_values = mesh.cell_data[scalar_name]
                
                # For 2D case, create vectors in Z direction scaled by scalar value
                vectors = np.column_stack([
                    np.zeros_like(scalar_values),  # X component
                    np.zeros_like(scalar_values),  # Y component  
                    scalar_values * 0.1  # Z component (scaled)
                ])
                return vectors
            return None
            
        except Exception as e:
            print(f"Error calculating scalar normal vectors: {e}")
            return None
    
    def _get_velocity_vectors_from_nodes(self, mesh):
        """Get velocity vectors directly from node data"""
        try:
            # Get mesh points (node positions)
            points = mesh.points
            
            # Try to get velocity data from the original mesh data
            if hasattr(mesh, '_original_data') and hasattr(mesh, '_node_id_to_index'):
                nodes = mesh._original_data.get_nodes()
                node_id_to_index = mesh._node_id_to_index
                
                # Create velocity array matching mesh points order
                velocities = np.zeros((len(points), 3))
                
                # Debug: let's check some velocity values
                debug_count = 0
                
                for node in nodes:
                    if node.get_id() in node_id_to_index:
                        index = node_id_to_index[node.get_id()]
                        vx = node.get_Vx() or 0.0
                        vy = node.get_Vy() or 0.0
                        
                        # Debug first few nodes
                        if debug_count < 5:
                            print(f"Node {node.get_id()}: vx={vx}, vy={vy}, pos=({node.get_coordX()}, {node.get_coordY()})")
                            debug_count += 1
                        
                        velocities[index] = [vx, vy, 0.0]
                
                # Let's also check if we need to normalize or process the vectors
                magnitudes = np.linalg.norm(velocities, axis=1)
                non_zero_magnitudes = magnitudes[magnitudes > 1e-10]
                print(f"Velocity stats: min={np.min(non_zero_magnitudes):.6f}, max={np.max(non_zero_magnitudes):.6f}, mean={np.mean(non_zero_magnitudes):.6f}")
                
                return points, velocities
            else:
                # Fallback: use interpolated velocity from cell data
                print("Using fallback interpolation method")
                return self._interpolate_velocity_to_nodes(mesh)
                
        except Exception as e:
            print(f"Error getting velocity vectors from nodes: {e}")
            return self._interpolate_velocity_to_nodes(mesh)
    
    def _interpolate_velocity_to_nodes(self, mesh):
        """Interpolate velocity from cell data to node positions"""
        try:
            # Convert cell data to point data for better node-based visualization
            mesh_with_point_data = mesh.cell_data_to_point_data()
            
            if 'Velocity X(r)' in mesh_with_point_data.point_data and 'Velocity Y(z)' in mesh_with_point_data.point_data:
                vel_x = mesh_with_point_data.point_data['Velocity X(r)']
                vel_y = mesh_with_point_data.point_data['Velocity Y(z)']
                vel_z = np.zeros_like(vel_x)
                
                vectors = np.column_stack([vel_x, vel_y, vel_z])
                return mesh.points, vectors
            else:
                return None, None
                
        except Exception as e:
            print(f"Error interpolating velocity to nodes: {e}")
            return None, None
    
    def _fallback_display(self, plotter, mesh, scalar_name, variable_name):
        """Fallback to normal scalar display when vector display fails"""
        if scalar_name in mesh.cell_data:
            plotter.add_mesh(
                mesh,
                scalars=mesh.cell_data[scalar_name],
                cmap='turbo',
                show_scalar_bar=True,
                scalar_bar_args={
                    'title': variable_name,
                },
                label=f"Mesh - {variable_name} (fallback)"
            )
    
    def _display_line_contours(self, plotter, mesh, scalars_array, variable_name, cmap, show_mesh_edges, edge_color):
        """Display contours as colored lines instead of filled regions"""
        
        # First, add the base mesh
        if show_mesh_edges:
            plotter.add_mesh(
                mesh,
                color='white',
                show_edges=True,
                edge_color=edge_color,
                line_width=1,
                opacity=0.1,
                label="Base Mesh"
            )
        else:
            plotter.add_mesh(
                mesh,
                color='white',
                opacity=0.1,
                show_edges=False,
                label="Base Mesh"
            )
        
        # Generate contour lines
        try:
            # Determine number of contour levels
            n_contours = 10
            
            # Get scalar range
            scalar_min = np.min(scalars_array)
            scalar_max = np.max(scalars_array)
            
            if scalar_min == scalar_max:
                print(f"Warning: Constant scalar values for {variable_name}")
                return
            
            # Generate contour levels
            contour_levels = np.linspace(scalar_min, scalar_max, n_contours)
            
            # Create mesh copy with scalars
            mesh_with_scalars = mesh.copy()
            if len(scalars_array) == mesh.n_cells:
                mesh_with_scalars.cell_data['scalars'] = scalars_array
                # Convert to point data for better contours
                mesh_with_scalars = mesh_with_scalars.cell_data_to_point_data()
            else:
                mesh_with_scalars.point_data['scalars'] = scalars_array
            
            # Generate contours
            contours = mesh_with_scalars.contour(
                scalars='scalars',
                isosurfaces=contour_levels
            )
            
            if contours.n_cells > 0:
                # Add contour lines with colors
                plotter.add_mesh(
                    contours,
                    scalars='scalars',
                    cmap=cmap,
                    line_width=2,
                    style='surface',
                    show_scalar_bar=True,
                    scalar_bar_args={
                        'title': variable_name,
                    },
                    label=f"Contours - {variable_name}"
                )
                print(f"Generated {contours.n_cells} contour lines for {variable_name}")
            else:
                print(f"No contour lines generated for {variable_name}")
                
        except Exception as e:
            print(f"Error generating contours for {variable_name}: {e}")
            # Fallback to normal display
            plotter.add_mesh(
                mesh,
                scalars=scalars_array,
                cmap=cmap,
                show_scalar_bar=True,
                scalar_bar_args={
                    'title': variable_name,
                },
                label=f"Mesh - {variable_name} (fallback)"
            )
    
    def display_mesh_with_constraints(self, plotter, mesh, mesh_color, edge_color, show_edges=True, show_constraints=False):
        """Display mesh with optional constraints"""
        # Display normal mesh first
        self.display_mesh(plotter, mesh, mesh_color, edge_color, show_edges)
        
        # Add constraints if requested
        if show_constraints:
            self._add_constraints_visualization(plotter, mesh)
    
    def _add_constraints_visualization(self, plotter, mesh):
        """Add constraint visualizations based on node codes"""
        codes = mesh.point_data['Node_Code']

        unique_codes, _ = np.unique(codes, return_counts=True)
        print(f"Unique codes: {unique_codes}")
        
        # Check if we have constraint information stored as mesh attribute
        if hasattr(mesh, '_constraint_info') and mesh._constraint_info:
            constraint_info = mesh._constraint_info
            node_ids = constraint_info['node_ids']
            positions_x = constraint_info['positions_x']
            positions_y = constraint_info['positions_y']
            constraint_codes = constraint_info['codes']
            
            self._create_constraint_shapes_from_arrays(plotter, mesh, node_ids, positions_x, positions_y, constraint_codes)
        
    def _create_constraint_shapes_from_arrays(self, plotter, mesh, node_ids, positions_x, positions_y, constraint_codes):
        """Create constraint shapes using arrays of node information"""
        
        constraint_size = self._calculate_proportional_size(mesh, base_factor=0.01)

        code_groups = {
            0: [],    # No constraint (nothing displayed)
            1: [],    # Red sphere
            2: [],    # Blue sphere
            3: [],    # black sphere
            -1: [],   # white sphere
            -2: [],   # white sphere
            'below_-10': []  # grey sphere
        }
        
        for i in range(len(node_ids)):
            node_id = node_ids[i]
            code = constraint_codes[i]
            position = [positions_x[i], positions_y[i], 0]
            
            if code == 0:
                continue # nothing to display
            elif code in [1, 2, 3, -1, -2]:
                code_groups[code].append((node_id, position))
            elif code <= -10:
                code_groups['below_-10'].append((node_id, position))
            else:
                print(f"Unknown constraint code {code} for node {node_id}")
        
        # Mapping of codes to colors and names
        code_settings = {
            1: ('red', 'constraint_red_sphere'),
            2: ('blue', 'constraint_blue_sphere'),
            3: ('black', 'constraint_sphere'),
            -1: ('#f2f2f2', 'constraint_white_sphere'),
            -2: ('#f2f2f2', 'constraint_white_sphere'),
            'below_-10': ('black', 'constraint_black_sphere'),
        }

        for code, (color, name_prefix) in code_settings.items():
            for node_id, position in code_groups[code]:
                sphere = pv.Sphere(radius=constraint_size, center=position)
                plotter.add_mesh(sphere, color=color, opacity=1.0,
                                name=f'{name_prefix}_{node_id}')

            
    def _apply_hd_contour(self, mesh, scalar_name):
        """Apply high definition contour"""
        mesh_copy = mesh.copy()
        mesh_with_point_data = mesh_copy.cell_data_to_point_data()
        
        if scalar_name in mesh_with_point_data.point_data:
            return mesh_with_point_data
        else:
            return mesh_copy
    
    def _get_scalar_data(self, mesh, scalar_name, hd_contour_enabled):
        """Get scalar data"""
        use_point_data = (hd_contour_enabled and 
                         hasattr(mesh, 'point_data') and 
                         scalar_name in mesh.point_data)
        
        if use_point_data:
            return mesh.point_data[scalar_name], True
        else:
            return mesh.cell_data[scalar_name], False