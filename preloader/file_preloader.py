"""
File Preloader Thread
Background thread for preloading .NEU files
"""

from parser import ParserNeutralFile
import os
from PyQt5.QtCore import QThread, pyqtSignal, QMutex
import logging
logger = logging.getLogger(__name__)


class FilePreloader(QThread):
    """Background thread for preloading .NEU files"""

    # Signal emitted when individual file is loaded (index, filename)
    file_loaded = pyqtSignal(int, str)
    # Signal emitted when all files are loaded
    all_files_loaded = pyqtSignal()
    # Signal emitted for progress updates (percentage, message)
    progress_updated = pyqtSignal(int, str)
    # Signal emitted on errors (error message)
    error_occurred = pyqtSignal(str)

    def __init__(self, neu_files, working_directory, start_index=1):
        super().__init__()
        self.neu_files = neu_files
        self.working_directory = working_directory
        self.start_index = start_index
        self.preloaded_data = {}
        self.mutex = QMutex()
        self.should_stop = False

    def run(self):
        """Main preloading loop executed in background thread"""
        total_files = len(self.neu_files)
        loaded_count = 0

        try:
            for i in range(0, len(self.neu_files)):
                if self.should_stop:
                    break

                # Yield to graphics loading if needed
                while hasattr(self, '_visualization_manager') and getattr(self._visualization_manager, 'graphics_loading', False):
                    if self.should_stop:
                        break
                    self.msleep(1000)  # Wait 1 second

                if self.should_stop:
                    break

                filename = self.neu_files[i]
                file_path = os.path.join(self.working_directory, filename)

                # Update progress before loading
                self.progress_updated.emit(
                    int((loaded_count / total_files) * 100),
                    f"Loading {filename}..."
                )

                try:
                    # Parse the mesh file
                    neutral_data = ParserNeutralFile.parser_file(file_path)
                    if neutral_data:
                        # Thread-safe storage
                        self.mutex.lock()
                        self.preloaded_data[i] = neutral_data
                        self.mutex.unlock()

                        self.file_loaded.emit(i, filename)
                        loaded_count += 1
                        logger.info(
                            f"Preloaded {i+1}/{len(self.neu_files)}: {filename}")

                except Exception as e:
                    logger.exception(f"Error loading {filename}: {e}")

                # Update progress after loading
                self.progress_updated.emit(
                    int((loaded_count / total_files) * 100),
                    f"Loaded {loaded_count}/{total_files} files"
                )

            # Completion handling
            if not self.should_stop:
                self.progress_updated.emit(
                    100, f"All {loaded_count} files loaded!")
                self.all_files_loaded.emit()
                logger.info(
                    f"Preloading complete: {loaded_count} files loaded")

        except Exception as e:
            self.error_occurred.emit(f"Preloading error: {str(e)}")

    def stop(self):
        """Request thread to stop preloading"""
        self.should_stop = True

    def get_preloaded_data(self, index):
        """Get preloaded mesh data by index (thread-safe)"""
        self.mutex.lock()
        data = self.preloaded_data.get(index)
        self.mutex.unlock()
        return data

    def set_visualization_manager(self, visualization_manager):
        """Set reference to check for graphics loading priority"""
        self._visualization_manager = visualization_manager
