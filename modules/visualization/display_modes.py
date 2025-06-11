
"""
Display Modes Management Module (normal, wireframe, variables)
"""

class DisplayModeManager:
    """Manager for different display modes"""
    
    def __init__(self):
        self.wireframe_mode = False
    
    def set_wireframe_mode(self, enabled):
        """Enable/disable wireframe mode"""
        self.wireframe_mode = enabled
    
    def display_mesh(self, plotter, mesh, mesh_color, edge_color, show_edges=True):
        """Display main mesh according to current mode"""
        if self.wireframe_mode:
            # Wireframe mode: only edges
            plotter.add_mesh(
                mesh,
                style='wireframe', 
                color=edge_color,
                line_width=1,
                label="Mesh - Wireframe"
            )
        else:
            # Normal mode: opaque mesh with edges
            plotter.add_mesh(
                mesh,
                show_edges=show_edges,
                edge_color=edge_color,
                line_width=1,
                color=mesh_color,
                opacity=1.0,
                label="Mesh"
            )
    
    def display_die(self, plotter, die_mesh, die_id):
        """Display die according to current mode"""
        if self.wireframe_mode:
            # Wireframe mode: only outlines
            plotter.add_mesh(
                die_mesh,
                style='wireframe',
                color='red',
                line_width=1,
                label=f"Die {die_id} - Wireframe"
            )
        else:
            # Normal mode: opaque die
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
        """Display variables according to current mode"""
        plotter.add_mesh(
            mesh,
            scalars=scalar_name,
            show_edges=True,
            edge_color=edge_color,
            line_width=1,
            opacity=1.0,
            cmap='turbo',  # Colormap with more colors
            show_scalar_bar=True,
            label=f"Mesh - {variable_name}"
        )

