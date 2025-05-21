import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application")
        self.setGeometry(100, 100, 400, 300)
        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()
        menu_item = menu_bar.addMenu("Fichier")
        menu_bar.addAction("Quitter", self.close)
        menu_bar.addAction("About", lambda: QMessageBox.information(self, "About", "This is a simple application."))

        action_open = QAction("Ouvrir", self)
        action_open.triggered.connect(self.open_dialog_box)

        menu_item.addAction(action_open)

    def open_dialog_box(self):
        QMessageBox.information(self, "Windows", "Windows")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
