"""
Main Visualization Module - Configuration and Main Controls
"""

import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel)
from pyvistaqt import QtInteractor
from PyQt5.QtWidgets import QFrame, QScrollArea
from PyQt5.QtCore import Qt
import numpy as np
import logging
logger = logging.getLogger(__name__) 
from .mesh_builder import MeshBuilder
from .interaction_handler import InteractionHandler
from .display_modes import DisplayModeManager
from .toolbar_manager import ToolbarManager

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

        self.graphics_loading = False
        
        # Default configuration
        self.default_mesh_color = 'yellow'
        self.default_edge_color = 'black'
        self.default_node_color = 'black'
        
        # Specialized modules
        self.mesh_builder = MeshBuilder()
        self.interaction_handler = InteractionHandler()
        self.display_manager = DisplayModeManager()
        
        # Toolbar manager
        self.toolbar_manager = ToolbarManager(main_window, self)
        
        self.preloaded_data = {}
        
        self.neu_files = []
        self.working_directory = None
        self.load_mesh_callback = None
        self.current_mesh_index = 0

        self.scales_cache = {}
            
        self._setup_visualization_widget()
    
    def _setup_visualization_widget(self):
        """Configure main visualization widget"""
        self.visualization_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Create toolbars using ToolbarManager
        self.toolbar_manager.create_toolbars(main_layout)
        
        # Create horizontal layout for plotter + info panel
        content_layout = QHBoxLayout()
        
        # PyVista visualization area
        self.plotter = QtInteractor(self.visualization_widget)
        content_layout.addWidget(self.plotter.interactor)
        
        # Info panel (hidden by default)
        self._create_info_panel()
        content_layout.addWidget(self.info_panel)
        self.info_panel.setVisible(False)
        
        main_layout.addLayout(content_layout)
        
        self.visualization_widget.setLayout(main_layout)
        
        # Plotter configuration
        self._configure_plotter()
    
    def _create_info_panel(self):
        """Create info panel for mesh information"""
        self.info_panel = QFrame()
        self.info_panel.setFixedWidth(300)
        
        info_layout = QVBoxLayout()
        
        # Title
        self.info_title = QLabel("Mesh Information")
        info_layout.addWidget(self.info_title)
        
        # Scrollable content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.info_content = QLabel("Select pick mode and click on the mesh")
        self.info_content.setWordWrap(True)
        self.info_content.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(self.info_content)
        info_layout.addWidget(scroll_area)
        
        self.info_panel.setLayout(info_layout)
    
    def _show_info_panel(self):
        """Show the info panel"""
        self.info_panel.setVisible(True)
    
    def _hide_info_panel(self):
        """Hide the info panel and disable picking"""
        self.info_panel.setVisible(False)
        self.toolbar_manager.mesh_info_btn.setChecked(False)
        self.interaction_handler.disable_mesh_picking()
    
    def _configure_plotter(self):
        """Configure plotter with automatic click"""
        self.plotter.show_axes()
        self.plotter.view_xy()
        
        # Initialize interaction handler
        self.interaction_handler.setup(self.plotter)
        self.interaction_handler.set_info_panel(
            self.info_panel, 
            self.info_content, 
            self.info_title
        )

    def reapply_mesh_picking_if_needed(self):
        """Reapply mesh picking after mesh operations"""
        self.interaction_handler.reapply_mesh_picking_if_needed()
    
    
    # === DEFORMED MESH METHODS ===
    
    def add_deformed_mesh_controls(self, neu_files, working_directory, load_callback):
        """Add navigation controls for deformed mesh"""
        self.neu_files = neu_files
        self.working_directory = working_directory
        self.load_mesh_callback = load_callback
        self.current_mesh_index = 0
        
        # Use toolbar manager
        self.toolbar_manager.show_navigation_controls(neu_files)
        
        # Update button states
        self._update_mesh_controls_state()
        
    def hide_deformed_mesh_controls(self):
        """Hide deformed mesh navigation controls"""
        # Use toolbar manager
        self.toolbar_manager.hide_navigation_controls()
    
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
            
            # Check if we have preloaded data
            preloaded_data = self.get_preloaded_data(self.current_mesh_index)
            if preloaded_data and preloaded_data.is_complete():
                logger.debug(f"Fast loading file {self.current_mesh_index + 1}/{len(self.neu_files)}: {current_file} (preloaded)")
                self.load_neutral_file(preloaded_data)
            else:
                logger.debug(f"Loading file {self.current_mesh_index + 1}/{len(self.neu_files)}: {current_file} (from disk)")
                self.load_mesh_callback(file_path)
            
            self._update_data_info()
    
    def _update_mesh_controls_state(self):
        """Update navigation controls state"""
        self.toolbar_manager.update_navigation_state(
            self.current_mesh_index, 
            len(self.neu_files)
        )
    
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
        
        # Create mesh for later use but don't display it
        mesh = self.mesh_builder.create_pyvista_mesh(self.current_data)
        if mesh:
            self.current_mesh = mesh
            self.interaction_handler.set_mesh_data(mesh, self.current_data)
        
        # Reapply currently selected variable if exists
        if hasattr(self.main_window, 'field_variables_handler'):
            self.main_window.field_variables_handler.reapply_current_variable()

    def set_working_directory(self, dir_name):
        """Set working directory"""
        self.current_dir = dir_name
    
    def _update_data_info(self):
        """Update displayed information"""
        info_text = ""
        
        if self.current_data and self.current_dir:
            # Get current filename if available
            filename = ""
            if hasattr(self, 'neu_files') and self.neu_files and hasattr(self, 'current_mesh_index'):
                if 0 <= self.current_mesh_index < len(self.neu_files):
                    filename = f" - {self.neu_files[self.current_mesh_index]}"
            
            info_text = (f"Nodes: {self.current_data.get_nb_nodes()} | "
                f"Elements: {self.current_data.get_nb_elements()}{filename}")
        elif self.current_dir:
            info_text = f"No data loaded"
        else:
            info_text = "No directory set"
        
        # Use toolbar manager
        self.toolbar_manager.update_data_info(info_text)
    
    def _add_dies_to_plot(self):
        """Add dies to visualization"""
        if not self.current_data:
            return
        
        dies = self.current_data.get_dies()
        
        for i, die in enumerate(dies):
            die_mesh = self.mesh_builder.create_die_mesh(die)
            if die_mesh:
                self.display_manager.display_die(
                    self.plotter, die_mesh, die.get_id()
                )
    
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
        """Set front view (XY plane) """
        if self.plotter:
            # Save current camera position to keep
            camera = self.plotter.camera
            current_position = camera.position
            current_focal_point = camera.focal_point
            
            # Calculate current distance
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

    def get_global_scale_range_for_variable(self, variable_name):
        """Calcule min/max UNIQUEMENT pour la variable demandée - VERSION SIMPLIFIÉE"""
        # Si auto-scale n'est pas activé, retourner None
        options = self.toolbar_manager.get_current_options()
        if not options.get('auto_scale_mode', False):
            return None, None
        
        # Vérifier le cache
        if variable_name in self.scales_cache:
            cached_scales = self.scales_cache[variable_name]
            return cached_scales['min'], cached_scales['max']
        
        # Calculer pour cette variable spécifique
        total_available_files = len(self.preloaded_data) + (1 if self.current_mesh else 0)
        logger.debug(f"Computing scales for {variable_name} from {total_available_files} files...")
        
        global_min = None
        global_max = None
        
        for file_index in sorted(self.preloaded_data.keys()):
            neutral_data = self.preloaded_data[file_index]
            
            try:
                var_min, var_max = self._extract_variable_range(neutral_data, variable_name)
                
                if var_min is not None and var_max is not None:
                    if global_min is None:
                        global_min = var_min
                        global_max = var_max
                    else:
                        global_min = min(global_min, var_min)
                        global_max = max(global_max, var_max)
                    
            except Exception as e:
                logger.exception(f"Error processing file {file_index}: {e}")
        
        if global_min is not None and global_max is not None:
            # Mettre en cache
            self.scales_cache[variable_name] = {'min': global_min, 'max': global_max}
            
            return global_min, global_max
        else:
            logger.error(f"No data found for variable {variable_name}")
            return None, None
    
    def _extract_variable_range(self, neutral_data, target_variable):
        """Extrait min/max pour UNE SEULE variable spécifique"""
        if not neutral_data:
            return None, None
        
        elements = list(neutral_data.get_elements())
        if not elements:
            return None, None
        
        var_min = None
        var_max = None
        
        var_extractors = {
            'Effective strain rate': lambda el: el.get_strain_rate_E(),
            'Effective strain': lambda el: el.get_strain_E(),
            'Effective stress': lambda el: el.get_stress_O(),
            'Average stress': lambda el: el.get_stress_Orr(),
            'Relative Density': lambda el: el.get_densy(),
            'Element Quality': lambda el: el.get_rindx(),
            'Strain rate x(r)': lambda el: el.get_strain_rate_Exx(),
            'Strain rate y(z)': lambda el: el.get_strain_rate_Eyy(),
            'Strain rate z(theta)': lambda el: el.get_strain_rate_Ezz(),
            'Strain rate xy(rz)': lambda el: el.get_strain_rate_Exy(),
            'Volumetric strain rate': lambda el: el.get_strain_rate_Ev(),
            'Strain x(r)': lambda el: el.get_strain_Exx(),
            'Strain y(z)': lambda el: el.get_strain_Eyy(),
            'Strain z(theta)': lambda el: el.get_strain_Ezz(),
            'Strain xy(rz)': lambda el: el.get_strain_Exy(),
            'Volumetric Strain': lambda el: el.get_strain_volumetric(),
            'Strain 1': lambda el: el.get_strain_E1(),
            'Strain 2': lambda el: el.get_strain_E2(),
            'Strain 3': lambda el: el.get_strain_E3(),
            'Stress x(r)': lambda el: el.get_stress_Oxx(),
            'Stress y(z)': lambda el: el.get_stress_Oyy(),
            'Stress z(theta)': lambda el: el.get_stress_Ozz(),
            'Stress xy(rz)': lambda el: el.get_stress_Oxy(),
            'Stress 1': lambda el: el.get_stress_1(),
            'Stress 2': lambda el: el.get_stress_2(),
            'Stress 3': lambda el: el.get_stress_3(),
            'Thickness (Plane Stress)': lambda el: el.get_thickness_plane_stress(),
            'Ductile Damage': lambda el: el.get_fract(),
            'Velocity X(r)': lambda el: el.get_velocity_x(),
            'Velocity Y(z)': lambda el: el.get_velocity_y(),
            'Total Velocity': lambda el: el.get_total_velocity(),
            'Force X(r)': lambda el: el.get_force_x(),
            'Force Y(z)': lambda el: el.get_force_y(),
            'Total Force': lambda el: el.get_total_force(),
            'Temperature': lambda el: el.get_temperature(),
            'Temperature Rate': lambda el: el.get_temperature_rate(),
        }
        
        if target_variable in var_extractors:
            extractor = var_extractors[target_variable]
            for element in elements:
                try:
                    value = extractor(element)
                    if value is not None:
                        fval = float(value)
                        if var_min is None:
                            var_min = var_max = fval
                        else:
                            var_min = min(var_min, fval)
                            var_max = max(var_max, fval)
                except (ValueError, TypeError):
                    pass
        
        return var_min, var_max

    def get_current_data(self):
        """Return currently loaded data"""
        return self.current_data
    
    def set_preloaded_data(self, preloaded_data_dict):
        """Set preloaded data from preloader"""
        self.preloaded_data = preloaded_data_dict
        logger.debug(f"Visualization manager received {len(preloaded_data_dict)} preloaded files")

    def get_preloaded_data(self, index):
        """Get preloaded data for specific index"""
        return self.preloaded_data.get(index)
    
    # Methods to access toolbar manager properties for backward compatibility
    @property
    def progress_bar(self):
        """Access progress bar through toolbar manager"""
        return self.toolbar_manager.progress_bar
    
    @property
    def progress_label(self):
        """Access progress label through toolbar manager"""
        return self.toolbar_manager.progress_label