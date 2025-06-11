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
            'Strain rate x(r)': [],
            'Strain rate y(z)': [],
            'Strain rate z(theta)': [],
            'Strain rate xy(rz)': [],
            'Effective strain rate': [],
            'Strain x(r)': [],
            'Strain y(z)': [],
            'Strain z(theta)': [],
            'Strain xy(rz)': [],
            'Effective strain': [],
            'Strain 1': [],
            'Strain 3': [],
            'Stress x(r)': [],
            'Stress y(z)': [],
            'Stress z(theta)': [],
            'Stress xy(rz)': [],
            'Effective stress': [],
            'Average stress': []
        }
        
        for element in elements:
            element_data['Element_ID'].append(element.get_id())
            element_data['Strain rate x(r)'].append(element.get_strain_rate_Exx() or 0.0)
            element_data['Strain rate y(z)'].append(element.get_strain_rate_Eyy() or 0.0)
            element_data['Strain rate z(theta)'].append(element.get_strain_rate_Ezz() or 0.0)
            element_data['Strain rate xy(rz)'].append(element.get_strain_rate_Exy() or 0.0)
            element_data['Effective strain rate'].append(element.get_strain_rate_E() or 0.0)
            element_data['Strain x(r)'].append(element.get_strain_Exx() or 0.0)
            element_data['Strain y(z)'].append(element.get_strain_Eyy() or 0.0)
            element_data['Strain z(theta)'].append(element.get_strain_Ezz() or 0.0)
            element_data['Strain xy(rz)'].append(element.get_strain_Exy() or 0.0)
            element_data['Effective strain'].append(element.get_strain_E() or 0.0)
            element_data['Strain 1'].append(element.get_strain_E1() or 0.0)
            element_data['Strain 3'].append(element.get_strain_E3() or 0.0)
            element_data['Stress x(r)'].append(element.get_stress_Oxx() or 0.0)
            element_data['Stress y(z)'].append(element.get_stress_Oyy() or 0.0)
            element_data['Stress z(theta)'].append(element.get_stress_Ozz() or 0.0)
            element_data['Stress xy(rz)'].append(element.get_stress_Oxy() or 0.0)
            element_data['Effective stress'].append(element.get_stress_O() or 0.0)
            element_data['Average stress'].append(element.get_stress_Orr() or 0.0)
                    
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
            
            if len(die_points) >= 3:
                cells = [len(die_points)] + list(range(len(die_points)))
                return pv.UnstructuredGrid(
                    cells,
                    [pv.CellType.POLYGON],
                    die_points
                )
        
        return None
    