"""
Build 3D Menu Handler
Handles 3D model generation from 2D models
"""

from parser.models.node import Node3D
from parser.models.element import Element3D
from parser.models.neutral_file import NeutralFile3D
from parser.models.die import Die3D
import os
import math
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QSpinBox, QDoubleSpinBox, QPushButton,
                             QGroupBox, QMessageBox, QProgressDialog)
from PyQt5.QtCore import Qt
import logging
logger = logging.getLogger(__name__)


class Build3DHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.working_directory = None

    def plane_strain_model(self):
        """Handle 3D Plane Strain Model"""
        self._show_build_dialog("plane_strain")

    def plane_stress_model(self):
        """Handle 3D Plane Stress Model"""
        self._show_build_dialog("plane_stress")

    def axisymmetric_model(self):
        """Handle 3D Axisymmetric Model"""
        self._show_build_dialog("axisymmetric")

    def axisymmetric_cheese_model(self):
        """Handle 3D Axisymmetric Cheese Model"""
        self._show_build_dialog("axisymmetric_cheese")

    def _show_build_dialog(self, model_type):
        """Show build 3D dialog"""
        if not self._check_prerequisites():
            return

        dialog = Build3DDialog(self.main_window, model_type)

        # Parse fem.dat to get thickness if available
        thickness = self._parse_fem_dat()
        if thickness is not None:
            dialog.set_thickness(thickness)

        if dialog.exec_() == QDialog.Accepted:
            params = dialog.get_parameters()
            self._build_3d_model(model_type, params)

    def _check_prerequisites(self):
        """Check if prerequisites are met"""
        visualization_manager = self.main_window.visualization_manager

        if not visualization_manager.working_directory:
            QMessageBox.warning(
                self.main_window,
                "No Working Directory",
                "Please set a working directory first."
            )
            return False

        if not visualization_manager.current_data:
            QMessageBox.warning(
                self.main_window,
                "No Data Loaded",
                "Please load mesh data first."
            )
            return False

        return True

    def _parse_fem_dat(self):
        """Parse fem.dat file to extract thickness"""
        visualization_manager = self.main_window.visualization_manager
        working_dir = visualization_manager.working_directory

        if not working_dir:
            return None

        fem_dat_path = os.path.join(working_dir, 'fem.dat')

        if not os.path.exists(fem_dat_path):
            logger.warning(f"fem.dat not found in {working_dir}")
            return None

        try:
            with open(fem_dat_path, 'r') as f:
                lines = f.readlines()

            if len(lines) < 5:
                logger.warning("fem.dat file is too short")
                return None

            # Parse line 5: nnode,ntype,ntoch,nfric,ncrit,ncrck
            line5_parts = lines[4].strip().split()
            if len(line5_parts) >= 2:
                ntype = int(line5_parts[1])

                # If ntype >= 2, thickness is on line 6
                if ntype >= 2 and len(lines) > 5:
                    thick_line = lines[5].strip()
                    thickness = float(thick_line.replace('D', 'E'))
                    logger.info(f"Found thickness: {thickness}")
                    return thickness

        except Exception as e:
            logger.exception(f"Error parsing fem.dat: {e}")

        return None

    def _build_3d_model(self, model_type, params):
        """Build 3D model from 2D data"""
        try:
            step = params['step']
            visualization_manager = self.main_window.visualization_manager
            visualization_manager._on_mesh_spinbox_changed(step)
            current_data = visualization_manager.current_data

            if not current_data:
                return

            progress_dialog = self._create_progress_dialog()
            progress_dialog.show()

            try:
                data_3d = self._create_3d_neutral_file(
                    current_data, model_type, params, progress_dialog
                )

                progress_dialog.close()

                if data_3d:
                    # Load the 3D model in visualization
                    visualization_manager.load_neutral_file(data_3d, True)

                    QMessageBox.information(
                        self.main_window,
                        "3D Model Created",
                        f"3D {model_type.replace('_', ' ').title()} model created successfully!"
                    )
                else:
                    QMessageBox.warning(
                        self.main_window,
                        "Error",
                        "Failed to create 3D model."
                    )

            except Exception as e:
                progress_dialog.close()
                raise e

        except Exception as e:
            logger.exception(f"Error building 3D model: {e}")
            QMessageBox.critical(
                self.main_window,
                "Error",
                f"Error building 3D model: {str(e)}"
            )

    def _create_progress_dialog(self):
        """Create progress dialog for 3D model creation"""

        progress_dialog = QProgressDialog(
            "Creating 3D model...",
            "Cancel",
            0,
            100,
            self.main_window
        )
        progress_dialog.setWindowTitle("Building 3D Model")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.setAutoClose(False)
        progress_dialog.setAutoReset(False)
        progress_dialog.setCancelButton(None)

        return progress_dialog

    def _create_3d_neutral_file(self, data_2d, model_type, params, progress_dialog):
        """Create 3D neutral file from 2D data"""

        # Create new 3D neutral file
        title_3d = f"3D_{model_type}_{data_2d.get_title()}"
        neutral_3d = NeutralFile3D(title_3d)
        neutral_3d.set_t_time(data_2d.get_t_time())

        # Create 3D nodes
        self._create_3d_nodes(data_2d, neutral_3d, model_type, params)

        # Create 3D elements
        self._create_3d_elements(
            data_2d, neutral_3d, model_type, params, progress_dialog)

        # Create 3D dies if any
        self._create_3d_dies(data_2d, neutral_3d, model_type, params)

        return neutral_3d

    def _create_3d_nodes(self, data_2d, neutral_3d, model_type, params):
        """Create 3D nodes from 2D nodes"""

        divisions = params['divisions']
        nodes_2d = list(data_2d.get_nodes())

        if model_type in ["axisymmetric", "axisymmetric_cheese"]:
            # Axisymmetric models: rotate around Z axis
            angle_total = 2 * math.pi
            if model_type == "axisymmetric_cheese":
                angle_total = math.radians(params['angle'])

            for i_div in range(divisions + 1):
                alpha = (angle_total * i_div) / divisions

                for node_2d in nodes_2d:
                    node_id_3d = node_2d.get_id() + i_div * len(nodes_2d)

                    # Convert r,z to x,y,z
                    r = node_2d.get_coordX()
                    z = node_2d.get_coordY()

                    x = r * math.cos(alpha)
                    y = r * math.sin(alpha)

                    node_3d = Node3D(node_id_3d)
                    node_3d.set_coordX(x)
                    node_3d.set_coordY(y)
                    node_3d.set_coordZ(z)

                    # Copy other properties
                    if node_2d.get_Vx() is not None:
                        vx = node_2d.get_Vx() * math.cos(alpha)
                        vy = node_2d.get_Vx() * math.sin(alpha)
                        node_3d.set_Vx(vx)
                        node_3d.set_Vy(vy)

                    if node_2d.get_Fx() is not None:
                        fx = node_2d.get_Fx() * math.cos(alpha)
                        fy = node_2d.get_Fx() * math.sin(alpha)
                        node_3d.set_Fx(fx)
                        node_3d.set_Fy(fy)

                    node_3d.set_Temp(node_2d.get_Temp())
                    node_3d.set_DTemp(node_2d.get_DTemp())
                    node_3d.set_code(node_2d.get_code())
                    node_3d.set_is_contact(node_2d.is_contact_node())

                    neutral_3d.add_node(node_3d)

        else:  # plane_strain or plane_stress
            thickness = params['thickness']

            for i_div in range(divisions + 1):
                if model_type == "plane_stress":
                    # For plane stress: calculate correction based on minimum z strain
                    z = self._calculate_plane_stress_z_coordinate(
                        data_2d, thickness, i_div, divisions)
                else:  # plane_strain
                    # For plane strain: simple linear distribution
                    z = (thickness * i_div) / divisions

                for node_2d in nodes_2d:
                    node_id_3d = node_2d.get_id() + i_div * len(nodes_2d)

                    node_3d = Node3D(node_id_3d)
                    node_3d.set_coordX(node_2d.get_coordX())
                    node_3d.set_coordY(node_2d.get_coordY())
                    node_3d.set_coordZ(z)

                    # Copy velocities and forces
                    node_3d.set_Vx(node_2d.get_Vx())
                    node_3d.set_Vy(node_2d.get_Vy())

                    node_3d.set_Fx(node_2d.get_Fx())
                    node_3d.set_Fy(node_2d.get_Fy())

                    node_3d.set_Temp(node_2d.get_Temp())
                    node_3d.set_DTemp(node_2d.get_DTemp())
                    node_3d.set_code(node_2d.get_code())
                    node_3d.set_is_contact(node_2d.is_contact_node())

                    neutral_3d.add_node(node_3d)

    def _create_3d_elements(self, data_2d, neutral_3d, model_type, params, progress_dialog=None):
        """Create 3D elements (hexahedra) from 2D elements (quads)"""

        divisions = params['divisions']
        elements_2d = list(data_2d.get_elements())
        nodes_2d_count = len(list(data_2d.get_nodes()))

        total_elements = len(elements_2d) * divisions
        elements_created = 0

        for i_div in range(divisions):
            for elem_2d in elements_2d:
                elem_id_3d = elem_2d.get_id() + i_div * len(elements_2d)

                elem_3d = Element3D(elem_id_3d)
                elem_3d.set_matno(elem_2d.get_matno())

                # Get 2D nodes
                nodes_2d = elem_2d.get_lnods()

                # Create hexahedron from quad
                # Bottom face (current level)
                node1_3d_id = nodes_2d[0].get_id() + i_div * nodes_2d_count
                node2_3d_id = nodes_2d[1].get_id() + i_div * nodes_2d_count
                node3_3d_id = nodes_2d[2].get_id() + i_div * nodes_2d_count
                node4_3d_id = nodes_2d[3].get_id() + i_div * nodes_2d_count

                # Top face (next level)
                if i_div == divisions - 1 and model_type in ["axisymmetric"]:
                    # For full axisymmetric, connect to first layer
                    node5_3d_id = nodes_2d[0].get_id()
                    node6_3d_id = nodes_2d[1].get_id()
                    node7_3d_id = nodes_2d[2].get_id()
                    node8_3d_id = nodes_2d[3].get_id()
                else:
                    node5_3d_id = nodes_2d[0].get_id(
                    ) + (i_div + 1) * nodes_2d_count
                    node6_3d_id = nodes_2d[1].get_id(
                    ) + (i_div + 1) * nodes_2d_count
                    node7_3d_id = nodes_2d[2].get_id(
                    ) + (i_div + 1) * nodes_2d_count
                    node8_3d_id = nodes_2d[3].get_id(
                    ) + (i_div + 1) * nodes_2d_count

                # Get actual node objects
                node1_3d = neutral_3d.get_node_by_id(node1_3d_id)
                node2_3d = neutral_3d.get_node_by_id(node2_3d_id)
                node3_3d = neutral_3d.get_node_by_id(node3_3d_id)
                node4_3d = neutral_3d.get_node_by_id(node4_3d_id)
                node5_3d = neutral_3d.get_node_by_id(node5_3d_id)
                node6_3d = neutral_3d.get_node_by_id(node6_3d_id)
                node7_3d = neutral_3d.get_node_by_id(node7_3d_id)
                node8_3d = neutral_3d.get_node_by_id(node8_3d_id)

                # Set hexahedron nodes
                elem_3d.set_lnods([node1_3d, node2_3d, node3_3d, node4_3d,
                                   node5_3d, node6_3d, node7_3d, node8_3d])

                # Copy element properties and transform for 3D
                self._copy_element_properties_3d(
                    elem_2d, elem_3d, model_type, i_div, divisions, params)

                neutral_3d.add_element(elem_3d)

                elements_created += 1

                # Update progress every 300 elements to avoid slowing down
                if elements_created % 300 == 0:
                    progress_percent = int(elements_created / total_elements)
                    progress_dialog.setValue(progress_percent)
                    self.main_window.repaint()

        progress_dialog.setValue(80)

    def _copy_element_properties_3d(self, elem_2d, elem_3d, model_type, i_div, divisions, params):
        """Copy and transform element properties for 3D"""
        # Copy basic properties
        elem_3d.set_rindx(elem_2d.get_rindx())
        elem_3d.set_densy(elem_2d.get_densy())
        elem_3d.set_fract(elem_2d.get_fract())

        # Transform strains and stresses based on model type
        if model_type in ["axisymmetric", "axisymmetric_cheese"]:
            # Axisymmetric transformation
            angle_total = 2 * math.pi
            if model_type == "axisymmetric_cheese":
                angle_total = math.radians(params['angle'])

            alpha = (angle_total * (i_div + 0.5)) / \
                divisions  # Mid-element angle

            # Transform strains (r,z,theta,rz) -> (x,y,z,xy,yz,zx)
            strain_r = elem_2d.get_strain_Exx() or 0.0
            strain_z = elem_2d.get_strain_Eyy() or 0.0
            strain_t = elem_2d.get_strain_Ezz() or 0.0

            strain_x = strain_r * \
                math.cos(alpha)**2 + strain_t * math.sin(alpha)**2
            strain_y = strain_r * \
                math.sin(alpha)**2 + strain_t * math.cos(alpha)**2
            strain_xy = (strain_r - strain_t) * \
                math.cos(alpha) * math.sin(alpha)

            elem_3d.set_strain_Exx(strain_x)
            elem_3d.set_strain_Eyy(strain_y)
            elem_3d.set_strain_Ezz(strain_z)
            elem_3d.set_strain_Exy(strain_xy)

            # Similar transformation for stresses
            stress_r = elem_2d.get_stress_Oxx() or 0.0
            stress_z = elem_2d.get_stress_Oyy() or 0.0
            stress_t = elem_2d.get_stress_Ozz() or 0.0

            stress_x = stress_r * \
                math.cos(alpha)**2 + stress_t * math.sin(alpha)**2
            stress_y = stress_r * \
                math.sin(alpha)**2 + stress_t * math.cos(alpha)**2
            stress_xy = (stress_r - stress_t) * \
                math.cos(alpha) * math.sin(alpha)

            elem_3d.set_stress_Oxx(stress_x)
            elem_3d.set_stress_Oyy(stress_y)
            elem_3d.set_stress_Ozz(stress_z)
            elem_3d.set_stress_Oxy(stress_xy)

        else:  # plane_strain or plane_stress
            # Direct copy with zero Z components
            elem_3d.set_strain_Exx(elem_2d.get_strain_Exx())
            elem_3d.set_strain_Eyy(elem_2d.get_strain_Eyy())
            elem_3d.set_strain_Ezz(elem_2d.get_strain_Ezz())
            elem_3d.set_strain_Exy(elem_2d.get_strain_Exy())

            elem_3d.set_stress_Oxx(elem_2d.get_stress_Oxx())
            elem_3d.set_stress_Oyy(elem_2d.get_stress_Oyy())
            elem_3d.set_stress_Ozz(elem_2d.get_stress_Ozz())
            elem_3d.set_stress_Oxy(elem_2d.get_stress_Oxy())

        # Copy other properties
        elem_3d.set_strain_E(elem_2d.get_strain_E())
        elem_3d.set_stress_O(elem_2d.get_stress_O())
        elem_3d.set_stress_Orr(elem_2d.get_stress_Orr())

        # Copy strain rates
        elem_3d.set_strain_rate_E(elem_2d.get_strain_rate_E())
        elem_3d.set_strain_rate_Ev(elem_2d.get_strain_rate_Ev())

    def _create_3d_dies(self, data_2d, neutral_3d, model_type, params):
        """Create 3D dies from 2D dies"""
        dies_2d = data_2d.get_dies()

        if not dies_2d:
            return

        divisions = params['divisions']
        thickness = params.get('thickness', 1.0)

        if model_type == "plane_stress":
            thickness /= 2.0

        for die_2d in dies_2d:
            die_3d = Die3D(die_2d.get_id())
            die_3d.set_temp(die_2d.get_temp())
            die_3d.set_m(die_2d.get_m())

            die_nodes_2d = die_2d.nodes

            if model_type in ["axisymmetric", "axisymmetric_cheese"]:
                angle_total = 2 * math.pi
                if model_type == "axisymmetric_cheese":
                    angle_total = math.radians(params['angle'])

                for i_div in range(divisions + 1):
                    alpha = (angle_total * i_div) / divisions

                    for node_2d in die_nodes_2d:
                        # Convert r,z to x,y,z for axisymmetric
                        r = node_2d.get_coordX()
                        z = node_2d.get_coordY()

                        x = r * math.cos(alpha)
                        y = r * math.sin(alpha)

                        # Create 3D node with unique ID
                        node_3d_id = -(1000 + die_2d.get_id() * 1000 +
                                       i_div * 100 + len(die_3d.get_nodes()))
                        node_3d = Node3D(node_3d_id)
                        node_3d.set_coordX(x)
                        node_3d.set_coordY(y)
                        node_3d.set_coordZ(z)

                        die_3d.add_node(node_3d)

            else:  # plane_strain or plane_stress
                for i_div in range(divisions + 1):
                    z = (thickness * i_div) / divisions

                    for node_2d in die_nodes_2d:
                        # Create 3D node with unique ID
                        node_3d_id = -(1000 + die_2d.get_id() * 1000 +
                                       i_div * 100 + len(die_3d.get_nodes()))
                        node_3d = Node3D(node_3d_id)
                        node_3d.set_coordX(node_2d.get_coordX())
                        node_3d.set_coordY(node_2d.get_coordY())
                        node_3d.set_coordZ(z)

                        die_3d.add_node(node_3d)

            neutral_3d.add_die(die_3d)

    def _calculate_plane_stress_z_coordinate(self, data_2d, thickness, i_div, divisions):
        """Calculate Z coordinate for plane stress model with strain correction"""

        if i_div == 0:
            return 0.0

        strain_z_min = 1.0e+10

        elements = list(data_2d.get_elements())
        for element in elements:
            strain_z = element.get_strain_Ezz() or 0.0
            if strain_z < strain_z_min:
                strain_z_min = strain_z

        correction = math.exp(strain_z_min)

        thickz = (0.5 * thickness * correction *
                  float(i_div)) / float(divisions)

        return thickz


