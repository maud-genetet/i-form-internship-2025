"""
Unified Visualization Options Manager
Handles all visualization options including wireframe and line contour
"""

class VisualizationOptions:
    """Manages all visualization options in one place"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        
        # All visualization options
        self.wireframe_mode = False
        self.show_mesh_edges = True
        self.monochromatic_mode = False
        self.high_definition_contour = False
        self.view_constraints = False
        self.line_contour_mode = False
        self.vector_mode = False
        
        self.constraint_size_factor = 1.0
        self.vector_size_factor = 1.0
    
    def get_current_options(self):
        """Get all current options as a dictionary"""
        return {
            'wireframe_mode': self.wireframe_mode,
            'show_mesh_edges': self.show_mesh_edges,
            'monochromatic_mode': self.monochromatic_mode,
            'high_definition_contour': self.high_definition_contour,
            'view_constraints': self.view_constraints,
            'line_contour_mode': self.line_contour_mode,
            'vector_mode': self.vector_mode,
            'constraint_size_factor': self.constraint_size_factor,
            'vector_size_factor': self.vector_size_factor
        }
    
    def update_options(self, options_dict):
        """Update multiple options at once"""
        for key, value in options_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def set_wireframe_mode(self, enabled):
        """Set wireframe mode"""
        self.wireframe_mode = enabled
        self._refresh_display()
    
    def set_show_mesh_edges(self, enabled):
        """Set show mesh edges"""
        self.show_mesh_edges = enabled
        self._refresh_display()
    
    def set_monochromatic_mode(self, enabled):
        """Set monochromatic mode"""
        self.monochromatic_mode = enabled
        self._refresh_display()
    
    def set_hd_contour(self, enabled):
        """Set HD contour mode"""
        self.high_definition_contour = enabled
        self._refresh_display()
    
    def set_view_constraints(self, enabled):
        """Set view constraints"""
        self.view_constraints = enabled
        self._refresh_display()
    
    def set_line_contour_mode(self, enabled):
        """Set line contour mode"""
        self.line_contour_mode = enabled
        self._refresh_display()
    
    def set_vector_mode(self, enabled):
        """Set vector mode"""
        self.vector_mode = enabled
        self._refresh_display()
    
    def set_constraint_size_factor(self, factor):
        """Set constraint size factor"""
        self.constraint_size_factor = factor
        self._refresh_display()
    
    def set_vector_size_factor(self, factor):
        """Set vector size factor"""
        self.vector_size_factor = factor
        self._refresh_display()
    
    def _refresh_display(self):
        """Refresh current display when options change"""
        if hasattr(self.main_window, 'field_variables_handler'):
            self.main_window.field_variables_handler.reapply_current_variable()