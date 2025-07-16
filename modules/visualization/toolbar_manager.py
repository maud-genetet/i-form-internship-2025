"""
Toolbar Manager
Centralizes all toolbar-related functionality
"""

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
                             QPushButton, QCheckBox, QSpinBox, QProgressBar)


class ToolbarManager:
    """Centralized manager for all toolbar components"""
    
    def __init__(self, main_window, visualization_manager):
        self.main_window = main_window
        self.visualization_manager = visualization_manager
        
        # Toolbar components
        self.top_toolbar_widget = None
        self.bottom_toolbar_widget = None
        
        # Navigation components
        self.data_info_label = None
        self.prev_mesh_btn = None
        self.next_mesh_btn = None
        self.mesh_spinbox = None
        
        # View components
        self.reset_view_btn = None
        self.front_view_btn = None
        self.mesh_info_btn = None
        
        # Visualization options
        self.wireframe_checkbox = None
        self.mesh_edges_checkbox = None
        self.constraints_checkbox = None
        self.constraint_size_spinbox = None
        self.monochromatic_checkbox = None
        self.hd_contour_checkbox = None
        self.line_contour_checkbox = None
        self.vector_checkbox = None
        self.vector_size_spinbox = None
        self.remove_variables_btn = None
        
        # Progress components
        self.progress_label = None
        self.progress_bar = None
        
        # State
        self.visualization_options = {}
    
    def create_toolbars(self, main_layout):
        """Create both top and bottom toolbars"""
        self._create_top_toolbar(main_layout)
        self._create_bottom_toolbar(main_layout)
    
    def _create_top_toolbar(self, main_layout):
        """Create top toolbar with all controls"""
        toolbar_layout = QHBoxLayout()
        
        # === LEFT SECTION: Data Info ===
        self._add_data_info_section(toolbar_layout)
        
        toolbar_layout.addStretch()
        
        # === CENTER SECTION: Navigation ===
        self._add_navigation_section(toolbar_layout)
        
        # === RIGHT SECTION: View Controls ===
        self._add_view_controls_section(toolbar_layout)
        
        # === VISUALIZATION OPTIONS ===
        self._add_visualization_options_section(toolbar_layout)
        
        # Assembly
        self.top_toolbar_widget = QWidget()
        self.top_toolbar_widget.setLayout(toolbar_layout)
        self.top_toolbar_widget.setMaximumHeight(40)
        main_layout.addWidget(self.top_toolbar_widget)
    
    def _add_data_info_section(self, toolbar_layout):
        """Add data information section"""
        self.data_info_label = QLabel("No data")
        toolbar_layout.addWidget(self.data_info_label)
    
    def _add_navigation_section(self, toolbar_layout):
        """Add mesh navigation section"""
        # Previous button
        self.prev_mesh_btn = QPushButton("◀")
        self.prev_mesh_btn.setMaximumWidth(30)
        self.prev_mesh_btn.clicked.connect(self._on_previous_mesh)
        self.prev_mesh_btn.setVisible(False)
        toolbar_layout.addWidget(self.prev_mesh_btn)
        
        # SpinBox for direct selection
        self.mesh_spinbox = QSpinBox()
        self.mesh_spinbox.setMinimumWidth(50)
        self.mesh_spinbox.setMaximumWidth(60)
        self.mesh_spinbox.valueChanged.connect(self._on_mesh_spinbox_changed)
        self.mesh_spinbox.setVisible(False)
        toolbar_layout.addWidget(self.mesh_spinbox)
        
        # Next button
        self.next_mesh_btn = QPushButton("▶")
        self.next_mesh_btn.setMaximumWidth(30)
        self.next_mesh_btn.clicked.connect(self._on_next_mesh)
        self.next_mesh_btn.setVisible(False)
        toolbar_layout.addWidget(self.next_mesh_btn)
    
    def _add_view_controls_section(self, toolbar_layout):
        """Add view control buttons"""
        # Reset view button
        self.reset_view_btn = QPushButton("Reset View")
        self.reset_view_btn.clicked.connect(self._on_reset_view)
        toolbar_layout.addWidget(self.reset_view_btn)
        
        # Front view button
        self.front_view_btn = QPushButton("Front View")
        self.front_view_btn.clicked.connect(self._on_front_view)
        toolbar_layout.addWidget(self.front_view_btn)
        
        # Mesh info button
        self.mesh_info_btn = QPushButton("Mesh Info")
        self.mesh_info_btn.setCheckable(True)
        self.mesh_info_btn.clicked.connect(self._on_mesh_info_clicked)
        toolbar_layout.addWidget(self.mesh_info_btn)
    
    def _add_visualization_options_section(self, toolbar_layout):
        """Add all visualization options"""
        # Separator
        separator = QLabel(" | ")
        toolbar_layout.addWidget(separator)
        
        # Wireframe mode
        self.wireframe_checkbox = QCheckBox("Wireframe")
        self.wireframe_checkbox.toggled.connect(self._on_wireframe_toggled)
        toolbar_layout.addWidget(self.wireframe_checkbox)
        
        # Show mesh edges
        self.mesh_edges_checkbox = QCheckBox("Show Mesh")
        self.mesh_edges_checkbox.setChecked(True)
        self.mesh_edges_checkbox.toggled.connect(self._on_mesh_edges_toggled)
        toolbar_layout.addWidget(self.mesh_edges_checkbox)
        
        # View constraints
        self.constraints_checkbox = QCheckBox("View Constraints")
        self.constraints_checkbox.toggled.connect(self._on_constraints_toggled)
        toolbar_layout.addWidget(self.constraints_checkbox)
        
        # Constraint size control
        constraint_size_label = QLabel("Size:")
        toolbar_layout.addWidget(constraint_size_label)
        
        self.constraint_size_spinbox = QSpinBox()
        self.constraint_size_spinbox.setRange(1, 500)
        self.constraint_size_spinbox.setValue(50)
        self.constraint_size_spinbox.setSuffix("%")
        self.constraint_size_spinbox.valueChanged.connect(self._on_constraint_size_changed)
        toolbar_layout.addWidget(self.constraint_size_spinbox)
        
        # Monochromatic mode
        self.monochromatic_checkbox = QCheckBox("Monochromatic")
        self.monochromatic_checkbox.toggled.connect(self._on_monochromatic_toggled)
        toolbar_layout.addWidget(self.monochromatic_checkbox)
        
        # HD Contour
        self.hd_contour_checkbox = QCheckBox("HD Contour")
        self.hd_contour_checkbox.toggled.connect(self._on_hd_contour_toggled)
        toolbar_layout.addWidget(self.hd_contour_checkbox)
        
        # Line Contour
        self.line_contour_checkbox = QCheckBox("Line Contour")
        self.line_contour_checkbox.toggled.connect(self._on_line_contour_toggled)
        toolbar_layout.addWidget(self.line_contour_checkbox)
        
        # Vector mode
        self.vector_checkbox = QCheckBox("Vector")
        self.vector_checkbox.toggled.connect(self._on_vector_toggled)
        toolbar_layout.addWidget(self.vector_checkbox)
        
        # Vector size control
        vector_size_label = QLabel("Size:")
        toolbar_layout.addWidget(vector_size_label)
        
        self.vector_size_spinbox = QSpinBox()
        self.vector_size_spinbox.setRange(1, 500)
        self.vector_size_spinbox.setValue(50)
        self.vector_size_spinbox.setSuffix("%")
        self.vector_size_spinbox.valueChanged.connect(self._on_vector_size_changed)
        toolbar_layout.addWidget(self.vector_size_spinbox)
        
        # Remove variables button
        self.remove_variables_btn = QPushButton("Remove Variables")
        self.remove_variables_btn.clicked.connect(self._on_remove_variables_clicked)
        toolbar_layout.addWidget(self.remove_variables_btn)
    
    def _create_bottom_toolbar(self, main_layout):
        """Create bottom toolbar with progress controls"""
        bottom_toolbar_layout = QHBoxLayout()
        
        # Progress controls
        self.progress_label = QLabel("Ready")
        self.progress_label.setMinimumWidth(50)
        self.progress_label.setVisible(False)
        bottom_toolbar_layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setMaximumHeight(20)
        self.progress_bar.setVisible(False)
        bottom_toolbar_layout.addWidget(self.progress_bar)
        
        bottom_toolbar_layout.addStretch()
        
        self.bottom_toolbar_widget = QWidget()
        self.bottom_toolbar_widget.setLayout(bottom_toolbar_layout)
        self.bottom_toolbar_widget.setMaximumHeight(40)
        main_layout.addWidget(self.bottom_toolbar_widget)
    
    # === EVENT HANDLERS ===
    
    def _on_previous_mesh(self):
        """Handle previous mesh button"""
        self.visualization_manager._previous_mesh()
    
    def _on_next_mesh(self):
        """Handle next mesh button"""
        self.visualization_manager._next_mesh()
    
    def _on_mesh_spinbox_changed(self, value):
        """Handle mesh spinbox change"""
        self.visualization_manager._on_mesh_spinbox_changed(value)
    
    def _on_reset_view(self):
        """Handle reset view button"""
        self.visualization_manager.reset_view()
    
    def _on_front_view(self):
        """Handle front view button"""
        self.visualization_manager.set_front_view()
    
    def _on_mesh_info_clicked(self, checked):
        """Handle mesh info button"""
        if checked:
            self.visualization_manager._show_info_panel()
            self.visualization_manager.interaction_handler.enable_mesh_picking()
        else:
            self.visualization_manager._hide_info_panel()
            self.visualization_manager.interaction_handler.disable_mesh_picking()
    
    def _on_wireframe_toggled(self, checked):
        """Handle wireframe toggle"""
        self.visualization_options['wireframe_mode'] = checked
        self.visualization_manager.display_manager.set_wireframe_mode(checked)
        self._refresh_display()
    
    def _on_mesh_edges_toggled(self, checked):
        """Handle mesh edges toggle"""
        self.visualization_options['show_mesh_edges'] = checked
        self._refresh_display()
    
    def _on_constraints_toggled(self, checked):
        """Handle constraints toggle"""
        self.visualization_options['view_constraints'] = checked
        self._refresh_display()
    
    def _on_constraint_size_changed(self, value):
        """Handle constraint size change"""
        self.visualization_options['constraint_size_factor'] = value / 100.0
        self._refresh_display()
    
    def _on_monochromatic_toggled(self, checked):
        """Handle monochromatic toggle"""
        self.visualization_options['monochromatic_mode'] = checked
        self._refresh_display()
    
    def _on_hd_contour_toggled(self, checked):
        """Handle HD contour toggle"""
        self.visualization_options['high_definition_contour'] = checked
        self._refresh_display()
    
    def _on_line_contour_toggled(self, checked):
        """Handle line contour toggle"""
        self.visualization_options['line_contour_mode'] = checked
        self._refresh_display()
    
    def _on_vector_toggled(self, checked):
        """Handle vector toggle"""
        self.visualization_options['vector_mode'] = checked
        self._refresh_display()
    
    def _on_vector_size_changed(self, value):
        """Handle vector size change"""
        self.visualization_options['vector_size_factor'] = value / 100.0
        self._refresh_display()
    
    def _on_remove_variables_clicked(self):
        """Handle remove variables button"""
        if hasattr(self.main_window, 'field_variables_handler'):
            self.main_window.field_variables_handler.standard_options()
    
    def _refresh_display(self):
        """Refresh display when options change"""
        if hasattr(self.main_window, 'field_variables_handler'):
            self.main_window.field_variables_handler.reapply_current_variable()
    
    # === PUBLIC INTERFACE ===
    
    def get_current_options(self):
        """Get all current visualization options"""
        return {
            'wireframe_mode': self.wireframe_checkbox.isChecked() if self.wireframe_checkbox else False,
            'show_mesh_edges': self.mesh_edges_checkbox.isChecked() if self.mesh_edges_checkbox else True,
            'monochromatic_mode': self.monochromatic_checkbox.isChecked() if self.monochromatic_checkbox else False,
            'high_definition_contour': self.hd_contour_checkbox.isChecked() if self.hd_contour_checkbox else False,
            'view_constraints': self.constraints_checkbox.isChecked() if self.constraints_checkbox else False,
            'line_contour_mode': self.line_contour_checkbox.isChecked() if self.line_contour_checkbox else False,
            'vector_mode': self.vector_checkbox.isChecked() if self.vector_checkbox else False,
            'constraint_size_factor': self.constraint_size_spinbox.value() / 100.0 if self.constraint_size_spinbox else 1.0,
            'vector_size_factor': self.vector_size_spinbox.value() / 100.0 if self.vector_size_spinbox else 1.0
        }
        
    def update_data_info(self, info_text):
        """Update data information display"""
        if self.data_info_label:
            self.data_info_label.setText(info_text)
    
    def show_navigation_controls(self, neu_files):
        """Show navigation controls for deformed mesh"""
        if self.mesh_spinbox:
            self.mesh_spinbox.setMinimum(1)
            self.mesh_spinbox.setMaximum(len(neu_files))
            self.mesh_spinbox.setValue(1)
            
        if self.prev_mesh_btn:
            self.prev_mesh_btn.setVisible(True)
        if self.mesh_spinbox:
            self.mesh_spinbox.setVisible(True)
        if self.next_mesh_btn:
            self.next_mesh_btn.setVisible(True)
    
    def hide_navigation_controls(self):
        """Hide navigation controls"""
        if self.prev_mesh_btn:
            self.prev_mesh_btn.setVisible(False)
        if self.mesh_spinbox:
            self.mesh_spinbox.setVisible(False)
        if self.next_mesh_btn:
            self.next_mesh_btn.setVisible(False)
    
    def update_navigation_state(self, current_index, max_index):
        """Update navigation controls state"""
        if self.prev_mesh_btn:
            self.prev_mesh_btn.setEnabled(current_index > 0)
        if self.next_mesh_btn:
            self.next_mesh_btn.setEnabled(current_index < max_index - 1)
        if self.mesh_spinbox:
            self.mesh_spinbox.blockSignals(True)
            self.mesh_spinbox.setValue(current_index + 1)
            self.mesh_spinbox.blockSignals(False)
    
    def show_progress(self, message="Loading..."):
        """Show progress controls"""
        if self.progress_label:
            self.progress_label.setText(message)
            self.progress_label.setVisible(True)
        if self.progress_bar:
            self.progress_bar.setVisible(True)
    
    def hide_progress(self):
        """Hide progress controls"""
        if self.progress_label:
            self.progress_label.setVisible(False)
        if self.progress_bar:
            self.progress_bar.setVisible(False)
    
    def update_progress(self, percentage, message):
        """Update progress display"""
        if self.progress_bar:
            self.progress_bar.setValue(percentage)
        if self.progress_label:
            self.progress_label.setText(message)