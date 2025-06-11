"""
User Interaction Management Module (click zoom, keyboard shortcuts)
"""

import numpy as np

class InteractionHandler:
    """Manager for user interactions with visualization"""
    
    def __init__(self):
        self.plotter = None
    
    def setup(self, plotter):
        """Configure interactions on plotter"""
        self.plotter = plotter
    
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

