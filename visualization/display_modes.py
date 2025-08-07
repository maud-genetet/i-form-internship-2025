"""
Unified Display Modes Management Module
Handles all display modes in one place
"""

import numpy as np
import pyvista as pv
import logging
logger = logging.getLogger(__name__) 

class DisplayModeManager:
    """Unified manager for all display modes and options"""
    
    # Centralized constraint configuration
    CONSTRAINT_CONFIG = {
        1: {'color': [1.0, 0.0, 0.0], 'name': 'red_constraints', 'description': 'Fixed X constraint'},
        2: {'color': [0.0, 0.0, 1.0], 'name': 'blue_constraints', 'description': 'Fixed Y constraint'},
        3: {'color': [0.0, 0.0, 0.0], 'name': 'black_constraints', 'description': 'Fixed XY constraint'},
        -1: {'color': [0.95, 0.95, 0.95], 'name': 'white_constraints_1', 'description': 'Special constraint -1'},
        -2: {'color': [0.95, 0.95, 0.95], 'name': 'white_constraints_2', 'description': 'Special constraint -2'},
        'below_-10': {'color': [0.0, 0.0, 0.0], 'name': 'special_constraints', 'description': 'Special constraints (code <= -10)'},
        'contact': {'color': [1.0, 0.41, 0.71], 'name': 'contact_constraints', 'description': 'Contact nodes'}
    }
    
    # Level of detail configuration
    LOD_SETTINGS = {
        'ultra_high': {'subdivisions': 16, 'max_count': 100},
        'high': {'subdivisions': 12, 'max_count': 500},
        'medium': {'subdivisions': 8, 'max_count': 2000},
        'low': {'subdivisions': 6, 'max_count': 10000},
        'ultra_low': {'subdivisions': 4, 'max_count': float('inf')}
    }
    
    def __init__(self):
        self.wireframe_mode = False
        self.cached_spheres = {}
    
    def set_wireframe_mode(self, enabled):
        """Enable/disable wireframe mode"""
        self.wireframe_mode = enabled
    
    def _get_constraint_config(self, code):
        """Get configuration for a constraint code"""
        if code == 0:
            return None
        elif code in self.CONSTRAINT_CONFIG:
            return self.CONSTRAINT_CONFIG[code]
        elif code <= -10:
            return self.CONSTRAINT_CONFIG['below_-10']
        else:
            return {'color': [0.5, 0.5, 0.5], 'name': f'unknown_constraint_{code}', 'description': f'Unknown constraint code {code}'}
    
    def _get_optimal_lod(self, total_constraints):
        """Determine optimal level of detail"""
        for lod_name, settings in self.LOD_SETTINGS.items():
            if total_constraints <= settings['max_count']:
                return settings['subdivisions'], lod_name
        return self.LOD_SETTINGS['ultra_low']['subdivisions'], 'ultra_low'
    
    def _get_cached_sphere(self, radius, subdivisions=8):
        """Get sphere from cache"""
        key = (radius, subdivisions)
        if key not in self.cached_spheres:
            self.cached_spheres[key] = pv.Sphere(
                radius=radius, 
                phi_resolution=subdivisions, 
                theta_resolution=subdivisions
            )
        return self.cached_spheres[key]
    
    def _create_batched_spheres(self, positions, radius, subdivisions=8):
        """Create spheres in batch with glyph"""
        if not positions:
            return None
            
        positions = np.array(positions)
        points = pv.PolyData(positions)
        sphere_source = self._get_cached_sphere(radius, subdivisions)
        return points.glyph(geom=sphere_source, scale=False, orient=False)
    
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
            plotter.add_mesh(die_mesh, style='wireframe', color='red', line_width=1, opacity=0.5,
                           label=f"Die {die_id} - Wireframe")
        else:
            plotter.add_mesh(die_mesh, color='lightgrey', opacity=0.5, show_edges=True, 
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
            self._display_vectors(plotter, mesh, scalar_name, variable_name)
        elif line_contour_mode:
            self._display_contours(plotter, mesh, scalars_array, variable_name, cmap)
        else:
            if wireframe_mode:
                plotter.add_mesh(
                    mesh,
                    scalars=scalars_array,
                    show_edges=False,
                    opacity=0.5,
                    cmap=cmap,
                    show_scalar_bar=True,
                    scalar_bar_args={'title': variable_name},
                    label=f"Mesh - {variable_name}"
                )
            else:
                plotter.add_mesh(
                    mesh,
                    scalars=scalars_array,
                    show_edges=show_mesh_edges,
                    edge_color=edge_color if show_mesh_edges else None,
                    line_width=1,
                    opacity=1.0,
                    cmap=cmap,
                    show_scalar_bar=True,
                    scalar_bar_args={'title': variable_name},
                    label=f"Mesh - {variable_name}"
                )
        
        # Add constraints if enabled
        if view_constraints and hasattr(mesh, '_constraint_info'):
            self._add_all_constraints(plotter, mesh)
        
        if use_point_data:
            logger.info(f"HD Contour: Using smooth interpolation for {variable_name}")
    
    def _add_all_constraints(self, plotter, mesh):
        """Add ALL constraints in ONE single add_mesh operation"""
        constraint_info = mesh._constraint_info
        node_ids = constraint_info['node_ids']
        positions_x = constraint_info['positions_x']
        positions_y = constraint_info['positions_y']
        constraint_codes = constraint_info['codes']
        
        all_positions = []
        all_colors = []
        
        constraint_size = self._calculate_proportional_size(mesh, base_factor=0.01)

        if hasattr(mesh, '_size_options') and mesh._size_options:
            constraint_size *= mesh._size_options.get('constraint_size_factor', 1.0)

        total_constraints = len([code for code in constraint_codes if code != 0])
        subdivisions, _ = self._get_optimal_lod(total_constraints)
        
        # Add node constraints
        for i in range(len(node_ids)):
            code = constraint_codes[i]
            if code == 0:
                continue
                
            position = [positions_x[i], positions_y[i], 0]
            config = self._get_constraint_config(code)
            if config:
                all_positions.append(position)
                all_colors.append(config['color'])
        
        # Add contact nodes
        nodes = mesh._original_data.get_nodes()
        contact_config = self.CONSTRAINT_CONFIG['contact']
        
        for node in nodes:
            if node.is_contact_node():
                all_positions.append([node.get_coordX(), node.get_coordY(), 0])
                all_colors.append(contact_config['color'])
        
        # Create ALL spheres in ONE operation
        if all_positions:
            combined_glyphs = self._create_batched_spheres(all_positions, constraint_size, subdivisions)
            
            if combined_glyphs:
                n_positions = len(all_positions)
                n_glyph_points = combined_glyphs.n_points
                points_per_sphere = n_glyph_points // n_positions
                
                # Expand colors to match all glyph points
                expanded_colors = []
                for i, color in enumerate(all_colors):
                    for _ in range(points_per_sphere):
                        expanded_colors.append(color)
                
                # Handle any remaining points
                while len(expanded_colors) < n_glyph_points:
                    expanded_colors.append(all_colors[-1])
                
                # Truncate if too many
                expanded_colors = expanded_colors[:n_glyph_points]
                
                # Add colors to points
                combined_glyphs.point_data['constraint_colors'] = np.array(expanded_colors)
                
                # Add everything in ONE add_mesh call
                plotter.add_mesh(
                    combined_glyphs,
                    scalars='constraint_colors',
                    rgb=True,
                    opacity=0.8,
                    name='all_constraints'
                )
                logger.info(f"Added {len(all_positions)} constraints in ONE operation")
    
    def _display_vectors(self, plotter, mesh, scalar_name, variable_name):
        """Display vectors"""
        try:
            if "Velocity" in variable_name:
                points, vectors = self._get_velocity_vectors_from_nodes(mesh)
            else:
                cell_centers = mesh.cell_centers()
                points = cell_centers.points
                vectors = self._calculate_vectors_from_variable(mesh, scalar_name, variable_name)
            
            if vectors is not None and len(vectors) == len(points):
                vector_mesh = pv.PolyData(points)
                vector_mesh['vectors'] = vectors
                magnitudes = np.linalg.norm(vectors, axis=1)
                vector_mesh['magnitude'] = magnitudes
                
                non_zero_mask = magnitudes > 1e-10
                if np.any(non_zero_mask):
                    filtered_points = points[non_zero_mask]
                    filtered_vectors = vectors[non_zero_mask]
                    filtered_magnitudes = magnitudes[non_zero_mask]
                    
                    vector_mesh = pv.PolyData(filtered_points)
                    vector_mesh['vectors'] = filtered_vectors
                    vector_mesh['magnitude'] = filtered_magnitudes
                    
                    mesh_bounds = mesh.bounds
                    mesh_size = max(mesh_bounds[1] - mesh_bounds[0], mesh_bounds[3] - mesh_bounds[2])
                    max_magnitude = np.max(filtered_magnitudes)
                    
                    if max_magnitude > 0:
                        scale_factor = (mesh_size * 0.03) / max_magnitude
                    else:
                        scale_factor = mesh_size * 0.01

                    if hasattr(mesh, '_size_options'):
                        scale_factor *= mesh._size_options.get('vector_size_factor', 1.0)
                    
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
                        scalar_bar_args={'title': f"{variable_name} Vectors"},
                        label=f"Vectors - {variable_name}"
                    )
                    
        except Exception as e:
            logger.exception(f"Error in vector display: {e}")
    
    def _display_contours(self, plotter, mesh, scalars_array, variable_name, cmap):
        """Display contours"""
        try:
            n_contours = 10
            scalar_min = np.min(scalars_array)
            scalar_max = np.max(scalars_array)
            
            if scalar_min == scalar_max:
                return
            
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
                plotter.add_mesh(
                    contours,
                    scalars='scalars',
                    cmap=cmap,
                    line_width=2,
                    style='surface',
                    show_scalar_bar=True,
                    scalar_bar_args={'title': variable_name},
                    label=f"Contours - {variable_name}"
                )
                
        except Exception as e:
            logger.exception(f"Error in contour display: {e}")
    
    def _calculate_vectors_from_variable(self, mesh, scalar_name, variable_name):
        """Calculate vector components based on the variable type"""
        
        try:
            # If not a vector variable, return None
            if not ("Velocity" in variable_name or "Force" in variable_name):
                return None
            
            # scalar_name is the array of scalar values
            if isinstance(scalar_name, str) and scalar_name in mesh.cell_data:
                scalar_values = mesh.cell_data[scalar_name]
            elif hasattr(scalar_name, '__len__'):
                scalar_values = scalar_name
            else:
                return None
            
            if "Total" in variable_name:
                if "Velocity" in variable_name:
                    if 'Velocity X(r)' in mesh.cell_data and 'Velocity Y(z)' in mesh.cell_data:
                        vel_x = mesh.cell_data['Velocity X(r)']
                        vel_y = mesh.cell_data['Velocity Y(z)']
                        vectors = np.column_stack([vel_x, vel_y, np.zeros_like(vel_x)])
                        return vectors
                elif "Force" in variable_name:
                    if 'Force X(r)' in mesh.cell_data and 'Force Y(z)' in mesh.cell_data:
                        force_x = mesh.cell_data['Force X(r)']
                        force_y = mesh.cell_data['Force Y(z)']
                        vectors = np.column_stack([force_x, force_y, np.zeros_like(force_x)])
                        return vectors
                return None
            
            elif "X" in variable_name or "(r)" in variable_name:
                vectors = np.column_stack([
                    scalar_values,
                    np.zeros_like(scalar_values),
                    np.zeros_like(scalar_values)
                ])
            elif "Y" in variable_name or "(z)" in variable_name:
                # Vertical Y direction
                vectors = np.column_stack([
                    np.zeros_like(scalar_values),
                    scalar_values,
                    np.zeros_like(scalar_values)
                ])
            else:
                return None
            
            return vectors
            
        except Exception as e:
            logger.exception(f"Error calculating vectors: {e}")
            return None
    
    def _get_velocity_vectors_from_nodes(self, mesh):
        """Get velocity vectors"""
        try:
            cell_centers = mesh.cell_centers()
            points = cell_centers.points
            
            return points, None
                
        except Exception as e:
            logger.exception(f"Error getting velocity vectors: {e}")
            return None, None
    
    def display_mesh_with_constraints(self, plotter, mesh, mesh_color, edge_color, show_edges=True, show_constraints=False):
        """Display mesh with optional constraints"""
        # Display normal mesh first
        self.display_mesh(plotter, mesh, mesh_color, edge_color, show_edges)
        
        # Add constraints if requested
        if show_constraints:
            self._add_constraints_visualization(plotter, mesh)
    
    def _add_constraints_visualization(self, plotter, mesh):
        """Add constraint visualizations based on node codes"""
        
        constraint_info = mesh._constraint_info
        node_ids = constraint_info['node_ids']
        positions_x = constraint_info['positions_x']
        positions_y = constraint_info['positions_y']
        constraint_codes = constraint_info['codes']
        
        constraint_size = self._calculate_proportional_size(mesh, base_factor=0.01)
        
        # Determine optimal level of detail
        total_constraints = len([code for code in constraint_codes if code != 0])
        subdivisions, _ = self._get_optimal_lod(total_constraints)
        
        # Group constraints by type
        constraint_groups = {}
        
        for i in range(len(node_ids)):
            code = constraint_codes[i]
            position = [positions_x[i], positions_y[i], 0]
            
            if code == 0:
                continue
                
            config = self._get_constraint_config(code)
            if config:
                group_key = config['name']
                if group_key not in constraint_groups:
                    constraint_groups[group_key] = {
                        'positions': [],
                        'config': config,
                        'codes': []
                    }
                constraint_groups[group_key]['positions'].append(position)
                constraint_groups[group_key]['codes'].append(code)
        
        self._create_batched_constraint_spheres(plotter, constraint_groups, constraint_size, subdivisions)
        
        # Add contact nodes
        self._add_contact_nodes_visualization(plotter, mesh, constraint_size, subdivisions)
        
        
    def _create_batched_constraint_spheres(self, plotter, constraint_groups, radius, subdivisions):
        """Create constraint spheres in batches"""
        
        for group_name, group_data in constraint_groups.items():
            positions = group_data['positions']
            config = group_data['config']
            
            if positions:
                # Create spheres in batch
                glyphs = self._create_batched_spheres(positions, radius, subdivisions)
                
                if glyphs:
                    plotter.add_mesh(
                        glyphs,
                        color=config['color'],
                        opacity=1.0,
                        name=group_name,
                        render=False  # Don't render immediately
                    )
                    logger.info(f"Added {len(positions)} {config['description']} ({group_name})")
        
        # Render all at once
        plotter.render()
    
    def _add_contact_nodes_visualization(self, plotter, mesh, constraint_size, subdivisions):
        """Add pink spheres for contact nodes"""
        nodes = mesh._original_data.get_nodes()
        contact_positions = []
        
        for node in nodes:
            if node.is_contact_node():
                contact_positions.append([node.get_coordX(), node.get_coordY(), 0])
        
        if contact_positions:
            # Use centralized configuration for contacts
            contact_config = self.CONSTRAINT_CONFIG['contact']
            
            # Create all contact spheres in batch
            glyphs = self._create_batched_spheres(contact_positions, constraint_size, subdivisions)
            
            if glyphs:
                plotter.add_mesh(
                    glyphs,
                    color=contact_config['color'],
                    opacity=1.0,
                    name=contact_config['name'],
                    render=False
                )
    
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