"""
XY Graphics Dialog for Dies Data
Simple dialog matching the provided interface
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QRadioButton,
                             QGroupBox, QSpinBox, QCheckBox,
                             QButtonGroup, QLineEdit, QComboBox)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
import logging
logger = logging.getLogger(__name__)


class XYGraphicsDialog(QDialog):
    def __init__(self, parent, neutral_data):
        super().__init__(parent)
        self.neutral_data = neutral_data
        
        self.setWindowTitle("Graphics")
        self.setFixedSize(640, 600)
        self.setModal(False)
        
        # Create matplotlib figure and canvas
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)

        self.created_figures = []
        
        self.setup_ui()
        self.setup_connections()

        self.update_step_limits()
        
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout()
        
        # Step controls
        step_layout = QHBoxLayout()
        
        # Initial Step Number
        step_layout.addWidget(QLabel("Initial Step Number"))
        self.initial_step = QSpinBox()
        self.initial_step.setMinimum(0)
        self.initial_step.setMaximum(999)
        self.initial_step.setValue(0)
        step_layout.addWidget(self.initial_step)
        
        step_layout.addStretch()
        
        # Final Step Number
        step_layout.addWidget(QLabel("Final Step Number"))
        self.final_step = QSpinBox()
        self.final_step.setMinimum(1)
        self.final_step.setMaximum(999)
        self.final_step.setValue(100)
        step_layout.addWidget(self.final_step)
        
        # Navigation buttons
        self.prev_btn = QPushButton("◄")
        self.prev_btn.setMaximumWidth(30)
        self.next_btn = QPushButton("►")
        self.next_btn.setMaximumWidth(30)
        step_layout.addWidget(self.prev_btn)
        step_layout.addWidget(self.next_btn)
        
        step_layout.addStretch()
        
        # Frequency
        step_layout.addWidget(QLabel("Frequency"))
        self.frequency = QSpinBox()
        self.frequency.setMinimum(1)
        self.frequency.setMaximum(1000)
        self.frequency.setValue(1)
        step_layout.addWidget(self.frequency)
        
        layout.addLayout(step_layout)
        
        # Axes selection
        axes_layout = QHBoxLayout()
        
        # X-axis group
        x_group = QGroupBox("X - axis")
        x_layout = QVBoxLayout()
        
        self.x_button_group = QButtonGroup()
        self.x_step = QRadioButton("Step Number")
        self.x_step.setChecked(True)
        self.x_vertical_disp = QRadioButton("Vertical Displacement")
        self.x_horizontal_disp = QRadioButton("Horizontal Displacement")
        self.x_time = QRadioButton("Time")
        
        self.x_button_group.addButton(self.x_step, 0)
        self.x_button_group.addButton(self.x_vertical_disp, 1)
        self.x_button_group.addButton(self.x_horizontal_disp, 2)
        self.x_button_group.addButton(self.x_time, 3)
        
        x_layout.addWidget(self.x_step)
        x_layout.addWidget(self.x_vertical_disp)
        x_layout.addWidget(self.x_horizontal_disp)
        x_layout.addWidget(self.x_time)
        
        x_group.setLayout(x_layout)
        axes_layout.addWidget(x_group)
        
        # Y-axis group
        y_group = QGroupBox("Y - axis")
        y_layout = QVBoxLayout()
        
        self.y_button_group = QButtonGroup()
        self.y_vertical_force = QRadioButton("Vertical Force")
        self.y_vertical_force.setChecked(True)
        self.y_horizontal_force = QRadioButton("Horizontal Force")
        self.y_vertical_velocity = QRadioButton("Vertical Velocity")
        self.y_horizontal_velocity = QRadioButton("Horizontal Velocity")
        self.y_error = QRadioButton("Error (Zienkiewicz - Zhu)")
        self.y_volume = QRadioButton("Volume (Normalised Variation)")
        
        self.y_button_group.addButton(self.y_vertical_force, 0)
        self.y_button_group.addButton(self.y_horizontal_force, 1)
        self.y_button_group.addButton(self.y_vertical_velocity, 2)
        self.y_button_group.addButton(self.y_horizontal_velocity, 3)
        self.y_button_group.addButton(self.y_error, 4)
        self.y_button_group.addButton(self.y_volume, 5)
        
        y_layout.addWidget(self.y_vertical_force)
        y_layout.addWidget(self.y_horizontal_force)
        y_layout.addWidget(self.y_vertical_velocity)
        y_layout.addWidget(self.y_horizontal_velocity)
        y_layout.addWidget(self.y_error)
        y_layout.addWidget(self.y_volume)
        
        # Die Number
        die_layout = QHBoxLayout()
        die_layout.addWidget(QLabel("Die Number"))
        self.die_number = QComboBox()
        self.update_die_numbers()
        die_layout.addWidget(self.die_number)
        y_layout.addLayout(die_layout)
        
        y_group.setLayout(y_layout)
        axes_layout.addWidget(y_group)
        
        layout.addLayout(axes_layout)
        
        format_group = QGroupBox("Format")
        format_layout = QVBoxLayout()
        
        # Scientific/Fixed style
        style_layout = QHBoxLayout()
        self.scientific = QRadioButton("Scientific")
        self.scientific.setChecked(True)
        self.fixed_style = QRadioButton("Fixed Style")
        style_layout.addWidget(self.scientific)
        style_layout.addWidget(self.fixed_style)
        format_layout.addLayout(style_layout)
        
        # Absolute values
        self.absolute_values = QCheckBox("Absolute Values")
        format_layout.addWidget(self.absolute_values)
        self.absolute_values.setChecked(True)
        
        # Significant Digits
        digits_layout = QHBoxLayout()
        digits_layout.addWidget(QLabel("Significant Digits"))
        digits_layout.addWidget(QLabel("X - axis"))
        digits_layout.addWidget(QLabel("Y - axis"))
        format_layout.addLayout(digits_layout)
        
        sig_layout = QHBoxLayout()
        sig_layout.addWidget(QLabel(""))
        self.x_sig_digits = QSpinBox()
        self.x_sig_digits.setMinimum(1)
        self.x_sig_digits.setMaximum(10)
        self.x_sig_digits.setValue(5)
        self.y_sig_digits = QSpinBox()
        self.y_sig_digits.setMinimum(1)
        self.y_sig_digits.setMaximum(10)
        self.y_sig_digits.setValue(5)
        sig_layout.addWidget(self.x_sig_digits)
        sig_layout.addWidget(self.y_sig_digits)
        format_layout.addLayout(sig_layout)
        
        # Decimal Places
        decimal_layout = QHBoxLayout()
        decimal_layout.addWidget(QLabel("Decimal Places"))
        self.x_decimal = QSpinBox()
        self.x_decimal.setMinimum(0)
        self.x_decimal.setMaximum(10)
        self.x_decimal.setValue(2)
        self.y_decimal = QSpinBox()
        self.y_decimal.setMinimum(0)
        self.y_decimal.setMaximum(10)
        self.y_decimal.setValue(2)
        decimal_layout.addWidget(self.x_decimal)
        decimal_layout.addWidget(self.y_decimal)
        format_layout.addLayout(decimal_layout)
        
        # Number Ticks
        ticks_layout = QHBoxLayout()
        ticks_layout.addWidget(QLabel("Number Ticks"))
        self.x_ticks = QSpinBox()
        self.x_ticks.setMinimum(1)
        self.x_ticks.setMaximum(20)
        self.x_ticks.setValue(11)
        self.y_ticks = QSpinBox()
        self.y_ticks.setMinimum(1)
        self.y_ticks.setMaximum(20)
        self.y_ticks.setValue(11)
        ticks_layout.addWidget(self.x_ticks)
        ticks_layout.addWidget(self.y_ticks)
        format_layout.addLayout(ticks_layout)
        
        format_group.setLayout(format_layout)
        layout.addWidget(format_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.ok_button = QPushButton("OK")
        self.ok_button.setMinimumWidth(80)
        self.exit_button = QPushButton("Exit")
        self.exit_button.setMinimumWidth(80)
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.exit_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.ok_button.clicked.connect(self.generate_plot)
        self.exit_button.clicked.connect(self.close)
        self.prev_btn.clicked.connect(self.previous_step)
        self.next_btn.clicked.connect(self.next_step)
    
    def update_die_numbers(self):
        """Update die number combo box"""
        if not self.neutral_data:
            return
            
        dies = self.neutral_data.get_dies()
        self.die_number.clear()
        
        for die in dies:
            self.die_number.addItem(str(die.get_id()))
    
    def previous_step(self):
        """Go to previous step"""
        current = self.final_step.value()
        if current > self.initial_step.value() + 1:
            self.final_step.setValue(current - 1)
    
    def next_step(self):
        """Go to next step"""
        current = self.final_step.value()
        self.final_step.setValue(current + 1)
    
    def get_selected_die(self):
        """Get selected die object"""
        if not self.neutral_data:
            return None
            
        selected_id = int(self.die_number.currentText()) if self.die_number.currentText() else None
        if selected_id is None:
            return None
            
        for die in self.neutral_data.get_dies():
            if die.get_id() == selected_id:
                return die
        return None
    
    def get_multiple_files_data(self):
        """Get data from multiple NEU files if available"""
        # Check if we have access to multiple files through the main window
        visualization_manager = self.parent().visualization_manager
        
        if not hasattr(visualization_manager, 'neu_files') or not visualization_manager.neu_files:
            return None
            
        if not hasattr(visualization_manager, 'preloaded_data') or not visualization_manager.preloaded_data:
            return None
            
        return visualization_manager.preloaded_data
    
    def get_x_data(self):
        """Get X-axis data from multiple files"""
        x_selection = self.x_button_group.checkedId()
        
        # Get multiple files data
        multiple_data = self.get_multiple_files_data()
        
        if multiple_data:
            x_data = []
            die_id = int(self.die_number.currentText()) if self.die_number.currentText() else 1
            
            sorted_indices = sorted(multiple_data.keys())
            
            initial_step = self.initial_step.value()
            final_step = self.final_step.value()
            frequency = int(self.frequency.value())
            
            filtered_indices = []
            for i, file_index in enumerate(sorted_indices):
                step_number = i + 1
                if initial_step <= step_number <= final_step:
                    # Appliquer la fréquence
                    if (step_number - initial_step) % frequency == 0:
                        filtered_indices.append((i, file_index))
            
            # Get initial coordinates from first file for displacement calculation
            initial_coords = None
            if x_selection in [1, 2] and filtered_indices:  # Displacement modes
                first_data = multiple_data[filtered_indices[0][1]]
                first_die = self._find_die_in_data(first_data, die_id)
                if first_die and first_die.get_main_node():
                    initial_coords = {
                        'x': first_die.get_main_node().get_coordX() or 0.0,
                        'y': first_die.get_main_node().get_coordY() or 0.0
                    }
            
            for i, file_index in filtered_indices:
                neutral_data = multiple_data[file_index]
                die = self._find_die_in_data(neutral_data, die_id)
                
                if x_selection == 0:  # Step Number
                    x_data.append(i + 1)  # Step number réel
                elif x_selection == 1:  # Vertical Displacement
                    if die and die.get_main_node() and initial_coords:
                        current_y = die.get_main_node().get_coordY() or 0.0
                        displacement = current_y - initial_coords['y']
                        x_data.append(-displacement)
                    else:
                        x_data.append(0.0)
                elif x_selection == 2:  # Horizontal Displacement
                    if die and die.get_main_node() and initial_coords:
                        current_x = die.get_main_node().get_coordX() or 0.0
                        displacement = current_x - initial_coords['x']
                        x_data.append(displacement)
                    else:
                        x_data.append(0.0)
                elif x_selection == 3:  # Time
                    x_data.append(neutral_data.get_t_time() or 0.0)
            
            return x_data
        else:
            # Single file - fallback to single point
            if x_selection == 0:  # Step Number
                return [1]
            elif x_selection == 1:  # Vertical Displacement
                die = self.get_selected_die()
                if die and die.get_main_node():
                    displacement = die.get_main_node().get_coordY() or 0.0
                    return [-displacement]
            elif x_selection == 2:  # Horizontal Displacement
                die = self.get_selected_die()
                if die and die.get_main_node():
                    return [die.get_main_node().get_coordX() or 0.0]
            elif x_selection == 3:  # Time
                return [self.neutral_data.get_t_time() or 0.0]
            
            return [0.0]

    def get_y_data(self):
        """Get Y-axis data from multiple files"""
        y_selection = self.y_button_group.checkedId()
        
        # Skip Error and Volume (not implemented)
        if y_selection in [4, 5]:  # Error or Volume
            return [0.0]
        
        # Get multiple files data
        multiple_data = self.get_multiple_files_data()
        
        if multiple_data:
            # We have multiple files - create proper time series
            y_data = []
            die_id = int(self.die_number.currentText()) if self.die_number.currentText() else 1
            
            # Get sorted file indices
            sorted_indices = sorted(multiple_data.keys())
            
            initial_step = self.initial_step.value()
            final_step = self.final_step.value()
            frequency = int(self.frequency.value())
            
            # Filtrer les indices selon les paramètres
            filtered_indices = []
            for i, file_index in enumerate(sorted_indices):
                step_number = i + 1  # Step commence à 1
                if initial_step <= step_number <= final_step:
                    # Appliquer la fréquence
                    if (step_number - initial_step) % frequency == 0:
                        filtered_indices.append(file_index)
            
            for file_index in filtered_indices:
                neutral_data = multiple_data[file_index]
                die = self._find_die_in_data(neutral_data, die_id)
                
                if die and die.get_main_node():
                    main_node = die.get_main_node()
                    
                    if y_selection == 0:  # Vertical Force
                        force_y = main_node.get_Fy() or 0.0
                        y_data.append(-force_y)
                    elif y_selection == 1:  # Horizontal Force
                        force_x = main_node.get_Fx() or 0.0
                        y_data.append(-force_x)
                    elif y_selection == 2:  # Vertical Velocity
                        velocity_y = main_node.get_Vy() or 0.0
                        y_data.append(-velocity_y)
                    elif y_selection == 3:  # Horizontal Velocity
                        velocity_x = main_node.get_Vx() or 0.0
                        y_data.append(-velocity_x)
                    else:
                        y_data.append(0.0)
                else:
                    y_data.append(0.0)
            
            return y_data
        else:
            # Single file - fallback to single point
            die = self.get_selected_die()
            
            if not die or not die.get_main_node():
                return [0.0]
            
            main_node = die.get_main_node()
            
            if y_selection == 0:  # Vertical Force
                force_y = main_node.get_Fy() or 0.0
                return [-force_y]
            elif y_selection == 1:  # Horizontal Force
                return [main_node.get_Fx() or 0.0]
            elif y_selection == 2:  # Vertical Velocity
                velocity_y = main_node.get_Vy() or 0.0
                return [-velocity_y]
            elif y_selection == 3:  # Horizontal Velocity
                return [main_node.get_Vx() or 0.0]
            
            return [0.0]
    
    def _find_die_in_data(self, neutral_data, die_id):
        """Find a specific die in neutral data by ID"""
        for die in neutral_data.get_dies():
            if die.get_id() == die_id:
                return die
        return None
    
    def get_axis_labels(self):
        """Get axis labels"""
        x_labels = ["Step Number", "Vertical Displacement", "Horizontal Displacement", "Time"]
        y_labels = ["Vertical Force", "Horizontal Force", "Vertical Velocity", 
                   "Horizontal Velocity", "Error (Not Implemented)", "Volume (Not Implemented)"]
        
        x_id = self.x_button_group.checkedId()
        y_id = self.y_button_group.checkedId()
        
        x_label = x_labels[x_id] if 0 <= x_id < len(x_labels) else "X"
        y_label = y_labels[y_id] if 0 <= y_id < len(y_labels) else "Y"
        
        return x_label, y_label
    
    def generate_plot(self):
        """Generate the plot with current settings"""
        try:
            # Get data
            x_data = self.get_x_data()
            y_data = self.get_y_data()
            x_label, y_label = self.get_axis_labels()
            
            # Check if we have enough data points
            if len(x_data) != len(y_data):
                min_len = min(len(x_data), len(y_data))
                x_data = x_data[:min_len]
                y_data = y_data[:min_len]
            
            if len(x_data) == 0:
                plt.ion()  # Mode interactif
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.text(0.5, 0.5, "No data available for plotting", 
                    ha='center', va='center', transform=ax.transAxes)
                ax.set_title("XY Graphics - No Data")
                plt.show()
                plt.ioff()  # Désactiver le mode interactif
                return
            
            # Activer le mode interactif
            plt.ion()
            
            # Create a proper plot window
            fig, ax = plt.subplots(figsize=(12, 7))

            self.created_figures.append(fig)
            
            # Apply absolute values if requested
            if self.absolute_values.isChecked():
                x_data = [abs(x) for x in x_data]
                y_data = [abs(y) for y in y_data]
            
            # Plot with proper line style
            if len(x_data) == 1:
                # Single point
                ax.plot(x_data, y_data, 'ro', markersize=8, label='Data Point')
            else:
                # Multiple points - line chart
                ax.plot(x_data, y_data, 'b-', linewidth=2, marker='o', markersize=4, label='Data')
            
            # Labels and title
            ax.set_xlabel(x_label, fontsize=12)
            ax.set_ylabel(y_label, fontsize=12)
            ax.set_title(f"{y_label} vs {x_label} (Die {self.die_number.currentText()})", fontsize=14)
            
            # Grid
            ax.grid(True, alpha=0.3)
            
            # Legend if multiple points
            if len(x_data) > 1:
                ax.legend()
            
            # === NUMBER OF TICKS ===
            x_min, x_max = ax.get_xlim()
            y_min, y_max = ax.get_ylim()
            
            x_ticks_count = max(2, self.x_ticks.value())
            y_ticks_count = max(2, self.y_ticks.value())
            
            x_ticks = np.linspace(x_min, x_max, x_ticks_count)
            y_ticks = np.linspace(y_min, y_max, y_ticks_count)
            
            ax.set_xticks(x_ticks)
            ax.set_yticks(y_ticks)
            
            # === FORMATTING ===
            if self.scientific.isChecked():
                # Scientific notation with significant digits
                
                x_sig = self.x_sig_digits.value()
                y_sig = self.y_sig_digits.value()
                
                def x_formatter(x, pos):
                    if x == 0:
                        return "0.0e+00"
                    precision = max(0, x_sig - 1)
                    return f"{x:.{precision}e}"
                
                def y_formatter(y, pos):
                    if y == 0:
                        return "0.0e+00"
                    precision = max(0, y_sig - 1)
                    return f"{y:.{precision}e}"
                
                ax.xaxis.set_major_formatter(FuncFormatter(x_formatter))
                ax.yaxis.set_major_formatter(FuncFormatter(y_formatter))
                
            else:
                # Fixed style with decimal places
                
                x_decimal = self.x_decimal.value()
                y_decimal = self.y_decimal.value()
                
                def x_formatter(x, pos):
                    return f"{x:.{x_decimal}f}"
                
                def y_formatter(y, pos):
                    return f"{y:.{y_decimal}f}"
                
                ax.xaxis.set_major_formatter(FuncFormatter(x_formatter))
                ax.yaxis.set_major_formatter(FuncFormatter(y_formatter))
            
            # Show statistics
            if len(x_data) > 1:
                stats_text = f"Points: {len(x_data)}\n"
                stats_text += f"X range: {min(x_data):.3e} to {max(x_data):.3e}\n"
                stats_text += f"Y range: {min(y_data):.3e} to {max(y_data):.3e}"
                
                ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
            
            # Adjust layout and show
            plt.tight_layout()
            plt.show()
            plt.ioff()  # Désactiver le mode interactif après affichage
            
        except Exception as e:
            logger.exception(f"Error generating plot: {e}")
            # Show error message
            plt.ion()
            fig, ax = plt.subplots(figsize=(6, 4))

            self.created_figures.append(fig)

            ax.text(0.5, 0.5, f"Error generating plot:\n{str(e)}", 
                ha='center', va='center', transform=ax.transAxes)
            ax.set_title("XY Graphics - Error")
            plt.show()
            plt.ioff()

    def closeEvent(self, event):
        """Override close event to close all matplotlib figures"""
        for fig in self.created_figures:
            try:
                plt.close(fig)
            except:
                pass
        plt.close('all')
        event.accept()

    def update_step_limits(self):
        """Update step number limits based on available files"""
        visualization_manager = self.parent().visualization_manager
        
        max_files = 1  # Default minimum
        
        max_files = len(visualization_manager.preloaded_data)
        
        # Update spinbox limits
        self.initial_step.setMinimum(1)
        self.initial_step.setMaximum(max_files)
        self.initial_step.setValue(1)
        
        self.final_step.setMinimum(1)
        self.final_step.setMaximum(max_files)
        self.final_step.setValue(max_files)