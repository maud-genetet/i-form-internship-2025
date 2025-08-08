"""
Graphics Menu Handler
Manages all graphics and plotting operations for dies data
"""

from PyQt5.QtWidgets import QProgressDialog, QMessageBox
from .graphics.xy_graphics_dialog import XYGraphicsDialog
from PyQt5.QtCore import Qt
from parser import ParserNeutralFile
import os
import logging
logger = logging.getLogger(__name__)


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
        
        # Check if we need to load all files for graphics
        if not self._ensure_all_files_loaded():
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
    
    def _ensure_all_files_loaded(self):
        """Ensure all files are loaded for graphics, load them if needed"""
        
        visualization_manager = self.main_window.visualization_manager
        
        # Check if we have neu_files
        if not hasattr(visualization_manager, 'neu_files') or not visualization_manager.neu_files:
            return True  # No multiple files, proceed with single file
        
        total_files = len(visualization_manager.neu_files)
        
        # Check current preloaded data
        if not hasattr(visualization_manager, 'preloaded_data'):
            visualization_manager.preloaded_data = {}
        
        loaded_count = len(visualization_manager.preloaded_data)
        
        # If all files are already loaded, proceed
        if loaded_count >= total_files:
            return True
        
        # SET GRAPHICS LOADING FLAG
        visualization_manager.graphics_loading = True
        
        try:
            # Show loading dialog
            progress = QProgressDialog("Loading files for graphics analysis...", "Cancel", 0, total_files, self.main_window)
            progress.setWindowTitle("Graphics Data Loading")
            progress.setWindowModality(Qt.WindowModal)
            progress.setMinimumDuration(0)
            progress.show()
            
            # Load missing files
            graphics_loaded = 0
            for i in range(total_files):
                if progress.wasCanceled():
                    QMessageBox.information(self.main_window, "Cancelled", "Graphics loading was cancelled.")
                    return False
                
                # Skip if already loaded
                if i in visualization_manager.preloaded_data:
                    progress.setValue(i + 1)
                    continue
                
                filename = visualization_manager.neu_files[i]
                progress.setLabelText(f"Loading {filename}...")
                progress.setValue(i)
                
                # Force GUI update
                progress.repaint()
                self.main_window.repaint()
                
                file_path = os.path.join(visualization_manager.working_directory, filename)
                
                try:
                    logger.info(f"Loading {filename} for graphics ({i+1}/{total_files})")
                    # Use parser_file_graphics to just load the dies information
                    neutral_data = ParserNeutralFile.parser_file_graphics(file_path)
                    if neutral_data:
                        visualization_manager.preloaded_data[i] = neutral_data
                        graphics_loaded += 1
                        logger.info(f"Successfully loaded {filename}")
                    else:
                        logger.error(f"Failed to parse {filename}")
                except Exception as e:
                    logger.exception(f"Error loading {filename}: {e}")
            
            progress.setValue(total_files)
            progress.close()
            
            final_loaded = len(visualization_manager.preloaded_data)
            logger.info(f"Graphics loading complete: {final_loaded}/{total_files} files loaded ({graphics_loaded} new files)")
            
            if final_loaded == 0:
                QMessageBox.warning(self.main_window, "Loading Failed", 
                                "Could not load any files for graphics analysis.")
                return False
            
            if final_loaded < total_files:
                QMessageBox.information(self.main_window, "Partial Loading", 
                                    f"Loaded {final_loaded}/{total_files} files. Graphics will work with available data.")
            
            return True
            
        finally:
            # ALWAYS CLEAR THE FLAG
            visualization_manager.graphics_loading = False
    