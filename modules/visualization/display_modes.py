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
    
    def display_mesh(self, plotter, mesh, mesh_color, edge_color, show_edges=True):
        """Display main mesh"""
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
        
        # Apply HD contour if needed
        if high_definition_contour:
            mesh = self._apply_hd_contour(mesh, scalar_name)
        
        # Choose colormap
        cmap = 'Blues' if monochromatic_mode else 'turbo'
        
        # Get scalar data
        scalars_array, use_point_data = self._get_scalar_data(mesh, scalar_name, high_definition_contour)
        
        # Add mesh with variable colors and wireframe overlay if needed
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
            
            self._create_constraint_shapes_from_arrays(plotter, node_ids, positions_x, positions_y, constraint_codes)
        
    def _create_constraint_shapes_from_arrays(self, plotter, node_ids, positions_x, positions_y, constraint_codes):
        """Create constraint shapes using arrays of node information"""
        constraint_size = 0.15

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