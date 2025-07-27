"""
File Menu Handler
Manages all file-related operations
"""

from PyQt5.QtWidgets import QFileDialog


class FileHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.working_directory = None
    
    def set_working_directory(self):
        """Set working directory"""
        directory = QFileDialog.getExistingDirectory(
            self.main_window,
            "Select Working Directory",
            self.working_directory
        )
        if directory:
            self._clear_previous_data()
            
            self.working_directory = directory
            self.main_window.visualization_manager.set_working_directory(directory)
            self.main_window.visualization_manager._update_data_info()
            
            # Enable click tracking ONCE when setting working directory
            visualization_manager = self.main_window.visualization_manager
            visualization_manager.interaction_handler.enable_click_tracking(visualization_manager.plotter)

            # deformed_mesh
            self.main_window.mesh_handler.deformed_mesh()
    
    def _clear_previous_data(self):
        """Clear all previous visualization data"""
        visualization_manager = self.main_window.visualization_manager
        
        # Clear visualization
        visualization_manager.clear()
        
        # Reset data
        visualization_manager.current_data = None
        visualization_manager.current_mesh = None
        
        # Hide deformed mesh controls
        visualization_manager.hide_deformed_mesh_controls()
        
        # Clear preloaded data
        visualization_manager.preloaded_data = {}
        
        # Stop any preloading in progress
        self.main_window.mesh_handler.preloader_manager.stop_preloading()
        
        # Reset mesh handler data
        self.main_window.mesh_handler.neu_files = []
        self.main_window.mesh_handler.working_directory = None

        self.main_window.mesh_handler.preloader_manager.preloaded_files = {}
        # Reset field variables handler current variable
        self.main_window.field_variables_handler.current_variable = None
        
        if hasattr(visualization_manager, 'scales_cache'):
            visualization_manager.scales_cache = {}
        
    def print_document(self):
        """Print current document"""
        pass
    
    def save_document(self):
        """Save current document"""
        # TODO: Implement save functionality
        pass
    
    def export_as_dxf(self):
        """Export document as DXF"""
        filename, _ = QFileDialog.getSaveFileName(
            self.main_window,
            "Export as DXF",
            self.working_directory,
            "DXF Files (*.dxf)"
        )
        if filename:
            # TODO: DXF export logic
            pass
    
    def export_as_ascii(self):
        """Export document as ASCII"""
        filename, _ = QFileDialog.getSaveFileName(
            self.main_window,
            "Export as ASCII",
            self.working_directory,
            "Text Files (*.txt)"
        )
        if filename:
            # TODO: ASCII export logic
            pass
    
    def export_as_rst(self):
        """Export document as RST"""
        filename, _ = QFileDialog.getSaveFileName(
            self.main_window,
            "Export as RST",
            self.working_directory,
            "RST Files (*.rst)"
        )
        if filename:
            # TODO: RST export logic
            pass