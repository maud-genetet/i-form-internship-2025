"""
File Preloader Thread
Background thread for preloading .NEU files
"""

import os
import sys
from PyQt5.QtCore import QThread, pyqtSignal, QMutex

current_dir = os.path.dirname(os.path.abspath(__file__))
parser_dir = os.path.join(current_dir, 'parser')
if parser_dir not in sys.path:
    sys.path.append(parser_dir)
from ParserNeutralFile import ParserNeutralFile


class FilePreloader(QThread):
    """Background thread for preloading .NEU files"""
    
    file_loaded = pyqtSignal(int, str)  # index, filename
    all_files_loaded = pyqtSignal()
    progress_updated = pyqtSignal(int, str)  # progress percentage, status message
    error_occurred = pyqtSignal(str)  # error message
    
    def __init__(self, neu_files, working_directory, start_index=1):
        super().__init__()
        self.neu_files = neu_files
        self.working_directory = working_directory
        self.start_index = start_index
        self.preloaded_data = {}
        self.mutex = QMutex()
        self.should_stop = False
        
    def run(self):
        """Run the preloading process"""
        total_files = len(self.neu_files) - self.start_index
        loaded_count = 0
        
        try:
            for i in range(self.start_index, len(self.neu_files)):
                if self.should_stop:
                    break
                    
                filename = self.neu_files[i]
                file_path = os.path.join(self.working_directory, filename)
                
                self.progress_updated.emit(
                    int((loaded_count / total_files) * 100),
                    f"Loading {filename}..."
                )
                
                try:
                    neutral_data = ParserNeutralFile.parser_file(file_path)
                    if neutral_data:
                        self.mutex.lock()
                        self.preloaded_data[i] = neutral_data
                        self.mutex.unlock()
                        
                        self.file_loaded.emit(i, filename)
                        loaded_count += 1
                        print(f"Preloaded {i+1}/{len(self.neu_files)}: {filename}")
                        
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                
                self.progress_updated.emit(
                    int((loaded_count / total_files) * 100),
                    f"Loaded {loaded_count}/{total_files} files"
                )
            
            if not self.should_stop:
                self.progress_updated.emit(100, f"All {loaded_count} files loaded!")
                self.all_files_loaded.emit()
                print(f"Preloading complete: {loaded_count} files loaded")
                
        except Exception as e:
            self.error_occurred.emit(f"Preloading error: {str(e)}")
    
    def stop(self):
        """Stop the preloading process"""
        self.should_stop = True
    
    def get_preloaded_data(self, index):
        """Get preloaded data for a specific index (thread-safe)"""
        self.mutex.lock()
        data = self.preloaded_data.get(index)
        self.mutex.unlock()
        return data