class Build3DDialog(QDialog):
    def __init__(self, parent=None, model_type="plane_strain"):
        super().__init__(parent)
        self.model_type = model_type
        self.thick = 1.0
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Build 3D Model")
        self.setFixedSize(400, 250)

        layout = QVBoxLayout()

        # Step Number section
        step_group = QGroupBox("Step Number")
        step_layout = QHBoxLayout()

        self.step_spinbox = QSpinBox()
        self.step_spinbox.setMinimum(1)
        self.step_spinbox.setMaximum(9999)
        self.step_spinbox.setValue(1)

        step_layout.addWidget(QLabel("Step Number:"))
        step_layout.addWidget(self.step_spinbox)
        step_layout.addStretch()

        step_group.setLayout(step_layout)
        layout.addWidget(step_group)

        # Model specific section
        model_group = QGroupBox()
        model_layout = QVBoxLayout()

        if self.model_type in ["axisymmetric", "axisymmetric_cheese"]:
            model_group.setTitle("Solid/Cheese Model")

            # Number of Divisions
            div_layout = QHBoxLayout()
            div_layout.addWidget(QLabel("Number of Divisions:"))
            self.divisions_spinbox = QSpinBox()
            self.divisions_spinbox.setMinimum(1)
            self.divisions_spinbox.setMaximum(999)
            self.divisions_spinbox.setValue(16)
            div_layout.addWidget(self.divisions_spinbox)
            div_layout.addStretch()
            model_layout.addLayout(div_layout)

            # Angle (only for cheese model)
            if self.model_type == "axisymmetric_cheese":
                angle_layout = QHBoxLayout()
                angle_layout.addWidget(
                    QLabel("Angle of the Rotational Cut (Degrees):"))
                self.angle_spinbox = QDoubleSpinBox()
                self.angle_spinbox.setMinimum(0.01)
                self.angle_spinbox.setMaximum(360.0)
                self.angle_spinbox.setValue(225.0)
                self.angle_spinbox.setDecimals(2)
                angle_layout.addWidget(self.angle_spinbox)
                angle_layout.addStretch()
                model_layout.addLayout(angle_layout)

        else:  # plane_strain or plane_stress
            model_group.setTitle("Plane Model")

            # Number of Divisions
            div_layout = QHBoxLayout()
            div_layout.addWidget(QLabel("Number of Divisions:"))
            self.divisions_spinbox = QSpinBox()
            self.divisions_spinbox.setMinimum(1)
            self.divisions_spinbox.setMaximum(999)
            self.divisions_spinbox.setValue(16)
            div_layout.addWidget(self.divisions_spinbox)
            div_layout.addStretch()
            model_layout.addLayout(div_layout)

            # Thickness display
            thick_layout = QHBoxLayout()
            thick_layout.addWidget(QLabel("Thickness:"))
            self.thickness_label = QLabel(f"{self.thick:.2f}")
            thick_layout.addWidget(self.thickness_label)
            thick_layout.addStretch()
            model_layout.addLayout(thick_layout)

        model_group.setLayout(model_layout)
        layout.addWidget(model_group)

        # Buttons
        button_layout = QHBoxLayout()

        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)

        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.reject)

        button_layout.addWidget(ok_btn)
        button_layout.addWidget(exit_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def set_thickness(self, thickness):
        """Set thickness value from fem.dat parsing"""
        self.thick = thickness
        if hasattr(self, 'thickness_label'):
            self.thickness_label.setText(f"{thickness:.2f}")

    def get_parameters(self):
        """Get dialog parameters"""
        params = {
            'step': self.step_spinbox.value(),
            'divisions': self.divisions_spinbox.value(),
            'thickness': self.thick
        }

        if self.model_type == "axisymmetric_cheese":
            params['angle'] = self.angle_spinbox.value()

        return params
