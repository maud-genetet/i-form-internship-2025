# -*- coding: utf-8 -*-
"""
Module de construction des mesh PyVista
"""

import numpy as np
import pyvista as pv


class MeshBuilder:
    """
    Responsable de la création des mesh PyVista à partir des données neutral
    """
    
    def create_pyvista_mesh(self, neutral_data):
        """
        Crée un mesh PyVista à partir des données neutral
        """
        if not neutral_data:
            return None
        
        nodes = neutral_data.get_nodes()
        elements = neutral_data.get_elements()
        
        if not nodes or not elements:
            return None
        
        # Construction des points
        points, node_id_to_index = self._build_points(nodes)
        
        # Construction des cellules
        cells = self._build_cells(elements, node_id_to_index)
        
        if not cells:
            return None
        
        # Création du mesh
        cell_types = [5] * (len(cells) // 5)  # Triangle par défaut
        mesh = pv.UnstructuredGrid(cells, np.array(cell_types), points)
        
        # Ajout des données scalaires
        self._add_scalar_data(mesh, elements)
        
        return mesh
    
    def _build_points(self, nodes):
        """Construit le tableau des points et la table de correspondance"""
        points = []
        node_id_to_index = {}
        
        for i, node in enumerate(nodes):
            x = node.get_coordX() if node.get_coordX() is not None else 0.0
            y = node.get_coordY() if node.get_coordY() is not None else 0.0
            points.append([x, y, 0.0])
            node_id_to_index[node.get_id()] = i
        
        return np.array(points), node_id_to_index
    
    def _build_cells(self, elements, node_id_to_index):
        """Construit le tableau des cellules"""
        cells = []
        
        for element in elements:
            element_nodes = element.get_lnods()
            if len(element_nodes) >= 3:
                node_indices = []
                for node in element_nodes:
                    if node and node.get_id() in node_id_to_index:
                        node_indices.append(node_id_to_index[node.get_id()])
                
                if len(node_indices) >= 3:
                    if len(node_indices) == 3:
                        cells.extend([3] + node_indices)
                    elif len(node_indices) == 4:
                        cells.extend([4] + node_indices)
                    else:
                        cells.extend([len(node_indices)] + node_indices)
        
        return cells
    
    def _add_scalar_data(self, mesh, elements):
        """Ajoute toutes les données scalaires disponibles au mesh"""
        element_data = {
            'Element_ID': [],
            'Contrainte': [],
            'Deformation': [],
            'Contrainte_XX': [],
            'Contrainte_YY': [],
            'Deformation_XX': [],
            'Deformation_YY': []
        }
        
        for element in elements:
            element_data['Element_ID'].append(element.get_id())
            element_data['Contrainte'].append(element.get_stress_O() or 0.0)
            element_data['Deformation'].append(element.get_strain_E() or 0.0)
            element_data['Contrainte_XX'].append(element.get_stress_Oxx() or 0.0)
            element_data['Contrainte_YY'].append(element.get_stress_Oyy() or 0.0)
            element_data['Deformation_XX'].append(element.get_strain_Exx() or 0.0)
            element_data['Deformation_YY'].append(element.get_strain_Eyy() or 0.0)
        
        # Ajout au mesh
        for key, values in element_data.items():
            if any(v != 0.0 for v in values):
                mesh.cell_data[key] = np.array(values)
    
    def create_die_mesh(self, die):
        """Crée un mesh pour un die"""
        die_nodes = die.get_nodes()
        
        if not die_nodes or len(die_nodes) < 3:
            return None
        
        die_points = []
        for node in die_nodes:
            x = node.get_coordX() if node.get_coordX() is not None else 0.0
            y = node.get_coordY() if node.get_coordY() is not None else 0.0
            die_points.append([x, y, 0.0])
        
        if len(die_points) >= 3:
            die_points = np.array(die_points)
            hull_points = self._create_convex_hull_2d(die_points)
            
            if len(hull_points) >= 3:
                cells = [len(hull_points)] + list(range(len(hull_points)))
                return pv.UnstructuredGrid(
                    cells,
                    [pv.CellType.POLYGON],
                    hull_points
                )
        
        return None
    
    def _create_convex_hull_2d(self, points):
        """Crée une enveloppe convexe 2D"""
        try:
            from scipy.spatial import ConvexHull
            points_2d = points[:, :2]
            hull = ConvexHull(points_2d)
            hull_points_2d = points_2d[hull.vertices]
            return np.column_stack([hull_points_2d, np.zeros(len(hull_points_2d))])
        except ImportError:
            # Fallback simple
            centroid = np.mean(points, axis=0)
            angles = [np.arctan2(p[1] - centroid[1], p[0] - centroid[0]) for p in points]
            sorted_indices = np.argsort(angles)
            return points[sorted_indices]
        except Exception:
            return points