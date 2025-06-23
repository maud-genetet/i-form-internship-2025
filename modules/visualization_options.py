"""
Unified Visualization Options Manager
Handles all visualization options including wireframe and line contour
"""

from PyQt5.QtWidgets import QCheckBox, QLabel


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
        self.line_contour_mode = False  # NEW: Line contour option
        
        # UI controls
        self.wireframe_checkbox = None
        self.mesh_edges_checkbox = None
        self.monochromatic_checkbox = None
        self.hd_contour_checkbox = None
        self.constraints_checkbox = None
        self.line_contour_checkbox = None  # NEW: Line contour checkbox
        
        self._setup_controls()
    
    def _setup_controls(self):
        """Setup UI controls in the toolbar"""
        visualization_manager = self._get_visualization_manager()
        if not visualization_manager or not hasattr(visualization_manager, 'visualization_widget'):
            return
            
        # Find the toolbar layout
        main_layout = visualization_manager.visualization_widget.layout()
        if main_layout.count() > 0:
            toolbar_widget = main_layout.itemAt(0).widget()
            toolbar_layout = toolbar_widget.layout()
            
            self._add_all_controls_to_toolbar(toolbar_layout)
    
    def _add_all_controls_to_toolbar(self, toolbar_layout):
        """Add all visualization controls together"""
        # Add separator before our controls
        separator = QLabel(" | ")
        toolbar_layout.addWidget(separator)
        
        # Add wireframe checkbox (moved from original position)
        self.wireframe_checkbox = QCheckBox("Wireframe")
        self.wireframe_checkbox.setChecked(self.wireframe_mode)
        self.wireframe_checkbox.toggled.connect(self._on_wireframe_toggled)
        toolbar_layout.addWidget(self.wireframe_checkbox)
        
        # Add mesh edges checkbox
        self.mesh_edges_checkbox = QCheckBox("Show Mesh")
        self.mesh_edges_checkbox.setChecked(self.show_mesh_edges)
        self.mesh_edges_checkbox.toggled.connect(self._on_mesh_edges_toggled)
        toolbar_layout.addWidget(self.mesh_edges_checkbox)
        
        # Add constraints checkbox
        self.constraints_checkbox = QCheckBox("View Constraints")
        self.constraints_checkbox.setChecked(self.view_constraints)
        self.constraints_checkbox.toggled.connect(self._on_constraints_toggled)
        toolbar_layout.addWidget(self.constraints_checkbox)
        
        # Add monochromatic mode checkbox
        self.monochromatic_checkbox = QCheckBox("Monochromatic")
        self.monochromatic_checkbox.setChecked(self.monochromatic_mode)
        self.monochromatic_checkbox.toggled.connect(self._on_monochromatic_toggled)
        toolbar_layout.addWidget(self.monochromatic_checkbox)
        
        # Add high definition contour checkbox
        self.hd_contour_checkbox = QCheckBox("HD Contour")
        self.hd_contour_checkbox.setChecked(self.high_definition_contour)
        self.hd_contour_checkbox.toggled.connect(self._on_hd_contour_toggled)
        toolbar_layout.addWidget(self.hd_contour_checkbox)
        
        # NEW: Add line contour checkbox
        self.line_contour_checkbox = QCheckBox("Line Contour")
        self.line_contour_checkbox.setChecked(self.line_contour_mode)
        self.line_contour_checkbox.toggled.connect(self._on_line_contour_toggled)
        toolbar_layout.addWidget(self.line_contour_checkbox)
        
        # Add remove variables button
        from PyQt5.QtWidgets import QPushButton
        self.remove_variables_btn = QPushButton("Remove Variables")
        self.remove_variables_btn.clicked.connect(self._on_remove_variables_clicked)
        toolbar_layout.addWidget(self.remove_variables_btn)
    
    def _get_visualization_manager(self):
        """Get visualization manager from main window"""
        return getattr(self.main_window, 'visualization_manager', None)
    
    def _on_wireframe_toggled(self, checked):
        """Handle wireframe mode toggle"""
        self.wireframe_mode = checked
        self._get_visualization_manager().display_manager.set_wireframe_mode(checked)
        print(f"Wireframe mode: {'ON' if checked else 'OFF'}")
        self._refresh_display()
    
    def _on_mesh_edges_toggled(self, checked):
        """Handle mesh edges toggle"""
        self.show_mesh_edges = checked
        print(f"Show mesh edges: {'ON' if checked else 'OFF'}")
        self._refresh_display()
    
    def _on_constraints_toggled(self, checked):
        """Handle constraints view toggle"""
        self.view_constraints = checked
        print(f"View constraints: {'ON' if checked else 'OFF'}")
        self._refresh_display()
    
    def _on_monochromatic_toggled(self, checked):
        """Handle monochromatic mode toggle"""
        self.monochromatic_mode = checked
        print(f"Monochromatic mode: {'ON' if checked else 'OFF'}")
        self._refresh_display()
    
    def _on_hd_contour_toggled(self, checked):
        """Handle HD contour toggle"""
        self.high_definition_contour = checked
        print(f"HD Contour mode: {'ON' if checked else 'OFF'}")
        self._refresh_display()
    
    # NEW: Line contour toggle handler
    def _on_line_contour_toggled(self, checked):
        """Handle line contour mode toggle"""
        self.line_contour_mode = checked
        print(f"Line Contour mode: {'ON' if checked else 'OFF'}")
        self._refresh_display()
    
    def _on_remove_variables_clicked(self):
        """Handle remove variables button click"""
        print("Removing variables - returning to geometry view")
        if hasattr(self.main_window, 'field_variables_handler'):
            self.main_window.field_variables_handler.standard_options()
    
    def _refresh_display(self):
        """Refresh current display when options change"""
        if hasattr(self.main_window, 'field_variables_handler'):
            self.main_window.field_variables_handler.reapply_current_variable()
    
    def get_current_options(self):
        """Get all current options as a dictionary"""
        return {
            'wireframe_mode': self.wireframe_mode,
            'show_mesh_edges': self.show_mesh_edges,
            'monochromatic_mode': self.monochromatic_mode,
            'high_definition_contour': self.high_definition_contour,
            'view_constraints': self.view_constraints,
            'line_contour_mode': self.line_contour_mode
        }