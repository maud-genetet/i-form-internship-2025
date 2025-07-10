"""
User Interaction Management Module (click zoom, keyboard shortcuts, cell picking)
"""

import numpy as np
import vtk
from PyQt5.QtCore import QTimer
import pyvista as pv
from PyQt5.QtWidgets import QButtonGroup, QRadioButton, QHBoxLayout, QLabel
import time

class InteractionHandler:
    """Manager for user interactions with visualization"""
    
    def __init__(self):
        self.plotter = None
        self.current_mesh = None
        self.current_data = None
        self.info_panel = None
        self.info_content = None
        self.info_title = None
        self.picking_enabled = False
        self.last_click_time = 0
        self.click_debounce_delay = 0.2  # 200ms delay between clicks
        
        self.pick_mode = "elements"  # elements or "nodes
        self.mode_controls = None
    
    def setup(self, plotter):
        """Configure interactions on plotter"""
        self.plotter = plotter
    
    def set_mesh_data(self, mesh, data):
        """Set current mesh and data for picking operations"""
        self.current_mesh = mesh
        self.current_data = data
    
    def set_info_panel(self, info_panel, info_content, info_title):
        """Set info panel components for displaying cell information"""
        self.info_panel = info_panel
        self.info_content = info_content
        self.info_title = info_title
        
        # Add mode selection controls to the info panel
        self._add_mode_controls()
    
    def _add_mode_controls(self):
        """Add radio buttons to select between element and node picking"""
        if not self.info_panel:
            return
            
        # Create mode selection controls
        mode_layout = QHBoxLayout()
        
        mode_label = QLabel("Pick Mode:")
        mode_layout.addWidget(mode_label)
        
        # Create radio buttons
        self.element_radio = QRadioButton("Elements")
        self.node_radio = QRadioButton("Nodes")
        
        # Set default selection
        self.element_radio.setChecked(True)
        
        # Create button group for mutual exclusion
        self.mode_button_group = QButtonGroup()
        self.mode_button_group.addButton(self.element_radio, 0)
        self.mode_button_group.addButton(self.node_radio, 1)
        
        # Connect signals
        self.element_radio.toggled.connect(self._on_mode_changed)
        self.node_radio.toggled.connect(self._on_mode_changed)
        
        mode_layout.addWidget(self.element_radio)
        mode_layout.addWidget(self.node_radio)
        
        # Add to info panel layout
        info_layout = self.info_panel.layout()
        if info_layout and info_layout.count() > 0:
            # Insert after the title
            info_layout.insertLayout(1, mode_layout)
    
    def _on_mode_changed(self):
        """Handle mode change between elements and nodes"""
        if self.element_radio.isChecked():
            self.pick_mode = "elements"
        else:
            self.pick_mode = "nodes"
        
        # Clear any current highlight
        self._clear_highlight()
    
    def _calculate_proportional_size(self, mesh, base_factor=0.006):
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
        
        # Element density factor (more elements = smaller spheres)
        n_elements = mesh.n_cells if hasattr(mesh, 'n_cells') else 1000
        density_factor = min(1.0, 1000.0 / n_elements) 
        
        # Calculate proportional size with density adjustment
        proportional_size = max_dimension * base_factor * density_factor
        
        # Ensure minimum and maximum sizes
        min_size = max_dimension * 0.0002
        max_size = max_dimension * 0.03
        
        proportional_size = max(min_size, min(proportional_size, max_size))
        
        return proportional_size
    
    def enable_mesh_picking(self):
        """Enable mesh picking with direct VTK approach"""
        if not self.plotter or not self.current_mesh:
            print("Cannot enable picking: missing plotter or mesh")
            return
            
        # Avoid multiple enabling
        if self.picking_enabled:
            return
            
        print(f"Enabling picking on mesh with {self.current_mesh.n_cells} cells")
        
        self.plotter.disable_picking()
        
        # Get the VTK render window interactor
        interactor = self.plotter.iren
        
        # Remove existing observers to avoid conflicts
        interactor.remove_observer('LeftButtonPressEvent')
        
        # Add our custom click handler
        interactor.add_observer('LeftButtonPressEvent', self._vtk_click_handler)
        self.picking_enabled = True
        print("Mesh picking enabled")
    
    def disable_mesh_picking(self):
        """Disable mesh picking"""
        self.picking_enabled = False
        
        # Clear any highlights
        self._clear_highlight()
        
        # Remove VTK observers
        if self.plotter and self.plotter.iren:
            interactor = self.plotter.iren
            interactor.remove_observer('LeftButtonPressEvent')
        
        # Disable PyVista picking
        if self.plotter:
            self.plotter.disable_picking()
                
        print("Mesh info picking disabled")
    
    def reapply_mesh_picking_if_needed(self):
        """Reapply mesh picking after mesh operations"""
        if self.picking_enabled:
            print("Reapplying mesh picking after mesh update")
            # Reset the picking_enabled flag to allow re-enabling
            self.picking_enabled = False
            # Small delay to ensure mesh is fully loaded
            QTimer.singleShot(100, self.enable_mesh_picking)
    
    def _vtk_click_handler(self, obj, event):
        """Handle VTK click events for cell picking"""
        # Debounce clicks to avoid multiple triggers
        current_time = time.time()
        if current_time - self.last_click_time < self.click_debounce_delay:
            return
        self.last_click_time = current_time
        
        # Get click position
        interactor = self.plotter.iren
        x, y = interactor.get_event_position()
        renderer = self.plotter.renderer
        
        if self.pick_mode == "elements":
            self._pick_element(x, y, renderer)
        else:
            self._pick_node(x, y, renderer)
    
    def _pick_element(self, x, y, renderer):
        """Pick and display element information"""
        # Create a cell picker
        picker = vtk.vtkCellPicker()
        picker.SetTolerance(0.001)
        
        # Perform the pick
        result = picker.Pick(x, y, 0, renderer)
        if result:
            cell_id = picker.GetCellId()
            
            if cell_id >= 0:
                print(f"Picked cell ID: {cell_id}")
                self._display_cell_info(cell_id)
                self._highlight_picked_cell(cell_id)
            else:
                if self.info_content:
                    self.info_content.setText("No element found at click position")
    
    def _pick_node(self, x, y, renderer):
        """Pick and display node information"""
        if not self.current_mesh:
            return
            
        try:
            # Use a cell picker first to get approximate location
            cell_picker = vtk.vtkCellPicker()
            cell_picker.SetTolerance(0.01)
            
            cell_result = cell_picker.Pick(x, y, 0, renderer)
            if cell_result:
                # Get the picked position in world coordinates
                world_pos = cell_picker.GetPickPosition()
                
                # Find the closest node in the main mesh
                points = self.current_mesh.points
                distances = np.linalg.norm(points - np.array(world_pos), axis=1)
                closest_point_id = np.argmin(distances)
                
                # Calculate reasonable distance threshold
                bounds = self.current_mesh.bounds
                max_dimension = max(bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4])
                distance_threshold = max_dimension * 0.02  # 2% of mesh size
                
                min_distance = distances[closest_point_id]
                
                if min_distance <= distance_threshold:
                    print(f"Picked node ID: {closest_point_id}")
                    self._display_node_info(closest_point_id)
                    self._highlight_picked_node(closest_point_id)
                else:
                    if self.info_content:
                        self.info_content.setText("No node found at click position")
            else:
                if self.info_content:
                    self.info_content.setText("No mesh found at click position")
                    
        except Exception as e:
            print(f"Node picking error: {e}")
            if self.info_content:
                self.info_content.setText(f"Error in node picking: {e}")
    
    def _highlight_picked_cell(self, cell_id):
        """Highlight the picked cell visually"""
        if self.current_mesh and cell_id < self.current_mesh.n_cells:
            # Clear previous highlight
            self._clear_highlight()
            
            # Extract the single cell
            single_cell = self.current_mesh.extract_cells([cell_id])
            
            # Add it as a highlighted overlay
            self.plotter.add_mesh(
                single_cell,
                color='red',
                opacity=0.8,
                style='wireframe',
                line_width=4,
                name='picked_element_highlight'
            )
    
    def _highlight_picked_node(self, point_id):
        """Highlight the picked node visually"""
        if self.current_mesh and point_id < self.current_mesh.n_points:
            # Clear previous highlight
            self._clear_highlight()
            
            # Get node position
            node_position = self.current_mesh.points[point_id]
            
            # Calculate proportional sphere size
            sphere_radius = self._calculate_proportional_size(self.current_mesh, base_factor=0.011)
            
            # Create a sphere at the node position
            sphere = pv.Sphere(radius=sphere_radius, center=node_position)
            
            # Add it as a highlighted overlay
            self.plotter.add_mesh(
                sphere,
                color='blue',
                opacity=0.5,
                name='picked_node_highlight'
            )
    
    def _pick_node_fallback(self, x, y, renderer):
        """Fallback method for node picking using world coordinates"""
        try:
            # Use a generic picker to get world coordinates
            picker = vtk.vtkWorldPointPicker()
            result = picker.Pick(x, y, 0, renderer)
            
            if result and self.current_mesh:
                world_pos = picker.GetPickPosition()
                
                # Find closest point manually
                points = self.current_mesh.points
                distances = np.linalg.norm(points - np.array(world_pos), axis=1)
                closest_point_id = np.argmin(distances)
                
                # Check if the closest point is reasonably close
                min_distance = distances[closest_point_id]
                
                # Calculate reasonable distance threshold
                bounds = self.current_mesh.bounds
                max_dimension = max(bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4])
                distance_threshold = max_dimension * 0.01  # 1% of mesh size
                
                if min_distance <= distance_threshold:
                    self._display_node_info(closest_point_id)
                    self._highlight_picked_node(closest_point_id)
                else:
                    if self.info_content:
                        self.info_content.setText("No node found at click position (fallback)")
                        
        except Exception as e:
            print(f"Fallback picking error: {e}")
            if self.info_content:
                self.info_content.setText("Error in node picking")
    
    def _clear_highlight(self):
        """Clear cell and node highlights"""
        if self.plotter:
            # Remove element highlight
            if 'picked_element_highlight' in self.plotter.actors:
                self.plotter.remove_actor('picked_element_highlight')
            
            # Remove node highlight  
            if 'picked_node_highlight' in self.plotter.actors:
                self.plotter.remove_actor('picked_node_highlight')
    
    def _display_cell_info(self, cell_index):
        """Display information for a specific cell index"""
        
        if not self.current_data:
            if self.info_content:
                self.info_content.setText("No mesh data available")
            return
            
        try:
            element = self.current_data.get_element_by_id(cell_index + 1)
            
            element_id = element.get_id()
            
            # Get all available information
            info_text = f"""ELEMENT INFORMATION \n{element.get_info()}"""
            
            # Update panel
            if self.info_title:
                self.info_title.setText(f"Element {element_id} Information")
            if self.info_content:
                self.info_content.setText(info_text)
            
        except Exception as e:
            error_msg = f"Error getting element info: {e}"
            if self.info_content:
                self.info_content.setText(error_msg)
    
    def _display_node_info(self, point_index):
        """Display information for a specific node/point index"""
        
        if not self.current_data:
            if self.info_content:
                self.info_content.setText("No mesh data available")
            return
            
        try:
            node = self.current_data.get_node_by_id(point_index + 1)
            node_id = node.get_id()

            # Get all available information
            info_text = f"""NODE INFORMATION \n{node.get_info()}"""
            # Update panel
            if self.info_title:
                self.info_title.setText(f"Node {node_id} Information")
            if self.info_content:
                self.info_content.setText(info_text)

        except Exception as e:
            error_msg = f"Error getting node info: {e}"
            if self.info_content:
                self.info_content.setText(error_msg)
    
    def enable_click_tracking(self, plotter):
        """Enable click tracking"""
        try:
            # Click position tracking
            if hasattr(plotter, 'track_click_position'):
                plotter.track_click_position(self._on_click_callback)
            else:
                # Alternative method with VTK events
                plotter.iren.AddObserver('LeftButtonPressEvent', self._on_left_click)
                
        except Exception as e:
            print(f"Error enabling click tracking: {e}")
    
    def _on_click_callback(self, point):
        """Callback called on click with track_click_position"""
        if point is not None:
            print(f"Click at: {point}")
            self.zoom_to_point_coordinates(point)
    
    def _on_left_click(self):
        """Alternative callback for clicks (VTK method)"""
        try:
            # Get click position
            iren = self.plotter.iren
            x, y = iren.GetEventPosition()
            
            # Convert to world coordinates
            picker = self.plotter.picker
            if picker.Pick(x, y, 0, self.plotter.renderer):
                world_pos = picker.GetPickPosition()
                print(f"Click detected at: {world_pos}")
                self.zoom_to_point_coordinates(world_pos)
            
        except Exception as e:
            print(f"Click error: {e}")
    
    def zoom_to_point_coordinates(self, target_point):
        """Zoom to specific point in 3D coordinates"""
        if not target_point or len(target_point) < 2:
            return
        
        try:
            camera = self.plotter.camera
            current_pos = np.array(camera.position)
            target_pos = np.array([target_point[0], target_point[1], target_point[2] if len(target_point) > 2 else 0])
            
            # Calculate new camera position
            new_pos = current_pos
            
            # Update camera
            camera.position = new_pos
            camera.focal_point = target_pos
            
            # Render
            self.plotter.render()
            
        except Exception as e:
            print(f"Zoom to point error: {e}")