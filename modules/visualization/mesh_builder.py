"""
PyVista Mesh Construction Module
"""

import numpy as np
import pyvista as pv

class MeshBuilder:
    """Responsible for creating PyVista meshes from neutral data"""
    
    def create_pyvista_mesh(self, neutral_data):
        """Create PyVista mesh from neutral data"""
        if not neutral_data:
            return None
        
        nodes = neutral_data.get_nodes()
        elements = neutral_data.get_elements()
        
        if not nodes or not elements:
            return None
        
        # Build points
        points, node_id_to_index = self._build_points(nodes)
        
        # Build cells
        cells = self._build_cells(elements, node_id_to_index)
        
        if not cells:
            return None
        
        # Create mesh
        cell_types = [5] * (len(cells) // 5)  # Triangle by default
        mesh = pv.UnstructuredGrid(cells, np.array(cell_types), points)
        
        # Add scalar data
        self._add_scalar_data(mesh, elements, nodes)
        
        return mesh
    
    def _build_points(self, nodes):
        """Build points array and correspondence table"""
        points = []
        node_id_to_index = {}
        
        for i, node in enumerate(nodes):
            x = node.get_coordX() if node.get_coordX() is not None else 0.0
            y = node.get_coordY() if node.get_coordY() is not None else 0.0
            points.append([x, y, 0.0])
            node_id_to_index[node.get_id()] = i
        
        return np.array(points), node_id_to_index
    
    def _build_cells(self, elements, node_id_to_index):
        """Build cells array"""
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
    
    def _add_scalar_data(self, mesh, elements, nodes):
        """Add all available scalar data to mesh including new variables"""
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
            'Average stress': [],
            'Element Quality': [],
            'Relative Density': [],
            'Stress y(z)/Ef.Stress': [],
            'Stress xy(rz)/Ef.Stress': [],
            'Average Stress/Ef.Stress': [],
            'Pressure': [],
            'Pressure/Ef.Stress': [],
            'Velocity X(r)': [],
            'Velocity Y(z)': [],
            'Total Velocity': [],
            'Force X(r)': [],
            'Force Y(z)': [],
            'Total Force': [],
            'Temperature': [],
            'Temperature Rate': [],
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
            stress_xx = element.get_stress_Oxx() or 0.0
            stress_yy = element.get_stress_Oyy() or 0.0
            stress_zz = element.get_stress_Ozz() or 0.0
            stress_xy = element.get_stress_Oxy() or 0.0
            effective_stress = element.get_stress_O() or 0.0
            average_stress = element.get_stress_Orr() or 0.0
            element_data['Stress x(r)'].append(stress_xx)
            element_data['Stress y(z)'].append(stress_yy)
            element_data['Stress z(theta)'].append(stress_zz)
            element_data['Stress xy(rz)'].append(stress_xy)
            element_data['Effective stress'].append(effective_stress)
            element_data['Average stress'].append(average_stress)
            element_data['Element Quality'].append(element.get_rindx() or 0.0)
            element_data['Relative Density'].append(element.get_densy() or 0.0)
            pressure = -(stress_xx + stress_yy + stress_zz) / 3.0
            element_data['Pressure'].append(pressure)
            if effective_stress != 0.0:
                element_data['Stress y(z)/Ef.Stress'].append(stress_yy / effective_stress)
                element_data['Stress xy(rz)/Ef.Stress'].append(stress_xy / effective_stress)
                element_data['Average Stress/Ef.Stress'].append(average_stress / effective_stress)
                element_data['Pressure/Ef.Stress'].append(pressure / effective_stress)
            else:
                element_data['Stress y(z)/Ef.Stress'].append(0.0)
                element_data['Stress xy(rz)/Ef.Stress'].append(0.0)
                element_data['Average Stress/Ef.Stress'].append(0.0)
                element_data['Pressure/Ef.Stress'].append(0.0)
            element_nodes = element.get_lnods()

            if element_nodes:
                
                # For this part we do the average of the values of the nodes
                vx_sum = vy_sum = fx_sum = fy_sum = temp_sum = dtemp_sum = 0.0
                valid_nodes = 0
                
                for node in element_nodes:
                    if node:
                        vx = node.get_Vx() or 0.0
                        vy = node.get_Vy() or 0.0
                        fx = node.get_Fx() or 0.0
                        fy = node.get_Fy() or 0.0
                        temp = node.get_Temp() or 0.0
                        dtemp = node.get_DTemp() or 0.0
                        
                        vx_sum += vx
                        vy_sum += vy
                        fx_sum += fx
                        fy_sum += fy
                        temp_sum += temp
                        dtemp_sum += dtemp
                        valid_nodes += 1
                
                if valid_nodes > 0:
                    avg_vx = vx_sum / valid_nodes
                    avg_vy = vy_sum / valid_nodes
                    avg_fx = fx_sum / valid_nodes
                    avg_fy = fy_sum / valid_nodes
                    avg_temp = temp_sum / valid_nodes
                    avg_dtemp = dtemp_sum / valid_nodes
                    
                    element_data['Velocity X(r)'].append(avg_vx)
                    element_data['Velocity Y(z)'].append(avg_vy)
                    element_data['Total Velocity'].append(np.sqrt(avg_vx**2 + avg_vy**2))
                    element_data['Force X(r)'].append(avg_fx)
                    element_data['Force Y(z)'].append(avg_fy)
                    element_data['Total Force'].append(np.sqrt(avg_fx**2 + avg_fy**2))
                    element_data['Temperature'].append(avg_temp)
                    element_data['Temperature Rate'].append(avg_dtemp)

        for key, values in element_data.items():
            if any(v != 0.0 for v in values):
                mesh.cell_data[key] = np.array(values)
    
    def create_die_mesh(self, die):
        """Create mesh for a die"""
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