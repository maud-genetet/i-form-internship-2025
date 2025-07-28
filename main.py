#!/usr/bin/env python3

"""
Main Application - Entry Point
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt
import logging 

from main_ui import Ui_MainWindow
from handlers.file_handler import FileHandler
from handlers.mesh_handler import MeshHandler
from visualization import VisualizationManager
from handlers.field_variables_handler import FieldVariablesHandler
from handlers.animation_handler import AnimationHandler
from handlers.graphics_handler import GraphicsHandler

'''
from modules.edit_handler import EditHandler
from modules.view_handler import ViewHandler
from modules.summary_handler import SummaryHandler
from modules.query_handler import QueryHandler
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
        self.animation_handler = AnimationHandler(self)
        self.graphics_handler = GraphicsHandler(self)

        '''
        self.edit_handler = EditHandler(self)
        self.view_handler = ViewHandler(self)
        self.summary_handler = SummaryHandler(self)
        self.query_handler = QueryHandler(self)
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
        self.ui.actionWorking_Directory.triggered.connect(self.file_handler.set_working_directory)
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
        
        # Animation Menu
        self.ui.actionAnimation_Controls.triggered.connect(self.animation_handler.animation_controls)

        self.ui.actionXY_Graphics.triggered.connect(self.graphics_handler.xy_graphics)
        self.ui.actionPrincipal_Strain_Space.triggered.connect(self.graphics_handler.principal_strain_space)
        self.ui.actionStrain_Stress_Triaxiality.triggered.connect(self.graphics_handler.strain_stress_triaxiality)
        self.ui.actionEvolution_of_Element_Center_or_Field_Variable_with_Time.triggered.connect(self.graphics_handler.evolution_of_element_center_or_field_variable_with_time)
        self.ui.actionMesh_Quality_Assessment.triggered.connect(self.graphics_handler.mesh_quality_assessment)
        self.ui.actionXY_Graphics_of_Electrical_Variables.triggered.connect(self.graphics_handler.xy_graphics_of_electrical_variables)
        
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
        self.ui.actionVelocity_x_r_2.triggered.connect(lambda: fv.apply_variable("Velocity_X"))
        self.ui.actionVelocity_y_z_2.triggered.connect(lambda: fv.apply_variable("Velocity_Y"))
        self.ui.actionTotal_Velocity_2.triggered.connect(lambda: fv.apply_variable("Total_Velocity"))
        
        # Force
        self.ui.actionForce_x_r_2.triggered.connect(lambda: fv.apply_variable("Force_X"))
        self.ui.actionForce_y_y.triggered.connect(lambda: fv.apply_variable("Force_Y"))
        self.ui.actionTotal_Force_2.triggered.connect(lambda: fv.apply_variable("Total_Force"))
        
        # Temperature
        self.ui.actionTemperature_Rate.triggered.connect(lambda: fv.apply_variable("Temperature_Rate"))
        self.ui.actionTemperature.triggered.connect(lambda: fv.apply_variable("Temperature"))
        
        # Strain Rate
        self.ui.actionStrain_Rate_x_r_2.triggered.connect(lambda: fv.apply_variable("Strain_Rate_X"))
        self.ui.actionStrain_Rate_y_z.triggered.connect(lambda: fv.apply_variable("Strain_Rate_Y"))
        self.ui.actionStrain_Rate_z_theta.triggered.connect(lambda: fv.apply_variable("Strain_Rate_Z"))
        self.ui.actionStrain_Rate_xy_z.triggered.connect(lambda: fv.apply_variable("Strain_Rate_XY"))
        self.ui.actionEffective_Strain_Rate_2.triggered.connect(lambda: fv.apply_variable("Effective_Strain_Rate"))
        self.ui.actionVolumetric_Strain_Rate.triggered.connect(lambda: fv.apply_variable("Volumetric_Strain_Rate"))
        
        # Strain
        self.ui.actionStrain_x_r_2.triggered.connect(lambda: fv.apply_variable("Strain_X"))
        self.ui.actionStrain_y_z.triggered.connect(lambda: fv.apply_variable("Strain_Y"))
        self.ui.actionStrain_z_theta_2.triggered.connect(lambda: fv.apply_variable("Strain_Z"))
        self.ui.actionStrain_xy_rz_2.triggered.connect(lambda: fv.apply_variable("Strain_XY"))
        self.ui.actionEffective_Strain_2.triggered.connect(lambda: fv.apply_variable("Effective_Strain"))
        self.ui.actionVolumetric_Strain_2.triggered.connect(lambda: fv.apply_variable("Volumetric_Strain"))
        self.ui.actionStrain_4.triggered.connect(lambda: fv.apply_variable("Strain_1"))
        self.ui.actionStrain_5.triggered.connect(lambda: fv.apply_variable("Strain_2"))
        self.ui.actionStrain_6.triggered.connect(lambda: fv.apply_variable("Strain_3"))
        
        # Stress
        self.ui.actionStress_x_r_2.triggered.connect(lambda: fv.apply_variable("Stress_X"))
        self.ui.actionStress_y_z_2.triggered.connect(lambda: fv.apply_variable("Stress_Y"))
        self.ui.actionStress_z_theta_2.triggered.connect(lambda: fv.apply_variable("Stress_ZZ"))
        self.ui.actionStress_xy_rz_2.triggered.connect(lambda: fv.apply_variable("Stress_XY"))
        self.ui.actionEffective_Stress_2.triggered.connect(lambda: fv.apply_variable("Effective_stress"))
        self.ui.actionAverage_Stress_2.triggered.connect(lambda: fv.apply_variable("Average_Stress"))
        self.ui.actionStress_3.triggered.connect(lambda: fv.apply_variable("Stress_1"))
        self.ui.actionStress_4.triggered.connect(lambda: fv.apply_variable("Stress_2"))
        self.ui.actionStress_5.triggered.connect(lambda: fv.apply_variable("Stress_3"))
        
        # Material Properties
        self.ui.actionThickness_Plane_Stress.triggered.connect(lambda: fv.apply_variable("Thickness_Plane_Stress"))
        self.ui.actionRelative_Density.triggered.connect(lambda: fv.apply_variable("Relative_Density"))
        self.ui.actionDuctile_Damage.triggered.connect(lambda: fv.apply_variable("Ductile_Damage"))
        
        # Electric
        self.ui.actionElectric_Potential.triggered.connect(lambda: fv.apply_variable("Electric_Potential"))
        self.ui.actionElectric_Current_Density.triggered.connect(lambda: fv.apply_variable("Electric_Current_Density"))
        self.ui.actionElectric_Resistivity.triggered.connect(lambda: fv.apply_variable("Electric_Resistivity"))
        
        # Special Options
        self.ui.actionStress_y_z_Ef_Stress.triggered.connect(lambda: fv.apply_variable("Stress_Y_Ef_Stress"))
        self.ui.actionStress_xy_rz_Ef_Stress.triggered.connect(lambda: fv.apply_variable("Stress_XY_Ef_Stress"))
        self.ui.actionAverage_Stress_Ef_Stress.triggered.connect(lambda: fv.apply_variable("Average_Stress_Ef_Stress"))
        self.ui.actionPressure.triggered.connect(lambda: fv.apply_variable("Pressure"))
        self.ui.actionPressure_Ef_Stress.triggered.connect(lambda: fv.apply_variable("Pressure_Ef_Stress"))
        self.ui.actionSurface_Enlargement_Ratio.triggered.connect(lambda: fv.apply_variable("Surface_Enlargement_Ratio"))
        
        # Element Quality
        self.ui.actionElement_Quality.triggered.connect(lambda: fv.apply_variable("Element_Quality"))
    
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
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    main()