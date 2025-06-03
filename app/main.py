#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application principale - Point d'entrée
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt

from main_ui import Ui_MainWindow
from modules.file_handler import FileHandler
from modules.mesh_handler import MeshHandler
from modules.visualization import VisualizationManager

'''
from modules.edit_handler import EditHandler
from modules.view_handler import ViewHandler
from modules.summary_handler import SummaryHandler
from modules.query_handler import QueryHandler
from modules.field_variables_handler import FieldVariablesHandler
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
        
        # Initialisation du gestionnaire de visualisation AVANT les autres modules
        self.visualization_manager = VisualizationManager(self)
        
        # Définir le widget de visualisation comme widget central par défaut
        self.visualization_manager.set_as_central_widget()
        
        # Initialisation des gestionnaires de modules
        self.init_handlers()
        
        # Connexion des signaux
        self.connect_signals()
        
        self.showMaximized()
    
    def init_handlers(self):
        """Initialise tous les gestionnaires de modules"""
        self.file_handler = FileHandler(self)
        self.mesh_handler = MeshHandler(self)

        '''
        self.edit_handler = EditHandler(self)
        self.view_handler = ViewHandler(self)
        self.summary_handler = SummaryHandler(self)
        self.query_handler = QueryHandler(self)
        self.field_variables_handler = FieldVariablesHandler(self)
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
        """Connecte tous les signaux des actions aux gestionnaires appropriés"""
        
        # Menu File
        self.ui.actionWorking_Derectory.triggered.connect(self.file_handler.set_working_directory)
        self.ui.actionPrint.triggered.connect(self.file_handler.print_document)
        self.ui.actionSave.triggered.connect(self.file_handler.save_document)
        self.ui.actionExport_as_DXF.triggered.connect(self.file_handler.export_as_dxf)
        self.ui.actionExport_as_ascii.triggered.connect(self.file_handler.export_as_ascii)
        self.ui.actionExport_as_RST.triggered.connect(self.file_handler.export_as_rst)
        self.ui.actionExit_Program.triggered.connect(self.close)
        
        # Menu Mesh
        self.ui.actionInitial_Mesh.triggered.connect(self.mesh_handler.initial_mesh)
        self.ui.actionDeformed_Mesh.triggered.connect(self.mesh_handler.deformed_mesh)
        
        '''
        # Menu Edit
        self.ui.actionSelect_Text.triggered.connect(self.edit_handler.select_text)
        self.ui.actionSelect_Graphics.triggered.connect(self.edit_handler.select_graphics)
        self.ui.actionSelect_All.triggered.connect(self.edit_handler.select_all)
        self.ui.actionCopy.triggered.connect(self.edit_handler.copy)
        self.ui.actionPaste.triggered.connect(self.edit_handler.paste)
        
        # Menu View
        self.ui.actionSize_To_Fit.triggered.connect(self.view_handler.size_to_fit)
        self.ui.actionFull_Screen.triggered.connect(self.view_handler.toggle_full_screen)
        self.ui.actionMagnification_Zoom.triggered.connect(self.view_handler.magnification_zoom)
        
        # Menu Summary
        self.ui.actionStandard_Options.triggered.connect(self.summary_handler.standard_options)
        self.ui.actionWorkpiece.triggered.connect(self.summary_handler.workpiece_summary)
        self.ui.actionDie.triggered.connect(self.summary_handler.die_summary)
        
        # Menu Query
        self.ui.actionStandard_Options_2.triggered.connect(self.query_handler.standard_options)
        self.ui.actionNodes.triggered.connect(self.query_handler.query_nodes)
        self.ui.actionElements.triggered.connect(self.query_handler.query_elements)
        self.ui.actionMinimum_Jacobian.triggered.connect(self.query_handler.minimum_jacobian)
        self.ui.actionSpecial_Options.triggered.connect(self.query_handler.special_options)
        self.ui.actionContact_Length_and_Ruler.triggered.connect(self.query_handler.contact_length_ruler)
        self.ui.actionSurface_Strains.triggered.connect(self.query_handler.surface_strains)
        
        # Menu Field Variables (nombreuses connexions)
        self.connect_field_variables_signals()
        
        # Autres menus
        # Animation, Graphics, etc. seront connectés selon les besoins
        '''
    
    def get_visualization_manager(self):
        """
        Permet aux autres modules d'accéder au gestionnaire de visualisation
        """
        return self.visualization_manager
    
    def get_current_data(self):
        """
        Retourne les données actuellement chargées
        """
        return self.visualization_manager.get_current_data()

        '''
    
    def connect_field_variables_signals(self):
        """Connecte les signaux du menu Field Variables"""
        fv = self.field_variables_handler
        
        # Standard
        self.ui.actionStandard_Options_4.triggered.connect(fv.standard_options)
        
        # Velocity
        self.ui.actionVelocity_x_r.triggered.connect(fv.velocity_x_r)
        self.ui.actionVelocity_y_z.triggered.connect(fv.velocity_y_z)
        self.ui.actionTotal_Velocity.triggered.connect(fv.total_velocity)
        
        # Force
        self.ui.actionForce_x_r.triggered.connect(fv.force_x_r)
        self.ui.actionForce_y_z.triggered.connect(fv.force_y_z)
        self.ui.actionTotal_Force.triggered.connect(fv.total_force)
        
        # Temperature
        self.ui.actionTemperature_Rate.triggered.connect(fv.temperature_rate)
        self.ui.actionTemperature.triggered.connect(fv.temperature)
        
        # Strain Rate
        self.ui.actionStrain_Rate_x_r.triggered.connect(fv.strain_rate_x_r)
        self.ui.actionStrain_Rate_y_r.triggered.connect(fv.strain_rate_y_z)
        self.ui.actionStrain_rate_z_theta.triggered.connect(fv.strain_rate_z_theta)
        self.ui.actionStrain_Rate_xy_rz.triggered.connect(fv.strain_rate_xy_rz)
        self.ui.actionEffective_Strain_Rate.triggered.connect(fv.effective_strain_rate)
        
        # Strain
        self.ui.actionStrain_x_r.triggered.connect(fv.strain_x_r)
        self.ui.actionStrain_y_r.triggered.connect(fv.strain_y_z)
        self.ui.actionStrain_z_theta.triggered.connect(fv.strain_z_theta)
        self.ui.actionStrain_xy_rz.triggered.connect(fv.strain_xy_rz)
        self.ui.actionEffective_Strain.triggered.connect(fv.effective_strain)
        self.ui.actionVolumetric_Strain.triggered.connect(fv.volumetric_strain)
        self.ui.actionStrain_1.triggered.connect(fv.strain_1)
        self.ui.actionStrain_2.triggered.connect(fv.strain_2)
        self.ui.actionStrain_3.triggered.connect(fv.strain_3)
        
        # Stress
        self.ui.actionStress_x_r.triggered.connect(fv.stress_x_r)
        self.ui.actionStress_y_z.triggered.connect(fv.stress_y_z)
        self.ui.actionStress_z_theta.triggered.connect(fv.stress_z_theta)
        self.ui.actionStress_xy_rz.triggered.connect(fv.stress_xy_rz)
        self.ui.actionEffective_Stress.triggered.connect(fv.effective_stress)
        self.ui.actionAverage_Stress.triggered.connect(fv.average_stress)
        self.ui.actionStress_1.triggered.connect(fv.stress_1)
        self.ui.actionStress_2.triggered.connect(fv.stress_2)
        self.ui.actionStress3.triggered.connect(fv.stress_3)
        '''
    
def main():
    """Point d'entrée principal de l'application"""
    app = QApplication(sys.argv)
    
    # Création et affichage de la fenêtre principale
    window = MainWindow()
    window.show()
    
    # Lancement de la boucle d'événements
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()