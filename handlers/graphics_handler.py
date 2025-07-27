"""
Graphics Menu Handler
Manages all graphics and plotting operations for dies data
"""

from PyQt5.QtWidgets import QMessageBox
from .graphics.xy_graphics_dialog import XYGraphicsDialog


class GraphicsHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        
    def get_current_data(self):
        """Get current mesh data"""
        return self.main_window.get_current_data()
    
    def standard_options(self):
        """Standard Options - not implemented"""
        QMessageBox.information(
            self.main_window, 
            "Not Implemented", 
            "Standard Options not yet implemented"
        )
    
    def xy_graphics(self):
        """Show XY Graphics dialog for dies data"""
        if not self._check_data_available():
            return
            
        dialog = XYGraphicsDialog(self.main_window, self.get_current_data())
        dialog.show()
    
    def principal_strain_space(self):
        """Principal Strain Space - not implemented"""
        QMessageBox.information(
            self.main_window, 
            "Not Implemented", 
            "Principal Strain Space not yet implemented"
        )
    
    def strain_stress_triaxiality(self):
        """Strain-Stress Triaxiality - not implemented"""
        QMessageBox.information(
            self.main_window, 
            "Not Implemented", 
            "Strain-Stress Triaxiality not yet implemented"
        )
    
    def evolution_of_element_center_or_field_variable_with_time(self):
        """Evolution of Element Center or Field Variable with Time - not implemented"""
        QMessageBox.information(
            self.main_window, 
            "Not Implemented", 
            "Evolution of Element Center or Field Variable with Time not yet implemented"
        )
    
    def mesh_quality_assessment(self):
        """Mesh Quality Assessment - not implemented"""
        QMessageBox.information(
            self.main_window, 
            "Not Implemented", 
            "Mesh Quality Assessment not yet implemented"
        )
    
    def xy_graphics_of_electrical_variables(self):
        """XY Graphics of Electrical Variables - not implemented"""
        QMessageBox.information(
            self.main_window, 
            "Not Implemented", 
            "XY Graphics of Electrical Variables not yet implemented"
        )
    
    def _check_data_available(self):
        """Check if mesh data with dies is available"""
        data = self.get_current_data()
        
        # Check if any data is loaded
        if not data:
            QMessageBox.warning(
                self.main_window,
                "No Data",
                "Please load a mesh file first."
            )
            return False
            
        # Check if dies are available
        dies = data.get_dies()
        if not dies or len(dies) == 0:
            QMessageBox.warning(
                self.main_window,
                "No Dies Data",
                "No dies found in the current mesh file.\n"
                "Graphics functionality requires dies data."
            )
            return False
            
        return True