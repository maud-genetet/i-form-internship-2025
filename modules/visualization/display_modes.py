"""
Unified Display Modes Management Module
Handles all display modes in one place
"""

import numpy as np


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
            # Add wireframe overlay
            plotter.add_mesh(
                mesh,
                style='wireframe',
                color=edge_color,
                line_width=1,
                label=f"Wireframe Overlay"
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
        
        if use_point_data:
            print(f"HD Contour: Using smooth interpolation for {variable_name}")
    
    def _apply_hd_contour(self, mesh, scalar_name):
        """Apply high definition contour"""
        try:
            mesh_copy = mesh.copy()
            mesh_with_point_data = mesh_copy.cell_data_to_point_data()
            
            if scalar_name in mesh_with_point_data.point_data:
                return mesh_with_point_data
            else:
                return mesh_copy
        except Exception as e:
            print(f"HD Contour error: {e}")
            return mesh
    
    def _get_scalar_data(self, mesh, scalar_name, hd_contour_enabled):
        """Get scalar data"""
        use_point_data = (hd_contour_enabled and 
                         hasattr(mesh, 'point_data') and 
                         scalar_name in mesh.point_data)
        
        if use_point_data:
            return mesh.point_data[scalar_name], True
        else:
            return mesh.cell_data[scalar_name], False