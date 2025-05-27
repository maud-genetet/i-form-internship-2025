import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QVBoxLayout,
    QWidget, QAction, QMessageBox
)
from PyQt5.QtGui import QFont
from pyvistaqt import QtInteractor
import pyvista as pv
from pyvista import examples
import numpy as np

# Import pour la lecture des fichiers
try:
    import meshio
    MESHIO_AVAILABLE = True
except ImportError:
    MESHIO_AVAILABLE = False

try:
    from ansys.mapdl import reader as pymapdl_reader
    PYANSYS_AVAILABLE = True
except ImportError:
    PYANSYS_AVAILABLE = False

from DeformedMeshDialog import DeformedMeshDialog

class MainWindow(QMainWindow):

    menu_bar = None

    def __init__(self):
        super().__init__()

        self.setWindowTitle("I Form")
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(screen_geometry)

        # Dynamic font for accessibility
        self.base_font_size = 10
        self.current_font_size = self.base_font_size
        self.default_font = QFont("Roboto", self.current_font_size)
        self.setFont(self.default_font)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Vertical layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # PyVista render area
        self.plotter = QtInteractor(self)
        self.layout.addWidget(self.plotter.interactor)
        self.plotter.show_axes() 
        mesh = examples.download_notch_stress()
        self.plotter.add_mesh(mesh, show_edges=True)

        self.create_menu()

    def create_menu(self):
        self.menu_bar = self.menuBar()

        self.summary_menu()
        self.query_menu()
        self.mesh_menu()
        self.field_menu()
        self.view_menu()
        self.quit_menu()

    def summary_menu(self):
        summary_menu = self.menu_bar.addMenu("Summary")

        # Standard options
        standard_options = QAction("Standard Options", self)
        summary_menu.addAction(standard_options)
        standard_options.setEnabled(False)

        # Workpiece
        workpiece = QAction("Workpiece", self)
        summary_menu.addAction(workpiece)

        # Die
        die = QAction("Die", self)
        summary_menu.addAction(die)

    def query_menu(self):
        query_menu = self.menu_bar.addMenu("Query")

    def mesh_menu(self):
        mesh_menu = self.menu_bar.addMenu("Mesh")

        # Standard options
        standard_options = QAction("Standard Options", self)
        mesh_menu.addAction(standard_options)
        standard_options.setEnabled(False)

        # Initial mesh
        initial_mesh = QAction("Initial Mesh", self)
        initial_mesh.triggered.connect(self.load_file)
        mesh_menu.addAction(initial_mesh)

        # Deformed mesh
        deformed_mesh = QAction("Deformed Mesh", self)
        deformed_mesh.triggered.connect(self.open_deformed_mesh_dialog)
        mesh_menu.addAction(deformed_mesh)

    def open_deformed_mesh_dialog(self):
        dialog = DeformedMeshDialog(self)
        dialog.exec_()

    def view_menu(self):
        # View menu (for font zoom)
        view_menu = self.menu_bar.addMenu("View")

        action_zoom_in = QAction("Zoom Text (+)", self)
        action_zoom_in.triggered.connect(self.zoom_in)
        view_menu.addAction(action_zoom_in)

        action_zoom_out = QAction("Zoom Text (-)", self)
        action_zoom_out.triggered.connect(self.zoom_out)
        view_menu.addAction(action_zoom_out)

        action_reset_zoom = QAction("Reset Text Zoom", self)
        action_reset_zoom.triggered.connect(self.reset_zoom)
        view_menu.addAction(action_reset_zoom)

    def field_menu(self):
        field_menu = self.menu_bar.addMenu("Field")

    def quit_menu(self):
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        self.menu_bar.addAction(quit_action)

    def load_file(self):
        # File dialog to choose only .neu or .rst files
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "ANSYS Files (*.neu *.rst)"
        )

        if file_path:
            self.visualize_mesh(file_path)

    def read_neu_file(self, file_path):
        """
        Lecture d'un fichier .neu avec parser manuel prioritaire
        """
        # Méthode 1: Essayer d'abord le parser manuel (plus fiable pour les .neu ANSYS)
        try:
            return self.read_neu_file_manual(file_path)
        except Exception as manual_error:
            print(f"Parser manuel échoué: {manual_error}")
    

    def read_neu_file_manual(self, file_path):
        """
        Parser manuel amélioré pour fichiers .neu (format ANSYS Neutral)
        """
        try:
            points = []
            cells = []
            point_ids = {}  # Mapping ID -> index
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Diviser en lignes et nettoyer
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            print(f"Lecture du fichier {file_path} - {len(lines)} lignes")
            
            # Analyser les premières lignes pour diagnostiquer le format
            for i, line in enumerate(lines[:10]):
                print(f"Ligne {i+1}: {line[:100]}")
            
            # Détecter le format du fichier (nombre de nœuds en première ligne)
            first_line = lines[0].strip()
            num_nodes = None
            try:
                num_nodes = int(first_line)
                print(f"Format détecté: {num_nodes} nœuds annoncés")
            except ValueError:
                print("Format non standard - pas de nombre de nœuds en première ligne")
            
            i = 0
            if num_nodes is not None:
                i = 1  # Commencer après le nombre de nœuds
            
            # Phase 1: Lire les nœuds
            nodes_read = 0
            print(f"Début lecture des nœuds à la ligne {i+1}")
            
            while i < len(lines) and (num_nodes is None or nodes_read < num_nodes):
                line = lines[i].strip()
                
                # Vérifier si on arrive aux éléments
                if (line.isdigit() and num_nodes is not None and nodes_read == num_nodes):
                    # Probablement le nombre d'éléments
                    break
                
                # Essayer de parser comme un nœud
                if line and line[0].isdigit():
                    old_count = len(points)
                    self.parse_node_line(line, points, point_ids)
                    if len(points) > old_count:
                        nodes_read += 1
                
                i += 1
            
            print(f"Nœuds lus: {len(points)}")
            
            # Phase 2: Lire les éléments
            if i < len(lines):
                # Vérifier si la ligne actuelle est le nombre d'éléments
                try:
                    num_elements = int(lines[i])
                    print(f"Nombre d'éléments annoncé: {num_elements}")
                    i += 1
                except ValueError:
                    print("Pas de nombre d'éléments explicite")
            
            print(f"Début lecture des éléments à la ligne {i+1}")
            elements_read = 0
            
            while i < len(lines):
                line = lines[i].strip()
                
                # Arrêter si on trouve des données qui ne sont pas des éléments
                if not line or not line[0].isdigit():
                    break
                
                # Essayer de parser comme un élément
                old_count = len(cells)
                self.parse_element_line(line, cells, point_ids)
                if len(cells) > old_count:
                    elements_read += 1
                
                i += 1
            
            print(f"Éléments lus: {len(cells)}")
            print(f"Nœuds trouvés: {len(points)}, Éléments trouvés: {len(cells)}")
            
            if not points:
                raise ValueError("Aucun nœud trouvé dans le fichier")
            
            # Créer le mesh PyVista
            points = np.array(points)
            
            if cells:
                # Convertir les cellules
                pv_cells = []
                cell_types = []
                
                for cell in cells:
                    if len(cell) == 3:  # Triangle
                        pv_cells.extend([3] + cell)
                        cell_types.append(pv.CellType.TRIANGLE)
                    elif len(cell) == 4:  # Tétraèdre ou Quad
                        pv_cells.extend([4] + cell)
                        cell_types.append(pv.CellType.TETRA)
                    elif len(cell) == 8:  # Hexaèdre
                        pv_cells.extend([8] + cell)
                        cell_types.append(pv.CellType.HEXAHEDRON)
                    elif len(cell) == 6:  # Prisme
                        pv_cells.extend([6] + cell)
                        cell_types.append(pv.CellType.WEDGE)
                    elif len(cell) == 5:  # Pyramide
                        pv_cells.extend([5] + cell)
                        cell_types.append(pv.CellType.PYRAMID)
                
                if pv_cells:
                    mesh = pv.UnstructuredGrid(pv_cells, cell_types, points)
                else:
                    mesh = pv.PolyData(points)
            else:
                # Créer un nuage de points
                mesh = pv.PolyData(points)
            
            return mesh
            
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture manuelle du fichier .neu: {str(e)}")

    def parse_node_line(self, line, points, point_ids):
        """Parse une ligne de nœud avec support notation scientifique Fortran"""
        try:
            # Remplacer la notation Fortran D par E pour Python
            line = line.replace('D+', 'E+').replace('D-', 'E-')
            
            # Différents formats possibles
            if line.startswith('N,'):
                # Format: N,ID,X,Y,Z
                parts = line.split(',')
                if len(parts) >= 5:
                    node_id = int(parts[1])
                    x, y, z = float(parts[2]), float(parts[3]), float(parts[4])
                    point_ids[node_id] = len(points)
                    points.append([x, y, z])
            elif ',' in line:
                # Format avec virgules: ID,X,Y,Z
                parts = line.split(',')
                if len(parts) >= 4:
                    node_id = int(parts[0])
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    point_ids[node_id] = len(points)
                    points.append([x, y, z])
            else:
                # Format avec espaces: ID X Y Z (format du fichier exemple)
                parts = line.split()
                if len(parts) >= 7:  # Format complet avec données supplémentaires
                    node_id = int(parts[0])
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    point_ids[node_id] = len(points)
                    points.append([x, y, z])
                elif len(parts) >= 4:  # Format minimal
                    node_id = int(parts[0])
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    point_ids[node_id] = len(points)
                    points.append([x, y, z])
        except (ValueError, IndexError) as e:
            print(f"Erreur parsing nœud: {line[:50]}... - {e}")

    def parse_element_line(self, line, cells, point_ids):
        """Parse une ligne d'élément"""
        try:
            if line.startswith('E,'):
                # Format: E,ID,TYPE,REAL,SECNUM,ESYS,N1,N2,N3,...
                parts = line.split(',')
                nodes = []
                for j in range(6, len(parts)):  # Commencer après les métadonnées
                    if parts[j].strip() and parts[j].strip().isdigit():
                        node_id = int(parts[j])
                        if node_id in point_ids:
                            nodes.append(point_ids[node_id])
                
                if len(nodes) >= 3:
                    cells.append(nodes)
            else:
                # Format du fichier exemple: ID TYPE N1 N2 N3 N4 (+ autres données)
                parts = line.split()
                if len(parts) >= 6:
                    try:
                        # Les premiers chiffres sont ID, TYPE, puis les nœuds
                        elem_id = int(parts[0])
                        elem_type = int(parts[1])
                        
                        nodes = []
                        # Essayer de parser les nœuds (généralement positions 2-5 ou 2-9)
                        for j in range(2, min(len(parts), 10)):
                            if parts[j].isdigit():
                                node_id = int(parts[j])
                                if node_id in point_ids:
                                    nodes.append(point_ids[node_id])
                                else:
                                    break  # Arrêter si on ne trouve plus de nœud valide
                        
                        if len(nodes) >= 3:
                            cells.append(nodes)
                    except (ValueError, IndexError):
                        pass
        except (ValueError, IndexError) as e:
            print(f"Erreur parsing élément: {line[:50]}... - {e}")

    def read_rst_file(self, file_path):
        """
        Lecture d'un fichier .rst avec pyansys
        """
        if not PYANSYS_AVAILABLE:
            raise ImportError("pyansys n'est pas installé. Utilisez: pip install ansys-mapdl-reader")
        
        try:
            # Lire le fichier .rst avec pyansys
            rst = pymapdl_reader.read_binary(file_path)
            
            # Obtenir le mesh
            mesh = rst.grid
            
            # Ajouter les résultats si disponibles
            try:
                # Essayer d'obtenir les déplacements
                nnum, disp = rst.nodal_solution(0)  # Premier pas de temps
                if disp is not None and len(disp) > 0:
                    # Ajouter les déplacements comme données nodales
                    if disp.shape[1] >= 3:
                        mesh.point_data['Displacement'] = disp[:, :3]
                        mesh.point_data['Displacement Magnitude'] = np.linalg.norm(disp[:, :3], axis=1)
            except Exception as e:
                print(f"Impossible de charger les déplacements: {e}")
            
            try:
                # Essayer d'obtenir les contraintes
                nnum, stress = rst.nodal_stress(0)  # Premier pas de temps
                if stress is not None and len(stress) > 0:
                    # Ajouter les contraintes comme données nodales
                    mesh.point_data['Stress'] = stress
                    # Calculer la contrainte de von Mises si possible
                    if stress.shape[1] >= 6:
                        # Contraintes principales: sx, sy, sz, sxy, syz, sxz
                        sx, sy, sz = stress[:, 0], stress[:, 1], stress[:, 2]
                        sxy, syz, sxz = stress[:, 3], stress[:, 4], stress[:, 5]
                        
                        # von Mises stress
                        von_mises = np.sqrt(0.5 * ((sx - sy)**2 + (sy - sz)**2 + (sz - sx)**2 + 
                                                  6 * (sxy**2 + syz**2 + sxz**2)))
                        mesh.point_data['von Mises Stress'] = von_mises
            except Exception as e:
                print(f"Impossible de charger les contraintes: {e}")
            
            return mesh
            
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du fichier .rst avec pyansys: {str(e)}")

    def visualize_mesh(self, file_path):
        """Visualiser le mesh selon le type de fichier"""
        try:
            # Clear previous mesh
            self.plotter.clear()
            
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.neu':
                mesh = self.read_neu_file(file_path)
            elif file_ext == '.rst':
                mesh = self.read_rst_file(file_path)
            else:
                raise ValueError(f"Format de fichier non supporté: {file_ext}")
            
            # Afficher le mesh
            self.plotter.add_mesh(mesh, show_edges=True, color='lightblue')
            
            # Si des données scalaires sont disponibles, les afficher
            scalar_data = None
            if mesh.point_data:
                # Prendre la première donnée scalaire disponible
                for name, data in mesh.point_data.items():
                    if len(data.shape) == 1:  # Données scalaires
                        scalar_data = name
                        break
                    elif len(data.shape) == 2 and 'Magnitude' in name:  # Magnitude de vecteur
                        scalar_data = name
                        break
            
            if scalar_data:
                # Afficher avec les données scalaires
                self.plotter.clear()
                self.plotter.add_mesh(mesh, show_edges=True, scalars=scalar_data, 
                                    show_scalar_bar=True, cmap='viridis')
                print(f"Affichage avec les données: {scalar_data}")
            
            self.plotter.reset_camera()
            self.plotter.render()
            
            # Afficher des informations sur le mesh
            info_msg = f"Mesh chargé avec succès:\n"
            info_msg += f"- Nombre de points: {mesh.n_points}\n"
            info_msg += f"- Nombre de cellules: {mesh.n_cells}\n"
            info_msg += f"- Type: {type(mesh).__name__}\n"
            
            # Lister les données disponibles
            if mesh.point_data:
                info_msg += f"- Données nodales: {list(mesh.point_data.keys())}\n"
            if mesh.cell_data:
                info_msg += f"- Données d'éléments: {list(mesh.cell_data.keys())}\n"
            
            QMessageBox.information(self, "Mesh chargé", info_msg)

        except Exception as e:
            error_msg = f"Erreur lors du chargement du fichier:\n{str(e)}"
            QMessageBox.critical(self, "Erreur", error_msg)

    # Font zoom in
    def zoom_in(self):
        self.current_font_size += 1
        self.update_font()

    # Font zoom out
    def zoom_out(self):
        if self.current_font_size > 1:
            self.current_font_size -= 1
            self.update_font()

    # Reset font size to default
    def reset_zoom(self):
        self.current_font_size = self.base_font_size
        self.update_font()

    # Apply font changes
    def update_font(self):
        new_font = QFont("Arial", self.current_font_size)
        self.setFont(new_font)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())