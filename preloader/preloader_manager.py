"""
Preloader Manager
Manages the file preloading system with UI progress
"""

from .file_preloader import FilePreloader
import logging
logger = logging.getLogger(__name__)


class PreloaderManager:
    """Manages the file preloading system"""

    def __init__(self, visualization_manager):
        self.visualization_manager = visualization_manager
        self.preloader_thread = None
        self.preloaded_files = {}
        self.setup_progress_ui()

    def setup_progress_ui(self):
        """Setup progress bar"""
        self.progress_bar = self.visualization_manager.progress_bar
        self.progress_label = self.visualization_manager.progress_label

    def start_preloading(self, neu_files, working_directory, first_file_loaded_index=0):
        """Begin background preloading of mesh files"""
        if self.preloader_thread and self.preloader_thread.isRunning():
            return

        logger.info(f"Starting preload of {len(neu_files)} files")

        # Disable auto-scale during loading
        if hasattr(self.visualization_manager, 'toolbar_manager'):
            self.visualization_manager.toolbar_manager.disable_auto_scale_during_loading()

        # Show progress indicators
        if self.progress_bar:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
        if self.progress_label:
            self.progress_label.setVisible(True)
            self.progress_label.setText("Starting preload...")

        # Create and configure preloader thread
        self.preloader_thread = FilePreloader(
            neu_files, working_directory, start_index=first_file_loaded_index
        )

        self.preloader_thread.set_visualization_manager(
            self.visualization_manager)

        # Connect thread signals
        self.preloader_thread.file_loaded.connect(self._on_file_loaded)
        self.preloader_thread.all_files_loaded.connect(
            self._on_all_files_loaded)
        self.preloader_thread.progress_updated.connect(
            self._on_progress_updated)

        # Start background loading
        self.preloader_thread.start()

    def _on_file_loaded(self, index):
        """Called when a single file is loaded"""
        if self.preloader_thread:
            data = self.preloader_thread.get_preloaded_data(index)
            if data:
                self.preloaded_files[index] = data

    def _on_all_files_loaded(self):
        """Called when all files are loaded"""
        logger.info(
            f"All files preloaded! Total: {len(self.preloaded_files)} files")

        # Hide progress indicators
        if self.progress_bar:
            self.progress_bar.setVisible(False)
        if self.progress_label:
            self.progress_label.setVisible(False)

        # Transfer data to visualization manager
        self.visualization_manager.set_preloaded_data(self.preloaded_files)

        # Re-enable auto-scale
        if hasattr(self.visualization_manager, 'toolbar_manager'):
            self.visualization_manager.toolbar_manager.enable_auto_scale_after_loading()

    def _on_progress_updated(self, percentage, message):
        """Called when progress is updated"""
        if self.progress_bar:
            self.progress_bar.setValue(percentage)
        if self.progress_label:
            self.progress_label.setText(message)

    def get_preloaded_data(self, index):
        """Get preloaded mesh data by file index"""
        return self.preloaded_files.get(index)

    def stop_preloading(self):
        """Stop preloading process"""
        if self.preloader_thread and self.preloader_thread.isRunning():
            self.preloader_thread.stop()
            self.preloader_thread.wait(3000)  # Wait max 3 seconds

        # Re-enable auto-scale
        if hasattr(self.visualization_manager, 'toolbar_manager'):
            self.visualization_manager.toolbar_manager.enable_auto_scale_after_loading()

        # Hide progress indicators
        if self.progress_bar:
            self.progress_bar.setVisible(False)
        if self.progress_label:
            self.progress_label.setVisible(False)
