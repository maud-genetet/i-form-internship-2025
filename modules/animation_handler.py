"""
Animation Menu Handler
Manages mesh animation functionality with frame control and timing
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QSpinBox, QDoubleSpinBox, QSlider,
                             QCheckBox, QGroupBox, QMessageBox)
from PyQt5.QtCore import QTimer, Qt
import os


class AnimationHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._next_animation_frame)
        
        # Animation state
        self.is_animating = False
        self.current_frame = 0
        self.start_frame = 1
        self.end_frame = 1
        self.frame_delay = 500  # milliseconds
        self.loop_animation = True
        self.reverse_direction = False
        self.animation_direction = 1  # 1 for forward, -1 for backward
        
        # Animation dialog
        self.animation_dialog = None
    
    def show_animation_dialog(self):
        """Show animation control dialog"""
        if not self._check_animation_available():
            return
            
        if self.animation_dialog is None:
            self._create_animation_dialog()
        
        self._update_dialog_values()
        self.animation_dialog.show()
        self.animation_dialog.raise_()
        self.animation_dialog.activateWindow()
    
    def _check_animation_available(self):
        """Check if animation is available (deformed mesh loaded)"""
        visualization_manager = self.main_window.visualization_manager
        
        if not hasattr(visualization_manager, 'neu_files') or not visualization_manager.neu_files:
            QMessageBox.warning(
                self.main_window,
                "Animation Not Available",
                "Please load deformed mesh files first via Mesh > Deformed Mesh."
            )
            return False
        
        if len(visualization_manager.neu_files) < 2:
            QMessageBox.warning(
                self.main_window,
                "Animation Not Available", 
                "Animation requires at least 2 mesh files. Only 1 file found."
            )
            return False
            
        return True
    
    def _create_animation_dialog(self):
        """Create animation control dialog"""
        self.animation_dialog = QDialog(self.main_window)
        self.animation_dialog.setWindowTitle("Mesh Animation Controls")
        self.animation_dialog.setFixedSize(400, 500)
        
        layout = QVBoxLayout()
        
        # Frame Range Group
        frame_group = QGroupBox("Frame Range")
        frame_layout = QVBoxLayout()
        
        # Start frame
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("Start Frame:"))
        self.start_frame_spin = QSpinBox()
        self.start_frame_spin.setMinimum(1)
        self.start_frame_spin.valueChanged.connect(self._on_start_frame_changed)
        start_layout.addWidget(self.start_frame_spin)
        frame_layout.addLayout(start_layout)
        
        # End frame
        end_layout = QHBoxLayout()
        end_layout.addWidget(QLabel("End Frame:"))
        self.end_frame_spin = QSpinBox()
        self.end_frame_spin.setMinimum(1)
        self.end_frame_spin.valueChanged.connect(self._on_end_frame_changed)
        end_layout.addWidget(self.end_frame_spin)
        frame_layout.addLayout(end_layout)
        
        # Current frame slider
        self.frame_slider = QSlider(Qt.Horizontal)
        self.frame_slider.valueChanged.connect(self._on_slider_changed)
        frame_layout.addWidget(QLabel("Current Frame:"))
        frame_layout.addWidget(self.frame_slider)
        
        # Current frame display
        self.current_frame_label = QLabel("Frame: 1")
        frame_layout.addWidget(self.current_frame_label)
        
        frame_group.setLayout(frame_layout)
        layout.addWidget(frame_group)
        
        # Timing Group
        timing_group = QGroupBox("Animation Timing")
        timing_layout = QVBoxLayout()
        
        # Frame delay
        delay_layout = QHBoxLayout()
        delay_layout.addWidget(QLabel("Frame Delay (ms):"))
        self.delay_spin = QSpinBox()
        self.delay_spin.setMinimum(50)
        self.delay_spin.setMaximum(5000)
        self.delay_spin.setValue(500)
        self.delay_spin.setSuffix(" ms")
        self.delay_spin.valueChanged.connect(self._on_delay_changed)
        delay_layout.addWidget(self.delay_spin)
        timing_layout.addLayout(delay_layout)
        
        # FPS display
        self.fps_label = QLabel("FPS: 2.0")
        timing_layout.addWidget(self.fps_label)
        
        timing_group.setLayout(timing_layout)
        layout.addWidget(timing_group)
        
        # Options Group
        options_group = QGroupBox("Animation Options")
        options_layout = QVBoxLayout()
        
        self.loop_checkbox = QCheckBox("Loop Animation")
        self.loop_checkbox.setChecked(True)
        self.loop_checkbox.toggled.connect(self._on_loop_changed)
        options_layout.addWidget(self.loop_checkbox)
        
        self.reverse_checkbox = QCheckBox("Reverse Direction")
        self.reverse_checkbox.toggled.connect(self._on_reverse_changed)
        options_layout.addWidget(self.reverse_checkbox)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Control Buttons
        controls_layout = QHBoxLayout()
        
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self._toggle_animation_dialog)
        controls_layout.addWidget(self.play_button)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self._stop_animation)
        controls_layout.addWidget(self.stop_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self._reset_animation)
        controls_layout.addWidget(self.reset_button)
        
        layout.addLayout(controls_layout)
        
        # Step controls
        step_layout = QHBoxLayout()
        
        self.prev_button = QPushButton("Prev")
        self.prev_button.clicked.connect(self._previous_frame)
        step_layout.addWidget(self.prev_button)
        
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self._next_frame)
        step_layout.addWidget(self.next_button)
        
        layout.addLayout(step_layout)
        
        # Info label
        self.info_label = QLabel("Ready to animate")
        layout.addWidget(self.info_label)
        
        self.animation_dialog.setLayout(layout)
    
    def _update_dialog_values(self):
        """Update dialog with current animation values"""
        visualization_manager = self.main_window.visualization_manager
        
        if hasattr(visualization_manager, 'neu_files') and visualization_manager.neu_files:
            max_frames = len(visualization_manager.neu_files)
            
            self.start_frame_spin.setMaximum(max_frames)
            self.end_frame_spin.setMaximum(max_frames)
            
            self.start_frame = 1
            self.end_frame = max_frames
            self.current_frame = visualization_manager.current_mesh_index + 1
            
            self.start_frame_spin.setValue(self.start_frame)
            self.end_frame_spin.setValue(self.end_frame)
            
            self.frame_slider.setMinimum(self.start_frame)
            self.frame_slider.setMaximum(self.end_frame)
            self.frame_slider.setValue(self.current_frame)
            
            self._update_frame_display()
            self._update_fps_display()
            
            self.info_label.setText(f"Ready to animate {max_frames} frames")
    
    def _on_start_frame_changed(self, value):
        """Handle start frame change"""
        self.start_frame = value
        if self.end_frame < value:
            self.end_frame_spin.setValue(value)
        self.frame_slider.setMinimum(value)
    
    def _on_end_frame_changed(self, value):
        """Handle end frame change"""
        self.end_frame = value
        if self.start_frame > value:
            self.start_frame_spin.setValue(value)
        self.frame_slider.setMaximum(value)
    
    def _on_slider_changed(self, value):
        """Handle frame slider change"""
        if not self.is_animating:
            self.current_frame = value
            self._load_frame(value - 1)  # Convert to 0-based index
            self._update_frame_display()
    
    def _on_delay_changed(self, value):
        """Handle delay change"""
        self.frame_delay = value
        self._update_fps_display()
        if self.is_animating:
            self.animation_timer.setInterval(value)
    
    def _on_loop_changed(self, checked):
        """Handle loop option change"""
        self.loop_animation = checked
    
    def _on_reverse_changed(self, checked):
        """Handle reverse option change"""
        self.reverse_direction = checked
        if checked:
            self.animation_direction = -1
        else:
            self.animation_direction = 1
    
    def _update_frame_display(self):
        """Update frame display"""
        self.current_frame_label.setText(f"Frame: {self.current_frame}")
        self.frame_slider.setValue(self.current_frame)
    
    def _update_fps_display(self):
        """Update FPS display"""
        fps = 1000.0 / self.frame_delay
        self.fps_label.setText(f"FPS: {fps:.1f}")
    
    def _toggle_animation_dialog(self):
        """Toggle animation play/pause from dialog"""
        if self.is_animating:
            self._pause_animation()
        else:
            self._start_animation()
    
    def _start_animation(self):
        """Start animation"""
        self.is_animating = True
        if hasattr(self, 'play_button'):
            self.play_button.setText("Pause")
        self.animation_timer.setInterval(self.frame_delay)
        self.animation_timer.start()
        if hasattr(self, 'info_label'):
            self.info_label.setText("Animation playing...")
        print(f"Animation started: frames {self.start_frame}-{self.end_frame}, delay={self.frame_delay}ms")
    
    def _pause_animation(self):
        """Pause animation"""
        self.is_animating = False
        if hasattr(self, 'play_button'):
            self.play_button.setText("Play")
        self.animation_timer.stop()
        if hasattr(self, 'info_label'):
            self.info_label.setText("Animation paused")
        print("Animation paused")
    
    def _stop_animation(self):
        """Stop animation"""
        self.is_animating = False
        if hasattr(self, 'play_button'):
            self.play_button.setText("Play")
        self.animation_timer.stop()
        if hasattr(self, 'info_label'):
            self.info_label.setText("Animation stopped")
        print("Animation stopped")
    
    def _reset_animation(self):
        """Reset animation to start"""
        self._stop_animation()
        
        # Initialize values if needed
        if not hasattr(self, 'start_frame') or not hasattr(self, 'end_frame'):
            visualization_manager = self.main_window.visualization_manager
            if hasattr(visualization_manager, 'neu_files') and visualization_manager.neu_files:
                max_frames = len(visualization_manager.neu_files)
                self.start_frame = 1
                self.end_frame = max_frames
            else:
                return
        
        if self.reverse_direction:
            self.current_frame = self.end_frame
        else:
            self.current_frame = self.start_frame
            
        self._load_frame(self.current_frame - 1)
        self._update_frame_display()
        if hasattr(self, 'info_label'):
            self.info_label.setText("Animation reset")
        print("Animation reset")
    
    def _next_frame(self):
        """Go to next frame manually"""
        if not hasattr(self, 'end_frame'):
            self._initialize_frame_values()
        
        if self.current_frame < self.end_frame:
            self.current_frame += 1
            self._load_frame(self.current_frame - 1)
            self._update_frame_display()
    
    def _previous_frame(self):
        """Go to previous frame manually"""
        if not hasattr(self, 'start_frame'):
            self._initialize_frame_values()
            
        if self.current_frame > self.start_frame:
            self.current_frame -= 1
            self._load_frame(self.current_frame - 1)
            self._update_frame_display()
    
    def _go_to_first_frame(self):
        """Go to first frame"""
        if not hasattr(self, 'start_frame'):
            self._initialize_frame_values()
            
        self.current_frame = self.start_frame
        self._load_frame(self.current_frame - 1)
        self._update_frame_display()
        print("Moved to first frame")
    
    def _go_to_last_frame(self):
        """Go to last frame"""
        if not hasattr(self, 'end_frame'):
            self._initialize_frame_values()
            
        self.current_frame = self.end_frame
        self._load_frame(self.current_frame - 1)
        self._update_frame_display()
        print("Moved to last frame")
    
    def _initialize_frame_values(self):
        """Initialize frame values if not set"""
        visualization_manager = self.main_window.visualization_manager
        if hasattr(visualization_manager, 'neu_files') and visualization_manager.neu_files:
            max_frames = len(visualization_manager.neu_files)
            self.start_frame = 1
            self.end_frame = max_frames
            self.current_frame = visualization_manager.current_mesh_index + 1 if hasattr(visualization_manager, 'current_mesh_index') else 1
        else:
            self.start_frame = 1
            self.end_frame = 1
            self.current_frame = 1
    
    def _toggle_animation(self):
        """Toggle animation play/pause - accessible from menu"""
        if not self._check_animation_available():
            return
        
        if self.is_animating:
            self._pause_animation()
        else:
            # Initialize if needed
            self._initialize_frame_values()
            self._start_animation()
    
    def _next_animation_frame(self):
        """Next frame in animation sequence"""
        self.current_frame += self.animation_direction
        
        # Handle boundaries
        if self.current_frame > self.end_frame:
            if self.loop_animation:
                self.current_frame = self.start_frame
            else:
                self._stop_animation()
                return
        elif self.current_frame < self.start_frame:
            if self.loop_animation:
                self.current_frame = self.end_frame
            else:
                self._stop_animation()
                return
        
        self._load_frame(self.current_frame - 1)
        self._update_frame_display()
    
    def _load_frame(self, frame_index):
        """Load specific frame"""
        visualization_manager = self.main_window.visualization_manager
        
        if hasattr(visualization_manager, 'neu_files') and visualization_manager.neu_files:
            if 0 <= frame_index < len(visualization_manager.neu_files):
                # Check if we have preloaded data
                preloaded_data = visualization_manager.get_preloaded_data(frame_index)
                
                if preloaded_data:
                    # Instant loading from preloaded data
                    visualization_manager.current_mesh_index = frame_index
                    visualization_manager.load_neutral_file(preloaded_data)
                else:
                    # Fallback to normal loading
                    visualization_manager.current_mesh_index = frame_index
                    visualization_manager._load_current_mesh()
                
                # Update controls
                if hasattr(visualization_manager, 'mesh_spinbox'):
                    visualization_manager.mesh_spinbox.blockSignals(True)
                    visualization_manager.mesh_spinbox.setValue(frame_index + 1)
                    visualization_manager.mesh_spinbox.blockSignals(False)
                    visualization_manager._update_mesh_controls_state()
   
    # Public interface methods for menu integration
    def animation_controls(self):
        """Show animation controls (called from menu)"""
        self.show_animation_dialog()
    
    def quick_play(self):
        """Quick play animation with default settings"""
        if not self._check_animation_available():
            return
            
        # Set default values
        visualization_manager = self.main_window.visualization_manager
        max_frames = len(visualization_manager.neu_files)
        
        self.start_frame = 1
        self.end_frame = max_frames
        self.current_frame = 1
        self.frame_delay = 500
        self.loop_animation = True
        self.reverse_direction = False
        self.animation_direction = 1
        
        # Load first frame
        self._load_frame(0)
        
        # Start animation
        self._start_animation()
        
        print(f"Quick animation started: {max_frames} frames, 500ms delay")
    
    def close_dialog(self):
        """Close animation dialog"""
        if self.animation_dialog:
            self._stop_animation()
            self.animation_dialog.close()