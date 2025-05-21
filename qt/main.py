import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QMessageBox, QMenuBar, QWidget
)
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application Accessible")
        self.setGeometry(100, 100, 400, 300)

        self.base_font_size = 10
        self.default_font = QFont("Arial", self.base_font_size)
        self.setFont(self.default_font)

        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()

        # Menu Fichier
        file_menu = menu_bar.addMenu("Fichier")
        action_open = QAction("Ouvrir", self)
        action_open.triggered.connect(self.open_dialog_box)
        file_menu.addAction(action_open)

        action_quit = QAction("Quitter", self)
        action_quit.triggered.connect(self.close)
        file_menu.addAction(action_quit)

        # Menu Affichage
        view_menu = menu_bar.addMenu("Affichage")

        action_zoom_in = QAction("Agrandir le texte (+)", self)
        action_zoom_in.triggered.connect(self.zoom_in)
        view_menu.addAction(action_zoom_in)

        action_zoom_out = QAction("Réduire le texte (-)", self)
        action_zoom_out.triggered.connect(self.zoom_out)
        view_menu.addAction(action_zoom_out)

        action_reset_zoom = QAction("Réinitialiser le zoom", self)
        action_reset_zoom.triggered.connect(self.reset_zoom)
        view_menu.addAction(action_reset_zoom)

        # À propos
        about_action = QAction("À propos", self)
        about_action.triggered.connect(lambda: QMessageBox.information(self, "À propos", "Ceci est une application accessible."))
        menu_bar.addAction(about_action)

    def open_dialog_box(self):
        QMessageBox.information(self, "Fenêtre", "Fenêtre")

    def zoom_in(self):
        self.base_font_size += 1
        self.update_font()

    def zoom_out(self):
        self.base_font_size = max(6, self.base_font_size - 1)
        self.update_font()

    def reset_zoom(self):
        self.base_font_size = 10
        self.update_font()

    def update_font(self):
        self.default_font.setPointSize(self.base_font_size)
        self.setFont(self.default_font)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
