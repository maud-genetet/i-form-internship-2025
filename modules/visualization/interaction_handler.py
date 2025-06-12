"""
User Interaction Management Module (click zoom, keyboard shortcuts, cell picking)
"""

import numpy as np
import vtk
from PyQt5.QtCore import QTimer
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
        
        # Create a cell picker
        picker = vtk.vtkCellPicker()
        picker.SetTolerance(0.001)  # Set picking tolerance
        
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
        else:
            if self.info_content:
                self.info_content.setText("Click on the mesh elements")
    
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
                name='picked_cell_highlight'  # Name it so we can manage it
            )
    
    def _clear_highlight(self):
        """Clear cell highlight"""
        if self.plotter and 'picked_cell_highlight' in self.plotter.actors:
            self.plotter.remove_actor('picked_cell_highlight')
    
    def _display_cell_info(self, cell_index):
        """Display information for a specific cell index"""
        
        if not self.current_data:
            if self.info_content:
                self.info_content.setText("No mesh data available")
            return
            
        try:
            elements = self.current_data.get_elements()
            
            if cell_index >= len(elements) or cell_index < 0:
                error_msg = f"Cell index {cell_index} out of range (0-{len(elements)-1})"
                if self.info_content:
                    self.info_content.setText(error_msg)
                return
                
            element = elements[cell_index]
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