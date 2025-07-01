"""
Preloader Manager
Manages the file preloading system with UI progress
"""

from PyQt5.QtWidgets import QProgressBar, QLabel
from .file_preloader import FilePreloader


class PreloaderManager:
    """Manages the file preloading system"""
    
    def __init__(self, visualization_manager):
        self.visualization_manager = visualization_manager
        self.preloader_thread = None
        self.progress_bar = None
        self.progress_label = None
        self.preloaded_files = {}
        self.setup_progress_ui()
    
    def setup_progress_ui(self):
        """Setup progress bar in the toolbar"""
        try:
            main_layout = self.visualization_manager.visualization_widget.layout()
            if main_layout.count() > 0:
                toolbar_widget = main_layout.itemAt(0).widget()
                toolbar_layout = toolbar_widget.layout()
                
                self.progress_label = QLabel("Ready")
                self.progress_label.setMinimumWidth(150)
                self.progress_label.setVisible(False)
                toolbar_layout.addWidget(self.progress_label)
                
                self.progress_bar = QProgressBar()
                self.progress_bar.setMinimumWidth(200)
                self.progress_bar.setMaximumHeight(20)
                self.progress_bar.setVisible(False)
                toolbar_layout.addWidget(self.progress_bar)
                
        except Exception as e:
            print(f"Could not setup progress UI: {e}")
    
    def start_preloading(self, neu_files, working_directory, first_file_loaded_index=0):
        """Start preloading files in background"""
        if self.preloader_thread and self.preloader_thread.isRunning():
            return
        
        print(f"Starting preload of {len(neu_files)} files")
        
        if self.progress_bar:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
        if self.progress_label:
            self.progress_label.setVisible(True)
            self.progress_label.setText("Starting preload...")
        
        self.preloader_thread = FilePreloader(
            neu_files, working_directory, start_index=first_file_loaded_index
        )
        
        self.preloader_thread.file_loaded.connect(self._on_file_loaded)
        self.preloader_thread.all_files_loaded.connect(self._on_all_files_loaded)
        self.preloader_thread.progress_updated.connect(self._on_progress_updated)
        
        self.preloader_thread.start()
    
    def _on_file_loaded(self, index, filename):
        """Called when a single file is loaded"""
        if self.preloader_thread:
            data = self.preloader_thread.get_preloaded_data(index)
            if data:
                self.preloaded_files[index] = data
    
    def _on_all_files_loaded(self):
        """Called when all files are loaded"""
        print(f"All files preloaded! Total: {len(self.preloaded_files)} files")
        
        if self.progress_bar:
            self.progress_bar.setVisible(False)
        if self.progress_label:
            self.progress_label.setVisible(False)
        
        self.visualization_manager.set_preloaded_data(self.preloaded_files)
    
    def _on_progress_updated(self, percentage, message):
        """Called when progress is updated"""
        if self.progress_bar:
            self.progress_bar.setValue(percentage)
        if self.progress_label:
            self.progress_label.setText(message)
    
    def get_preloaded_data(self, index):
        """Get preloaded data for specific index"""
        return self.preloaded_files.get(index)
    
    def stop_preloading(self):
        """Stop preloading process"""
        if self.preloader_thread and self.preloader_thread.isRunning():
            self.preloader_thread.stop()
            self.preloader_thread.wait(3000)
            
        if self.progress_bar:
            self.progress_bar.setVisible(False)
        if self.progress_label:
            self.progress_label.setVisible(False)