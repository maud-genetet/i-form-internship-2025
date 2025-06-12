#!/usr/bin/env python3

"""
Main Application - Entry Point
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt

from main_ui import Ui_MainWindow
from modules.file_handler import FileHandler
from modules.mesh_handler import MeshHandler
from modules.visualization import VisualizationManager # We import the module thanks to the __init__.py file
from modules.field_variables_handler import FieldVariablesHandler

'''
from modules.edit_handler import EditHandler
from modules.view_handler import ViewHandler
from modules.summary_handler import SummaryHandler
from modules.query_handler import QueryHandler
from modules.animation_handler import AnimationHandler
from modules.graphics_handler import GraphicsHandler
from modules.analysis.die_stress_handler import DieStressHandler
from modules.analysis.die_thermal_handler import DieThermalHandler
from modules.build_3d_handler import Build3DHandler
from modules.state_handler import StateHandler
from modules.window_handler import WindowHandler
from modules.help_handler import HelpHandler
'''


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Initialize visualization manager BEFORE other modules
        self.visualization_manager = VisualizationManager(self)
        
        # Set visualization widget as default central widget
        self.visualization_manager.set_as_central_widget()
        
        # Initialize module handlers
        self.init_handlers()
        
        # Connect signals
        self.connect_signals()
        
        self.showMaximized()
    
    def init_handlers(self):
        """Initialize all module handlers"""
        self.file_handler = FileHandler(self)
        self.mesh_handler = MeshHandler(self)
        self.field_variables_handler = FieldVariablesHandler(self)

        '''
        self.edit_handler = EditHandler(self)
        self.view_handler = ViewHandler(self)
        self.summary_handler = SummaryHandler(self)
        self.query_handler = QueryHandler(self)
        self.animation_handler = AnimationHandler(self)
        self.graphics_handler = GraphicsHandler(self)
        self.die_stress_handler = DieStressHandler(self)
        self.die_thermal_handler = DieThermalHandler(self)
        self.build_3d_handler = Build3DHandler(self)
        self.state_handler = StateHandler(self)
        self.window_handler = WindowHandler(self)
        self.help_handler = HelpHandler(self)
        '''
    
    def connect_signals(self):
        """Connect all action signals to appropriate handlers"""
        
        # File Menu
        self.ui.actionWorking_Derectory.triggered.connect(self.file_handler.set_working_directory)
        self.ui.actionPrint.triggered.connect(self.file_handler.print_document)
        self.ui.actionSave.triggered.connect(self.file_handler.save_document)
        self.ui.actionExport_as_DXF.triggered.connect(self.file_handler.export_as_dxf)
        self.ui.actionExport_as_ascii.triggered.connect(self.file_handler.export_as_ascii)
        self.ui.actionExport_as_RST.triggered.connect(self.file_handler.export_as_rst)
        self.ui.actionExit_Program.triggered.connect(self.close)
        
        # Mesh Menu
        self.ui.actionInitial_Mesh.triggered.connect(self.mesh_handler.initial_mesh)
        self.ui.actionDeformed_Mesh.triggered.connect(self.mesh_handler.deformed_mesh)
        
        # Field Variables Menu
        self.connect_field_variables_signals()
        
        '''
        # Edit Menu
        self.ui.actionSelect_Text.triggered.connect(self.edit_handler.select_text)
        self.ui.actionSelect_Graphics.triggered.connect(self.edit_handler.select_graphics)
        self.ui.actionSelect_All.triggered.connect(self.edit_handler.select_all)
        self.ui.actionCopy.triggered.connect(self.edit_handler.copy)
        self.ui.actionPaste.triggered.connect(self.edit_handler.paste)
        
        # View Menu
        self.ui.actionSize_To_Fit.triggered.connect(self.view_handler.size_to_fit)
        self.ui.actionFull_Screen.triggered.connect(self.view_handler.toggle_full_screen)
        self.ui.actionMagnification_Zoom.triggered.connect(self.view_handler.magnification_zoom)
        
        # Summary Menu
        self.ui.actionStandard_Options.triggered.connect(self.summary_handler.standard_options)
        self.ui.actionWorkpiece.triggered.connect(self.summary_handler.workpiece_summary)
        self.ui.actionDie.triggered.connect(self.summary_handler.die_summary)
        
        # Query Menu
        self.ui.actionStandard_Options_2.triggered.connect(self.query_handler.standard_options)
        self.ui.actionNodes.triggered.connect(self.query_handler.query_nodes)
        self.ui.actionElements.triggered.connect(self.query_handler.query_elements)
        self.ui.actionMinimum_Jacobian.triggered.connect(self.query_handler.minimum_jacobian)
        self.ui.actionSpecial_Options.triggered.connect(self.query_handler.special_options)
        self.ui.actionContact_Length_and_Ruler.triggered.connect(self.query_handler.contact_length_ruler)
        self.ui.actionSurface_Strains.triggered.connect(self.query_handler.surface_strains)
        
        # Other menus will be connected as needed
        '''
    
    def connect_field_variables_signals(self):
        """Connect Field Variables menu signals"""
        fv = self.field_variables_handler
        
        # Standard Options
        self.ui.actionStandard_Options_4.triggered.connect(fv.standard_options)
        
        # Velocity
        self.ui.actionVelocity_x_r_2.triggered.connect(fv.velocity_x_r)
        self.ui.actionVelocity_y_z_2.triggered.connect(fv.velocity_y_z)
        self.ui.actionTotal_Velocity_2.triggered.connect(fv.total_velocity)
        
        # Force
        self.ui.actionForce_x_r_2.triggered.connect(fv.force_x_r)
        self.ui.actionForce_y_y.triggered.connect(fv.force_y_z)
        self.ui.actionTotal_Force_2.triggered.connect(fv.total_force)
        
        # Temperature
        self.ui.actionTemperature_Rate.triggered.connect(fv.temperature_rate)
        self.ui.actionTemperature.triggered.connect(fv.temperature)
        
        # Strain Rate
        self.ui.actionStrain_Rate_x_r_2.triggered.connect(fv.strain_rate_x_r)
        self.ui.actionStrain_Rate_y_z.triggered.connect(fv.strain_rate_y_z)
        self.ui.actionStrain_Rate_z_theta.triggered.connect(fv.strain_rate_z_theta)
        self.ui.actionStrain_Rate_xy_z.triggered.connect(fv.strain_rate_xy_rz)
        self.ui.actionEffective_Strain_Rate_2.triggered.connect(fv.effective_strain_rate)
        self.ui.actionVolumetric_Strain_Rate.triggered.connect(fv.volumetric_strain_rate)
        
        # Strain
        self.ui.actionStrain_x_r_2.triggered.connect(fv.strain_x_r)
        self.ui.actionStrain_y_z.triggered.connect(fv.strain_y_z)
        self.ui.actionStrain_z_theta_2.triggered.connect(fv.strain_z_theta)
        self.ui.actionStrain_xy_rz_2.triggered.connect(fv.strain_xy_rz)
        self.ui.actionEffective_Strain_2.triggered.connect(fv.effective_strain)
        self.ui.actionVolumetric_Strain_2.triggered.connect(fv.volumetric_strain)
        self.ui.actionStrain_4.triggered.connect(fv.strain_1)
        self.ui.actionStrain_5.triggered.connect(fv.strain_2)
        self.ui.actionStrain_6.triggered.connect(fv.strain_3)
        
        # Stress
        self.ui.actionStress_x_r_2.triggered.connect(fv.stress_x_r)
        self.ui.actionStress_y_z_2.triggered.connect(fv.stress_y_z)
        self.ui.actionStress_z_theta_2.triggered.connect(fv.stress_z_theta)
        self.ui.actionStress_xy_rz_2.triggered.connect(fv.stress_xy_rz)
        self.ui.actionEffective_Stress_2.triggered.connect(fv.effective_stress)
        self.ui.actionAverage_Stress_2.triggered.connect(fv.average_stress)
        self.ui.actionStress_3.triggered.connect(fv.stress_1)
        self.ui.actionStress_4.triggered.connect(fv.stress_2)
        self.ui.actionStress_5.triggered.connect(fv.stress_3)
        
        self.ui.actionThickness_Plane_Stress.triggered.connect(fv.thickness_plane_stress)
        self.ui.actionRelative_Density.triggered.connect(fv.relative_density)
        self.ui.actionDuctile_Damage.triggered.connect(fv.ductile_damage)
        
        # Electric
        self.ui.actionElectric_Potential.triggered.connect(fv.electric_potential)
        self.ui.actionElectric_Current_Density.triggered.connect(fv.electric_current_density)
        self.ui.actionElectric_Resistivity.triggered.connect(fv.electric_resistivity)
        
        # Special Options
        self.ui.actionStress_y_z_Ef_Stress.triggered.connect(fv.stress_y_z_ef_stress)
        self.ui.actionStress_xy_rz_Ef_Stress.triggered.connect(fv.stress_xy_rz_ef_stress)
        self.ui.actionAverage_Stress_Ef_Stress.triggered.connect(fv.average_stress_ef_stress)
        self.ui.actionPressure.triggered.connect(fv.pressure)
        self.ui.actionPressure_Ef_Stress.triggered.connect(fv.pressure_ef_stress)
        self.ui.actionSurface_Enlargement_Ratio.triggered.connect(fv.surface_enlargement_ratio)
        
        # Element Quality
        self.ui.actionElement_Quality.triggered.connect(fv.element_quality)
    
    def get_visualization_manager(self):
        """Return visualization manager for other modules"""
        return self.visualization_manager
    
    def get_current_data(self):
        """Return currently loaded data"""
        return self.visualization_manager.get_current_data()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()