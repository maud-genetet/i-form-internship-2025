
"""
Main Visualization Module - Configuration and Main Controls
"""

import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QCheckBox, QSpinBox)
from pyvistaqt import QtInteractor
import pyvista as pv

try:
    from .mesh_builder import MeshBuilder
    from .interaction_handler import InteractionHandler
    from .display_modes import DisplayModeManager
except ImportError:
    # Fallback for direct import
    from modules.visualization.mesh_builder import MeshBuilder
    from modules.visualization.interaction_handler import InteractionHandler
    from modules.visualization.display_modes import DisplayModeManager


class VisualizationManager:
    """
    Centralized manager for PyVista visualization
    Shared between all application modules
    """
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.plotter = None
        self.visualization_widget = None
        self.current_data = None
        self.current_dir = None
        self.current_mesh = None
        
        # Default configuration
        self.default_mesh_color = 'yellow'
        self.default_edge_color = 'black'
        self.default_node_color = 'black'
        
        # Specialized modules
        self.mesh_builder = MeshBuilder()
        self.interaction_handler = InteractionHandler()
        self.display_manager = DisplayModeManager()
        
        self._setup_visualization_widget()
    
    def _setup_visualization_widget(self):
        """Configure main visualization widget"""
        self.visualization_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Toolbar
        self._create_toolbar(main_layout)
        
        # PyVista visualization area
        self.plotter = QtInteractor(self.visualization_widget)
        main_layout.addWidget(self.plotter.interactor)
        
        self.visualization_widget.setLayout(main_layout)
        
        # Plotter configuration
        self._configure_plotter()
    
    def _configure_plotter(self):
        """Configure plotter with automatic click zoom"""
        self.plotter.show_axes()
        self.plotter.view_xy()
        
        # Initialize interaction handler
        self.interaction_handler.setup(self.plotter)
    
    def _create_toolbar(self, main_layout):
        """Create control toolbar"""
        toolbar_layout = QHBoxLayout()
        
        # Data information
        self.data_info_label = QLabel("No data")
        toolbar_layout.addWidget(self.data_info_label)
        
        toolbar_layout.addStretch()

        # Wireframe checkbox
        self.wireframe_checkbox = QCheckBox("Wireframe")
        self.wireframe_checkbox.toggled.connect(self._on_wireframe_toggled)
        toolbar_layout.addWidget(self.wireframe_checkbox)
        
        # Control buttons
        reset_btn = QPushButton("Reset View")
        reset_btn.clicked.connect(self.reset_view)
        toolbar_layout.addWidget(reset_btn)
        
        # Front view button
        front_view_btn = QPushButton("Front View")
        front_view_btn.clicked.connect(self.set_front_view)
        toolbar_layout.addWidget(front_view_btn)
        
        # Deformed mesh controls (hidden by default)
        self.deformed_controls_layout = QHBoxLayout()
        
        # Previous button
        self.prev_mesh_btn = QPushButton("◀")
        self.prev_mesh_btn.setMaximumWidth(30)
        self.prev_mesh_btn.clicked.connect(self._previous_mesh)
        self.prev_mesh_btn.setVisible(False)
        self.deformed_controls_layout.addWidget(self.prev_mesh_btn)
        
        # SpinBox for direct selection
        self.mesh_spinbox = QSpinBox()
        self.mesh_spinbox.setMinimumWidth(50)
        self.mesh_spinbox.setMaximumWidth(60)
        self.mesh_spinbox.valueChanged.connect(self._on_mesh_spinbox_changed)
        self.mesh_spinbox.setVisible(False)
        self.deformed_controls_layout.addWidget(self.mesh_spinbox)
        
        # Next button
        self.next_mesh_btn = QPushButton("▶")
        self.next_mesh_btn.setMaximumWidth(30)
        self.next_mesh_btn.clicked.connect(self._next_mesh)
        self.next_mesh_btn.setVisible(False)
        self.deformed_controls_layout.addWidget(self.next_mesh_btn)
        
        # Variables for deformed mesh
        self.neu_files = []
        self.working_directory = None
        self.load_mesh_callback = None
        self.current_mesh_index = 0
        
        toolbar_layout.addLayout(self.deformed_controls_layout)
        
        # Assembly
        toolbar_widget = QWidget()
        toolbar_widget.setLayout(toolbar_layout)
        toolbar_widget.setMaximumHeight(40)
        main_layout.addWidget(toolbar_widget)
    
    def _on_wireframe_toggled(self, checked):
        """Wireframe mode callback"""
        self.display_manager.set_wireframe_mode(checked)
        print(f"Wireframe mode: {'ON' if checked else 'OFF'}")
        
        if self.current_data:
            self.visualize_mesh()
    
    # === DEFORMED MESH METHODS ===
    
    def add_deformed_mesh_controls(self, neu_files, working_directory, load_callback):
        """Add navigation controls for deformed mesh"""
        self.neu_files = neu_files
        self.working_directory = working_directory
        self.load_mesh_callback = load_callback
        self.current_mesh_index = 0
        
        # Configure spinbox
        self.mesh_spinbox.setMinimum(1)
        self.mesh_spinbox.setMaximum(len(neu_files))
        self.mesh_spinbox.setValue(1)
        
        # Show controls
        self.prev_mesh_btn.setVisible(True)
        self.mesh_spinbox.setVisible(True)
        self.next_mesh_btn.setVisible(True)
        
        # Update button states
        self._update_mesh_controls_state()
        
    def hide_deformed_mesh_controls(self):
        """Hide deformed mesh navigation controls"""
        self.prev_mesh_btn.setVisible(False)
        self.mesh_spinbox.setVisible(False)
        self.next_mesh_btn.setVisible(False)
    
    def _previous_mesh(self):
        """Load previous mesh file"""
        if self.current_mesh_index > 0:
            self.current_mesh_index -= 1
            self._load_current_mesh()
            self._update_mesh_controls_state()
    
    def _next_mesh(self):
        """Load next mesh file"""
        if self.current_mesh_index < len(self.neu_files) - 1:
            self.current_mesh_index += 1
            self._load_current_mesh()
            self._update_mesh_controls_state()
    
    def _on_mesh_spinbox_changed(self, value):
        """Spinbox value change callback"""
        new_index = value - 1  # Convert 1-based to 0-based
        if 0 <= new_index < len(self.neu_files):
            self.current_mesh_index = new_index
            self._load_current_mesh()
            self._update_mesh_controls_state()
    
    def _load_current_mesh(self):
        """Load current mesh file"""
        if self.neu_files and self.working_directory and self.load_mesh_callback:
            current_file = self.neu_files[self.current_mesh_index]
            file_path = f"{self.working_directory}/{current_file}"
            print(f"Loading file {self.current_mesh_index + 1}/{len(self.neu_files)}: {current_file}")
            self.load_mesh_callback(file_path)
    
    def _update_mesh_controls_state(self):
        """Update navigation controls state"""
        # Previous/next buttons
        self.prev_mesh_btn.setEnabled(self.current_mesh_index > 0)
        self.next_mesh_btn.setEnabled(self.current_mesh_index < len(self.neu_files) - 1)
        
        # SpinBox (block signals to avoid recursion)
        self.mesh_spinbox.blockSignals(True)
        self.mesh_spinbox.setValue(self.current_mesh_index + 1)
        self.mesh_spinbox.blockSignals(False)
    
    # === PUBLIC METHODS ===
    
    def get_widget(self):
        """Return visualization widget"""
        return self.visualization_widget
    
    def set_as_central_widget(self):
        """Set as central widget"""
        self.main_window.setCentralWidget(self.visualization_widget)
    
    def load_neutral_file(self, neutral_file):
        """Load neutral file for visualization"""
        self.current_data = neutral_file
        self._update_data_info()
        
        # Visualize mesh with dies
        self.visualize_mesh(show_edges=True, show_nodes=False, show_dies=True)
        
        # Reapply currently selected variable if exists
        if hasattr(self.main_window, 'field_variables_handler'):
            self.main_window.field_variables_handler.reapply_current_variable()

    def set_working_directory(self, dir_name):
        """Set working directory"""
        self.current_dir = dir_name
    
    def visualize_mesh(self, show_edges=True, show_nodes=False, show_dies=True):
        """Visualize mesh with specified options"""
        if not self.current_data:
            return
        
        self.clear()
        
        try:
            # Create mesh via builder
            mesh = self.mesh_builder.create_pyvista_mesh(self.current_data)
            if mesh:
                self.current_mesh = mesh
                
                # Display according to mode
                self.display_manager.display_mesh(
                    self.plotter, mesh, 
                    self.default_mesh_color, self.default_edge_color,
                    show_edges
                )
                
                # Additional elements
                if show_nodes:
                    self._add_nodes_to_plot()
                
                if show_dies:
                    self._add_dies_to_plot()

        except Exception as e:
            print(f"Visualization error: {e}")
        
        # Force rendering to ensure everything is displayed
        if self.plotter:
            self.plotter.render()
    
    def _update_data_info(self):
        """Update displayed information"""
        if self.current_data and self.current_dir:
            info = (f"Directory: {self.current_dir} | "
                   f"Nodes: {self.current_data.get_nb_nodes()} | "
                   f"Elements: {self.current_data.get_nb_elements()}")
            self.data_info_label.setText(info)
        elif self.current_dir:
            self.data_info_label.setText(f"Directory: {self.current_dir} | No data loaded")
        else:
            self.data_info_label.setText("No data")
    
    def _add_nodes_to_plot(self):
        """Add nodes to visualization"""
        if not self.current_data:
            return
        
        nodes = self.current_data.get_nodes()
        points = []
        
        for node in nodes:
            x = node.get_coordX() if node.get_coordX() is not None else 0.0
            y = node.get_coordY() if node.get_coordY() is not None else 0.0
            points.append([x, y, 0.0])
        
        if points:
            points_mesh = pv.PolyData(np.array(points))
            self.plotter.add_mesh(
                points_mesh,
                color=self.default_node_color,
                point_size=3,
                render_points_as_spheres=True,
                label="Node"
            )
    
    def _add_dies_to_plot(self):
        """Add dies to visualization"""
        if not self.current_data:
            return
        
        dies = self.current_data.get_dies()
        
        if not dies:
            print("No dies found in data")
            return
        
        print(f"Displaying {len(dies)} die(s)")
        
        for i, die in enumerate(dies):
            try:
                die_mesh = self.mesh_builder.create_die_mesh(die)
                if die_mesh:
                    self.display_manager.display_die(
                        self.plotter, die_mesh, die.get_id()
                    )
                    print(f"Die {die.get_id()} added")
                else:
                    print(f"Cannot create mesh for die {die.get_id()}")
            except Exception as e:
                print(f"Error adding die {i}: {e}")
    
    def clear(self):
        """Clear visualization"""
        if self.plotter:
            self.plotter.clear()
    
    def reset_view(self):
        """Reset view to default"""
        if self.plotter:
            self.plotter.reset_camera()
            self.plotter.view_xy()
    
    def set_front_view(self):
        """Set front view (XY plane) keeping current zoom"""
        if self.plotter:
            # Save current camera position to keep zoom
            camera = self.plotter.camera
            current_position = camera.position
            current_focal_point = camera.focal_point
            
            # Calculate current distance (to keep zoom)
            import numpy as np
            current_distance = np.linalg.norm(
                np.array(current_position) - np.array(current_focal_point)
            )
            
            # Set new orientation (front view XY)
            # Position: above focal point, looking down
            new_position = [
                current_focal_point[0],  # same X as focal point
                current_focal_point[1],  # same Y as focal point  
                current_focal_point[2] + current_distance  # Z = focal + distance
            ]
            
            # Apply new view
            camera.position = new_position
            camera.focal_point = current_focal_point
            camera.view_up = [0, 1, 0]  # Y upward
            
            # Render
            self.plotter.render()
            print("Front view activated (zoom preserved)")
    
    def export_image(self, filename):
        """Export current view as image"""
        if self.plotter:
            self.plotter.screenshot(filename)
    
    def get_current_data(self):
        """Return currently loaded data"""
        return self.current_data
    
    def add_custom_mesh(self, mesh, **kwargs):
        """Add custom mesh to visualization"""
        if self.plotter:
            self.plotter.add_mesh(mesh, **kwargs)